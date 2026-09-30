#!/usr/bin/env bash
# backup_daily.sh — node01 数学问题库每日热备（3-2-1 本地份）
# 部署: crontab 每日 04:00；RPO <= 24h
# 用法: backup_daily.sh [keep_days]
set -u
KEEP=${1:-14}
PILOT=/home/user/Wholeworks/wanganan/math_openproblem/pilot
DB="$PILOT/db.sqlite3"
BDIR="$PILOT/backups/daily"
STAMP=$(date +%F_%H%M)
OUT="$BDIR/db_$STAMP.sqlite3"
mkdir -p "$BDIR"

# 1) 在线一致热备
python3 - "$DB" "$OUT" <<'PY'
import sqlite3, sys
src, dst = sys.argv[1], sys.argv[2]
s = sqlite3.connect(src)
d = sqlite3.connect(dst)
with d:
    s.backup(d)
s.close(); d.close()
PY

# 2) 完整性校验
CHK=$(python3 - "$OUT" <<'PY'
import sqlite3, sys
con = sqlite3.connect(sys.argv[1])
print(con.execute("PRAGMA integrity_check").fetchone()[0])
con.close()
PY
)
if [ "$CHK" != "ok" ]; then
    echo "[$STAMP] integrity_check FAILED: $CHK" >&2
    rm -f "$OUT"
    exit 1
fi

# 3) 清理旧份（保留 $KEEP 天）
find "$BDIR" -name 'db_*.sqlite3' -mtime +$KEEP -delete
echo "[$STAMP] OK $(du -h "$OUT" | cut -f1)"
