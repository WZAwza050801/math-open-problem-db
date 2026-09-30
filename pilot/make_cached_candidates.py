"""Build a server candidates list containing ONLY papers with cached fulltext."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
cands = json.loads((BASE / "candidates.json").read_text(encoding="utf-8"))
have = {p.stem for p in (BASE / "latex_cache").glob("*.tex")}
sub = [c for c in cands if c["arxiv_id"].replace("/", "_") in have]
(BASE / "candidates_cached.json").write_text(
    json.dumps(sub, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"total={len(cands)} cached={len(sub)} missing={len(cands) - len(sub)}")
