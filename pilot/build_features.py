"""P3: objective feature snapshot with MSC x era standardization (SOP M5). Zero API.
Raw values AND percentile-normalized values stored side by side.
Usage: python3 build_features.py
"""
import json, math, os, sqlite3
from collections import Counter, defaultdict
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "db.sqlite3")
CURRENT_YEAR = 2026

def hashlib_sha(t):
    import hashlib
    return hashlib.sha256(t.encode()).hexdigest()[:16]

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
con.execute("PRAGMA busy_timeout=60000")
con.execute("""CREATE TABLE IF NOT EXISTS objective_feature_snapshots (
    canonical_uid TEXT PRIMARY KEY, n_cards INTEGER, n_distinct_papers INTEGER,
    n_total_citations INTEGER, n_recent_citations INTEGER, vitality REAL,
    age_years INTEGER, era_bucket TEXT, msc_top TEXT, in_alias_hotlist INTEGER,
    n_total_pctl REAL, n_recent_pctl REAL, vitality_pctl REAL,
    n_cards_pctl REAL, n_papers_pctl REAL, missing_flags TEXT,
    feature_hash TEXT, created_at TEXT)""")

# canonical -> members
clusters = defaultdict(list)
for r in con.execute("SELECT p.id, p.canonical_uid, p.arxiv_id, p.msc_primary, p.pub_year "
                     "FROM problems p WHERE p.canonical_uid IS NOT NULL"):
    clusters[r["canonical_uid"]].append(r)
cites = {r["arxiv_id"]: (r["n_total"] or 0, r["n_2021_2026"] or 0, r["latest_citing"])
         for r in con.execute("SELECT * FROM paper_cite_stats")}

# alias hotlist (multi-paper aliases) via named_problem_seed.csv
hot_arxiv = set()
p = os.path.join(BASE, "named_problem_seed.csv")
if os.path.exists(p):
    import csv
    for row in csv.DictReader(open(p, encoding="utf-8")):
        if int(row["n_papers"]) >= 2:
            hot_arxiv.update(a.strip() for a in row["sample_papers"].split(";"))

def era_bucket(y):
    if y is None: return "?"
    for lo in (2000, 2005, 2010, 2015):
        if lo <= y <= lo + 4: return f"{lo}-{lo+4}"
    return "2020-2025" if y >= 2020 else "pre-2000"

def vitality(nt, nr, latest):
    v = math.log1p(nt) + 2 * math.log1p(nr)
    if latest and str(latest)[:4] == str(CURRENT_YEAR):
        v += 1.0
    return round(v, 3)

raw = {}
for uid, members in clusters.items():
    papers = {m["arxiv_id"] for m in members}
    nt = sum(cites.get(a, (0, 0, None))[0] for a in papers)
    nr = sum(cites.get(a, (0, 0, None))[1] for a in papers)
    vit = sum(vitality(*cites.get(a, (0, 0, None))) for a in papers)
    years = [m["pub_year"] for m in members if m["pub_year"]]
    mscs = [m["msc_primary"] for m in members if m["msc_primary"]]
    msc = max(set(mscs), key=mscs.count) if mscs else None
    med_year = sorted(years)[len(years) // 2] if years else None
    age = CURRENT_YEAR - med_year if med_year else None
    hot = int(bool(papers & hot_arxiv))
    raw[uid] = {"n_cards": len(members), "n_distinct_papers": len(papers),
                "n_total_citations": nt, "n_recent_citations": nr, "vitality": vit,
                "age_years": age, "era_bucket": era_bucket(med_year),
                "msc_top": (msc[:2] if msc else "?"), "in_alias_hotlist": hot}

def percentile_of(value, pool):
    below = sum(1 for x in pool if x <= value)
    return round(below / len(pool), 4) if pool else None

# group keys: msc_top x era_bucket, fallback msc_top, fallback global
groups = defaultdict(list)
for uid, f in raw.items():
    groups[(f["msc_top"], f["era_bucket"])].append(uid)
msc_groups = defaultdict(list)
for uid, f in raw.items():
    msc_groups[f["msc_top"]].append(uid)
all_uids = list(raw)

FIELDS = ["n_total_citations", "n_recent_citations", "vitality", "n_cards", "n_distinct_papers"]
done = 0
for uid, f in raw.items():
    out = {}
    for fld in FIELDS:
        pool = [(k, raw[k][fld]) for g in (groups[(f["msc_top"], f["era_bucket"])],
                msc_groups[f["msc_top"]], all_uids) if len(g) >= 20 for k in g]
        if not pool:
            pool = [(k, raw[k][fld]) for k in all_uids]
        out[fld + "_pctl"] = percentile_of(f[fld], [v for _, v in pool])
    missing = json.dumps([k for k in ("msc_top", "age_years") if f.get(k) in (None, "?")])
    fh = hashlib_sha(json.dumps({**f, **out}, sort_keys=True))
    con.execute("INSERT OR REPLACE INTO objective_feature_snapshots VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (uid, f["n_cards"], f["n_distinct_papers"], f["n_total_citations"],
                 f["n_recent_citations"], f["vitality"], f["age_years"], f["era_bucket"],
                 f["msc_top"], f["in_alias_hotlist"], out["n_total_citations_pctl"],
                 out["n_recent_citations_pctl"], out["vitality_pctl"], out["n_cards_pctl"],
                 out["n_distinct_papers_pctl"], missing, fh,
                 datetime.now().isoformat(timespec="seconds")))
    done += 1
    if done % 1000 == 0:
        con.commit()
        print(f"  {done}/{len(raw)}", flush=True)
con.commit()
print("integrity:", con.execute("PRAGMA integrity_check").fetchone()[0])
print("by era:", con.execute("SELECT era_bucket, COUNT(*) FROM objective_feature_snapshots GROUP BY era_bucket").fetchall())
print("hotlist:", con.execute("SELECT in_alias_hotlist, COUNT(*) FROM objective_feature_snapshots GROUP BY in_alias_hotlist").fetchall())
con.close()
