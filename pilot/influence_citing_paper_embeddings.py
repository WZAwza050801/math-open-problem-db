"""Stage 2a: embed unique citing-paper texts with bge-m3 (SiliconFlow).

Input:  citation_enrich_citing_papers.jsonl (68,916 edges, 56,013 unique citing papers)
Output: influence_citing_paper_embeddings.npy (float32 Nx1024) + influence_citing_paper_embeddings_ids.json
        (s2_paper_id list, same row order as the matrix)
Text:   "title. abstract" whitespace-normalized, first 1500 chars
        (matches canon_prototype/embed_all.py preprocessing so cosine
        similarity against card embeddings is comparable)
Checkpoint-resume: matrix + ids saved every 10 batches; rerun resumes.
Key:    .env SILICONFLOW_KEY (gitignored). Direct connection, no proxy
        (api.siliconflow.cn is domestic).
Usage:  python s2_citing_embed.py
"""
from __future__ import annotations

import json
import os
import time
import urllib.request

import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "citation_enrich_citing_papers.jsonl")
OUT_NPY = os.path.join(BASE, "influence_citing_paper_embeddings.npy")
OUT_IDS = os.path.join(BASE, "influence_citing_paper_embeddings_ids.json")
MODEL = "BAAI/bge-m3"
BATCH = 32
MAX_CHARS = 1500


def load_key():
    for line in open(os.path.join(BASE, ".env"), encoding="utf-8"):
        line = line.strip()
        if line.startswith("SILICONFLOW_KEY") and "=" in line:
            return line.split("=", 1)[1].strip()
    raise RuntimeError("SILICONFLOW_KEY not found in .env")


def collect_papers():
    """Dedupe citing papers by s2_paper_id; keep those with abstract."""
    papers = {}
    with open(SRC, encoding="utf-8") as f:  # iterate by \n; splitlines breaks on U+2028
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)
            for e in rec["edges"]:
                pid = e.get("s2_paper_id")
                if not pid or pid in papers:
                    continue
                abs_ = (e.get("abstract") or "").strip()
                title = (e.get("title") or "").strip()
                if not abs_:
                    continue  # title-only vectors too weak for filtering; count separately
                text = " ".join(f"{title}. {abs_}".split())[:MAX_CHARS]
                papers[pid] = text
    return papers


def main():
    key = load_key()
    papers = collect_papers()
    ids = list(papers.keys())
    texts = [papers[p] for p in ids]
    n = len(ids)
    print(f"[cite-embed] {n} unique citing papers with abstract, batch={BATCH}", flush=True)

    if os.path.exists(OUT_NPY) and os.path.exists(OUT_IDS):
        done_ids = json.load(open(OUT_IDS, encoding="utf-8"))
        mat = np.load(OUT_NPY)
        start = len(done_ids)
        if done_ids != ids[:start]:
            print("[cite-embed] id order changed, restarting matrix", flush=True)
            start, mat = 0, np.zeros((n, 1024), dtype=np.float32)
        else:
            full = np.zeros((n, 1024), dtype=np.float32)
            full[:start] = mat[:start]
            mat = full
            print(f"[cite-embed] resume at {start}/{n}", flush=True)
    else:
        start, mat = 0, np.zeros((n, 1024), dtype=np.float32)

    t0 = time.time()
    nb = 0
    for s in range(start, n, BATCH):
        chunk = texts[s:s + BATCH]
        body = {"model": MODEL, "input": chunk}
        req = urllib.request.Request(
            "https://api.siliconflow.cn/v1/embeddings",
            data=json.dumps(body).encode(), method="POST",
            headers={"Authorization": "Bearer " + key,
                     "Content-Type": "application/json"})
        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, timeout=180) as r:
                    d = json.load(r)
                break
            except Exception as e:
                wait = 10 * (attempt + 1)
                print(f"[cite-embed] batch@{s} {type(e).__name__}: {str(e)[:80]}"
                      f" -> retry in {wait}s", flush=True)
                time.sleep(wait)
        else:
            raise RuntimeError(f"batch@{s} failed after retries")
        for item in d["data"]:
            mat[s + item["index"]] = item["embedding"]
        nb += 1
        if nb % 10 == 0 or s + BATCH >= n:
            np.save(OUT_NPY, mat)
            json.dump(ids, open(OUT_IDS, "w", encoding="utf-8"))
        if nb % 50 == 0:
            done = s + BATCH - start
            rate = done / (time.time() - t0)
            print(f"[cite-embed] {s + BATCH}/{n}  ({rate:.0f}/s,"
                  f" ETA {(n - s - BATCH) / max(rate, 1e-9) / 60:.1f}m)", flush=True)

    np.save(OUT_NPY, mat)
    json.dump(ids, open(OUT_IDS, "w", encoding="utf-8"))
    print(f"[cite-embed] DONE {n} vectors ({os.path.getsize(OUT_NPY)/1e6:.0f} MB,"
          f" {time.time()-t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
