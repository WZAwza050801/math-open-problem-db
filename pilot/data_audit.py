"""Full data health audit for the server DB (zero API). Idempotent, read-only
except runs table log. Produces audit_report_YYYYMMDD.txt on server.

Run:  python3 data_audit.py
"""

import json
import os
import sqlite3
import time
from collections import Counter
from datetime import datetime

DB = "db.sqlite3"


def main():
    t0 = time.time()
    con = sqlite3.connect(DB)
    con.execute("PRAGMA busy_timeout=60000")
    L = [f"=== DATA HEALTH AUDIT {datetime.now().isoformat(timespec='seconds')} ==="]

    # 1. integrity
    ic = con.execute("PRAGMA integrity_check").fetchone()[0]
    L.append(f"\n[1] integrity_check: {ic}")

    # 2. orphan cards
    orphans = con.execute(
        "SELECT count(*) FROM problems p LEFT JOIN papers pa "
        "ON p.arxiv_id = pa.arxiv_id WHERE pa.arxiv_id IS NULL").fetchone()[0]
    n_cards = con.execute("SELECT count(*) FROM problems").fetchone()[0]
    n_papers = con.execute("SELECT count(*) FROM papers").fetchone()[0]
    L.append(f"[2] cards={n_cards} papers={n_papers} orphan_cards={orphans}")

    # 3. content_hash duplicates
    dup = con.execute(
        "SELECT content_hash, count(*) c FROM problems GROUP BY content_hash "
        "HAVING c > 1 ORDER BY c DESC LIMIT 10").fetchall()
    n_dup = con.execute(
        "SELECT count(*) FROM (SELECT content_hash FROM problems "
        "GROUP BY content_hash HAVING count(*) > 1)").fetchone()[0]
    L.append(f"[3] duplicate content_hash groups: {n_dup}")
    for h, c in dup:
        L.append(f"    {h[:24]}... x{c}")

    # 4. per-column null/empty matrix (problems)
    cols = [r[1] for r in con.execute("PRAGMA table_info(problems)")]
    L.append(f"\n[4] field quality matrix ({len(cols)} cols):")
    for c in cols:
        nulls = con.execute(
            f"SELECT count(*) FROM problems WHERE {c} IS NULL").fetchone()[0]
        empties = con.execute(
            f"SELECT count(*) FROM problems WHERE {c} = ''").fetchone()[0]
        flag = " <-- " if (nulls or empties) else ""
        L.append(f"    {c:<22} null={nulls:<5} empty={empties}{flag}")

    # 5. cross distribution label x paper_time_status x journal
    L.append("\n[5] label x paper_time_status x journal:")
    rows = con.execute(
        "SELECT pa.journal_name, p.label, p.paper_time_status, count(*) "
        "FROM problems p JOIN papers pa ON p.arxiv_id = pa.arxiv_id "
        "GROUP BY 1,2,3 ORDER BY 1,4 DESC").fetchall()
    cur_j = None
    for j, lab, pts, c in rows:
        if j != cur_j:
            L.append(f"    -- {j} --")
            cur_j = j
        L.append(f"    {str(lab):<22} {str(pts):<22} {c}")

    # 6. decade x paper_time_status (genesis-material)
    L.append("\n[6] pub_year bucket x paper_time_status (open-problem ratio trend):")
    rows = con.execute(
        "SELECT (pa.pub_year/5)*5, p.paper_time_status, count(*) FROM problems p "
        "JOIN papers pa ON p.arxiv_id=pa.arxiv_id GROUP BY 1,2 ORDER BY 1").fetchall()
    buckets = {}
    for yb, pts, c in rows:
        buckets.setdefault(yb, {})[pts] = c
    for yb in sorted(buckets):
        d = buckets[yb]
        tot = sum(d.values())
        opn = d.get("open_at_paper_time", 0) + d.get("background_known_open", 0)
        L.append(f"    {yb}s: total={tot:<5} open={opn:<5} ({opn/tot*100:.0f}%)")

    # 7. MSC distribution
    L.append("\n[7] msc_primary top 15:")
    for m, c in con.execute(
            "SELECT msc_primary, count(*) FROM problems "
            "WHERE msc_primary IS NOT NULL GROUP BY 1 ORDER BY 2 DESC LIMIT 15"):
        L.append(f"    {m:<10} {c}")

    # 8. citations summary
    try:
        n_cit = con.execute("SELECT count(*) FROM citations").fetchone()[0]
        hooked = con.execute(
            "SELECT count(*) FROM paper_cite_stats WHERE n_total > 0").fetchone()[0]
        L.append(f"\n[8] citations={n_cit}  papers_with_citations={hooked}/{n_papers}")
    except sqlite3.OperationalError:
        L.append("\n[8] citations table not present (run hook_citations.py)")

    L.append(f"\nelapsed={time.time()-t0:.0f}s")
    report = "\n".join(L)
    fn = f"audit_report_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(fn, "w", encoding="utf-8") as f:
        f.write(report)
    print(report)
    print(f"\n[audit] -> {fn}")


if __name__ == "__main__":
    main()
