# 命名规范（2026-09-30 定稿，立即生效）

> 配套文档：`ASSET_REGISTRY_2026-09-30.md`（资产注册表，代号对照表在其附录 A）。
> **动因**：项目内曾用内部代号命名管线与文件（M13、P5、nap、canon、s2、nb8、E1…），外人无法从名字
> 理解任何东西，且已实际造成误用风险（旧目标集误用、监控盯错日志）。本规范终结这一习惯。

---

## 一、铁律（1-6 为 2026-09-30 首批，7-8 为后续拍板追加）

1. **语义命名公式**：`对象_性质_版本或日期`。
   - 对象：`problem_card` / `canonical_problem` / `paper` / `citation` / `external_card` / `solver_attempt` / `influence` …
   - 性质：`importance` / `difficulty` / `vitality` / `identity` / `status` / `msc` / `embedding` / `short_title` …
   - 例：`difficulty_fit_v3.py` ✅（原名 m13 fit）、`importance_scores.jsonl` ✅（原名 p5_ranking）
2. **代号只允许出现在三个地方**：本规范附录、密钥台账（KEYS_LEDGER.md，密钥编组本身是敏感内部物）、
   服务器运维日志原文。**其余一切产物——文件名、目录名、表名、列名、文档标题、报告、提交信息——禁用代号。**
3. **外部事实用全称**：公开模型名（GLM-5.3、DeepSeek-V4-Pro、Kimi-K3）、数据集名（UnsolvedMath、
   OpenConjecture）、期刊名、组织名（OpenCitations、Semantic Scholar）允许出现，但首次出现给中文
   说明（如"语义向量模型 BGE-M3"），不允许缩写自造（❌ dsv4、dsr、kimi 单独出现）。
4. **日期后缀**统一 `YYYY-MM-DD`（文件名可用 `YYYYMMDD`），禁止 `0929` 这类无年份写法用于新文件。
5. **目录单一职责**：一个目录只放一类东西；一次性脚本进 `scratch/`，用完当班归档 attic。
6. **人话优先（2026-09-30 用户拍板，最高优先级）**：**凡是给人看的清单、任务名、流程说明（任务/断点表、
   交接文档的待办、汇报材料），一律大白话**——一句话说清这件事在干什么；技术代号只许出现在括号里当
   "定位符"（指明去哪个文件操作），绝不许当任务名或标题。例：❌"外部卡 MSC 富集" → ✅"给外部导入的
   卡标注数学分支（`enrich_msc_glm.py`）"；❌"DDL 定稿" → ✅"数据库结构改版脚本定稿"。判定标准：
   把这行字念给一个不懂项目的人听，他能复述出这件事是干什么的才算合格。
7. **实验开工五要素登记（2026-09-30 用户拍板）**：任何新实验/管线开工前，必须在
   `EXPERIMENT_REGISTRY.md`（实验台账）按模板登记一张卡片，五要素缺一不可：
   **① 测什么（一句话）② 在哪台机器跑（本地/服务器，为什么）③ 用哪家 AI 接口（供应商+模型+钥匙编组）④
   数据存在哪（输入/输出/断点文件路径）⑤ 完成判据（什么数字算完）**。没登记的实验不许跑；收工后
   台账状态行必须更新数字。监控任何实验只看台账，不需要读代码。
   **实验的唯一标识 = 大白话名字本身**（如「引用影响力判定」）。
   **2026-09-30 晚间用户补充裁定（取代此前"禁止编号"的表述）**：字母/编号**可以**用作流水句柄
   （如步骤号 S001、批次号 v4、档位 I1-I5），但两个硬条件，缺一即违规：
   ① **不裸用**——任何引用处必须与大白话名字同现（"S001 · 新卡片归堆"✅；裸写"S001"❌）；
   ② **每一步必须用最直白的话写清输入与增量**——输入是什么（哪个文件/表+当时数量）、跑完什么变了
   （哪张表/文件加了多少、什么状态从几变成几），记入实验步骤日志 `STEP_LOG.md`（append-only 流水）。
8. **AI 调用完整留痕 = 模型责任标注（2026-10-01 用户拍板，"六条铁律"实际已是八条）**：
   未来任何实验送 AI，必须完整记录**用哪家 API + 哪版提示词**，缺一不许跑：
   ① 提示词正文存 `pilot/prompts/`（版本化档案 `PROMPTS_REGISTRY.md`），**改一个字就升版本号新建文件，
     旧版永不删**——提示词变了等于实验条件变了，必须可追溯；
   ② 每条 AI 产出（verdict/attempt/score 行）落盘时带**责任四件套**：
     `vendor + model + endpoint + prompt_sha256`；
   ③ 实验台账卡片的"用哪家 AI"一栏写明模型与提示词版本；
   ④ 引擎与既有判官有供应商亲缘时，责任标注必须带 `kinship_warning`（下游统计可见家族偏差风险）；
   ⑤ 计费纪律：国内引擎尽量走 Coding Plan 套餐（零现金）；按量钥匙（海外旗舰、智谱资源包、
     DeepSeek 官方、火山 ark）只用于终审类刀刃场景，动用前在密钥台账登记。

### 检查与执行

- 新文件落盘前自查："一个第一次来的人能从文件名说出这文件是什么吗？"
- 季度审计：对工作区跑一遍附录 A 代号 grep，新出现的违规即改。

---

## 二、代号 → 语义名对照（强制替换表）

| 旧代号（禁用于新产物） | 新语义名 |
|---|---|
| M13 | 难度评估（difficulty） |
| M13 attempts / verdicts | 求解尝试 / 进度裁决（solver_attempt / progress_verdict） |
| P5 | 重要性评分（importance） |
| P0 / P4 | 评分校准（锚库 / 金标准盲测） |
| nap | 非命题分诊（non_proposition_triage） |
| canon_judge / canon_2nd | 同一性一审 / 二审（identity_verdict / identity_verdict_second） |
| s2_* | 引用富化与影响力（citation_enrich / influence_*） |
| L1 / L2（车道） | 影响力车道 / 主管线车道（仅在 SESSION_LANES 登记表用） |
| nb541…nb8 / lane | 抽取批次车道（extraction_lane_*） |
| E1 / E2 / E3 | 对撞通道：跨源标题 / 变体折叠 / 别名（collision_title / collision_variant / collision_alias） |
| ext-um | 外部卡·UnsolvedMath 源（external_card_unsolvedmath） |
| EP / FC / OC / OPG / TOPP / UM / wiki | 外部源全名（见注册表 §8.2） |
| COCI | OpenCitations 开放引用索引 |
| 37cf / team2 / lite | 密钥编组 A / B / C（仅密钥台账） |
| glm / dsv4 / dsr / kimi | GLM-5.3 / DeepSeek-V4-Pro / DeepSeek-R1 / Kimi-K3 |
| node01 | 实验室服务器 |
| batch400 / next_batch / batch_retry | 候选池：批次一 / 延伸批次 / 重试批次（沿用现名至池退役，见 §四） |
| embed_vectors / canon_vectors | 语义向量：外部卡 / 本库命题簇 |

---

## 三、文档层命名

- 顶层文档按 `主题_日期.md`（如 `ASSET_REGISTRY_2026-09-30.md`）；讨论稿在文内标"状态：讨论稿"。
- 交接文档（HANDOVER）：现行版 `HANDOVER_2026-09-29.md`，含旧代号属历史事实，**不回改**，
  新版交接必须用语义名并引用本规范。
- 报告/导出文件：`内容_口径_日期`（如 `demo_cards_famous_2026-09-29.csv` ✅ 已合规）。

---

## 四、物理改名计划（分三批，安全优先）

> 原则：**活跃进程依赖的路径一律等窗口**；历史归档（attic）不回改，MANIFEST 即字典。

### 第一批（已执行，2026-09-30）

- 本机根 `pilot\` → `服务器运维\`（原"两处 pilot 混淆"根源消除）
- 根目录游离数据 `still_missing_0929.json` 归档

### 第二批（✅ 已执行，2026-09-30 15:20 维护窗口）

> 执行条件已满足：服务器车道池见底（541 批收官，仅剩空转进程）、全部实验进程已干净收停
> （run_pilot ×2、daemon ×2、注册表 lanes/sidecars 全 disabled，DB 无损 15,964/1,710）。
> 双端同步 mv + sed 修补引用 + py_compile 冒烟 + watchdog 纯监视态冒烟，全部通过。

**服务器侧（node01）已改名**：

| 旧名 | 新名 |
|---|---|
| `m13_attempt.py` / `m13_verify.py` | `solver_attempt.py` / `progress_verdict.py` |
| `m13_targets_v4.json` / `m13_pool_qualified.json` | `difficulty_targets_v4.json` / `difficulty_qualified_pool.json` |
| `nap_prefilter.py` / `nap_triage.jsonl` | `non_proposition_triage.py` / `.jsonl` |
| `canon_judge.py` / `canon_second_opinion.py` | `identity_verdict.py` / `identity_verdict_second.py` |
| `runs/m13-v1/` | `runs/difficulty-v1/`（内含 `difficulty_targets_merged110.json`、`solver_v4_2026-09-30_completed.log`） |
| `s2_influence/` | `influence_calibration/`（校准输入/双引擎裁决/冒烟全换语义名） |
| 注册表 sidecar | `difficulty_solver`（环境变量 `SOLVER_TARGETS/SOLVER_ENGINE/SOLVER_WORKERS`，即原 `M13_*`）+ `difficulty_progress_verdict`，均 disabled |

**本机镜像侧同批改名**：上表全部 + `s2_citing_enrich.py → citation_enrich_semantic_scholar.py`、`s2_citing_embed.py → influence_citing_paper_embeddings.py`、`s2_edge_sim.py → influence_edge_similarity.py`、`s2_calib_sample.py → influence_calibration_sample.py`、`s2_influence_judge.py → influence_verdict.py`、`s2_enrich.py → paper_enrich_semantic_scholar.py`、`m13_verify_local.py → progress_verdict_local.py`、数据文件（`citing_embeddings.npy → influence_citing_paper_embeddings.npy`、`s2_citing_enrich.jsonl → citation_enrich_citing_papers.jsonl` 等）与日志/断点文件同步更名。

**引用修补范围**：双端 24 个活跃脚本内部路径与 pgrep 匹配串、watchdog/daemon/看板、注册表、`after_lanes.sh`、`migrate_ddl_v2.py`（冲突类型枚举注释）。

**保留不改的合理残留**（Semantic Scholar 数据字段，业界标准缩写，改名会破坏既有 JSONL schema 兼容）：
`s2_paper_id` / `s2_status` / `s2_edges` 等**数据字段名**；`canon_verdicts*` 表名与 `canon_embed/canon_vectors/canon_fts` 数据文件名（数据库层，归第三批）。

### ~~第二批（下一维护窗口：服务器车道空闲 + cron 暂停时执行）~~ → 已于 2026-09-30 15:20 执行完毕，见上方执行记录

| 现名（服务器+本机镜像） | 新名 | 需同步修改 |
|---|---|---|
| ~~`m13_attempt.py` / `m13_verify.py`~~ | `solver_attempt.py` / `progress_verdict.py` | ~~车道注册表 sidecars cmd、HANDOVER 引用~~ |
| ~~`m13_targets_v4.json`~~ | `difficulty_targets_v4.json` | ~~同上~~ |
| ~~`nap_prefilter.py` / `nap_triage.jsonl`~~ | `non_proposition_triage.py` / `.jsonl` | ~~管线 daemon 接力链~~ |
| ~~`canon_judge.py` / `canon_second_opinion.py`~~ | `identity_verdict.py` / `_second.py` | ~~同上~~ |
| ~~`s2_*.py` 系列~~ | `citation_enrich_*` / `influence_*` | ~~本机 L1 车道登记~~ |
| ~~`runs/m13-v1/`~~ | `runs/difficulty-v1/` | ~~逐文件 mv，保留 verdicts 原名内容不动~~ |

### 第三批（V3 DDL 迁移窗口，走 schema_migrations 版本化）

| 现表名 | 建议新名 |
|---|---|
| `canon_verdicts` / `canon_verdicts_2nd` | `identity_verdict` / `identity_verdict_second` |
| `score_aggregates` | `importance_scores`（dimension 列语义已正确） |
| 指标层新表（规划中三表） | **直接用语义名落地**：`solver_attempt` / `progress_verdict` / `engine_skill`（替代原方案里的 m13_* 命名——DB_METRICS_PLAN §3.2 的表名据此修正） |
| `problems.paper_time_status` 等列名 | 语义已清晰，不动 |

### 明确不改的

- `open_problem_db/pilot/`（本地）与服务器 `…/math_openproblem/pilot/` 目录名：双端同步纪律要求同 名，
  且服务器 cron/进程 cwd 依赖；其语义（"试点管线"）已由 README 界定，改名的收益不值风险。
- 历史日志、归档区、memory 记录：历史事实，不回改。
- ssh 主机别名 `node01`：基础设施标识，只出现在运维上下文。

---

## 五、与既有治理文档的关系

- `DB_GOVERNANCE_PLAN.md` 六条铁律不变，本规范补第七条：**语义命名**。
- `SESSION_LANES.md` 车道登记继续用车道编号（那是内部调度需要），但车道内容描述必须用语义名。
- 本规范与资产注册表一并作为导师汇报材料；修订需登记日期与原因。
