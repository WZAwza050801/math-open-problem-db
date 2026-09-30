#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pipeline_daemon.py — node01 常驻流水线调度器 (v1, 2026-09-29)

循环逻辑（每 5 分钟一拍）：
  1. MONITOR  : 抽取车道 / M13 是否存活；心跳写日志
  2. FEED     : 合并待抽取池 -> next_batch_v2_0929.json（不足则先做引用网络扩充）
  3. PREFETCH : 预下载 LaTeX（_prefetch_latex_0929.py，断点安全）
  4. EXTRACT  : 按可用 key 铺车道（ENGINE_SLICE，PILOT_WORKERS=3）
  5. DOWNSTREAM : 抽取批次完成后 -> non_proposition_triage -> identity_verdict -> identity_verdict_second
                （三个脚本全部原生断点续跑，重复调用无害）
  6. 循环

安全约束：
  - 不杀任何现存进程；只在自己启动的车道上工作
  - pool 空且引用扩充失败 -> 空转告警，不瞎抓
  - 所有子步骤失败 -> 记日志下拍重试（nap/canon 天然幂等）
"""
import json, os, re, subprocess, sys, time, glob
from datetime import datetime

BASE = "/home/user/Wholeworks/wanganan/math_openproblem/pilot"
LOG = os.path.join(BASE, "logs", "daemon_0929.log")
BATCH_FILE = os.path.join(BASE, "next_batch_v2_0929.json")
POOL_FILES = ["five_journal_backfill.json", "next_batch.json", "batch400.json", "batch_retry.json"]   # 五刊补全最优先（安安 9/29 拍板）
CITATIONS = os.path.join(BASE, "citations.jsonl")
CITE_META = os.path.join(BASE, "citations_meta_cache.jsonl")   # ocid -> metadata 缓存
POOL_MIN = 50          # 池子低于此数触发引用扩充
BATCH_SIZE = 300       # 每批最多喂多少篇
LITE_RESET_AT = "2026-09-30 09:40"   # GLM lite 周配额解禁时间

os.chdir(BASE)

def log(msg):
    line = f"{datetime.now().strftime('%m-%d %H:%M:%S')} {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def sh(cmd, timeout=60):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)

def env_dict():
    d = {}
    for line in open(os.path.join(BASE, ".env"), encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            d[k.strip()] = v.strip().strip('"').strip("'")
    return d

ENV = env_dict()
QF_KEY = open(os.path.join(BASE, ".qianfan_key")).read().strip() if os.path.exists(os.path.join(BASE, ".qianfan_key")) else ""

def now_past(s):
    return datetime.now() >= datetime.strptime(s, "%Y-%m-%d %H:%M")

# ---------------------------------------------------------------- 状态探测
def pgrep_count(pattern):
    r = sh(f"pgrep -fc '{pattern}'")
    try:
        return int(r.stdout.strip() or 0)
    except ValueError:
        return 0

def extract_lanes_running():
    return pgrep_count("run_pilot.py")

def difficulty_running():
    return pgrep_count("solver_attempt.py")

# ---------------------------------------------------------------- FEED: 池合并 + 引用扩充
def db_have():
    import sqlite3
    con = sqlite3.connect(f"file:{BASE}/db.sqlite3?mode=ro", uri=True)
    have = {r[0] for r in con.execute("SELECT arxiv_id FROM papers")}
    con.close()
    return have

def merge_pool(have):
    seen, merged = set(), []
    for name in POOL_FILES:
        p = os.path.join(BASE, name)
        if not os.path.exists(p):
            continue
        try:
            b = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        for x in b if isinstance(b, list) else []:
            aid = x.get("arxiv_id")
            if not aid or aid in have or aid in seen:
                continue
            seen.add(aid)
            merged.append(x)
    return merged

ARXIV_DOI = re.compile(r"10\.48550/arxiv\.(\d{4}\.\d{4,5})(v\d+)?", re.I)

def citation_expand(have):
    """OpenCitations 引用网络扩充：解析 citing works 的元数据，收 arXiv DOI 的论文进 batch400.json"""
    ocids, order = set(), []
    for line in open(CITATIONS, encoding="utf-8"):
        try:
            rec = json.loads(line)
        except Exception:
            continue
        for c in rec.get("citations") or []:
            oci = (c.get("citing") or c.get("oci") or "").replace("omid:", "")
            if oci and oci not in ocids:
                ocids.add(oci)
                order.append(oci)
    log(f"[expand] citing ocids total {len(order)}")

    cache = {}
    if os.path.exists(CITE_META):
        for line in open(CITE_META, encoding="utf-8"):
            try:
                d = json.loads(line)
                cache[d["ocid"]] = d
            except Exception:
                continue
    todo = [o for o in order if o not in cache]
    log(f"[expand] meta cached {len(cache)}, to fetch {len(todo)}")

    if todo:
        import urllib.request
        URL = "https://opencitations.net/index/api/v2/metadata"
        fetched = 0
        with open(CITE_META, "a", encoding="utf-8") as out:
            for i in range(0, min(len(todo), 20000), 200):
                chunk = todo[i:i+200]
                body = " ".join(chunk).encode()
                req = urllib.request.Request(URL, data=body,
                                             headers={"Content-Type": "text/plain",
                                                      "User-Agent": "open-problem-pipeline/1.0"})
                try:
                    with urllib.request.urlopen(req, timeout=90) as resp:
                        rows = json.loads(resp.read().decode())
                    if not isinstance(rows, list):
                        rows = [rows]
                    for ocid, row in zip(chunk, rows):   # 按位对齐；缺失位为 null
                        if not row:
                            continue
                        if isinstance(row, str):
                            try:
                                row = json.loads(row)
                            except Exception:
                                continue
                        if not isinstance(row, dict):
                            continue
                        rec = {"ocid": ocid, "doi": row.get("doi") or "",
                               "title": (row.get("title") or "")[:300],
                               "year": row.get("pub_date") or row.get("year") or ""}
                        out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                        cache[ocid] = rec
                    fetched += len(chunk)
                    out.flush()
                    time.sleep(1.2)   # OpenCitations 礼貌限速
                except Exception as e:
                    log(f"[expand] fetch fail at {i}: {str(e)[:80]}")
                    time.sleep(5)
        log(f"[expand] fetched ~{fetched} metadata rows")

    added = 0
    pool = json.load(open(os.path.join(BASE, "batch400.json"), encoding="utf-8")) \
        if os.path.exists(os.path.join(BASE, "batch400.json")) else []
    seen_pool = {x.get("arxiv_id") for x in pool}
    for ocid, m in cache.items():
        doi = m.get("doi") or ""
        mt = ARXIV_DOI.match(doi)
        if not mt:
            continue
        aid = mt.group(1)
        if aid in have or aid in seen_pool:
            continue
        seen_pool.add(aid)
        pool.append({"arxiv_id": aid, "title": (m.get("title") or "")[:200],
                     "source_file": "cite_expand", "pub_year": m.get("year") or ""})
        added += 1
    if added:
        json.dump(pool, open(os.path.join(BASE, "batch400.json"), "w", encoding="utf-8"),
                  ensure_ascii=False)
    log(f"[expand] new arxiv candidates appended to batch400.json: {added}")
    return added

# ---------------------------------------------------------------- EXTRACT: 车道
def build_lanes():
    """返回 [(name, env_dict)]，只含探测可用的引擎"""
    lanes = []
    team = ENV.get("GLM_CODING_TEAM_KEY", "")
    team2 = ENV.get("GLM_CODING_TEAM2_KEY", "")
    lite = ENV.get("GLM_CODING_LITE_KEY", "")
    if team and team2:
        lanes.append(("l1_glm_team12", {"GLM_KEYS": f"{team},{team2}"}))
    elif team:
        lanes.append(("l1_glm_team", {"GLM_KEYS": team}))
    elif team2:
        lanes.append(("l1_glm_team2", {"GLM_KEYS": team2}))
    if QF_KEY:
        lanes.append(("l3_qf_dsv4", {"GLM_BASE_URL": "https://qianfan.baidubce.com/v2/tokenplan/personal",
                                     "GLM_KEYS": QF_KEY, "GLM_MODEL": "deepseek-v4-pro",
                                     "ENGINE_FLAVOR": "qianfan"}))
        lanes.append(("l4_qf_kimi", {"GLM_BASE_URL": "https://qianfan.baidubce.com/v2/tokenplan/personal",
                                     "GLM_KEYS": QF_KEY, "GLM_MODEL": "kimi-k2.6",
                                     "ENGINE_FLAVOR": "qianfan"}))
    if lite and now_past(LITE_RESET_AT):
        lanes.append(("l5_glm_lite", {"GLM_KEYS": lite}))
    return lanes

def launch_lanes(candidates_n):
    lanes = build_lanes()
    n = len(lanes)
    if n == 0:
        log("[extract] no lanes available, skip")
        return 0
    log(f"[extract] launching {n} lanes for {candidates_n} papers")
    for i, (name, extra) in enumerate(lanes, 1):
        env = dict(os.environ)
        env.update(extra)
        env["CANDIDATES_JSON_PATH"] = BATCH_FILE
        env["ENGINE_SLICE"] = f"{i}/{n}"
        env["PILOT_WORKERS"] = "3"
        env["ARXIV_GAP"] = "6"
        logf = open(f"logs/daemon_lane_{name}.log", "ab")
        subprocess.Popen(["setsid", "python3", "-u", "run_pilot.py"],
                         env=env, stdout=logf, stderr=subprocess.STDOUT,
                         stdin=subprocess.DEVNULL, start_new_session=True)
        log(f"[extract] lane {i}/{n} {name} launched -> logs/daemon_lane_{name}.log")
        time.sleep(6)
    return n

# ---------------------------------------------------------------- 主循环
def main():
    log("[daemon] started, pid " + str(os.getpid()))
    downstream_done_for_batch = False   # 本批抽取是否已跑过下游
    last_lane_count = -1

    while True:
        try:
            lanes_n = extract_lanes_running()
            difficulty_n = difficulty_running()

            # --- 有车道在跑：监控 + 心跳
            if lanes_n > 0:
                if lanes_n != last_lane_count:
                    log(f"[monitor] extraction lanes running: {lanes_n}")
                    last_lane_count = lanes_n
                    downstream_done_for_batch = False
                if difficulty_n:
                    log(f"[monitor] heartbeat: lanes={lanes_n} difficulty=ok")
                else:
                    log(f"[monitor] heartbeat: lanes={lanes_n} difficulty=FINISHED_or_dead")
                time.sleep(300)
                continue

            # --- 抽取空闲：先看本批是否收尾（跑下游）
            if not downstream_done_for_batch and last_lane_count > 0:
                log("[downstream] extraction batch finished, running nap -> canon -> 2nd opinion")
                for cmd, tag in [("python3 -u non_proposition_triage.py", "nap"),
                                 ("python3 -u identity_verdict.py", "identity_verdict"),
                                 ("python3 -u identity_verdict_second.py", "identity_verdict_2nd")]:
                    log(f"[downstream] >>> {tag}")
                    r = sh(cmd, timeout=3600 * 6)
                    log(f"[downstream] <<< {tag} rc={r.returncode} tail={r.stdout.strip().splitlines()[-1][:120] if r.stdout.strip() else '(empty)'}")
                downstream_done_for_batch = True
                last_lane_count = -1
                continue

            # --- 抽取空闲且下游已跑：喂下一批
            have = db_have()
            pool = merge_pool(have)
            log(f"[feed] pool size (not in db): {len(pool)}")
            if len(pool) < POOL_MIN:
                log("[feed] pool low -> citation expansion")
                try:
                    citation_expand(have)
                    pool = merge_pool(have)
                    log(f"[feed] pool after expansion: {len(pool)}")
                except Exception as e:
                    log(f"[feed] expansion failed: {str(e)[:120]}")
            if len(pool) < POOL_MIN:
                log("[feed] pool still low, idle 30min (需人工扩充候选源)")
                time.sleep(1800)
                continue

            batch = pool[:BATCH_SIZE]
            json.dump(batch, open(BATCH_FILE, "w", encoding="utf-8"), ensure_ascii=False)
            log(f"[feed] batch written: {len(batch)} papers -> {os.path.basename(BATCH_FILE)}")

            # 预下载 LaTeX（限量 30 分钟，防阻塞；run_pilot 自己也会边跑边抓）
            r = sh("timeout 1800 python3 -u _prefetch_latex_0929.py", timeout=1900)
            log(f"[prefetch] rc={r.returncode} (tail) {r.stdout.strip().splitlines()[-1][:100] if r.stdout.strip() else ''}")

            launched = launch_lanes(len(batch))
            if launched:
                downstream_done_for_batch = False
                last_lane_count = launched
            time.sleep(300)
        except Exception as e:
            log(f"[daemon] cycle error: {type(e).__name__}: {str(e)[:200]}")
            time.sleep(300)

if __name__ == "__main__":
    main()
