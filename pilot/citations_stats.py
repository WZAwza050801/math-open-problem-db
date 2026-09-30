import json, statistics as st
from pathlib import Path

BASE = Path(__file__).resolve().parent
cands = {c["crossref_doi"]: c for c in json.load(open(BASE/"candidates.json", encoding="utf-8")) if c.get("crossref_doi")}
recs = [json.loads(l) for l in open(BASE/"citations.jsonl", encoding="utf-8")]

data = []
for r in recs:
    c = cands.get(r["doi"])
    if not c:
        continue
    yrs = [int(str(x.get("creation") or "0")[:4]) for x in r["citations"]]
    age = max(2026 - c["pub_year"], 1)
    data.append({"doi": r["doi"], "j": c["journal"], "y": c["pub_year"], "n": r["n_citing"],
                 "age": age, "capy": r["n_citing"]/age, "yrs": yrs})

title_of = {c["crossref_doi"]: c["crossref_title"] for c in cands.values()}

print("== 覆盖 ==")
print(f"{len(data)} 篇有DOI, 有被引 {sum(1 for d in data if d['n']>0)}, 总被引 {sum(d['n'] for d in data):,}")

print("\n== 按期刊（中位/平均被引, 中位被引/年） ==")
for j in ("annals", "inventiones", "jams", "acta", "ihes"):
    g = [d for d in data if d["j"] == j]
    print(f"{j:12s} n={len(g):3d}  med={st.median(d['n'] for d in g):6.0f}  "
          f"mean={st.mean(d['n'] for d in g):7.1f}  med/yr={st.median(d['capy'] for d in g):5.2f}")

print("\n== 按发表年份段（中位被引 / p90） ==")
for b in (2000, 2005, 2010, 2015, 2020):
    g = [d for d in data if b <= d["y"] < b + 5]
    if g:
        print(f"{b}-{b+4}: n={len(g):3d}  med={st.median(d['n'] for d in g):6.0f}  "
              f"p90={sorted(d['n'] for d in g)[int(len(g)*0.9)]:6.0f}")

print("\n== 被引 Top 12 ==")
for d in sorted(data, key=lambda x: -x["n"])[:12]:
    print(f"{d['n']:6d}  {d['j']:12s} {d['y']}  {title_of[d['doi']][:70]}")

print("\n== 近期高热（2020+ 发表, 被引/年 Top 8） ==")
recent = sorted([d for d in data if d["y"] >= 2020], key=lambda x: -x["capy"])[:8]
for d in recent:
    print(f"{d['capy']:6.1f}/yr  (tot {d['n']:4d})  {d['j']:12s} {d['y']}  {title_of[d['doi']][:60]}")

print("\n== 被引的年度分布示例（Top1 论文） ==")
t1 = sorted(data, key=lambda x: -x["n"])[0]
cnt = {}
for y in t1["yrs"]:
    if y:
        cnt[y] = cnt.get(y, 0) + 1
print(f"{title_of[t1['doi']][:60]} ({t1['y']})")
for y in sorted(cnt):
    print(f"  {y}: {'#' * min(cnt[y], 60)} {cnt[y]}")
