"""Hook citations.jsonl into the server DB (idempotent).

Creates:
  citations table:  (cited_doi, citing_doi, citing_year, citing_month, fetched_at)
  paper_cite_stats: (arxiv_id, crossref_doi, n_total, n_2021_2026, latest_citing)

Usage (server):  python3 hook_citations.py
Idempotent: tables are dropped & rebuilt on each run.
"""

import json
import os
import sqlite3
import time

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "db.sqlite3")
SRC = os.path.join(BASE, "citations.jsonl")


def main():
    t0 = time.time()
    con = sqlite3.connect(DB)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA busy_timeout=60000")

    con.execute("DROP TABLE IF EXISTS citations")
    con.execute("DROP TABLE IF EXISTS paper_cite_stats")
    con.execute(
        "CREATE TABLE citations ("
        " cited_doi TEXT NOT NULL, citing_doi TEXT, citing_year INTEGER,"
        " citing_month TEXT, fetched_at TEXT)")
    con.execute(
        "CREATE INDEX idx_cit_cited ON citations(cited_doi)")
    con.execute(
        "CREATE INDEX idx_cit_citing ON citations(citing_doi)")

    rows, dois_seen, parse_errs = [], set(), 0
    with open(SRC, encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except Exception:
                parse_errs += 1
                continue
            if rec.get("n_citing") is None:      # fetch error record
                continue
            dois_seen.add(rec["doi"])
            for c in rec.get("citations", []):
                # "omid:... doi:10.xxxx openalex:W..." -- extract citing doi
                cd = ""
                for tok in c.get("citing", "").split():
                    if tok.startswith("doi:"):
                        cd = tok[4:]
                        break
                creation = c.get("creation", "")  # "2025-07" or "2025-11-13"
                year = int(creation[:4]) if creation[:4].isdigit() else None
                month = creation[5:7] if len(creation) >= 7 and creation[5:7].isdigit() else None
                rows.append((rec["doi"], cd, year, month, rec.get("fetched_at", "")))

    con.executemany("INSERT INTO citations VALUES (?,?,?,?,?)", rows)
    con.commit()

    # paper-level stats, joined via papers.crossref_doi
    con.execute(
        "CREATE TABLE paper_cite_stats AS "
        "SELECT p.arxiv_id, p.crossref_doi, "
        " COUNT(c.citing_doi) AS n_total, "
        " SUM(CASE WHEN c.citing_year >= 2021 THEN 1 ELSE 0 END) AS n_2021_2026, "
        " MAX(c.citing_year) AS latest_citing "
        "FROM papers p LEFT JOIN citations c ON c.cited_doi = p.crossref_doi "
        "GROUP BY p.arxiv_id")
    con.commit()

    n = con.execute("SELECT COUNT(*) FROM citations").fetchone()[0]
    hooked = con.execute(
        "SELECT COUNT(*) FROM paper_cite_stats WHERE n_total > 0").fetchone()[0]
    tot = con.execute("SELECT COUNT(*) FROM paper_cite_stats").fetchone()[0]
    print(f"[hook] citation rows: {n} (from {len(dois_seen)} DOIs, {parse_errs} parse errors)")
    print(f"[hook] papers with citations: {hooked}/{tot}")
    top = con.execute(
        "SELECT arxiv_id, n_total, n_2021_2026, latest_citing "
        "FROM paper_cite_stats ORDER BY n_total DESC LIMIT 8").fetchall()
    print("[hook] most-cited:")
    for r in top:
        print(f"   {r[0]:<14} total={r[1]:<5} 2021-26={r[2]:<5} latest={r[3]}")
    ic = con.execute("PRAGMA integrity_check").fetchone()[0]
    print(f"[hook] integrity: {ic}  elapsed={time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
