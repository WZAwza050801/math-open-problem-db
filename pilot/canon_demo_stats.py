import sqlite3
import json

con = sqlite3.connect("db.sqlite3")

names = ["Milnor", "Poincare", "Poincaré", "Riemann hypothesis",
         "P vs NP", "Hodge", "Birch and Swinnerton-Dyer",
         "Navier-Stokes", "Yang-Mills", "Collatz", "Goldbach",
         "twin prime", "Riemann Hypothesis"]

print("=== 名猜想在 7,471 张卡中的出现次数（按 original_quote+self_contained）===")
for name in ["Milnor", "Poincar", "Riemann hypothesis", "P vs NP",
             "Hodge conjecture", "Birch", "Navier-Stokes", "Yang-Mills",
             "Collatz", "Goldbach", "twin prime"]:
    n = con.execute(
        "select count(*) from problems where "
        "original_quote like ? or self_contained like ?",
        (f"%{name}%", f"%{name}%")).fetchone()[0]
    if n:
        print(f"  {name:<22} {n:>4} 张卡提到")

print()
print("=== 同一篇论文拆出多卡的情况（重复度土壤）===")
for r in con.execute(
        "select count(*) c, sum(1) from (select arxiv_id, count(*) c"
        " from problems group by arxiv_id having c >= 5)"):
    pass
rows = con.execute(
    "select cnt, count(*) from (select arxiv_id, count(*) cnt"
    " from problems group by arxiv_id) group by cnt order by cnt").fetchall()
total_multi = sum(n for cnt, n in rows if cnt >= 2)
print("  papers_by_cards_per_paper:", rows)
print(f"  出多卡的论文数: {total_multi}")

# 示例：挑 Milnor 卡看跨论文分布
print()
print("=== 提到 Milnor 的卡分布在多少篇不同论文 ===")
n_papers = con.execute(
    "select count(distinct arxiv_id) from problems where "
    "original_quote like '%Milnor%' or self_contained like '%Milnor%'"
).fetchone()[0]
print(f"  {n_papers} 篇不同论文")
