#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""influence_final_adjudication.py — 三家分歧对的旗舰终审（引擎无关）

对应 2026-10-01 用户拍板：三家判官仍分歧的对 + 双判官一致 A 的对，升高级 API
按"复合条件"终审；国内引擎尽量走 Coding Plan（零现金），按量旗舰只用于终审。

引擎无关设计：OpenAI 兼容协议，三样参数全走环境变量——
  FINAL_BASE_URL   端点（如 micu 的 GPT-5.6、modcon 的 Fable、kimi 官方 coding 端点）
  FINAL_API_KEY    钥匙（密码书抄入，绝不落 git）
  FINAL_MODEL      模型名
可选：
  FINAL_KEYFILE    钥匙文件路径（优先于 FINAL_API_KEY）
  FINAL_EXTRA_JSON 追加 body 字段（如 {"thinking":{"type":"disabled"}}）
  FINAL_WORKERS    并发（默认 2，旗舰推理型建议别开高）

强制留痕（模型责任标注）：每条 verdict 落盘时带
  vendor/model/prompt_sha256/endpoint_host/tokens —— 归档进 pilot/prompts/ 台账。

输入：
  influence_calibration/influence_retest_input.jsonl        300 对样本
  s2_influence/retest_verdicts_{glm,qds}.jsonl              双判官
  s2_influence/arbiter_doubao.jsonl                          豆包仲裁
输出：
  s2_influence/final_verdicts_{model}.jsonl                  断点续跑

触发条件（复合，本脚本只处理这两种）：
  1. 三家互不相同（或豆包缺席时两家差>=2档）
  2. 双判官一致判 A（两判官都给 A 的对，无论豆包如何）
"""
import hashlib
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

BASE = os.path.dirname(os.path.abspath(__file__))
PROMPT_FILE = os.path.join(BASE, "prompts", "influence_final_v2.txt")
IN_FILE = os.path.join(BASE, "influence_calibration", "influence_retest_input.jsonl")
G_FILE = os.path.join(BASE, "s2_influence", "retest_verdicts_glm.jsonl")
D_FILE = os.path.join(BASE, "s2_influence", "retest_verdicts_qds.jsonl")
A_FILE = os.path.join(BASE, "s2_influence", "arbiter_doubao.jsonl")
GRADES = "ABCD"

BASE_URL = os.environ.get("FINAL_BASE_URL", "")
MODEL = os.environ.get("FINAL_MODEL", "")
KEYFILE = os.environ.get("FINAL_KEYFILE", "")
API_KEY = os.environ.get("FINAL_API_KEY", "") or (open(KEYFILE).read().strip() if KEYFILE else "")
EXTRA = json.loads(os.environ.get("FINAL_EXTRA_JSON", "{}"))
WORKERS = int(os.environ.get("FINAL_WORKERS", "2"))

PROMPT = open(PROMPT_FILE, encoding="utf-8").read()
# 只要 prompt body（去掉文件头的建档说明）
BODY = PROMPT.split("--- PROMPT BODY ---", 1)[1].strip()
PROMPT_SHA = hashlib.sha256(PROMPT.encode("utf-8")).hexdigest()[:16]


def build_prompt(pair, ga, ra, gb, rb, gc, rc):
    ctx = "\n".join(f"  {i+1}. {c}" for i, c in enumerate(pair["contexts"])) or "  (none available)"
    return BODY.format(
        statement=pair["card_statement"], title=pair["citing_title"],
        abstract=pair["citing_abstract"] or "(none)", contexts=ctx,
        grade_a=ga or "n/a", reason_a=(ra or "")[:200],
        grade_b=gb or "n/a", reason_b=(rb or "")[:200],
        grade_c=gc or "n/a", reason_c=(rc or "")[:200])


def call(item):
    pid, prompt = item
    body = {"model": MODEL, "max_tokens": 3000, "temperature": 0.2,
            "messages": [{"role": "user", "content": prompt}]}
    body.update(EXTRA)
    req = urllib.request.Request(BASE_URL.rstrip("/") + "/chat/completions",
                                 data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": "Bearer " + API_KEY,
                                          "Content-Type": "application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                d = json.load(r)
            txt = d["choices"][0]["message"].get("content") or ""
            usage = d.get("usage") or {}
            s, e = txt.find("{"), txt.rfind("}")
            rec = {"pair_id": pid, "vendor": urlparse(BASE_URL).hostname, "model": MODEL,
                   "endpoint": BASE_URL, "prompt_sha256": PROMPT_SHA,
                   "tokens_in": usage.get("prompt_tokens"),
                   "tokens_out": usage.get("completion_tokens")}
            j = json.loads(txt[s:e + 1])
            rec.update({"crux": str(j.get("crux", ""))[:200],
                        "decisive_evidence": str(j.get("decisive_evidence", ""))[:300],
                        "grade": str(j.get("grade", "?")).strip().upper()[:1],
                        "confidence": float(j.get("confidence", 0)),
                        "reason": str(j.get("reason", ""))[:300]})
            return rec
        except Exception as ex:
            wait = 20 * (attempt + 1)
            print(f"  [{pid}] {type(ex).__name__} {str(ex)[:80]} -> {wait}s", flush=True)
            time.sleep(wait)
    return {"pair_id": pid, "vendor": urlparse(BASE_URL).hostname, "model": MODEL,
            "grade": "ERROR", "reason": "api failed after retries"}


def main():
    if not (BASE_URL and MODEL and API_KEY):
        sys.exit("缺引擎参数：FINAL_BASE_URL / FINAL_MODEL / FINAL_API_KEY(或 FINAL_KEYFILE)"
                 "\n例：FINAL_BASE_URL=https://<micu端点>/v1 FINAL_MODEL=gpt-5.6 "
                 "FINAL_KEYFILE=.micu_key python influence_final_adjudication.py")
    g, d, a = {}, {}, {}
    for f, store in ((G_FILE, g), (D_FILE, d), (A_FILE, a)):
        if os.path.exists(f):
            for l in open(f, encoding="utf-8"):
                if l.strip():
                    r = json.loads(l)
                    store[r["pair_id"]] = r
    pairs = {json.loads(l)["pair_id"]: json.loads(l)
             for l in open(IN_FILE, encoding="utf-8") if l.strip()}

    targets = {}
    for pid in pairs:
        ga, db, ab = g.get(pid, {}).get("grade"), d.get(pid, {}).get("grade"), a.get(pid, {}).get("grade")
        both_A = ga == "A" and db == "A"
        tri_disagree = (ab is not None and ab in GRADES and ga in GRADES and db in GRADES
                        and ab != ga and ab != db)
        if both_A or tri_disagree:
            targets[pid] = (ga, db, ab)
    print(f"[final] 终审目标：{len(targets)} 对"
          f"（双判一致A {sum(1 for v in targets.values() if v[0]=='A' and v[1]=='A')}"
          f" + 三家互异 {sum(1 for v in targets.values() if not (v[0]=='A' and v[1]=='A'))}）")
    print(f"[final] 引擎：{MODEL} @ {urlparse(BASE_URL).hostname}，"
          f"prompt_sha256={PROMPT_SHA}，workers={WORKERS}")

    out_file = os.path.join(BASE, "s2_influence", f"final_verdicts_{MODEL.replace('/', '_')}.jsonl")
    done = set()
    if os.path.exists(out_file):
        for l in open(out_file, encoding="utf-8"):
            if l.strip():
                try:
                    done.add(json.loads(l)["pair_id"])
                except Exception:
                    pass
    todo = [(pid, build_prompt(pairs[pid],
                               g.get(pid, {}).get("grade"), g.get(pid, {}).get("reason"),
                               d.get(pid, {}).get("grade"), d.get(pid, {}).get("reason"),
                               a.get(pid, {}).get("grade"), a.get(pid, {}).get("reason")))
            for pid in targets if pid not in done]
    print(f"[final] done={len(done)} todo={len(todo)} -> {out_file}", flush=True)

    t0 = time.time()
    with open(out_file, "a", encoding="utf-8") as out, \
         ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for i, rec in enumerate(ex.map(call, todo), 1):
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            out.flush()
            if i % 10 == 0 or i == len(todo):
                print(f"[final] {i}/{len(todo)} elapsed={(time.time()-t0)/60:.1f}m", flush=True)

    # 汇总
    fins = {}
    for l in open(out_file, encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            fins[r["pair_id"]] = r
    import collections
    print("[final] 档位分布：", dict(collections.Counter(
        v.get("grade") for v in fins.values())))
    over = {}
    for pid, (ga, db, ab) in targets.items():
        fg = fins.get(pid, {}).get("grade")
        if fg in GRADES:
            over[pid] = fg
    changed = sum(1 for pid, fg in over.items()
                  if targets[pid][0] in GRADES and targets[pid][1] in GRADES
                  and fg not in (targets[pid][0], targets[pid][1]))
    print(f"[final] 终审改判（不与任何原判官一致）：{changed}/{len(over)}")


if __name__ == "__main__":
    sys.exit(main())
