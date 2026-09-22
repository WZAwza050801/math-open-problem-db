"""Test: do requests for DIFFERENT paper ids (uncached, origin-served) trigger 406?"""
import time, urllib.request, urllib.error

IDS = ["2403.04774", "2307.02749", "2306.03909", "2302.11922", "2310.11871"]
HDRS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"}

def try_id(aid, gap=20):
    t0 = time.time()
    try:
        req = urllib.request.Request(f"https://arxiv.org/src/{aid}", headers=HDRS)
        with urllib.request.urlopen(req, timeout=120) as r:
            d = r.read()
            print(f"  {aid}: {r.status} len={len(d)} ({time.time()-t0:.1f}s)", flush=True)
            return True
    except urllib.error.HTTPError as e:
        print(f"  {aid}: HTTP {e.code} ({time.time()-t0:.1f}s)", flush=True)
        return e.code != 406
    except Exception as e:
        print(f"  {aid}: {type(e).__name__} {e}", flush=True)
        return False

for i, aid in enumerate(IDS):
    try_id(aid)
    if i < len(IDS) - 1:
        time.sleep(20)
print("done", flush=True)
