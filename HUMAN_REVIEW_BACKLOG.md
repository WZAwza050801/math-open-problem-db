# 人工审核总账（HUMAN_REVIEW_BACKLOG）

> **创建**：2026-09-28 ｜ **性质**：活文档，持续追加 ｜ **约定**：完成一项就打勾 `[x]` 并注日期；
> 新欠账由 agent 在做任务时直接追加到对应分区，不另开文件。
> 原则：欠着不丢，最后一起补。每项都写明"怎么审"，保证隔几个月拿起来还能直接上手。

---

## 使用说明

- 优先级含义：**P0** = 结果会影响下游数据正确性，审之前别大规模复用该结论；
  **P1** = 大批量质量把关，适合整块时间批量刷；**P2** = 抽检性质，确认流程没跑歪即可。
- 涉及 API key 的文件（.glm_key 等）不在审核范围内，别动。
- 所有路径相对于 `open_problem_db/`。

---

## P0 · 影响数据正确性的

### [ ] P0-1 M13 高分 attempt 核验（6 条，约 1-2 小时）

M13 裁决给出了 4 条 level-4（完整候选解）和 2 条 level-3。**这些如果坐实，等于 AI 解决了 I4 级开放问题**——更大概率是 (a) 该问题已被文献解决（题卡状态滞后），或 (b) 裁决被误导。逐条人工判断属于哪种。
**2026-09-29 晚更新**：导师试审后——#1-3（op-2026-000491，MIP*=RE）**确认文献已解决**（C-1，补 status_event solved_in_literature）；#4（op-2026-000069，Eremenko 构造）按铁律 **wont_fix 挂起**，待导师明确表态构造真伪；#5、#6 未进本次试审，仍待核。

| # | 文件 | 裁决理由摘要 | 核验要点 |
|---|---|---|---|
| 1 | `pilot/runs/m13-v1/attempts/op-2026-000491__t0.json` | 关联集分离 ⇔ 非局部游戏值 gap，援引 JNVWY 否定解答 | MIP*=RE (Ji et al. 2020) 是否确实蕴涵该问题的否定答案 |
| 2 | `op-2026-000491__t1.json` | 同上，基于 MIP*=RE 推导 C_qa ⊊ C_qc | 同上；**此题 3 轨迹一致判 4/4/3**，优先审 |
| 3 | `op-2026-000491__t2.json` | 同上 | 同上 |
| 4 | `op-2026-000069__t2.json` | Bishop 反例 + 拟共形折叠构造，声称否定 Eremenko 猜想 | 构造是否真实可溯源；Eremenko 猜想现状（2017 后有无已发表反例） |
| 5 | `op-2026-004153__t0.json` | S³ 反例：P(S³) 的 π₀ 可数 + Thurston 定理 ⇒ 家族 GV 的 π₀ 不可数 | S³ 上 Godbillon-Vey 取值论证是否成立 |
| 6 | `pilot/runs/m13-v1/attempts/op-2026-006170__t0.json`（判 3） | cdh 下降把任意簇归约到光滑射影，证 Tate 猜想 ⇒ dRW | 归约逻辑；缺口是否如裁决所述 |

**附带动作**：若 P0-1 的 #1-3 坐实（文献已解决），把题卡 `op-2026-000491` 的 `current_status` 从 unknown 改为 resolved（注明来源 MIP*=RE），并在状态史里补一条。

### [x] P0-3 canonical 二裁顽固 unsure 5 对终审（已生成 2026-09-29，约 30-40 分钟）— ✅ 2026-09-29 晚导师试审"都通过"，5 对全判 distinct（采纳预审建议），裁决记录 `review_pack_2026-09-29/trial_verdicts_2026-09-29.jsonl`（A1-1..5），待车道空闲跑 `apply_trial_verdicts.py` 落库

canon_verdicts 一裁 + canon_verdicts_2nd 二裁后仅剩 **5 对 verdict=unsure**（node01 `db.sqlite3` canon_verdicts_2nd）。全部是"同篇或同主题、但陈述层次不同"（一条是定义/定理、另一条才是开放问题）。**默认处置建议：distinct（不合并）——宁缺勿滥，且符合"卡有独立提出价值"语义**；审的时候只看是否有我看漏的 same 证据。

| # | 卡 A（arxiv / 内容要点） | 卡 B（arxiv / 内容要点） | 二裁 reason 摘要 | 我的预审 |
|---|---|---|---|---|
| 1 | OP-1BFEDC49E0F1 / 0808.0319 / group-like series 的 γ-可分解定理 | OP-6E35F66F63B2 / 0808.0319 / 双 shuffle 设定下的开放问题 | 同篇共享 setup，A 是定理 B 是问题 | **distinct**：一卡一问题本体 |
| 2 | OP-37DE18DB107C / 2002.09655 / CBER 定义（截断） | OP-3C43F4923E5A / 2002.09655 / CBER 上具体开放问题 | A 仅定义、B 才是问题 | **distinct**：定义卡本就该独立 |
| 3 | OP-26D9CD37115C / math/0103175 / CM motives 范畴描述 | OP-E13E61144957 / math/0103175 / 假设 Hodge 后的 goodness 问题 | 同篇 intro 不同层次 | **distinct**：#1/#2 同类 |
| 4 | OP-7C760A46299D / 1601.06467 / Schwarzschild-Kerr 非线性稳定定理背景 | OP-A5685EFDFEFE / 0805.4309 / 只是 vague motivational outlook | 跨论文同主题，B 无独立陈述 | **distinct**：B 是 motivation 非同题；且 B 未来可能进 nap 分诊 |
| 5 | OP-DAEBEA2BEF20 / math/0204065 / Tannakian motive 构造（§10） | OP-DBA257DADE45 / math/0103175 / CM Hodge 相关问题 | 跨论文 Milne 两著作，A 构造 B 提问 | **distinct**：跨论文、层次不同 |

**裁决落法**：same → 填 canonical_uid + merge_log(verdict=manual, actor=human)；distinct → 两卡独立、把本次终审写进 conflict_queue(status=adjudicated)；拿不准 → wont_fix 挂起。

### [x] P0-2 M13 双裁决器分歧条目核验（已生成 2026-09-29，人工终审 ~30 分钟）

GLM glm-5.3（coding 端点，thinking disabled）已于 2026-09-29 对 150 条 v1 attempt 交叉裁决完毕（`pilot/runs/m13-v1/verdicts_cross_glm.jsonl`）。
配对 147 条：exact 一致 99（67%），分歧 48，**diff≥2 共 4 条**（`verifier_disagreement_0929.json`）：

| # | uid | traj | doubao | glm | 备注 |
|---|---|---|---|---|---|
| 1 | op-2026-000069 | t2 | 4 | 1 | Eremenko 反例，P0-1 #2 印证 |
| 2 | op-2026-000491 | t2 | 3 | 1 | MIP*=RE，P0-1 #1 印证（GLM 认为只是文献梳理） |
| 3 | op-2026-001983 | t0 | 1 | 4 | **新增**：GLM 判完整解（level 4），doubao 只认 level 1——若坐实是"题卡状态滞后"又一例 |
| 4 | op-2026-006170 | t0 | 3 | 1 | cdh 下降/Tate，P0-1 #4 印证 |

另：GLM 交叉裁决 3 条 parse_fail（level=None），重跑前需从 verdicts_cross_glm.jsonl 剔除。

---

## P1 · 批量质量把关

### [ ] P1-1 canonical 归一化裁决：2,305 对（大头，预计多个半天）

- **文件**：`canon_prototype/pending_pairs.jsonl`（2,305 对，每对是"疑似同一猜想"的候选合并对）
- **欠因**：FTS5 召回 + GLM 预判的三段式管线，第三段人工查验从原型期一直拖到现在
- **怎么审**：每对看两条题卡的 statement 是否真的指同一猜想 → `merge` / `reject` / `unsure`。
  建议先按 GLM 预判置信度排序，从高分对开始刷（过一遍最快建立手感）
- **注意**：裁决是**可逆的**（证据型归并），不用怕判错，marked uncertain 的留到最后
- **2026-09-29 增补（二次裁决）**：unsure 50 对 + 矛盾 84 对已由 team2 glm-5.3 独立二裁（`canon_verdicts_2nd` 表，日志 `pilot/logs/canon_2nd_0929.log`）。结果：same 37 / distinct 81 / unsure 5 / parse_fail 11。**人工优先看二裁判 same 的矛盾对**（原判 distinct、二裁判 same 的翻转项，最可能是真合并）；11 条 parse_fail 待换引擎重跑后再进人工堆。

### [ ] P1-2 batch400 抽卡抽检（50 张，约 1-2 小时）

- **背景**：batch400 已产出 ~722 卡（glm-5.3 386 + qwen3.8-max 336），历史可核验率 99.5% 是 glm 老批次的数据，**新批次要重新抽检确认**
- **怎么审**：从 db 里按 engine 分层各抽 25 张，对照原论文 LaTeX 核三件事：
  (1) 命题是否真在论文中；(2) 19 字段的出处页码/章节是否准确；(3) statement 是否忠实（无量词偷换）
- **入口**：node01 `~/.../pilot/db.sqlite3`，`select * from cards where created_at > '2026-09-28'`

### [ ] P1-3 not_a_proposition 复核：2,090 卡（约 28% 库存）

- **背景**：抽取时标记为"不是命题"（背景陈述/观点/综述段落），占 28%
- **怎么审**：分两层——先跑一遍 AI 预筛（找出"其实是个正经开放问题"的漏网卡，预计 5-10%），
  人工只终审 AI 判为"捞回"的部分 + 随机 100 张抽检 AI 判定准确率
- **状态**：AI 预筛脚本未写，做的时候找 agent 现写（小 prompt 任务，可用千帆 plan）

### [ ] P1-4 nap（not-a-proposition 预筛）短名单人工终审（2026-09-29 新欠）

- **背景**：`nap_prefilter.py`（脚本头明确写 *NEVER updates the DB*）对 2,674 张被标
  `paper_time_status='not_a_proposition'` 的卡做 AI 预筛，输出 `pilot/nap_triage.jsonl`：
  **confirm 2,437（确认非命题）/ background 125 / restated_open 100（误标，应捞回为开放问题）/ parse_fail 6 / unsure 6**
- **纠正**：这不是"状态回填"——verdict 表达的是"是否命题"，**不能**直接写进 `current_status`（那个字段是"是否已解决"）。
  正确动作是**人工终审短名单**而非自动落库
- **怎么审**（短名单已导出，见 `reports/2026-09-29_.../nap_review_shortlist_2026-09-29.csv`）：
  ① 优先审 **106 条（restated_open 100 + unsure 6）**：逐条看 statement，确认是否真是开放问题 → 是则
  把 `paper_time_status` 从 not_a_proposition 翻回 open_at_paper_time（这是 P1-3 的"捞回"动作）；
  **2026-09-29 晚进度**：试审 5 张（跨期刊抽样）导师全确认捞回（B-1..5，`trial_verdicts_2026-09-29.jsonl`）；
  剩 101 条按同样方式批量审
  ② **background 125 条**：改为 background_known_open（可选，低优先）；
  ③ confirm 2,437 条只需抽检 20 条验证预筛准确率，确认无系统性漏捞；
  ④ parse_fail 6 条换引擎重跑
- **关联**：本项完成即等于 P1-3（2,090 卡 not_a_proposition 复核）的 AI 预筛段落地

### [ ] P1-5 blocked 规范陈述簇处置（2026-09-29 新欠，规则设计+抽检）

- **背景**：RH 主簇（op-2026-000009，5 卡 5 篇）等一批簇的 `canonical_statement.review_state=blocked`——
  原因是簇内卡片**全是背景引用卡**（"假设 RH 证明 X"），无正面陈述可合成。质量门禁正确拦截（显示"未评级"），
  但这批簇恰是**最有名的问题**，平台上线时 RH/Hodge 显示"未评级"会很难看
- **怎么审**：① 先统计 blocked 簇总量和别名热点重合度；② 定规则：是否允许用"簇内卡 + 别名字典"合成代表性陈述
  （需双人审核）；③ 人工定稿 RH/Hodge 等 top 20 blocked 簇的规范陈述（这是最有杠杆的人工活之一）

---

## P2 · 抽检/确认性质

### [ ] P2-1 P5 边界随机分配抽检（20 张，约 30 分钟）

`canon_prototype/p5_ranking_assigned.jsonl` 里 `assign_mode` 为 `random_top2` 的条目
（边界分数随机分档，seed=42 可复现）。抽 20 张看随机分配是否造成明显荒谬的分档。

### [ ] P2-2 别名表审核（named problem alias）

有名问题（如 Bootstrap 猜想、Eremenko 猜想）的别名归一表人工过一遍。
入口：`canon_prototype/NAMED_PROBLEM_SEED_REPORT.md` 及其关联 CSV。
**欠因**：早期建库时排期"数据库建立后统一审"，一直未启动。

### [ ] P2-3 M13 求解器行为抽检（10 条，约 40 分钟）

随机抽 10 条 attempt 全文对照裁决，确认裁决标准执行一致（尤其 level 1/2 边界）。
这是给"以后用 M13 数据训练 IRT"提前建立的信度依据。

### [ ] P2-5 卡片 MSC 与论文 arXiv 学科标签背离抽检（2026-09-29 新欠，约 1 小时）

- **背景**：2026-09-29 补齐了全部论文的 arXiv 元数据（`paper_extra` 表：摘要、作者自填学科分类），
  拿它跟卡片抽取出的 `msc_primary` 做了交叉体检（`_msc_consistency2_0929.py`）：
  **9,508 张有分类的卡里，核心一致 68.7%、跨学科但合理 21.1%、距核心较远 10.2%（966 条）**
- **重要口径**：这 10.2% **不是错误率**——数学论文普遍跨学科（数论论文里出现表示论问题完全正常）。
  它只是一份**便宜的人工抽查短名单**，不要当成质量指标对外报"错误率"
- **怎么审**：短名单已导出 `pilot/msc_far_mismatch_0929.csv`（966 行，含 card_id/arXiv 链接/标签/MSC/arXiv 分类/陈述预览）。
  按 (arXiv 分类 → MSC) 分组批量看，重点看 top pairs：DS→32、PR→81、AP→83、AG→05、NT→12、GT→30。
  审完只需标两态：合理跨学科 / 抽取标错（后者改 msc_primary，并回喂抽取 prompt）
- **附带价值**：审完这批能直接产出"哪类论文抽取容易串领域"，是 prompt 迭代的输入

### [ ] P2-4 MSC 细分码中文翻译抽检（2026-09-29 新欠，约 30 分钟）

- **背景**：`msc2020_map.json` 里 `codes_zh` 的 98 个高频码是 agent 手译的（Top60 主分类+38 常见副码），
  其余 1,500+ 副码只有官方英文名（msc_code 表）。全量中文翻译待 LLM 小批量 + 抽检
- **怎么审**：① 抽 30 个手译码对照官方英文名看翻译是否地道（数学行话习惯，如 "percolation" 译"渗流"是否合适）；
  ② LLM 批量翻译完成后同样分层抽检
- **附带**：`msc_secondary` 有 115 个码不在官方 MSC2020 表内（如 11L41）——疑似抽取噪声或旧码，
  抽 20 张卡看是拼错还是组合码，属抽取质量问题反馈

---

## 已完成的审核（存档）

（暂无）

---

## 变更日志

- 2026-09-28 建档：P0-1（6 条）、P0-2（待生成）、P1-1（2,305 对）、P1-2（50 张）、P1-3（2,090 卡）、P2-1/2/3
- 2026-09-29 追加：P1-4（nap 回填核验）、P1-5（blocked 陈述簇处置）、P2-4（MSC 翻译抽检+非法码排查）——
  来自当日导师汇报材料制作过程（RH 主簇 blocked 发现、MSC 三级映射落地时的伴生发现）
- 2026-09-29 追加：P2-5（MSC × arXiv 分类背离短名单 966 条抽检）——来自当日论文元数据补齐后的交叉体检
