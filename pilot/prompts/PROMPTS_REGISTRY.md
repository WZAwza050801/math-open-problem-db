# 提示词档案（PROMPT REGISTRY）

> **建立** 2026-10-01。**这是什么**：项目所有送 AI 的提示词的版本化户口本。
> **为什么强制**（用户 2026-10-01 拍板）：未来任何实验都要完整记录"用哪家 API + 哪版提示词"，
> 让每条 AI 产出都能追责到具体模型——提示词改动就是换了一个实验条件，不许悄悄发生。
> **规矩**：
> 1. 提示词正文一律存本目录 `名字_v版本.txt`，**改一个字就升版本号、算新文件**，旧版永不删；
> 2. 每个调用该提示词的脚本必须在产出里记 `prompt_sha256`（本目录文件 sha256 前 16 位）；**口径 = 文本模式读取（UTF-8、换行归一 LF）再哈希**，与脚本实现一致，避免 Windows CRLF 造成双口径；
> 3. 产出台账（EXPERIMENT_REGISTRY）的实验卡片写明"用哪版提示词"；
> 4. 模型责任标注：verdict/attempt 行内记 vendor + model + endpoint + prompt_sha256 四件套。

## 现行版本

| 文件 | sha256[:16] | 用途 | 调用脚本 | 引擎 |
|---|---|---|---|---|
| `influence_judge_v1.txt` | f2ec5dadee3a947c | 引用影响力一审/二审四档判定 | `influence_verdict.py`（及 retest 变体） | 智谱 glm-5.3 / 千帆 deepseek-v4-pro |
| `influence_arbiter_doubao_v1.txt` | 62ff43f63fbaed07 | 第三引擎仲裁（tie-break 提示，含分歧说明） | `influence_arbiter_doubao.py`（本机变体 `_local.py`） | 火山 doubao-seed-2-1-pro-260628 |
| `influence_final_v2.txt` | 0c96c647ee4d09a7 | **旗舰终审**（复合条件：完整证据 + 三家判官档位与理由 + 要求先点名分歧 crux 再裁决 + 保守倾向 D） | `influence_final_adjudication.py`（引擎无关，参数走环境变量） | 待定：micu GPT-5.6 / modcon Fable / kimi k3（见下） |

## 终审引擎选型（2026-10-01 拍板中）

**原则**：国内引擎尽量走 Coding Plan（零现金）；按量海外旗舰只用于终审（约几百对，花费可控）。

| 候选 | 供应商亲缘 | 计费 | 实测 | 备注 |
|---|---|---|---|---|
| micu · GPT-5.6 | 无（海外） | 按量（密码书） | ⏸ 待用户抄 base URL/key/模型名 | 用户点名首选 |
| modcon · Fable 系列 | 无（海外） | 按量（密码书） | ⏸ 同上 | 用户点名备选 |
| kimi k3（官方 coding 端点 api.kimi.com，模型名 `k3`） | 无（月之暗面，与智谱/千帆/火山都无亲缘） | **Coding Plan 套餐内，零现金** | ✅ 2026-10-01 探测通过 | 国产首选替补 |
| 智谱资源包 glm-5.3/4.6（paas 端点） | ⚠️ 与一审 glm-5.3 同家族 | 按量 | ✅ 探测通过 | 仅作兜底（同家族有偏袒嫌疑，责任标注会显式记这一点） |
| DeepSeek 官方 v4-pro | ⚠️ 与二审 deepseek 同家族 | 按量 | ✅ 探测通过 | 同上 |

**亲缘纪律**：终审引擎优先选与三个判官（智谱/千帆/火山）都无供应商亲缘的；被迫用同家族引擎时，
verdict 行的责任标注必须写明 `kinship_warning`，下游统计可见该批终审有家族偏差风险。
