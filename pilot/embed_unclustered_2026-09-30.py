"""embed_unclustered_2026-09-30.py — 给 6,424 张悬空卡补 BGE-M3 向量（T09）

输入：unclustered_cards_2026-09-30.jsonl（服务器导出的悬空本源卡 id+self_contained）
输出：unclustered_embeddings_2026-09-30.npy / _ids.json（与 canon_prototype 的
      7,471 条向量同一模型同一口径：BAAI/bge-m3、self_contained 前 1500 字符、批 32）

方式：硅基流动 API（与原 7,471 条完全一致，保证向量空间可比）。
断点续跑：每 10 批落盘一次；重启后按已完成 id 续。

用法：python embed_unclustered_2026-09-30.py
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
IN_JSONL = os.path.join(BASE, "unclustered_cards_2026-09-30.jsonl")
OUT_NPY = os.path.join(BASE, "unclustered_embeddings_2026-09-30.npy")
OUT_IDS = os.path.join(BASE, "unclustered_embeddings_2026-09-30_ids.json")
ENV = os.path.join(BASE, ".env")

API = "https://api.siliconflow.cn/v1/embeddings"
MODEL = "BAAI/bge-m3"
BATCH = 32
MAX_CHARS = 1500
DIM = 1024
CHECKPOINT_EVERY = 10


def load_key():
    for line in open(ENV, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            if k.strip() == "SILICONFLOW_KEY":
                return v.strip()
    raise SystemExit(".env 里没有 SILICONFLOW_KEY")


def embed_batch(key, texts, retries=5):
    body = json.dumps({"model": MODEL, "input": texts}).encode()
    for attempt in range(retries):
        req = urllib.request.Request(
            API, data=body, method="POST",
            headers={"Authorization": f"Bearer {key}",
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.loads(r.read())
            # 按 index 对齐返回顺序
            vecs = sorted(data["data"], key=lambda d: d["index"])
            return np.array([v["embedding"] for v in vecs], dtype=np.float32)
        except Exception as e:
            wait = min(60, 2 ** attempt * 3)
            print(f"[embed] 批失败({e})，{wait}s 后重试 {attempt+1}/{retries}", flush=True)
            time.sleep(wait)
    raise RuntimeError("单批重试耗尽")


def main():
    key = load_key()
    rows = []
    for line in open(IN_JSONL, encoding="utf-8"):
        if line.strip():
            o = json.loads(line)
            rows.append((o["card_id"], (" ".join((o["text"] or "").split()))[:MAX_CHARS]))
    n = len(rows)
    print(f"[embed] {n} 张悬空卡，维度 {DIM}，批大小 {BATCH}", flush=True)

    done_ids, mat = [], np.zeros((n, DIM), dtype=np.float32)
    if os.path.exists(OUT_IDS) and os.path.exists(OUT_NPY):
        done_ids = json.load(open(OUT_IDS, encoding="utf-8"))
        if done_ids == [r[0] for r in rows[:len(done_ids)]]:
            mat = np.load(OUT_NPY)
            print(f"[embed] 续跑：{len(done_ids)}/{n}", flush=True)
        else:
            print("[embed] id 顺序变化，重新开始矩阵", flush=True)
            done_ids = []

    start = len(done_ids)
    n_batches = (n - start + BATCH - 1) // BATCH
    for bi in range(n_batches):
        lo = start + bi * BATCH
        hi = min(lo + BATCH, n)
        mat[lo:hi] = embed_batch(key, [t for _, t in rows[lo:hi]])
        done_now = hi
        if (bi + 1) % CHECKPOINT_EVERY == 0 or hi == n:
            np.save(OUT_NPY, mat)
            json.dump([r[0] for r in rows[:done_now]], open(OUT_IDS, "w"))
            print(f"[embed] 进度 {done_now}/{n}", flush=True)

    print(f"[embed] 完成：{n}/{n}，输出 {OUT_NPY}", flush=True)


if __name__ == "__main__":
    main()
