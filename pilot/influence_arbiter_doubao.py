#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""influence_arbiter_doubao.py — 第三引擎仲裁小试（豆包，火山引擎 Ark）

对应 NEXT_PHASE_PLAN §11.3 升级路径：300 对复测外推人工队列约 5,651 对 > 300 门禁，
升级第三引擎仲裁。本脚本是小试（T20 后续）：
  输入 = 300 对复测中两判官"差>=2档"的分歧对 + 任一判官判 A 的对（去重）
  规则 = 豆包独立判一遍；与任一判官一致 -> 采用该档；三家互不相同 -> 仍进人工
  输出 = s2_influence/arbiter_doubao.jsonl（pair_id 断点续跑）+ 汇总压缩率
规模：本批约 81 + 29 ≈ 105 对，量极小（几千 token 级）。
"""
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "/home/user/Wholeworks/wanganan/math_openproblem/pilot"
CAL = os.path.join(BASE, "influence_calibration")
IN_FILE = os.path.join(CAL, "influence_retest_input.jsonl")
G_FILE = os.path.join(BASE, "s2_influence", "retest_verdicts_glm.jsonl")
D_FILE = os.path.join(BASE, "s2_influence", "retest_verdicts_qds.jsonl")
OUT_FILE = os.path.join(BASE, "s2_influence", "arbiter_doubao.jsonl")

URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
MODEL = os.environ.get("ARB_MODEL", "doubao-seed-2-1-pro-260628")
KEY = open(os.path.join(BASE, ".ark_key")).read().strip()
WORKERS = int(os.environ.get("ARB_WORKERS", "3"))
GRADES = "ABCD"

PROMPT = """You are a tie-breaking mathematical librarian. Two other librarians disagreed about the citation relationship below; you are the independent third vote.

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

Reply with ONLY a JSON object:
{{"grade": "A|B|C|D", "confidence": 0.0-1.0, "reason": "<=30 words, cite the decisive evidence"}}"""


def call(pair):
    ctx = "\n".join(f"  {i+1}. {c}" for i, c in enumerate(pair["contexts"])) or "  (none available)"
    prompt = PROMPT.format(statement=pair["card_statement"], title=pair["citing_title"],
                           abstract=pair["citing_abstract"] or "(none)", contexts=ctx)
    body = {"model": MODEL, "max_tokens": 2000, "temperature": 0.2,
            "messages": [{"role": "user", "content": prompt}]}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": "Bearer " + key,
                                          "Content-Type": "application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                d = json.load(r)
            txt = d["choices"][0]["message"].get("content") or ""
            s, e = txt.find("{"), txt.rfind("}")
            rec = {"pair_id": pair["pair_id"], "engine": "doubao", "model": MODEL}
            j = json.loads(txt[s:e + 1])
            rec.update({"grade": str(j.get("grade", "?")).strip().upper()[:1],
                        "confidence": float(j.get("confidence", 0)),
                        "reason": str(j.get("reason", ""))[:300]})
            return rec
        except Exception as ex:
            wait = 15 * (attempt + 1)
            print(f"  [{pair['pair_id']}] {type(ex).__name__} {str(ex)[:70]} -> {wait}s", flush=True)
            time.sleep(wait)
    return {"pair_id": pair["pair_id"], "engine": "doubao", "grade": "ERROR",
            "confidence": 0, "reason": "api failed after retries"}


def main():
    g, d = {}, {}
    for line in open(G_FILE):
        r = json.loads(line); g[r["pair_id"]] = r.get("grade")
    for line in open(D_FILE):
        r = json.loads(line); d[r["pair_id"]] = r.get("grade")

    pairs = {json.loads(l)["pair_id"]: json.loads(l)
             for l in open(IN_FILE) if l.strip()}
    targets = []
    for pid in pairs:
        ga, db = g.get(pid), d.get(pid)
        if ga not in GRADES or db not in GRADES:
            targets.append(pid)  # PARSE_FAIL/ERROR 也送仲裁
        elif abs(GRADES.index(ga) - GRADES.index(db)) >= 2:
            targets.append(pid)
        elif "A" in (ga, db):
            targets.append(pid)
    print(f"[arbiter] 分歧>=2档 + PARSE_FAIL + 任一判A 的对：{len(targets)}", flush=True)

    done = set()
    if os.path.exists(OUT_FILE):
        for l in open(OUT_FILE):
            if l.strip():
                try:
                    done.add(json.loads(l)["pair_id"])
                except Exception:
                    pass
    todo = [pairs[pid] for pid in targets if pid not in done]
    print(f"[arbiter] done={len(done)} todo={len(todo)} workers={WORKERS}", flush=True)
    t0 = time.time()
    with open(OUT_FILE, "a", encoding="utf-8") as out, \
         ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for i, rec in enumerate(ex.map(call, todo), 1):
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            out.flush()
            if i % 20 == 0 or i == len(todo):
                el = time.time() - t0
                print(f"[arbiter] {i}/{len(todo)} elapsed={el/60:.1f}m", flush=True)

    # ---------- 汇总：仲裁能压掉多少人工 ----------
    arb = {}
    for l in open(OUT_FILE):
        if l.strip():
            r = json.loads(l); arb[r["pair_id"]] = r.get("grade")
    resolved = still = a_flag = 0
    n_valid = 0
    for pid in targets:
        ga, db, ab = g.get(pid), d.get(pid), arb.get(pid)
        if pid not in arb:
            continue
        n_valid += 1
        if ab not in GRADES:
            still += 1
            continue
        if ga in GRADES and db in GRADES:
            if abs(GRADES.index(ga) - GRADES.index(db)) >= 2:
                if ab in (ga, db):
                    resolved += 1
                else:
                    still += 1
            elif "A" in (ga, db):
                a_flag += 1   # A 档仍强制人工（规则第 4 条不因仲裁放松）
                if ab in (ga, db):
                    resolved += 1  # 但档位可以由仲裁定，人工只做复核
        else:
            if ab in (x for x in (ga, db) if x in GRADES) or ab in GRADES:
                resolved += 1
    print(f"[arbiter] 仲裁判完 {n_valid}/{len(targets)}："
          f"分歧对被仲裁解决 {resolved}，仍进人工 {still}，A档强制复核 {a_flag}")
    N = 27689
    # 全量外推：差>=2档占 7.1%+1.4% = 8.5% ≈ 2355 对是仲裁目标
    print(f"[arbiter] 全量外推（如压缩率同本批）："
          f"差>=2档仲裁目标约 {int(N * 0.085)} 对，"
          f"按本批解决率后仍进人工约 {int(N * 0.085 * (still / max(n_valid, 1)))} 对")


if __name__ == "__main__":
    sys.exit(main())
