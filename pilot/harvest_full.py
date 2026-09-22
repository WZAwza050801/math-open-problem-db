"""Full-corpus harvest wrapper: incremental, crash/proxy-flake tolerant.

Why this exists: harvest.py's arxiv_query() has no retry, and the local sandbox
proxy (tunnel) throws 502 Bad Gateway in bursts. A single harvest.py run can lose
most arXiv queries AND overwrite candidates.json with a crippled list (seen live:
run 2 kept only 1 of 10 queries). This wrapper:

  1. keeps the arXiv candidate pool in arxiv_pool.json (accumulates across runs);
  2. tracks per-query completion in queries_done.json;
  3. retries each unfinished query up to N times with backoff, skips the rest
     until the next invocation -- nothing is lost, nothing is overwritten;
  4. only when ALL queries are done does it run the same join as harvest.py
     (imported verbatim from harvest.py) and write candidates.json.

Usage:  python harvest_full.py          (repeat until it prints ALL_QUERIES_DONE)
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import harvest as H

BASE = H.BASE
POOL = BASE / "arxiv_pool.json"
DONE = BASE / "queries_done.json"


def load_json(path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def arxiv_query_paginated(q, page=200, max_total=2000):
    """arxiv_query with pagination.

    Live observation: the same query returned 304 entries once, then only
    exactly 200 on later runs -- something between arXiv and us truncates
    responses at 200 entries. Fetching page by page (start=0,200,400,...)
    until a short/empty page sidesteps the cap.
    """
    all_rows, start = [], 0
    while start < max_total:
        url = H.ARXIV_API + "?" + __import__("urllib.parse", fromlist=["urlencode"]).urlencode({
            "search_query": q, "sortBy": "relevance", "sortOrder": "descending",
            "start": start, "max_results": page,
        })
        import urllib.request as _ur
        req = _ur.Request(url, headers=H.ARXIV_UA)
        with _ur.urlopen(req, timeout=120) as r:
            xml = r.read().decode("utf-8", "replace")
        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml)
        rows = []
        for e in root.findall("atom:entry", H.ATOM_NS):
            aid = e.findtext("atom:id", default="", namespaces=H.ATOM_NS).split("/abs/")[-1]
            rows.append({
                "arxiv_id": aid.split("v")[0],
                "version": aid,
                "title": " ".join(e.findtext("atom:title", default="", namespaces=H.ATOM_NS).split()),
                "journal_ref": (e.findtext("arxiv:journal_ref", default="", namespaces=H.ATOM_NS) or "").strip(),
                "doi": (e.findtext("arxiv:doi", default="", namespaces=H.ATOM_NS) or "").strip().lower(),
                "authors": [a.findtext("atom:name", default="", namespaces=H.ATOM_NS)
                            for a in e.findall("atom:author", H.ATOM_NS)],
                "published": e.findtext("atom:published", default="", namespaces=H.ATOM_NS)[:10],
            })
        all_rows.extend(rows)
        if len(rows) < page:
            break
        start += page
        time.sleep(3)
    # dedup within query by arxiv_id, preserving order
    seen, uniq = set(), []
    for r in all_rows:
        if r["arxiv_id"] in seen:
            continue
        seen.add(r["arxiv_id"])
        uniq.append(r)
    return uniq


def main():
    retries = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    pool = load_json(POOL, {})
    done = load_json(DONE, {})

    toc = H.load_toc()

    all_queries = []
    for jkey, queries in H.ARXIV_QUERIES.items():
        for q in queries:
            all_queries.append((jkey, q))

    pending = [(j, q) for (j, q) in all_queries if done.get(f"{j}||{q}") != "ok"]
    print(f"[pool] {len(pool)} candidates cached; {len(all_queries) - len(pending)}/{len(all_queries)} queries done, {len(pending)} pending")

    for jkey, q in pending:
        key = f"{jkey}||{q}"
        full = f"{q} AND submittedDate:[{H.YEAR_FROM}01010000 TO {H.YEAR_TO}12312359]"
        ok = False
        for attempt in range(1, retries + 1):
            try:
                rows = arxiv_query_paginated(full)
            except Exception as e:
                print(f"[arxiv] {jkey} {q!r} attempt {attempt}/{retries} FAILED {type(e).__name__}: {e}", flush=True)
                time.sleep(5 * attempt)
                continue
            new = 0
            for r in rows:
                if r["arxiv_id"] not in pool:
                    pool[r["arxiv_id"]] = r
                    new += 1
            print(f"[arxiv] {jkey} {q!r} returned {len(rows)}, new {new}", flush=True)
            done[key] = "ok"
            ok = True
            break
        POOL.write_text(json.dumps(pool, ensure_ascii=False), encoding="utf-8")
        DONE.write_text(json.dumps(done, ensure_ascii=False, indent=1), encoding="utf-8")
        if not ok:
            print(f"[arxiv] {jkey} {q!r} still failing -- rerun this script later", flush=True)
        time.sleep(3)

    still = [k for k in (f"{j}||{q}" for (j, q) in all_queries) if done.get(k) != "ok"]
    if still:
        print(f"INCOMPLETE: {len(still)} queries pending -- rerun harvest_full.py")
        return

    print("ALL_QUERIES_DONE -- running join")
    # ---- identical join to harvest.main() (kept in sync deliberately)
    accepted = []
    methods = {}
    for jkey in H.JOURNALS:
        by_doi, by_title, tok_index = H.build_index(toc[jkey])
        for aid, p in pool.items():
            row, how = H.match(p, by_doi, by_title, tok_index)
            if row is None:
                continue
            if row["year"] < H.YEAR_FROM or row["year"] > H.YEAR_TO:
                continue
            accepted.append({
                "journal": jkey, "journal_name": H.JOURNALS[jkey]["name"],
                "crossref_doi": row["doi"], "crossref_title": row["title"],
                "crossref_journal": row["journal"], "pub_year": row["year"],
                "volume": row.get("volume"), "page": row.get("page"),
                "arxiv_id": aid, "arxiv_title": p["title"],
                "arxiv_journal_ref": p["journal_ref"], "arxiv_doi": p["doi"],
                "authors": p["authors"], "published": p["published"],
                "match_method": how,
            })
            methods[how.split("(")[0]] = methods.get(how.split("(")[0], 0) + 1

    rank = {"doi": 0, "title-exact": 1}
    accepted.sort(key=lambda r: (r["journal"], rank.get(r["match_method"].split("(")[0], 2), -r["pub_year"]))
    seen, uniq = set(), []
    for r in accepted:
        key = (r["journal"], r["arxiv_id"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(r)

    picked = []
    for jkey in H.JOURNALS:
        rows = [r for r in uniq if r["journal"] == jkey]
        picked.extend(rows)          # full corpus: no PER_JOURNAL cap

    print("\n=== join result (arXiv x Crossref) ===")
    for k in H.JOURNALS:
        n_toc = len(toc[k])
        n = sum(1 for r in uniq if r["journal"] == k)
        print(f"  {k:12} toc={n_toc:>5}  with-arXiv-fulltext={n:>4}  ({100.0 * n / n_toc:.1f}%)")
    print(f"  match methods: {methods}")
    print(f"  FULL CORPUS: {len(picked)}")

    H.CANDIDATES.write_text(json.dumps(picked, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {H.CANDIDATES}")


if __name__ == "__main__":
    main()
