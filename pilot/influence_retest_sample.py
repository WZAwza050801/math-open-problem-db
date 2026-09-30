"""influence_retest_sample.py — T20：从 27,689 对全量池不分层抽 300 对

对应 NEXT_PHASE_PLAN_2026-09-30 §3.6 / T20 与 EXPERIMENT_REGISTRY 仲裁规则第 8 条。
抽样来源 = 全量粗筛池（sim>=0.60 或（有引用句且 sim>=0.55）），均匀随机、不分层，
覆盖低相似度、无引用句等各形态（计划书 §11.4 补字）。
输出格式与 influence_calibration_input.jsonl 完全一致（供 influence_verdict.py 直接吃，
JUDGE_INPUT 环境变量指向本文件即可），pair_id 前缀 ret- 以免与试判 cal- 撞 checkpoint。

用法：python influence_retest_sample.py [n=300]
"""
import json
import os
import random
import sqlite3
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SIM_FILE = os.path.join(BASE, "influence_edge_similarity.jsonl")
ENRICH = os.path.join(BASE, "citation_enrich_citing_papers.jsonl")
OUT = os.path.join(BASE, "influence_calibration", "influence_retest_input.jsonl")

random.seed(20260930)


def rule_B(r):
    s = r.get("max_sim")
    return (s is not None and s >= 0.60) or (s is not None and s >= 0.55 and r["has_contexts"])


def main(n=300):
    pool = []
    stats = {"sim_ge_060": 0, "ctx_055_060": 0}
    for line in open(SIM_FILE, encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line)
        if not rule_B(r):
            continue
        pool.append(r)
        s = r["max_sim"]
        if s >= 0.60:
            stats["sim_ge_060"] += 1
        else:
            stats["ctx_055_060"] += 1
    print(f"[T20] 全量池 {len(pool)} 对（sim>=0.60: {stats['sim_ge_060']}，"
          f"ctx&0.55-0.60: {stats['ctx_055_060']}）")
    assert len(pool) == 27689, f"池子数对不上 27,689：{len(pool)}"

    # 卡片陈述：从生产库导出的本地 canon_db（与试判同源）
    con = sqlite3.connect(os.path.join(BASE, "..", "canon_prototype", "canon_db.sqlite3"))
    cards = {r[0]: (r[1] or "", r[2] or "")
             for r in con.execute("SELECT id, self_contained, paper_time_status FROM problems")}
    con.close()

    meta = {}
    for line in open(ENRICH, encoding="utf-8"):
        if not line.strip():
            continue
        rec = json.loads(line)
        for e in rec["edges"]:
            meta[(rec["our_doi"], e.get("s2_paper_id"))] = e

    random.shuffle(pool)
    out = open(OUT, "w", encoding="utf-8")
    picked = 0
    no_meta = no_card = 0
    for r in pool:
        if picked >= n:
            break
        e = meta.get((r["our_doi"], r["s2_paper_id"]))
        if not e:
            no_meta += 1
            continue
        stmt, status = cards.get(r["best_card_id"], ("", ""))
        if not stmt:
            no_card += 1
            continue
        picked += 1
        out.write(json.dumps({
            "pair_id": f"ret-{picked:04d}",
            "stratum": "unstratified",
            "our_doi": r["our_doi"], "s2_paper_id": r["s2_paper_id"],
            "card_id": r["best_card_id"], "card_status": status,
            "card_statement": stmt[:1200],
            "citing_title": (e.get("title") or "")[:300],
            "citing_abstract": (e.get("abstract") or "")[:600],
            "contexts": [c[:400] for c in (e.get("contexts") or [])[:3]],
            "max_sim": r["max_sim"], "intents": r["intents"],
            "is_influential": r["is_influential"],
        }, ensure_ascii=False) + "\n")
    out.close()
    print(f"[T20] 抽出 {picked} 对 -> {OUT}（缺引用元数据 {no_meta}，缺卡片陈述 {no_card}）")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 300)
