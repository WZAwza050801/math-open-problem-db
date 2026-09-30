"""apply_identity_verdicts_2026-09-30.py — 增量归堆（T13）：把今晚判定应用到生产库

铁律：
  - 旧命题号（op-2026-000001..006868）一律不动——6,752 条重要性分数挂在旧号上
  - 只合并判成 same 的对；distinct/拿不准一律不并
  - 一审判 unsure 的：二审说 distinct → 保持分开（新建单独命题）；
    二审说 same/仍拿不准/失败 → 人工队列（保守：并卡必须一审就是 same）
  - same 传递闭包内部出现 distinct 边（矛盾）、或一个组件横跨 ≥2 个旧命题
    → 整组不自动并，进冲突队列 + 人工队列
  - 每张卡的每次归属变化都写 merge_log；全程单事务，跑前对账跑后核验

对账公式（计划书阶段 1 验收）：并入卡数 M + 新建命题成员数 N + 人工队列卡数 H = 6,424

用法：python3 apply_identity_verdicts_2026-09-30.py <db_path> [--commit]
  不带 --commit 只打印方案不写库；带 --commit 真写。
"""
import json
import os
import sys
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.join(BASE, "identity_candidates_2026-09-30.jsonl")
BATCH = "identity-batch-2026-09-30"
ACTOR = "apply_identity_verdicts_2026-09-30"

NEW_UID_START = 6869  # 生产库现最大 op-2026-006868


def load_verdicts(con):
    """每对取终态判定：优先 same/distinct/unsure，同级取最新时间戳。"""
    best = {}
    for a, b, v, at in con.execute(
            "SELECT a_id, b_id, verdict, judged_at FROM canon_verdicts"):
        key = (a, b)
        rank = {"same": 3, "distinct": 3, "unsure": 2, "parse_fail": 1}[v]
        if key not in best or (rank, at) > best[key][0]:
            best[key] = ((rank, at), v)
    return {k: v[1] for k, v in best.items()}


def load_second(con):
    best = {}
    for a, b, v, at in con.execute(
            "SELECT a_id, b_id, verdict, judged_at FROM canon_verdicts_2nd"):
        key = (a, b)
        if key not in best or at > best[key][0]:
            best[key] = (at, v)
    return {k: v[1] for k, v in best.items()}


class UF:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[self.p[x]]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def main(db_path, commit):
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA busy_timeout=60000")
    con.isolation_level = None  # 手动事务
    verdicts = load_verdicts(con)
    second = load_second(con)

    pairs = [json.loads(l) for l in open(CAND, encoding="utf-8")]
    cur_uid = dict(con.execute(
        "SELECT id, canonical_uid FROM problems WHERE id NOT LIKE 'ext-%'"))
    card_arxiv = dict(con.execute(
        "SELECT id, arxiv_id FROM problems WHERE id NOT LIKE 'ext-%'"))
    unclustered_before = sum(1 for u in cur_uid.values() if not u)
    print(f"[对账] 悬空卡（跑前）: {unclustered_before}")

    uf = UF()
    same_edges, distinct_edges, unsure_pairs = [], [], []
    for p in pairs:
        key = (p["a_id"], p["b_id"])
        v = verdicts.get(key, "missing")
        if v == "same":
            same_edges.append(key)
            uf.union(*key)
        elif v == "distinct":
            distinct_edges.append(key)
        elif v == "unsure":
            unsure_pairs.append(key)
        else:
            print(f"  [警告] 对 {key} 无终态判定，按拿不准处理")
            unsure_pairs.append(key)

    comps = defaultdict(set)
    for a, b in same_edges:
        comps[uf.find(a)].update((a, b))

    # 组件分类
    merge_into, new_clusters, human_cards = [], [], set()
    conflict_notes = []
    for root, members in comps.items():
        uids = {cur_uid.get(m) for m in members} - {None, ""}
        # 矛盾检测：distinct 边两端落在同一 same 组件里
        has_contra = any(uf.find(a) == root and uf.find(b) == root
                         for a, b in distinct_edges)
        if len(uids) >= 2:
            conflict_notes.append(
                f"same 传递闭包横跨多个旧命题 {sorted(uids)}：{' '.join(sorted(members))}")
            human_cards.update(m for m in members if not cur_uid.get(m))
            continue
        if has_contra:
            conflict_notes.append(
                f"组件内同时有 same 与 distinct 边：{' '.join(sorted(members))}")
            human_cards.update(m for m in members if not cur_uid.get(m))
            continue
        if len(uids) == 1:
            uid = uids.pop()
            fresh = sorted(m for m in members if not cur_uid.get(m))
            if fresh:
                merge_into.append((uid, fresh))
        else:
            new_clusters.append(sorted(members))

    # 剩余悬空卡：先算已被 same 组件覆盖的集合
    handled = set()
    for _, fresh in merge_into:
        handled.update(fresh)
    for members in new_clusters:
        handled.update(members)
    all_unclustered = {c for c, u in cur_uid.items() if not u}

    # unsure 对的处置（一审不是 same，绝不自动并；已被 same 组件收编的卡跳过）
    for a, b in unsure_pairs:
        v2 = second.get((a, b))
        for m in (a, b):
            if cur_uid.get(m) or m in handled:
                continue
            if v2 == "distinct":
                continue          # 保持分开 → 落入下面的单独新建
            else:                 # 2nd=same/unsure/缺 → 人工
                human_cards.add(m)

    singleton_new = sorted(all_unclustered - handled - human_cards)

    M = sum(len(f) for _, f in merge_into)
    N_multi = sum(len(m) for m in new_clusters)
    N_single = len(singleton_new)
    H = len(human_cards)
    print(f"[方案] 并入旧命题卡数 M={M}（{len(merge_into)} 个旧命题）")
    print(f"[方案] 新建命题 N：多成员命题 {len(new_clusters)} 个（成员 {N_multi}）"
          f" + 单成员命题 {N_single} 个（成员 {N_single}）")
    print(f"[方案] 人工队列 H={H}")
    ok = (M + N_multi + N_single + H == unclustered_before)
    print(f"[对账] M+N+H = {M + N_multi + N_single + H} / {unclustered_before}"
          f" {'✓ 一致' if ok else '✗ 不一致，拒绝写库！'}")
    if not ok or not commit:
        if not commit:
            print("[dry] 未带 --commit，不写库")
        return ok

    con.execute("BEGIN")
    try:
        next_uid = NEW_UID_START
        # 1) 并入旧命题
        for uid, fresh in merge_into:
            for cid in fresh:
                r = con.execute(
                    "SELECT verdict, reason FROM canon_verdicts WHERE a_id=? AND b_id=?"
                    " OR a_id=? AND b_id=? ORDER BY judged_at DESC LIMIT 1",
                    (cid, uid, uid, cid)).fetchone()
                con.execute(
                    "INSERT INTO merge_log (action,card_id,from_uid,to_uid,actor,"
                    "verdict,reason,batch_id,created_at) VALUES (?,?,?,?,?,?,?,?,?)",
                    ("merge", cid, None, uid, ACTOR,
                     r[0] if r else "same", (r[1] or "")[:200] if r else "",
                     BATCH, datetime.now().isoformat(timespec="seconds")))
                con.execute("UPDATE problems SET canonical_uid=? WHERE id=?", (uid, cid))
            members = [c for c, u in cur_uid.items() if u == uid] + fresh
            papers = {card_arxiv[c] for c in members} - {None}
            con.execute(
                "UPDATE canonical_problem SET n_cards=?, n_distinct_papers=?"
                " WHERE canonical_uid=?", (len(members), len(papers), uid))

        # 2) 新建命题（多成员 + 单成员）
        for members in new_clusters + [[c] for c in singleton_new]:
            uid = f"op-2026-{next_uid:06d}"
            next_uid += 1
            papers = {card_arxiv[c] for c in members} - {None}
            con.execute(
                "INSERT INTO canonical_problem (canonical_uid, rep_card_id, n_cards,"
                " n_distinct_papers, review_state, created_at) VALUES (?,?,?,?,?,?)",
                (uid, members[0], len(members), len(papers), "draft",
                 datetime.now().isoformat(timespec="seconds")))
            for cid in members:
                con.execute(
                    "INSERT INTO merge_log (action,card_id,from_uid,to_uid,actor,"
                    "verdict,reason,batch_id,created_at) VALUES (?,?,?,?,?,?,?,?,?)",
                    ("new_cluster", cid, None, uid, ACTOR, "-", "无 >=0.80 近邻或判定为不同",
                     BATCH, datetime.now().isoformat(timespec="seconds")))
                con.execute("UPDATE problems SET canonical_uid=? WHERE id=?", (uid, cid))

        # 3) 人工队列：冲突进 conflict_queue，卡留观并计数
        for note in conflict_notes:
            con.execute(
                "INSERT INTO conflict_queue (kind, payload_json, status, created_at)"
                " VALUES (?,?,?,?)",
                ("identity_contradiction", json.dumps(
                    {"batch": BATCH, "note": note}, ensure_ascii=False),
                 "open", datetime.now().isoformat(timespec="seconds")))
        for cid in sorted(human_cards):
            con.execute(
                "INSERT INTO conflict_queue (kind, payload_json, status, created_at)"
                " VALUES (?,?,?,?)",
                ("identity_human_queue", json.dumps(
                    {"batch": BATCH, "card_id": cid}, ensure_ascii=False),
                 "open", datetime.now().isoformat(timespec="seconds")))
        con.execute("COMMIT")
    except Exception as e:
        con.execute("ROLLBACK")
        raise

    # 收尾核验
    left = con.execute(
        "SELECT COUNT(*) FROM problems WHERE id NOT LIKE 'ext-%'"
        " AND (canonical_uid IS NULL OR canonical_uid='')").fetchone()[0]
    total_uids = con.execute("SELECT COUNT(*) FROM canonical_problem").fetchone()[0]
    merge_rows = con.execute(
        "SELECT COUNT(*) FROM merge_log WHERE batch_id=?", (BATCH,)).fetchone()[0]
    print(f"[核验] 剩余悬空本源卡: {left}（应 = H + 0）")
    print(f"[核验] canonical_problem 总数: 6,868 → {total_uids}")
    print(f"[核验] merge_log 本批行数: {merge_rows}（应 = M + N_multi + N_single）")
    print(f"[核验] integrity_check: {con.execute('PRAGMA integrity_check').fetchone()[0]}")
    con.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("用法: python3 apply_identity_verdicts_2026-09-30.py <db> [--commit]")
    main(sys.argv[1], "--commit" in sys.argv)
