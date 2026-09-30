"""Abstract-level triage for backfill papers via Qwen Token Plan (node01).

Classifies every paper-with-abstract: does the paper POSE a conjecture/open
problem, PROVE one, or merely USE/mention one (or none)? pose/prove are
extraction-worthy. Complements the regex screen (catches phrasing without
keywords). Checkpoint-resume; circuit breaker on quota errors.

Usage: python3 triage_qwen.py [limit]
Input:  triage_input.jsonl   Output: triage_qwen.jsonl
"""
import json, os, re, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import threading

BASE = os.path.dirname(os.path.abspath(__file__))
IN = os.path.join(BASE, "triage_input.jsonl")
OUT = os.path.join(BASE, "triage_qwen.jsonl")
URL = "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions"
KEY = os.environ.get("BAILIAN_TOKENPLAN_KEY", "")
MODEL = "qwen3.8-max"
WORKERS = 4

PROMPT = """你是数学论文筛选器。根据标题和摘要判断这篇论文与"开放问题/猜想"的关系：

- pose: 提出了新的猜想或公开问题
- prove: 证明（或否定）了某个已有的猜想/开放问题
- use: 仅在论证中引用/依赖某猜想（如 "assuming the X conjecture"），本身不提出也不证明
- no: 与猜想/开放问题无关

只输出 JSON：{"v": "pose|prove|use|no", "why": "不超过15字的依据"}"""

def build_prompt(title, abstract):
    return (PROMPT + """

标题：""" + title + """
摘要：""" + abstract)

lock = threading.Lock()
stats = {"n": 0, "pose": 0, "prove": 0, "use": 0, "no": 0, "err": 0, "parse": 0}
quota_killed = threading.Event()
t0 = time.time()


def call(payload):
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": payload}],
        "temperature": 0,
        "max_tokens": 200,
        "enable_thinking": False,
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)
    if "choices" not in d:
        raise RuntimeError(f"no-choices: {json.dumps(d, ensure_ascii=False)[:200]}")
    return d["choices"][0]["message"]["content"]


def process(item):
    if quota_killed.is_set():
        return
    rec = {"doi": item["doi"], "regex_hit": item["regex_hit"]}
    if not item["regex_hit"]:  # regex positives skip the call, auto pose/prove pool
        try:
            txt = call(build_prompt(item["title"], item["abstract"]))
            m = re.search(r'\{[^}]*\}', txt, re.S)
            if m:
                try:
                    j = json.loads(m.group(0))
                    if isinstance(j, dict):
                        rec["v"] = str(j.get("v", "no_v"))
                        rec["why"] = str(j.get("why", ""))[:60]
                    else:
                        rec["v"], rec["parse"] = "parse_fail", True
                        rec["raw"] = txt[:120]
                except json.JSONDecodeError:
                    rec["v"], rec["parse"] = "parse_fail", True
                    rec["raw"] = txt[:120]
            else:
                rec["v"], rec["parse"] = "parse_fail", True
                rec["raw"] = txt[:120]
        except urllib.error.HTTPError as e:
            rec["v"], rec["err"] = f"http_{e.code}", True
            rec["emsg"] = e.read().decode()[:200] if e.code != 429 else "rate-limited"
            if e.code in (429, 402, 403):
                with lock:
                    stats["err"] += 1
                if stats["err"] >= 5:
                    quota_killed.set()
                    print("[triage] QUOTA/AUTH circuit breaker fired", flush=True)
                return
        except Exception as e:
            rec["v"], rec["err"] = f"{type(e).__name__}", True
            rec["emsg"] = str(e)[:200]
    else:
        rec["v"] = "regex_hit"  # keep, no call needed
    with lock:
        with open(OUT, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        stats["n"] += 1
        v = rec.get("v", "")
        if v in ("pose", "prove", "use", "no"):
            stats[v] += 1
        elif v == "regex_hit":
            stats["regex_hit"] = stats.get("regex_hit", 0) + 1
        else:
            stats["err"] += 1
        n = stats["n"]
        if n % 100 == 0:
            el = time.time() - t0
            eta = el / n * (TOTAL - n) / 60
            print(f"[{n}/{TOTAL}] pose={stats['pose']} prove={stats['prove']} "
                  f"use={stats['use']} no={stats['no']} err={stats['err']} "
                  f"eta={eta:.0f}min", flush=True)


rows = [json.loads(l) for l in open(IN, encoding="utf-8") if l.strip()]
done = set()
if os.path.exists(OUT):
    for l in open(OUT, encoding="utf-8"):
        if l.strip():
            try:
                done.add(json.loads(l)["doi"])
            except Exception:
                pass
todo = [r for r in rows if r["doi"] not in done]
limit = int(sys.argv[1]) if len(sys.argv) > 1 else len(todo)
todo = todo[:limit]
TOTAL = len(todo)
print(f"[triage] total={len(rows)} done={len(done)} todo={TOTAL} "
      f"key_set={bool(KEY)}", flush=True)
if not KEY:
    print("[triage] FATAL: BAILIAN_TOKENPLAN_KEY not set")
    sys.exit(1)

with ThreadPoolExecutor(max_workers=WORKERS) as ex:
    list(ex.map(process, todo))

print(f"[triage] DONE n={stats['n']} pose={stats['pose']} "
      f"prove={stats['prove']} use={stats['use']} no={stats['no']} "
      f"err={stats['err']} parse={stats['parse']} "
      f"elapsed={(time.time() - t0) / 60:.0f}min", flush=True)
