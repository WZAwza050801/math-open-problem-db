"""Probe whether arXiv /src/ rate-limit has lifted. Waits and retries."""
import time, urllib.request, urllib.error

TEST_ID = "2302.11922"
HDRS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36"}

for i in range(12):
    try:
        req = urllib.request.Request(f"https://arxiv.org/src/{TEST_ID}", headers=HDRS)
        with urllib.request.urlopen(req, timeout=60) as r:
            d = r.read()
            print(f"attempt {i+1}: RECOVERED 200 len={len(d)}", flush=True)
            raise SystemExit(0)
    except urllib.error.HTTPError as e:
        print(f"attempt {i+1}: HTTP {e.code} still limited", flush=True)
    except Exception as e:
        print(f"attempt {i+1}: {type(e).__name__} {e}", flush=True)
    time.sleep(75)

print("STILL LIMITED after 12 attempts", flush=True)
