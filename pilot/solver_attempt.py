"""M13 AI real-attempt harness — solver side (SOP §11). v2 concurrent.

Local machine. Engine via M13_ENGINE env (glm|kimi), default glm.
3 trajectories per problem, fixed budget, full transcript + sha256.
Solver never grades itself (verifier runs separately on node01).

Usage: python solver_attempt.py [n_problems] [offset]
Input:  difficulty_targets.json     Output: runs/difficulty-v1/attempts/<uid>__t<i>.json
"""
import json, hashlib, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(BASE, "runs", "difficulty-v1")
ATT = os.path.join(RUN, "attempts")
ENGINE = os.environ.get("M13_ENGINE", "glm")
URLS = {"glm": "https://open.bigmodel.cn/api/coding/paas/v4/chat/completions",
        "kimi": "https://api.kimi.com/coding/v1/chat/completions",
        "deepseek": "https://api.deepseek.com/chat/completions",
        "qglm": "https://qianfan.baidubce.com/v2/tokenplan/personal/chat/completions",
        "qds": "https://qianfan.baidubce.com/v2/tokenplan/personal/chat/completions"}
MODELS = {"glm": "glm-5.3", "kimi": "kimi-k3", "deepseek": "deepseek-reasoner",
          "qglm": "glm-5.3",  # qglm = glm-5.3 via qianfan tokenplan (small-prompt tasks only)
          "qds": "deepseek-v4-pro"}  # qds = v4-pro via qianfan; reasoning bills vs max_tokens
N_TRAJ = 3
# 32k starved: kimi-k3 and deepseek-reasoner reasoning can eat the whole
# budget with content empty; deepseek accepts 64k (probed). qds: tiny input
# (~2k tok) so 64k out keeps in+out far under the ~104k personal-lane window
MAX_OUT = 64000 if ENGINE in ("deepseek", "qds") else 32000
READ_TIMEOUT = 3000
WORKERS = int(os.environ.get("M13_WORKERS", "2"))  # keep low: key shared with extraction

PROMPT = """You are a research mathematician working at a top department. Below is an open problem from a leading mathematics journal (posed {pub_year}). Make a genuine research attempt on it.

Rules:
- Work toward real progress: reductions, special cases, examples, counterexample attempts, obstructions, partial results, reformulations.
- Do NOT claim a full solution unless you can actually produce a complete rigorous proof or an explicit counterexample (rare; honesty matters more than bravado).
- If the problem statement seems incomplete or ambiguous, say precisely what extra information would be needed, then attempt the most natural interpretation.
- Show your reasoning in full; finish with a clearly labeled "PARTIAL PROGRESS SUMMARY" section listing what was established and what remains open.

Problem (MSC {msc}):
{statement}
"""

def sha256(t):
    return hashlib.sha256(t.encode()).hexdigest()


def attempt(item, tid):
    prompt = PROMPT.format(pub_year=item.get("pub_year") or "unknown",
                           msc=item.get("msc") or "?",
                           statement=item["statement"])
    keyfile = os.path.join(BASE, f".{ENGINE}_key")
    headers = {"Authorization": "Bearer " + open(keyfile).read().strip(),
               "Content-Type": "application/json"}
    if ENGINE in ("glm", "qglm"):
        # thinking DISABLED: hidden reasoning burned 32k tokens with zero
        # output on research-level problems (9/9 timeouts at 50min). Visible
        # CoT in the transcript is gradeable by the verifier instead.
        body = json.dumps({"model": MODELS[ENGINE],
                           "messages": [{"role": "user", "content": prompt}],
                           "max_tokens": MAX_OUT, "temperature": 0.7,
                           "thinking": {"type": "disabled"}}).encode()
    elif ENGINE in ("deepseek", "qds"):
        # deepseek-reasoner: visible CoT by design (reasoning_content);
        # temperature/seed unsupported -> omit.
        # qds (v4-pro @ qianfan): temperature IS accepted (probed 0.1); keep
        # 0.7 for exploration diversity, no thinking param (reasoning is
        # automatic and lands in reasoning_content).
        body = json.dumps({"model": MODELS[ENGINE],
                           "messages": [{"role": "user", "content": prompt}],
                           **({"max_tokens": MAX_OUT} if ENGINE == "deepseek" else
                              {"max_tokens": MAX_OUT, "temperature": 0.7})}).encode()
    else:
        body = json.dumps({"model": MODELS[ENGINE],
                           "messages": [{"role": "user", "content": prompt}],
                           "max_tokens": MAX_OUT,
                           "thinking": {"type": "disabled"},  # probed OK on kimi endpoint
                           "seed": 1000 + tid}).encode()
    req = urllib.request.Request(URLS[ENGINE], data=body, headers=headers)
    t0 = time.time()
    for attempt_i in range(5):
        try:
            with urllib.request.urlopen(req, timeout=READ_TIMEOUT) as r:
                d = json.load(r)
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt_i < 4:
                time.sleep(60 * (attempt_i + 1))  # backoff: 1,2,3,4 min
                continue
            raise
    ch = (d.get("choices") or [{}])[0]
    content = (ch.get("message") or {}).get("content") or ""
    if not content:
        # starvation fallback: reasoning ate max_tokens but left a CoT trail —
        # the reasoning transcript is itself a gradeable real attempt
        content = (ch.get("message") or {}).get("reasoning_content") or ""
    if not content:
        raise RuntimeError(f"empty response body: {json.dumps(d)[:160]}")
    u = d.get("usage", {})
    rec = {"uid": item["uid"], "traj": tid, "model": MODELS[ENGINE],
           "attempt_sha256": sha256(content), "chars": len(content),
           "tokens_in": u.get("prompt_tokens"), "tokens_out": u.get("completion_tokens"),
           "latency_s": round(time.time() - t0, 1),
           "ts": datetime.now().isoformat(timespec="seconds"),
           "content": content}
    out = os.path.join(ATT, f"{item['uid']}__t{tid}.json")
    json.dump(rec, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return rec


def main():
    n_prob = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    offset = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    targets = json.load(open(os.environ.get("M13_TARGETS",
                             os.path.join(BASE, "difficulty_targets.json")),
                             encoding="utf-8"))[offset:offset + n_prob]
    os.makedirs(ATT, exist_ok=True)
    if not os.path.exists(os.path.join(BASE, f".{ENGINE}_key")):
        print(f"FATAL: .{ENGINE}_key missing")
        sys.exit(1)
    print(f"[difficulty] problems={len(targets)} traj/target={N_TRAJ} engine={ENGINE} "
          f"model={MODELS[ENGINE]} max_out={MAX_OUT} workers={WORKERS}", flush=True)

    tasks = [(t, i) for t in targets for i in range(N_TRAJ)]
    todo = [(t, i) for t, i in tasks
            if not os.path.exists(os.path.join(ATT, f"{t['uid']}__t{i}.json"))]
    print(f"[difficulty] tasks={len(tasks)} todo={len(todo)}", flush=True)

    t0 = time.time()
    done_n = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(attempt, t, i): (t["uid"], i) for t, i in todo}
        for fut in as_completed(futs):
            uid, tid = futs[fut]
            try:
                rec = fut.result()
                done_n += 1
                tag = "EMPTY!" if rec["chars"] < 200 else "ok"
                print(f"  {uid} t{tid} {tag} {rec['chars']:,} chars "
                      f"out={rec['tokens_out']} {rec['latency_s']}s "
                      f"[{done_n}/{len(todo)} {time.time()-t0:.0f}s]", flush=True)
            except Exception as e:
                print(f"  {uid} t{tid} FAIL {type(e).__name__}: {str(e)[:100]} "
                      f"[{time.time()-t0:.0f}s]", flush=True)
    print(f"[difficulty] DONE ok/empty={done_n}/{len(todo)} "
          f"elapsed={(time.time()-t0)/60:.0f}min", flush=True)


if __name__ == "__main__":
    main()
