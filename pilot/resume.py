"""One-command resume. Safe to run repeatedly -- every stage is idempotent.

  python resume.py            full chain: fetch -> extract -> report -> validate
  python resume.py --quick    skip the report/validate step

What "resumable" means here:
  * harvest.py writes candidates.json (Crossref-verified); regenerate with --refresh-toc
    only when you want a fresh corpus.
  * run_pilot.py skips any paper already marked fetch_status='extracted', so re-running
    it retries exactly the pending/failed ones. Full texts live in latex_cache/ and are
    reused, so a resume costs LLM calls only.
  * problem ids are derived from (arxiv_id + quote) content, so re-extracting a paper
    overwrites its own rows instead of duplicating or clobbering other papers' rows.
  * every run appends to runs.log and to the `runs` table.

Long jobs: start it in the background and check back with `python status.py`.
"""
from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
PY = sys.executable
LOG = BASE / "runs.log"


def sh(script, env_note=None):
    print(f"\n{'=' * 70}\n>>> {script} {env_note or ''}\n{'=' * 70}", flush=True)
    t0 = time.time()
    rc = subprocess.call([PY, "-u", str(BASE / script)], cwd=str(BASE))
    dt = time.time() - t0
    print(f"<<< {script} exit={rc} in {dt:.0f}s", flush=True)
    return rc, dt


def snapshot():
    db = BASE / "db.sqlite3"
    if not db.exists():
        return "no db yet"
    conn = sqlite3.connect(db)
    p = dict(conn.execute("SELECT fetch_status, COUNT(*) FROM papers GROUP BY 1").fetchall())
    cards = conn.execute("SELECT COUNT(*) FROM problems").fetchone()[0]
    return f"papers={p} cards={cards}"


def main():
    quick = "--quick" in sys.argv
    started = time.strftime("%Y-%m-%dT%H:%M:%S")
    print(f"resume run started {started}")
    print(f"before: {snapshot()}")

    log_lines = [f"\n### resume {started}", f"before: {snapshot()}"]

    # 1. candidates must exist
    if not (BASE / "candidates.json").exists():
        rc, _ = sh("harvest.py")
        log_lines.append(f"harvest.py exit={rc}")

    # 2. fetch + extract (resumable; retries failures automatically)
    rc, dt = sh("run_pilot.py")
    log_lines.append(f"run_pilot.py exit={rc} {dt:.0f}s")

    if not quick:
        rc, _ = sh("make_review.py")
        log_lines.append(f"make_review.py exit={rc}")
        rc, _ = sh("validate_cards.py")
        log_lines.append(f"validate_cards.py exit={rc}")

    log_lines.append(f"after: {snapshot()}")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")

    print(f"\nafter: {snapshot()}")
    print(f"log appended to {LOG}")


if __name__ == "__main__":
    main()
