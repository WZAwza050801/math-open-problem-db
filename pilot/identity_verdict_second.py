#!/usr/bin/env python3
"""Second-opinion pass on canonical judgments (server-side).
Re-judges with an INDEPENDENT engine (team2 glm-5.3, single-pair calls):
  1) all 'unsure' pairs from canon_verdicts (conservative non-merges)
  2) all contradiction pairs (33 blocked clusters / 84 pairs)
Results go to a SEPARATE table canon_verdicts_2nd — never touches canon_verdicts.
Resumable via (a_id,b_id,source) dedup.
Usage: python3 identity_verdict_second.py
"""
import json, os, sqlite3, sys, threading, time, queue, re, urllib.request, urllib.error
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "db.sqlite3")
ENV = os.path.join(BASE, ".env")
CONTRA = os.path.join(BASE, "runs", "canon-20260926T203100Z-v1", "contradiction_pairs.json")
TABLE = "canon_verdicts_2nd"
BASE_URL = os.environ.get("SO_URL", "https://open.bigmodel.cn/api/coding/paas/v4")
MODEL = os.environ.get("SO_MODEL", "glm-5.3")
WORKERS = int(os.environ.get("SO_WORKERS", "3"))

env = {}
for line in open(ENV, encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
KEY = os.environ.get("SO_KEY") or env.get("GLM_CODING_TEAM2_KEY", "")
if not KEY:
    sys.exit("no team2 key found")

PROMPT = """You are normalizing mathematical problem statements for a research database.
Decide whether the two statements below describe THE SAME underlying mathematical
problem (same canonical entry, possibly different wording, generality, or context).
- "same": clearly the same problem
- "distinct": different mathematical problems
- "unsure": cannot decide from the given text
Pay special attention to: one statement being a special case / generalization of
the other (that is "distinct" unless the weaker one is merely a rephrasing).

-- Statement A (paper {ar}):
{a}

-- Statement B (paper {br}):
{b}

Answer ONLY JSON: {{"verdict": "same"|"distinct"|"unsure", "confidence": 0-1, "reason": "<one short sentence>"}}"""


def short(t, n=900):
    t = " ".join((t or "").split())
    return t[:n] + ("..." if len(t) > n else "")


def call(prompt):
    body = {"model": MODEL, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000, "temperature": 0.1,
            "thinking": {"type": "disabled"}}
    last = None
    for i in range(4):
        try:
            req = urllib.request.Request(BASE_URL.rstrip("/") + "/chat/completions",
                                         data=json.dumps(body).encode(),
                                         headers={"Authorization": "Bearer " + KEY,
                                                  "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            last = f"http_{e.code}"
            if e.code == 429 and i < 3:
                time.sleep(30 * (i + 1)); continue
            raise RuntimeError(last)
        except Exception as e:
            last = str(e)[:80]
            if i < 3:
                time.sleep(15); continue
            raise RuntimeError(last)


def judge_one(p, texts):
    a, b = texts[p["a"]], texts[p["b"]]
    txt = call(PROMPT.format(ar=a[1], br=b[1], a=short(a[0]), b=short(b[0])))
    content = (txt.get("choices") or [{}])[0].get("message", {}).get("content") or ""
    cands = re.findall(r"\{.*?\}", content, re.S)
    for c in cands:
        try:
            j = json.loads(c)
            if isinstance(j, dict) and j.get("verdict") in ("same", "distinct", "unsure"):
                return j["verdict"], str(j.get("confidence", ""))[:6], str(j.get("reason", ""))[:150]
        except Exception:
            continue
    return "parse_fail", "", content[:120]


def main():
    con = sqlite3.connect(DB, check_same_thread=False)
    con.execute("PRAGMA busy_timeout=60000")
    con.execute(f"CREATE TABLE IF NOT EXISTS {TABLE} ("
                " a_id TEXT, b_id TEXT, source TEXT, verdict TEXT, confidence TEXT,"
                " reason TEXT, engine TEXT, judged_at TEXT,"
                " PRIMARY KEY (a_id, b_id, source))")
    done = {r[0] for r in con.execute(f"SELECT a_id||'|'||b_id||'|'||source FROM {TABLE} "
                                      "WHERE verdict IN ('same','distinct','unsure')")}
    tasks = []
    for r in con.execute("SELECT a_id, b_id FROM canon_verdicts WHERE verdict='unsure'"):
        tasks.append({"a": r[0], "b": r[1], "src": "unsure"})
    contra = json.load(open(CONTRA, encoding="utf-8"))
    for p in contra:
        tasks.append({"a": p["a"], "b": p["b"], "src": "contradiction"})
    todo = [t for t in tasks if f"{t['a']}|{t['b']}|{t['src']}" not in done]
    print(f"[2nd-opinion] total={len(tasks)} done={len(tasks)-len(todo)} todo={len(todo)}", flush=True)

    texts = {}
    ids = {t["a"] for t in tasks} | {t["b"] for t in tasks}
    for cid in ids:
        r = con.execute(
            "SELECT p.self_contained, pa.arxiv_id FROM problems p "
            "JOIN papers pa ON p.arxiv_id=pa.arxiv_id WHERE p.id=?", (cid,)).fetchone()
        texts[cid] = (r[0] if r else "", r[1] if r else "?")

    q = queue.Queue()
    for t in todo:
        q.put(t)
    lock = threading.Lock()
    stats = {"n": 0}

    def worker():
        while True:
            try:
                t = q.get_nowait()
            except queue.Empty:
                return
            try:
                v, cf, reason = judge_one(t, texts)
            except Exception as e:
                v, cf, reason = "error", "", str(e)[:100]
            with lock:
                con.execute(f"INSERT OR REPLACE INTO {TABLE} VALUES (?,?,?,?,?,?,?,?)",
                            (t["a"], t["b"], t["src"], v, cf, reason, MODEL,
                             datetime.now().isoformat(timespec="seconds")))
                con.commit()
                stats["n"] += 1
                stats[v] = stats.get(v, 0) + 1
                if stats["n"] % 10 == 0:
                    print(f"  [progress] {stats['n']}/{len(todo)} {dict((k, val) for k, val in stats.items() if k != 'n')}", flush=True)

    ths = [threading.Thread(target=worker, daemon=True) for _ in range(min(WORKERS, len(todo)))]
    t0 = time.time()
    for t in ths:
        t.start()
    for t in ths:
        t.join()
    print(f"[2nd-opinion] DONE {(time.time()-t0)/60:.0f}min {dict((k, v) for k, v in stats.items() if k != 'n')}", flush=True)


if __name__ == "__main__":
    main()
