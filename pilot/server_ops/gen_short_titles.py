#!/usr/bin/env python3
"""给本库 7,471 张 canonical 卡生成外部风格的英文短标题。
输入: canon_embed_input.jsonl (uid, text)
输出: canon_short_titles.jsonl (uid, title) —— 断点续跑，按已存在 uid 跳过
用法: python3 gen_short_titles.py [--limit N] [--workers 6]
"""
import argparse, json, os, time, threading
from concurrent.futures import ThreadPoolExecutor
import urllib.request

BASE = "https://qianfan.baidubce.com/v2/tokenplan/personal/chat/completions"
MODEL = "deepseek-v4-pro"

SYS = """You are a mathematical editor preparing entries for a curated open-problem database (in the style of erdosproblems.com). Given a description of a mathematical problem extracted from a research paper, rewrite it as ONE self-contained declarative sentence (or question) stating the open problem itself.

Requirements:
- English only.
- Keep standard mathematical notation / LaTeX ($...$) exactly as needed.
- Remove ALL paper framing: no "this paper", "the authors", "we study", no history, no partial results, no citations, no attribution dates.
- Start with "Is it true that", "Does there exist", "Determine whether", "Prove or disprove", or a direct declarative statement of the conjecture.
- At most 80 words.
- Output ONLY the sentence, nothing else."""


def call_api(key, text, retries=3):
    body = json.dumps({"model": MODEL, "temperature": 0.2,
                       "messages": [{"role": "system", "content": SYS},
                                    {"role": "user", "content": text[:6000]}]}).encode()
    for attempt in range(retries):
        try:
            req = urllib.request.Request(BASE, data=body, method="POST",
                                         headers={"Authorization": f"Bearer {key}",
                                                  "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.loads(r.read())
            return d["choices"][0]["message"]["content"].strip()
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(5 * (attempt + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="canon_embed_input.jsonl")
    ap.add_argument("--out", default="canon_short_titles.jsonl")
    ap.add_argument("--keyfile", default=".qianfan_key")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()

    key = open(args.keyfile).read().strip()
    done = set()
    if os.path.exists(args.out):
        with open(args.out, encoding="utf-8") as f:
            for line in f:
                try:
                    done.add(json.loads(line)["uid"])
                except Exception:
                    pass
    tasks = []
    with open(args.input, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r["uid"] not in done:
                tasks.append(r)
    if args.limit:
        tasks = tasks[:args.limit]
    print(f"total {len(done)} done, {len(tasks)} to go, workers={args.workers}", flush=True)

    lock = threading.Lock()
    stats = {"ok": 0, "err": 0}
    fout = open(args.out, "a", encoding="utf-8")

    def work(r):
        try:
            title = call_api(key, r["text"])
            title = " ".join(title.split())
            with lock:
                fout.write(json.dumps({"uid": r["uid"], "title": title}, ensure_ascii=False) + "\n")
                fout.flush()
                stats["ok"] += 1
                if stats["ok"] % 50 == 0:
                    print(f"[{stats['ok']}] {r['uid']} ok | err={stats['err']}", flush=True)
        except Exception as e:
            with lock:
                stats["err"] += 1
                if stats["err"] <= 5:
                    print(f"ERR {r['uid']}: {e}", flush=True)

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        list(ex.map(work, tasks))
    fout.close()
    print(f"DONE ok={stats['ok']} err={stats['err']} elapsed={(time.time()-t0)/60:.1f}min", flush=True)


if __name__ == "__main__":
    main()
