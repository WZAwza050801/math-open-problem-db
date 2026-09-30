# Dump local kimi extraction results for server merge (LF, utf-8)
import json
import sqlite3

# Only export papers the server has NOT already extracted (delta merge).
conn = sqlite3.connect("db.sqlite3")
conn.row_factory = sqlite3.Row

import json
import subprocess

SRV = subprocess.run(
    ["ssh", "node01",
     "cd /home/user/Wholeworks/wanganan/math_openproblem/pilot"
     " && python3 -c \"import sqlite3;"
     " con=sqlite3.connect('db.sqlite3');"
     " [print(r[0]) for r in con.execute("
     "\\\"select arxiv_id from papers where fetch_status='extracted'\\\")]\""],
    capture_output=True, text=True, timeout=120)
srv_ids = set(SRV.stdout.split())

papers = [dict(r) for r in conn.execute(
    "select * from papers where fetch_status='extracted'"
    ) if dict(r)["arxiv_id"] not in srv_ids]
ids = [p["arxiv_id"] for p in papers]

problems = []
qmarks = ",".join("?" * len(ids))
for r in conn.execute(
        f"select * from problems where arxiv_id in ({qmarks})", ids):
    problems.append(dict(r))

data = {"papers": papers, "problems": problems}
with open("exports/local_kimi_merge.json", "w", encoding="utf-8",
          newline="\n") as f:
    json.dump(data, f, ensure_ascii=False)

print(f"exported papers={len(papers)} cards={len(problems)}")
