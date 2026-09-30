"""Backfill screener v2: OpenAlex-by-DOI.
For each unscreened paper (Crossref TOC minus 823 candidates), fetch OpenAlex
work record, reconstruct abstract from inverted index, detect conjecture/open-
problem markers. Also extract arxiv_id from locations for later LaTeX download.

Usage: python match_backfill.py [limit]
Output: backfill_matches.jsonl (checkpoint-resume, one line per paper)
Rate: ~2.5 req/s (OpenAlex polite pool, mailto in UA). ~25 min for 3,614.
"""
import json, os, re, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "backfill_matches.jsonl")
MARKERS = re.compile(
    r"\bconjectures?\b|\bopen (problems?|questions?)\b|\bwe (ask|pose)\b"
    r"|\bfamous (problem|question)s?\b|\bunsolved\b", re.I)
ARXIV_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/([^\s/?#]+)", re.I)

handler = urllib.request.ProxyHandler({})
opener = urllib.request.build_opener(handler)
opener.addheaders = [("User-Agent",
                      "open-problem-db/0.1 (mailto:3116809059@qq.com)")]

toc = json.load(open(os.path.join(BASE, "crossref_toc.json"), encoding="utf-8"))
cand = json.load(open(os.path.join(BASE, "candidates.json"), encoding="utf-8"))
cand_dois = {(c.get("crossref_doi") or "").strip().lower() for c in cand}

all_p = []
for j, items in toc.items():
    for t in items:
        doi = (t.get("doi") or "").strip().lower()
        if doi and doi not in cand_dois:
            all_p.append({"journal": j, "doi": doi,
                          "title": re.sub(r"\s+", " ", t.get("title") or ""),
                          "year": t.get("year")})

done = {}
if os.path.exists(OUT):
    for line in open(OUT, encoding="utf-8"):
        if line.strip():
            try:
                r = json.loads(line)
                if not r.get("error"):
                    done[r["doi"]] = r
            except Exception:
                pass
todo = [p for p in all_p if p["doi"] not in done]
limit = int(sys.argv[1]) if len(sys.argv) > 1 else len(todo)
todo = todo[:limit]
print(f"[backfill] total={len(all_p)} screened={len(done)} todo={len(todo)}",
      flush=True)


def fetch_openalex(doi):
    """Return (status, work_dict_or_None). status in ok/not_found/error."""
    url = f"https://api.openalex.org/works/doi:{doi}?mailto=3116809059@qq.com"
    try:
        with opener.open(url, timeout=30) as r:
            return "ok", json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "not_found", None
        return "error", str(e)[:150]
    except Exception as e:
        return "error", f"{type(e).__name__}: {str(e)[:130]}"


def reconstruct_abstract(inv):
    if not inv:
        return ""
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


def extract_arxiv_id(w):
    ids = []
    for loc in w.get("locations") or []:
        for u in (loc.get("landing_page_url"), loc.get("pdf_url")):
            if u:
                m = ARXIV_RE.search(u)
                if m:
                    ids.append(m.group(1))
    ids = [i if i.count("v") == 0 or not i[-1].isdigit() or "v" not in i
           else i.split("v")[0] for i in set(ids)]
    # strip version suffix
    ids = [re.sub(r"v\d+$", "", i) for i in set(ids)]
    return sorted(ids)[0] if ids else None


WORKERS = 6
flock = __import__("threading").Lock()
t0 = time.time()
stats = {"i": 0, "hits": 0, "nf": 0, "err": 0, "has_abs": 0}


def process(p):
    rec = dict(p, abstract="", arxiv_id=None, marker=False,
               marker_hits=[], status="", ts=datetime.now().isoformat(
                   timespec="seconds"))
    status, data = fetch_openalex(p["doi"])
    rec["status"] = status
    if status == "ok":
        abs_txt = reconstruct_abstract(data.get("abstract_inverted_index"))
        rec["abstract"] = abs_txt
        rec["arxiv_id"] = extract_arxiv_id(data)
        text = (p["title"] or "") + " || " + abs_txt
        ms = [m.group(0).lower() for m in MARKERS.finditer(text)]
        rec["marker"] = bool(ms)
        rec["marker_hits"] = sorted(set(ms))
    elif status == "not_found":
        rec["status"] = "not_found"
    else:
        rec["error"] = str(data)
        rec["status"] = "error"
    with flock:
        with open(OUT, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        stats["i"] += 1
        if status == "ok":
            if rec["marker"]:
                stats["hits"] += 1
            if rec["abstract"]:
                stats["has_abs"] += 1
        elif status == "not_found":
            stats["nf"] += 1
        else:
            stats["err"] += 1
        i = stats["i"]
        if i % 200 == 0:
            el = time.time() - t0
            eta = el / i * (len(todo) - i) / 60
            print(f"[{i}/{len(todo)}] hits={stats['hits']} "
                  f"not_found={stats['nf']} err={stats['err']} "
                  f"eta={eta:.0f}min", flush=True)
    return rec


with ThreadPoolExecutor(max_workers=WORKERS) as ex:
    list(ex.map(process, todo))

print(f"[backfill] DONE todo={len(todo)} marker_hits={stats['hits']} "
      f"not_found={stats['nf']} errors={stats['err']} "
      f"has_abstract={stats['has_abs']} "
      f"elapsed={(time.time() - t0) / 60:.0f}min", flush=True)
