"""migrate_ddl_v2.py — DB_DESIGN_V2 迁移脚本（幂等、只加不改）
导师批复 ① 条件：保留卡片原始证据、稳定 UID、状态事件、可撤销归并；迁移核对卡片一张不丢。

设计原则（对齐 GOVERNANCE 铁律）：
  - 只加表、只加列、只回填新列——现有 17 张表的数据一个字不改
  - 全部 IF NOT EXISTS / 先查 pragma 再加列，可重复执行
  - 收尾硬性校验：problems/canonical_problem 计数前后一致、无孤儿指针

用法：python migrate_ddl_v2.py <db_path>
"""
import hashlib
import re
import sqlite3
import sys
from datetime import datetime

MIGRATION_VERSION = "v2.0"
BATCH_ID = "ar5iv-5journal-2026-09"

NEW_TABLES = """
-- 状态事件链（V2 §3.3）：status 的唯一权威来源，canonical.status 只是它的缓存
CREATE TABLE IF NOT EXISTS status_event (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_uid TEXT NOT NULL REFERENCES canonical_problem(canonical_uid),
    event_type    TEXT NOT NULL,   -- proposed_at_paper|solved_in_paper|claimed_solved|disputed|background_known_open|human_verified|external_source|solved_in_literature
    source_arxiv_id TEXT,
    source_card_id  TEXT,
    source_url      TEXT,
    year          INTEGER,
    note          TEXT,
    created_at    TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_se_uid ON status_event(canonical_uid, year);

-- 归并留痕（GOVERNANCE §2.3）：拆并 = 读 merge_log 反向回放
CREATE TABLE IF NOT EXISTS merge_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    action     TEXT NOT NULL,        -- merge | split
    card_id    TEXT NOT NULL,
    from_uid   TEXT,
    to_uid     TEXT,
    actor      TEXT NOT NULL,        -- 'pipeline:canon_judge_v2' | 'human:导师' | ...
    verdict    TEXT,                 -- same | unsure | manual
    reason     TEXT,
    batch_id   TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- 一切写操作留痕（GOVERNANCE §一.5）
CREATE TABLE IF NOT EXISTS audit_log (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    actor        TEXT NOT NULL,
    action       TEXT NOT NULL,
    target_table TEXT,
    target_id    TEXT,
    detail_json  TEXT,
    batch_id     TEXT,
    created_at   TEXT DEFAULT (datetime('now'))
);

-- 冲突终审队列（GOVERNANCE）：双裁决矛盾对、外部状态冲突都进这里
CREATE TABLE IF NOT EXISTS conflict_queue (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    kind        TEXT NOT NULL,       -- identity_contradiction | status_conflict | nap_rescue | difficulty_claim
    payload_json TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'open',   -- open | adjudicated | wont_fix
    resolved_by TEXT,
    created_at  TEXT DEFAULT (datetime('now')),
    resolved_at TEXT
);

-- schema 版本登记
CREATE TABLE IF NOT EXISTS schema_migrations (
    version    TEXT PRIMARY KEY,
    applied_at TEXT DEFAULT (datetime('now')),
    note       TEXT
);

-- 有名问题别名字典（V2 §3.4）
CREATE TABLE IF NOT EXISTS named_problem (
    alias      TEXT NOT NULL,
    alias_norm TEXT NOT NULL,
    lang       TEXT NOT NULL DEFAULT 'en',
    canonical_uid TEXT REFERENCES canonical_problem(canonical_uid),
    source     TEXT,
    PRIMARY KEY (alias_norm, lang)
);

-- 问题间关系（V2 §3.4）
CREATE TABLE IF NOT EXISTS problem_relation (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    from_uid   TEXT NOT NULL REFERENCES canonical_problem(canonical_uid),
    to_uid     TEXT NOT NULL REFERENCES canonical_problem(canonical_uid),
    kind       TEXT NOT NULL,   -- specializes|generalizes|equivalent_to|implies|motivated_by|appears_in
    evidence_card_id TEXT,
    source_arxiv_id  TEXT,
    review_state TEXT NOT NULL DEFAULT 'machine_extracted',
    created_at TEXT DEFAULT (datetime('now'))
);

-- 多数据集注入溯源（V2 §3.4）
CREATE TABLE IF NOT EXISTS ingest_batch (
    batch_id   TEXT PRIMARY KEY,
    dataset    TEXT NOT NULL,
    note       TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- 标签体系（V1 §四：MSC 骨架 + 正交维度 + 自由标签）
CREATE TABLE IF NOT EXISTS tag (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name   TEXT NOT NULL,
    kind   TEXT NOT NULL,        -- orthogonal | free
    note   TEXT,
    UNIQUE(name, kind)
);
CREATE TABLE IF NOT EXISTS problem_tag (
    canonical_uid TEXT NOT NULL REFERENCES canonical_problem(canonical_uid),
    tag_id        INTEGER NOT NULL REFERENCES tag(id),
    source        TEXT NOT NULL DEFAULT 'manual',   -- manual | pipeline | external
    created_at    TEXT DEFAULT (datetime('now')),
    PRIMARY KEY (canonical_uid, tag_id)
);

-- 人工裁决（apply_trial_verdicts.py 同款，放这里保证单一口径）
CREATE TABLE IF NOT EXISTS human_adjudication (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    item         TEXT NOT NULL,
    kind         TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    actor        TEXT NOT NULL,
    decided_at   TEXT NOT NULL,
    applied_at   TEXT DEFAULT (datetime('now')),
    UNIQUE(item, decided_at)
);

-- 迁移期关键索引（没有它，canonical 相关回填是 O(n²) 全表扫）
CREATE INDEX IF NOT EXISTS idx_problems_canonical_uid ON problems(canonical_uid);
CREATE INDEX IF NOT EXISTS idx_canonical_problem_uid ON canonical_problem(canonical_uid);
CREATE INDEX IF NOT EXISTS idx_status_event_uid ON status_event(canonical_uid);
"""

# (table, column, ddl)
NEW_COLUMNS = [
    ("problems", "batch_id", f"ALTER TABLE problems ADD COLUMN batch_id TEXT DEFAULT '{BATCH_ID}'"),
    ("problems", "verdict_note", "ALTER TABLE problems ADD COLUMN verdict_note TEXT"),
    ("problems", "statement_hash", "ALTER TABLE problems ADD COLUMN statement_hash TEXT"),
    ("canonical_problem", "status", "ALTER TABLE canonical_problem ADD COLUMN status TEXT DEFAULT 'open'"),
    ("canonical_problem", "origin_type", "ALTER TABLE canonical_problem ADD COLUMN origin_type TEXT DEFAULT 'journal_mined'"),
    ("canonical_problem", "origin_arxiv_id", "ALTER TABLE canonical_problem ADD COLUMN origin_arxiv_id TEXT"),
    ("canonical_problem", "origin_year", "ALTER TABLE canonical_problem ADD COLUMN origin_year INTEGER"),
    ("canonical_problem", "msc_primary", "ALTER TABLE canonical_problem ADD COLUMN msc_primary TEXT"),
    ("canonical_problem", "msc_secondary", "ALTER TABLE canonical_problem ADD COLUMN msc_secondary TEXT"),
    ("canonical_problem", "vitality_score", "ALTER TABLE canonical_problem ADD COLUMN vitality_score REAL"),
    ("canonical_problem", "merged_into", "ALTER TABLE canonical_problem ADD COLUMN merged_into TEXT"),
]


def normalize_quote(s: str) -> str:
    """GOVERNANCE §2.2：lower + 去空白/LaTeX 控制序列 + 去标点"""
    s = (s or "").lower()
    s = re.sub(r"\\[a-zA-Z]+", " ", s)          # LaTeX 控制序列
    s = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", s)  # 去标点/空白/符号
    return s


def has_column(con, table, col):
    return col in [r[1] for r in con.execute(f"pragma table_info({table})")]


def main():
    db_path = sys.argv[1]
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA foreign_keys=OFF")  # 迁移期不拦旧数据
    before_problems = con.execute("SELECT count(*) FROM problems").fetchone()[0]
    before_canon = con.execute("SELECT count(*) FROM canonical_problem").fetchone()[0]
    print(f"[before] problems={before_problems} canonical={before_canon}")

    # Phase 1 新表
    con.executescript(NEW_TABLES)
    print("[p1] 10 张新表就绪（已存在则跳过）")

    # Phase 2 新列
    added = []
    for table, col, ddl in NEW_COLUMNS:
        if not has_column(con, table, col):
            con.execute(ddl)
            added.append(f"{table}.{col}")
    print(f"[p2] 新列 +{len(added)}: {added}")

    # Phase 3 回填（全部只写新列/新表）
    # 3a. ingest_batch 登记
    con.execute(
        "INSERT OR IGNORE INTO ingest_batch(batch_id, dataset, note) VALUES (?,?,?)",
        (BATCH_ID, "ar5iv_5j", "五刊 2000-2025 管线抽取，V2 迁移时登记"))

    # 3b. canonical_problem 派生列回填（Python 侧单遍聚合，避免关联子查询 O(n²)）
    rep = {r[0]: r[1:] for r in con.execute(
        "SELECT id, arxiv_id, msc_primary, msc_secondary_json, paper_time_status FROM problems")}
    min_year = {}
    for uid, yr in con.execute(
            "SELECT canonical_uid, pub_year FROM problems "
            "WHERE canonical_uid IS NOT NULL AND canonical_uid != '' AND pub_year IS NOT NULL"):
        if uid not in min_year or yr < min_year[uid]:
            min_year[uid] = yr
    vitality = {}
    if "objective_feature_snapshots" in [r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")]:
        vitality = dict(con.execute(
            "SELECT canonical_uid, vitality FROM objective_feature_snapshots"))
    canon_rows = con.execute(
        "SELECT canonical_uid, rep_card_id FROM canonical_problem WHERE origin_arxiv_id IS NULL").fetchall()
    updates = []
    for uid, rep_id in canon_rows:
        r = rep.get(rep_id, (None, None, None, None))
        arxiv, msc_p, msc_s, pts = r
        status = "solved" if pts == "solved_in_paper" else "open"
        updates.append((arxiv, msc_p, msc_s, min_year.get(uid), status,
                        vitality.get(uid), uid))
    con.executemany("""
        UPDATE canonical_problem SET origin_arxiv_id=?, msc_primary=?, msc_secondary=?,
            origin_year=?, status=?, vitality_score=?
        WHERE canonical_uid=? AND origin_arxiv_id IS NULL
    """, updates)
    print(f"[p3b] canonical 派生列回填 {len(updates)} 条（origin/msc/status 缓存/vitality）")

    # 3c. problems.statement_hash 回填
    n_hash = 0
    rows = con.execute(
        "SELECT id, original_quote FROM problems WHERE statement_hash IS NULL").fetchall()
    for pid, quote in rows:
        h = hashlib.sha1(normalize_quote(quote).encode("utf-8")).hexdigest()
        con.execute("UPDATE problems SET statement_hash=? WHERE id=?", (h, pid))
        n_hash += 1
    print(f"[p3c] statement_hash 回填 {n_hash} 张")

    # 3d. status_event 回填（V2 §3.3 流程 1-2，Python 侧组装避免关联子查询）
    have_proposed = {r[0] for r in con.execute(
        "SELECT canonical_uid FROM status_event WHERE event_type='proposed_at_paper'")}
    have_events = set(con.execute(
        "SELECT canonical_uid, event_type, source_card_id FROM status_event "
        "WHERE source_card_id IS NOT NULL"))
    events = []
    rep_of = {}
    for uid, rep_id in con.execute("SELECT canonical_uid, rep_card_id FROM canonical_problem"):
        rep_of[uid] = rep_id
        if uid not in have_proposed:
            r = rep.get(rep_id)
            if r and r[0]:
                events.append((uid, "proposed_at_paper", r[0], rep_id,
                               min_year.get(uid), "V2 迁移回填：代表卡"))
    for uid, arxiv, pid, yr, pts in con.execute(
            "SELECT canonical_uid, arxiv_id, id, pub_year, paper_time_status FROM problems "
            "WHERE canonical_uid IS NOT NULL AND canonical_uid != '' "
            "AND paper_time_status IN ('solved_in_paper','background_known_open')"):
        if rep_of.get(uid) == pid or (uid, pts, pid) in have_events:
            continue
        events.append((uid, pts, arxiv, pid, yr, "V2 迁移回填：成员卡时点状态"))
    con.executemany(
        "INSERT INTO status_event(canonical_uid, event_type, source_arxiv_id, source_card_id, year, note)"
        " VALUES (?,?,?,?,?,?)", events)
    n_events = con.execute("SELECT count(*) FROM status_event").fetchone()[0]
    print(f"[p3d] status_event 新增 {len(events)} 条，累计 {n_events} 条")

    # 3e. status 缓存按事件链重算（有 solved 事件的 canonical 优先标 solved）
    solved_uids = {r[0] for r in con.execute(
        "SELECT DISTINCT canonical_uid FROM status_event "
        "WHERE event_type IN ('solved_in_paper','solved_in_literature','human_verified')")}
    con.executemany(
        "UPDATE canonical_problem SET status='solved' WHERE canonical_uid=? AND status!='solved'",
        [(u,) for u in solved_uids])

    # Phase 4 登记 + 校验
    con.execute(
        "INSERT OR REPLACE INTO schema_migrations(version, note) VALUES (?,?)",
        (MIGRATION_VERSION, f"V2 DDL：10 新表 + {len(added)} 新列 + 回填；源 problems={before_problems}"))
    con.commit()

    after_problems = con.execute("SELECT count(*) FROM problems").fetchone()[0]
    after_canon = con.execute("SELECT count(*) FROM canonical_problem").fetchone()[0]
    orphans = con.execute("""
        SELECT count(*) FROM problems p LEFT JOIN canonical_problem cp
        ON cp.canonical_uid = p.canonical_uid
        WHERE p.canonical_uid IS NOT NULL AND p.canonical_uid != ''
          AND cp.canonical_uid IS NULL
    """).fetchone()[0]
    canon_no_origin = con.execute(
        "SELECT count(*) FROM canonical_problem WHERE origin_year IS NULL").fetchone()[0]
    dup_hash = con.execute("""
        SELECT count(*) FROM (SELECT statement_hash, arxiv_id FROM problems
            WHERE statement_hash IS NOT NULL
            GROUP BY statement_hash, arxiv_id HAVING count(*) > 1)
    """).fetchone()[0]

    print("\n===== 校验报告（导师条件：一张不丢）=====")
    print(f"problems: {before_problems} → {after_problems}  {'✅' if before_problems == after_problems else '❌'}")
    print(f"canonical_problem: {before_canon} → {after_canon}  {'✅' if before_canon == after_canon else '❌'}")
    print(f"孤儿指针（problems.canonical_uid 无对应 canonical）: {orphans}  {'✅' if orphans == 0 else '⚠️'}")
    print(f"origin_year 未回填: {canon_no_origin}（成员卡未挂 uid 的 canonical 会为 0 之外的情况）")
    print(f"同论文 statement_hash 撞车组数: {dup_hash}（L1 同卡重复线索，供归并管线消费）")
    con.close()


if __name__ == "__main__":
    main()
