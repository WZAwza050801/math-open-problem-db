"""One-glance status of the pilot. Read-only, safe to run while the pipeline is running.

Usage:  python status.py
"""
from __future__ import annotations

import json
import sqlite3
import time
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent
DB = BASE / "db.sqlite3"
CAND = BASE / "candidates.json"

PENDING_STATES = ("pending", "extract_failed", "fulltext_failed", "no_fulltext", "crashed")


def main():
    if not CAND.exists():
        print("no candidates.json -- run harvest.py first")
        return
    cands = json.loads(CAND.read_text(encoding="utf-8"))
    by_id = {c["arxiv_id"]: c for c in cands}

    if not DB.exists():
        print(f"candidates.json: {len(cands)} papers")
        print("db.sqlite3 not created yet -- nothing has been processed")
        print("\nnext: python run_pilot.py")
        return

    conn = sqlite3.connect(DB)
    papers = {r[0]: r for r in conn.execute(
        "SELECT arxiv_id, journal, fetch_status, source_kind, extract_mode, "
        "tokens_in, tokens_out, latex_chars, title FROM papers")}
    cards = conn.execute("SELECT COUNT(*) FROM problems").fetchone()[0]

    print("=" * 74)
    print("  PILOT STATUS")
    print("=" * 74)
    print(f"  candidates.json      {len(cands)} papers")
    print(f"  processed            {len(papers)}")
    print(f"  not yet attempted    {len(cands) - len(papers)}")
    print(f"  cards in db          {cards}")
    print()

    print("  ---- papers by status ----")
    for st, n in sorted(Counter(p[2] for p in papers.values()).items(), key=lambda kv: -kv[1]):
        print(f"    {st:18} {n}")
    print()

    done = [p for p in papers.values() if p[2] == "extracted"]
    if done:
        ti = sum(p[5] or 0 for p in done)
        to = sum(p[6] or 0 for p in done)
        ch = sorted(p[7] or 0 for p in done)
        print("  ---- extraction ----")
        print(f"    tokens in            {ti:,}  ({ti // len(done):,}/paper)")
        print(f"    tokens out           {to:,}  ({to // len(done):,}/paper)")
        print(f"    source chars         median {ch[len(ch) // 2]:,}  max {ch[-1]:,}")
        print(f"    extract mode         {dict(Counter(p[4] for p in done))}")
        print(f"    channel              {dict(Counter(p[3] for p in done))}")
        print()

    if cards:
        print("  ---- cards by label ----")
        for lab, n in conn.execute("SELECT label, COUNT(*) FROM problems GROUP BY 1 ORDER BY 2 DESC"):
            print(f"    {lab:20} {n:4}  ({100.0 * n / cards:.0f}%)")
        print()
        print("  ---- cards by journal ----")
        for j, n in conn.execute("SELECT journal, COUNT(*) FROM problems GROUP BY 1 ORDER BY 2 DESC"):
            print(f"    {j:14} {n:4}")
        print()

    todo = [(aid, by_id[aid]) for aid in by_id if aid not in papers]
    retry = [(aid, p) for aid, p in papers.items() if p[2] in PENDING_STATES]
    if todo or retry:
        print("  ---- to do ----")
        print(f"    never attempted      {len(todo)}")
        print(f"    failed, will retry   {len(retry)}")
        for aid, p in retry[:15]:
            print(f"      retry  {aid:11} [{p[1]:12}] {p[2]}")
        if len(retry) > 15:
            print(f"      ... and {len(retry) - 15} more")
        print()
        print("  next:  python resume.py        (or: python run_pilot.py)")
    else:
        print("  ALL CANDIDATES PROCESSED.")
        print("  next:  python make_review.py && python validate_cards.py")
    print("=" * 74)


if __name__ == "__main__":
    main()
