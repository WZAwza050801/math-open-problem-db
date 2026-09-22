import urllib.request, urllib.error, gzip, io, json

TEST_ID = "2302.11922"

VARIANTS = [
    ("e-print plain", f"https://arxiv.org/e-print/{TEST_ID}", {}),
    ("e-print +UA", f"https://arxiv.org/e-print/{TEST_ID}", {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36"}),
    ("e-print +Accept*", f"https://arxiv.org/e-print/{TEST_ID}", {"User-Agent": "Mozilla/5.0", "Accept": "*/*"}),
    ("src endpoint", f"https://arxiv.org/src/{TEST_ID}", {"User-Agent": "Mozilla/5.0"}),
    ("export mirror", f"https://export.arxiv.org/e-print/{TEST_ID}", {"User-Agent": "Mozilla/5.0"}),
    ("pdf", f"https://arxiv.org/pdf/{TEST_ID}", {"User-Agent": "Mozilla/5.0"}),
]

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, msg + " -> " + newurl, headers, fp)

opener = urllib.request.build_opener(NoRedirect)

for name, url, headers in VARIANTS:
    try:
        req = urllib.request.Request(url, headers=headers)
        with opener.open(req, timeout=60) as r:
            data = r.read()
            ct = r.headers.get("Content-Type", "")
            print(f"[{name}] {r.status} len={len(data)} ct={ct} head={data[:8]!r}")
    except urllib.error.HTTPError as e:
        loc = e.headers.get("Location", "") if e.headers else ""
        print(f"[{name}] HTTP {e.code} {e.reason} loc={loc}")
    except Exception as e:
        print(f"[{name}] ERR {type(e).__name__}: {e}")
