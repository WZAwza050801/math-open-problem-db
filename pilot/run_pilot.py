"""Pilot v3: extract open problems from a *Crossref-verified* corpus.

Pipeline: candidates.json (from harvest.py) -> fulltext (LaTeX /src/ -> ar5iv) ->
GLM-5.3 structured extraction -> SQLite -> JSONL export.

Changes vs v2 and why:
  * input is candidates.json, not an arXiv `jr:` guess. Journal identity and
    publication year come from Crossref, so precision is 100% by construction.
  * 3 worker threads. arXiv requests are serialised behind a global lock with a
    5s gap (arXiv cools down per-paper-id and punishes bursts); LLM calls, which
    dominate wall-clock, run concurrently.
  * glm-5.3 is a reasoning model and its thinking tokens are billed as output.
    v2 lost whole papers to `content=""` when thinking ate max_tokens. Now we
    request thinking ON with a high ceiling, and on failure retry with thinking
    OFF so the JSON is always emitted.
  * content-derived stable ids keep reruns idempotent.
"""
from __future__ import annotations

import gzip
import hashlib
from io import BytesIO
import json
import os
import posixpath
import re
import sqlite3
import tarfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent
DB_PATH = BASE / "db.sqlite3"
EXPORT_DIR = BASE / "exports"
LATEX_CACHE = BASE / "latex_cache"
CANDIDATES_JSON = Path(os.environ.get("CANDIDATES_JSON_PATH") or (BASE / "candidates.json"))

def load_env_file(path):
    """Minimal .env reader - deliberately dependency-free (stdlib only).

    The API key must never be committed. Resolution order:
      1. a real environment variable (this is how a server is configured)
      2. a local .env file, which .gitignore excludes
    A working copy therefore keeps running with no extra setup, while nothing
    secret can reach the repository.
    """
    if not path.exists():
        return {}
    out = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


_LOCAL_ENV = load_env_file(BASE / ".env")

GLM_BASE = os.environ.get("GLM_BASE_URL") or "https://open.bigmodel.cn/api/coding/paas/v4"
# Coding Plan endpoint (-- /api/coding/paas/v4 deducts SUBSCRIPTION credits).
# NEVER swap to /api/paas/v4: that endpoint bills the account balance
# (pay-as-you-go). Quota exhaustion on the coding endpoint raises an error
# instead of spending money -- that is the desired failure mode.
#
# Key chain: GLM_KEYS env (comma-separated) > GLM_KEY env > .env coding keys.
# When one key's quota runs out (1113 balance / 429 quota / 1311 plan), calls
# rotate to the next key; the chain NEVER falls back to a pay-as-you-go key.
GLM_KEYS = [k.strip() for k in os.environ.get("GLM_KEYS", "").split(",") if k.strip()]
if not GLM_KEYS:
    _k1 = os.environ.get("GLM_KEY") or _LOCAL_ENV.get("GLM_KEY", "")
    if _k1:
        GLM_KEYS = [_k1]
if not GLM_KEYS:
    GLM_KEYS = [k for k in (_LOCAL_ENV.get("GLM_CODING_LITE_KEY", ""),
                            _LOCAL_ENV.get("GLM_CODING_TEAM_KEY", "")) if k]
GLM_MODEL = os.environ.get("GLM_MODEL", "glm-5.3")
# Engine flavor: "glm" adds the GLM thinking param + GLM retry plan;
# "openai" = generic OpenAI-compatible endpoint (Qwen token plan etc.),
# no thinking param, smaller max_tokens plan.
ENGINE_FLAVOR = os.environ.get("ENGINE_FLAVOR", "glm")
# ENGINE_SLICE=i/N: process only every N-th paper of the remaining todo,
# starting at i. Lets multiple engine processes share one queue with ZERO
# overlap; every engine restarts recompute from done_ids, still disjoint.
ENGINE_SLICE = os.environ.get("ENGINE_SLICE", "")
# Keys that are forbidden on the billing endpoint even as a last resort.
GLM_KEYS = [k for k in GLM_KEYS if k]

# All three knobs are environment-overridable so a server run can be tuned
# without editing source: PILOT_WORKERS=16 MAX_CHARS=180000 python run_pilot.py
#
# WORKERS  - concurrent LLM calls. This is the real speed lever, because the
#            bottleneck is waiting on the API, not local compute. Raise it until
#            the provider rate-limits, then back off.
# ARXIV_GAP- seconds between arXiv fulltext requests, enforced globally across
#            threads. arXiv punishes bursts, so downloads stay serial by design;
#            they are not the bottleneck anyway.
# MAX_CHARS- source budget per paper. This is the COST lever: input scales with
#            paper length and dominates the bill on long-form corpora.
WORKERS = int(os.environ.get("PILOT_WORKERS", "6"))
ARXIV_GAP = float(os.environ.get("ARXIV_GAP", "5"))
MAX_CHARS = int(os.environ.get("MAX_CHARS", "260000"))   # median paper is 207k
TAIL_FRACTION = float(os.environ.get("TAIL_FRACTION", "0.35"))

UA = {"User-Agent": "open-problem-db-pilot/0.1 (research; contact: local)"}
BROWSER_UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36",
    "Accept": "*/*",
}

_arxiv_lock = threading.Lock()
_arxiv_last = [0.0]
_db_lock = threading.Lock()
_print_lock = threading.Lock()
_counter_lock = threading.Lock()


def log(msg):
    with _print_lock:
        print(msg, flush=True)


def arxiv_get(url, timeout=180):
    """Serialised, rate-limited arXiv access."""
    with _arxiv_lock:
        wait = ARXIV_GAP - (time.time() - _arxiv_last[0])
        if wait > 0:
            time.sleep(wait)
        try:
            req = urllib.request.Request(url, headers=BROWSER_UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        finally:
            _arxiv_last[0] = time.time()


def http_get(url, timeout=120, headers=None):
    req = urllib.request.Request(url, headers=headers or UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


# ---------- full text ----------
def decode_bytes(payload):
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            return payload.decode(enc)
        except UnicodeDecodeError:
            continue
    return payload.decode("utf-8", "replace")


LATEX_EXTS = (".tex", ".ltx", ".latex")
INCLUDE_PATTERN = re.compile(r"\\(?:input|include)\s*\{(?P<target>[^{}]+)\}", re.I)


def extract_tex_docs(payload):
    docs = {}
    try:
        with tarfile.open(fileobj=BytesIO(payload), mode="r:*") as tf:
            for m in tf.getmembers():
                if m.isfile() and m.name.lower().endswith(LATEX_EXTS):
                    docs[m.name] = decode_bytes(tf.extractfile(m).read())
        if docs:
            return docs
    except tarfile.ReadError:
        pass
    try:
        payload = gzip.decompress(payload)
    except OSError:
        pass
    text = decode_bytes(payload)
    if "\\begin{" in text or "\\documentclass" in text:
        docs["source.tex"] = text
    return docs


def norm_path(p):
    p = posixpath.normpath(p.replace("\\", "/").strip())
    return p[2:] if p.startswith("./") else p


def assemble(docs):
    file_map = {}
    for name, content in docs.items():
        file_map.setdefault(norm_path(name), content)
    roots = sorted(k for k, c in file_map.items()
                   if "\\documentclass" in c.lower() or "\\begin{document}" in c.lower()) or sorted(file_map)

    def resolve(path, stack):
        if path in stack or len(stack) > 20:
            return ""
        src = file_map.get(path)
        if src is None:
            return ""
        cur = posixpath.dirname(path)

        def repl(m):
            t = norm_path(m.group("target"))
            cands = [posixpath.join(cur, t), t]
            if not t.lower().endswith(LATEX_EXTS):
                cands += [c + e for c in (posixpath.join(cur, t), t) for e in LATEX_EXTS]
            for c in cands:
                c = norm_path(c)
                if c in file_map:
                    return "\n" + resolve(c, stack + [path])
            base = [k for k in file_map if posixpath.basename(k) in
                    (posixpath.basename(t), posixpath.basename(t) + ".tex")]
            if len(base) == 1:
                return "\n" + resolve(base[0], stack + [path])
            return ""
        return INCLUDE_PATTERN.sub(repl, src)
    return "\n\n".join(resolve(r, []) for r in roots)


def html_unescape(s):
    import html as _h
    return _h.unescape(s)


def html_to_text(html: str) -> str:
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<math[^>]*alttext=\"([^\"]*)\"[^>]*>.*?</math>", r" $\1$ ", html, flags=re.S | re.I)
    html = re.sub(r"<h([1-6])[^>]*>", r"\n\n## ", html, flags=re.I)
    html = re.sub(r"</p>|</div>|</li>|<br\s*/?>", "\n", html, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", html)
    text = html_unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fetch_fulltext(arxiv_id):
    """LaTeX source first, HTML second.

    Channel discovery (see probe_channels.py): `arxiv.org/src/{id}` and
    `arxiv.org/e-print/{id}` return HTTP 406 for ids this host has never fetched,
    while the official export mirror `export.arxiv.org/e-print/{id}` serves the
    same gzip LaTeX tarball with a 200. The 406 is per (host, path, id) -- an id
    that has already been fetched from arxiv.org keeps working -- so retrying is
    useless and the mirror is the correct primary channel.

    The two channels are cached under different names on purpose: ar5iv text is
    HTML-derived and its mathematics is mangled, so it must never masquerade as a
    LaTeX source for a later run.
    """
    LATEX_CACHE.mkdir(exist_ok=True)
    stem = arxiv_id.replace("/", "_")
    tex_cache = LATEX_CACHE / f"{stem}.tex"
    html_cache = LATEX_CACHE / f"{stem}.ar5iv.txt"

    if tex_cache.exists():
        txt = tex_cache.read_text(encoding="utf-8", errors="replace")
        if len(txt) > 1500:
            return txt, "cache-latex"

    for url, name in ((f"https://export.arxiv.org/e-print/{arxiv_id}", "export/e-print"),
                      (f"https://arxiv.org/src/{arxiv_id}", "arxiv/src")):
        try:
            payload = arxiv_get(url)
        except urllib.error.HTTPError as e:
            log(f"  [{arxiv_id}] {name} HTTP {e.code}")
            continue
        except Exception as e:
            log(f"  [{arxiv_id}] {name} {type(e).__name__}: {e}")
            continue
        if payload[:5] == b"%PDF-":
            log(f"  [{arxiv_id}] {name} returned PDF-only source")
            continue
        docs = extract_tex_docs(payload)
        if docs:
            full = assemble(docs)
            if full.strip():
                tex_cache.write_text(full, encoding="utf-8")
                return full, name
        log(f"  [{arxiv_id}] {name} assembly empty")

    if html_cache.exists():
        txt = html_cache.read_text(encoding="utf-8", errors="replace")
        if len(txt) > 3000:
            return txt, "cache-ar5iv"

    try:
        html = arxiv_get(f"https://ar5iv.labs.arxiv.org/html/{arxiv_id}")
        text = html_to_text(html.decode("utf-8", "replace"))
        if len(text) > 3000:
            html_cache.write_text(text, encoding="utf-8")
            return text, "ar5iv"
        log(f"  [{arxiv_id}] ar5iv too short ({len(text)})")
    except urllib.error.HTTPError as e:
        log(f"  [{arxiv_id}] ar5iv HTTP {e.code}")
    except Exception as e:
        log(f"  [{arxiv_id}] ar5iv {type(e).__name__}: {e}")
    return None, None


# ---------- extraction ----------
EXTRACT_PROMPT = """You are an expert mathematical literature extractor. Read the FULL source of the paper below and extract every open problem, conjecture, question, and stated research direction.

## Label taxonomy (use EXACTLY these six; do not compress into three)
- "real_open": a genuine unresolved mathematical proposition posed or left open by THIS paper (or explicitly adopted by this paper as its own open target). Must be a decidable-ish mathematical statement.
- "background_open": a famous open problem cited as background/motivation (e.g. Riemann, Hodge, abc, mass gap). NOT this paper's own target.
- "method_obstruction": the paper shows a method/estimate fails or a hypothesis is needed, WITHOUT formally posing an open problem.
- "future_application": a value judgement, taste comment, or application outlook ("may be useful for simulations", "should extend to other systems"). NOT a mathematical proposition.
- "solved_in_paper": the paper itself proves/disproves it, or proves the crucial special case.
- "uncertain": insufficient context to decide.

## Discipline rules (violating any = failure)
1. VERBATIM QUOTE: original_quote must be copied character-for-character from the source. Never paraphrase or reconstruct.
2. ORIGINAL CONDITIONS ARE SACRED: self_contained MUST carry over every hypothesis, constraint, domain, and parameter range of the original statement. Never strengthen or weaken a condition. If the original says "0<l<1", do not write "for all l>0". If the original says "any manifold", do not write "any compact manifold".
3. NO SHORTHAND REFERENCES: never write "with the same notation as above", "as defined earlier", "the above problem", etc. Every card must be independently readable on its own. Define every symbol you use.
4. SYMBOL-LEVEL SELF-CHECK: for any statement containing a parameter range, an inequality, or an asymptotic order (O(.), ~, -> infinity), re-derive or re-read the claim literally. Flag any place where the source's own claim looks questionable (e.g. an exponent conclusion that only holds in part of the stated range) in flag_for_human - do NOT silently reproduce a suspicious inference.
5. NO TASKIFICATION: never turn a value judgement, taste remark, or application outlook into a research task. If the source is not a proposition, label "future_application" and say so explicitly in self_contained.
6. NO DUPLICATE CARDS: if two statements from the same paper are essentially the same problem (one general, one a special case or an implementation of it), emit ONE card and note the relation in related_note.
7. Two status fields, never mixed:
   - paper_time_status: was it unresolved AT THE TIME the paper was written, as this paper treats it? ("open_at_paper_time" / "solved_in_paper" / "background_known_open" / "not_a_proposition")
   - current_status: today's status. You CANNOT verify this from the paper alone - always write "unknown" (it is filled later by a dedicated literature-tracking stage).
8. self_check: answer these four in one line each: conditions_complete (yes/no) | notation_self_contained (yes/no) | parameter_ranges_verbatim (yes/no) | solved_in_this_paper (yes/no).
9. msc_2020: one primary code plus optional secondary codes (e.g. "11N", "14J", "35Q", "42B", "53D12", "81T13").
10. JSON SAFETY: the output must be machine-parsable JSON. Inside every JSON string, every backslash must be doubled (write \\Sigma, \\ref{sec:intro}, \\frf), and every double quote must be escaped. Verbatim quotes are full of LaTeX, so this is the single most common way the output gets destroyed - check it before you finish.
11. Never fabricate. Anything doubtful goes to uncertainty_notes or flag_for_human.

Return ONE JSON object only (no markdown fences), exactly this shape:
{
  "paper_summary": "one sentence",
  "problems": [
    {
      "original_quote": "verbatim excerpt",
      "quote_location": "e.g. Section 5 / Remark 6.5 / Concluding remarks",
      "self_contained": "fully self-contained statement; all hypotheses and parameter ranges inlined",
      "label": "real_open | background_open | method_obstruction | future_application | solved_in_paper | uncertain",
      "label_rationale": "why this label, max 40 words",
      "paper_time_status": "open_at_paper_time | solved_in_paper | background_known_open | not_a_proposition",
      "current_status": "unknown",
      "msc_primary": "53D12",
      "msc_secondary": ["14A30"],
      "difficulty_hint": "easy | medium | hard | frontier",
      "self_check": "conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no",
      "flag_for_human": "suspicious inference or missing context, else empty",
      "related_note": "relation to another card from this paper, else empty",
      "uncertainty_notes": ""
    }
  ]
}
If the paper contains NO problems of any kind, return {"paper_summary": "...", "problems": []}.

PAPER METADATA:
Title: {title}
Authors: {authors}
Journal: {journal} ({year})
arXiv: {arxiv_id}

FULL SOURCE:
{latex}
"""


INVALID_ESCAPE = re.compile(r'\\(?!["\\/bfnrtu])')


def parse_json_loose(text):
    """Parse model JSON as forgivingly as possible.

    The dominant real failure is NOT truncation: verbatim LaTeX quotes contain
    backslashes (\\Sigma, \\ref{...}) and the model sometimes emits them unescaped,
    which makes the whole document invalid JSON ('\\S' is not a legal escape). A
    second attempt usually escapes correctly, which is why this looks intermittent.
    We therefore retry with invalid escapes doubled up, and allow raw control
    characters inside strings.
    """
    text = (text or "").strip()
    if not text:
        return None

    candidates = []
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S | re.I)
    if m:
        candidates.append(m.group(1).strip())
    candidates.append(text)

    for s in candidates:
        repaired = INVALID_ESCAPE.sub(r"\\\\", s)
        for variant in (s, repaired):
            for strict in (True, False):
                try:
                    obj = json.loads(variant, strict=strict)
                    if isinstance(obj, (dict, list)):
                        return obj
                except Exception:
                    pass

    dec = json.JSONDecoder(strict=False)
    for m in re.finditer(r"[\[{]", text):
        try:
            obj, _ = dec.raw_decode(text[m.start():])
            return obj
        except Exception:
            continue
    return None


def _glm_call(prompt, max_tokens, thinking):
    if not GLM_KEYS:
        raise RuntimeError(
            "missing credential: set GLM_KEYS (comma-separated coding-plan keys), or add "
            "GLM_CODING_LITE_KEY / GLM_CODING_TEAM_KEY to "
            f"{BASE / '.env'}. Never commit real keys.")
    body = {"model": GLM_MODEL, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens}
    if ENGINE_FLAVOR == "glm":
        body["temperature"] = 0.1   # kimi-for-coding only accepts temperature=1
    if thinking is not None and ENGINE_FLAVOR == "glm":
        body["thinking"] = {"type": thinking}
    # Quota-exhaustion signatures on the coding endpoint. On these we rotate to
    # the next key in the chain instead of retrying the spent key. A billing
    # endpoint (1113 balance) can never be reached because GLM_BASE is pinned
    # to /api/coding/paas/v4.
    # NOTE: 1302 ("并发量过高") is a CONCURRENCY rejection, not exhaustion --
    # rotating keys does not help; the caller's 429 backoff handles it.
    # 1311 ("套餐未开放该模型") is a plan-permission error -- same on every key.
    _QUOTA_SIGNS = ("1113", "余额不足", "额度已用", "使用上限")
    kind, last = None, None
    for ki, key in enumerate(GLM_KEYS):
        for attempt in range(20):
            req = urllib.request.Request(
                GLM_BASE.rstrip("/") + "/chat/completions", data=json.dumps(body).encode(), method="POST",
                headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=900) as resp:
                    return json.load(resp)
            except urllib.error.HTTPError as e:
                detail = ""
                try:
                    detail = e.read().decode("utf-8", "replace")
                except Exception:
                    pass
                last = f"key#{ki + 1} HTTP {e.code}: {detail[:160]}"
                if e.code != 429:
                    kind = "http"
                    log(f"  [glm] {last}")
                    break
                if any(s in detail for s in _QUOTA_SIGNS):
                    kind = "quota"          # exhausted: rotate to next key
                    log(f"  [glm] {last}")
                    break
                # 1302 concurrency / other rate limit: wait, retry SAME key
                time.sleep(30)
                continue
            except Exception as e:
                kind = "neterr"
                last = f"key#{ki + 1} {type(e).__name__}: {e}"
                log(f"  [glm] {last}")
                break
        if kind in ("quota", "neterr") and ki + 1 < len(GLM_KEYS):
            continue
        break
    raise RuntimeError(f"all {len(GLM_KEYS)} GLM keys failed; last: {last}")


def truncate_source(text, budget=MAX_CHARS, tail_frac=TAIL_FRACTION):
    """Head + tail, not a plain prefix cut.

    Open problems overwhelmingly appear in the introduction (as motivation) and in
    the final section ("Concluding remarks", "Further questions"). A naive
    text[:MAX] keeps only the former, so we always reserve part of the budget for
    the end of the paper.
    """
    if len(text) <= budget:
        return text
    tail = int(budget * tail_frac)
    head = budget - tail
    omitted = len(text) - budget
    return (text[:head]
            + f"\n\n[... {omitted:,} characters from the middle of the source omitted ...]\n\n"
            + text[-tail:])


def llm_extract(cand, latex_text):
    prompt = (EXTRACT_PROMPT
              .replace("{title}", cand.get("crossref_title") or cand.get("title") or "")
              .replace("{authors}", ", ".join(cand.get("authors", [])[:6]))
              .replace("{journal}", cand.get("journal_name") or cand.get("journal") or "")
              .replace("{year}", str(cand.get("pub_year") or cand.get("year") or ""))
              .replace("{arxiv_id}", cand["arxiv_id"])
              .replace("{latex}", truncate_source(latex_text)))
    # attempt 1: reason carefully. attempt 2: no thinking, so the JSON always lands.
    # glm-5.3 forces thinking: "disabled" is rejected (1210), so the fallback
    # attempt uses the low thinking tier instead -- it preserves the JSON output
    # budget (enabled-mode reasoning can starve it, finish=length content empty).
    # 96k output budget (max accepted by the coding endpoint, probed live):
    # runaway reasoning on hard/long papers hit 48k then 64k; 96k lets even
    # the worst case finish thinking AND write the full JSON answer.
    if ENGINE_FLAVOR == "openai":
        plan = [(65536, None, "std"), (32768, None, "fb")]
    else:
        plan = [(98304, "enabled", "reasoning"), (98304, "low", "fast")]
    last = None
    in_tok = out_tok = 0
    d = None                  # both retries may fail before assignment (quota wall)
    for max_tokens, thinking, mode in plan:
        for retry in range(2):
            try:
                d = _glm_call(prompt, max_tokens, thinking)
            except urllib.error.HTTPError as e:
                last = f"HTTP {e.code}: {e.read().decode()[:160]}"
                if e.code == 429:
                    time.sleep(25 * (retry + 1))
                else:
                    break
                continue
            except Exception as e:
                last = f"{type(e).__name__}: {e}"
                time.sleep(5)
                continue
        u = (d or {}).get("usage", {}) or {}
        in_tok += u.get("prompt_tokens", 0) or 0
        out_tok += u.get("completion_tokens", 0) or 0
        ch = ((d or {}).get("choices") or [{}])[0]
        content = (ch.get("message") or {}).get("content") or ""
        fin = ch.get("finish_reason")
        parsed = parse_json_loose(content)
        if parsed is not None and isinstance(parsed, dict) and "problems" in parsed:
            return parsed, {"in": in_tok, "out": out_tok, "mode": mode}

        # Diagnose WHY it failed, because the remedy differs sharply.
        #
        # Case A - thinking ate the whole budget: finish=length, content empty, and
        #   usage.completion_tokens_details.reasoning_tokens ~= max_tokens.
        #   Observed on the longest papers: 47,994 of 48,000 tokens were reasoning and
        #   ZERO content came back. Retrying the SAME mode is pure waste (two more
        #   paid calls that cannot succeed), so skip straight to the next mode.
        # Case B - content came back but did not parse: a transcription defect. This
        #   IS worth one immediate retry, because the model usually escapes correctly
        #   the second time (the failure is intermittent, not systematic).
        details = (u.get("completion_tokens_details") or {})
        reasoning_tok = details.get("reasoning_tokens", 0) or 0
        starved = (fin == "length") or (not content)
        if starved and reasoning_tok >= max_tokens * 0.9:
            last = (f"{mode}: thinking starved the budget "
                    f"(reasoning={reasoning_tok}/{max_tokens}, content={len(content)})")
            break                      # this mode cannot work; go to the next one
        if not parsed and content:
            last = f"{mode}: finish={fin} content_len={len(content)} parse failed"
            continue                   # intermittent escape defect - retry this mode
        last = f"{mode}: finish={fin} content_len={len(content)}"
        break                          # empty and not starved: retrying is pointless
    return None, {"error": last, "in": in_tok, "out": out_tok}


# ---------- storage ----------
SCHEMA = """
CREATE TABLE IF NOT EXISTS papers (
    arxiv_id TEXT PRIMARY KEY, journal TEXT, journal_name TEXT,
    crossref_doi TEXT, crossref_journal TEXT, pub_year INTEGER, match_method TEXT,
    title TEXT, authors_json TEXT, arxiv_journal_ref TEXT,
    latex_chars INTEGER, source_kind TEXT, fetch_status TEXT,
    extract_mode TEXT, tokens_in INTEGER, tokens_out INTEGER,
    extracted_at TEXT, error TEXT
);
CREATE TABLE IF NOT EXISTS problems (
    id TEXT PRIMARY KEY, arxiv_id TEXT, journal TEXT, pub_year INTEGER,
    original_quote TEXT, quote_location TEXT, self_contained TEXT,
    label TEXT, label_rationale TEXT, msc_primary TEXT, msc_secondary_json TEXT,
    difficulty_hint TEXT, uncertainty_notes TEXT, content_hash TEXT,
    paper_time_status TEXT, current_status TEXT, self_check TEXT,
    flag_for_human TEXT, related_note TEXT
);
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT, stage TEXT, detail TEXT,
    at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=60)
    # WAL + generous busy_timeout: multiple engine processes share this db.
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=60000")
    conn.executescript(SCHEMA)
    return conn


def save_paper(conn, cand, **kw):
    with _db_lock:
        conn.execute(
            "INSERT OR REPLACE INTO papers (arxiv_id, journal, journal_name, crossref_doi, "
            "crossref_journal, pub_year, match_method, title, authors_json, arxiv_journal_ref, "
            "latex_chars, source_kind, fetch_status, extract_mode, tokens_in, tokens_out, "
            "extracted_at, error) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (cand["arxiv_id"], cand["journal"], cand.get("journal_name") or cand["journal"], cand["crossref_doi"],
             cand.get("crossref_journal") or "", cand.get("pub_year") or cand.get("year") or 0,
             cand.get("match_method") or cand.get("id_source") or "",
             cand.get("crossref_title") or cand.get("title") or "", json.dumps(cand.get("authors", [])),
             cand.get("arxiv_journal_ref", ""),
             kw.get("latex_chars") or 0, kw.get("source_kind"), kw.get("fetch_status"),
             kw.get("extract_mode"), kw.get("tokens_in") or 0, kw.get("tokens_out") or 0,
             kw.get("extracted_at"), kw.get("error")))
        conn.commit()


def save_problems(conn, cand, probs):
    with _db_lock:
        for p in probs:
            quote = p.get("original_quote", "") or ""
            pid = "OP-" + hashlib.sha1(
                (cand["arxiv_id"] + "|" + quote[:300]).encode()).hexdigest()[:12].upper()
            chash = hashlib.sha256((cand["arxiv_id"] + quote).encode()).hexdigest()[:16]
            conn.execute(
                "INSERT OR REPLACE INTO problems (id, arxiv_id, journal, pub_year, original_quote, "
                "quote_location, self_contained, label, label_rationale, msc_primary, msc_secondary_json, "
                "difficulty_hint, uncertainty_notes, content_hash, paper_time_status, current_status, "
                "self_check, flag_for_human, related_note) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (pid, cand["arxiv_id"], cand["journal"], cand.get("pub_year") or cand.get("year") or 0, quote,
                 p.get("quote_location", ""), p.get("self_contained", ""), p.get("label", "uncertain"),
                 p.get("label_rationale", ""), p.get("msc_primary", ""),
                 json.dumps(p.get("msc_secondary", [])), p.get("difficulty_hint", ""),
                 p.get("uncertainty_notes", ""), chash, p.get("paper_time_status", ""),
                 p.get("current_status", "unknown"), p.get("self_check", ""),
                 p.get("flag_for_human", ""), p.get("related_note", "")))
        conn.commit()


def done_ids(conn):
    with _db_lock:
        return {r[0] for r in conn.execute(
            "SELECT arxiv_id FROM papers WHERE fetch_status='extracted'")}


# ---------- worker ----------
def process(conn, cand):
    aid = cand["arxiv_id"]
    tag = f"{aid}[{cand['journal']}]"
    try:
        text, kind = fetch_fulltext(aid)
    except Exception as e:
        log(f"  {tag} fulltext failed: {e}")
        save_paper(conn, cand, fetch_status="fulltext_failed", error=str(e)[:200])
        return 0, 0, 0, "failed"
    if text is None:
        log(f"  {tag} no fulltext")
        save_paper(conn, cand, fetch_status="no_fulltext")
        return 0, 0, 0, "no_fulltext"

    result, usage = llm_extract(cand, text)
    if result is None:
        log(f"  {tag} extract failed: {usage.get('error')}")
        save_paper(conn, cand, latex_chars=len(text), source_kind=kind,
                   fetch_status="extract_failed", error=str(usage.get("error"))[:200],
                   tokens_in=usage.get("in"), tokens_out=usage.get("out"))
        return 0, usage.get("in", 0), usage.get("out", 0), "failed"

    probs = result.get("problems", []) or []
    save_problems(conn, cand, probs)
    save_paper(conn, cand, latex_chars=len(text), source_kind=kind, fetch_status="extracted",
               extract_mode=usage.get("mode"), tokens_in=usage.get("in"),
               tokens_out=usage.get("out"), extracted_at=time.strftime("%Y-%m-%dT%H:%M:%S"))
    log(f"  {tag} -> {len(probs)} cards  ({len(text):,} chars via {kind}, mode={usage.get('mode')}, "
        f"in={usage.get('in')}, out={usage.get('out')})")
    return len(probs), usage.get("in", 0), usage.get("out", 0), "extracted"


def main():
    EXPORT_DIR.mkdir(exist_ok=True)
    if not CANDIDATES_JSON.exists():
        print("run harvest.py first")
        return
    cands = json.loads(CANDIDATES_JSON.read_text(encoding="utf-8"))
    conn = init_db()
    done = done_ids(conn)
    todo = [c for c in cands if c["arxiv_id"] not in done]

    # Cache-missing papers burn ~6-9 min each serialized on the arXiv lock
    # (server has no arXiv access; timeouts only). Push them to the END so
    # cached papers extract immediately; the lost-cause tail drains last.
    def _has_cache(c):
        stem = c["arxiv_id"].replace("/", "_")
        return ((LATEX_CACHE / f"{stem}.tex").exists()
                or (LATEX_CACHE / f"{stem}.ar5iv.txt").exists())

    todo.sort(key=lambda c: 0 if _has_cache(c) else 1)
    n_nocache = sum(1 for c in todo if not _has_cache(c))
    print(f"[pilot] cache-missing pushed to tail: {n_nocache}")

    if ENGINE_SLICE:
        i, n = (int(x) for x in ENGINE_SLICE.split("/"))
        todo = todo[i - 1::n]
        print(f"[pilot] engine slice {i}/{n} -> {len(todo)} papers "
              f"(flavor={ENGINE_FLAVOR}, model={GLM_MODEL})")
    print(f"[pilot] candidates={len(cands)} done={len(done)} todo={len(todo)} workers={WORKERS}")

    t0 = time.time()
    n_cards = n_in = n_out = 0
    status = {"extracted": 0, "no_fulltext": 0, "failed": 0}
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(process, conn, c): c for c in todo}
        for i, f in enumerate(as_completed(futs), 1):
            c = futs[f]
            try:
                cards, ti, to, st = f.result()
            except Exception as e:
                log(f"  {c['arxiv_id']} worker crashed: {type(e).__name__}: {e}")
                save_paper(conn, c, fetch_status="crashed", error=str(e)[:200])
                cards, ti, to, st = 0, 0, 0, "failed"
            n_cards += cards
            n_in += ti or 0
            n_out += to or 0
            status[st] = status.get(st, 0) + 1
            log(f"[{i}/{len(todo)}] {st}  elapsed={time.time()-t0:,.0f}s  cards={n_cards}")

    # ---- export
    cols = [c[1] for c in conn.execute("PRAGMA table_info(problems)")]
    rows = [dict(zip(cols, r)) for r in conn.execute("SELECT * FROM problems ORDER BY journal, id")]
    with open(EXPORT_DIR / "problems.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with _db_lock:
        conn.execute("INSERT INTO runs (stage, detail) VALUES (?,?)",
                     ("pilot_v3_complete",
                      f"candidates={len(cands)} {status} cards={n_cards} "
                      f"tokens_in={n_in} tokens_out={n_out} seconds={int(time.time()-t0)}"))
        conn.commit()
    # durable checkpoint line, so the record survives even without resume.py
    with open(BASE / "runs.log", "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} run_pilot candidates={len(cands)} "
                f"processed={len(todo)} {status} cards={n_cards} "
                f"tokens_in={n_in} tokens_out={n_out} seconds={int(time.time()-t0)}\n")
    print(f"\nDONE in {time.time()-t0:,.0f}s. cards={n_cards} status={status} "
          f"tokens in={n_in:,} out={n_out:,}")


if __name__ == "__main__":
    main()
