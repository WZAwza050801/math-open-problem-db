"""recompute_current_status_2026-09-30.py — 补全事件链 + 按事件链重算现行状态（零 AI）

对应 NEXT_PHASE_PLAN_2026-09-30 T15（阶段 2 的状态部分）。三个动作：

1. 补事件（V2 §3.3 流程 1-2 的完整版，幂等）：
   - proposed_at_paper：无该事件的命题从代表卡生成 1 条
   - solved_in_paper / background_known_open：挂 uid 成员卡逐张生成，
     已有 (uid, event_type, source_card_id) 的跳过
   背景：v2 迁移只回填了小部分卡事件（solved 250/3,573 张、bg 83/2,226 张），
   历史上另有脚本直接刷 status 缓存绕过事件表（1,820 个 solved 命题无事件）。

2. 重算缓存（唯一规则）：
   - 有 solved_in_paper / solved_in_literature / human_verified 事件 → solved
   - 其余 → open
   与 v2 迁移 3e 的口径完全一致；not_a_proposition 成员命题沿用旧口径标 open
   （1,900 新 + 1,990 旧同性质，不在本任务里引入新状态枚举）。

3. 对账（不悄悄覆盖）：
   - 旧命题（op-2026-006868 及以前）重算前后 status 变化逐条落清单文件
   - 命题数 = solved + open；uid 为 NULL 的 107 张人工队列卡不挂命题
   - problems / status_event 既有行不被修改，只新增

用法：python3 recompute_current_status_2026-09-30.py <db_path> [--apply]
不带 --apply 时只演练统计，不写库。
"""
import json
import os
import sqlite3
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
BATCH_ID = "2026-09-30-历史批次"
OLD_MAX = "op-2026-006868"
SOLVED_EVENTS = ("solved_in_paper", "solved_in_literature", "human_verified")


def main(db_path, apply):
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    q = con.execute

    before_counts = {t: q(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                     for t in ("problems", "canonical_problem", "status_event")}
    before_status = dict(q("SELECT status, COUNT(*) FROM canonical_problem GROUP BY status"))

    # ---------- 1. 补事件 ----------
    have_proposed = {r[0] for r in q(
        "SELECT DISTINCT canonical_uid FROM status_event WHERE event_type='proposed_at_paper'")}
    have_card_events = {tuple(r) for r in q(
        "SELECT canonical_uid, event_type, source_card_id FROM status_event "
        "WHERE source_card_id IS NOT NULL")}

    prop_events, solved_events, bg_events = [], [], []
    for uid, rep_id, rep_arxiv, rep_year in q(
            "SELECT canonical_uid, rep_card_id, origin_arxiv_id, origin_year FROM canonical_problem"):
        if uid not in have_proposed:
            prop_events.append((uid, "proposed_at_paper", rep_arxiv, rep_id, rep_year,
                                "T15 补全：代表卡（无 proposed 事件的命题）"))
    for uid, arxiv, pid, yr, pts in q(
            "SELECT canonical_uid, arxiv_id, id, pub_year, paper_time_status FROM problems "
            "WHERE canonical_uid IS NOT NULL AND canonical_uid != '' "
            "AND paper_time_status IN ('solved_in_paper','background_known_open')"):
        if (uid, pts, pid) in have_card_events:
            continue
        row = (uid, pts, arxiv, pid, yr, "T15 补全：成员卡时点状态（v2 迁移漏回填部分）")
        (solved_events if pts == "solved_in_paper" else bg_events).append(row)
    new_events = prop_events + solved_events + bg_events

    # ---------- 2. 重算缓存 ----------
    solved_uids = {r[0] for r in q(
        "SELECT DISTINCT canonical_uid FROM status_event "
        "WHERE event_type IN (?,?,?)", SOLVED_EVENTS)}
    # 补进来的 solved 事件也要算进去
    solved_uids |= {e[0] for e in solved_events}

    all_uids = [r[0] for r in q("SELECT canonical_uid FROM canonical_problem")]
    changes = []   # 旧命题前后变化清单
    new_status = {}
    for uid in all_uids:
        st = "solved" if uid in solved_uids else "open"
        new_status[uid] = st

    old_rows = q(f"SELECT canonical_uid, status FROM canonical_problem "
                 f"WHERE canonical_uid <= '{OLD_MAX}'").fetchall()
    for r in old_rows:
        if new_status[r["canonical_uid"]] != r["status"]:
            changes.append({"uid": r["canonical_uid"], "before": r["status"],
                            "after": new_status[r["canonical_uid"]]})

    after_status = {"solved": sum(1 for v in new_status.values() if v == "solved"),
                    "open": sum(1 for v in new_status.values() if v == "open")}

    # ---------- 演练输出 ----------
    print(f"[T15] 演练（{'写库' if apply else '只读'}模式）")
    print(f"[T15] 补事件：proposed {len(prop_events)} + solved {len(solved_events)} "
          f"+ bg_known {len(bg_events)} = {len(new_events)} 条新增")
    print(f"[T15] status_event {before_counts['status_event']} -> "
          f"{before_counts['status_event'] + len(new_events)}")
    print(f"[T15] status 缓存 {before_status} -> {after_status}")
    print(f"[T15] 旧命题前后变化 {len(changes)} 个（open->solved {sum(1 for c in changes if c['after']=='solved')} / 其他 {sum(1 for c in changes if c['after']!='solved')}）")
    assert after_status["solved"] + after_status["open"] == before_counts["canonical_problem"], \
        "命题数对不上"

    if not apply:
        print("[T15] 未写库。加 --apply 执行。")
        con.close()
        return

    # ---------- 写库 ----------
    con.executemany(
        "INSERT INTO status_event(canonical_uid, event_type, source_arxiv_id, "
        "source_card_id, year, note) VALUES (?,?,?,?,?,?)", new_events)
    con.executemany(
        "UPDATE canonical_problem SET status=? WHERE canonical_uid=?",
        [(st, uid) for uid, st in new_status.items()])
    con.commit()

    if changes:
        fp = os.path.join(BASE, "scratch", "status_recompute_changes_2026-09-30.json")
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(changes, f, ensure_ascii=False, indent=1)
        print(f"[T15] 变化清单已落 {fp}")

    # ---------- 写后硬校验 ----------
    after_counts = {t: q(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                    for t in ("problems", "canonical_problem", "status_event")}
    assert before_counts["problems"] == after_counts["problems"], "problems 计数变了！"
    assert before_counts["canonical_problem"] == after_counts["canonical_problem"], \
        "canonical_problem 计数变了！"
    final_status = dict(q("SELECT status, COUNT(*) FROM canonical_problem GROUP BY status"))
    assert final_status == after_status, f"写后分布与预期不符：{final_status}"
    # 幂等复算：第二遍应零新增事件、零状态变化
    assert q("SELECT COUNT(*) FROM status_event WHERE canonical_uid=? "
             "AND event_type='proposed_at_paper' AND source_card_id IS NULL AND note LIKE 'T15%'",
             ("op-2026-006869",)).fetchone()[0] <= 1
    print(f"[T15] 写库完成：integrity={q('PRAGMA integrity_check').fetchone()[0]}；"
          f"problems={after_counts['problems']} canonical={after_counts['canonical_problem']}（前后一致 ✓）")
    con.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("用法: python3 recompute_current_status_2026-09-30.py <db_path> [--apply]")
    main(sys.argv[1], "--apply" in sys.argv)
