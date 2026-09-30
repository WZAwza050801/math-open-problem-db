"""Coverage report: S2 citing enrichment vs COCI baseline.

Compares citations.jsonl (COCI edges) with citation_enrich_citing_papers.jsonl (S2 edges):
  - per-source-doi status counts (ok / s2_not_found / error)
  - edge totals, unique citing papers (by DOI / s2_paper_id)
  - coverage: with_contexts / with_abstract / with_intents / is_influential
  - overlap: COCI citing DOIs found in S2 edges, S2-only edges (S2 bonus)
Usage: python citation_enrich_coverage_report.py
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent
COCI = BASE / "citations.jsonl"
S2 = BASE / "citation_enrich_citing_papers.jsonl"

DOI_RE = re.compile(r"doi:(\S+)")


def main():
    coci_edges = {}          # our_doi -> set of citing dois
    coci_citing_all = set()
    for line in COCI.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        ds = set()
        for c in rec.get("citations", []):
            m = DOI_RE.search(c.get("citing", ""))
            if m:
                d = m.group(1).lower().rstrip(" .")
                ds.add(d)
                coci_citing_all.add(d)
        coci_edges[rec["doi"]] = ds

    status = Counter()
    s2_edges = 0
    s2_citing_all = set()
    n_ctx = n_abs = n_int = n_infl = 0
    per_doi = []
    with S2.open(encoding="utf-8") as fh:  # iterate by \n only: splitlines() breaks on \u2028 etc. inside abstracts
        s2_lines = [l for l in fh if l.strip()]
    for line in s2_lines:
        rec = json.loads(line)
        status[rec["s2_status"]] += 1
        s2_edges += rec["n_edges"]
        with_doi = set()
        for e in rec["edges"]:
            key = (e.get("citing_doi") or e.get("s2_paper_id") or "").lower()
            if key:
                s2_citing_all.add(key)
                if e.get("citing_doi"):
                    with_doi.add(e["citing_doi"].lower())
            if e.get("contexts"):
                n_ctx += 1
            if e.get("abstract"):
                n_abs += 1
            if e.get("intents"):
                n_int += 1
            if e.get("is_influential"):
                n_infl += 1
        per_doi.append((rec["our_doi"], rec["n_edges"], len(coci_edges.get(rec["our_doi"], set()))))

    overlap = {d for d in coci_citing_all if d in s2_citing_all}
    print("=== S2 citing enrichment coverage ===")
    print(f"source DOIs processed: {sum(status.values())}  status: {dict(status)}")
    print(f"S2 edges: {s2_edges}  (COCI baseline: 39,426)")
    print(f"unique citing papers S2: {len(s2_citing_all)}  COCI: {len(coci_citing_all)}")
    print(f"COCI citing DOIs recovered in S2: {len(overlap)}/{len(coci_citing_all)}"
          f" ({100*len(overlap)/max(1,len(coci_citing_all)):.1f}%)")
    print(f"S2-only citing papers (bonus beyond COCI): {len(s2_citing_all - coci_citing_all)}")
    print(f"edge field coverage: contexts {n_ctx} ({100*n_ctx/max(1,s2_edges):.1f}%)"
          f"  abstract {n_abs} ({100*n_abs/max(1,s2_edges):.1f}%)"
          f"  intents {n_int} ({100*n_int/max(1,s2_edges):.1f}%)"
          f"  influential {n_infl} ({100*n_infl/max(1,s2_edges):.1f}%)")
    zero = [d for d, n, _ in per_doi if n == 0]
    print(f"source DOIs with zero S2 edges: {len(zero)}")


if __name__ == "__main__":
    main()
