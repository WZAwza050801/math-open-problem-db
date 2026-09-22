"""Probe: what does arXiv `jr:` actually match, and can we get precision + coverage?

Tests, per journal:
  A. quoted phrase variants         -> does jr:"Ann. of Math." work?
  B. sortBy=relevance vs submittedDate -> is the candidate pool clean?
  C. arxiv:doi presence             -> is a Crossref cross-check viable?
Prints, for each query, the journal_ref values returned with a strict-verify verdict.
"""
from __future__ import annotations

import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ARXIV_API = "https://export.arxiv.org/api/query"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
UA = {"User-Agent": "open-problem-db-pilot/0.1 (research; contact: local)"}

DATE = "submittedDate:[200001010000 TO 202512312359]"

QUERIES = {
    "annals-phrase-abbrev": 'jr:"Ann. of Math."',
    "annals-phrase-full": 'jr:"Annals of Mathematics"',
    "annals-loose": "jr:Annals AND jr:Mathematics",
    "acta-phrase-abbrev": 'jr:"Acta Math."',
    "acta-phrase-full": 'jr:"Acta Mathematica"',
    "invent-phrase-abbrev": 'jr:"Invent. Math."',
    "invent-phrase-full": 'jr:"Inventiones Mathematicae"',
    "invent-loose": "jr:Inventiones",
    "jams-phrase-abbrev": 'jr:"J. Amer. Math. Soc."',
    "jams-phrase-full": 'jr:"Journal of the American Mathematical Society"',
    "ihes-hautes": "jr:Hautes",
    "ihes-phrase": 'jr:"Publ. Math. Inst. Hautes"',
}

# strict, anchored: the journal_ref must *be* the journal, not merely contain the words
STRICT = {
    "annals": re.compile(
        r"^\s*(ann\.?\s+of\s+math\.?|annals\s+of\s+mathematics)\b"
        r"(?!\s*(and|or|studies|philosophy|physics|letters))", re.I),
    "acta": re.compile(
        r"^\s*(acta\s+math\.?|acta\s+mathematica)\b"
        r"(?!\s*(hungar|sinica|scientia|vietnam|applicandae|univ|academ))", re.I),
    "inventiones": re.compile(r"^\s*(invent\.?\s+math|inventiones\s+math)", re.I),
    "jams": re.compile(r"^\s*(j\.?\s*amer\.?\s*math\.?\s*soc|journal\s+of\s+the\s+american\s+mathematical\s+society)\b", re.I),
    "ihes": re.compile(r"^\s*(publ\.?\s*math\.?\s*(i\.?\s*h\.?\s*e\.?\s*s|inst)|hautes\s+etudes)", re.I),
}


def http_get(url, params=None, timeout=90):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def query(q, max_results=50, sort_by="relevance"):
    xml = http_get(ARXIV_API, {
        "search_query": q, "sortBy": sort_by, "sortOrder": "descending",
        "start": 0, "max_results": max_results,
    }).decode("utf-8", "replace")
    root = ET.fromstring(xml)
    total = root.find("{http://a9.com/-/spec/opensearch/1.1/}totalResults")
    out = []
    for e in root.findall("atom:entry", ATOM_NS):
        aid = e.findtext("atom:id", default="", namespaces=ATOM_NS).split("/abs/")[-1].split("v")[0]
        out.append({
            "id": aid,
            "title": " ".join(e.findtext("atom:title", default="", namespaces=ATOM_NS).split())[:60],
            "jr": (e.findtext("arxiv:journal_ref", default="", namespaces=ATOM_NS) or "").strip(),
            "doi": (e.findtext("arxiv:doi", default="", namespaces=ATOM_NS) or "").strip(),
            "pub": e.findtext("atom:published", default="", namespaces=ATOM_NS)[:10],
        })
    return int(total.text) if total is not None and total.text else -1, out


def verdict(jkey, jr):
    if not jr:
        return "-"
    for k, pat in STRICT.items():
        if pat.search(jr):
            return "TRUE" if k == jkey else f"WRONG:{k}"
    return "false"


def main():
    print(f"{'query':24} {'total':>7} {'n':>4}  true/other   sample journal_refs")
    print("-" * 120)
    doi_hits = 0
    total_entries = 0
    for name, q in QUERIES.items():
        jkey = name.split("-")[0]
        jkey = {"annals": "annals", "acta": "acta", "invent": "inventiones",
                "jams": "jams", "ihes": "ihes"}[jkey]
        try:
            total, rows = query(f"{q} AND {DATE}", max_results=50)
        except Exception as e:
            print(f"{name:24} FAILED {type(e).__name__}: {e}")
            continue
        trues = [r for r in rows if verdict(jkey, r["jr"]) == "TRUE"]
        for r in rows:
            total_entries += 1
            if r["doi"]:
                doi_hits += 1
        print(f"{name:24} {total:>7} {len(rows):>4}  {len(trues):>2}/{len(rows)-len(trues):<3}       "
              f"{' | '.join(r['jr'][:38] for r in rows[:3])}")
        if trues:
            for r in trues[:4]:
                print(f"{'':24} {'':>7} {'':>4}   TRUE  {r['id']}  {r['jr'][:60]}  doi={r['doi'][:30]}")
        time.sleep(3)
    print("-" * 120)
    print(f"doi present on {doi_hits}/{total_entries} entries")


if __name__ == "__main__":
    main()
