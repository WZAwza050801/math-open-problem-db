"""P0 S0.2: blind-test 3 engines on the public-consensus gold set.
Per engine: one thread, sequential over 25 items, checkpoint-resume JSONL.
Usage: python3 gold_blind_test.py            # run all pending
       python3 gold_blind_test.py --report   # score existing results
"""
import json, os, sys, threading, time, urllib.request, urllib.error
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
ENV = os.path.join(BASE, ".env")
RUBRIC = """You are judging the mathematical importance of a problem for a research database.

Importance tiers (I1-I5):
- I5 foundational/landmark: solving it would significantly restructure a field, or a widely recognized central conjecture with broad downstream impact
- I4 field-level major: strong influence on a mature subfield; could unify important results or produce reusable methods
- I3 substantive research problem: non-trivial, clearly posed, recognizable scholarly increment after solution, but influence mostly confined to one direction
- I2 local/technical: narrow extension, parameter improvement, or technical gap; real value but limited scope
- I1 weak independent value: remark, exercise-style question, extraction noise, or lacking evidence of being a real research problem

Judge from the problem statement itself using: centrality, potential downstream impact, method value, sustained attention it would merit. Do NOT rate by fame of keywords alone; a famous name attached to a trivial question is still trivial.

Answer ONLY this JSON object:
{"tier": <1-5>, "tier_probabilities": [<p1>,<p2>,<p3>,<p4>,<p5>], "criterion_levels": {"centrality": <1-5>, "downstream_impact": <1-5>, "method_value": <1-5>, "sustained_attention": <1-5>}, "rationale": "<two sentences max>"}
The five probabilities must sum to 1."""

RUBRIC_V11 = """You are judging the mathematical importance of a problem for a research database.

Importance tiers (I1-I5):
- I5 foundational/landmark: solving it would restructure the foundations of a broad field or resolve a universally acknowledged central problem. Calibration example: the Poincare conjecture (classifying all closed 3-manifolds).
- I4 field-level major: strong influence on one mature subfield; could unify important results or yield reusable methods. Calibration example: a conjecture that would complete the classification program of an entire subfield.
- I3 substantive research problem: non-trivial, clearly posed, recognizable scholarly increment after solution, but influence mostly confined to one direction. Calibration example: a well-posed open question in one subfield that a handful of specialists actively pursue.
- I2 local/technical: narrow extension, parameter improvement, or technical gap; real value but limited scope. Calibration example: improving an exponent in a specific known bound.
- I1 weak independent value: remark, exercise-style question, extraction noise, or lacking evidence of being a real research problem. Calibration example: verifying a small finite case or a routine computation.

FAME GUARD (critical):
- Fame, age, or a catchy name does NOT raise the tier. A well-known problem whose resolution would mainly matter inside one subfield is I3 or I4, never I5.
- I5 is reserved for problems whose resolution changes the toolbox or foundations of a broad area (e.g., the Riemann Hypothesis, P vs NP). Long-standing open problems that are merely popular or elementary-to-state (e.g., Collatz-type, coloring-of-the-plane-type, runner-type problems) belong to I3 at most unless you can articulate a concrete field-structural consequence.
- Judge the mathematical consequences of resolution, not how often the problem is cited in popular media.

Judge from the problem statement itself using: centrality, potential downstream impact, method value, sustained attention it would merit.

Answer ONLY this JSON object:
{"tier": <1-5>, "tier_probabilities": [<p1>,<p2>,<p3>,<p4>,<p5>], "criterion_levels": {"centrality": <1-5>, "downstream_impact": <1-5>, "method_value": <1-5>, "sustained_attention": <1-5>}, "rationale": "<two sentences max>"}
The five probabilities must sum to 1."""

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
GLM_KEY = ENVV.get("GLM_CODING_TEAM2_KEY", "")
KIMI_KEY = ENVV.get("KIMI_CODING_KEY", "")
TP_KEY = ENVV.get("BAILIAN_TOKENPLAN_KEY", "")

# 引擎纪律（老板 2026-09-27 指示）：Kimi 只允许走官方 coding plan（api.kimi.com），
# 禁止用 SiliconFlow 等按量计费渠道调 Kimi。
ENGINES = [
    ("glm-5.3", "https://open.bigmodel.cn/api/coding/paas/v4", GLM_KEY, "glm-5.3",
     {"thinking": {"type": "disabled"}}),
    ("kimi-k3-coding", "https://api.kimi.com/coding/v1", KIMI_KEY, "k3", {}),
    ("qwen3.8-max", "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1", TP_KEY,
     "qwen3.8-max", {"enable_thinking": False}),
]

def call(base, key, model, prompt, timeout, extra):
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1500, "temperature": 0.1}
    body.update(extra or {})
    req = urllib.request.Request(base.rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)

def run_engine(name, base, key, model, extra, items, suffix=""):
    out = os.path.join(BASE, f"gold_judgments_{suffix}{name}.jsonl")
    done_ids = set()
    if os.path.exists(out):
        done_ids = {json.loads(l)["id"] for l in open(out, encoding="utf-8") if l.strip()}
    for it in items:
        if it["id"] in done_ids:
            continue
        prompt = RUBRIC_TO_USE + "\n\nPROBLEM:\n" + it["statement"]
        rec = {"id": it["id"], "engine": name, "ts": datetime.now().isoformat(timespec="seconds")}
        for attempt in range(3):
            try:
                r = call(base, key, model, prompt, timeout=600, extra=extra)
                content = r["choices"][0]["message"]["content"] or ""
                import re
                m = re.search(r"\{.*\}", content, re.S)
                obj = json.loads(m.group(0)) if m else {}
                rec.update({"tier": obj.get("tier"),
                            "tier_probabilities": obj.get("tier_probabilities"),
                            "criterion_levels": obj.get("criterion_levels"),
                            "rationale": obj.get("rationale"), "ok": True})
                break
            except Exception as e:
                rec.update({"ok": False, "error": str(e)[:150]})
                if attempt == 2:
                    rec["tier"] = None
                time.sleep(10 * (attempt + 1))
        with open(out, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"[{name}] done", flush=True)

def report(items, suffix=""):
    gold = {it["id"]: it["tier"] for it in items}
    print(f"{'engine':<15} {'n':>3} {'within1':>8} {'exact':>6} {'catastroph':>10}")
    for name, *_ in ENGINES:
        p = os.path.join(BASE, f"gold_judgments_{suffix}{name}.jsonl")
        if not os.path.exists(p):
            continue
        rows = [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
        ok = [r for r in rows if r.get("ok") and r.get("tier")]
        w1 = sum(1 for r in ok if abs(int(r["tier"]) - gold[r["id"]]) <= 1)
        ex = sum(1 for r in ok if int(r["tier"]) == gold[r["id"]])
        cat = sum(1 for r in ok if abs(int(r["tier"]) - gold[r["id"]]) >= 3)
        print(f"{name:<12} {len(ok):>3} {w1:>4}/{len(ok)} {ex:>4}/{len(ok)} {cat:>10}")
    # aggregate vote: mean expected tier vs gold
    by_id = {}
    for name, *_ in ENGINES:
        p = os.path.join(BASE, f"gold_judgments_{suffix}{name}.jsonl")
        if not os.path.exists(p):
            continue
        for r in (json.loads(l) for l in open(p, encoding="utf-8") if l.strip()):
            if r.get("ok") and r.get("tier"):
                by_id.setdefault(r["id"], []).append(int(r["tier"]))
    if by_id:
        import statistics
        w1 = ex = cat = 0
        for gid, tiers in by_id.items():
            mu = statistics.mean(tiers)
            d = abs(mu - gold[gid])
            w1 += d <= 1; ex += d <= 0.5; cat += d >= 2
        n = len(by_id)
        print(f"\n[ensemble mean] within1 {w1}/{n} ({w1/n:.0%})  exact {ex}/{n}  catastroph(>=2) {cat}/{n}")
        verdict = "PASS" if w1 / n >= 0.9 and cat == 0 else "FAIL"
        print(f"P0 GATE: {verdict}")

if __name__ == "__main__":
    items = json.load(open(os.path.join(BASE, "gold_set.json"), encoding="utf-8"))["items"]
    suffix = "v11_" if "--rubric" in sys.argv and "v11" in sys.argv else ""
    if suffix:
        RUBRIC_TO_USE = RUBRIC_V11
    else:
        RUBRIC_TO_USE = RUBRIC
    if "--report" in sys.argv:
        report(items, suffix)
        sys.exit(0)
    threads = []
    for name, base, key, model, extra in ENGINES:
        if not key:
            print(f"[skip] no key for {name}")
            continue
        t = threading.Thread(target=run_engine,
                             args=(name, base, key, model, extra, items, suffix), daemon=True)
        t.start(); threads.append(t)
    for t in threads:
        t.join()
    print("\n=== REPORT ===")
    report(items, suffix)
