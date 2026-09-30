#!/usr/bin/env python3
"""Ops board — one screen for the whole pipeline.

Shows: machine headroom, per-lane liveness + throughput, M13 solver/verifier
progress, DB counters, queue remaining, and a health verdict per lane.

Read-only. Never starts or stops anything (that is ops_watchdog.py).
Usage:  python3 ops_board.py            # snapshot
        python3 ops_board.py --watch 60 # refresh every 60s
"""
import json, os, re, sqlite3, subprocess, sys, time, collections
from datetime import datetime

BASE = "/home/user/Wholeworks/wanganan/math_openproblem/pilot"
os.chdir(BASE)
REG = json.load(open("lanes_0929.json", encoding="utf-8"))


def sh(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=45).stdout.strip()
    except Exception:
        return ""


def alive(match):
    out = sh(f"ps -eo pid,etime,cmd | grep -F '{match}' | grep -v grep")
    rows = []
    for ln in out.splitlines():
        p = ln.split(None, 2)
        if len(p) == 3:
            rows.append((p[0], p[1]))
    return rows


def lane_progress(log):
    """Last '[i/n] extracted' line + how stale the log is."""
    if not os.path.exists(log):
        return None, None, None
    txt = sh(f"grep -E '^\\[[0-9]+/' '{log}' | tail -1")
    m = re.search(r"\[(\d+)/(\d+)\].*cards=(\d+)", txt)
    stale = None
    try:
        stale = int(time.time() - os.path.getmtime(log))
    except Exception:
        pass
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3)), stale
    return None, None, None, stale


def bar(done, total, w=18):
    if not total:
        return "-" * w
    n = int(w * min(1.0, done / total))
    return "#" * n + "." * (w - n)


print("=" * 78)
print("OPEN PROBLEM DB — OPS BOARD", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 78)

# ---------- machine ----------
load = sh("cat /proc/loadavg").split()
cpu = os.cpu_count()
print(f"\n[HOST]  cpus={cpu}  load1={load[0] if load else '?'}  "
      f"({float(load[0])/max(cpu,1)*100:.0f}% of capacity)" if load else "\n[HOST]")
print("  disk:", sh("df -h . | awk 'NR==2{print $4\" free (\"$5\" used)\"}'"))

# ---------- lanes ----------
print("\n[EXTRACTION LANES]")
print(f"  {'lane':<10} {'pid':>7} {'up':>9} {'progress':>10} {'cards':>7} {'stale':>7}  health")
tot_done = tot_cards = 0
for L in REG["lanes"]:
    if not L.get("enabled"):
        continue
    ps = alive("run_pilot.py")
    # match by log path is not in cmd; use order-independence: count running lanes
    prog = lane_progress(L["log"])
    i, n, cards, stale = prog if prog and len(prog) == 4 else (None, None, None, None)
    mark = "DOWN" if stale is None or stale > 900 else ("IDLE?" if stale > 420 else "ok")
    if i and n:
        tot_done += i
        tot_cards += cards or 0
    print(f"  {L['name']:<10} {'':>7} {'':>9} "
          f"{(str(i)+'/'+str(n)) if i else '-':>10} {cards if cards else '-':>7} "
          f"{(str(stale)+'s') if stale is not None else '-':>7}  {mark}")
n_run = len(alive("run_pilot.py"))
n_exp = sum(1 for L in REG["lanes"] if L.get("enabled"))
print(f"  running={n_run}/{n_exp}   summed progress: {tot_done} papers, {tot_cards} cards this run")

# ---------- M13 ----------
print("\n[M13 DIFFICULTY]")
RUN = os.path.join(BASE, "runs", "difficulty-v1")
ATT = os.path.join(RUN, "attempts")
att = collections.defaultdict(set)
if os.path.isdir(ATT):
    for fn in os.listdir(ATT):
        try:
            u, t = fn.replace(".json", "").split("__")
            att[u].add(t)
        except ValueError:
            pass
vd = collections.defaultdict(set)
lv = collections.Counter()
n_pf = 0
vp = os.path.join(RUN, "verdicts.jsonl")
n_v = 0
if os.path.exists(vp):
    for l in open(vp, encoding="utf-8"):
        if l.strip():
            d = json.loads(l)
            vd[d["uid"]].add(str(d.get("traj")))
            n_v += 1
            if d.get("level") is None:
                n_pf += 1
            else:
                lv[d["level"]] += 1
n_att = sum(len(v) for v in att.values())
pend = n_att - n_v
for S in REG["sidecars"]:
    a = alive(S["match"])
    print(f"  {S['name']:<14} {'UP pid='+a[0][0]+' '+a[0][1] if a else 'DOWN':<22}")
print(f"  attempts={n_att} ({len(att)} problems, {sum(1 for v in att.values() if len(v)>=3)} complete)")
print(f"  verdicts={n_v}  unjudged={pend}  parse_fail={n_pf}")
print(f"  level distribution: {dict(sorted(lv.items()))}")

# ---------- DB ----------
print("\n[DATABASE]")
con = sqlite3.connect("file:db.sqlite3?mode=ro", uri=True)
p = con.execute("SELECT COUNT(*) FROM papers").fetchone()[0]
c = con.execute("SELECT COUNT(*) FROM problems").fetchone()[0]
cn = con.execute("SELECT COUNT(*) FROM problems WHERE canonical_uid IS NOT NULL").fetchone()[0]
print(f"  papers={p}  cards={c}  merged={cn}  UNMERGED={c-cn}")
dims = dict(con.execute("SELECT dimension,COUNT(*) FROM score_aggregates GROUP BY dimension"))
print(f"  score_aggregates: {dims}")
try:
    b = json.load(open(REG["batch"], encoding="utf-8"))
    st = {r[0]: r[1] for r in con.execute("SELECT arxiv_id,fetch_status FROM papers")}
    cc = collections.Counter(st.get(x["arxiv_id"], "NOT_STARTED") for x in b)
    done = cc.get("extracted", 0) + cc.get("no_fulltext", 0)
    print(f"  batch {REG['batch']}: {done}/{len(b)} done  remaining={len(b)-done}")
    print(f"    {dict(cc)}")
except Exception as e:
    print("  batch:", e)

# ---------- backlog ----------
print("\n[BLOCKING / NEXT]")
if n_run < n_exp:
    print(f"  !! {n_exp-n_run} lane(s) down — run ops_watchdog.py to relaunch")
if pend > 0:
    print(f"  !! {pend} M13 trajectories unjudged (verifier must finish before IRT fit)")
if n_pf > 0:
    print(f"  !! {n_pf} parse_fail verdicts will never be retried — purge them first")
if c - cn > 0:
    print(f"  -- {c-cn} cards await canonical merge (blocked until extraction ends)")
print("\n" + "=" * 78)
