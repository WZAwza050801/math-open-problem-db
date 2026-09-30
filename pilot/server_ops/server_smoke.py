import run_pilot as R

print("GLM_BASE:", R.GLM_BASE)
print("GLM_MODEL:", R.GLM_MODEL)
print("keys:", len(R.GLM_KEYS), [k[:8] + "..." for k in R.GLM_KEYS])
d = R._glm_call("Reply with exactly: SERVER_CHAIN_OK", 2048, "enabled")
c = (d.get("choices") or [{}])[0].get("message", {}).get("content", "")
print("reply:", repr(c))
print("SERVER_SMOKE_OK" if "SERVER_CHAIN_OK" in c else "SERVER_SMOKE_FAIL")
