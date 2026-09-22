"""Test matrix: 2 Coding Plan keys x endpoints x models. NO secrets printed.

Matrix:
  keys:    GLM_CODING_LITE_KEY, GLM_CODING_TEAM_KEY (from .env)
  endpoints: coding (/api/coding/paas/v4), paas (/api/paas/v4)
  models:  glm-5.3, glm-5.3-flash, glm-5.3-flashx

Each cell = one tiny request (max_tokens=2048, thinking enabled -- 5.3 forces it).
Result rows go to stdout AND pilot/keymatrix.json for the ledger.

Usage: python test_key_matrix.py
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent

ENV = {}
for raw in (BASE / ".env").read_text(encoding="utf-8").splitlines():
    line = raw.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, _, v = line.partition("=")
    ENV[k.strip()] = v.strip().strip('"').strip("'")

KEYS = {
    "lite": ENV.get("GLM_CODING_LITE_KEY", ""),
    "team": ENV.get("GLM_CODING_TEAM_KEY", ""),
}
ENDPOINTS = {
    "coding": "https://open.bigmodel.cn/api/coding/paas/v4/chat/completions",
    "paas":   "https://open.bigmodel.cn/api/paas/v4/chat/completions",
}
MODELS = ["glm-5.3", "glm-5.3-flash", "glm-5.3-flashx"]


def call(url, key, model, timeout=90):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "Reply with exactly: OK"}],
        "max_tokens": 2048,
        "thinking": {"type": "enabled"},
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    })
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.load(r)
        dt = time.time() - t0
        u = d.get("usage") or {}
        det = (u.get("completion_tokens_details") or {})
        return {
            "status": "OK", "ms": int(dt * 1000),
            "finish": (d.get("choices") or [{}])[0].get("finish_reason"),
            "content": ((d.get("choices") or [{}])[0].get("message") or {}).get("content", "")[:40],
            "prompt_tokens": u.get("prompt_tokens"),
            "completion_tokens": u.get("completion_tokens"),
            "reasoning_tokens": det.get("reasoning_tokens"),
        }
    except urllib.error.HTTPError as e:
        dt = time.time() - t0
        try:
            detail = e.read().decode("utf-8", "replace")[:300]
        except Exception:
            detail = ""
        return {"status": f"HTTP {e.code}", "ms": int(dt * 1000), "detail": detail}
    except Exception as e:
        return {"status": f"{type(e).__name__}", "ms": int((time.time() - t0) * 1000),
                "detail": str(e)[:200]}


def main():
    rows = []
    for kname, key in KEYS.items():
        if not key:
            print(f"[skip] {kname}: no key")
            continue
        for ename, url in ENDPOINTS.items():
            for model in MODELS:
                r = call(url, key, model)
                row = {"key": kname, "endpoint": ename, "model": model, **r}
                rows.append(row)
                print(json.dumps(row, ensure_ascii=False), flush=True)
                time.sleep(2)
    (BASE / "keymatrix.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nwrote keymatrix.json", flush=True)


if __name__ == "__main__":
    main()
