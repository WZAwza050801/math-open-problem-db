"""Controlled experiment: which request header combination passes arXiv /src/?

Waits for the IP rate-limit to lift, then tests header variants one at a time
with generous spacing so each result is clean.
"""
import time, urllib.request, urllib.error

TEST_ID = "2302.11922"
URL = f"https://arxiv.org/src/{TEST_ID}"

CHROME = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"

VARIANTS = [
    ("A: UA=Mozilla/5.0 only", {"User-Agent": "Mozilla/5.0"}),
    ("B: full Chrome UA, no Accept", {"User-Agent": CHROME}),
    ("C: full Chrome UA + Accept */*", {"User-Agent": CHROME, "Accept": "*/*"}),
    ("D: no headers at all", {}),
]


def try_once(headers):
    try:
        req = urllib.request.Request(URL, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, len(r.read())
    except urllib.error.HTTPError as e:
        return e.code, 0
    except Exception as e:
        return f"{type(e).__name__}: {e}", 0


print("waiting for rate limit to lift (max 12 min)...", flush=True)
for i in range(10):
    code, n = try_once({"User-Agent": "Mozilla/5.0"})
    print(f"  probe {i+1}: {code} len={n}", flush=True)
    if code == 200:
        break
    time.sleep(70)
else:
    print("never recovered, aborting", flush=True)
    raise SystemExit(1)

for name, hdrs in VARIANTS:
    code, n = try_once(hdrs)
    print(f"[{name}] -> {code} len={n}", flush=True)
    time.sleep(25)

print("done", flush=True)
