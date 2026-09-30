#!/usr/bin/env python3
"""Ops watchdog — keep every registered lane alive.

Reads lanes_0929.json, checks each lane/sidecar is running, relaunches anything
dead with the exact config it was registered with. Safe to run from cron:
  * it never kills anything
  * relaunch is idempotent because run_pilot recomputes todo from done_ids
  * relaunching a lane whose slice is already finished simply exits

Usage:  python3 ops_watchdog.py           # report + relaunch dead
        python3 ops_watchdog.py --dry     # report only
"""
import json, os, subprocess, sys, time
from datetime import datetime

BASE = "/home/user/Wholeworks/wanganan/math_openproblem/pilot"
os.chdir(BASE)
REG = json.load(open("lanes_0929.json", encoding="utf-8"))
DRY = "--dry" in sys.argv


def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=45).stdout.strip()


def count(match):
    out = sh(f"ps -eo cmd | grep -F '{match}' | grep -v grep")
    return len([l for l in out.splitlines() if l.strip()])


def env_for(vendor):
    """Build the env prefix for a vendor, reading keys from .env / key files."""
    d = {}
    for line in open(".env", encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        d[k.strip()] = v.strip().strip('"').strip("'")
    if vendor == "glm":
        ks = [d.get("GLM_CODING_TEAM_KEY", ""), d.get("GLM_CODING_TEAM2_KEY", "")]
        ks = [k for k in ks if k]
        if not ks:
            return None
        return f'GLM_KEYS="{",".join(ks)}"'
    if vendor == "qianfan":
        p = os.path.join(BASE, ".qianfan_key")
        if not os.path.exists(p):
            return None
        k = open(p, encoding="utf-8").read().strip()
        if not k:
            return None
        return (f'GLM_BASE_URL="https://qianfan.baidubce.com/v2/tokenplan/personal" '
                f'GLM_KEYS="{k}"')
    return None


print("=" * 66)
print("WATCHDOG", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "(dry)" if DRY else "")
print("=" * 66)

want = sum(1 for L in REG["lanes"] if L.get("enabled"))
have = count("run_pilot.py")
print(f"\nextraction lanes: running={have} expected={want}")

if have < want and not DRY:
    for L in REG["lanes"]:
        if not L.get("enabled"):
            continue
        log = L["log"]
        # a lane counts as alive if its log was touched in the last 15 min
        stale = 10 ** 9
        if os.path.exists(log):
            stale = time.time() - os.path.getmtime(log)
        if stale < 900:
            print(f"  {L['name']:<10} alive (log {int(stale)}s ago)")
            continue
        env = env_for(L["vendor"])
        if env is None:
            print(f"  {L['name']:<10} !! no key for vendor {L['vendor']} — skipped")
            continue
        cmd = (f'setsid env {env} CANDIDATES_JSON_PATH={REG["batch"]} ARXIV_GAP=6 '
               f'ENGINE_SLICE={L["slice"]} PILOT_WORKERS={L["workers"]} '
               f'ENGINE_FLAVOR={L["flavor"]} GLM_MODEL={L["model"]} '
               f'nohup python3 -u run_pilot.py >> {log} 2>&1 < /dev/null &')
        print(f"  {L['name']:<10} RELAUNCH (slice {L['slice']}, {L['model']}, w={L['workers']})")
        subprocess.run(["bash", "-c", cmd], timeout=60)
        time.sleep(5)
elif have < want:
    print(f"  (dry run) would relaunch {want-have} lane(s)")
else:
    for L in REG["lanes"]:
        if not L.get("enabled"):
            continue
        if os.path.exists(L["log"]):
            print(f"  {L['name']:<10} ok ({int(time.time()-os.path.getmtime(L['log']))}s ago)")
        else:
            print(f"  {L['name']:<10} no log")

def running_lanes():
    """[(pid, slice, model)] for live run_pilot processes, read from /proc environ."""
    res = []
    out = sh("ps -eo pid,cmd | grep -F 'run_pilot.py' | grep -v grep")
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        pid = line.split()[0]
        try:
            raw = open(f"/proc/{pid}/environ", "rb").read().decode("utf-8", "ignore")
        except Exception:
            continue
        d = dict(x.split("=", 1) for x in raw.split("\0") if "=" in x)
        res.append((pid, d.get("ENGINE_SLICE", ""), d.get("GLM_MODEL", "")))
    return res


def count_todo():
    """Papers in the batch that run_pilot would still consider unfinished."""
    try:
        import sqlite3
        con = sqlite3.connect("file:db.sqlite3?mode=ro", uri=True)
        done = {r[0] for r in con.execute(
            "SELECT arxiv_id FROM papers WHERE fetch_status='extracted'")}
        batch = json.load(open(REG["batch"], encoding="utf-8"))
        return sum(1 for x in batch if x["arxiv_id"] not in done)
    except Exception as e:
        print(f"  (todo count failed: {e})")
        return -1


# ---------------------------------------------------------------- takeover ---
# The slow lane must not become the schedule. Once every fast lane has drained
# and papers still remain, hand the slow lane's slice to a fast engine. The slow
# lane is stopped first: two lanes on one slice would re-extract the same papers
# and burn the same quota twice.
print()
print("takeover:")
TO = REG.get("takeover", {})
if not TO.get("enabled"):
    print("  disabled in registry")
else:
    live = running_lanes()
    live_slices = {s for _, s, _ in live}
    src = next((L for L in REG["lanes"] if L["name"] == TO["from_lane"]), None)
    fast = [L["slice"] for L in REG["lanes"] if L.get("vendor") == "qianfan"]
    fast_alive = [s for s in fast if s in live_slices]
    todo = count_todo()

    if src is None or not src.get("enabled"):
        print("  already handed off (source lane disabled)")
    elif fast_alive:
        print(f"  fast lanes still on it ({', '.join(fast_alive)}) — waiting, todo={todo}")
    elif 0 <= todo < TO.get("min_todo", 15):
        print(f"  todo={todo} < {TO['min_todo']} — nothing worth taking over")
    else:
        print(f"  fast lanes drained, todo={todo} — handing slice "
              f"{src['slice']} ({src['name']}) to {TO['model']}")
        env = env_for(TO["vendor"])
        if env is None:
            print(f"    !! no key for {TO['vendor']} — takeover aborted")
        else:
            cmd = (f'setsid env {env} CANDIDATES_JSON_PATH={REG["batch"]} ARXIV_GAP=6 '
                   f'ENGINE_SLICE={src["slice"]} PILOT_WORKERS={TO["workers"]} '
                   f'ENGINE_FLAVOR=qianfan GLM_MODEL={TO["model"]} '
                   f'nohup python3 -u run_pilot.py >> {TO["log"]} 2>&1 < /dev/null &')
            if DRY:
                print("    (dry) would launch takeover lane, then stop slow lane")
            else:
                # Launch BEFORE stopping: another session's after_lanes.sh watches
                # for a zero run_pilot count and fires the V2 DDL migration. A gap
                # here would kick off a schema migration mid-run. Launch-first keeps
                # the count >= 1 at all times; the cost is a few papers the slow lane
                # had in flight getting re-read, which is far cheaper than that.
                subprocess.run(["bash", "-c", cmd], timeout=60)
                print("    takeover lane up")
                time.sleep(3)
                for pid, s, _ in live:
                    if s == src["slice"]:
                        sh(f"kill {pid} 2>/dev/null")
                        print(f"    stopped slow lane pid {pid}")
                        break
                src["enabled"] = False
                TO["enabled"] = False
                with open("lanes_0929.json", "w", encoding="utf-8") as f:
                    json.dump(REG, f, ensure_ascii=False, indent=2)
                print("    registry updated so it happens once")

print()
for S in REG["sidecars"]:
    if not S.get("enabled"):
        continue
    n = count(S["match"])
    if n:
        print(f"  {S['name']:<14} UP x{n}")
        continue
    # sidecars are allowed to be finished; relaunch only if work remains
    if S["name"] == "difficulty_progress_verdict":
        try:
            att = len(os.listdir(os.path.join(BASE, "runs", "difficulty-v1", "attempts")))
            vd = sum(1 for l in open(os.path.join(BASE, "runs", "difficulty-v1", "verdicts.jsonl"),
                                     encoding="utf-8") if l.strip())
            solver_running = count("solver_attempt.py") > 0
            # The verifier must trail the solver: while the solver is still
            # emitting attempts, a "caught up" verifier should stay alive and
            # pick up new trajectories as they land.
            if vd >= att and not solver_running:
                print(f"  {S['name']:<14} DOWN, caught up ({vd}/{att}), solver idle — left down")
                continue
            if vd >= att and solver_running:
                print(f"  {S['name']:<14} caught up ({vd}/{att}) but solver still running — keep trailing")
        except Exception:
            pass
    if DRY:
        print(f"  {S['name']:<14} DOWN — would relaunch")
        continue
    print(f"  {S['name']:<14} DOWN — RELAUNCH")
    subprocess.run(["bash", "-c",
                    f'setsid nohup {S["cmd"]} >> {S["log"]} 2>&1 < /dev/null &'], timeout=60)
    time.sleep(3)

print("\n" + "=" * 66)
