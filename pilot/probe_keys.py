"""Probe which API endpoints respond, without ever hard-coding a credential.

Keys are read from the environment, falling back to the gitignored pilot/.env.
Template: pilot/.env.example. Run: python probe_keys.py
"""
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from run_pilot import load_env_file

BASE = Path(__file__).resolve().parent
# real environment wins over .env, same precedence as run_pilot.py
ENV = {**load_env_file(BASE / ".env"), **os.environ}


def key(name):
    v = ENV.get(name, "")
    if not v:
        print(f"[skip] {name} not set - export it or add it to pilot/.env")
    return v


def probe(name, base_url, api_key, model):
    if not api_key:
        return False
    url = base_url.rstrip("/") + "/chat/completions"
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "Reply with exactly: OK"}],
        "max_tokens": 10,
    }).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            d = json.load(resp)
            text = d["choices"][0]["message"]["content"]
            print(f"[{name}] 200 model={model} reply={text.strip()!r} usage={d.get('usage', {})}")
            return True
    except urllib.error.HTTPError as e:
        print(f"[{name}] HTTP {e.code} model={model} body={e.read().decode()[:300]}")
    except Exception as e:
        print(f"[{name}] ERR {type(e).__name__}: {e}")
    return False


# A: GLM Coding Plan key (the coding-plan endpoint, then the standard one)
glm = key("GLM_KEY")
for base, m in [("https://open.bigmodel.cn/api/coding/paas/v4", "glm-5.3"),
                ("https://open.bigmodel.cn/api/paas/v4", "glm-5.3")]:
    if probe("glm-codingplan", base, glm, m):
        break

# B: GLM resource-pack key (long-lived fallback)
probe("glm-resourcepack", "https://open.bigmodel.cn/api/paas/v4",
      key("GLM_RESOURCEPACK_KEY"), "glm-5-turbo")

# C: DeepSeek cheap backup
probe("deepseek", "https://api.deepseek.com",
      key("DEEPSEEK_API_KEY"), "deepseek-chat")
