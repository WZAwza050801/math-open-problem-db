"""Asset inventory + gap detection for handover document."""
import json
import os
import sqlite3

con = sqlite3.connect("db.sqlite3")
con.row_factory = sqlite3.Row

print("=== 论文元数据缺口 ===")
n = con.execute("select count(*) from papers").fetchone()[0]
for col in ["crossref_doi", "title", "authors_json", "pub_year",
            "journal_name", "latex_chars"]:
    empty = con.execute(
        f"select count(*) from papers where {col} is null or {col}='' or {col}=0"
    ).fetchone()[0]
    print(f"  {col:<16} 缺失 {empty:>3}/{n}")

print()
print("=== 卡片字段缺口 (7,471) ===")
n_c = con.execute("select count(*) from problems").fetchone()[0]
for col in ["self_contained", "original_quote", "msc_primary",
            "difficulty_hint", "label", "content_hash"]:
    empty = con.execute(
        f"select count(*) from problems where {col} is null or {col}=''"
    ).fetchone()[0]
    print(f"  {col:<16} 缺失 {empty:>3}/{n_c}")

print()
print("=== 年份分布 ===")
for r in con.execute(
        "select (pub_year/5)*5 as bucket, count(*) from papers"
        " group by bucket order by bucket"):
    print(f"  {r[0]}-{r[0]+4}: {r[1]}")

print()
print("=== 状态字段覆盖 ===")
print("  paper_time_status:", con.execute(
    "select coalesce(paper_time_status,'NULL'), count(*) from problems"
    " group by 1 order by 2 desc").fetchall())
print("  current_status:", con.execute(
    "select coalesce(current_status,'NULL'), count(*) from problems"
    " group by 1 order by 2 desc limit 5").fetchall())
print("  flag_for_human 非空:", con.execute(
    "select count(*) from problems where flag_for_human is not null"
    " and flag_for_human!=''").fetchone()[0])

print()
print("=== 引用网络覆盖 ===")
if os.path.exists("citations.jsonl"):
    dois_db = set(r[0] for r in con.execute(
        "select distinct crossref_doi from papers"
        " where crossref_doi is not null and crossref_doi!=''"))
    n_cit = cited = 0
    cit_dois = set()
    with open("citations.jsonl", encoding="utf-8") as f:
        for line in f:
            n_cit += 1
            try:
                rec = json.loads(line)
                cit_dois.add(rec.get("doi"))
            except Exception:
                pass
    print(f"  citations.jsonl: {n_cit} 条记录")
    print(f"  库内有 DOI 的论文: {len(dois_db)}")
    print(f"  已抓到引用的 DOI: {len([d for d in cit_dois if d])}")

print()
print("=== latex_cache ===")
n_tex = len([f for f in os.listdir("latex_cache") if f.endswith(".tex")])
print(f"  .tex files: {n_tex}")
