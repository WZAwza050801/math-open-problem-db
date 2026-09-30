"""import_metric_history_2026-09-30.py — 把已算好的重要性分数按历史批次搬进正式表（零 AI）

对应 NEXT_PHASE_PLAN_2026-09-30 T05 的 importance 部分：
  来源  服务器 runs/p5/pilot_ranking.jsonl（6,752 行，run_id=score-full-20260927-v1）
  去向  canonical_metric 新表，每命题三个指标：
        importance_mu         value_num = mu（五维概率期望）
        importance_band       value_text = display_label（I1..I5）
        importance_confidence value_text = state（confident/boundary/disputed/ungraded）
  provenance 三元组（NOT NULL 表约）：{model_or_script, date, config_version, batch_id}
  纪律：
    - 只写 canonical_metric，canonical_problem 缓存列一个不碰（计划书明确）
    - 幂等：同批次已存在的行跳过并计数，可重复执行
    - 三个数对账：处理数 = 写入数 + 跳过数 + 失败数；失败行落文件不吞
    - 收尾硬校验：problems / canonical_problem 计数前后一致
用法：python3 import_metric_history_2026-09-30.py <db_path> [ranking_jsonl]
"""
import json
import os
import sqlite3
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RANKING = os.path.join(BASE, "runs", "p5", "pilot_ranking.jsonl")

BATCH_ID = "2026-09-30-历史批次"
PROVENANCE = json.dumps({
    "model_or_script": "full_score.py（主判 glm-5.3，触发项升级判 qwen，重跑稳定 30/30）",
    "date": "2026-09-27",
    "config_version": "rubric_v11+extra_dims / run score-full-20260927-v1 / seed 20260927",
    "batch_id": BATCH_ID,
}, ensure_ascii=False)

VALID_STATES = {"confident", "boundary", "disputed", "ungraded"}


def main(db_path, ranking_path):
    rows = []
    with open(ranking_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    n_source = len(rows)

    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row

    # v3 表必须在（先跑 migrate_ddl_v3.py）
    have = {r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    assert "canonical_metric" in have, "canonical_metric 表不存在，先跑 migrate_ddl_v3.py"

    before = {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
              for t in ("problems", "canonical_problem", "canonical_metric")}

    uid_ok = {r[0] for r in con.execute("SELECT canonical_uid FROM canonical_problem")}
    have_rows = {(r["canonical_uid"], r["metric"]) for r in con.execute(
        "SELECT canonical_uid, metric FROM canonical_metric WHERE provenance LIKE ?",
        (f'%{BATCH_ID}%',))}

    written = skipped = 0
    failures = []
    inserts = []
    for r in rows:
        uid = r.get("uid")
        mu = r.get("mu")
        label = r.get("display_label")
        state = r.get("state")
        if not uid or uid not in uid_ok:
            failures.append({"uid": uid, "reason": "uid 不在 canonical_problem"})
            continue
        if mu is None or label is None or state not in VALID_STATES:
            failures.append({"uid": uid, "reason": f"字段缺失或非法 state={state}"})
            continue
        for metric, val_num, val_text in (
                ("importance_mu", float(mu), None),
                ("importance_band", None, str(label)),
                ("importance_confidence", None, str(state))):
            if (uid, metric) in have_rows:
                skipped += 1
                continue
            inserts.append((uid, metric, val_num, val_text, PROVENANCE))

    con.executemany(
        "INSERT INTO canonical_metric(canonical_uid, metric, value_num, value_text, provenance)"
        " VALUES (?,?,?,?,?)", inserts)
    con.commit()

    after = {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
             for t in ("problems", "canonical_problem", "canonical_metric")}

    assert before["problems"] == after["problems"], "problems 计数变了！"
    assert before["canonical_problem"] == after["canonical_problem"], "canonical_problem 计数变了！"

    # 对账：按指标数（每行源数据 3 个指标）：处理×3 = 写入 + 跳过 + 失败×3
    assert n_source * 3 == len(inserts) + skipped + len(failures) * 3, \
        f"对账不平：{n_source}*3 != {len(inserts)}+{skipped}+{len(failures)}*3"
    assert after["canonical_metric"] == before["canonical_metric"] + len(inserts)

    if failures:
        fp = os.path.join(BASE, "scratch", "import_metric_failures_2026-09-30.json")
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(failures, f, ensure_ascii=False, indent=1)

    print(f"[T05] 来源 {n_source} 行（{ranking_path}）")
    print(f"[T05] canonical_metric {before['canonical_metric']} -> {after['canonical_metric']}（写入 {len(inserts)}，幂等跳过 {skipped}）")
    print(f"[T05] 失败 {len(failures)} 行" + (f"，已落 {fp}" if failures else ""))
    print(f"[T05] problems={after['problems']} canonical_problem={after['canonical_problem']}（前后一致 ✓）")

    # 抽 3 例看一眼
    for uid in ("op-2026-002779", "op-2026-001146"):
        for r in con.execute(
                "SELECT metric, value_num, value_text FROM canonical_metric WHERE canonical_uid=?",
                (uid,)):
            print(f"[抽查] {uid}  {r['metric']}  num={r['value_num']}  text={r['value_text']}")
    con.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("用法: python3 import_metric_history_2026-09-30.py <db_path> [ranking_jsonl]")
    ranking = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_RANKING
    main(sys.argv[1], ranking)
