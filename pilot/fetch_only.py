"""Fetch-only dry run: measure channel success for every candidate before paying for LLM calls.

Fills latex_cache/ so the real pilot run hits cache, and prints the chars/kind for
each paper so coverage of the corpus is known up front.
"""
import json
import time
from pathlib import Path

import run_pilot as rp

BASE = Path(__file__).resolve().parent


def main():
    cands = json.loads((BASE / "candidates.json").read_text(encoding="utf-8"))
    ok, bad = [], []
    t0 = time.time()
    for i, c in enumerate(cands, 1):
        aid = c["arxiv_id"]
        t = time.time()
        try:
            text, kind = rp.fetch_fulltext(aid)
        except Exception as e:
            text, kind = None, f"{type(e).__name__}: {e}"
        if text:
            ok.append((aid, c["journal"], kind, len(text)))
            print(f"[{i:2}/{len(cands)}] OK   {aid:11} {c['journal']:12} {kind:14} {len(text):>9,} chars "
                  f"({time.time()-t:.1f}s)  {c['crossref_title'][:46]}")
        else:
            bad.append((aid, c["journal"], kind))
            print(f"[{i:2}/{len(cands)}] FAIL {aid:11} {c['journal']:12} {kind}")

    print(f"\n=== channel report ({time.time()-t0:.0f}s) ===")
    from collections import Counter
    print("  succeeded:", len(ok), "/", len(cands))
    print("  by channel:", Counter(k for _, _, k, _ in ok))
    print("  failures :", len(bad))
    for a, j, k in bad:
        print(f"    {a} [{j}] {k}")
    if ok:
        sizes = sorted(n for *_, n in ok)
        print(f"  chars: min={sizes[0]:,} median={sizes[len(sizes)//2]:,} max={sizes[-1]:,}")
    (BASE / "fetch_report.json").write_text(json.dumps(
        {"ok": ok, "failed": bad}, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
