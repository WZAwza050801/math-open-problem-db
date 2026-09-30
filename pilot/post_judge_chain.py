"""Post-judge auto chain: wait for identity_verdict to finish, then (zero-API):
  1. union-find over verdict='same' edges
  2. contradiction-triple detection (A=B, B=C same but A=distinct inside cluster)
  3. canonical_problem generation (uid op-2026-NNNNNN) + problems.canonical_uid backfill
  4. cluster QC metrics + report + JSONL export

Run:  nohup python3 post_judge_chain.py > post_judge_chain.log 2>&1 &
"""
import json
import os
import sqlite3
import subprocess
import time
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
PAIRS = os.path.join(BASE, "pending_pairs.jsonl")
DB = os.path.join(BASE, "db.sqlite3")
RUNS = os.path.join(BASE, "runs")
RUN_ID = "canon-" + datetime.utcnow().strftime("%Y%m%dT%H%M%SZ") + "-v1"
TOTAL_PAIRS = 2305
POLL_SEC = 60
MAX_WAIT_H = 4


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def judge_running():
    try:
        out = subprocess.run(["pgrep", "-f", "identity_verdict.py"],
                             capture_output=True, text=True)
        return out.returncode == 0
    except Exception:
        return False


def wait_for_judge():
    log(f"waiting for judge to finish ({TOTAL_PAIRS} pairs, poll {POLL_SEC}s)...")
    t0 = time.time()
    while True:
        con = sqlite3.connect(DB)
        n = con.execute("SELECT COUNT(*) FROM canon_verdicts WHERE verdict IN "
                        "('same','distinct','unsure','parse_fail')").fetchone()[0]
        con.close()
        if n >= TOTAL_PAIRS and not judge_running():
            log(f"judge finished: {n}/{TOTAL_PAIRS} verdicts in terminal state")
            return
        if (time.time() - t0) > MAX_WAIT_H * 3600:
            log(f"TIMEOUT after {MAX_WAIT_H}h with {n}/{TOTAL_PAIRS}; aborting chain")
            raise SystemExit(2)
        time.sleep(POLL_SEC)


class UF:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def build():
    pairs = [json.loads(l) for l in open(PAIRS, encoding="utf-8")]
    con = sqlite3.connect(DB)
    con.execute("PRAGMA busy_timeout=60000")
    v = dict(con.execute("SELECT a_id || '|' || b_id, verdict FROM canon_verdicts").fetchall())

    same, distinct, unsure, pfail, missing = [], [], [], [], []
    for p in pairs:
        key = f"{p['a']}|{p['b']}"
        verdict = v.get(key)
        if verdict == "same":
            same.append((p["a"], p["b"]))
        elif verdict == "distinct":
            distinct.append((p["a"], p["b"]))
        elif verdict == "unsure":
            unsure.append(key)
        elif verdict == "parse_fail":
            pfail.append(key)
        else:
            missing.append(key)

    log(f"verdicts: same={len(same)} distinct={len(distinct)} "
        f"unsure={len(unsure)} parse_fail={len(pfail)} missing={len(missing)}")

    # union-find over same edges only
    uf = UF()
    for a, b in same:
        uf.union(str(a), str(b))

    # collect clusters
    clusters = {}
    for a, b in same:
        for c in (str(a), str(b)):
            clusters.setdefault(uf.find(c), set()).add(c)
    clusters = {r: sorted(members) for r, members in clusters.items()}

    # contradiction: distinct edge with both endpoints inside one same-cluster
    contradiction = []
    for a, b in distinct:
        ra, rb = uf.find(str(a)), uf.find(str(b))
        if ra == rb:
            contradiction.append((a, b))
    blocked_roots = {uf.find(str(a)) for a, _ in contradiction}

    # all cards
    cards = [str(r[0]) for r in con.execute("SELECT id FROM problems")]
    card_paper = dict(con.execute("SELECT id, arxiv_id FROM problems"))
    in_cluster = set()
    for members in clusters.values():
        in_cluster.update(members)
    for c in cards:
        if c not in in_cluster:
            clusters[uf.find(c)] = [c]

    # canonical table
    con.execute("CREATE TABLE IF NOT EXISTS canonical_problem ("
                "canonical_uid TEXT PRIMARY KEY, rep_card_id TEXT, n_cards INTEGER, "
                "n_distinct_papers INTEGER, review_state TEXT, created_at TEXT)")
    cols = [r[1] for r in con.execute("PRAGMA table_info(problems)")]
    if "canonical_uid" not in cols:
        con.execute("ALTER TABLE problems ADD COLUMN canonical_uid TEXT")
    con.execute("UPDATE problems SET canonical_uid=NULL")

    # deterministic uid order: size desc, then min card id (ids are strings
    # like 'OP-44EC9EEC022C', never int())
    ordered = sorted(clusters.values(), key=lambda m: (-len(m), m[0]))
    con.execute("DELETE FROM canonical_problem")
    stats = {"n_canonical": 0, "blocked": 0, "multi_paper": 0}
    for members in ordered:
        root = uf.find(members[0])
        papers = {card_paper.get(c) for c in members}
        papers.discard(None)
        state = "blocked" if root in blocked_roots else "draft"
        uid = f"op-2026-{stats['n_canonical'] + 1:06d}"
        con.execute("INSERT OR REPLACE INTO canonical_problem VALUES (?,?,?,?,?,?)",
                    (uid, members[0], len(members), len(papers), state,
                     datetime.now().isoformat(timespec="seconds")))
        con.execute(f"UPDATE problems SET canonical_uid=? WHERE id IN "
                    f"({','.join('?' * len(members))})", [uid] + members)
        stats["n_canonical"] += 1
        stats["blocked"] += state == "blocked"
        stats["multi_paper"] += len(papers) >= 2
    con.commit()

    # metrics
    sizes = sorted((len(m) for m in ordered), reverse=True)
    n = len(sizes)
    metrics = {
        "run_id": RUN_ID,
        "n_problems": len(cards),
        "n_canonical": n,
        "cluster_size_max": sizes[0] if sizes else 0,
        "cluster_size_p50": sizes[n // 2] if n else 0,
        "cluster_size_p90": sizes[int(n * 0.9)] if n else 0,
        "cluster_size_p99": sizes[min(n - 1, int(n * 0.99))] if n else 0,
        "singleton_rate": round(sum(1 for s in sizes if s == 1) / n, 4) if n else None,
        "multi_paper_rate": round(stats["multi_paper"] / n, 4) if n else None,
        "large_cluster_count_ge10": sum(1 for s in sizes if s >= 10),
        "contradiction_pairs": len(contradiction),
        "blocked_clusters": stats["blocked"],
        "unmerged_parse_fail_pairs": len(pfail),
        "unmerged_missing_pairs": len(missing),
    }

    # export
    rdir = os.path.join(RUNS, RUN_ID)
    os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "canonical_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    with open(os.path.join(rdir, "contradiction_pairs.json"), "w") as f:
        json.dump([{"a": a, "b": b} for a, b in contradiction], f, indent=2)
    with open(os.path.join(rdir, "large_clusters.json"), "w") as f:
        big = [{"canonical_uid": None, "n_cards": len(m), "card_ids": m}
               for m in ordered if len(m) >= 10]
        json.dump(big, f, indent=2)
    integrity = con.execute("PRAGMA integrity_check").fetchone()[0]
    con.close()
    metrics["integrity_check"] = integrity

    log("METRICS " + json.dumps(metrics, ensure_ascii=False))
    log("chain DONE")


if __name__ == "__main__":
    wait_for_judge()
    build()
