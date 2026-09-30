"""P1 S1.4: merge AI-judged bank + external consensus anchors (gold set) into
anchor_bank_v0 final. Zero API."""
import json, os
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
bank = [json.loads(l) for l in open(os.path.join(BASE, "anchor_bank_v0.jsonl"), encoding="utf-8")]
gold = json.load(open(os.path.join(BASE, "gold_set.json"), encoding="utf-8"))["items"]

# external consensus anchors: only I4/I5 famous (synthetic trivial ones stay out;
# they are calibration probes, not scale anchors)
ext = []
for g in gold:
    if g["synthetic"]:
        continue
    if g["tier"] in (4, 5):
        ext.append({"canonical_uid": f"EXT-{g['id']}", "tiers": {"public_consensus": g["tier"]},
                    "expected_tier": float(g["tier"]), "display_tier": g["tier"],
                    "stratum": "external", "msc": "?", "aliases": [],
                    "statement": g["statement"], "basis": g["basis"],
                    "source": "public_consensus"})
# dedupe: EXT anchor whose statement matches an AI-judged bank row is unlikely;
# keep both (EXT row marks the consensus ruler)
merged = bank + ext
with open(os.path.join(BASE, "anchor_bank_v0_final.jsonl"), "w", encoding="utf-8") as f:
    for r in merged:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

dist = Counter(r["display_tier"] for r in merged)
msc_top = Counter((r["msc"] or "?")[:2] for r in merged)
print(json.dumps({
    "total": len(merged),
    "ai_judged": len(bank),
    "external_consensus": len(ext),
    "tier_distribution": {f"I{k}": dist.get(k, 0) for k in range(1, 6)},
    "quota_check": {f"I{k}": "OK" if dist.get(k, 0) >= 8 else "SHORT" for k in range(1, 6)},
    "msc_top_categories_covered": len(msc_top),
}, ensure_ascii=False, indent=1))
