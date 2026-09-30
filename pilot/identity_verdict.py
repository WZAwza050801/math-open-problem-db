"""Canonical judging pipeline (server-side): read pending_pairs.jsonl,
judge each pair (same/distinct/unsure) with batched LLM calls, store verdicts
in canon_verdicts table. Idempotent + resumable.

Design:
  * 8 pairs per call (matches prototype batched-judging validation)
  * 4 worker threads, each with its own key-rotation loop
  * engine fallback: GLM coding -> Bailian Token Plan qwen3.8-max -> SF Kimi-K2.6
  * checkpoint: canon_verdicts table (INSERT OR REPLACE), pairs with existing
    verdicts are skipped on restart
  * NEVER touches /api/paas/v4 (pay-as-you-go) -- coding endpoint only

Usage:
  python3 identity_verdict.py            # full run
  python3 identity_verdict.py --dry     # dry-run: build prompts, call nothing
"""

import json
import os
import queue
import sqlite3
import sys
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
PAIRS = os.path.join(BASE, "pending_pairs.jsonl")
DB = os.path.join(BASE, "db.sqlite3")
ENV = os.path.join(BASE, ".env")

GLM_BASE = "https://open.bigmodel.cn/api/coding/paas/v4"   # 铁律：coding 端点
TP_BASE = "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
SF_BASE = "https://api.siliconflow.cn/v1"
BATCH = 8
WORKERS = 4
QUOTA_SIGNS = ("1113", "1310", "余额不足", "额度已用", "使用上限")


def load_env():
    env = {}
    with open(ENV, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


ENVV = load_env()
GLM_KEYS = [k for k in (ENVV.get("GLM_CODING_TEAM2_KEY", ""),
                        ENVV.get("GLM_CODING_TEAM_KEY", ""),
                        ENVV.get("GLM_CODING_LITE_KEY", "")) if k]
TP_KEY = ENVV.get("BAILIAN_TOKENPLAN_KEY", "")
KIMI_KEY = ENVV.get("KIMI_CODING_KEY", "")   # 只允许官方 coding plan (api.kimi.com)；SF 按量计费禁用

PROMPT = """You are normalizing mathematical problem statements for a research database.
For each numbered PAIR below, decide whether the two statements describe THE SAME
underlying mathematical problem (same canonical entry, possibly different wording,
generality, or context).
- "same": clearly the same problem
- "distinct": different mathematical problems
- "unsure": cannot decide from the given text

{pairs}

Answer ONLY a JSON array in order:
[{{"i": 1, "verdict": "same"|"distinct"|"unsure", "reason": "<one short sentence>"}}, ...]"""


def short(t, n=700):
    t = " ".join((t or "").split())
    return t[:n] + ("..." if len(t) > n else "")


def call_engine(tag, base, key, model, prompt, timeout=600, extra=None):
    def _post(body):
        req = urllib.request.Request(
            base.rstrip("/") + "/chat/completions", data=json.dumps(body).encode(),
            method="POST",
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r)

    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 3000, "temperature": 0.1}
    if extra:
        body.update(extra)
    try:
        return _post(body)
    except urllib.error.HTTPError as e:
        if e.code == 400 and extra:
            # engine rejected an optional param (e.g. thinking): retry without it
            e.read()
            body = {k: v for k, v in body.items() if k not in extra}
            return _post(body)
        raise


RAW_FAIL_DIR = os.path.join(BASE, "raw_fail")


def dump_raw_fail(tag, resp):
    """Save raw response of a permanently unparsable batch for audit/replay."""
    try:
        os.makedirs(RAW_FAIL_DIR, exist_ok=True)
        fn = os.path.join(RAW_FAIL_DIR, f"{tag}_{datetime.now().strftime('%H%M%S')}.json")
        with open(fn, "w", encoding="utf-8") as f:
            json.dump(resp, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def judge_batch(pairs):
    """pairs: list of dicts with i, a_text, b_text. Returns (verdicts, engine, usage)."""
    blocks = "\n\n".join(
        f"PAIR {p['i']}:\n-- Statement A (paper {p['a_arxiv']}):\n{p['a_text']}\n"
        f"-- Statement B (paper {p['b_arxiv']}):\n{p['b_text']}"
        for p in pairs)
    prompt = PROMPT.format(pairs=blocks)

    # GLM coding keys (rotate on quota wall)
    if GLM_KEYS:
        last = None
        for key in GLM_KEYS:
            for attempt in range(6):
                try:
                    # glm-5.3 is a reasoning model: without disabling thinking it
                    # burns the whole max_tokens budget on reasoning and returns
                    # EMPTY content (finish_reason=length) -> all parse_fail.
                    r = call_engine("glm", GLM_BASE, key, "glm-5.3", prompt,
                                    extra={"thinking": {"type": "disabled"}})
                    return r, "glm-5.3", r.get("usage", {})
                except urllib.error.HTTPError as e:
                    d = e.read().decode("utf-8", "replace")
                    last = f"HTTP {e.code}: {d[:120]}"
                    if e.code == 429 and any(s in d for s in QUOTA_SIGNS):
                        break                      # next key
                    if e.code in (429, 500, 502, 503):
                        time.sleep(30)
                        continue
                    break
                except Exception as e:
                    last = f"{type(e).__name__}"
                    time.sleep(15)
                    continue
        print(f"  [glm] exhausted ({last}) -> Token Plan", flush=True)
    # Token Plan qwen
    if TP_KEY:
        try:
            r = call_engine("tp", TP_BASE, TP_KEY, "qwen3.8-max", prompt, timeout=900)
            return r, "qwen3.8-max", r.get("usage", {})
        except Exception as e:
            print(f"  [tp] failed ({str(e)[:80]}) -> SF Kimi", flush=True)
    # Kimi official coding plan
    if KIMI_KEY:
        for attempt in range(3):
            try:
                r = call_engine("kimi", "https://api.kimi.com/coding/v1", KIMI_KEY, "k3",
                                prompt, timeout=420)
                return r, "kimi-k3", r.get("usage", {})
            except Exception as e:
                print(f"  [kimi] attempt {attempt+1}: {str(e)[:80]}", flush=True)
                time.sleep(20 * (attempt + 1))
    raise RuntimeError("all engines failed")


def worker(wid, q, con_lock, con, stats):
    while True:
        try:
            batch = q.get_nowait()
        except queue.Empty:
            return
        texts = {}
        with con_lock:
            for p in batch:
                for cid in (p["a"], p["b"]):
                    if cid not in texts:
                        r = con.execute(
                            "SELECT p.self_contained, pa.arxiv_id FROM problems p "
                            "JOIN papers pa ON p.arxiv_id=pa.arxiv_id WHERE p.id=?",
                            (cid,)).fetchone()
                        texts[cid] = (r[0] if r else "", r[1] if r else "?")
        payload = []
        for j, p in enumerate(batch, 1):
            payload.append({"i": j, "a_arxiv": texts[p["a"]][1],
                            "b_arxiv": texts[p["b"]][1],
                            "a_text": short(texts[p["a"]][0]),
                            "b_text": short(texts[p["b"]][0])})
        try:
            resp, engine, usage = judge_batch(payload)
            content = resp["choices"][0]["message"]["content"]
            import re
            m = re.search(r"\[.*\]", content, re.S)
            arr = json.loads(m.group(0)) if m else []
            vmap = {int(it["i"]): it for it in arr if isinstance(it, dict)}
            if len(vmap) < len(batch) * 0.8:      # reply mostly unparsable
                raise RuntimeError(
                    f"parsed {len(vmap)}/{len(batch)} verdicts only")
        except Exception as e:
            # one retry through the full fallback chain (different engine
            # family avoids repeating the same parsing failure)
            try:
                resp, engine, usage = judge_batch(payload)
                content = resp["choices"][0]["message"]["content"]
                import re
                m = re.search(r"\[.*\]", content, re.S)
                arr = json.loads(m.group(0)) if m else []
                vmap = {int(it["i"]): it for it in arr if isinstance(it, dict)}
            except Exception as e2:
                print(f"  [w{wid}] batch failed permanently: {str(e2)[:100]}", flush=True)
                try:
                    dump_raw_fail(f"batch_w{wid}", resp)   # resp may be undefined if call itself failed
                except Exception:
                    pass
                with con_lock:
                    for p in batch:
                        con.execute(
                            "INSERT OR REPLACE INTO canon_verdicts VALUES (?,?,?,?,?,?)",
                            (p["a"], p["b"], "parse_fail", str(e2)[:150], "-", datetime.now().isoformat(timespec='seconds')))
                    con.commit()
                stats["parse_fail"] += len(batch)
                q.task_done()
                continue
        with con_lock:
            for j, p in enumerate(batch, 1):
                it = vmap.get(j, {"verdict": "parse_fail",
                                  "reason": "missing in model reply"})
                con.execute(
                    "INSERT OR REPLACE INTO canon_verdicts VALUES (?,?,?,?,?,?)",
                    (p["a"], p["b"], it.get("verdict", "parse_fail"),
                     it.get("reason", "")[:150], engine,
                     datetime.now().isoformat(timespec='seconds')))
                stats[it.get("verdict", "parse_fail")] = stats.get(it.get("verdict", "parse_fail"), 0) + 1
            con.commit()
        stats["calls"] += 1
        ti, to = usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)
        stats["tin"] += ti
        stats["tout"] += to
        if stats["calls"] % 10 == 0:
            print(f"  [progress] calls={stats['calls']} pairs~{stats['calls']*BATCH} "
                  f"in={stats['tin']:,} out={stats['tout']:,}", flush=True)
        q.task_done()


def main():
    dry = "--dry" in sys.argv
    pairs = [json.loads(l) for l in open(PAIRS, encoding="utf-8")]
    con = sqlite3.connect(DB, check_same_thread=False)
    con.execute("PRAGMA busy_timeout=60000")
    con.execute(
        "CREATE TABLE IF NOT EXISTS canon_verdicts ("
        " a_id TEXT, b_id TEXT, verdict TEXT, reason TEXT, engine TEXT, judged_at TEXT)")
    done = {r[0] for r in con.execute(
        "SELECT a_id || '|' || b_id FROM canon_verdicts "
        "WHERE verdict IN ('same','distinct','unsure')")}
    todo = [p for p in pairs if f"{p['a']}|{p['b']}" not in done]
    print(f"[judge] pairs={len(pairs)} done={len(pairs)-len(todo)} todo={len(todo)}", flush=True)

    # attach texts for batches
    batches = []
    for s in range(0, len(todo), BATCH):
        batches.append(todo[s:s + BATCH])
    if dry:
        est_calls = len(batches)
        est_in = est_calls * 8000
        print(f"[dry] would make ~{est_calls} calls, ~{est_in:,} prompt tokens, "
              f"~{est_calls*4000:,} completion tokens")
        print(f"[dry] engines: glm keys={len(GLM_KEYS)} tp={'Y' if TP_KEY else 'N'} "
              f"sf={'Y' if SF_KEY else 'N'}")
        return

    q = queue.Queue()
    for b in batches:
        q.put(b)
    con_lock = threading.Lock()
    stats = {"calls": 0, "tin": 0, "tout": 0}
    threads = [threading.Thread(target=worker, args=(i, q, con_lock, con, stats),
                                daemon=True)
               for i in range(min(WORKERS, len(batches)))]
    t0 = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"\n[judge] DONE in {(time.time()-t0)/60:.0f}min  "
          f"calls={stats['calls']} in={stats['tin']:,} out={stats['tout']:,}", flush=True)
    for k, v in sorted(stats.items()):
        if k not in ("calls", "tin", "tout"):
            print(f"   {k}: {v}", flush=True)


if __name__ == "__main__":
    main()
