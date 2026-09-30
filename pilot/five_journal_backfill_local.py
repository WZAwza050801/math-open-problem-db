#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""five_journal_backfill_local.py — 五刊缺口 × arXiv 重匹配（本地版，2026-09-30）

和 node01 版逻辑一致，差异：
- 输入 backfill_missing.json（node01 导出的 2722 条缺口，本地不需要 db）
- TIME_BUDGET 秒后优雅退出（分片跑），BACKFILL_LIMIT 条数上限（冒烟用）
- lockfile 互斥，防止 automation 与手动跑撞车
- arXiv 429 专门退避
产出：five_journal_backfill.json（同步到 node01 供 daemon 优先消费）+ state jsonl 断点
"""
import json, difflib, os, re, sys, time, urllib.request, urllib.parse
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
MISSING = os.path.join(BASE, "backfill_missing.json")
OUT = os.path.join(BASE, "five_journal_backfill.json")
STATE = os.path.join(BASE, "five_journal_backfill_state.jsonl")
LOG = os.path.join(BASE, "logs", "backfill_local.log")
LOCK = os.path.join(BASE, "backfill_local.lock")
GAP = 3.5
SIM_MIN = 0.90
UA = "openproblem-backfill/1.0 (mailto:3116809059@qq.com)"

def log(msg):
    line = f"{datetime.now().strftime('%m-%d %H:%M:%S')} {msg}"
    print(line, flush=True)
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def norm_title(t):
    t = (t or "").lower()
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def load_state():
    done = {}
    if os.path.exists(STATE):
        for line in open(STATE, encoding="utf-8"):
            try:
                d = json.loads(line)
                done[d["doi"]] = d
            except Exception:
                continue
    return done

def main():
    budget = int(os.environ.get("TIME_BUDGET", "0"))   # 秒，0=不限
    limit = int(os.environ.get("BACKFILL_LIMIT", "0"))
    t_start = time.time()

    if os.path.exists(LOCK):
        log("[backfill-local] lock exists, another instance running -> exit")
        return
    with open(LOCK, "w") as f:
        f.write(str(os.getpid()))
    try:
        _run(budget, limit, t_start)
    finally:
        if os.path.exists(LOCK):
            os.remove(LOCK)

def _run(budget, limit, t_start):
    missing = json.load(open(MISSING, encoding="utf-8"))
    log(f"[backfill-local] missing list {len(missing)}")

    state = load_state()
    candidates = []
    if os.path.exists(OUT):
        try:
            candidates = json.load(open(OUT, encoding="utf-8"))
            have_aids = {c["arxiv_id"] for c in candidates}
        except Exception:
            candidates, have_aids = [], set()
    else:
        have_aids = set()

    n_ok = n_no = n_err = 0
    consec_err = 0
    processed = 0
    for idx, e in enumerate(missing):
        if budget and time.time() - t_start > budget:
            log(f"[backfill-local] time budget {budget}s reached -> stop")
            break
        if limit and processed >= limit:
            log(f"[backfill-local] limit {limit} reached -> stop")
            break
        doi = e["doi"]
        if state.get(doi, {}).get("result") in ("ok", "no_arxiv_match"):
            st = state[doi]
            if st.get("result") == "ok" and st.get("arxiv_id") and st["arxiv_id"] not in have_aids:
                candidates.append(st["candidate"])
                have_aids.add(st["arxiv_id"])
            continue

        title = e.get("title") or ""
        q = urllib.parse.quote(f'ti:"{title}"')
        url = f"https://export.arxiv.org/api/query?search_query={q}&max_results=5"
        found = None
        net_err = False
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=45) as resp:
                    xml = resp.read().decode("utf-8", "replace")
                entries = re.findall(r"<entry>(.*?)</entry>", xml, re.S)
                nt = norm_title(title)
                for en in entries:
                    aid_m = re.search(r"<id>https?://arxiv.org/abs/([^<]+)</id>", en)
                    t_m = re.search(r"<title>(.*?)</title>", en, re.S)
                    if not aid_m or not t_m:
                        continue
                    cand_title = re.sub(r"\s+", " ", t_m.group(1)).strip()
                    sim = difflib.SequenceMatcher(None, nt, norm_title(cand_title)).ratio()
                    y_m = re.search(r"<published>(\d{4})", en)
                    ay = int(y_m.group(1)) if y_m else 0
                    py = int(e.get("year") or 0)
                    if sim >= SIM_MIN and (py == 0 or ay == 0 or py <= ay <= py + 2):
                        found = {"arxiv_id": aid_m.group(1).strip(), "title": cand_title,
                                 "journal": e["journal"], "pub_year": py,
                                 "crossref_doi": doi, "crossref_journal": "",
                                 "match_method": "title_rejoin_0930_local", "sim": round(sim, 3),
                                 "source_file": "five_journal_backfill"}
                        break
                break
            except urllib.error.HTTPError as ex:
                if ex.code == 429:
                    time.sleep(20)   # arXiv 限流，退避
                net_err = True
                n_err += 1
                consec_err += 1
                log(f"[backfill-local] err {doi}: HTTP {ex.code} (attempt {attempt+1})")
                time.sleep(10)
            except Exception as ex:
                net_err = True
                n_err += 1
                consec_err += 1
                log(f"[backfill-local] err {doi}: {type(ex).__name__} {str(ex)[:60]} (attempt {attempt+1})")
                time.sleep(10)
        processed += 1
        if found:
            n_ok += 1
            consec_err = 0
            state[doi] = {"doi": doi, "result": "ok", "arxiv_id": found["arxiv_id"],
                          "candidate": found}
            if found["arxiv_id"] not in have_aids:
                candidates.append(found)
                have_aids.add(found["arxiv_id"])
        elif net_err:
            state[doi] = {"doi": doi, "result": "error"}
            with open(STATE, "a", encoding="utf-8") as f:
                f.write(json.dumps(state[doi], ensure_ascii=False) + "\n")
            if consec_err >= 10:
                log(f"[backfill-local] {consec_err} consecutive net errors -> local net down?, sleep 5min")
                time.sleep(300)
                consec_err = 0
            continue
        else:
            n_no += 1
            consec_err = 0
            state[doi] = {"doi": doi, "result": "no_arxiv_match"}
        with open(STATE, "a", encoding="utf-8") as f:
            f.write(json.dumps(state[doi], ensure_ascii=False) + "\n")

        if (idx + 1) % 50 == 0:
            json.dump(candidates, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
            log(f"[backfill-local] progress {idx+1}/{len(missing)} ok={n_ok} no={n_no} err={n_err} new_arxiv={len(candidates)}")
        time.sleep(GAP)

    json.dump(candidates, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    log(f"[backfill-local] EXIT processed={processed} ok={n_ok} no={n_no} err={n_err} -> {OUT} ({len(candidates)} candidates)")

if __name__ == "__main__":
    main()
