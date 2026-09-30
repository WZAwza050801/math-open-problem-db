"""Build calibration sample (200 pairs) for influence adjudication.

Strata (from rule-B universe):
  sim>=0.70: 40 | 0.65-0.70: 40 | 0.60-0.65: 60 | 0.55-0.60 & ctx: 40 | no_emb & ctx: 20
Output: influence_calibration_input.jsonl
  {pair_id, our_doi, s2_paper_id, card_id, card_status, card_statement,
   citing_title, citing_abstract(<=600 chars), contexts(<=3, each<=400),
   max_sim, intents, is_influential, stratum}
"""
import json
import random
import sqlite3

random.seed(20260930)

con = sqlite3.connect("../canon_prototype/canon_db.sqlite3")
cards = {r[0]: (r[1] or "", r[2] or "")
         for r in con.execute("SELECT id, self_contained, paper_time_status FROM problems")}

meta = {}
for line in open("citation_enrich_citing_papers.jsonl", encoding="utf-8"):
    if not line.strip():
        continue
    rec = json.loads(line)
    for e in rec["edges"]:
        meta[(rec["our_doi"], e.get("s2_paper_id"))] = e

pools = {k: [] for k in ("s70", "s65", "s60", "s55ctx", "noemb")}
for line in open("influence_edge_similarity.jsonl", encoding="utf-8"):
    if not line.strip():
        continue
    r = json.loads(line)
    s = r["max_sim"]
    if s is not None and s >= 0.70:
        pools["s70"].append(r)
    elif s is not None and s >= 0.65:
        pools["s65"].append(r)
    elif s is not None and s >= 0.60:
        pools["s60"].append(r)
    elif s is not None and s >= 0.55 and r["has_contexts"]:
        pools["s55ctx"].append(r)
    elif s is None and r["has_contexts"]:
        pools["noemb"].append(r)

quota = {"s70": 40, "s65": 40, "s60": 60, "s55ctx": 40, "noemb": 20}
out = open("influence_calibration_input.jsonl", "w", encoding="utf-8")
n = 0
for stratum, k in quota.items():
    pool = pools[stratum]
    random.shuffle(pool)
    picked = 0
    for r in pool:
        if picked >= k:
            break
        e = meta.get((r["our_doi"], r["s2_paper_id"]))
        if not e:
            continue
        stmt, status = cards.get(r["best_card_id"], ("", ""))
        if not stmt:
            continue
        n += 1
        picked += 1
        out.write(json.dumps({
            "pair_id": f"cal-{n:04d}", "stratum": stratum,
            "our_doi": r["our_doi"], "s2_paper_id": r["s2_paper_id"],
            "card_id": r["best_card_id"], "card_status": status,
            "card_statement": stmt[:1200],
            "citing_title": (e.get("title") or "")[:300],
            "citing_abstract": (e.get("abstract") or "")[:600],
            "contexts": [c[:400] for c in (e.get("contexts") or [])[:3]],
            "max_sim": r["max_sim"], "intents": r["intents"],
            "is_influential": r["is_influential"],
        }, ensure_ascii=False) + "\n")
    print(f"{stratum}: pool={len(pool)} picked={picked}")
out.close()
print("total", n)
