#!/usr/bin/env python3
"""在 node01 上给外部候选卡算 bge-m3 向量。
输入: embed_input.jsonl (uid, src, text)
输出: embed_vectors.npz (uids, srcs, vecs float16) + 进度日志
用法: python3 embed_external.py --input embed_input.jsonl --model ./bge-m3 --out embed_vectors.npz
"""
import argparse, json, time
import numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--batch", type=int, default=64)
    args = ap.parse_args()

    from sentence_transformers import SentenceTransformer
    import torch

    model = SentenceTransformer(args.model, device="cuda" if torch.cuda.is_available() else "cpu")
    model.max_seq_length = 512   # bge-m3 支持长文本，512 token 覆盖绝大多数陈述

    uids, srcs, texts = [], [], []
    with open(args.input, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            uids.append(r["uid"]); srcs.append(r.get("src") or ""); texts.append(r["text"])
    print(f"loaded {len(uids)} texts, device={model.device}", flush=True)

    t0 = time.time()
    vecs = model.encode(texts, batch_size=args.batch, show_progress_bar=True,
                        normalize_embeddings=True, convert_to_numpy=True)
    dt = time.time() - t0
    print(f"encoded in {dt:.0f}s -> {vecs.shape}, dtype={vecs.dtype}", flush=True)

    np.savez_compressed(args.out, uids=np.array(uids), srcs=np.array(srcs), vecs=vecs.astype(np.float16))
    print("saved", args.out, flush=True)

    # 自检：三条已知同题对的相似度
    probe = {
        "erdos5": [i for i, u in enumerate(uids) if "erdosproblems" in (srcs[i] or "") and u.endswith("/5")],
    }
    idx = probe["erdos5"]
    if len(idx) >= 1:
        i = idx[0]
        sims = vecs[:200] @ vecs[i]
        top = np.argsort(-sims)[:3]
        print("sanity probe erdos#5 top sims:", [round(float(sims[j]), 3) for j in top], flush=True)

if __name__ == "__main__":
    main()
