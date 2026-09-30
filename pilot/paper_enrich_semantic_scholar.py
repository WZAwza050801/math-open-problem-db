"""Resolve arxiv_id (and optionally abstract) for backfill rows via Semantic
Scholar, by DOI. Fills gaps OpenAlex left: positives without arxiv_id, and
no-abstract papers (abstract rescue attempt).

Usage:
  python paper_enrich_semantic_scholar.py ids       # resolve arxiv_id for marker-positive rows
  python paper_enrich_semantic_scholar.py abstracts # attempt abstract rescue for no-abstract rows
Checkpoint: paper_enrich_semantic_scholar.jsonl
"""
import json, os, sys, time, urllib.request
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
MATCHES = os.path.join(BASE, "backfill_matches.jsonl")
OUT = os.path.join(BASE, "paper_enrich_semantic_scholar.jsonl")
POSITIVE_FN = os.path.join(BASE, "backfill_positives.json")

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
opener.addheaders = [("User-Agent", "opb/0.1 (mailto:3116809059@qq.com)")]


def load_unique():
    best = {}
    for l in open(MATCHES, encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            if r.get("error") and r["doi"] in best:
                continue
            best[r["doi"]] = r
    return best


def s2_fetch(doi, fields="title,externalIds,abstract"):
    url = (f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
           f"?fields={fields}")
    for attempt in range(3):
        try:
            with opener.open(url, timeout=25) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code == 429:  # rate limit
                time.sleep(10 * (attempt + 1))
                continue
            raise
        except Exception:
            if attempt == 2:
                raise
            time.sleep(5)
    return None


def main(mode):
    best = load_unique()
    done = {}
    if os.path.exists(OUT):
        for l in open(OUT, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                done[r["doi"]] = r
    if mode == "ids":
        # positives still lacking a valid arxiv_id (positives_no_id.json)
        todo = json.load(open(POSITIVE_FN.replace(
            "backfill_positives", "positives_no_id"), encoding="utf-8"))
    else:
        todo = [r for r in best.values()
                if not r.get("marker") and not r.get("abstract")]
    todo = [dict(r, doi=r.get("doi") or r.get("crossref_doi"))
            for r in todo]
    todo = [r for r in todo if r["doi"] not in done]
    print(f"[s2] mode={mode} todo={len(todo)}", flush=True)

    got_id = got_abs = miss = err = 0
    t0 = time.time()
    for i, r in enumerate(todo, 1):
        rec = {"doi": r["doi"], "mode": mode,
               "ts": datetime.now().isoformat(timespec="seconds")}
        try:
            p = s2_fetch(r["doi"])
            if p is None:
                miss += 1
                rec["status"] = "not_found"
            else:
                rec["status"] = "ok"
                aid = (p.get("externalIds") or {}).get("ArXiv")
                ab = p.get("abstract") or ""
                if aid:
                    rec["arxiv_id"] = aid
                    got_id += 1
                if ab:
                    rec["abstract"] = ab
                    got_abs += 1
                if not aid and not ab:
                    miss += 1
        except Exception as e:
            err += 1
            rec["status"] = "error"
            rec["error"] = f"{type(e).__name__}: {str(e)[:100]}"
        with open(OUT, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        time.sleep(1.2)  # S2 unauth politeness ~100 req / 2min
        if i % 50 == 0:
            el = time.time() - t0
            eta = el / i * (len(todo) - i) / 60
            print(f"[{i}/{len(todo)}] arxiv_id={got_id} abs={got_abs} "
                  f"miss={miss} err={err} eta={eta:.0f}min", flush=True)
    print(f"[s2] DONE mode={mode} todo={len(todo)} arxiv_id={got_id} "
          f"abstract={got_abs} miss={miss} err={err} "
          f"elapsed={(time.time() - t0) / 60:.0f}min", flush=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ids")
