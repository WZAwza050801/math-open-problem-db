#!/bin/bash
# Graceful shutdown of extraction engines + watchdog.
# Safe-kill: only python3 processes whose cmdline contains run_pilot.py.

cd /home/user/Wholeworks/wanganan/math_openproblem/pilot || exit 1
SELF=$$

echo "== step 1: stop watchdog =="
WD_PIDS=$(pgrep -f "^bash watchdog_daemon.sh$" || true)
for pid in $WD_PIDS; do
    if [ "$pid" != "$SELF" ]; then
        kill "$pid" && echo "watchdog $pid terminated"
    fi
done
[ -z "$WD_PIDS" ] && echo "watchdog: not running"
sleep 2

echo "== step 2: stop engines (python3 + run_pilot.py cmdline) =="
for pid in $(pgrep -f "run_pilot.py"); do
    exe=$(readlink "/proc/$pid/exe" 2>/dev/null)
    case "$exe" in
        *python*)
            kill "$pid" && echo "engine $pid ($exe) terminated"
            ;;
        *)
            echo "skip $pid (exe=$exe, not python)"
            ;;
    esac
done
sleep 3

echo "== step 3: verify =="
LEFT=$(pgrep -f "run_pilot.py" | grep -v "^$$\$" || true)
WD_LEFT=$(pgrep -f "^bash watchdog_daemon.sh$" || true)
if [ -z "$LEFT" ] && [ -z "$WD_LEFT" ]; then
    echo "ALL CLEAR: no watchdog, no engines"
else
    echo "REMAINING: engines=[$LEFT] watchdog=[$WD_LEFT]"
fi

echo "== final db state =="
python3 -c "
import sqlite3
con = sqlite3.connect('db.sqlite3')
print('extracted:', con.execute(\"select count(*) from papers where fetch_status='extracted'\").fetchone()[0])
print('cards:', con.execute('select count(*) from problems').fetchone()[0])
"
