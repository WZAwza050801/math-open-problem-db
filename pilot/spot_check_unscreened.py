"""Spot-check: do unscreened papers (Crossref TOC minus 823 candidates) actually
lack open problems? Sample N, fetch abstracts (Crossref / arXiv), regex for
problem-marker phrases, report hit rate with confidence interval.
Run from LOCAL machine (server egress to api.crossref.org unverified).
"""
import json, os, random, re, sys, urllib.request, urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))
TOC = os.path.join(BASE, "crossref_toc.json")
CAND = os.path.join(BASE, "candidates_cached.json")
N = 30
MARKERS = re.compile(
    r"\b(open (problem|question)|we (conjecture|ask|pose)|conjecture that|"
    r"it (is|remains) (an? )?(open|conjectured)|natural (question|problem) (is|arises)|"
    r"we leave (it )?(as )?open)\b", re.I)

def fetch(doi):
    url = "https://api.crossref.org/works/" + doi
    req = urllib.request.Request(url, headers={"User-Agent": "open-problem-db/0.1 (mailto:3116809059@qq.com)"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            m = json.load(r)["message"]
        return (m.get("abstract") or "", m.get("title", [""])[0])
    except Exception as e:
        return (None, str(e)[:60])

toc = json.load(open(TOC, encoding="utf-8"))
if isinstance(toc, dict):
    toc = toc.get("items") or toc.get("papers") or list(toc.values())[0]
cand = json.load(open(CAND, encoding="utf-8"))
if isinstance(cand, dict):
    cand = cand.get("items") or cand.get("candidates") or list(cand.values())[0]

def norm(x):
    return (x or "").strip().lower()

cand_dois = {norm(c.get("doi")) for c in cand if isinstance(c, dict)}
toc_dois = [norm(t.get("doi")) for t in toc if isinstance(t, dict) and norm(t.get("doi"))]
unscreened = sorted(set(toc_dois) - cand_dois - {""})
print(f"TOC total={len(toc_dois)}  candidates={len(cand_dois)}  unscreened={len(unscreened)}")

rng = random.Random(42)
sample = rng.sample(unscreened, min(N, len(unscreened)))
hits = checked = noabs = 0
detail = []
for doi in sample:
    abstract, title = fetch(doi)
    if abstract is None:
        detail.append({"doi": doi, "status": "fetch_fail", "info": title})
        continue
    checked += 1
    if not abstract.strip():
        noabs += 1
        detail.append({"doi": doi, "status": "no_abstract", "title": title[:80]})
        continue
    hit = bool(MARKERS.search(abstract))
    hits += hit
    detail.append({"doi": doi, "status": "hit" if hit else "clean",
                   "title": title[:80], "marker": MARKERS.search(abstract).group(0) if hit else None})

print(json.dumps({"sampled": len(sample), "checked": checked, "no_abstract": noabs,
                  "marker_hits": hits,
                  "hit_rate": round(hits / max(checked - noabs, 1), 3)},
                 ensure_ascii=False, indent=1))
for d in detail:
    print(d)
