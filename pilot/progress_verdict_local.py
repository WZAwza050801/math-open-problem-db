#!/usr/bin/env python3
"""M13 verifier — LOCAL version on doubao-seed-2.1-pro (Volcano Ark).
Independent judge, 0-4 levels. Reads local attempts, appends verdicts.jsonl.
Usage: python progress_verdict_local.py [limit]
"""
import json, os, sys, time, re, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(BASE, "runs", "difficulty-v1")
ATT = os.path.join(RUN, "attempts")
URL = os.environ.get("VERIFY_URL", "https://ark.cn-beijing.volces.com/api/v3/chat/completions")
MODEL = os.environ.get("VERIFY_MODEL", "doubao-seed-2-1-pro-260628")
KEY = open(os.environ.get("VERIFY_KEYFILE", os.path.join(BASE, ".ark_key"))).read().strip()
WORKERS = 3

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


def verify(item, att):
    body = {"model": MODEL,
            "messages": [{"role": "user", "content": PROMPT.format(
                levels=LEVELS, statement=item["statement"][:4000],
                attempt=att["content"][:30000])}],
            "max_tokens": int(os.environ.get("VERIFY_MAX_TOKENS", "2000"))}
    if os.environ.get("VERIFY_THINK_DISABLED") == "1":
        body["thinking"] = {"type": "disabled"}
    payload = json.dumps(body).encode()
    req = urllib.request.Request(URL, data=payload, headers={
        "Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    last = None
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.load(r)
            break
        except urllib.error.HTTPError as e:
            last = f"http_{e.code}"
            if e.code == 429 and i < 3:
                time.sleep(30 * (i + 1))
                continue
            raise RuntimeError(last)
        except Exception as e:
            last = f"{type(e).__name__}: {str(e)[:80]}"
            if i < 3:
                time.sleep(15)
                continue
            raise RuntimeError(last)
    txt = (d.get("choices") or [{}])[0].get("message", {}).get("content") or ""
    if not txt:
        txt = (d.get("choices") or [{}])[0].get("message", {}).get("reasoning_content") or ""
    # robust JSON extraction: fenced block first, then brace-matched scan
    cands = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", txt, re.S)
    if not cands:
        for i, ch in enumerate(txt):
            if ch == "{":
                depth = 0
                for j in range(i, len(txt)):
                    if txt[j] == "{":
                        depth += 1
                    elif txt[j] == "}":
                        depth -= 1
                        if depth == 0:
                            cands.append(txt[i:j + 1])
                            break
    for c in cands:
        try:
            j = json.loads(c)
            if isinstance(j, dict) and "level" in j:
                lv = j.get("level")
                try:
                    lv = int(lv)
                    if not 0 <= lv <= 4:
                        lv = None
                except Exception:
                    lv = None
                return {"level": lv, "rationale": str(j.get("rationale", ""))[:120],
                        "red_flags": str(j.get("red_flags", ""))[:120]}
        except Exception:
            continue
    return {"level": None, "rationale": "parse_fail", "raw": txt[:150]}


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 99999
    targets_path = os.environ.get("VERIFY_TARGETS", os.path.join(BASE, "difficulty_targets.json"))
    targets = {t["uid"]: t for t in json.load(open(targets_path, encoding="utf-8"))}
    out = os.environ.get("VERIFY_OUT", os.path.join(RUN, "verdicts.jsonl"))
    done = set()
    if os.path.exists(out):
        for l in open(out, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                done.add((r["uid"], r["traj"]))
    files = sorted(f for f in os.listdir(ATT) if f.endswith(".json"))
    todo = []
    for f in files:
        uid, _, tid = f[:-5].partition("__t")
        tid = int(tid)
        if (uid, tid) in done or uid not in targets:
            continue
        todo.append((f, uid, tid))
    todo = todo[:limit]
    print(f"[verify-local] todo={len(todo)} model={MODEL} workers={WORKERS}", flush=True)
    lock_write = open(out, "a", encoding="utf-8")
    n = 0
    with ThreadPoolExecutor(WORKERS) as ex:
        futs = {}
        for f, uid, tid in todo:
            att = json.load(open(os.path.join(ATT, f), encoding="utf-8"))
            futs[ex.submit(verify, targets[uid], att)] = (f, uid, tid, att)
        for fu in as_completed(futs):
            f, uid, tid, att = futs[fu]
            try:
                v = fu.result()
            except Exception as e:
                v = {"level": None, "rationale": str(e)[:100]}
            rec = {"uid": uid, "traj": tid, "attempt_sha256": att["attempt_sha256"],
                   "model": MODEL, "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), **v}
            lock_write.write(json.dumps(rec, ensure_ascii=False) + "\n")
            lock_write.flush()
            n += 1
            print(f"  {uid} t{tid} -> level={v['level']} {str(v['rationale'])[:50]} [{n}/{len(todo)}]", flush=True)
    lock_write.close()
    print(f"[verify-local] done {n}", flush=True)


if __name__ == "__main__":
    main()
