"""Generate the human-reviewable Markdown report from the pilot DB.

v3: the corpus is Crossref-verified, so each paper is reported with its authoritative
journal, DOI and publication year alongside the arXiv id and the join method that
linked the two.
"""
import json
import sqlite3
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent
conn = sqlite3.connect(BASE / "db.sqlite3")

ICON = {
    "real_open": "🟢", "background_open": "🔵", "method_obstruction": "🟠",
    "future_application": "⚪", "solved_in_paper": "🔴", "uncertain": "🟡",
}
MEANING = {
    "real_open": "论文自己提出的真开放问题（核心产出）",
    "background_open": "引用的著名背景开放问题",
    "method_obstruction": "方法/估计失效，但未正式提问",
    "future_application": "应用展望/品味评论（非命题）",
    "solved_in_paper": "论文内已解决",
    "uncertain": "上下文不足",
}
JORDER = ["annals", "acta", "inventiones", "jams", "ihes"]
JNAME = {
    "annals": "Annals of Mathematics", "acta": "Acta Mathematica",
    "inventiones": "Inventiones Mathematicae",
    "jams": "Journal of the American Mathematical Society",
    "ihes": "Publications Mathématiques de l'IHÉS",
}

papers = {}
for r in conn.execute(
        "SELECT arxiv_id, journal, title, crossref_doi, crossref_journal, pub_year, "
        "match_method, latex_chars, source_kind, fetch_status, extract_mode, "
        "tokens_in, tokens_out FROM papers"):
    papers[r[0]] = dict(zip(
        ["arxiv_id", "journal", "title", "doi", "cjournal", "year", "match",
         "chars", "kind", "status", "mode", "tin", "tout"], r))

ok = [p for p in papers.values() if p["status"] == "extracted"]
total = conn.execute("SELECT COUNT(*) FROM problems").fetchone()[0]
n_real = conn.execute("SELECT COUNT(*) FROM problems WHERE label='real_open'").fetchone()[0]
t_in = sum(p["tin"] or 0 for p in papers.values())
t_out = sum(p["tout"] or 0 for p in papers.values())

L = []
A = L.append
A("# 试跑报告 v3：五大刊开放问题提取（Crossref 权威语料）")
A("")
A("> 引擎：glm-5.3（GLM Coding Plan 团队版）｜全文：arXiv `/src/` LaTeX → ar5iv HTML 双通道")
A("> 采集：Crossref 按 ISSN 枚举期刊完整目录（2000–2025），再与 arXiv 按 DOI / 标题连接")
A("> 提示词：v2 六分类标签 + 双状态字段 + 条件保全 + 自包含硬化 + 符号级自检")
A("")
A(f"## 总览")
A("")
A(f"- 成功提取论文：**{len(ok)}** 篇")
A(f"- 候选问题卡：**{total}** 条（其中 `real_open` 核心产出 **{n_real}** 条）")
A(f"- 消耗 token：输入 {t_in:,} / 输出 {t_out:,}")
A("")
A("### 标签分布")
A("")
A("| 标签 | 数量 | 含义 |")
A("|------|-----:|------|")
for lab, cnt in conn.execute("SELECT label, COUNT(*) FROM problems GROUP BY label ORDER BY 2 DESC"):
    A(f"| {ICON.get(lab,'⚪')} `{lab}` | {cnt} | {MEANING.get(lab,'')} |")
A("")

A("### 分刊统计")
A("")
A("| 期刊 | 试跑提取论文 | 候选卡 | real_open |")
A("|------|-------------:|-------:|----------:|")
for j in JORDER:
    n = len([p for p in ok if p["journal"] == j])
    if not n and not conn.execute("SELECT COUNT(*) FROM problems WHERE journal=?", (j,)).fetchone()[0]:
        continue
    pc = conn.execute("SELECT COUNT(*) FROM problems WHERE journal=?", (j,)).fetchone()[0]
    rc = conn.execute("SELECT COUNT(*) FROM problems WHERE journal=? AND label='real_open'", (j,)).fetchone()[0]
    A(f"| {JNAME[j]} | {n} | {pc} | {rc} |")
A("")

A("### 抓取与提取状态")
A("")
A("| 状态 | 数量 |")
A("|------|-----:|")
for st, n in conn.execute("SELECT fetch_status, COUNT(*) FROM papers GROUP BY fetch_status ORDER BY 2 DESC"):
    A(f"| `{st}` | {n} |")
A("")
mc = Counter(p["match"] and p["match"].split("(")[0] for p in papers.values())
A("Crossref↔arXiv 连接方式：" + "，".join(f"`{k}` {v}" for k, v in mc.items()))
A("")
A("### 全文通道与提取模式")
A("")
A("| 指标 | 分布 |")
A("|------|------|")
sk = Counter(p["kind"] for p in papers.values() if p["kind"])
em = Counter(p["mode"] for p in papers.values() if p["mode"])
A(f"| 全文通道 | {'，'.join(f'{k}: {v}' for k,v in sk.items())} |")
A(f"| 提取模式 | {'，'.join(f'{k}: {v}' for k,v in em.items())} |")
A("")
A("---")
A("")
A("## 逐篇明细")
A("")
for j in JORDER:
    group = sorted([p for p in ok if p["journal"] == j], key=lambda x: -(x["year"] or 0))
    if not group:
        continue
    A(f"# {JNAME[j]}")
    A("")
    for p in group:
        a = p["arxiv_id"]
        A(f"## `{a}` — {p['title']}")
        A(f"- 权威出处：**{p['cjournal']}** {p['year']}，DOI `{p['doi']}`")
        A(f"- 连接方式：`{p['match']}`｜全文 {p['chars']:,} 字符 via `{p['kind']}`｜提取模式 `{p['mode']}`")
        A("")
        rows = conn.execute(
            "SELECT id, label, paper_time_status, current_status, msc_primary, difficulty_hint, "
            "original_quote, quote_location, self_contained, label_rationale, self_check, "
            "flag_for_human, related_note, uncertainty_notes FROM problems "
            "WHERE arxiv_id=? ORDER BY CASE label WHEN 'real_open' THEN 0 WHEN 'background_open' THEN 1 "
            "WHEN 'method_obstruction' THEN 2 WHEN 'solved_in_paper' THEN 3 ELSE 4 END, id", (a,)).fetchall()
        for (pid, label, pts, cs, msc, diff, quote, loc, sc, rat, chk, flag, rel, unc) in rows:
            A(f"### {ICON.get(label,'⚪')} `{pid}` — `{label}` | MSC {msc} | 难度 {diff}")
            A("")
            A(f"- 论文当时状态：`{pts}` → 当前状态：`{cs}`")
            A(f"- 出处：{loc}")
            A(f"- 自检：{chk}")
            A("")
            A("**原文引文**")
            A("")
            A(f"> {quote[:700]}{'…' if len(quote) > 700 else ''}")
            A("")
            A(f"**自包含改写**：{sc}")
            A("")
            A(f"**判定理由**：{rat}")
            if flag:
                A("")
                A(f"**⚠️ 人工复核标记**：{flag}")
            if rel:
                A("")
                A(f"**关联卡**：{rel}")
            if unc:
                A("")
                A(f"**存疑**：{unc}")
            A("")
        A("")

out = BASE / "exports" / "REVIEW_v3.md"
out.write_text("\n".join(L), encoding="utf-8")
print("written", out, len(L), "lines")

cols = [c[1] for c in conn.execute("PRAGMA table_info(problems)")]
rows = [dict(zip(cols, r)) for r in conn.execute("SELECT * FROM problems ORDER BY journal, id")]
jout = BASE / "exports" / "problems_v3.jsonl"
with open(jout, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("written", jout, len(rows), "rows")
