# GLM Key 台账与分配策略

> 更新：2026-09-27 02:00 GMT+8
> 明文密钥只存在 `pilot/.env`（本机+服务器，gitignore/600）和用户的密码书。本文件只记前缀和策略。

## 一、Key 清单（实测 2026-09-27 凌晨）

| 名称 | 前缀 | 套餐 | 额度 | 状态 |
|---|---|---|---|---|
| **team2** | `955ac1ff` | 团队席位（Coding Plan）**新开** | 待实测（15,000/5h + 66,000/周 级别？） | ✅ 2026-09-27 实测 coding 端点 glm-5.3 / 5.3-flash 双通；**裁决链首位**；已入本机+服务器 .env（GLM_CODING_TEAM2_KEY） |
| team | `884fd568` | 团队席位（Coding Plan） | 15,000 积分/5h + 66,000/周 | ⛔ 1310 周上限，2026-09-29 08:05:49 重置；重置后回归链第二位 |
| lite | `6395f31e` | 个人 Lite（Coding Plan） | 2,000 积分/5h + 10,000/周 | ⛔ 1310 周上限，2026-09-30 09:40 重置 |
| resourcepack | `7b3e8bd5` | 资源包（按量扣减） | 未知余额 | ⏸ 备用，仅用户明确批准才动 |
| 旧团队版 | `37cf5d59` | Coding Plan 团队版 | — | ❌ 2026-09-18 到期；**2026-09-27 实测 401 令牌过期**（用户误以为可用，已核实作废） |

### 服务器裁决链当前顺序（canon_judge.py）
team2（有量，现役）→ team（9/29 重置）→ lite（9/30 重置）→ Token Plan qwen3.8-max → SF Kimi-K2.6

## 二、端点铁律

- **只准走** `https://open.bigmodel.cn/api/coding/paas/v4`（扣套餐积分）
- **绝不走** `https://open.bigmodel.cn/api/paas/v4`（扣账户余额，按量计费）
- `run_pilot.py` 的 `GLM_BASE` 已钉死在 coding 端点，可用 `GLM_BASE_URL` 环境变量覆盖（覆盖时须自知后果）
- 实测确认：coding 端点额度耗尽**不会**自动转按量扣费，只会报错——这正是想要的失败模式

## 三、实测矩阵（keymatrix.json 为原始数据）

| key | 端点 | glm-5.3 | glm-5.3-flash | glm-5.3-flashx |
|---|---|---|---|---|
| lite | coding | ✅ 2.0s | ✅ 1.8s | ❌ 1311 套餐未开放 |
| lite | paas | ⚠️ 通（烧试用/余额） | ⚠️ 通 | ✅（勿用） |
| team | coding | ✅ 3.1s | ✅ 2.6s | ❌ 1311 |
| team | paas | ❌ 1113 | ❌ 1113 | ❌ 1311 |

**flashx 两个套餐都没权限，出局。**

## 四、积分换算与全量跑批账本

单篇实测消耗 ≈ 91k 输入 + 41k 输出（含思考 token）：

| 模型 | 峰值积分/篇 | 非峰值（五折）/篇 |
|---|---|---|
| glm-5.3 | ≈161 | ≈80.6 |
| glm-5.3-flash | ≈54 | ≈27 |

非高峰 = 工作日 14:00–18:00 (UTC+8) 之外的**全部时段**。

**全量 823 篇 @ glm-5.3（非高峰）≈ 66,300 积分**，两池周额度合计 76,000 →
**理论上一周内可零现金成本磨完全量**，前提：
- 全程非高峰时段跑（工作日白天 14-18 点停或烧得贵一倍）
- 5 小时窗口节奏：team 窗口 ≈186 篇，lite 窗口 ≈24 篇

## 五、分配策略（已实装进 run_pilot.py）

1. **抽取主任务（全量）**：`glm-5.3` @ coding 端点——试跑 377 卡 / 99.5% 可核验率就是这个模型，质量不冒险
2. **Key 链**：`GLM_KEYS` 环境变量 > `GLM_KEY` > `.env` 的 lite+team。额度耗尽（429 + 1113/1311/1302/额度/资源包 签名）自动轮换下一把，**链里没有任何按量 key**，结构上烧不到余额
3. **Flash 用途**：等未来的轻任务（MSC 预标注、去重预筛这类不怕错的活）；若要用于抽取，必须先 A/B 十篇对比可核验率
4. **降级底线**：两个池子同时见底 → 停机等重置；只有用户明确批准才允许动 `GLM_RESOURCEPACK_KEY`（且须走 paas 端点 + 换 GLM_BASE_URL）

## 六、风险备注

- Coding Plan 条款面向"编程/智能体工具交互式使用"，批量抽取属灰色地带；key 是用户自己的，决策权在用户
- 服务器跑批时两把 key 都要用环境变量注入（`export GLM_KEYS=...`），不要落到服务器磁盘明文（或放服务器端 600 权限的 .env）

| qianfan | `bce-v3/ALTAKSP` | 百度千帆 Token Plan（个人） | 见下 | ✅ **2026-09-29 修复**：此 key 是 Token Plan 个人版专属 key，**只能走专属端点** `https://qianfan.baidubce.com/v2/tokenplan/personal/chat/completions`（普通 `/v2/chat/completions` 一律 401 `token_plan_person_api_key_not_allowed`）。专属端点实测 deepseek-v4-pro 双通（OpenAI 兼容协议）。注意 Token Plan 个人版模型阵容与常规千帆不同（glm-5.3 在列；kimi-k2.6 已于 2026-09-29 下线）。key 存 pilot/.qianfan_key + .env(QIANFAN_API_KEY)，服务器副本 .qianfan_key(600) |
