# 外部开源问题数据库 · 注入与归档方案（讨论稿）

> 2026-09-29 · 基于 DB_DESIGN_V1（多数据集注入决议）+ DB_DESIGN_V2 §五/§六（origin_type 与字段映射初稿）扩展
> 状态：讨论稿——随 V2 一并交导师过目
> 本文回答一个问题：**未来把 OpenConjecture、Formal Conjectures、UnsolvedMath 等外部开源问题库"安插"进我们 7,471 卡的库时，具体怎么进、进什么、进完怎么归并。**

---

## 一、总原则（继承 V1/V2，五条铁律）

1. **外部条目不是覆盖，是增量**。所有外部条目走 `ingest_batch` 溯源（V2 §3.4），`origin_type=external_import`（V2 §五），强制 `review_state=draft`，人工抽检后才能 `published`。
2. **外部条目先进库、后归并**。注入时一律**独立建 canonical 条目**（宁缺勿滥，V1 §六.1），然后通过与现有 7,471 卡相同的双通道归一管线（FTS5 短语 + bge-m3 embedding，V2 §二）做**对撞归并**——撞上了就并，撞不上就保持独立。绝不按"来源说这是同一个问题"直接信任。
3. **schema 不动**。V2 DDL 已预留全部所需字段（`source_url`、`source_dataset`、`origin_type`、`status_event.event_type=external_source`、`named_problem.source`）。注入新数据集 = 新写一个 extractor，不改表。
4. **许可先记录后注入**。每个数据集的 license 记入 `ingest_batch.note`；无明确许可的个人维护站点（如 erdosproblems.com）先引用 URL 不批量复制正文（见 §六.风险）。
5. **外部 ≠ 权威**。外部条目自带的状态（open/solved）写进 `status_event(event_type=external_source)`，**不直接改** `canonical_problem.status` 缓存列；status 仍由本库事件链推导，冲突项进人工抽检队列。
6. **能抄则抄、能并则并**（2026-09-29 用户拍板）：开源问题集、应用数学问题集，凡许可允许的一律欢迎注入，去粗取精——抄数据不抄定位，工程教训（V1 §九）照单全收；应用数学问题集与纯数学开放问题同权入库，靠标签区分（见 §二 B8/B9）。

---

## 二、外部数据源全景清单（2026-09-29 调研）

### A 层 · 结构化数据集（有机器可读导出，注入成本低，价值最高）

| # | 数据源 | 规模 | 形态/获取 | 许可 | 对本库的价值 |
|---|---|---|---|---|---|
| A1 | **UnsolvedMath**（unsolvedmath.com + HF `cafsdf/UnsolvedMath`） | v1.7 共 **15,458** 条：Oberwolfach Reports 6,673 / AIM workshop 3,359 / AMR lists 3,342 / OpenGarden 422 / Kirby 低维拓扑 366 / Kourovka 150 / Erdős 632 / Green 100 / Hilbert / Smale / DARPA / Landau / Hardy-Littlewood / Millennium | JSON（HF datasets），problems.json + categories + difficulty + sets | **CC BY 4.0** | **一箭多雕**：一次注入覆盖十几个经典问题集。字段含 statement/background/domain/difficulty(L1-L5)/status/year_proposed/solved_year/source_url。注意其含 AI 生成的文献综述（v1.5-1.7 自述"机器生成、需独立验证"），statement 部分可用，AI 综述部分只存 note |
| A2 | **OpenConjecture**（HF `OpenConjecture/openconjecture` + github `davisrbr/conjectures-arxiv`） | 4,420 猜想 / 26.7k arXiv 论文，持续周更 | HF datasets（含 arxiv_id、plain_text、interestingness/viability 分数、license 字段、label 置信度） | 数据字段带 license_family（多为 arXiv nonexclusive-distrib），需逐条核对 | **与我们五刊管线同构**（LLM 从论文抽猜想），可直接按 `arxiv_id` 与本库对撞；其 interestingness/viability 分数正好接我们 Bradley-Terry 难度评估规划。缺口：与本库五刊时段（2000-2025）重叠的是 arXiv 同期论文，撞并潜力大 |
| A3 | **DeepMind Formal Conjectures**（github `google-deepmind/formal-conjectures`） | **2,615** 条 Lean 4 形式化（1,029 open + 836 solved），按来源分类：Erdős / Wikipedia / MathOverflow / OEIS / arXiv / Millennium / Hilbert / Green / Kourovka / WoWII | Lean 4 仓库 + Mathlib，结构化目录 | Apache 2.0（代码）/ **CC BY 4.0**（内容） | **形式化层锚点**：每条带 Lean 陈述 + MSC2020 标签 + 来源溯源，正好补 V2 §六"ProofAtlas 形式化层"的实际落点。Lean `formal_statement` 存 `note/source_url`（V2 §六映射已留） |
| A4 | **erdosproblems.com**（Thomas Bloom） | **1,220** 题（48% 已解），带标签体系、引用、逐题讨论 | 网站 + 博客；有 HF 间接镜像（A1 的 Erdős 子集仅 632 条，不全）。抓取需确认 | 个人维护站点，无明示批量许可 → **先引用 URL，不批量复制正文** | Erdős 问题事实标准；标签体系（number theory 576 / graph theory 277…）可映射我们的正交维度词表；OPEN→SOLVED 事件流是 status_event 素材 |
| A5 | **AIM Problem Lists**（aimath.org） | 专家编辑的问题列表若干，版本化，哈佛 Dataverse 永久归档 | 网站；UnsolvedMath 已收录 3,359 条 AIM workshop 记录 | 开源工具 + Dataverse 归档 | 专家可信度高；优先经 A1 间接注入，直接爬取列为 P2 |

### B 层 · 平台/维基（半结构化，爬取或选摘，中等成本）

| # | 数据源 | 规模 | 定位 |
|---|---|---|---|
| B1 | **Open Problem Garden**（openproblemgarden.org） | ~709 条（algebra 294 / graph theory 228 / number theory 49…） | 老牌社区 wiki，更新慢；A1 已收录其 422 条（OpenGarden），**优先走 A1 间接注入**，缺口部分直接爬 |
| B2 | **Wikipedia 问题列表族**（List of unsolved problems in mathematics 及各分支页、List of conjectures） | 数百命名条目 | **named_problem 别名字典种子**（V1 §四既定）；每条带英文名/中文名 → 直接填 `named_problem`，同时补 status_event |
| B3 | **MathDB**（mathdb.com，Caltech 团队） | 数千条（仅纽结理论就 900+），从文献爬取，**追踪 AI 辅助突破的状态更新**（日更） | 定位与本库最接近（社区问题库+讨论），是**最直接的同类竞品+互补状态源**；其 status/progress 更新快，适合做 status_event 的对照源；注意社区条目含未验证 AI 声称（数学界已有批评），只取 `claimed_solved` 级别事件 |
| B4 | **Polymath Wiki**（michaelnielsen.org/polymath） | ~20 个项目记录 | 量小但价值特殊：massive collaboration 的完整状态史，做 status_event + 讨论案例 |
| B5 | **MathOverflow** | 海量 | 不做批量注入；借 A3 的 MO 来源子集 + 后期精选问题注入 |
| B6 | **Written on the Wall II**（West，图猜想清单） | 数百条图论猜想 | A3 已收录其条目；图论密度可观的补充源，P2 直接爬 |
| B7 | **VibeMathed**（vibemathed.com） | AI 声称解决的问题记录 | 参考性：给我们 `claimed_solved` 事件的人工核验队列提供外部对照，P2 观察名单 |
| B8 | **Blondel & Megretski《Unsolved Problems in Mathematical Systems and Control Theory》**（PUP 2004 + inma.ucl.ac.be 1998 网络版） | 控制论 60+49 题，PUP 官网带**逐题 partial solution 追踪页** | 应用数学方向最规范的开放问题集：专家出题、结构统一（描述/动机/已有结果/文献）、状态更新页天然是 status_event 素材。P2 |
| B9 | **ESGI 工业数学研习组报告**（European Study Groups with Industry，1968 牛津起源，每年 5-7 期，报告公开上网） | ~160 期 × 每期 3-6 题 ≈ **数百个工业数学问题**（流体/制造/环境/金融/生物…） | 注意定位差异：这些是"工业界提出的挑战"不是"理论开放问题"，多数无 solved/open 二值状态。注入时用正交标签 `problem_kind=industrial_challenge` 与理论问题区分，价值在于把平台扩展到应用数学社区。P2 观察 |

### C 层 · 形式化与对象库（不进 canonical_problem，做关系/标注补充）

| # | 数据源 | 用途 |
|---|---|---|
| C1 | **ProofAtlas**（proofatlas.ai） | V2 §六已定映射。239 open conjectures + **Top 500 两两比较排名（34,890 对，多 LLM 融合）**——与我们 Bradley-Terry 规划直接同构，排名结果作难度/重要性先验，不复制正文，存 `source_url` |
| C2 | **Open Conjecture Formalizations**（github SamuelSchlesinger/open-conjecture-formalizations） | 小型 Lean 4 形式化集 + Wikipedia 猜想索引（含 proved/disproved 年表），补 named_problem 与形式化链接 |
| C3 | **AlphaEvolve Repository of Problems**（google-deepmind，CC BY 4.0） | 67 题（Tao 参与监制），含验证代码，P2 |
| C4 | **π-Base / House of Graphs / LMFDB / OEIS / KnotInfo / FindStat / polyDB** | 对象数据库，**不建问题条目**；远期做"问题 ↔ 反例对象/序列/图"关联（problem_relation 的 appears_in/motivated_by 素材）。OEIS 猜想子集已进 A3 |
| C5 | **经典名单**（Guy《Unsolved Problems in Number Theory》、Bárány 等 branch 清单、各 Barbados 图论 workshop 等） | 大部分已被 A1/A3 覆盖；未覆盖者按 P2 逐个评估 |
| C6 | **Lean 形式化状态追踪**（2026-09-29 用户提问后调研） | **Palomar**（Kim Morrison 2026-08 上线的 Registry of Lean-Verified Mathematics，"命题是否已被 Lean 形式化"的注册表，重点跟踪）；**1000+ theorems**（mathlib docs/1000.yaml，Wikipedia 千定理 237 已形式化）；**mathlib docs/100.yaml + 100-missing**（Wiedijk 百定理榜）。用途：给我们 canonical 条目挂 formal_status（未形式化/陈述已形式化/证明已检验），与 A3 的 formal_proof 链接互补 |
| C7 | **Axiom Math**（洪乐潼，Palo Alto，2026 估值 $1.6B） | 商业服务商非数据库：AxiomProver（Putnam 12/12）、AXLE 引擎+开放 API/MCP、命题提取服务；开源资产 PrimeGapsLib。定位：**工具提供方**，未来可用其 API 做命题提取/形式化验证；不入库，观察名单 |

**明确不收**：FrontierMath / miniF2F 等 AI 基准（问题非公开、定位是评测不是问题库）；MathWorld / MathPages（弱结构、无维护承诺）。

---

## 三、优先级与排期建议

| 批次 | 数据源 | 理由 | 预估规模 |
|---|---|---|---|
| **P0（canonical 定稿后第一批）** | A1 UnsolvedMath → A3 Formal Conjectures → B2 Wikipedia 列表 | A1 一箭多雕铺底盘；A3 带来 Lean 陈述 + MSC；B2 喂饱别名字典（发布前检索刚需） | ~16,000 条外部条目 → 对撞后预计新增数千独立 canonical |
| **P1** | A2 OpenConjecture（含周更）→ A4 erdosproblems（先 URL 引用） | A2 与本库管线同构、对撞价值最高；A4 需先谈许可 | +5,600 |
| **P2（按需）** | A5 / B1 缺口 / B3 MathDB / B4 Polymath / B6 WoWII / **B8 控制论问题集** / B9 ESGI / C 层 | 状态对照、关系补充、形式化扩展、**应用数学扩域** | 弹性 |

**节奏约束**：P0/P1 全部排在 **canonical 归一全量跑完之后**（GLM 9/29-9/30 重置后的全量裁决是当前最高优先级，不要被注入任务分流）。注入管线写好放着，归一收尾即插即用。

---

## 四、注入管线设计（统一 ingest 接口）

```
外部源（HF/GitHub/网站）
   │
   ▼ ① extractor（每源一个脚本，输出统一中间格式）
   JSONL: { source_id, title, statement_raw, statement_lang,
            status_external, year, subject_tags, license,
            source_url, formal_statement?, extras }
   │
   ▼ ② 准入过滤（强制）
   - origin_type = external_import
   - review_state = draft（不进公开检索）
   - ingest_batch 落一条（batch_id = '<dataset>-<yyyymm>'，note 记 license 与版本快照）
   │
   ▼ ③ 独立建卡建条目
   - 每条先建 problem_card（verbatim = statement_raw，批次标 batch_id）
   - 建临时 canonical（uid 照常 op-2026-xxxxx，statement_en 取清洗后陈述）
   │
   ▼ ④ 对撞归并（核心步骤，复用 V2 §二管线，双向）
   - 通道 1：外部条目 ↔ 现有 7,471 卡（bge-m3 余弦 top-k + FTS5 短语）
   - 通道 2：外部条目 ↔ 外部条目（跨源去重：Erdős 问题在 A1/A3/A4 里出现三次是常态）
   - LLM 裁决 same/distinct/unsure → union-find 只吃 same（宁缺勿滥）
   - A2 OpenConjecture 特例：优先用 arxiv_id 精确对撞，再走语义通道兜底
   │
   ▼ ⑤ 富化（写入既有字段）
   - A3 的 Lean 陈述 → formal_statement（note/source_url 落库）
   - A1/A3 的 MSC → msc_primary / msc_secondary
   - 外部 status → status_event(event_type='external_source', source_url=…)
   - 命名 → named_problem（source 字段填数据集名）
   - A1 的 difficulty L1-L5 / A2 的 interestingness/viability → 缓存列或 extras JSON
   │
   ▼ ⑥ 人工抽检（老师介入点，继承 V2 §二.⑤）
   - 每源每批抽 5%：错并（拆）/漏并（合）/状态错误
```

**工程要点**：
- extractor 输出统一 JSONL 后，②-⑥ 全部复用现有管线代码，**新增代码只存在于 ①**；
- embedding 向量与现有 7,471 卡同一模型（bge-m3，1024 维），保证对撞余弦可比；
- 每次注入在 git 导出仓里单独 commit（batch_id 为 message 前缀），可整体回滚（V1 §五版本化原则）；
- 周更型来源（A2、B3）走增量：extractor 记录 content_hash（A2 原生带），无变化跳过。

---

## 五、与三互补层定位的对齐（修订 V2 §六结论）

V2 §六只写了 OpenConjecture/ProofAtlas 两个，调研后修正为**四层生态**：

| 层 | 代表 | 分工 | 互链方式 |
|---|---|---|---|
| 文献挖掘层（**本库**） | 五大刊 7,471 卡 | 提出处、引用网络、状态史、MSC 骨架 | uid 为锚，others 指 source_url 回本库 |
| 聚合层 | UnsolvedMath（A1） | 经典问题集 + 难度分级 + AI 文献综述 | 注入为条目，来源 URL 互指 |
| 社区流层 | OpenConjecture（A2）、MathDB（B3） | arXiv 周更流、AI 突破状态追踪 | arxiv_id 对撞 + status_event 对照 |
| 形式化层 | Formal Conjectures（A3）、ProofAtlas（C1） | Lean 4 陈述与机器检验证明 | formal_statement 存本库 note/source_url，ProofAtlas 只存排名先验 |

不重复建条目、以 uid + DOI/arxiv_id 互链的原则不变（V2 §六）。

---

## 六、风险记录（如实）

1. **许可不明的站点**（A4 erdosproblems.com 等）：个人维护、无明示批量导出许可。策略：先只存 `source_url` + 标题做检索索引（链接不受版权约束），正文批量复制等联系作者/导师把关。这与 V1 §七"先建后补"一致，但外部站点的风险低于逐字引用出版社论文。
2. **AI 生成内容混入**：A1 的 v1.5-1.7 文献综述、A2 的 label、B3 的社区状态都含未验证 AI 产出。策略：statement（原始陈述）与 AI 增值字段（综述/评分）**分列存放**，后者挂 `review_state=draft` 且发布界面明确标注"机器生成待验证"；A3 论文实测形式化错误率不低（误形式化三分法：句法 3%/语义 35%/误表达 48%），Lean 陈述照录但不当作"该问题的权威定义"。
3. **重复注入导致计数虚胖**：同一 Erdős 问题会从 A1/A3/A4 进三次。对策即 §四.④ 跨源对撞 + 抽检；短期接受"先胖后瘦"，uid 唯一性由归并保证。
4. **status 冲突**：外部说 solved、本库文献链说 open（或反之）。策略：只落 `external_source` 事件不改 status 缓存，冲突进人工队列——这恰好是"问题的一生"研究视角下最有价值的数据点之一。
5. **规模预期**：外部注入后 canonical 总量可能从数千跳到数万，SQLite 仍在十万条内（V1 §五结论不变），但 FTS5/embedding 索引重建时间要预留；注入批次永远在归一收尾后跑，不与全量裁决抢 GLM 额度。

---

## 七、下一步（待批准）

1. [ ] 本文与 DB_DESIGN_V2 一并交导师过目
2. [ ] canonical 全量归一收尾（当前最高优先级，不并行）
3. [ ] 归一收尾后：写 A1 UnsolvedMath extractor（HF 数据集直接下载，零爬虫）作为统一 ingest 接口的首个实现
4. [ ] A3 Formal Conjectures clone + Lean 陈述提取脚本（YAML/Lean 头部解析）
5. [ ] B2 Wikipedia 别名字典注入脚本（V1 §四既定任务的落地）
6. [ ] A4 erdosproblems.com：拟一封许可询问邮件草稿（给导师过目后发）

---
## 勘误与执行记录（2026-09-30）

- **A1 规模勘误**：HF `cafsdf/UnsolvedMath` 仓库（2026-06-25 版）实际仅 **2,084 条**（Erdős 632 / OpenGarden 422 / Kirby 366 / Kourovka 150 / Green 85 / DARPA 17 / Hilbert 11 / Smale 8 / Millennium 6 / Landau 1 / 无集合 374）；原记 15,458 是 unsolvedmath.com 上游含 Oberwolfach/AIM/AMR 的口径，HF 导出未含这些子集。若需要 Oberwolfach/AIM 部分需另行从 unsolvedmath.com 或 AIM Dataverse 获取。
- **A1 注入执行**：`external_ingest/unsolvedmath/`（raw 已下载 + extract_unsolvedmath.py）。产出 `ingest_unsolvedmath_2026-09-30.jsonl`：2,084 → 去内部重复 15 → **2,069 条**（origin_type=external_import / review_state=draft / 逐条 license+source_url / status 只走 external_source 事件）。字面 hash 与本库 0 撞（预期内——风格差异大，真对撞走 embedding 归并管线）。**待办**：ingestor 落库（等 V2 迁移完成后）+ 对撞归并。
