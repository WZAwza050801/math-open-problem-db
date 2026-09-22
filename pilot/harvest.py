"""Stage 1 (rewritten): authoritative harvest.

Old approach (broken, see pilot log): search arXiv `jr:` with loose boolean queries
and validate with a regex allowlist. Two independent failures:
  * precision  ~39%  (9 of 23 accepted papers were actually in the target journal;
                      arXiv jr: matching pulled in "Annals of Mathematics and Physics",
                      "Acta Mathematica Hungarica", "...An Electronic Journal of the AMS", ...)
  * coverage   ~0% of the intended sample: sorting the loose query by submittedDate
                returned the most recent (mostly wrong) journals, so genuine
                Annals/Acta papers never entered the 24-slot candidate window.

New approach: Crossref is the ground truth for "which papers exist in journal J".
  1. enumerate each journal's full 2000-2025 TOC from Crossref by ISSN (complete, exact);
  2. query arXiv with *quoted,* `jr:` phrases so the candidate pool is mostly genuine;
  3. join arXiv <-> Crossref on DOI, falling back to near-exact normalized title.
A candidate is accepted only when Crossref confirms the journal and the publication year.

Outputs: crossref_toc.json (authoritative denominator), candidates.json (matched, ready
to fetch), and a printed coverage report.
"""
from __future__ import annotations

import difflib
import json
import os
import random
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

BASE = Path(__file__).resolve().parent
TOC_CACHE = BASE / "crossref_toc.json"
CANDIDATES = BASE / "candidates.json"

MAILTO = "open-problem-db-pilot@example.com"
CROSSREF_UA = {"User-Agent": f"open-problem-db-pilot/0.1 (mailto:{MAILTO})"}
ARXIV_UA = {"User-Agent": "open-problem-db-pilot/0.1 (research; contact: local)"}

ARXIV_API = "https://export.arxiv.org/api/query"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

YEAR_FROM, YEAR_TO = 2000, 2025

# --- the five target journals, keyed by the ISSN Crossref indexes them under -------------
JOURNALS = {
    "annals": {"name": "Annals of Mathematics", "issn": "0003-486X"},
    "acta": {"name": "Acta Mathematica", "issn": "0001-5962"},
    "inventiones": {"name": "Inventiones Mathematicae", "issn": "0020-9910"},
    "jams": {"name": "Journal of the American Mathematical Society", "issn": "0894-0347"},
    "ihes": {"name": "Publications Mathematiques de l'IHES", "issn": "0073-8301"},
}

# --- precise arXiv queries: quoted phrases only -----------------------------------------
# Verified against the API: these return near-100% genuine journal_refs, whereas
# `jr:Annals AND jr:Mathematics` returns ~44% junk.
ARXIV_QUERIES = {
    "annals": ['jr:"Ann. of Math."', 'jr:"Annals of Mathematics"'],
    "acta": ['jr:"Acta Math."', 'jr:"Acta Mathematica"'],
    "inventiones": ['jr:"Invent. Math."', 'jr:"Inventiones Mathematicae"'],
    "jams": ['jr:"J. Amer. Math. Soc."', 'jr:"Journal of the American Mathematical Society"'],
    "ihes": ['jr:"Publ. Math. Inst. Hautes"', 'jr:Hautes'],
}

# Corpus size. The defaults are PILOT sized (8 per journal) so a casual run stays
# cheap. For a full-corpus run set the environment variables rather than editing
# this file, so the same source serves both modes:
#
#   PER_JOURNAL=100000 CANDIDATES_PER_QUERY=2000 python harvest.py
#
# CANDIDATES_PER_QUERY is the arXiv pool fetched per quoted-phrase query, and it
# is what bounds recall: only papers present in that pool can be joined to the
# Crossref list. arXiv serves at most 2000 per request, so 2000 is the ceiling
# for a single query.
PER_JOURNAL = int(os.environ.get("PER_JOURNAL", "8"))
CANDIDATES_PER_QUERY = int(os.environ.get("CANDIDATES_PER_QUERY", "200"))


# ------------------------------------------------------------------ helpers
def http_json(url, timeout=60, retries=4):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=CROSSREF_UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            wait = 5 * (i + 1) if e.code == 429 else 2 * (i + 1)
            print(f"    [{last}] retry in {wait}s")
            time.sleep(wait)
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"crossref failed: {last}")


def norm_title(t: str) -> str:
    """Aggressively normalize a title so Crossref and arXiv spellings collide."""
    t = re.sub(r"<[^>]+>", " ", t or "")            # MathML / HTML tags
    t = t.replace("&amp;", "&").replace("--", "-")
    t = re.sub(r"\$[^$]*\$", " MATH ", t)           # inline math -> placeholder token
    t = re.sub(r"\\[a-zA-Z]+", " MATH ", t)          # latex commands
    t = t.lower()
    t = re.sub(r"[^a-z0-9]+", " ", t)
    toks = [w for w in t.split() if w not in ("math", "a", "the", "of", "on", "and", "for", "to", "in")]
    return " ".join(toks)


def year_of(item):
    for k in ("published-print", "published-online", "published", "issued"):
        dp = ((item.get(k) or {}).get("date-parts") or [[None]])[0]
        if dp and dp[0]:
            return int(dp[0])
    return None


# ------------------------------------------------------------------ stage 1a: Crossref TOC
def fetch_toc(jkey, issn, rows=500):
    print(f"[crossref] {jkey} ({issn}) enumerating {YEAR_FROM}-{YEAR_TO} ...")
    items, cursor, seen = [], "*", 0
    while True:
        url = (f"https://api.crossref.org/journals/{issn}/works?"
               + urllib.parse.urlencode({
                   "filter": f"from-pub-date:{YEAR_FROM}-01-01,until-pub-date:{YEAR_TO}-12-31,type:journal-article",
                   "rows": rows, "cursor": cursor, "mailto": MAILTO,
                   "select": "DOI,title,container-title,published,published-print,published-online,volume,page,type",
               }))
        d = http_json(url)
        msg = d["message"]
        batch = msg.get("items", [])
        if not batch:
            break
        items.extend(batch)
        seen += len(batch)
        cursor = msg.get("next-cursor")
        print(f"    ... {seen} (total-results={msg.get('total-results')})")
        if not cursor or len(batch) < rows:
            break
        time.sleep(2)
    out = []
    for it in items:
        y = year_of(it)
        if y is None or not (YEAR_FROM <= y <= YEAR_TO):
            continue
        out.append({
            "doi": (it.get("DOI") or "").lower().strip(),
            "title": (it.get("title") or [""])[0],
            "journal": (it.get("container-title") or [""])[0],
            "year": y,
            "volume": it.get("volume"),
            "page": it.get("page"),
        })
    print(f"    -> kept {len(out)}")
    return out


def load_toc(force=False):
    if TOC_CACHE.exists() and not force:
        return json.loads(TOC_CACHE.read_text(encoding="utf-8"))
    toc = {}
    for jkey, cfg in JOURNALS.items():
        toc[jkey] = fetch_toc(jkey, cfg["issn"])
    TOC_CACHE.write_text(json.dumps(toc, ensure_ascii=False, indent=1), encoding="utf-8")
    return toc


# ------------------------------------------------------------------ stage 1b: arXiv pool
def arxiv_query(q, max_results=CANDIDATES_PER_QUERY, sort_by="relevance"):
    url = ARXIV_API + "?" + urllib.parse.urlencode({
        "search_query": q, "sortBy": sort_by, "sortOrder": "descending",
        "start": 0, "max_results": max_results,
    })
    req = urllib.request.Request(url, headers=ARXIV_UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        xml = r.read().decode("utf-8", "replace")
    root = ET.fromstring(xml)
    rows = []
    for e in root.findall("atom:entry", ATOM_NS):
        aid = e.findtext("atom:id", default="", namespaces=ATOM_NS).split("/abs/")[-1]
        rows.append({
            "arxiv_id": aid.split("v")[0],
            "version": aid,
            "title": " ".join(e.findtext("atom:title", default="", namespaces=ATOM_NS).split()),
            "journal_ref": (e.findtext("arxiv:journal_ref", default="", namespaces=ATOM_NS) or "").strip(),
            "doi": (e.findtext("arxiv:doi", default="", namespaces=ATOM_NS) or "").strip().lower(),
            "authors": [a.findtext("atom:name", default="", namespaces=ATOM_NS)
                        for a in e.findall("atom:author", ATOM_NS)],
            "published": e.findtext("atom:published", default="", namespaces=ATOM_NS)[:10],
        })
    return rows


def clean_doi(d: str) -> str:
    d = (d or "").lower().strip()
    for pre in ("https://doi.org/", "http://doi.org/", "doi:"):
        if d.startswith(pre):
            d = d[len(pre):]
    return d.strip()


# ------------------------------------------------------------------ stage 1c: join
def build_index(toc_rows):
    """DOI map + normalized-title map + token inverted index (for cheap fuzzy join)."""
    by_doi, by_title, tok_index = {}, {}, {}
    for r in toc_rows:
        by_doi[r["doi"]] = r
        nt = norm_title(r["title"])
        if not nt:
            continue
        by_title.setdefault(nt, r)
        for tok in set(nt.split()):
            if len(tok) >= 4:
                tok_index.setdefault(tok, set()).add(nt)
    return by_doi, by_title, tok_index


def match(paper, by_doi, by_title, tok_index):
    """Return (toc_row, method) or (None, None). DOI first, then near-exact title.

    The fuzzy step is restricted to titles sharing >=2 significant tokens, which
    turns an O(pool x toc) brute force into a handful of comparisons per paper.
    """
    doi = clean_doi(paper.get("doi"))
    if doi and doi in by_doi:
        return by_doi[doi], "doi"
    nt = norm_title(paper["title"])
    if not nt:
        return None, None
    if nt in by_title:
        return by_title[nt], "title-exact"
    shared = {}
    for tok in set(nt.split()):
        if len(tok) < 4:
            continue
        for k in tok_index.get(tok, ()):
            shared[k] = shared.get(k, 0) + 1
    best, best_r = None, 0.0
    for k, c in shared.items():
        if c < 2 or abs(len(k) - len(nt)) > 25:
            continue
        r = difflib.SequenceMatcher(None, nt, k).ratio()
        if r > best_r:
            best, best_r = k, r
    if best and best_r >= 0.93:
        return by_title[best], f"title-fuzzy({best_r:.3f})"
    return None, None


def main():
    force = "--refresh-toc" in sys.argv
    toc = load_toc(force=force)

    print("\n=== authoritative denominator (Crossref) ===")
    grand = 0
    for k, rows in toc.items():
        grand += len(rows)
        print(f"  {k:12} {len(rows):>5} papers  ({YEAR_FROM}-{YEAR_TO})")
    print(f"  {'TOTAL':12} {grand:>5}")

    # ---- arXiv candidate pool
    pool = {}          # arxiv_id -> paper (dedup across queries)
    for jkey, queries in ARXIV_QUERIES.items():
        for q in queries:
            full = f"{q} AND submittedDate:[{YEAR_FROM}01010000 TO {YEAR_TO}12312359]"
            try:
                rows = arxiv_query(full)
            except Exception as e:
                print(f"[arxiv] {jkey} {q!r} FAILED {type(e).__name__}: {e}")
                continue
            new = 0
            for r in rows:
                if r["arxiv_id"] not in pool:
                    pool[r["arxiv_id"]] = r
                    new += 1
            print(f"[arxiv] {jkey:12} {q:52} returned {len(rows):>3}, new {new}")
            time.sleep(3)
    print(f"\n[arxiv] unique candidates: {len(pool)}")

    # ---- join + strict accept
    accepted, rejected, per_journal = [], [], {k: 0 for k in JOURNALS}
    methods = {}
    for jkey in JOURNALS:
        by_doi, by_title, tok_index = build_index(toc[jkey])
        for aid, p in pool.items():
            row, how = match(p, by_doi, by_title, tok_index)
            if row is None:
                continue
            if row["year"] < YEAR_FROM or row["year"] > YEAR_TO:
                continue
            accepted.append({
                "journal": jkey, "journal_name": JOURNALS[jkey]["name"],
                "crossref_doi": row["doi"], "crossref_title": row["title"],
                "crossref_journal": row["journal"], "pub_year": row["year"],
                "volume": row.get("volume"), "page": row.get("page"),
                "arxiv_id": aid, "arxiv_title": p["title"],
                "arxiv_journal_ref": p["journal_ref"], "arxiv_doi": p["doi"],
                "authors": p["authors"], "published": p["published"],
                "match_method": how,
            })
            methods[how.split("(")[0]] = methods.get(how.split("(")[0], 0) + 1

    # dedup by arxiv_id keeping the entry with the strongest match
    rank = {"doi": 0, "title-exact": 1}
    accepted.sort(key=lambda r: (r["journal"], rank.get(r["match_method"].split("(")[0], 2),
                                 -r["pub_year"]))
    seen, uniq = set(), []
    for r in accepted:
        key = (r["journal"], r["arxiv_id"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(r)

    # cap per journal, prefer recent publications
    picked = []
    for jkey in JOURNALS:
        rows = [r for r in uniq if r["journal"] == jkey]
        rows.sort(key=lambda r: -r["pub_year"])
        picked.extend(rows[:PER_JOURNAL])
        per_journal[jkey] = len(rows)

    print("\n=== join result (arXiv x Crossref) ===")
    for k in JOURNALS:
        n_toc = len(toc[k])
        n_cand = per_journal[k]
        print(f"  {k:12} toc={n_toc:>5}  with-arXiv-fulltext={n_cand:>4}  "
              f"({100.0 * n_cand / n_toc:.1f}% of journal)  taking {min(n_cand, PER_JOURNAL)}")
    print(f"  match methods: {methods}")
    print(f"  selected for pilot: {len(picked)}")

    CANDIDATES.write_text(json.dumps(picked, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nwrote {CANDIDATES}")

    print("\n=== selected papers ===")
    for r in sorted(picked, key=lambda x: (x["journal"], -x["pub_year"])):
        print(f"  [{r['journal']:12}] {r['pub_year']}  {r['arxiv_id']:11} {r['match_method']:20} "
              f"{r['crossref_title'][:62]}")


if __name__ == "__main__":
    main()
