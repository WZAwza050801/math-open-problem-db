"""freeze_identity_candidates_2026-09-30.py — 冻结"可能是同一个命题"的候选对（T10）

输入：
  unclustered_embeddings_2026-09-30.npy/_ids.json   悬空卡 6,424 条向量
  canon_prototype/embeddings.npy/_ids.json          已挂卡 7,471 条向量（覆盖全部命题代表卡）
  canonical_rep_map.json                            命题 -> 代表卡
输出：
  identity_candidates_2026-09-30.jsonl   每行 {a_id, b_id, kind, cos}
    kind: new_vs_existing（悬空卡 × 命题代表卡） / new_vs_new（悬空卡 × 悬空卡）
  统计打到 stdout：对数、覆盖多少张悬空卡、最高/最低相似度分布
规则（计划书 §3.4）：每张悬空卡两类近邻各取最近 20；余弦 ≥ 0.80 冻结；对去重。

用法：python freeze_identity_candidates_2026-09-30.py
"""
import json
import os
from collections import defaultdict

import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
NEW_NPY = os.path.join(BASE, "unclustered_embeddings_2026-09-30.npy")
NEW_IDS = os.path.join(BASE, "unclustered_embeddings_2026-09-30_ids.json")
OLD_NPY = os.path.join(BASE, "..", "canon_prototype", "embeddings.npy")
OLD_IDS = os.path.join(BASE, "..", "canon_prototype", "embeddings_ids.json")
REPMAP = os.path.join(BASE, "canonical_rep_map.json")
OUT = os.path.join(BASE, "identity_candidates_2026-09-30.jsonl")

TOP_K = 20
THRESH = 0.80


def topk_cos(mat_q, mat_ref, k):
    """返回 (idx, cos) 的 k 近邻，mat 已归一化。"""
    sim = mat_q @ mat_ref.T
    idx = np.argpartition(-sim, kth=min(k, sim.shape[1] - 1), axis=1)[:, :k]
    vals = np.take_along_axis(sim, idx, axis=1)
    order = np.argsort(-vals, axis=1)
    return np.take_along_axis(idx, order, 1), np.take_along_axis(vals, order, 1)


def main():
    new_ids = json.load(open(NEW_IDS, encoding="utf-8"))
    new_mat = np.load(NEW_NPY)
    old_ids = json.load(open(OLD_IDS, encoding="utf-8"))
    old_mat = np.load(OLD_NPY)
    reps = json.load(open(REPMAP, encoding="utf-8"))

    old_pos = {cid: i for i, cid in enumerate(old_ids)}
    rep_ids, rep_uid = [], []
    for uid, cid in reps.items():
        if cid in old_pos:
            rep_ids.append(cid)
            rep_uid.append(uid)
    rep_mat = old_mat[[old_pos[c] for c in rep_ids]]
    print(f"悬空卡 {len(new_ids)}，命题代表卡 {len(rep_ids)}/{len(reps)}")

    pairs = {}

    def add(a, b, kind, cos):
        key = (a, b) if a < b else (b, a)
        if key not in pairs or cos > pairs[key][1]:
            pairs[key] = (kind, float(cos))

    # 悬空 × 命题代表
    idx, vals = topk_cos(new_mat, rep_mat, TOP_K)
    covered_existing = set()
    for qi in range(len(new_ids)):
        for j, c in zip(idx[qi], vals[qi]):
            if c >= THRESH:
                add(new_ids[qi], rep_ids[j], "new_vs_existing", c)
                covered_existing.add(new_ids[qi])

    # 悬空 × 悬空（排除自身）
    idx2, vals2 = topk_cos(new_mat, new_mat, TOP_K + 1)
    covered_new = set()
    for qi in range(len(new_ids)):
        for j, c in zip(idx2[qi], vals2[qi]):
            if j == qi:
                continue
            if c >= THRESH:
                add(new_ids[qi], new_ids[j], "new_vs_new", c)
                covered_new.add(new_ids[qi])

    with open(OUT, "w", encoding="utf-8") as f:
        for (a, b), (kind, cos) in sorted(pairs.items(), key=lambda kv: -kv[1][1]):
            f.write(json.dumps({"a_id": a, "b_id": b, "kind": kind,
                                "cos": round(cos, 4)}, ensure_ascii=False) + "\n")

    ks = np.array([v[1] for v in pairs.values()])
    print(f"候选对冻结：{len(pairs)} 对")
    print(f"  其中 悬空×已有命题：{sum(1 for v in pairs.values() if v[0]=='new_vs_existing')}")
    print(f"  其中 悬空×悬空：{sum(1 for v in pairs.values() if v[0]=='new_vs_new')}")
    print(f"  至少有一个 ≥0.80 近邻的悬空卡：{len(covered_existing | covered_new)}/{len(new_ids)}")
    print(f"  近邻全部 <0.80（将各自新建命题）：{len(new_ids) - len(covered_existing | covered_new)}")
    if len(ks):
        for lo, hi in ((0.80, 0.85), (0.85, 0.90), (0.90, 0.95), (0.95, 1.01)):
            print(f"  余弦 {lo:.2f}–{hi:.2f}：{int(((ks >= lo) & (ks < hi)).sum())} 对")


if __name__ == "__main__":
    main()
