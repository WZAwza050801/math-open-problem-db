"""M13 difficulty fit v2 — partial-credit model on verdict levels.

Model: for attempt o on problem p by solver m, graded level l in 0..4:
    logit P(l >= k) = theta_m - (beta_p + delta_k),  k = 1..4
  beta_p = problem difficulty (higher = harder), theta_m = solver ability,
  delta_k = level thresholds. Fit by batch gradient descent + L2, pure numpy.
Output: pilot/runs/difficulty-v1/difficulty_fit_v2.json (+ per-problem table printed)
"""
import json, math, os
from collections import defaultdict

import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(BASE, "runs", "difficulty-v1")

# ---- load verdicts + targets ----
vs = [json.loads(l) for l in open(os.environ.get("FIT_VERDICTS", os.path.join(RUN, "verdicts.jsonl")), encoding="utf-8") if l.strip()]
targets = {t["uid"]: t for t in json.load(open(os.environ.get("FIT_TARGETS", os.path.join(BASE, "difficulty_targets.json")), encoding="utf-8"))}
# solver identity lives in the ATTEMPT file (verdicts record the verifier model)
att_model = {}
for f in os.listdir(os.path.join(RUN, "attempts")):
    if f.endswith(".json"):
        a = json.load(open(os.path.join(RUN, "attempts", f), encoding="utf-8"))
        uid, _, tid = f[:-5].partition("__t")
        att_model[(uid, int(tid))] = a.get("model", "unknown")
vs = [v for v in vs if v.get("level") is not None]
for v in vs:
    v["solver"] = att_model.get((v["uid"], v["traj"]), "unknown")
problems = sorted({v["uid"] for v in vs})
solvers = sorted({v["solver"] for v in vs})  # glm / deepseek / kimi
smap = {s: i for i, s in enumerate(solvers)}
pmap = {p: i for i, p in enumerate(problems)}

P, M, K = len(problems), len(solvers), 4  # thresholds k=1..4
obs = [(pmap[v["uid"]], smap[v["solver"]], int(v["level"])) for v in vs]

# ---- params ----
rng = np.random.default_rng(42)
beta = rng.normal(0, 0.1, P)          # problem difficulty
theta = np.zeros(M)                    # solver ability
delta = np.array([-2.0, -0.5, 1.5, 3.0])  # threshold offsets (init monotone)

L2 = 1e-3
lr = 0.05
for epoch in range(3000):
    gb = np.zeros(P); gt = np.zeros(M); gd = np.zeros(K)
    for p, m, l in obs:
        for k in range(1, K + 1):
            z = theta[m] - (beta[p] + delta[k - 1])
            pr = 1.0 / (1.0 + math.exp(-max(min(z, 30), -30)))
            y = 1.0 if l >= k else 0.0
            g = (pr - y)
            gt[m] += g; gb[p] -= g; gd[k - 1] -= g
    theta -= lr * (gt / len(obs) + L2 * theta)
    beta -= lr * (gb / len(obs) + L2 * beta)
    # keep delta centered (identifiability): subtract mean each step
    gd -= gd.mean()
    delta -= lr * (gd / len(obs))

# ---- metrics ----
# log-likelihood
ll = 0.0
for p, m, l in obs:
    for k in range(1, K + 1):
        z = theta[m] - (beta[p] + delta[k - 1])
        pr = 1.0 / (1.0 + math.exp(-max(min(z, 30), -30)))
        y = 1.0 if l >= k else 0.0
        ll += y * math.log(max(pr, 1e-12)) + (1 - y) * math.log(max(1 - pr, 1e-12))

# difficulty ordering + correlation with raw mean levels
raw_mean = defaultdict(list)
for v in vs:
    raw_mean[v["uid"]].append(v["level"])
raw = {u: sum(x) / len(x) for u, x in raw_mean.items()}
blist = {problems[i]: float(beta[i]) for i in range(P)}
common = [u for u in problems if u in raw]
xs = [raw[u] for u in common]; ys = [blist[u] for u in common]
mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
cov = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
sx = math.sqrt(sum((a - mx) ** 2 for a in xs)); sy = math.sqrt(sum((b - my) ** 2 for b in ys))
corr = cov / (sx * sy)

out = {
    "model": "partial_creditPCM_v1", "n_obs": len(obs), "n_problems": P,
    "solvers": solvers, "theta": {s: float(theta[i]) for s, i in smap.items()},
    "delta": [float(d) for d in delta], "loglik": round(ll, 2),
    "corr_beta_vs_rawmean": round(corr, 3),
    "problems": [
        {"uid": u, "beta": round(blist[u], 3), "raw_mean": raw.get(u),
         "msc": targets.get(u, {}).get("msc"), "pub_year": targets.get(u, {}).get("pub_year")}
        for u in sorted(problems, key=lambda u: -blist[u])],
}
json.dump(out, open(os.path.join(RUN, "difficulty_fit_v2.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print(f"fit done: ll={ll:.1f} corr(beta, raw_mean)={corr:.3f}")
print("solver abilities theta:", {s: round(float(theta[i]), 2) for s, i in smap.items()})
print("thresholds delta:", [round(float(d), 2) for d in delta])
print("\nTop-8 hardest (beta high):")
for row in out["problems"][:8]:
    print(f"  {row['uid']} beta={row['beta']:+.2f} raw={row['raw_mean']} MSC{row['msc']}")
print("Top-5 easiest:")
for row in out["problems"][-5:]:
    print(f"  {row['uid']} beta={row['beta']:+.2f} raw={row['raw_mean']} MSC{row['msc']}")
