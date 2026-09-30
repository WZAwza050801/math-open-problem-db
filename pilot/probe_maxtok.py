"""Probe GLM-5.3 max accepted max_tokens on the coding endpoint."""
import json
import run_pilot as R

for cap in (98304, 81920):
    body = {"model": R.GLM_MODEL,
            "messages": [{"role": "user", "content": "Reply with exactly: OK"}],
            "max_tokens": cap, "temperature": 0.1, "thinking": {"type": "low"}}
    req = R.urllib.request.Request(
        R.GLM_BASE.rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": "Bearer " + R.GLM_KEYS[0], "Content-Type": "application/json"})
    try:
        with R.urllib.request.urlopen(req, timeout=120) as resp:
            d = json.load(resp)
        u = d.get("usage") or {}
        print(f"cap={cap}: ACCEPTED, finish={(d.get('choices') or [{}])[0].get('finish_reason')}, "
              f"completion={u.get('completion_tokens')}")
        break
    except R.urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", "replace")[:150]
        except Exception:
            pass
        print(f"cap={cap}: HTTP {e.code} {detail}")
