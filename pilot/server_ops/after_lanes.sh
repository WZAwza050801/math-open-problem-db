#!/bin/bash
# after_lanes.sh — 车道收官后自动执行：V2 迁移 + 试审裁决落库（2026-09-30）
P=/home/user/Wholeworks/wanganan/math_openproblem/pilot
LOG=$P/logs/ddl_migration_0930.log
echo "[watch] start $(date '+%F %T')" >> $LOG
while pgrep -f 'run_pilo[t].py' > /dev/null; do sleep 60; done
echo "[watch] lanes idle at $(date '+%F %T'), start migration" >> $LOG
cd $P
python3 -u migrate_ddl_v2.py db.sqlite3 >> $LOG 2>&1
echo "[migrate] exit=$? $(date '+%F %T')" >> $LOG
python3 -u apply_trial_verdicts.py >> $LOG 2>&1
echo "[verdicts] exit=$? $(date '+%F %T')" >> $LOG
# 收官快照
python3 -c "import sqlite3; from datetime import datetime; ts=datetime.now().strftime('%Y%m%d_%H%M%S'); s=sqlite3.connect('db.sqlite3'); d=sqlite3.connect(f'backups/db_post_migration_{ts}.sqlite3'); s.backup(d); print('snapshot', ts)" >> $LOG 2>&1
echo "[watch] all done $(date '+%F %T')" >> $LOG
