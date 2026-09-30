"""List the 32 no-fulltext papers (PDF scan-tail candidates). Server-side."""
import sqlite3

con = sqlite3.connect("db.sqlite3")
rows = con.execute(
    "SELECT arxiv_id, journal, pub_year, source_kind, fetch_status, title "
    "FROM papers WHERE fetch_status='no_fulltext' OR source_kind LIKE '%pdf%' "
    "ORDER BY pub_year, journal").fetchall()
print(len(rows), "papers without TeX fulltext:")
for r in rows:
    kind = r[3] or "?"
    status = r[4] or "?"
    print(f"  {r[0]:<16} {r[1] or '?':<12} {r[2]}  kind={kind:<10} status={status:<12} {(r[5] or '')[:45]}")
