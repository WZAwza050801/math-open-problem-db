"""P1 S1.1: annotate 126 anchor candidates with importance tiers.
2 engines (GLM + TokenPlan qwen; Kimi blocked by node01 egress), rubric v1.1.
Checkpoint-resume JSONL per engine. Zero destructive ops.
Usage: python3 anchor_annotate.py            # run pending
       python3 anchor_annotate.py --report   # aggregate + anchor bank v0
"""
import json, os, statistics, sys, threading, time, urllib.request
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
CANDS = os.path.join(BASE, "anchor_candidates.json")
RUBRIC_FILE = os.path.join(BASE, "rubric_v11.txt")

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
ENGINES = [
    ("glm-5.3", "https://open.bigmodel.cn/api/coding/paas/v4", ENVV.get("GLM_CODING_TEAM2_KEY", ""),
     "glm-5.3", {"thinking": {"type": "disabled"}}),
    ("qwen3.8-max", "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
     ENVV.get("BAILIAN_TOKENPLAN_KEY", ""), "qwen3.8-max", {"enable_thinking": False}),
]

RUBRIC = open(RUBRIC_FILE, encoding="utf-8").read() if os.path.exists(RUBRIC_FILE) else None

def build_prompt(c):
    ev = (f"Evidence profile (objective signals; citation counts are WEAK evidence -- "
          f"judge the mathematics first, low citations may mean a cold subfield):\n"
          f"- cluster size (evidence cards): {c['n_cards']}\n"
          f"- distinct papers posing it: {c['n_distinct_papers']}\n"
          f"- total citations of source papers: {c['n_total_citations']}\n"
          f"- recent citations (2021-2026): {c['n_recent_citations']}\n"
          f"- MSC class: {c['msc']}  era: {c['era']}\n"
          f"- recognized named problem: {'yes (' + ', '.join(c['aliases'][:3]) + ')' if c['aliases'] else 'no'}")
    return RUBRIC + "\n\n" + ev + "\n\nPROBLEM STATEMENT:\n" + c["statement_excerpt"]

def call(base, key, model, prompt, timeout, extra):
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1200, "temperature": 0.1}
    body.update(extra or {})
    req = urllib.request.Request(base.rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)

def run_engine(name, base, key, model, extra, cands):
    out = os.path.join(BASE, f"anchor_judgments_{name}.jsonl")
    done = set()
    if os.path.exists(out):
        done = {json.loads(l)["uid"] for l in open(out, encoding="utf-8") if l.strip()}
    for i, c in enumerate(cands):
        if c["canonical_uid"] in done:
            continue
        rec = {"uid": c["canonical_uid"], "engine": name,
               "ts": datetime.now().isoformat(timespec="seconds")}
        for attempt in range(3):
            try:
                r = call(base, key, model, build_prompt(c), 600, extra)
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
                time.sleep(15 * (attempt + 1))
        with open(out, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        if (i + 1) % 20 == 0:
            print(f"[{name}] {i+1}/{len(cands)}", flush=True)
    print(f"[{name}] done", flush=True)

def report(cands):
    from collections import Counter
    by_uid = {}
    for name, *_ in ENGINES:
        p = os.path.join(BASE, f"anchor_judgments_{name}.jsonl")
        if not os.path.exists(p):
            continue
        for l in open(p, encoding="utf-8"):
            r = json.loads(l)
            if r.get("ok") and r.get("tier"):
                by_uid.setdefault(r["uid"], {})[name] = int(r["tier"])
    bank, pile = [], []
    for c in cands:
        uid = c["canonical_uid"]
        eng = by_uid.get(uid, {})
        if len(eng) < 2:
            pile.append((uid, "incomplete", eng))
            continue
        tiers = list(eng.values())
        agree = abs(tiers[0] - tiers[1]) <= 1
        mu = statistics.mean(tiers)
        rec = {"canonical_uid": uid, "tiers": eng, "expected_tier": round(mu, 2),
               "display_tier": int(round(mu)), "stratum": c["stratum"],
               "msc": c["msc"], "aliases": c["aliases"][:3]}
        if agree:
            bank.append(rec)
        else:
            pile.append((uid, f"disputed {tiers[0]} vs {tiers[1]}", eng))
    with open(os.path.join(BASE, "anchor_bank_v0.jsonl"), "w", encoding="utf-8") as f:
        for r in bank:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(os.path.join(BASE, "review_pile.md"), "w", encoding="utf-8") as f:
        f.write("# 锚点复核堆（v0，异步审阅，不阻塞）\n\n")
        for uid, why, eng in pile:
            f.write(f"- `{uid}`  {why}  {eng}\n")
    dist = Counter(r["display_tier"] for r in bank)
    msc_n = len({r["msc"] for r in bank})
    print(json.dumps({"bank": len(bank), "pile": len(pile),
                      "tier_distribution": {f"I{k}": v for k, v in sorted(dist.items())},
                      "msc_covered": msc_n}, ensure_ascii=False))
    need = {t: dist.get(t, 0) for t in range(1, 6)}
    print("quota check (need >=8/tier):", need,
          "PASS" if all(v >= 8 for v in need.values()) else "NEED TOP-UP")

if __name__ == "__main__":
    cands = json.load(open(CANDS, encoding="utf-8"))["candidates"]
    if RUBRIC is None:
        sys.exit("rubric_v11.txt missing")
    if "--report" in sys.argv:
        report(cands)
        sys.exit(0)
    threads = []
    for name, base, key, model, extra in ENGINES:
        if not key:
            print(f"[skip] {name}: no key")
            continue
        t = threading.Thread(target=run_engine,
                             args=(name, base, key, model, extra, cands), daemon=True)
        t.start(); threads.append(t)
    for t in threads:
        t.join()
    print("\n=== P1 REPORT ===")
    report(cands)
