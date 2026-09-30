#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""s2_influence_judge.py — A/B/C/D influence adjudication (runs on node01).

ENGINE env: glm | qds   (key files .glm_key / .qds_key in pilot/, M13 pattern)
Input:  influence_calibration/influence_calibration_input.jsonl (or any pairs file, env JUDGE_INPUT)
Output: s2_influence/verdicts_{engine}.jsonl — checkpoint-resume by pair_id
Each verdict: {pair_id, engine, model, grade, confidence, reason, raw?}
Grades:
  A = substantive progress on THIS conjecture (solves/partial/disproves/improves)
  B = direct build-on (generalization, variant, core tool/motivation)
  C = nominal mention only (intro/related-work listing)
  D = unrelated to this conjecture (cites the source paper for other reasons)
"""
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "/home/user/Wholeworks/wanganan/math_openproblem/pilot"
WORK = os.path.join(BASE, "s2_influence")
ENGINE = os.environ.get("JUDGE_ENGINE", "glm")
URLS = {"glm": "https://open.bigmodel.cn/api/coding/paas/v4/chat/completions",
        "qds": "https://qianfan.baidubce.com/v2/tokenplan/personal/chat/completions"}
MODELS = {"glm": "glm-5.3", "qds": "deepseek-v4-pro"}
MAX_OUT = 4000 if ENGINE == "qds" else 2000
WORKERS = int(os.environ.get("JUDGE_WORKERS", "2"))
IN_FILE = os.environ.get("JUDGE_INPUT", os.path.join(WORK, "influence_calibration_input.jsonl"))
OUT_FILE = os.path.join(WORK, f"verdicts_{ENGINE}.jsonl")

PROMPT = """You are a mathematical librarian classifying citation relationships.

CONJECTURE C (an open problem card extracted from a paper P):
\"\"\"{statement}\"\"\"

CITING PAPER Q (which cites P):
Title: {title}
Abstract: {abstract}
Citation contexts (sentences in Q where P is cited):
{contexts}

Task: classify Q's relationship to THIS SPECIFIC conjecture C (not to P in general):
A = substantive progress on C: solves it, settles special cases, disproves it, or improves known bounds/conditions of C
B = direct build-on: generalizes C, poses variants of C, or uses C as a core tool/motivation for Q's main results
C = nominal mention: C (or P's relevance to C) appears only in introduction/related-work listing; Q's actual work does not depend on C
D = unrelated: Q cites P for other results/techniques/background; C plays no role

If the evidence is insufficient (e.g. no abstract, no contexts), choose the most likely grade and lower confidence.

Reply with ONLY a JSON object:
{{"grade": "A|B|C|D", "confidence": 0.0-1.0, "reason": "<=30 words, cite the decisive evidence"}}"""


def call(pair):
    ctx = "\n".join(f"  {i+1}. {c}" for i, c in enumerate(pair["contexts"])) or "  (none available)"
    prompt = PROMPT.format(statement=pair["card_statement"], title=pair["citing_title"],
                           abstract=pair["citing_abstract"] or "(none)", contexts=ctx)
    key = open(os.path.join(BASE, f".{ENGINE}_key")).read().strip()
    body = {"model": MODELS[ENGINE], "max_tokens": MAX_OUT, "temperature": 0.2,
            "messages": [{"role": "user", "content": prompt}]}
    if ENGINE == "glm":
        body["thinking"] = {"type": "disabled"}
    req = urllib.request.Request(URLS[ENGINE], data=json.dumps(body).encode(),
                                 method="POST",
                                 headers={"Authorization": "Bearer " + key,
                                          "Content-Type": "application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                d = json.load(r)
            txt = d["choices"][0]["message"].get("content") or ""
            usage = d.get("usage") or {}
            return parse(pair, txt, usage)
        except Exception as e:
            wait = 15 * (attempt + 1)
            print(f"  [{pair['pair_id']}] {type(e).__name__} {str(e)[:70]} -> {wait}s", flush=True)
            time.sleep(wait)
    return {"pair_id": pair["pair_id"], "engine": ENGINE, "grade": "ERROR",
            "confidence": 0, "reason": "api failed after retries"}


def parse(pair, txt, usage):
    s = txt.find("{")
    e = txt.rfind("}")
    rec = {"pair_id": pair["pair_id"], "engine": ENGINE, "model": MODELS[ENGINE],
           "tokens_in": usage.get("prompt_tokens"), "tokens_out": usage.get("completion_tokens")}
    try:
        j = json.loads(txt[s:e + 1])
        rec.update({"grade": str(j.get("grade", "?")).strip().upper()[:1],
                    "confidence": float(j.get("confidence", 0)),
                    "reason": str(j.get("reason", ""))[:300]})
    except Exception:
        rec.update({"grade": "PARSE_FAIL", "confidence": 0, "reason": txt[:300]})
    return rec


def main():
    pairs = [json.loads(l) for l in open(IN_FILE, encoding="utf-8") if l.strip()]
    done = set()
    if os.path.exists(OUT_FILE):
        for l in open(OUT_FILE, encoding="utf-8"):
            if l.strip():
                try:
                    done.add(json.loads(l)["pair_id"])
                except Exception:
                    pass
    todo = [p for p in pairs if p["pair_id"] not in done]
    print(f"[judge:{ENGINE}] total={len(pairs)} done={len(done)} todo={len(todo)}"
          f" workers={WORKERS}", flush=True)
    t0 = time.time()
    with open(OUT_FILE, "a", encoding="utf-8") as out, \
         ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for i, rec in enumerate(ex.map(call, todo), 1):
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            out.flush()
            if i % 10 == 0 or i == len(todo):
                el = time.time() - t0
                print(f"[judge:{ENGINE}] {i}/{len(todo)} elapsed={el/60:.1f}m"
                      f" eta={el/i*(len(todo)-i)/60:.1f}m", flush=True)
    print(f"[judge:{ENGINE}] DONE", flush=True)


if __name__ == "__main__":
    sys.exit(main())
