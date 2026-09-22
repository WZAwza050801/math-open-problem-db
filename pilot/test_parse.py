"""Regression tests for parse_json_loose.

Each case states its own expectation, so a non-dict result is only a failure when
the case actually expected a dict. The previous version printed a hardcoded
"(expected None for truncated)" on the else-branch, which mislabelled every
non-dict outcome - the truncated case passes precisely BECAUSE it returns None.
"""
import sys

sys.path.insert(0, ".")
import run_pilot as rp

# (name, input, expect_dict)
CASES = [
    ("properly escaped", '{"a": "\\\\Sigma and \\\\ref{x}"}', True),
    ("UNESCAPED backslash (the real bug)", '{"a": "\\Sigma and \\ref{x}"}', True),
    ("raw newline inside string", '{"a": "line1\nline2"}', True),
    ("fenced json", '```json\n{"a": 1}\n```', True),
    ("prose before and after", 'Here you go:\n{"a": 1}\nHope that helps.', True),
    ("prose then unfenced json", 'Sure! {"a": 1}', True),
    # A truncated payload must NOT be salvaged into a half-populated card - that
    # would silently record a fragment as if it were the model's full answer.
    ("truncated - must return None", '{"problems": [{"original_quote": "abc', False),
    ("empty - must return None", "", False),
    ("prose only - must return None", "I cannot help with that.", False),
]

failed = 0
for name, s, expect_dict in CASES:
    r = rp.parse_json_loose(s)
    got_dict = isinstance(r, dict)
    ok = got_dict == expect_dict
    if not ok:
        failed += 1
    mark = "pass" if ok else "FAIL"
    want = "dict" if expect_dict else "None"
    got = repr(r.get("a")) if got_dict else "None"
    print(f"  [{mark}] {name:34} expected={want:4} got={got}")

print()
print(f"{len(CASES) - failed}/{len(CASES)} passed")
sys.exit(1 if failed else 0)
