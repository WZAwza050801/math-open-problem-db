#!/usr/bin/env python3
"""M13 verifier — runs on node01 (GLM 37cf). Independent judge, 0-4 levels.
Reads attempts dir synced from local, writes verdicts.jsonl.
Usage: python3 progress_verdict.py [limit]
"""
import json, os, sys, time, urllib.request, urllib.error

BASE = "/home/user/Wholeworks/wanganan/math_openproblem/pilot"
RUN = os.path.join(BASE, "runs", "difficulty-v1")
ATT = os.path.join(RUN, "attempts")
URL = "https://open.bigmodel.cn/api/coding/paas/v4/chat/completions"
MODEL = "glm-5.3"

LEVELS = """0 = 无有效进展：复述问题、明显错误、不可核查的猜测，或陈述不完整导致无法作答
1 = 可用探索：正确的小例子、文献化归、失败路线的有效诊断
2 = 局部进展：新的特殊情形、改进的界、可验证的计算证据或有效引理
3 = 主要突破：解决了核心障碍但仍有明确缺口
4 = 完整候选解：完整证明或反例（同时指出需要独立严格核验）"""

PROMPT = """You are a strict mathematical referee. A research model was given the open problem below and produced ONE attempt transcript. Grade the attempt.

Progress levels:
{levels}

Rules:
- Be skeptical: check whether claimed progress is actually verifiable/correct, not just plausible-sounding.
- If the attempt only restates the problem or makes unverifiable claims, grade 0.
- Grade the BEST verifiable content in the transcript.

Output ONLY JSON: {{"level": 0-4, "rationale": "不超过80字", "red_flags": "发现的问题或无"}}

Problem:
{statement}

Attempt transcript (may be truncated):
{attempt}
"""

def key():
    txt = open(os.path.join(BASE, "engine.sh")).read()
    m = re.search(r'NAME" = "glm".*?GLM_KEYS="([^"]+)"', txt, re.S)
    return m.group(1)

import re

def verify(item, att):
    body = json.dumps({"model": MODEL,
                       "messages": [{"role": "user", "content": PROMPT.format(
                           levels=LEVELS, statement=item["statement"][:4000],
                           attempt=att["content"][:30000])}],
                       "max_tokens": 400,
                       "thinking": {"type": "disabled"}}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Authorization": "Bearer " + key(), "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.load(r)
    txt = d["choices"][0]["message"]["content"] or ""
    m = re.search(r"\{[^}]*\}", txt, re.S)
    if not m:
        return {"level": None, "rationale": "parse_fail", "raw": txt[:150]}
    j = json.loads(m.group(0))
    lv = j.get("level")
    try:
        lv = int(lv)
        if not 0 <= lv <= 4: lv = None
    except Exception:
        lv = None
    return {"level": lv, "rationale": str(j.get("rationale", ""))[:120],
            "red_flags": str(j.get("red_flags", ""))[:120]}

def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 99999
    targets = {t["uid"]: t for t in json.load(
        open(os.path.join(RUN, "targets.json"), encoding="utf-8"))}
    out = os.path.join(RUN, "verdicts.jsonl")
    done = set()
    if os.path.exists(out):
        for l in open(out, encoding="utf-8"):
            if l.strip():
                done.add((json.loads(l)["uid"], json.loads(l)["traj"]))
    files = sorted(f for f in os.listdir(ATT) if f.endswith(".json"))
    n = 0
    for f in files:
        if n >= limit: break
        uid, _, tid = f[:-5].partition("__t")
        tid = int(tid)
        if (uid, tid) in done or uid not in targets:
            continue
        att = json.load(open(os.path.join(ATT, f), encoding="utf-8"))
        try:
            v = verify(targets[uid], att)
        except urllib.error.HTTPError as e:
            v = {"level": None, "rationale": f"http_{e.code}"}
        except Exception as e:
            v = {"level": None, "rationale": f"{type(e).__name__}: {str(e)[:80]}"}
        rec = {"uid": uid, "traj": tid, "attempt_sha256": att["attempt_sha256"],
               "model": MODEL, "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), **v}
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        n += 1
        print(f"  {uid} t{tid} -> level={v['level']} {v['rationale'][:50]}", flush=True)
        time.sleep(2)
    print(f"[verify] done {n}", flush=True)

if __name__ == "__main__":
    main()
