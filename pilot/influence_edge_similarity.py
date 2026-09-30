"""Stage 2b: per-edge max cosine similarity (citing paper x source-paper cards).

For each S2 citation edge (our_doi -> citing paper), compute the max cosine
similarity between the citing paper's embedding and ALL cards extracted from
our_doi's paper. This is the coarse filter for the LLM adjudication stage:
high sim = citing paper likely engages with a specific conjecture statement.

Inputs:
  canon_prototype/embeddings.npy + embeddings_ids.json   (7,471 card vectors)
  canon_prototype/canon_db.sqlite3                       (card id -> arxiv_id)
  pilot/candidates.json                                  (crossref_doi <-> arxiv_id)
  pilot/influence_citing_paper_embeddings.npy + influence_citing_paper_embeddings_ids.json
  pilot/citation_enrich_citing_papers.jsonl                           (edges)
Output:
  pilot/influence_edge_similarity.jsonl  one line per edge:
    {our_doi, s2_paper_id, max_sim, best_card_id, has_contexts,
     is_influential, intents}
  prints distribution stats + suggested thresholds.
Usage: python influence_edge_similarity.py
"""
from __future__ import annotations

import json
import os
import sqlite3
from collections import defaultdict

import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(BASE, "..", "canon_prototype")


def norm_rows(m: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(m, axis=1, keepdims=True)
    n[n == 0] = 1.0
    return m / n


def main():
    # card vectors + card -> arxiv
    card_ids = json.load(open(os.path.join(CANON, "embeddings_ids.json"), encoding="utf-8"))
    card_mat = norm_rows(np.load(os.path.join(CANON, "embeddings.npy")).astype(np.float32))
    con = sqlite3.connect(os.path.join(CANON, "canon_db.sqlite3"))
    card_arxiv = {r[0]: r[1] for r in con.execute("SELECT id, arxiv_id FROM problems")}
    arxiv2rows = defaultdict(list)
    for i, cid in enumerate(card_ids):
        arxiv2rows[card_arxiv.get(cid)].append(i)

    # doi -> arxiv
    cands = json.load(open(os.path.join(BASE, "candidates.json"), encoding="utf-8"))
    doi2arxiv = {c["crossref_doi"]: c.get("arxiv_id") for c in cands}

    # citing vectors
    cit_ids = json.load(open(os.path.join(BASE, "influence_citing_paper_embeddings_ids.json"), encoding="utf-8"))
    cit_mat = norm_rows(np.load(os.path.join(BASE, "influence_citing_paper_embeddings.npy")).astype(np.float32))
    cit_row = {pid: i for i, pid in enumerate(cit_ids)}

    out_path = os.path.join(BASE, "influence_edge_similarity.jsonl")
    n_edges = n_scored = n_no_emb = n_no_cards = 0
    sims = []
    with open(os.path.join(BASE, "citation_enrich_citing_papers.jsonl"), encoding="utf-8") as f, \
         open(out_path, "w", encoding="utf-8") as out:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)
            our_doi = rec["our_doi"]
            rows = arxiv2rows.get(doi2arxiv.get(our_doi), [])
            for e in rec["edges"]:
                n_edges += 1
                pid = e.get("s2_paper_id")
                base = {"our_doi": our_doi, "s2_paper_id": pid,
                        "has_contexts": bool(e.get("contexts")),
                        "is_influential": e.get("is_influential", False),
                        "intents": e.get("intents") or []}
                ci = cit_row.get(pid)
                if ci is None:
                    n_no_emb += 1
                    out.write(json.dumps({**base, "max_sim": None, "best_card_id": None}) + "\n")
                    continue
                if not rows:
                    n_no_cards += 1
                    out.write(json.dumps({**base, "max_sim": None, "best_card_id": None}) + "\n")
                    continue
                s = card_mat[rows] @ cit_mat[ci]
                j = int(np.argmax(s))
                sims.append(float(s[j]))
                n_scored += 1
                out.write(json.dumps({**base, "max_sim": round(float(s[j]), 4),
                                      "best_card_id": card_ids[rows[j]]}) + "\n")

    sims = np.array(sims)
    print(f"edges={n_edges} scored={n_scored} no_citing_emb={n_no_emb} no_cards={n_no_cards}")
    print("max_sim distribution:")
    for q in (50, 60, 70, 80, 90, 95, 99):
        print(f"  p{q}: {np.percentile(sims, q):.4f}")
    for t in (0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70):
        print(f"  >= {t:.2f}: {(sims >= t).sum():>6}  ({100 * (sims >= t).mean():.1f}%)")


if __name__ == "__main__":
    main()
