"""apply_trial_verdicts.py — 把 trial_verdicts_2026-09-29.jsonl 落到 node01 生产库
铁律执行：
  0. 跑之前确认无 run_pilot 车道在跑（单写者）；
  1. 先整库备份（backups/db_pre_trial_verdicts_<ts>.sqlite3）；
  2. 全部裁决先落 human_adjudication 表（additive DDL，不影响现有管线）；
  3. B 捞回 UPDATE 前置校验：当前值必须是 not_a_proposition，否则跳过并报告；
  4. A same 对：本阶段只落裁决记录——problems 表尚无 canonical_uid 列，
     待 DDL 落地后由归并管线消费本表（verdict=same 的对优先合并）；
  5. 幂等：同 item+decided_at 已存在则跳过。
用法（在 node01 pilot 目录）：python3 apply_trial_verdicts.py
"""
import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB = Path("/home/user/Wholeworks/wanganan/math_openproblem/pilot/db.sqlite3")
VERDICTS = Path("/home/user/Wholeworks/wanganan/math_openproblem/pilot/trial_verdicts_2026-09-29.jsonl")

DDL = """
CREATE TABLE IF NOT EXISTS human_adjudication (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    item        TEXT NOT NULL,
    kind        TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    actor       TEXT NOT NULL,
    decided_at  TEXT NOT NULL,
    applied_at  TEXT DEFAULT (datetime('now')),
    UNIQUE(item, decided_at)
);
"""


def main():
    records = [json.loads(l) for l in VERDICTS.open(encoding="utf-8")]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    src = sqlite3.connect(DB)
    bak = DB.parent / "backups" / f"db_pre_trial_verdicts_{ts}.sqlite3"
    bak.parent.mkdir(exist_ok=True)
    dst = sqlite3.connect(bak)
    src.backup(dst)
    dst.close()
    print(f"[backup] {bak}")

    src.executescript(DDL)
    inserted = skipped = 0
    for r in records:
        try:
            src.execute(
                "INSERT INTO human_adjudication(item, kind, payload_json, actor, decided_at) VALUES (?,?,?,?,?)",
                (r["item"], r["kind"], json.dumps(r, ensure_ascii=False), r["actor"], r["decided_at"]))
            inserted += 1
        except sqlite3.IntegrityError:
            skipped += 1
    print(f"[adjudication] inserted={inserted} skipped(dup)={skipped}")

    rescued, rescue_skipped = [], []
    for r in records:
        if r["kind"] != "nap_rescue":
            continue
        cur = src.execute("SELECT paper_time_status FROM problems WHERE id=?", (r["card_id"],)).fetchone()
        if not cur:
            rescue_skipped.append((r["card_id"], "not_found"))
        elif cur[0] != r["from"]:
            rescue_skipped.append((r["card_id"], f"status={cur[0]} unexpected"))
        else:
            src.execute("UPDATE problems SET paper_time_status=? WHERE id=?", (r["to"], r["card_id"]))
            rescued.append(r["card_id"])
    src.commit()
    print(f"[rescue] updated={len(rescued)} skipped={rescue_skipped}")

    n = src.execute("SELECT count(*) FROM human_adjudication").fetchone()[0]
    print(f"[verify] human_adjudication total={n}")
    src.close()


if __name__ == "__main__":
    main()
