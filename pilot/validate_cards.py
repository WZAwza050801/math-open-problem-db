"""Mechanical (LLM-free) validator for extracted problem cards.

Everything here is checkable by string/schema rules, so it is cheap and repeatable
and can run on every rerun as a regression gate.

Checks
  1. label in the six-label taxonomy
  2. current_status must be 'unknown' (only the status-tracking stage may fill it)
  3. self_check present with all four sub-items
  4. original_quote verifiable against the cached fulltext
     - strict: verbatim after whitespace normalisation
     - lenient: also after stripping LaTeX macros / braces / math delimiters
       (needed because ar5iv-sourced text is HTML-derived and never byte-identical)
  5. banned shorthand phrases in self_contained
  6. msc_primary format
  7. paper_time_status in allowed values
  8. duplicate quotes across cards
  9. suspiciously short quotes (weak evidence of a real citation)
 10. self_contained long enough to actually be self-contained
"""
import difflib
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
CACHE = BASE / "latex_cache"

NEAR_RATIO = 0.97
DUP_RATIO = 0.80      # self_contained similarity that means "same problem, twice"

ALLOWED_LABELS = {"real_open", "background_open", "method_obstruction",
                  "future_application", "solved_in_paper", "uncertain"}
ALLOWED_PAPER_TIME = {"open_at_paper_time", "solved_in_paper",
                      "background_known_open", "not_a_proposition"}
BANNED_PHRASES = re.compile(
    r"same notation as above|notation as above|as defined (above|earlier|previously)|"
    r"the above (problem|conjecture|statement)|with the notation of|see above", re.I)
MSC_RE = re.compile(r"^\d{2}[A-Z](\d{2})?$")
MIN_QUOTE = 40
MIN_SELF_CONTAINED = 60


def norm_ws(s):
    return " ".join((s or "").split())


def norm_latex(s):
    """Collapse LaTeX/HTML noise so an ar5iv-derived cache can still match a quote."""
    s = re.sub(r"\\[a-zA-Z]+\*?", " ", s or "")
    s = re.sub(r"[{}$\\_^~]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def norm_escape_typo(s):
    """Undo JSON-escape damage when the model transcribed plain prose with LaTeX habits.

    Observed, and the reason this function exists: the source reads
    "Whether or not this sequence ..." but the model emitted the prose word "not" as a
    LaTeX \\not inside the JSON string. `\\n` is a legal JSON escape, so the parser
    resolved it to a REAL newline and the stored quote became
    "Whether or<NEWLINE>ot this sequence". The letter "n" is gone and can never match.

    Repair, narrowly targeted: the prose word "not" was written as LaTeX \\not, and JSON
    resolved the \\n to a REAL newline - so "or not" is stored as "or<NEWLINE>ot". The
    letter n is gone. Restore it as " n" (space plus n), giving back "or not".

    DO NOT strip other backslashes: the source legitimately contains \\cite{BM},
    \\ref{...} etc. A blanket rule that deletes "\\" before a letter destroys real LaTeX
    and was observed to turn a matching quote into a non-matching one.

    Apply this to the QUOTE ONLY. The fulltext legitimately contains newlines everywhere,
    so repairing it would corrupt the very text we are matching against.
    """
    s = s or ""
    s = re.sub(r"(?<=[a-zA-Z])\n(?=[a-z])", " n", s)   # \n artifact that ATE the word "not"
    return s


def quote_found(quote, fulltext):
    """Classify how well a claimed verbatim quote is supported by the source.

    'verbatim'         exact, after whitespace normalisation
    'verbatim-lenient' exact after stripping LaTeX/HTML noise (needed for ar5iv text)
                       or after undoing \\not-style transcription typos
    'near-verbatim'    anchored window matches at >= NEAR_RATIO; in practice this is
                       a source typo the model silently corrected (observed:
                       "which is is ordinary" -> "which is ordinary")
    'partial'          both head and tail present, middle diverges
    'missing'          could not be located
    """
    # NOTE ORDER MATTERS: repair escape damage BEFORE whitespace normalisation,
    # because norm_ws would already have collapsed the offending newline into a space
    # and the evidence would be destroyed.
    q_raw, f_raw = quote or "", fulltext or ""
    q, f = norm_ws(q_raw), norm_ws(f_raw)
    if not q:
        return "missing"
    if q in f:
        return "verbatim"
    # transcription typos: model emitted the prose word "not" as LaTeX \not, so JSON
    # turned \n into a real newline and swallowed a letter. Repair the QUOTE only -
    # touching the fulltext would corrupt its legitimate newlines.
    qt = norm_ws(norm_escape_typo(q_raw))
    if qt and qt in f:
        return "verbatim-typo-repaired"
    ql, fl = norm_latex(q), norm_latex(f)
    if ql and ql in fl:
        return "verbatim-lenient"
    # hardest case: source wraps as "definitions of  pairs,\nsingularities" (two
    # spaces before the break) and the model rejoined it as "of pairs, singularities".
    # Collapsing ALL internal whitespace on both sides recovers it.
    qc, fc = re.sub(r"\s+", "", q), re.sub(r"\s+", "", f)
    if qc and qc in fc:
        return "verbatim-ws-collapsed"
    head, tail = q[:60], q[-60:]
    if head and tail and head in f and tail in f:
        return "partial"
    if head and head in f:
        return "partial"
    hl = norm_latex(head)
    if hl and hl in fl:
        return "partial"

    # anchored fuzzy: find the longest intact prefix (>=30 chars) and measure what
    # fraction of the quote is covered, in order, by a window around that anchor.
    # NOTE: difflib's ratio() is normalised by the sum of both lengths, so comparing
    # a 400-char quote against a 700-char window can never exceed ~0.72. We must use
    # the share of the *quote* that is matched instead.
    #
    # The prefix itself may be mutated (observed: "Theorem \ref{X}" -> "Theorems
    # \ref{X} and \ref{Y}"), so a full-length anchor finds nothing. Fall back through
    # shrinking anchors, and for each anchor that hits, score a window around it.
    best_cov, best_qlen = 0.0, len(q)
    for anchor_len in (80, 60, 45, 30, 20):
        probe = q[:anchor_len]
        if not probe or probe not in f:
            continue
        pos = f.index(probe)
        window = f[pos:pos + len(q) + 300]
        sm = difflib.SequenceMatcher(None, q, window, autojunk=False)
        coverage = sum(b.size for b in sm.get_matching_blocks()) / len(q)
        if coverage > best_cov:
            best_cov = coverage
        if coverage >= NEAR_RATIO:
            break
    if best_cov >= NEAR_RATIO:
        return "near-verbatim"
    if best_cov >= 0.80:
        # mostly the real sentence with an edited detail (added/removed \ref,
        # pluralised noun). Still evidence, but the quote is NOT faithful.
        return "partial-edited"
    if best_cov >= 0.60:
        return "partial"
    return "missing"


def main():
    conn = sqlite3.connect(BASE / "db.sqlite3")
    cols = [c[1] for c in conn.execute("PRAGMA table_info(problems)")]
    rows = [dict(zip(cols, r)) for r in conn.execute("SELECT * FROM problems")]
    if not rows:
        print("no cards to validate yet")
        return

    stats = Counter(cards=len(rows))
    issues = []
    cache = {}
    quote_seen = defaultdict(list)

    for r in rows:
        pid = r["id"]
        lab = r.get("label", "")
        if lab not in ALLOWED_LABELS:
            stats["label_bad"] += 1
            issues.append(f"{pid}: label '{lab}' not in taxonomy")
        if (r.get("current_status") or "") != "unknown":
            stats["cts_bad"] += 1
            issues.append(f"{pid}: current_status must be 'unknown', got '{r.get('current_status')}'")
        sc = r.get("self_check") or ""
        if not all(k in sc.lower() for k in ("conditions_complete", "notation_self_contained",
                                             "parameter_ranges_verbatim", "solved_in_this_paper")):
            stats["selfcheck_bad"] += 1
            issues.append(f"{pid}: self_check incomplete -> {sc[:80]!r}")
        if (r.get("paper_time_status") or "") not in ALLOWED_PAPER_TIME:
            stats["pts_bad"] += 1
            issues.append(f"{pid}: paper_time_status '{r.get('paper_time_status')}' invalid")
        if BANNED_PHRASES.search(r.get("self_contained") or ""):
            stats["banned_phrase"] += 1
            issues.append(f"{pid}: self_contained contains banned shorthand phrase")
        if not MSC_RE.match(r.get("msc_primary") or ""):
            stats["msc_bad"] += 1
            issues.append(f"{pid}: msc_primary '{r.get('msc_primary')}' malformed")

        q = r.get("original_quote") or ""
        if len(norm_ws(q)) < MIN_QUOTE:
            stats["quote_short"] += 1
            issues.append(f"{pid}: quote only {len(norm_ws(q))} chars (<{MIN_QUOTE})")
        if len(r.get("self_contained") or "") < MIN_SELF_CONTAINED:
            stats["self_contained_short"] += 1
            issues.append(f"{pid}: self_contained only {len(r.get('self_contained') or '')} chars")

        key = norm_latex(q)[:200]
        if key:
            quote_seen[key].append(pid)

        aid = r["arxiv_id"]
        if aid not in cache:
            p = CACHE / f"{aid}.tex"
            cache[aid] = p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""
        if not cache[aid]:
            stats["no_cache"] += 1
            issues.append(f"{pid}: no cached fulltext for {aid} -> unverifiable")
        res = quote_found(q, cache[aid])
        stats[f"quote_{res}"] += 1
        if res == "missing":
            issues.append(f"{pid}: quote NOT found in fulltext (possible fabrication) [{r.get('journal')}]")

    dup = {k: v for k, v in quote_seen.items() if len(v) > 1}
    if dup:
        stats["duplicate_quotes"] += len(dup)
        for k, v in list(dup.items())[:10]:
            issues.append(f"duplicate quote across cards: {v}")

    # intra-paper near-duplicate cards: the same problem emitted twice, once as a
    # general statement and once as a special case / restatement
    by_paper = defaultdict(list)
    for r in rows:
        by_paper[r["arxiv_id"]].append(r)
    for aid, group in by_paper.items():
        if len(group) < 2:
            continue
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                a, b = group[i], group[j]
                sa, sb = norm_ws(a.get("self_contained")), norm_ws(b.get("self_contained"))
                if len(sa) < 80 or len(sb) < 80:
                    continue
                ratio = difflib.SequenceMatcher(None, sa[:2000], sb[:2000]).ratio()
                if ratio >= DUP_RATIO:
                    stats["near_duplicate_pairs"] += 1
                    issues.append(
                        f"near-duplicate cards in {aid}: {a['id']}({a.get('label')}) "
                        f"~ {b['id']}({b.get('label')}) ratio={ratio:.2f}")

    print("=== mechanical validation ===")
    for k in ("cards", "label_bad", "cts_bad", "selfcheck_bad", "pts_bad", "banned_phrase",
              "msc_bad", "quote_short", "self_contained_short", "no_cache"):
        print(f"  {k:22} {stats[k]}")

    verb = (stats["quote_verbatim"] + stats["quote_verbatim-lenient"]
            + stats["quote_near-verbatim"])
    part = stats["quote_partial"]
    miss = stats["quote_missing"]
    print(f"\n  quote strict-verbatim   {stats['quote_verbatim']}")
    print(f"  quote lenient-verbatim  {stats['quote_verbatim-lenient']}")
    print(f"  quote near-verbatim     {stats['quote_near-verbatim']}   "
          f"(anchored diff >= {NEAR_RATIO}; usually a source typo silently corrected)")
    print(f"  quote partial           {part}")
    print(f"  quote MISSING           {miss}")
    print(f"  quote verifiability     {verb + part}/{stats['cards']} = {100*(verb+part)/stats['cards']:.1f}%")
    print(f"  duplicate quote groups  {stats['duplicate_quotes']}")
    print(f"  near-duplicate card pairs {stats['near_duplicate_pairs']}")
    print(f"\n  issues: {len(issues)}")
    for i in issues[:60]:
        print("   -", i)
    if len(issues) > 60:
        print(f"   ... and {len(issues)-60} more")

    print("\n=== quote verifiability by label ===")
    per = defaultdict(lambda: Counter())
    for r in rows:
        aid = r["arxiv_id"]
        res = quote_found(r.get("original_quote") or "", cache.get(aid, ""))
        per[r.get("label", "?")][res] += 1
    for lab, c in sorted(per.items(), key=lambda kv: -sum(kv[1].values())):
        tot = sum(c.values())
        good = c["verbatim"] + c["verbatim-lenient"] + c["near-verbatim"] + c["partial"]
        print(f"  {lab:20} {good}/{tot} = {100*good/tot:5.1f}%  {dict(c)}")


if __name__ == "__main__":
    main()
