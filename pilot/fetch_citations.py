"""Fetch incoming citations for all 823 papers from OpenCitations (COCI).

Input:  candidates.json (crossref_doi field)
Output: citations.jsonl -- one line per DOI:
        {"doi": ..., "n_citing": N, "fetched_at": ..., "citations": [...]}
        DOIs with no data get n_citing=0 and citations=[] (fetched, not missing).

Design notes:
  * Resumable: DOIs already present in citations.jsonl are skipped on rerun
    (rewrite is atomic via tmp file + replace).
  * Politeness: 1.5s gap between requests; OpenCitations asks for modest rates.
  * The v2 API needs a `doi:` prefix, e.g. /index/api/v2/citations/doi:10.2307/x.
  * Zero dependencies (stdlib only), runs fine on the local Windows box --
    the server cannot reach opencitations.net anyway.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
CANDIDATES = BASE / "candidates.json"
OUT = BASE / "citations.jsonl"
GAP = 1.5
UA = {"User-Agent": "open-problem-db-pilot/0.1 (citation archive; contact: local)"}


def load_done():
    done = {}
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            try:
                rec = json.loads(line)
                done[rec["doi"]] = rec
            except Exception:
                continue
    return done


def fetch_citations(doi):
    url = f"https://opencitations.net/index/api/v2/citations/doi:{doi}"
    last = None
    for attempt in range(4):
        req = urllib.request.Request(url, headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r), None
        except urllib.error.HTTPError as e:
            if e.code == 400:
                return [], f"400-bad-id"
            last = f"HTTP {e.code}"
            if e.code in (404,):
                return [], None  # genuinely absent -> empty, not an error
            time.sleep(5 * (attempt + 1))
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
            time.sleep(5 * (attempt + 1))
    return None, last


def main():
    cands = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    dois = [c["crossref_doi"] for c in cands if c.get("crossref_doi")]
    done = load_done()
    todo = [d for d in dois if d not in done]
    print(f"[citations] total={len(dois)} done={len(done)} todo={len(todo)}", flush=True)

    t0 = time.time()
    n_ok = n_zero = n_err = 0
    for i, doi in enumerate(todo, 1):
        rows, err = fetch_citations(doi)
        if rows is None:
            n_err += 1
            rec = {"doi": doi, "error": err, "n_citing": None, "citations": []}
        else:
            rec = {
                "doi": doi,
                "n_citing": len(rows),
                "citations": rows,
                "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }
            if rows:
                n_ok += 1
            else:
                n_zero += 1
        done[doi] = rec
        # atomic rewrite every record (823 small records -- cheap, crash-safe)
        tmp = OUT.with_suffix(".jsonl.tmp")
        with tmp.open("w", encoding="utf-8") as f:
            for rec2 in done.values():
                f.write(json.dumps(rec2, ensure_ascii=False) + "\n")
        tmp.replace(OUT)
        if i % 25 == 0 or i == len(todo):
            rate = i / max(time.time() - t0, 1) * 3600
            print(f"[citations] [{i}/{len(todo)}] ok={n_ok} zero={n_zero} "
                  f"err={n_err} ({rate:,.0f}/h)", flush=True)
        time.sleep(GAP)
    print(f"[citations] DONE ok={n_ok} zero={n_zero} err={n_err}", flush=True)


if __name__ == "__main__":
    main()
