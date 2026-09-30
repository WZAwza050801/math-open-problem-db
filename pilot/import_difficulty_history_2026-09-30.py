"""import_difficulty_history_2026-09-30.py — 把 v4 批解题轨迹 180 条 + 判定 + 拟合入正式表（零 AI）

对应 NEXT_PHASE_PLAN T05 的 solver_attempt / progress_verdict / engine_skill 部分。
数据甄别（2026-09-30 22:40 核实）：
  - 服务器 runs/difficulty-v1/attempts/ = v4 终态批 180 条（glm-5.3 48 + deepseek-v4-pro 132，
    2026-09-28~30 产，62 题）；verdicts.jsonl 180 条 glm-5.3 独立判定，sha256 全部对上 attempt
  - 本地 runs/m13-v1/ = 更早批次（150 doubao 判定 + 150 cross + 149 v2），按"历史行保留"
    原则留档文件不入库（计划书 §3.2：只收正式表需要的当前批）
  - 拟合：本地 difficulty_fit_v3.json（partial_creditPCM_v3，n_obs 298 / 100 题 / corr -0.915，
    混合了早期批判定）→ engine_skill 以 fit_batch=v3-pcm 收编；
    本地 v1/v2 拟合是不同量表批（S006 报告 corr -0.915 为当前口径），v1/v2 保留文件不重复入表

纪律：幂等（batch_id 相同的 attempt/verdict/fit 跳过）；provenance 齐全；收尾硬校验。
用法：python3 import_difficulty_history_2026-09-30.py <db_path> [fit_json]
"""
import json
import os
import sqlite3
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
ATT_DIR = os.path.join(BASE, "runs", "difficulty-v1", "attempts")
VER_FILE = os.path.join(BASE, "runs", "difficulty-v1", "verdicts.jsonl")
DEFAULT_FIT = os.path.join(BASE, "runs", "m13-v1", "difficulty_fit_v3.json")

BATCH_ID = "2026-09-30-历史批次"


def main(db_path, fit_path):
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    q = con.execute

    have = {r[0] for r in q("SELECT name FROM sqlite_master WHERE type='table'")}
    for t in ("solver_attempt", "progress_verdict", "engine_skill"):
        assert t in have, f"{t} 表不存在，先跑 migrate_ddl_v3.py"

    before = {t: q(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
              for t in ("problems", "canonical_problem", "solver_attempt",
                        "progress_verdict", "engine_skill")}
    uid_ok = {r[0] for r in q("SELECT canonical_uid FROM canonical_problem")}

    # ---------- 1. solver_attempt：180 条轨迹 ----------
    att_files = sorted(os.listdir(ATT_DIR))
    atts = {}
    for f in att_files:
        a = json.load(open(os.path.join(ATT_DIR, f), encoding="utf-8"))
        atts[a["attempt_sha256"]] = a
    # 已入库的（按 batch_id + sha 去重）：attempt_json 里存了 sha
    have_sha = set()
    for r in q("SELECT attempt_json FROM solver_attempt WHERE batch_id=?", (BATCH_ID,)):
        have_sha.add(json.loads(r["attempt_json"]).get("attempt_sha256"))

    n_att = n_att_skip = n_att_bad = 0
    ins_att = []
    for sha, a in atts.items():
        if a["uid"] not in uid_ok:
            n_att_bad += 1
            continue
        if sha in have_sha:
            n_att_skip += 1
            continue
        payload = json.dumps({
            "attempt_sha256": sha, "uid": a["uid"], "traj": a["traj"],
            "chars": a.get("chars"), "latency_s": a.get("latency_s"),
            "ts": a.get("ts"), "tokens_in": a.get("tokens_in"),
            "tokens_out": a.get("tokens_out"), "content": a.get("content"),
        }, ensure_ascii=False)
        ins_att.append((a["uid"], a["model"], payload,
                        json.dumps({"temperature": 0.2, "max_tokens": None,
                                    "source_file": f}, ensure_ascii=False),
                        BATCH_ID))
        n_att += 1
    con.executemany(
        "INSERT INTO solver_attempt(canonical_uid, engine, attempt_json, config, batch_id)"
        " VALUES (?,?,?,?,?)", ins_att)
    con.commit()

    # ---------- 2. progress_verdict：180 条判定挂到刚插入的 attempt ----------
    # 需要 attempt_id：按 (uid, engine, batch, sha) 关联
    sha_to_id = {}
    for r in q("SELECT id, attempt_json FROM solver_attempt WHERE batch_id=?", (BATCH_ID,)):
        sha_to_id[json.loads(r["attempt_json"]).get("attempt_sha256")] = r["id"]
    have_ver = {r[0] for r in q(
        "SELECT attempt_id FROM progress_verdict WHERE judge='glm-5.3' AND version='v1'")}
    vers = [json.loads(l) for l in open(VER_FILE, encoding="utf-8") if l.strip()]
    n_ver = n_ver_skip = 0
    ver_failures = []
    ins_ver = []
    for v in vers:
        aid = sha_to_id.get(v["attempt_sha256"])
        if v.get("level") is None:
            # 6 条 parse_fail（rationale='parse_fail'）：level NOT NULL 不能入库，落清单不吞
            ver_failures.append({"uid": v["uid"], "traj": v["traj"],
                                 "attempt_sha256": v["attempt_sha256"], "ts": v.get("ts")})
            continue
        if aid is None or aid in have_ver:
            n_ver_skip += 1
            continue
        ins_ver.append((aid, v.get("model", "glm-5.3"), int(v["level"]), "v1",
                        json.dumps({"rationale": v.get("rationale"),
                                    "red_flags": v.get("red_flags"),
                                    "ts": v.get("ts")}, ensure_ascii=False)))
        n_ver += 1
    con.executemany(
        "INSERT INTO progress_verdict(attempt_id, judge, level, version, note)"
        " VALUES (?,?,?,?,?)", ins_ver)
    con.commit()

    # ---------- 3. engine_skill：v3 拟合 ----------
    fit = json.load(open(fit_path, encoding="utf-8"))
    n_fit = 0
    for engine, theta in fit["theta"].items():
        row = q("SELECT 1 FROM engine_skill WHERE engine=? AND fit_batch=?",
                (engine, "v3-pcm")).fetchone()
        if row:
            continue
        con.execute(
            "INSERT INTO engine_skill(engine, fit_batch, theta, n_problems,"
            " artifact_note, corr_check) VALUES (?,?,?,?,?,?)",
            (engine, "v3-pcm", theta, fit["n_problems"],
             "glm-5.3: qianfan-32k-truncation 疑似伪影（见 M13 报告），前端禁用" if engine == "glm-5.3" else None,
             fit.get("corr_beta_vs_rawmean")))
        n_fit += 1
    con.commit()

    # ---------- 对账 + 硬校验 ----------
    after = {t: q(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
             for t in ("problems", "canonical_problem", "solver_attempt",
                       "progress_verdict", "engine_skill")}
    assert before["problems"] == after["problems"]
    assert before["canonical_problem"] == after["canonical_problem"]
    assert n_att == len(ins_att) and after["solver_attempt"] == before["solver_attempt"] + n_att
    assert after["progress_verdict"] == before["progress_verdict"] + n_ver

    print(f"[T05余] solver_attempt {before['solver_attempt']} -> {after['solver_attempt']}"
          f"（写入 {n_att}，跳过 {n_att_skip}，uid 无效 {n_att_bad}）")
    print(f"[T05余] progress_verdict {before['progress_verdict']} -> {after['progress_verdict']}"
          f"（写入 {n_ver}，跳过 {n_ver_skip}，parse_fail 不入库 {len(ver_failures)}）")
    if ver_failures:
        fp = os.path.join(BASE, "scratch", "progress_verdict_failures_2026-09-30.json")
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(ver_failures, f, ensure_ascii=False, indent=1)
        print(f"[T05余] parse_fail 清单已落 {fp}")
    print(f"[T05余] engine_skill {before['engine_skill']} -> {after['engine_skill']}"
          f"（写入 {n_fit}，fit v3-pcm corr={fit.get('corr_beta_vs_rawmean')}）")
    print(f"[T05余] problems={after['problems']} canonical={after['canonical_problem']}（前后一致 ✓）")
    for r in q("SELECT engine, COUNT(*) FROM solver_attempt GROUP BY engine"):
        print("[抽查]", tuple(r))
    con.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("用法: python3 import_difficulty_history_2026-09-30.py <db_path> [fit_json]")
    fit = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_FIT
    main(sys.argv[1], fit)
