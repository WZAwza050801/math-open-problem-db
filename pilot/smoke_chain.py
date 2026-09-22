"""Smoke test the GLM key chain in run_pilot (coding endpoint, rotation)."""
import run_pilot as R

print("GLM_BASE:", R.GLM_BASE)
print("GLM_MODEL:", R.GLM_MODEL)
print("keys in chain:", len(R.GLM_KEYS), "prefixes:", [k[:8] + "..." for k in R.GLM_KEYS])
d = R._glm_call("Reply with exactly: CHAIN_OK", 2048, "enabled")
c = (d.get("choices") or [{}])[0].get("message", {}).get("content", "")
u = d.get("usage") or {}
print("reply:", repr(c))
print("usage:", u.get("prompt_tokens"), "in /", u.get("completion_tokens"), "out")
print("SMOKE_OK" if "CHAIN_OK" in c else "SMOKE_FAIL")
