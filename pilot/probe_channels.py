"""Probe the arXiv full-text channels to find out what 406 actually means.

Earlier we concluded "per-paper-id cooldown", but the v3 run got a 406 on its very
first, never-before-requested id -- so that diagnosis was wrong. Here we test, with
polite spacing, several endpoints and header sets against both a fresh id and one
that succeeded minutes ago.
"""
from __future__ import annotations

import time
import urllib.error
import urllib.request

RESEARCH_UA = {"User-Agent": "open-problem-db-pilot/0.1 (research; contact: local)"}
BROWSER_UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/131.0 Safari/537.36",
    "Accept": "*/*",
}
FULL_BROWSER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/131.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://arxiv.org/",
    "Connection": "keep-alive",
}

FRESH = "2303.15347"      # never requested before today
KNOWN = "2503.20277"      # fetched successfully live earlier today

TRIALS = [
    (FRESH, "https://arxiv.org/abs/{id}", RESEARCH_UA, "abs page (site reachability)"),
    (FRESH, "https://arxiv.org/src/{id}", BROWSER_UA, "src + browser UA"),
    (FRESH, "https://arxiv.org/src/{id}", RESEARCH_UA, "src + research UA"),
    (FRESH, "https://arxiv.org/src/{id}", FULL_BROWSER, "src + full browser headers"),
    (FRESH, "https://arxiv.org/e-print/{id}", BROWSER_UA, "e-print + browser UA"),
    (FRESH, "https://export.arxiv.org/e-print/{id}", BROWSER_UA, "export mirror e-print"),
    (FRESH, "https://arxiv.org/pdf/{id}", BROWSER_UA, "pdf + browser UA"),
    (KNOWN, "https://arxiv.org/src/{id}", BROWSER_UA, "src of an id that worked earlier"),
    (FRESH, "https://arxiv.org/html/{id}v1", BROWSER_UA, "official arXiv HTML"),
    (FRESH, "https://ar5iv.labs.arxiv.org/html/{id}", BROWSER_UA, "ar5iv HTML"),
]

GAP = 8


def probe(aid, tmpl, headers, label):
    url = tmpl.format(id=aid)
    req = urllib.request.Request(url, headers=headers)
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read(400_000)
            kind = "PDF" if data[:5] == b"%PDF-" else ("gzip/tar" if data[:2] == b"\x1f\x8b" else "text")
            ct = r.headers.get("Content-Type", "")
            print(f"  {label:38} {r.status}  {len(data):>8,}B  {ct[:34]:34} {kind}")
            return
    except urllib.error.HTTPError as e:
        body = e.read()[:120].decode("utf-8", "replace").replace("\n", " ")
        print(f"  {label:38} HTTP {e.code}  {e.headers.get('Retry-After') or ''}  {body[:70]}")
    except Exception as e:
        print(f"  {label:38} {type(e).__name__}: {e}")
    finally:
        print(f"  {'':38} ({time.time()-t:.1f}s)")


def main():
    for i, (aid, tmpl, headers, label) in enumerate(TRIALS, 1):
        print(f"[{i}/{len(TRIALS)}] {aid}")
        probe(aid, tmpl, headers, label)
        if i < len(TRIALS):
            time.sleep(GAP)


if __name__ == "__main__":
    main()
