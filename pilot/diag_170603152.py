"""Diagnose the persistent extract failure on 1706.03152.

We lost paid attempts to `finish=stop content_len=30036`: the model DID return content
but our parser rejected it. This re-runs the SAME call with the SAME prompt, saves the
raw content, and reports exactly why parse_json_loose failed - so we fix the real cause
instead of guessing.
"""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
import run_pilot as R

ARXIV_ID = "1706.03152"
OUT = BASE / "diag_last_content.txt"


def main():
    cands = json.loads((BASE / "candidates.json").read_text(encoding="utf-8"))
    cand = next(c for c in cands if str(c.get("arxiv_id")) == ARXIV_ID)
    print("journal:", cand.get("journal_name"), "| year:", cand.get("pub_year"))

    tex = R.LATEX_CACHE / f"{ARXIV_ID}.tex"
    fulltext = tex.read_text(encoding="utf-8", errors="replace")
    print(f"fulltext chars: {len(fulltext):,}")
    src = R.truncate_source(fulltext)
    print(f"after truncate: {len(src):,}")

    prompt = (R.EXTRACT_PROMPT
              .replace("{title}", cand["crossref_title"])
              .replace("{authors}", ", ".join(cand.get("authors", [])[:6]))
              .replace("{journal}", cand["journal_name"])
              .replace("{year}", str(cand["pub_year"]))
              .replace("{arxiv_id}", cand["arxiv_id"])
              .replace("{latex}", src))
    print(f"prompt chars: {len(prompt):,}")

    plan = [(48000, "enabled", "reasoning"), (32000, "disabled", "fast")]
    for max_tokens, thinking, mode in plan:
        print(f"\n=== mode={mode} thinking={thinking} max_tokens={max_tokens} ===")
        try:
            resp = R._glm_call(prompt, max_tokens, thinking)
        except Exception as e:
            print("  call error:", type(e).__name__, str(e)[:200])
            continue
        ch = (resp.get("choices") or [{}])[0]
        content = (ch.get("message") or {}).get("content") or ""
        fin = ch.get("finish_reason")
        print(f"  finish={fin} content_len={len(content)} usage={resp.get('usage')}")
        OUT.write_text(content, encoding="utf-8")
        print(f"  raw saved -> {OUT}")

        parsed = R.parse_json_loose(content)
        print("  parse_json_loose ->", "OK" if parsed else "None")
        if parsed:
            print("  keys:", list(parsed)[:8])
            break
        print("  HEAD:", repr(content[:250]))
        print("  TAIL:", repr(content[-250:]))
        try:
            json.loads(content)
            print("  stdlib json.loads: OK -> parse_json_loose has a bug")
        except Exception as e:
            print("  stdlib json error:", e)
            pos = getattr(e, "pos", None)
            if pos is not None:
                print("  near error:", repr(content[max(0, pos - 150):pos + 150]))


if __name__ == "__main__":
    main()
