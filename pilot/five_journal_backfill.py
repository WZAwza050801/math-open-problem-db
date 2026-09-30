#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""five_journal_backfill.py — 五刊目录缺口 × arXiv 重匹配 (2026-09-29)

逻辑：crossref_toc.json (4437 篇权威目录) − db 已入库 − 当前批处理中
     → 对缺口逐条到 arXiv API 按标题搜索 → 标题相似度≥0.9 且年份合理才收
产出：five_journal_backfill.json（daemon 池子里优先级最高的文件）
断点：five_journal_backfill_state.jsonl 记录每个 doi 的结果，重启跳过
限速：arXiv API 3.5s/req，全量 ~3000 条 ≈ 3 小时
"""
import json, difflib, os, re, sys, time, urllib.request, urllib.parse, sqlite3
from datetime import datetime

BASE = "/home/user/Wholeworks/wanganan/math_openproblem/pilot"
TOC = os.path.join(BASE, "crossref_toc.json")
OUT = os.path.join(BASE, "five_journal_backfill.json")
STATE = os.path.join(BASE, "five_journal_backfill_state.jsonl")
LOG = os.path.join(BASE, "logs", "backfill_0929.log")
GAP = 3.5
SIM_MIN = 0.90

os.chdir(BASE)

def log(msg):
    line = f"{datetime.now().strftime('%m-%d %H:%M:%S')} {msg}"
    print(line, flush=True)
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
    limit = int(os.environ.get("BACKFILL_LIMIT", "0"))
    toc = json.load(open(TOC, encoding="utf-8"))

    con = sqlite3.connect(f"file:{BASE}/db.sqlite3?mode=ro", uri=True)
    db_dois = {r[0].strip().lower() for r in con.execute(
        "SELECT crossref_doi FROM papers WHERE crossref_doi IS NOT NULL AND crossref_doi!=''")}
    db_titles = {norm_title(r[0]) for r in con.execute("SELECT title FROM papers") if r[0]}
    # 当前在跑/在池的（next_batch_v2 候选带 crossref_doi）
    cur_dois = set()
    try:
        for x in json.load(open(os.path.join(BASE, "next_batch_v2_0929.json"))):
            d = (x.get("crossref_doi") or "").strip().lower()
            if d:
                cur_dois.add(d)
    except Exception:
        pass

    missing = []
    for jr, lst in toc.items():
        for e in lst:
            doi = (e.get("doi") or "").strip().lower()
            if not doi or doi in db_dois or doi in cur_dois:
                continue
            if norm_title(e.get("title")) in db_titles:
                continue
            missing.append((jr, e))
    log(f"[backfill] TOC total {sum(len(v) for v in toc.values())}, missing {len(missing)}")

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
    for idx, (jr, e) in enumerate(missing):
        doi = (e.get("doi") or "").strip().lower()
        if doi in state and state[doi].get("result") in ("ok", "no_arxiv_match"):
            st = state[doi]
            if st.get("result") == "ok" and st.get("arxiv_id") and st["arxiv_id"] not in have_aids:
                candidates.append(st["candidate"])
                have_aids.add(st["arxiv_id"])
            continue
        if limit and idx >= limit:
            break

        title = e.get("title") or ""
        q = urllib.parse.quote(f'ti:"{title}"')
        url = f"https://export.arxiv.org/api/query?search_query={q}&max_results=5"
        found = None
        net_err = False
        for attempt in range(4):
            try:
                with urllib.request.urlopen(url, timeout=45) as resp:
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
                                 "journal": jr, "pub_year": py,
                                 "crossref_doi": doi, "crossref_journal": e.get("journal") or "",
                                 "match_method": "title_rejoin_0929", "sim": round(sim, 3),
                                 "source_file": "five_journal_backfill"}
                        break
                break
            except Exception as ex:
                net_err = True
                n_err += 1
                consec_err += 1
                log(f"[backfill] err {doi}: {type(ex).__name__} {str(ex)[:60]} (attempt {attempt+1})")
                time.sleep(10)
        if found:
            n_ok += 1
            consec_err = 0
            state[doi] = {"doi": doi, "result": "ok", "arxiv_id": found["arxiv_id"],
                          "candidate": found}
            if found["arxiv_id"] not in have_aids:
                candidates.append(found)
                have_aids.add(found["arxiv_id"])
        elif net_err:
            # 网络错误不算定论，记 error 状态，下轮重试
            state[doi] = {"doi": doi, "result": "error"}
            with open(STATE, "a", encoding="utf-8") as f:
                f.write(json.dumps(state[doi], ensure_ascii=False) + "\n")
            if consec_err >= 10:
                log(f"[backfill] {consec_err} consecutive net errors -> egress down, sleep 10min")
                time.sleep(600)
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
            log(f"[backfill] progress {idx+1}/{len(missing)} ok={n_ok} no={n_no} err={n_err} new_arxiv={len(candidates)}")
        time.sleep(GAP)

    json.dump(candidates, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    log(f"[backfill] DONE ok={n_ok} no={n_no} err={n_err} -> {OUT} ({len(candidates)} candidates)")

if __name__ == "__main__":
    main()
