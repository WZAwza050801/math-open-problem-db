"""Build a Cursor-ready audit workspace from the pilot db.

Batch 1: 20 papers stratified by journal (prefer high-card-count papers),
each with source LaTeX + rendered CARDS.md + a pre-filled verdicts.csv.

Audit task per card (this is what Grok-in-Cursor will help verify):
  1. VERBATIM: original_quote appears character-for-character in source.tex
     (whitespace/line-break tolerant).
  2. CONDITIONS: self_contained carries the original parameter ranges.
  3. LABEL: real_open / background_open / method_obstruction / ... is right.
Verdict vocabulary: verbatim_ok | quote_mismatch | condition_altered |
label_wrong | fabricated
"""
from __future__ import annotations

import csv
import json
import shutil
import sqlite3
import textwrap
from pathlib import Path

BASE = Path(__file__).resolve().parent
DB = Path(r"D:/数学研究平台开发/open_problem_db/backups/db_2026-09-25_0915.sqlite3")
LATEX_CACHE = BASE / "latex_cache"
OUT = BASE / "audits" / "batch1"
N_PAPERS = 20
PER_JOURNAL_MIN = 1

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

rows = con.execute("""
    select p.arxiv_id, p.journal, p.journal_name, p.pub_year, p.title,
           p.crossref_doi, p.authors_json, count(pr.id) n_cards
    from papers p join problems pr on pr.arxiv_id = p.arxiv_id
    where p.fetch_status = 'extracted'
    group by p.arxiv_id order by p.journal, n_cards desc
""").fetchall()

# stratified pick: round-robin across journals, highest card count first
by_journal: dict[str, list] = {}
for r in rows:
    by_journal.setdefault(r["journal"], []).append(r)
picked = []
pools = {j: list(v) for j, v in by_journal.items()}
while len(picked) < N_PAPERS and any(pools.values()):
    for j in sorted(pools):
        if pools[j] and len(picked) < N_PAPERS:
            picked.append(pools[j].pop(0))

OUT.mkdir(parents=True, exist_ok=True)
verdict_rows = []

for r in picked:
    stem = r["arxiv_id"].replace("/", "_")
    safe = stem.replace(".", "_")
    folder = OUT / f"{r['journal']}_{r['pub_year']}_{safe}"
    folder.mkdir(exist_ok=True)

    tex_src = LATEX_CACHE / f"{stem}.tex"
    if tex_src.exists():
        shutil.copy(tex_src, folder / "source.tex")

    cards = con.execute(
        "select * from problems where arxiv_id = ? order by id",
        (r["arxiv_id"],)).fetchall()

    md = [f"# Audit: {r['title']}",
          "",
          f"- **Journal**: {r['journal_name']} ({r['pub_year']})",
          f"- **DOI**: {r['crossref_doi']}  |  **arXiv**: {r['arxiv_id']}",
          f"- **Cards**: {len(cards)}",
          "",
          "For each card check against `source.tex`:",
          "1. QUOTE — does `original_quote` appear verbatim (ignore whitespace/line breaks)?",
          "2. CONDITIONS — does `self_contained` keep the original hypotheses/parameter ranges?",
          "3. LABEL — is the label the right one for what the paper does?",
          "",
          "---", ""]
    for c in cards:
        md += [f"## {c['id']}  `{c['label']}`",
               "",
               f"**Location**: {c['quote_location'] or '(unspecified)'}",
               "",
               "**original_quote**:",
               "",
               textwrap.fill(c["original_quote"] or "", 100),
               "",
               "**self_contained**:",
               "",
               textwrap.fill(c["self_contained"] or "", 100),
               "",
               f"**MSC**: {c['msc_primary']}  |  **difficulty**: {c['difficulty_hint']}"
               f"  |  **paper_time_status**: {c['paper_time_status']}",
               f"**self_check**: {c['self_check']}",
               ]
        if c["flag_for_human"]:
            md += ["", f"⚠️ **flag_for_human**: {c['flag_for_human']}"]
        if c["uncertainty_notes"]:
            md += ["", f"**uncertainty_notes**: {c['uncertainty_notes']}"]
        md += ["", "---", ""]
        verdict_rows.append({
            "card_id": c["id"], "arxiv_id": r["arxiv_id"],
            "journal": r["journal"], "label": c["label"],
            "verdict": "", "note": ""})

    (folder / "CARDS.md").write_text("\n".join(md), encoding="utf-8")

with open(OUT / "verdicts.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["card_id", "arxiv_id", "journal", "label",
                                      "verdict", "note"])
    w.writeheader()
    w.writerows(verdict_rows)

summary = [f"# Batch 1 audit workspace", "",
           f"Papers: {len(picked)}  |  Cards: {len(verdict_rows)}", "",
           "## How to run this in Cursor",
           "",
           "1. Open this folder (`audits/batch1`) in Cursor.",
           "2. For each paper folder, ask Grok (Composer):",
           "   'Open CARDS.md and source.tex. For every card, verify the three checks",
           "   (quote verbatim, conditions preserved, label correct). Report any card",
           "   that fails, with the exact reason.'",
           "3. Spot-check Grok's claims yourself for a few cards per paper",
           "   (the model can be wrong in BOTH directions).",
           "4. Fill `verdict` in verdicts.csv using the vocabulary:",
           "   verbatim_ok | quote_mismatch | condition_altered | label_wrong | fabricated",
           "", "## Papers included", ""]
for r in picked:
    stem = r["arxiv_id"].replace("/", "_")
    safe = stem.replace(".", "_")
    has_tex = "tex✓" if (LATEX_CACHE / f"{stem}.tex").exists() else "tex✗(ar5iv only)"
    summary.append(f"- `{r['journal']}_{r['pub_year']}_{safe}` — {r['title'][:60]} "
                   f"({r['n_cards']} cards, {has_tex})")
(OUT / "AUDIT_GUIDE.md").write_text("\n".join(summary), encoding="utf-8")

print(f"workspace: {OUT}")
print(f"papers={len(picked)} cards={len(verdict_rows)}")
for r in picked:
    print(f"  {r['journal']:12s} {r['pub_year']}  {r['n_cards']:3d} cards  {r['title'][:50]}")
