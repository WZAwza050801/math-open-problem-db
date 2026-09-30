"""P2: canonical statement build + independent verification (SOP M4).
- singleton canonicals: copy self_contained card statement (zero API)
- multi-card clusters: GLM synthesizes statement_en, qwen verifies 3 questions
- statement_quality < 0.7 -> ungraded (excluded from scoring later)
- checkpoint-resume via canonical_statement table; zero destructive ops.
Usage: python3 statement_build.py            # run pending
       python3 statement_build.py --report   # stats only
"""
import hashlib, json, os, queue, sqlite3, sys, threading, time, urllib.request
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "db.sqlite3")

def load_env():
    env = {}
    with open(os.path.join(BASE, ".env"), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env

ENVV = load_env()
GLM_KEY = ENVV.get("GLM_CODING_TEAM2_KEY", "")
TP_KEY = ENVV.get("BAILIAN_TOKENPLAN_KEY", "")
WORKERS = 4

GEN_PROMPT = """You are building ONE canonical statement for a research database.
Below are {n} evidence statements (from different papers) that were judged to describe
the same underlying mathematical problem. Write ONE self-contained English statement that:
1. captures the common mathematical claim of the evidence;
2. is NOT stronger than the evidence (no strengthening of conclusions or hypotheses);
3. omits nothing necessary for the problem to be well-posed;
4. is phrased as a clear, self-contained research problem (no references to "the paper" or authors).

EVIDENCE:
{evidence}

Answer ONLY this JSON object:
{{"statement_en": "<the canonical statement>", "omitted_details": ["<any evidence detail you left out>"], "confidence": <0.0-1.0>}}"""

VERIFY_PROMPT = """You are an independent verifier for a research database.
EVIDENCE STATEMENTS (ground truth):
{evidence}

CANDIDATE CANONICAL STATEMENT:
{statement}

Answer three questions strictly:
1. Is the candidate STRONGER than the evidence (claims more than any evidence supports)?
2. Does it OMIT a condition necessary for the problem to be well-posed?
3. Is it MISFRAMED (not actually a research problem, or changes the subject)?

Answer ONLY this JSON object:
{{"stronger": <true|false>, "missing": <true|false>, "misframed": <true|false>, "quality": <0.0-1.0>, "reason": "<one sentence>"}}"""

def call(base, key, model, prompt, timeout, extra):
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1600, "temperature": 0.1}
    body.update(extra or {})
    req = urllib.request.Request(base.rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)

def parse_obj(content):
    import re
    m = re.search(r"\{.*\}", content or "", re.S)
    return json.loads(m.group(0)) if m else {}

def sha(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()[:16]

def short(t, n=900):
    t = " ".join((t or "").split())
    return t[:n] + ("..." if len(t) > n else "")

def worker(wid, q, con_lock, con, stats):
    while True:
        try:
            job = q.get_nowait()
        except queue.Empty:
            return
        uid, mode, cards = job   # cards: list of (card_id, text)
        try:
            if mode == "blocked":
                with con_lock:
                    con.execute("INSERT OR REPLACE INTO canonical_statement VALUES (?,?,?,?,?,?,?,?)",
                                (uid, None, None, "[]", "none", None, "blocked",
                                 datetime.now().isoformat(timespec="seconds")))
                    con.commit()
                stats["blocked"] += 1
                q.task_done()
                continue
            evidence = "\n\n".join(f"[{i+1}] (card {cid}) {short(t)}"
                                   for i, (cid, t) in enumerate(cards))
            if mode == "synthesized":
                gen = None
                for attempt in range(3):
                    try:
                        r = call("https://open.bigmodel.cn/api/coding/paas/v4", GLM_KEY,
                                 "glm-5.3", GEN_PROMPT.format(n=len(cards), evidence=evidence),
                                 600, {"thinking": {"type": "disabled"}})
                        gen = parse_obj(r["choices"][0]["message"]["content"] or "")
                        if gen.get("statement_en"):
                            break
                    except Exception as e:
                        stats["gen_retry"] = stats.get("gen_retry", 0) + 1
                        time.sleep(10 * (attempt + 1))
                if not gen or not gen.get("statement_en"):
                    with con_lock:
                        con.execute("INSERT OR REPLACE INTO canonical_statement VALUES (?,?,?,?,?,?,?,?)",
                                    (uid, None, None, json.dumps([c[0] for c in cards]),
                                     "synthesized", 0.0, "pending_build",
                                     datetime.now().isoformat(timespec="seconds")))
                        con.commit()
                    stats["pending_build"] += 1
                    q.task_done()
                    continue
                stmt = " ".join(gen["statement_en"].split())
                # independent verification (different engine family)
                quality, vstate = 0.5, "ungraded"
                try:
                    r = call("https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
                             TP_KEY, "qwen3.8-max",
                             VERIFY_PROMPT.format(evidence=evidence, statement=stmt),
                             600, {"enable_thinking": False})
                    v = parse_obj(r["choices"][0]["message"]["content"] or "")
                    quality = float(v.get("quality", 0.5))
                    quality = min(quality, 0.3) if (v.get("stronger") or v.get("missing")
                                                    or v.get("misframed")) else max(quality, 0.5)
                except Exception as e:
                    stats["verify_fail"] = stats.get("verify_fail", 0) + 1
                state = "verified" if quality >= 0.7 else "ungraded"
                with con_lock:
                    con.execute("INSERT OR REPLACE INTO canonical_statement VALUES (?,?,?,?,?,?,?,?)",
                                (uid, stmt, sha(stmt), json.dumps([c[0] for c in cards]),
                                 "synthesized", round(quality, 2), state,
                                 datetime.now().isoformat(timespec="seconds")))
                    con.commit()
                stats["synth_" + state] = stats.get("synth_" + state, 0) + 1
            else:  # single_copy
                cid, text = cards[0]
                if text and len(text.strip()) > 30:
                    with con_lock:
                        con.execute("INSERT OR REPLACE INTO canonical_statement VALUES (?,?,?,?,?,?,?,?)",
                                    (uid, text, sha(text), json.dumps([cid]),
                                     "single_copy", 1.0, "draft",
                                     datetime.now().isoformat(timespec="seconds")))
                        con.commit()
                    stats["single"] += 1
                else:
                    with con_lock:
                        con.execute("INSERT OR REPLACE INTO canonical_statement VALUES (?,?,?,?,?,?,?,?)",
                                    (uid, None, None, json.dumps([cid]), "single_copy",
                                     0.0, "pending_build",
                                     datetime.now().isoformat(timespec="seconds")))
                        con.commit()
                    stats["pending_build"] += 1
        except Exception as e:
            stats["error"] = stats.get("error", 0) + 1
            print(f"  [w{wid}] error on {uid}: {str(e)[:100]}", flush=True)
        q.task_done()

def main():
    dry = "--report" in sys.argv
    con = sqlite3.connect(DB, check_same_thread=False)
    con.execute("PRAGMA busy_timeout=60000")
    con.execute("""CREATE TABLE IF NOT EXISTS canonical_statement (
        canonical_uid TEXT PRIMARY KEY, statement_en TEXT, statement_hash TEXT,
        source_card_ids TEXT, build_mode TEXT, statement_quality REAL,
        review_state TEXT, created_at TEXT)""")
    done = {r[0] for r in con.execute("SELECT canonical_uid FROM canonical_statement")}
    blocked = {r[0] for r in con.execute(
        "SELECT canonical_uid FROM canonical_problem WHERE review_state='blocked'")}
    clusters = {}
    rep = {}
    for r in con.execute("SELECT p.id, p.canonical_uid, p.self_contained "
                         "FROM problems p WHERE p.canonical_uid IS NOT NULL"):
        uid = r[1]
        clusters.setdefault(uid, []).append((r[0], r[2] or ""))
    for uid, members in clusters.items():
        best = max(members, key=lambda m: len(m[1] or ""))
        rep[uid] = {"members": members, "best": best}
    jobs = []
    for uid, info in rep.items():
        if uid in done:
            continue
        if uid in blocked:
            jobs.append((uid, "blocked", []))
            continue
        if len(info["members"]) == 1:
            jobs.append((uid, "single_copy", [info["best"]]))
        else:
            jobs.append((uid, "synthesized", info["members"]))
    print(f"[stmt] total={len(rep)} done={len(done)} todo={len(jobs)} "
          f"(blocked={sum(1 for j in jobs if j[1]=='blocked')}, "
          f"single={sum(1 for j in jobs if j[1]=='single_copy')}, "
          f"synth={sum(1 for j in jobs if j[1]=='synthesized')})", flush=True)
    if dry:
        return
    q = queue.Queue()
    for j in jobs:
        q.put(j)
    con_lock = threading.Lock()
    stats = {"single": 0, "pending_build": 0, "blocked": 0}
    threads = [threading.Thread(target=worker,
                                args=(i, q, con_lock, con, stats), daemon=True)
               for i in range(min(WORKERS, len(jobs)) or 1)]
    t0 = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"\n[stmt] DONE in {(time.time()-t0)/60:.0f}min  stats={stats}", flush=True)
    print("by review_state:", con.execute(
        "SELECT review_state, COUNT(*) FROM canonical_statement GROUP BY review_state").fetchall())
    print("quality: avg=", con.execute(
        "SELECT ROUND(AVG(statement_quality),3), COUNT(*) FROM canonical_statement "
        "WHERE statement_quality IS NOT NULL").fetchone())
    print("integrity:", con.execute("PRAGMA integrity_check").fetchone()[0])

if __name__ == "__main__":
    main()
