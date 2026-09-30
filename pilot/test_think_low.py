"""Verify thinking='low' works on the coding endpoint and yields parseable JSON."""
import json
import run_pilot as R

d = R._glm_call(
    'List 3 famous open problems in analytic number theory as strict JSON array: '
    '[{"idx":1,"problem_name":"...","depends_on":["..."]}]. No markdown, no prose.',
    4000, "low")
msg = (d.get("choices") or [{}])[0].get("message", {})
u = d.get("usage") or {}
det = (u.get("completion_tokens_details") or {})
print("finish:", (d.get("choices") or [{}])[0].get("finish_reason"))
print("content_head:", repr((msg.get("content") or "")[:200]))
print("reasoning_tokens:", det.get("reasoning_tokens"), "content_tokens:",
      (u.get("completion_tokens") or 0) - (det.get("reasoning_tokens") or 0))
try:
    arr = json.loads(msg["content"][msg["content"].index("["):msg["content"].rindex("]") + 1])
    print("PARSED_OK items:", len(arr))
except Exception as e:
    print("PARSE_FAIL:", e)
