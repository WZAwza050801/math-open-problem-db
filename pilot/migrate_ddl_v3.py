"""migrate_ddl_v3.py — 第三版库结构迁移（幂等、只加不改）

依据 NEXT_PHASE_PLAN_2026-09-30 §3.2：本版只解决"分数进正式表要带来源三元组"一件事。
新建五张表，全部用语义名（命名规范 2026-09-30）：
  canonical_metric  每个命题一项指标的当前正式值（重要性/生命力/难度）
  metric_series     同一指标的历史点，只追加不覆盖
  solver_attempt    一次模型对一个命题的解题尝试原文
  progress_verdict  独立判官给某次尝试打的进度等级
  engine_skill      某次统计拟合里各模型的能力值，带样本量与伪影标注

设计原则（对齐 migrate_ddl_v2.py 与治理铁律）：
  - 只加表，现有表一个字不改；全部 IF NOT EXISTS，可重复执行
  - 指标表统一带 visibility 列，默认 internal，升公开走人工
  - provenance（来源三元组：谁算的/哪天/哪版配置）NOT NULL——缺来源的分数拒绝入库
  - 收尾硬校验：problems/canonical_problem 计数前后一致
  - 第二遍执行必须是"新增 0 张表"，否则视为异常（计划书停机条件之一）

用法：python3 migrate_ddl_v3.py <db_path>
"""
import sqlite3
import sys
from datetime import datetime

MIGRATION_VERSION = "v3.0"

NEW_TABLES = """
-- 命题级指标当前正式值：一行一个指标，缓存列只允许由本表同步
CREATE TABLE IF NOT EXISTS canonical_metric (
    canonical_uid TEXT NOT NULL REFERENCES canonical_problem(canonical_uid),
    metric        TEXT NOT NULL,   -- importance_mu|importance_band|importance_confidence|vitality|difficulty_beta|difficulty_band|semantic_influence|citation_gap
    value_num     REAL,
    value_text    TEXT,            -- 档位等离散值
    provenance    TEXT NOT NULL,   -- JSON: {model_or_script, date, config_version, batch_id}
    computed_at   TEXT DEFAULT (datetime('now')),
    visibility    TEXT NOT NULL DEFAULT 'internal',
    PRIMARY KEY (canonical_uid, metric)
);

-- 指标历史点：月度生命力、每次重算，只追加不覆盖
CREATE TABLE IF NOT EXISTS metric_series (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type TEXT NOT NULL,     -- canonical | paper
    entity_id   TEXT NOT NULL,
    metric      TEXT NOT NULL,
    value_num   REAL NOT NULL,
    provenance  TEXT NOT NULL,
    computed_at TEXT DEFAULT (datetime('now')),
    visibility  TEXT NOT NULL DEFAULT 'internal'
);
CREATE INDEX IF NOT EXISTS idx_metric_series ON metric_series(entity_type, entity_id, metric, computed_at);

-- 一次引擎对一题的解题尝试（含思路/结论/自评原文，config 供截断伪影追溯）
CREATE TABLE IF NOT EXISTS solver_attempt (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_uid TEXT NOT NULL,
    engine        TEXT NOT NULL,   -- glm-5.3 | deepseek-v4-pro | kimi-k2.6 | qwen3.8-max ...
    attempt_json  TEXT NOT NULL,
    config        TEXT,            -- JSON: 温度/max_tokens/截断参数
    batch_id      TEXT,
    created_at    TEXT DEFAULT (datetime('now'))
);

-- 独立判官对某次尝试的进度等级（不同 version 的量表不可混算）
CREATE TABLE IF NOT EXISTS progress_verdict (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    attempt_id  INTEGER NOT NULL REFERENCES solver_attempt(id),
    judge       TEXT NOT NULL,     -- 裁决引擎或 human:<name>
    level       INTEGER NOT NULL,  -- 1..5 五级量表
    version     TEXT NOT NULL,     -- v1 | v2 | ...
    note        TEXT,
    created_at  TEXT DEFAULT (datetime('now'))
);

-- BT 拟合产物：引擎能力 θ，小样本必须带 n_problems，伪影必须带 artifact_note
CREATE TABLE IF NOT EXISTS engine_skill (
    engine        TEXT NOT NULL,
    fit_batch     TEXT NOT NULL,
    theta         REAL NOT NULL,
    n_problems    INTEGER NOT NULL,
    artifact_note TEXT,            -- 如 qianfan-32k-truncation；非空则该 θ 前端禁用
    corr_check    REAL,
    computed_at   TEXT DEFAULT (datetime('now')),
    visibility    TEXT NOT NULL DEFAULT 'internal',
    PRIMARY KEY (engine, fit_batch)
);
"""

TABLE_NAMES = ["canonical_metric", "metric_series",
               "solver_attempt", "progress_verdict", "engine_skill"]


def main(db_path):
    con = sqlite3.connect(db_path)
    existing = {r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}

    before_counts = {t: con.execute(
        f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        for t in ("problems", "canonical_problem")}

    created = 0
    con.executescript(NEW_TABLES)
    con.commit()
    for t in TABLE_NAMES:
        if t not in existing:
            created += 1

    after_existing = {r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    for t in TABLE_NAMES:
        assert t in after_existing, f"表 {t} 建表后仍不存在"

    after_counts = {t: con.execute(
        f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        for t in ("problems", "canonical_problem")}
    for t in before_counts:
        assert before_counts[t] == after_counts[t], \
            f"{t} 计数变了：{before_counts[t]} -> {after_counts[t]}"

    if created > 0:
        con.execute(
            "INSERT INTO schema_migrations (version, applied_at, note) VALUES (?,?,?)",
            (MIGRATION_VERSION, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
             f"V3 DDL：新增 {created} 张指标表（五张语义名）；"
             f"problems={after_counts['problems']}"))
        con.commit()

    print(f"[v3] 新增表 {created}/{len(TABLE_NAMES)} 张；"
          f"problems={after_counts['problems']} "
          f"canonical_problem={after_counts['canonical_problem']}（前后一致）")
    rows = con.execute(
        "SELECT version, applied_at, note FROM schema_migrations ORDER BY applied_at").fetchall()
    for r in rows:
        print("[v3] 迁移记录:", r)
    con.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("用法: python3 migrate_ddl_v3.py <db_path>")
    main(sys.argv[1])
