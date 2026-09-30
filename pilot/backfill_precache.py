"""Backfill stage 2: positives list + LaTeX precache.

Reads backfill_matches.jsonl (OpenAlex abstract screening), writes
backfill_positives.json (candidates.json-compatible format), then downloads
LaTeX fulltext for every positive with an arxiv_id (reuses run_pilot
fetch_fulltext + latex_cache, idempotent).

Usage:
  python backfill_precache.py list     # build positives list, print stats
  python backfill_precache.py fetch    # build list + download LaTeX (5s gap)
"""
import json, os, sys, time

import run_pilot as R

BASE = R.BASE
MATCHES = BASE / "backfill_matches.jsonl"
POSITIVES = BASE / "backfill_positives.json"


def build_list():
    best = {}  # doi -> row, keep last non-error row per DOI
    for l in open(MATCHES, encoding="utf-8"):
        if not l.strip():
            continue
        r = json.loads(l)
        if r.get("error") and r["doi"] in best:
            continue
        best[r["doi"]] = r
    rows = list(best.values())
    pos = [r for r in rows if r.get("marker")]
    no_arxiv = [r for r in pos if not r.get("arxiv_id")]
    out = []
    for r in pos:
        out.append({
            "arxiv_id": r.get("arxiv_id"),
            "crossref_doi": r["doi"],
            "title": r["title"],
            "journal": r["journal"],
            "year": r["year"],
            "marker_hits": r.get("marker_hits", []),
            "source": "backfill_v2",
        })
    POSITIVES.write_text(json.dumps(out, ensure_ascii=False, indent=1),
                         encoding="utf-8")
    print(f"[positives] screened={len(rows)} marker_pos={len(pos)} "
          f"with_arxiv={len(out)} no_arxiv={len(no_arxiv)}", flush=True)
    if no_arxiv:
        print("[positives] no-arxiv examples (first 5):")
        for r in no_arxiv[:5]:
            print(f"  {r['doi']}  {r['title'][:70]}", flush=True)
    return out


def fetch_all():
    # load as-is; do NOT rebuild here — build_list() would wipe merged ids
    list_path = os.environ.get("FETCH_LIST")
    if list_path:
        pos = json.load(open(list_path, encoding="utf-8"))
        print(f"[fetch] FETCH_LIST={list_path} n={len(pos)}", flush=True)
    else:
        pos = json.load(open(POSITIVES, encoding="utf-8"))
    ids = [p["arxiv_id"] for p in pos if p.get("arxiv_id")]
    print(f"[fetch] positives={len(pos)} with_valid_id={len(ids)}", flush=True)
    ok, failed = 0, []
    t0 = time.time()
    for i, aid in enumerate(ids, 1):
        try:
            txt, src = R.fetch_fulltext(aid)
            ok += 1
            print(f"[{i}/{len(ids)}] {aid} {src} {len(txt)} chars "
                  f"ok={ok} fail={len(failed)} "
                  f"elapsed={int(time.time() - t0)}s", flush=True)
        except Exception as e:
            failed.append(aid)
            print(f"[{i}/{len(ids)}] {aid} FAIL {type(e).__name__}: "
                  f"{str(e)[:80]} ok={ok} fail={len(failed)}", flush=True)
            time.sleep(10)
    print(f"[precache-backfill] DONE ok={ok} failed={len(failed)} "
          f"elapsed={int((time.time() - t0) / 60)}min", flush=True)
    if failed:
        (BASE / "precache_backfill_failed.json").write_text(
            json.dumps(failed), encoding="utf-8")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "fetch":
        fetch_all()
    else:
        build_list()
