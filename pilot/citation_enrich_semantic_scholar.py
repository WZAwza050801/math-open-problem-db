"""Stage 1a: enrich citing papers via Semantic Scholar Graph API.

For each of our 818 source DOIs (from citations.jsonl), fetch its S2 citations
with per-citation semantics: contexts (citation sentences), intents,
isInfluential + citing paper metadata (title/abstract/tldr/year/venue/ids).

Network: sandbox Python SSL is blocked, so HTTP goes through curl subprocess
via proxy 127.0.0.1:12000 (iKuuu VPN must be running).

Output: citation_enrich_citing_papers.jsonl -- one line per citing edge:
  {our_doi, s2_status, citing_doi, s2_paper_id, title, abstract, tldr,
   year, venue, arxiv, contexts, intents, is_influential}
Checkpoint: citation_enrich_done.txt (completed our_dois, one per line).
Resume: rerun the script; done DOIs are skipped, output deduped on our_doi.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
CITATIONS = BASE / "citations.jsonl"
OUT = BASE / "citation_enrich_citing_papers.jsonl"
DONE = BASE / "citation_enrich_done.txt"
PROXY = "http://127.0.0.1:12000"
FIELDS = "contexts,intents,isInfluential,title,abstract,year,venue,externalIds"
GAP = 1.1  # seconds between requests (unauthenticated S2 ~1 rps shared pool)


def curl_get(url: str, timeout: int = 40):
    """Return (http_code, text)."""
    p = subprocess.run(
        ["curl", "-s", "--max-time", str(timeout), "-x", PROXY, url, "-w", "\n%{http_code}"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    body, _, code = p.stdout.rpartition("\n")
    try:
        return int(code), body
    except ValueError:
        return 0, body


def fetch_citations(doi: str):
    """Fetch all citation edges for doi from S2. Returns (edges, status)."""
    edges, offset = [], 0
    while True:
        url = (f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
               f"/citations?fields={FIELDS}&limit=1000&offset={offset}")
        for attempt in range(5):
            code, body = curl_get(url)
            if code == 200:
                break
            if code == 404:
                return [], "s2_not_found"
            wait = 8 * (attempt + 1)
            print(f"    [{doi}] HTTP {code}, retry in {wait}s", flush=True)
            time.sleep(wait)
        else:
            return edges, f"error_http_{code}"
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            return edges, "error_bad_json"
        for rec in payload.get("data", []):
            cp = rec.get("citingPaper") or {}
            ext = cp.get("externalIds") or {}
            edges.append({
                "citing_doi": ext.get("DOI"),
                "s2_paper_id": cp.get("paperId"),
                "title": cp.get("title"),
                "abstract": cp.get("abstract"),
                "tldr": (cp.get("tldr") or {}).get("text") if cp.get("tldr") else None,
                "year": cp.get("year"),
                "venue": cp.get("venue"),
                "arxiv": ext.get("ArXiv"),
                "contexts": rec.get("contexts") or [],
                "intents": rec.get("intents") or [],
                "is_influential": bool(rec.get("isInfluential")),
            })
        nxt = payload.get("next")
        if nxt is None:
            return edges, "ok"
        offset = nxt
        time.sleep(GAP)


def load_done():
    if DONE.exists():
        return set(DONE.read_text(encoding="utf-8").split())
    return set()


def main():
    dois = []
    for line in CITATIONS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("n_citing") is not None:  # skip COCI fetch errors
            dois.append(rec["doi"])
    done = load_done()
    todo = [d for d in dois if d not in done]
    print(f"[s2-citing] total={len(dois)} done={len(done)} todo={len(todo)}", flush=True)

    t0 = time.time()
    n_edges = 0
    with OUT.open("a", encoding="utf-8") as out, DONE.open("a", encoding="utf-8") as ddone:
        for i, doi in enumerate(todo, 1):
            edges, status = fetch_citations(doi)
            out.write(json.dumps({
                "our_doi": doi, "s2_status": status, "n_edges": len(edges),
                "edges": edges, "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }, ensure_ascii=False) + "\n")
            out.flush()
            ddone.write(doi + "\n")
            ddone.flush()
            n_edges += len(edges)
            if i % 25 == 0 or i == len(todo):
                el = time.time() - t0
                eta = el / i * (len(todo) - i)
                print(f"[s2-citing] {i}/{len(todo)} edges={n_edges} "
                      f"elapsed={el/60:.1f}m eta={eta/60:.1f}m", flush=True)
            time.sleep(GAP)
    print(f"[s2-citing] DONE dois={len(todo)} edges={n_edges}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
