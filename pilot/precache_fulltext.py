"""Pre-cache LaTeX fulltext for every candidate, NO API calls, zero cost.

Idempotent: fetch_fulltext() checks latex_cache/ first, so re-running after a
crash or proxy outage only downloads what is still missing.

Usage:  python precache_fulltext.py
Env:    ARXIV_GAP (default 5s, arXiv politeness), PRECACHE_ATTEMPTS (default 3)
"""
from __future__ import annotations

import json
import sys
import time
import traceback

import run_pilot as R


def main():
    cands = json.loads(R.CANDIDATES_JSON.read_text(encoding="utf-8"))
    ids = [c["arxiv_id"] for c in cands]
    attempts = int(R.os.environ.get("PRECACHE_ATTEMPTS", "3"))
    print(f"[precache] {len(ids)} papers, gap={R.ARXIV_GAP}s, attempts={attempts}", flush=True)

    ok, failed = {}, []
    t0 = time.time()
    for i, aid in enumerate(ids, 1):
        got = None
        for attempt in range(1, attempts + 1):
            try:
                txt, src = R.fetch_fulltext(aid)
                got = (src, len(txt))
                break
            except Exception as e:
                print(f"  [{i}/{len(ids)}] {aid} attempt {attempt}/{attempts} {type(e).__name__}: {e}", flush=True)
                time.sleep(10 * attempt)
        if got:
            ok[aid] = got
            print(f"[{i}/{len(ids)}] {aid} {got[0]} {got[1]} chars  ok={len(ok)} fail={len(failed)} "
                  f"elapsed={int(time.time() - t0)}s", flush=True)
        else:
            failed.append(aid)
            print(f"[{i}/{len(ids)}] {aid} FAILED after {attempts} attempts  ok={len(ok)}", flush=True)

    print("\n=== precache summary ===", flush=True)
    print(f"ok={len(ok)}  failed={len(failed)}  elapsed={int(time.time() - t0)}s", flush=True)
    if failed:
        print("failed ids:", " ".join(failed), flush=True)
        (R.BASE / "precache_failed.json").write_text(json.dumps(failed), encoding="utf-8")
    else:
        print("ALL_CACHED", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
