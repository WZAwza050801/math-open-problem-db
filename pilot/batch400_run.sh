#!/bin/bash
# batch400_run.sh — launch extraction for batch400 on node01, 2 engine slices.
cd /home/user/Wholeworks/wanganan/math_openproblem/pilot || exit 1

# 1) filter candidates to those with local fulltext (server has no arXiv egress)
python3 - << 'EOF'
import json, os
cands = json.load(open('batch400.json', encoding='utf-8'))
keep = []
for c in cands:
    stem = c['arxiv_id'].replace('/', '_')
    if os.path.exists(f'latex_cache/{stem}.tex') or os.path.exists(f'latex_cache/{stem}.ar5iv.txt'):
        keep.append(c)
json.dump(keep, open('batch400_server.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('server batch:', len(keep), '/', len(cands))
EOF

GLM_KEY=$(grep -A5 'NAME" = "glm"' engine.sh | grep GLM_KEYS | cut -d= -f2- | tr -d '"')
QWEN_KEY=$(grep -A5 'NAME" = "qwen"' engine.sh | grep GLM_KEYS | cut -d= -f2- | tr -d '"')
export CANDIDATES_JSON_PATH="$PWD/batch400_server.json"

# 2) GLM slice 1/2
GLM_BASE_URL="https://open.bigmodel.cn/api/coding/paas/v4" \
GLM_MODEL="glm-5.3" ENGINE_FLAVOR="glm" ENGINE_SLICE="1/2" \
GLM_KEYS="$GLM_KEY" PILOT_WORKERS=2 \
nohup python3 -u run_pilot.py >> logs/batch400_glm.log 2>&1 &
echo "glm pid $!"

# 3) Qwen slice 2/2
GLM_BASE_URL="https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1" \
GLM_MODEL="qwen3.8-max" ENGINE_FLAVOR="openai" ENGINE_SLICE="2/2" \
GLM_KEYS="$QWEN_KEY" PILOT_WORKERS=2 \
nohup python3 -u run_pilot.py >> logs/batch400_qwen.log 2>&1 &
echo "qwen pid $!"
