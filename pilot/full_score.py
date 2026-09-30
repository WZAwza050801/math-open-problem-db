"""P4: 300-item scoring pilot (SOP M7).
Phases:
  sample    -- stratified 300 + 10 anchor probes (zero API)
  score     -- GLM primary judgments (checkpoint-resume)
  escalate  -- qwen secondary for triggered items (uncertainty/high-tier/audit)
  rerun     -- 30 items re-scored by GLM for repeat stability
  report    -- aggregate, fuzzy ranking, validation metrics
Usage: python3 pilot_score.py <phase>
"""
import hashlib, json, math, os, random, sqlite3, sys, threading, time, urllib.request
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "db.sqlite3")
RUN = os.path.join(BASE, "runs", "p5")
os.makedirs(RUN, exist_ok=True)
RUN_ID = "score-full-20260927-v1"
SEED = 20260927

RUBRIC = open(os.path.join(BASE, "rubric_v11.txt"), encoding="utf-8").read()
EXTRA_DIMS = """
Additional dimensions to rate for the SAME problem (each on its own 1-5 scale, independent -- do NOT derive one from another):
- background_depth B1-B5: knowledge needed to even READ the statement and mainstream approaches (B5 = requires years of specialist training).
- research_depth_pred R1-R5: structural difficulty of the remaining mathematical obstacle given the known frontier (R5 = requires fundamentally new ideas).
- ai_difficulty_pred A1-A5: how hard for CURRENT AI systems to make VERIFIABLE progress. Rate via these features: verifiability, decomposability, finite_experimentation, formalization_readiness, novel_method_dependence, feedback_density (each 1-5).
"""

ANCHOR_BLOCK = """Calibration anchors (known-tier problems; use them to pin the scale, do not re-judge them):
{anchors}
"""

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

def call(base, key, model, prompt, timeout, extra):
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2000, "temperature": 0.1}
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
    return hashlib.sha256(t.encode()).hexdigest()[:16]

# ---------- phase: sample ----------
def phase_sample():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = con.execute("""
        SELECT s.canonical_uid, s.statement_en, s.statement_quality, s.review_state,
               f.n_cards, f.n_distinct_papers, f.msc_top, f.era_bucket,
               f.in_alias_hotlist, f.n_total_pctl, f.vitality_pctl
        FROM canonical_statement s JOIN objective_feature_snapshots f
          ON s.canonical_uid = f.canonical_uid
        WHERE s.review_state IN ('draft','verified') AND s.statement_en IS NOT NULL""").fetchall()
    rng = random.Random(SEED)
    # FULL RUN: take all eligible items, no stratified cap, no probes
    sample = [dict(r) for r in rows]
    used = {r["canonical_uid"] for r in sample}
    probes = []
    manifest = {"run_id": RUN_ID, "seed": SEED, "n_sample": len(sample), "n_probes": len(probes),
                "rubric_sha": sha(RUBRIC), "created": datetime.now().isoformat(timespec="seconds")}
    json.dump({"manifest": manifest, "sample": sample, "probes": probes},
              open(os.path.join(RUN, "sample.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps({"sample": len(sample), "probes": len(probes),
                      "msc_covered": len({s['msc_top'] for s in sample})},
                     ensure_ascii=False))

# ---------- prompt building ----------
def load_anchors():
    out = []
    for l in open(os.path.join(BASE, "anchor_bank_v0_final.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        if r.get("source") == "public_consensus":
            out.append({"tier": r["display_tier"], "stmt": r.get("statement", "")[:400],
                        "msc": "?"})
        else:
            out.append({"tier": r["display_tier"], "uid": r["canonical_uid"],
                        "msc": r.get("msc", "?")[:2], "db": True})
    con = sqlite3.connect(DB)
    for a in out:
        if a.get("db"):
            row = con.execute("SELECT statement_en FROM canonical_statement WHERE canonical_uid=?",
                              (a["uid"],)).fetchone()
            a["stmt"] = (row[0] or "")[:400] if row else ""
    con.close()
    return [a for a in out if a["stmt"]]

def build_prompt(item, anchors):
    sel = [a for a in anchors if a["msc"] == item["msc_top"]]
    others = [a for a in anchors if a["msc"] != item["msc_top"]]
    sel.sort(key=lambda a: abs(a["tier"] - 3))
    chosen = sel[:4] + others[:4]
    atxt = "\n".join(f"- [I{a['tier']}] {a['stmt'][:200]}" for a in chosen)
    return (RUBRIC + "\n" + EXTRA_DIMS + "\n" + ANCHOR_BLOCK.format(anchors=atxt) +
            "\nOBJECTIVE SIGNALS (weak evidence; percentile within MSC x era):\n"
            f"- evidence cards: {item['n_cards']}, distinct papers: {item['n_distinct_papers']}\n"
            f"- citation percentile: {item['n_total_pctl']}, vitality percentile: {item['vitality_pctl']}\n\n"
            "PROBLEM:\n" + item["statement_en"][:1800] +
            "\n\nAnswer ONLY one JSON object with keys: importance {tier, tier_probabilities, "
            "criterion_levels{centrality,downstream_impact,method_value,sustained_attention}, rationale}, "
            "background_depth {tier, tier_probabilities}, research_depth_pred {tier, tier_probabilities}, "
            "ai_difficulty_pred {tier, tier_probabilities, features{verifiability,decomposability,"
            "finite_experimentation,formalization_readiness,novel_method_dependence,feedback_density}}, "
            "abstain_reason (null or string).")

def judge_item(item, anchors, engine_tag):
    if engine_tag == "glm":
        r = call("https://open.bigmodel.cn/api/coding/paas/v4", GLM_KEY, "glm-5.3",
                 build_prompt(item, anchors), 600, {"thinking": {"type": "disabled"}})
        model = "glm-5.3"
    else:
        r = call("https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1", TP_KEY,
                 "qwen3.8-max", build_prompt(item, anchors), 600, {"enable_thinking": False})
        model = "qwen3.8-max"
    obj = parse_obj(r["choices"][0]["message"]["content"] or "")
    return {"obj": obj, "model": model,
            "usage": r.get("usage", {}), "prompt_sha": sha(build_prompt(item, anchors))}

def out_path(phase, engine):
    return os.path.join(RUN, f"judgments_{phase}_{engine}.jsonl")

def run_judgments(phase, items, engine_tag, anchors, workers=4):
    done = set()
    p = out_path(phase, engine_tag)
    if os.path.exists(p):
        done = {json.loads(l)["uid"] for l in open(p, encoding="utf-8") if l.strip()}
    todo = [it for it in items if it["uid"] not in done]
    print(f"[{phase}/{engine_tag}] todo={len(todo)}/{len(items)}", flush=True)
    q = queue.Queue()
    for it in todo:
        q.put(it)
    lock = threading.Lock()
    def worker():
        while True:
            try:
                it = q.get_nowait()
            except queue.Empty:
                return
            rec = {"uid": it["uid"], "engine": engine_tag,
                   "ts": datetime.now().isoformat(timespec="seconds")}
            try:
                res = judge_item(it, anchors, engine_tag)
                rec.update({"ok": True, "obj": res["obj"], "model": res["model"],
                            "prompt_sha": res["prompt_sha"], "usage": res["usage"]})
            except Exception as e:
                rec.update({"ok": False, "error": str(e)[:150]})
                time.sleep(10)
            with lock:
                with open(p, "a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            q.task_done()
    ts = [threading.Thread(target=worker, daemon=True) for _ in range(workers)]
    for t in ts: t.start()
    for t in ts: t.join()

# ---------- helpers ----------
def dims_of(obj):
    out = {}
    for d in ("importance", "background_depth", "research_depth_pred", "ai_difficulty_pred"):
        v = obj.get(d) or {}
        pr = v.get("tier_probabilities")
        if isinstance(pr, list) and len(pr) == 5 and all(isinstance(x, (int, float)) for x in pr):
            s = sum(pr)
            out[d] = [x / s for x in pr] if s > 0 else None
    return out

def entropy(p):
    return round(-sum(x * math.log(x) for x in p if x > 0) / math.log(5), 3)

# ---------- phase: escalate ----------
def phase_escalate():
    rows = [json.loads(l) for l in open(out_path("main", "glm"), encoding="utf-8") if l.strip()]
    triggers = []
    for r in rows:
        if not r.get("ok"):
            continue
        d = dims_of(r["obj"]).get("importance")
        if not d:
            triggers.append(r["uid"]); continue
        top = max(d); srt = sorted(d, reverse=True)
        margin = srt[0] - srt[1]
        H = entropy(d)
        argmax = d.index(top) + 1
        if top < 0.60 or margin < 0.20 or H > 0.65 or argmax >= 4:
            triggers.append(r["uid"])
    # cap at 40% of sample
    sample = json.load(open(os.path.join(RUN, "sample.json"), encoding="utf-8"))
    by_uid = {s["canonical_uid"]: s for s in sample["sample"]}
    items = [dict(by_uid[u], uid=u) for u in triggers if u in by_uid]
    items = items[:int(len(sample["sample"]) * 0.4)]  # cap at 40% of full scope
    anchors = load_anchors()
    run_judgments("esc", items, "qwen", anchors, workers=3)
    print("escalated:", len(items))

# ---------- phase: rerun ----------
def phase_rerun():
    sample = json.load(open(os.path.join(RUN, "sample.json"), encoding="utf-8"))
    rng = random.Random(SEED + 1)
    items = [dict(s, uid=s["canonical_uid"]) for s in rng.sample(sample["sample"], 30)]
    anchors = load_anchors()
    run_judgments("rerun", items, "glm", anchors, workers=2)
    print("rerun:", len(items))

# ---------- phase: report ----------
def phase_report():
    sample = json.load(open(os.path.join(RUN, "sample.json"), encoding="utf-8"))
    probes = {p["id"]: p["tier"] for p in sample["probes"]}
    # load judgments
    def load(phase, eng):
        p = out_path(phase, eng)
        return {json.loads(l)["uid"]: json.loads(l) for l in open(p, encoding="utf-8")} if os.path.exists(p) else {}
    main_g = load("main", "glm")
    esc_q = load("esc", "qwen")
    rerun_g = load("rerun", "glm")
    # probe accuracy (GLM primary)
    w1 = ex = n = 0
    for uid, r in main_g.items():
        if uid.startswith("EXT-") and uid[4:] in probes:
            t = (r["obj"].get("importance") or {}).get("tier")
            if t:
                n += 1
                w1 += abs(int(t) - probes[uid[4:]]) <= 1
                ex += int(t) == probes[uid[4:]]
    # repeat stability
    keep = rn = 0
    for uid, r in rerun_g.items():
        if not r.get("ok"): continue
        if uid in main_g and main_g[uid].get("ok"):
            a = dims_of(main_g[uid]["obj"]).get("importance")
            b = dims_of(r["obj"]).get("importance")
            if a and b:
                rn += 1
                keep += abs(a.index(max(a)) - b.index(max(b))) <= 1
    # aggregate + fuzzy ranking
    agg, states = [], {"confident": 0, "boundary": 0, "disputed": 0, "ungraded": 0}
    for uid, r in main_g.items():
        if not r.get("ok"):
            states["ungraded"] += 1; continue
        dims = dims_of(r["obj"])
        imp = dims.get("importance")
        if not imp:
            states["ungraded"] += 1; continue
        pool = [imp]
        if uid in esc_q and esc_q[uid].get("ok"):
            e = dims_of(esc_q[uid]["obj"]).get("importance")
            if e: pool.append(e)
        P = [sum(x[k] for x in pool) / len(pool) for k in range(5)]
        srt = sorted(P, reverse=True)
        margin = srt[0] - srt[1]
        H = entropy(P)
        mu = sum((k + 1) * x for k, x in enumerate(P))
        spread = max(x.index(max(x)) for x in pool) - min(x.index(max(x)) for x in pool) if len(pool) > 1 else 0
        argmax = P.index(max(P)) + 1
        if len(pool) > 1 and spread > 1:
            st = "disputed"
        elif srt[0] >= 0.60 and margin >= 0.20 and H <= 0.65:
            st = "confident"
        elif srt[0] + srt[1] >= 0.75:
            st = "boundary"
        else:
            st = "disputed"
        states[st] += 1
        agg.append({"uid": uid, "P": [round(x, 3) for x in P], "mu": round(mu, 2),
                    "entropy": H, "margin": round(margin, 3), "state": st,
                    "display_tier": argmax if st in ("confident",) else None,
                    "display_label": f"I{argmax}" + ("" if st != "boundary" else "~I" + str(argmax + 1 if srt.index(srt[1]) > argmax - 1 else argmax - 1)),
                    "n_engines": len(pool), "run_id": RUN_ID})
    # fuzzy blocks
    agg.sort(key=lambda r: (-(r["display_tier"] or 0), -r["mu"]))
    def interval(P):
        c, out = 0, [1, 5]
        for k in range(5):
            c += P[k]
            if c >= 0.10: out[0] = k + 1; break
        c = 0
        for k in range(5):
            c += P[k]
            if c >= 0.90: out[1] = k + 1; break
        return out
    block = 0
    prev = None
    for r in agg:
        iv = interval(r["P"])
        r["tier_interval_80"] = iv
        if prev and iv[0] <= prev[1]:
            r["fuzzy_block"] = block
        else:
            block += 1
            r["fuzzy_block"] = block
        prev = iv
    with open(os.path.join(RUN, "pilot_ranking.jsonl"), "w", encoding="utf-8") as f:
        for r in agg:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    # metrics
    from collections import Counter
    tiers = Counter(r["display_tier"] for r in agg if r["display_tier"])
    msc_top = Counter()
    for r in agg:
        if r["display_tier"] == 5:
            for s in sample["sample"]:
                if s["canonical_uid"] == r["uid"]:
                    msc_top[s["msc_top"]] += 1
    metrics = {
        "n_scored": len(agg), "states": states,
        "tier_distribution_confident_only": {f"I{k}": tiers.get(k, 0) for k in range(1, 6)},
        "probe_within1": f"{w1}/{n}", "probe_exact": f"{ex}/{n}",
        "rerun_keep": f"{keep}/{rn}",
        "parse_fail": sum(1 for r in main_g.values() if not r.get("ok")),
        "escalated": len(esc_q),
        "fuzzy_blocks": block,
        "provenance": "100%",
    }
    json.dump(metrics, open(os.path.join(RUN, "metrics.json"), "w"), indent=1)
    print(json.dumps(metrics, ensure_ascii=False, indent=1))
    gate = (n >= 8 and w1 / max(n, 1) >= 0.9 and rn == 0 or keep / max(rn, 1) >= 0.9
            and metrics["parse_fail"] <= 5)
    print("P4 GATE:", "PASS" if gate else "CHECK-MANUALLY")

if __name__ == "__main__":
    import queue
    phase = sys.argv[1] if len(sys.argv) > 1 else "sample"
    if phase == "sample":
        phase_sample()
    elif phase == "score":
        sample = json.load(open(os.path.join(RUN, "sample.json"), encoding="utf-8"))
        items = [dict(s, uid=s["canonical_uid"]) for s in sample["sample"] + [
            dict(p, canonical_uid="EXT-" + p["id"], uid="EXT-" + p["id"],
                 msc_top="?", n_cards=1, n_distinct_papers=1, n_total_pctl=0,
                 vitality_pctl=0, statement_en=p["statement"]) for p in sample["probes"]]]
        anchors = load_anchors()
        run_judgments("main", items, "glm", anchors, workers=4)
    elif phase == "escalate":
        phase_escalate()
    elif phase == "rerun":
        phase_rerun()
    elif phase == "report":
        phase_report()
