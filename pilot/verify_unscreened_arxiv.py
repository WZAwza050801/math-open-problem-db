"""Verify: do unscreened papers (TOC minus 823 candidates) actually lack open problems?
Sample 30, match titles on arXiv API (server has arXiv egress), regex abstracts.
"""
import json, os, random, re, time, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
toc = json.load(open(os.path.join(BASE, "crossref_toc.json"), encoding="utf-8"))
cand = json.load(open(os.path.join(BASE, "candidates.json"), encoding="utf-8"))

cand_dois = {(c.get("crossref_doi") or "").strip().lower() for c in cand}
all_p = []
for j, items in toc.items():
    for t in items:
        all_p.append({"journal": j, "doi": (t.get("doi") or "").strip().lower(),
                      "title": re.sub(r"\s+", " ", t.get("title") or "")})
unscreened = [p for p in all_p if p["doi"] and p["doi"] not in cand_dois]
print(f"total={len(all_p)} cand={len(cand_dois)} unscreened={len(unscreened)}")

MARKERS = re.compile(
    r"\b(open (problem|question)s?|we (conjecture|ask|pose)|conjecture (that|is)|"
    r"it (is|remains) (an? )?(open|unclear)|natural (question|problem)|(main )?(result|theorem) (is|:))", re.I)
CONJ_WORD = re.compile(r"\bconjecture|open problem|open question\b", re.I)

def arxiv_abstract(title):
    q = 'ti:"' + '" AND ti:"'.join(title.split()[:8]) + '"'
    url = ("http://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(q)
           + "&max_results=1")
    try:
        with urllib.request.urlopen(url, timeout=25) as r:
            xml = r.read().decode("utf-8", "replace")
        m = re.search(r"<summary>(.*?)</summary>", xml, re.S)
        total = re.search(r"totalResults[^>]*>(\d+)", xml)
        if m and total and int(total.group(1)) > 0:
            return " ".join(m.group(1).split())
    except Exception as e:
        return None
    return ""

rng = random.Random(7)
sample = rng.sample(unscreened, 30)
checked = matched = hits = conj = 0
detail = []
for p in sample:
    ab = arxiv_abstract(p["title"])
    time.sleep(3)  # arXiv rate limit
    if ab is None:
        detail.append({"title": p["title"][:60], "st": "query_fail"}); continue
    checked += 1
    if not ab:
        detail.append({"title": p["title"][:60], "st": "no_arxiv_match"}); continue
    matched += 1
    h = bool(CONJ_WORD.search(ab))
    hits += h
    if h:
        mm = CONJ_WORD.search(ab)
        detail.append({"title": p["title"][:60], "st": "HIT",
                       "ctx": ab[max(0, mm.start()-60):mm.end()+60]})
    else:
        detail.append({"title": p["title"][:60], "st": "clean"})
print(json.dumps({"sampled": 30, "arxiv_matched": matched, "marker_hits": hits,
                  "hit_rate_among_matched": round(hits / max(matched, 1), 3)},
                 ensure_ascii=False, indent=1))
for d in detail:
    print(d)
