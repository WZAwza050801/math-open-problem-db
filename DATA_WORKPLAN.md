# 数据统计与整理工作计划（9/26 → 9/29 全量归一启动前）

> 2026-09-26 ｜ 视角：数据库工程师 ｜ 原则：先把"零 API / 纯算力"的活全部清掉，9/29 额度一到只做 LLM 裁决
> 标注：🖥=服务器 node01 跑 ｜ 💻=本机跑 ｜ ⏳=等 9/29 额度 ｜ 👤=等人工

---

## ⭐ 2026-09-29 老板新增需求（看卡片实例后提出，落账待排期）

三个维度，按"已有/半成品/真缺"分层：

| # | 需求 | 现状 | 动作 |
|---|---|---|---|
| R1 | 精确原文索引 + 相关论文链接 | **已有数据，未物化到卡片视图**：卡上已有 arxiv_id + quote_location（精确到定理/猜想编号）；papers 表已有 crossref_doi（如 JAMS 2025 → `10.1090/jams/1049`）。卡片导出/展示层没 join 出 DOI 和 URL | 零 API：导出视图把 `https://arxiv.org/abs/<id>` + doi.org 链接直接挂到每张卡 |
| R2 | 具体问题分支（如"调和分析"） | **半成品**：msc_primary/msc_secondary_json 已 100% 填充（42B25 就是调和分析的子码），但库内只有码、没有人话分支名 | 零 API：内置 MSC→中文分支名映射（42=傅里叶分析/调和分析），卡片和 canonical 双侧挂 |
| R3 | 基础知识路径（prerequisite chain） | **真缺**：19 字段里没有前置知识字段；V2 设计的 relation 表和正交维度词表也未落地 | 分两步：① canonical 层加 `prerequisites` 列（初值 none），② 用 LLM 从 MSC+规范陈述生成 2-3 层知识路径（需 API + 人工抽检），成本可控后排期 |

注：R1/R2 纯本地活，随时可做；R3 涉及 schema 变更，**必须**并入 DB_DESIGN V3 统一落 DDL（9/28 对抗审计已指出 schema 与设计分叉，不再打补丁加列）。

---

## 一、数据一致性体检（🖥 零 API，最先跑）

库是所有下游的地基，先出一份"体检报告"而不是发现问题再补：

1. **完整性**：PRAGMA integrity_check、外键完整性（problems.arxiv_id → papers 孤儿卡）、content_hash 幂等验证（同 hash 卡应唯一）
2. **字段质量矩阵**：19 个卡字段逐列统计 null/empty/超长/异常值 → 一页"字段质量仪表盘"（交接文档只盘了 5 个核心字段，这次全字段）
3. **交叉分布**：label × paper_time_status × journal × pub_year 四维交叉表——任何一格异常都提示抽取系统性偏差
4. **重复土壤探查**：同 arxiv_id 内 self_contained 相似度 >0.9 的卡对清单（同篇拆卡重复，归一第一批工作对象）

## 二、引用网络深度加工（🖥 零 API）

citations 表已有 39,426 行，但只算过总量。要加工成"可用档案"：

1. **年度引用曲线**：每篇论文的 citing_year 直方图 → 论文影响力时间序列（表 paper_cite_timeline）
2. **网络指标**：被引度分布（长尾形态）、co-citation 对（经常被一起引的论文对 → 主题簇信号）
3. **全量快照导出**：citations + stats 导出 JSONL 双份存档（服务器+本机），纳入 git 版本化
4. **生命力重算调度**：vitality 已在本机落地，服务器版重算脚本部署 + 约定每月重跑（引用数据会增长）

## 三、领域结构统计（🖥 零 API）

1. **MSC 分布**：msc_primary 直方图（哪个领域卡多/少，冷热领域清单——讨论平台冷启动的分区依据）
2. **年代 × 状态趋势**：paper_time_status 随年代的分布变迁——"开放问题占比"的年代曲线，这是**猜想发生学研究的直接素材**（导师方向）
3. **期刊画像**：五刊的 label 分布差异（Annals 偏 solved？Acta 偏 construction？）——校准"期刊→问题类型"先验

## 四、归一预备（💻 本机，为 9/29 装弹）

1. **邻居表落盘**：7,471² 暴力余弦的 top-20 邻居写进 canon_db（neighbors 表：card_id, neighbor_id, cos, rank）——无论阈值怎么调，一次算完永久复用；"相关卡"功能也直接用它
2. **候选对冻结**：cos>0.80 的 3,392 对 + 别名共同出现对（named_problem_seed 卡组）合并去重 → `pending_pairs.jsonl`（裁决输入文件，9/29 直接喂 GLM）
3. **别名 × embedding 交叉验证**：42 个归并热点名下卡组的组内余弦分布——验证别名表质量，顺带给裁决对加权
4. **status_event 第一批回填（⏳ 不等额度！）**：proposed_at_paper / solved_in_paper / background_known_open 三类事件**不需要 LLM**——纯从卡上 paper_time_status + pub_year 聚合即可。canonical 未生成前先做成"按 arxiv_id 聚合"的中间表，canonical 生成后一条 JOIN 挂接

## 五、9/29 额度窗口的任务单（⏳ 装弹完毕即开火）

按优先级（积分预算 ~76,000/周）：

| # | 任务 | 规模 | 预算 |
|---|---|---|---|
| 1 | 3,392 对 canonical 裁决 | 3.4k 次调用 | ~5.1 万 |
| 2 | 裁决结果 union-find → canonical 生成 → statement_rewritten（每组 1 次） | ~数百次 | ~1 万 |
| 3 | 关系抽取第二批（related_note 里的 mentions，仅对已生成 canonical） | 待定 | 余量 |
| 4 | 32 篇 PDF 扫尾（Qwen3-VL，Token Plan） | 32 篇 | Token Plan 份额 |

**纪律**：裁决脚本沿用断点续跑 + 引擎降级链；每晚增量导出 JSONL + git commit（V1 §五 版本化约定）。

## 六、schema 落地预备（💻）

1. V2 DDL 空表先行：canonical_problem / status_event / problem_relation / named_problem / pairwise_comparison 以空表 + 索引形式建到 canon_db（数据后填，结构先立）
2. JSONL 导出管线统一：每次跑批一个 commit，git 仓库存导出（V1 决议）

## 七、等人工（不阻塞上述任何一项）

- 👤 batch1 审计 367 卡（你，Cursor+Grok）
- 👤 5 对 same 查验 + 别名字典 818 条过表（你/同学）
- 👤 导师：V2 定稿 + 归并语义边界 + 评分系统（RATING_DESIGN_NOTE 一并过）

---

## 执行顺序（本周）

```
今天    ① 体检脚本上服务器跑 + ② 邻居表/候选对冻结（本机） + ④ status_event 中间表
明天    ③ 领域结构统计 + 引用时间线 + 快照导出双份
9/28    全部复核 → pending_pairs.jsonl 终版 → 裁决脚本预演（dry-run 不调 API）
9/29 早 GLM 额度重置 → 全量裁决开火
```
