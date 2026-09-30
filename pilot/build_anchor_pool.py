"""M6 anchor candidate pool builder (zero API).

Stratified selection of ~150 anchor candidates from canonical_problem, using
objective signals only -- AI later annotates tiers, humans audit extremes.

Strata:
  A  top        : multi-paper + famous conjecture alias or citation top 1%   (~30)
  B  upper-mid  : multi-paper or citation >= P95                              (~30)
  C  mid        : citation P75-P95, self-contained statement                  (~30)
  D  lower-mid  : citation P40-P70                                            (~30)
  E  noise/low  : extraction-noise labels or citation P10-P30                 (~30)

Diversified round-robin by MSC group inside each stratum.
Output: anchor_candidates.json + anchor_candidates.csv
"""
import csv
import json
import os
import sqlite3
from collections import defaultdict
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "db.sqlite3")
ALIAS_CSV = os.path.join(BASE, "named_problem_seed.csv")
OUT_JSON = os.path.join(BASE, "anchor_candidates.json")
OUT_CSV = os.path.join(BASE, "anchor_candidates.csv")
PER_STRATUM = 30

# famous anchors force-included by alias name (public consensus tiers exist)
FAMOUS = ("riemann", "hodge", "birch", "swinnerton", "yang-mills", "navier",
          "poincare", "p-vs-np", "p versus np", "goldbach", "twin-prime",
          "collatz", "erdos", "kadison", "hodge-conjecture")

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
con.execute("PRAGMA busy_timeout=60000")

# alias hotlist: arxiv_id -> set of conjecture aliases with n_papers>=2
alias_by_arxiv = defaultdict(set)
famous_alias = set()
try:
    with open(ALIAS_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            alias, kind = row["alias_norm"], row["kind"]
            n_papers = int(row["n_papers"])
            multi = n_papers >= 2
            if any(k in alias for k in FAMOUS) and n_papers >= 3:
                famous_alias.add(alias)
            if multi:
                for arxiv in row["sample_papers"].split(";"):
                    alias_by_arxiv[arxiv.strip()].add(alias)
except FileNotFoundError:
    print("[warn] alias csv missing; hotlist flags will be empty")

# per canonical: members + signals
cards = defaultdict(list)
for r in con.execute(
        "SELECT p.id, p.canonical_uid, p.arxiv_id, p.msc_primary, p.pub_year, "
        "p.label, p.self_contained, p.current_status "
        "FROM problems p WHERE p.canonical_uid IS NOT NULL"):
    cards[r["canonical_uid"]].append(r)

cites = {r["arxiv_id"]: (r["n_total"] or 0, r["n_2021_2026"] or 0)
         for r in con.execute("SELECT * FROM paper_cite_stats")}

cands = []
for uid, members in cards.items():
    papers = {m["arxiv_id"] for m in members}
    n_total = sum(cites.get(a, (0, 0))[0] for a in papers)
    n_recent = sum(cites.get(a, (0, 0))[1] for a in papers)
    mscs = [m["msc_primary"] for m in members if m["msc_primary"]]
    msc = max(set(mscs), key=mscs.count) if mscs else "?"
    years = [m["pub_year"] for m in members if m["pub_year"]]
    aliases = set()
    for a in papers:
        aliases |= alias_by_arxiv.get(a, set())
    famous = bool(aliases & famous_alias)
    # best statement: prefer multi-card clusters' longest self_contained
    stmt = max((m["self_contained"] or "" for m in members), key=len)
    labels = {m["label"] for m in members}
    cands.append({
        "canonical_uid": uid, "n_cards": len(members),
        "n_distinct_papers": len(papers), "n_total_citations": n_total,
        "n_recent_citations": n_recent, "msc": msc,
        "era": f"{min(years) if years else '?'}-{max(years) if years else '?'}",
        "aliases": sorted(aliases)[:5], "famous_alias": famous,
        "labels": sorted(labels), "statement_excerpt": stmt[:900],
    })

# citation percentiles (within all canonical)
totals = sorted(c["n_total_citations"] for c in cands)
def pct(p):
    i = int(len(totals) * p)
    return totals[min(i, len(totals) - 1)] if totals else 0
p10, p40, p70, p75, p90, p95, p99 = (pct(x) for x in (.10, .40, .70, .75, .90, .95, .99))

for c in cands:
    t, multi = c["n_total_citations"], c["n_distinct_papers"] >= 2
    noise = bool({"note", "remark", "exercise", "open_question_unclear"} & set(c["labels"]))
    if (multi and (c["famous_alias"] or t >= p99)) or t >= p99 and multi:
        c["stratum"] = "A"
    elif multi or t >= p95:
        c["stratum"] = "B"
    elif p75 <= t < p95 and len(c["statement_excerpt"]) > 300:
        c["stratum"] = "C"
    elif p40 <= t < p70:
        c["stratum"] = "D"
    elif noise or t <= p10:
        c["stratum"] = "E"
    else:
        c["stratum"] = None  # middle-of-road, not needed for anchors

# diversify by MSC within stratum, round-robin
pool = []
for s in "ABCDE":
    group = defaultdict(list)
    for c in cands:
        if c["stratum"] == s:
            group[c["msc"]].append(c)
    for g in group.values():
        g.sort(key=lambda c: (-c["n_total_citations"], -c["n_distinct_papers"]))
    picked, order = [], sorted(group, key=lambda k: -len(group[k]))
    idx = 0
    while len(picked) < PER_STRATUM and any(group[k] for k in order):
        for k in order:
            if group[k] and len(picked) < PER_STRATUM:
                picked.append(group[k].pop(0))
        idx += 1
        if idx > 200:
            break
    pool.extend(picked)

# force-include famous alias canonicals not already picked
famous_uids = {c["canonical_uid"] for c in pool}
for c in cands:
    if (c["famous_alias"] and c["n_distinct_papers"] >= 2
            and c["canonical_uid"] not in famous_uids):
        c["stratum"] = (c["stratum"] or "A") + "+famous"
        pool.append(c)
        famous_uids.add(c["canonical_uid"])

now = datetime.now().isoformat(timespec="seconds")
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump({"generated_at": now, "percentiles": {
        "p10": p10, "p40": p40, "p70": p70, "p75": p75,
        "p90": p90, "p95": p95, "p99": p99},
        "candidates": pool}, f, ensure_ascii=False, indent=2)
with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["canonical_uid", "stratum", "n_cards",
        "n_distinct_papers", "n_total_citations", "n_recent_citations",
        "msc", "era", "famous_alias", "aliases", "labels", "statement_excerpt"])
    w.writeheader()
    w.writerows(pool)

from collections import Counter
print(json.dumps({
    "pool_size": len(pool),
    "by_stratum": dict(Counter(c["stratum"] for c in pool)),
    "by_msc_top10": dict(Counter(c["msc"] for c in pool).most_common(10)),
    "famous_included": sum(1 for c in pool if c["famous_alias"]),
}, ensure_ascii=False))
