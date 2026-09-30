"""Post-processing pass: enrich extracted problem cards.

For each extracted paper, one small LLM call over (paper context + all its
problem quotes) to recover what the main extraction pass did not capture:

  - problem_name   : does the text NAME this problem (Berry conjecture style)?
  - relations      : explicit statements like "special case of X", "generalizes Y"
  - depends_on     : famous conjectures/hypotheses it is tied to (RH, GRH, ...)

Context per paper: window around each quote from the local latex_cache
(no API cost for context building), fallback to head+tail of the source.

Output: enrich_results.jsonl, one record per paper:
  {"arxiv_id", "model", "items": [{"idx", "problem_id", "problem_name",
    "name_evidence", "relations": [...], "depends_on": [...]}]}
Idempotent: papers already present in the output file are skipped.

Usage: python enrich_cards.py [--limit N]
Env:   same key chain as run_pilot (GLM_KEYS > GLM_KEY > .env coding keys)
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
import time
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import run_pilot as R

BASE = R.BASE
DB = BASE / "db.sqlite3"
OUT = BASE / "enrich_results.jsonl"
WORKERS = int(R.os.environ.get("ENRICH_WORKERS", "3"))
MAX_Q = 1500          # context chars before quote
MAX_T = 1200          # context chars after quote
HEAD = 3500           # fallback: source head
TAIL = 2500           # fallback: source tail

PROMPT = """You are cataloguing open problems for a mathematics database.
Below are verbatim problem statements (quoted) extracted from ONE paper, each with a context excerpt from the paper's LaTeX source.

For EACH numbered problem, output strict JSON (no markdown), an array aligned with the input numbering:
[{{"idx": 1, "problem_name": null | "short canonical English name used in the literature",
   "name_evidence": null | "verbatim snippet (<=200 chars) where the text names it",
   "relations": [{{"kind": "specializes|generalizes|equivalent_to|implies|motivated_by",
                   "target": "name or short description of the other problem",
                   "evidence": "verbatim snippet (<=200 chars)"}}],
   "depends_on": ["famous conjecture/hypothesis names the problem is tied to, ONLY if stated"]}}]

Rules:
- problem_name is null unless the text (or standard usage evident in the text) actually names it.
- relations ONLY when the paper explicitly states the link; evidence must be verbatim from the text.
- Never invent relation targets; if none, use [].
- depends_on: only famous, widely-known conjectures/hypotheses explicitly mentioned.

Paper: {title} ({journal}, {year}), authors: {authors}

{contexts}
"""


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def context_for_paper(arxiv_id: str, quotes: list[str]) -> str:
    src_path = R.LATEX_CACHE / (arxiv_id.replace("/", "_") + ".tex")
    html_path = R.LATEX_CACHE / (arxiv_id.replace("/", "_") + ".ar5iv.txt")
    src = None
    for p in (src_path, html_path):
        if p.exists():
            txt = p.read_text(encoding="utf-8", errors="replace")
            if len(txt) > 1500:
                src = txt
                break
    if src is None:
        return "(source not cached; judge from the quotes alone)"
    nsrc = norm(src)
    blocks = []
    for i, q in enumerate(quotes, 1):
        nq = norm(q)
        probe = nq[:120]
        pos = nsrc.find(probe) if probe else -1
        if pos >= 0:
            lo, hi = max(0, pos - MAX_Q), min(len(nsrc), pos + len(nq) + MAX_T)
            blocks.append(f"[context {i}] ...{nsrc[lo:hi]}...")
        else:
            blocks.append(f"[context {i}] (exact location not found; source head/tail) "
                          f"HEAD: {nsrc[:HEAD]} ... TAIL: {nsrc[-TAIL:]}")
            break                       # fallback shared for the rest of this paper
    seen, uniq = set(), []
    for b in blocks:
        k = b[:80]
        if k not in seen:
            seen.add(k)
            uniq.append(b)
    return "\n\n".join(uniq)


def load_done() -> set[str]:
    done = set()
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    done.add(json.loads(line)["arxiv_id"])
                except Exception:
                    pass
    return done


def parse_items(content: str) -> list:
    """Robust parse: strip fences, try whole-array, then salvage complete objects."""
    c = content.strip()
    c = re.sub(r"^```(?:json)?\s*|\s*```$", "", c, flags=re.M)
    try:
        start = c.index("[")
        return json.loads(c[start:c.rindex("]") + 1])
    except Exception:
        pass
    items, dec, pos = [], json.JSONDecoder(), 0
    while True:
        brace = c.find("{", pos)
        if brace < 0:
            break
        try:
            obj, end = dec.raw_decode(c, brace)
            if isinstance(obj, dict) and "idx" in obj:
                items.append(obj)
            pos = max(end, brace + 1)
        except Exception:
            pos = brace + 1
    return items


def enrich_paper(row, problems) -> dict:
    arxiv_id = row["arxiv_id"]
    # Chunk large papers: long problem lists make the model reason until the
    # token budget starves the JSON (seen live: 16000 out, content_chars=0).
    CH = 6
    chunks = [problems[i:i + CH] for i in range(0, len(problems), CH)]
    all_items, tin, tout = [], 0, 0
    model = R.GLM_MODEL
    for ci, chunk in enumerate(chunks, 1):
        quotes = [p["original_quote"] for p in chunk]
        ctx = context_for_paper(arxiv_id, quotes)
        listing = "\n".join(
            f"[problem {i}] {norm(p['original_quote'])[:600]}\n  (label={p['label']}, section={p['quote_location']})"
            for i, p in enumerate(chunk, 1))
        prompt = PROMPT.format(
            title=row["title"] or "", journal=row["journal_name"] or row["journal"] or "",
            year=row["pub_year"], authors=(row["authors_json"] or "")[:300],
            contexts=f"{listing}\n\n{ctx}")
        d = R._glm_call(prompt, 16000, "low")
        content = (d.get("choices") or [{}])[0].get("message", {}).get("content", "")
        items = parse_items(content)
        u = d.get("usage") or {}
        tin += u.get("prompt_tokens") or 0
        tout += u.get("completion_tokens") or 0
        model = d.get("model", model)
        if not items:
            ch = (d.get("choices") or [{}])[0]
            all_items.append({"idx": None, "chunk": ci, "parse_empty": True,
                              "debug": {"finish": ch.get("finish_reason"),
                                        "content_chars": len(content),
                                        "tail": content[-300:]}})
            continue
        for it in items:
            idx = it.get("idx")
            if isinstance(idx, int) and 1 <= idx <= len(chunk):
                it["problem_id"] = chunk[idx - 1]["id"]
            it["chunk"] = ci
            all_items.append(it)
    return {"arxiv_id": arxiv_id, "model": model,
            "tokens_in": tin, "tokens_out": tout, "items": all_items}


def main():
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    papers = {r["arxiv_id"]: r for r in conn.execute(
        "select * from papers where fetch_status='extracted'")}
    by_paper = {}
    for p in conn.execute("select * from problems"):
        by_paper.setdefault(p["arxiv_id"], []).append(p)
    done = load_done()
    jobs = [(papers[aid], probs) for aid, probs in sorted(by_paper.items())
            if aid in papers and aid not in done]
    if limit:
        jobs = jobs[:limit]
    total_in = total_out = 0
    print(f"[enrich] papers={len(jobs)} skipped(done)={len(done)} workers={WORKERS}", flush=True)
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(enrich_paper, r, ps): r["arxiv_id"] for r, ps in jobs}
        for i, f in enumerate(as_completed(futs), 1):
            aid = futs[f]
            try:
                rec = f.result()
            except Exception as e:
                print(f"[{i}/{len(jobs)}] {aid} FAILED {type(e).__name__}: {str(e)[:140]}", flush=True)
                continue
            with OUT.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            total_in += rec.get("tokens_in") or 0
            total_out += rec.get("tokens_out") or 0
            n_named = sum(1 for it in rec["items"] if it.get("problem_name"))
            n_rel = sum(len(it.get("relations") or []) for it in rec["items"])
            print(f"[{i}/{len(jobs)}] {aid} items={len(rec['items'])} named={n_named} "
                  f"relations={n_rel} ok_total={i} elapsed={int(time.time()-t0)}s", flush=True)
    print(f"\nDONE papers={len(jobs)} tokens in={total_in:,} out={total_out:,} "
          f"elapsed={int(time.time()-t0)}s", flush=True)


if __name__ == "__main__":
    main()
