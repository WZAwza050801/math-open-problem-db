"""Final archive verification for the extraction campaign.

Checks db integrity, prints final counts, writes a fresh snapshot
to backups/ and exports all cards to JSONL.
"""
import json
import shutil
import sqlite3
from datetime import datetime

STAMP = datetime.now().strftime("%Y-%m-%d_%H%M")

con = sqlite3.connect("db.sqlite3")
con.row_factory = sqlite3.Row

# 1. integrity check
ic = con.execute("PRAGMA integrity_check").fetchone()[0]
print("integrity_check:", ic)

# 2. final counts
n_papers = con.execute("select count(*) from papers").fetchone()[0]
n_cards = con.execute("select count(*) from problems").fetchone()[0]
n_ex = con.execute(
    "select count(*) from papers where fetch_status='extracted'").fetchone()[0]
n_nf = con.execute(
    "select count(*) from papers where fetch_status='no_fulltext'").fetchone()[0]
print(f"papers={n_papers} extracted={n_ex} no_fulltext={n_nf} cards={n_cards}")

# per-journal breakdown
for r in con.execute(
        "select journal, count(*) from papers where fetch_status='extracted'"
        " group by journal order by 2 desc"):
    print("  extracted", tuple(r))

# orphan check: cards pointing to non-existent papers
orph = con.execute(
    "select count(*) from problems p left join papers a"
    " on p.arxiv_id=a.arxiv_id where a.arxiv_id is null").fetchone()[0]
print("orphan cards:", orph)

if ic != "ok":
    raise SystemExit("INTEGRITY CHECK FAILED - aborting backup")

# 3. snapshot backup
dst = f"backups/db_final_{STAMP}.sqlite3"
con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
con.close()
shutil.copy2("db.sqlite3", dst)
print("snapshot ->", dst)

# 4. full JSONL export of cards (joined with paper metadata)
con = sqlite3.connect("db.sqlite3")
con.row_factory = sqlite3.Row
out = f"exports/cards_final_{STAMP}.jsonl"
n = 0
with open(out, "w", encoding="utf-8", newline="\n") as f:
    for r in con.execute(
            "select p.id, p.arxiv_id, p.journal, p.pub_year,"
            " p.original_quote, p.quote_location, p.self_contained,"
            " p.label, p.label_rationale, p.msc_primary,"
            " p.msc_secondary_json, p.difficulty_hint, p.content_hash,"
            " p.paper_time_status, p.related_note,"
            " a.title, a.authors_json, a.crossref_doi"
            " from problems p left join papers a on p.arxiv_id=a.arxiv_id"):
        f.write(json.dumps(dict(r), ensure_ascii=False) + "\n")
        n += 1
print(f"cards exported -> {out} ({n} lines)")
