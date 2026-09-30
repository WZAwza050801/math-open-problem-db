#!/usr/bin/env python3
"""not_a_proposition AI prefilter (server-side, stage 1 of the two-stage review).
Re-reads every card flagged paper_time_status='not_a_proposition' and triages:
  restated_open  — actually a genuine open problem / conjecture statement
                   (mis-flagged; candidate to flip back to open)
  background     — discusses someone else's known open problem, not posed here
  confirm        — genuinely not a proposition (method/comment/definition)
  unsure         — cannot decide
Output: non_proposition_triage.jsonl (checkpoint, resumable). NEVER updates the DB —
human review decides flips; this only builds the shortlist.
Engine: team2 glm-5.3 (separate quota pool from extraction 37cf).
Usage: python3 non_proposition_triage.py [limit]
"""
import json, os, sqlite3, sys, threading, time, queue, re, urllib.request, urllib.error
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "db.sqlite3")
ENV = os.path.join(BASE, ".env")
OUT = os.path.join(BASE, "non_proposition_triage.jsonl")
BASE_URL = os.environ.get("NAP_URL", "https://open.bigmodel.cn/api/coding/paas/v4")
MODEL = os.environ.get("NAP_MODEL", "glm-5.3")
WORKERS = int(os.environ.get("NAP_WORKERS", "4"))

env = {}
for line in open(ENV, encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
KEY = os.environ.get("NAP_KEY") or env.get("GLM_CODING_TEAM2_KEY", "")
if not KEY:
    sys.exit("no team2 key found")

PROMPT = """You triage math-paper statements for a research database of open problems.
The statement below was auto-flagged as "not_a_proposition". Decide which it really is:

- "restated_open": a genuine open problem / conjecture / question is being posed or
  formally restated (mis-flag; candidate to restore as an open problem)
- "background": mentions/discusses a known open problem but the paper does not pose it
  (survey context, related-work remarks)
- "confirm": genuinely not a problem statement (method description, comment,
  definition, remark, exercise answer, etc.)
- "unsure": cannot decide from the given text

Statement (from paper {arxiv}):
{quote}

Label given by the extractor: {label}
Rationale: {rationale}

Answer ONLY JSON: {{"verdict": "restated_open"|"background"|"confirm"|"unsure", "reason": "<one short sentence>"}}"""


def call(prompt):
    body = {"model": MODEL, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 400, "temperature": 0.1, "thinking": {"type": "disabled"}}
    last = None
    for i in range(4):
        try:
            req = urllib.request.Request(BASE_URL.rstrip("/") + "/chat/completions",
                                         data=json.dumps(body).encode(),
                                         headers={"Authorization": "Bearer " + KEY,
                                                  "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=240) as r:
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


def triage(row):
    txt = call(PROMPT.format(arxiv=row["arxiv_id"] or "?",
                             quote=" ".join((row["original_quote"] or "").split())[:1200],
                             label=row["label"] or "?", rationale=row["label_rationale"] or "?"))
    content = (txt.get("choices") or [{}])[0].get("message", {}).get("content") or ""
    for c in re.findall(r"\{.*?\}", content, re.S):
        try:
            j = json.loads(c)
            if isinstance(j, dict) and j.get("verdict") in ("restated_open", "background", "confirm", "unsure"):
                return j["verdict"], str(j.get("reason", ""))[:150]
        except Exception:
            continue
    return "parse_fail", content[:120]


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 99999
    con = sqlite3.connect(DB, check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA busy_timeout=60000")
    rows = [dict(r) for r in con.execute(
        "SELECT id, arxiv_id, original_quote, label, label_rationale FROM problems "
        "WHERE paper_time_status='not_a_proposition'")]
    done = set()
    if os.path.exists(OUT):
        for l in open(OUT, encoding="utf-8"):
            if l.strip():
                done.add(json.loads(l)["id"])
    todo = [r for r in rows if r["id"] not in done][:limit]
    print(f"[nap] total={len(rows)} done={len(done)} todo={len(todo)}", flush=True)

    q = queue.Queue()
    for r in todo:
        q.put(r)
    lock = threading.Lock()
    fo = open(OUT, "a", encoding="utf-8")
    stats = {"n": 0}

    def worker():
        while True:
            try:
                r = q.get_nowait()
            except queue.Empty:
                return
            try:
                v, reason = triage(r)
            except Exception as e:
                v, reason = "error", str(e)[:100]
            with lock:
                fo.write(json.dumps({"id": r["id"], "arxiv_id": r["arxiv_id"],
                                     "verdict": v, "reason": reason, "model": MODEL,
                                     "ts": datetime.now().isoformat(timespec="seconds")},
                                    ensure_ascii=False) + "\n")
                fo.flush()
                stats["n"] += 1
                stats[v] = stats.get(v, 0) + 1
                if stats["n"] % 25 == 0:
                    print(f"  [progress] {stats['n']}/{len(todo)} {dict((k, x) for k, x in stats.items() if k != 'n')}", flush=True)

    ths = [threading.Thread(target=worker, daemon=True) for _ in range(min(WORKERS, len(todo)))]
    t0 = time.time()
    for t in ths:
        t.start()
    for t in ths:
        t.join()
    fo.close()
    print(f"[nap] DONE {(time.time()-t0)/60:.0f}min {dict((k, v) for k, v in stats.items() if k != 'n')}", flush=True)


if __name__ == "__main__":
    main()
