#!/bin/bash
# usage: engine.sh <name> <workers>   (marker arg --engine lets pgrep find us)
NAME=$1; WORKERS=$2
cd /home/user/Wholeworks/wanganan/math_openproblem/pilot || exit 1
if [ "$NAME" = "glm" ]; then
  export GLM_BASE_URL="https://open.bigmodel.cn/api/coding/paas/v4"
  export GLM_MODEL="glm-5.3"
  export ENGINE_FLAVOR="glm"
  export ENGINE_SLICE="1/4"
  export GLM_KEYS="37cf5d59d7ad41129fbea36bcd40e4b0.luBRDLDKa8LSFExD"
elif [ "$NAME" = "qwen" ]; then
  export GLM_BASE_URL="https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  export GLM_MODEL="qwen3.8-max"
  export ENGINE_FLAVOR="openai"
  export ENGINE_SLICE="2/4"
  export GLM_KEYS="sk-sp-H.DHIMLP.S4LQ.MEYCIQDCcz20ZdU6VE8ZNR6J3lmgq0nBNw2VMA7se-kgwGpnUgIhAL_2OZUwqQ7qLCcmwTVkLwE5M9mR5-jbfNM7meGT2rM1"
elif [ "$NAME" = "lite" ]; then
  export GLM_BASE_URL="https://open.bigmodel.cn/api/coding/paas/v4"
  export GLM_MODEL="glm-5.3"
  export ENGINE_FLAVOR="glm"
  export ENGINE_SLICE="4/4"
  export GLM_KEYS="6395f31e8c2d4d94bf1a1444220b3a56.v5trDkh4nJg06DMn"
else
  echo unknown engine $NAME; exit 1
fi
export PILOT_WORKERS=$WORKERS
exec python3 -u run_pilot.py --engine "$NAME" >> run_${NAME}.log 2>\&1
