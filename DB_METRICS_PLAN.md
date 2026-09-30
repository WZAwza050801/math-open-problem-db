# 指标层数据库规划（DB Metrics Layer，讨论稿）

> 2026-09-29 · 基于全管线指标盘点 + DB_DESIGN_V2 + RATING_DESIGN_NOTE + DATA_WORKPLAN
> 状态：讨论稿——随 V2 一并交导师过目
> 回答两个问题：**① 除了问题卡片本身，我们手里已经算了哪些指标？② 这些指标在数据库里怎么放、怎么版本化、怎么发布？**

---

## 一、指标资产盘点（2026-09-29 实测口径）

### 已有并落库的（✅）

| 指标 | 层级 | 规模/数值 | 存储位置 |
|---|---|---|---|
| paper_time_status 四类 | 卡 | open 2,183 / solved 2,179 / not_a_prop 2,090 / bg_known 1,019（7,471 口径，现已 9,223 卡待重统） | problems 表列 |
| difficulty_hint | 卡 | 9,192/9,223 已填（缺 31） | problems 表列，RATING §四.2 定为"AI 先验、永不直接发布" |
| quality_score + review_state | 卡 | flag_for_human 2,396；blocked 门禁有正面案例（RH 主簇 5 背景卡被拦） | problems 表列 |
| 引用网络 | 论文 | citations 39,426 行；paper_cite_stats：806/818 篇有引用，总被引 39,294、篇均 48、max 396 | citations + paper_cite_stats 表 |
| 归并簇 | canonical | 6,868 簇（2,305 对裁决：same 673 / distinct 1,582 / unsure 50，零失败） | canonical 归并结果 |
| 归并候选与邻居 | 卡对 | bge-m3 全量 embedding（31MB）；cos>0.80 → 3,392 对；top-20 neighbors 表 | canon_db neighbors / pending_pairs.jsonl |
| 二裁与矛盾对 | 卡对 | canon_verdicts_2nd（same 37/distinct 81/unsure 5）；矛盾对 84 中 37 翻案 | canon_verdicts_2nd 表 / contradiction_pairs.json |
| 别名种子 | 词条 | 818 别名、42 个跨≥3 论文归并热点（hodge 26 卡/kakeya 13 卡…） | named_problem_seed.csv（未入库） |

### 已算但还漂在库外的（⚠️ 要收编）

| 指标 | 现状 | 收编去向（§三） |
|---|---|---|
| **P5 重要性** | 全量 6,752 条：五维概率向量 P → μ → I1-I5 档（I1 1228/I2 1730/I3 2438/I4 1337/I5 19）；置信分层 confident 1,889/boundary 4,426/disputed 437 | p5_ranking_assigned.jsonl → canonical_metric |
| **vitality 生命力** | 本机已算（vitality_local.py）；服务器版+月度重算是计划未落地 | → canonical_problem.vitality_score 缓存列 + metric_series 时序 |
| **M13 难度 BT 拟合** | attempts 299（四引擎）/ verdicts v1 150 + v2 107；fit v1 corr -0.975、v2 -0.761（36 题小样本，θ(glm-5.3)=-3.37 为千帆 32k 截断伪影须标注）；GLM×doubao 交叉验证一致率 67% | 本地 jsonl → m13_attempt / m13_verdict / engine_skill 三表 |
| **nap 分诊** | 2,674 张 not_a_prop 卡分诊（restated_open/background/confirm/unsure），早期信号翻回率低（350 张里 restated_open 仅 8） | nap_triage.jsonl → problems.triage 列 |

### 真缺、规划要覆盖的（❌）

| 缺口 | 出处 | 规划动作 |
|---|---|---|
| current_status 全 unknown | V2 §3.3 已有四步回填流程，未跑 | 按 V2 流程管线化，落 status_event |
| R3 基础知识路径 prerequisites | DATA_WORKPLAN R3，19 字段无此概念 | V3 DDL 加列 + LLM 生成 + 抽检（涉 schema 变更，不打补丁） |
| R1 精确原文索引物化 | 数据全有（arxiv_id+quote_location+crossref_doi），卡片视图没 join | 零 API，导出视图解决，不动表 |
| R2 MSC→中文分支名 | msc 码 100% 填充但无人话名 | 内置映射表 msc_name（码→中英分支名），小表一张 |
| 领域结构统计（MSC 分布/年代×状态/期刊画像） | DATA_WORKPLAN §三，部分已跑未沉淀 | 进 stats 快照导出，服务猜想发生学研究与冷启动分区 |

---

## 二、指标层设计原则（四条，与治理方案铁律对齐）

1. **证据层 / 派生层物理分离**。指标全部是派生数据：可从原始卡+外部数据重算，丢了不心疼，错了重算。原始卡永不被指标计算修改。
2. **provenance 三元组强制**（RATING §四.2 已立规矩）：任何 AI 参与产生的指标必须带 `{model_or_script, date, config_version}`；缺三元组的指标行拒绝入库。
3. **热指标列缓存、冷指标表时序**。排序/筛选要用的（vitality、importance_band、difficulty_band）放 canonical_problem 缓存列（V2 已预留）；历史值、多版本值、实验值一律进 metric_series 表，**缓存列只允许被最新一次正式重算覆盖，历史永不丢**。
4. **数据有归有，开不开放另说**（2026-09-29 用户拍板，优先级高于本文其他发布条款）：**所有指标一律先收编入库，采集阶段不做任何减法**——包括 AI 评分、引擎 θ、disputed 争议项、伪影数据，全部留。发布是独立的后置决策：每行指标带 `visibility` 位（`internal` 默认 / `research` 导师研究可见 / `public` 公开），前端只渲染 public。入库默认值一律 internal，升级 visibility 走人工，与 review_state 流程同轨。
5. **发布纪律**（作用于 visibility=public 的内容）：连续分后台存、前端只显示 band（★级）；0 比较/0 证据的条目显示"未评级"不显示分；AI 指标默认不升 public（RATING §四.3 冷启动规则继承）——但这是"默认档"不是"不采集"，与第 4 条不矛盾。

---

## 三、DDL 规划（指标层新增，与 V2 DDL 正交、可独立落）

> 本节所有指标表统一带 `visibility TEXT NOT NULL DEFAULT 'internal'`（internal / research / public，§二.4），下方各表 DDL 从略不重复书写。

### 3.1 canonical_metric：canonical 级指标物化（收编 P5/vitality/未来难度）

```sql
CREATE TABLE canonical_metric (
    canonical_uid TEXT NOT NULL REFERENCES canonical_problem(uid),
    metric        TEXT NOT NULL,
        -- 'importance_mu' | 'importance_band' | 'importance_confidence'
        -- 'vitality' | 'difficulty_beta' | 'difficulty_band'
    value_num     REAL,
    value_text    TEXT,              -- band/档位等离散值
    provenance    TEXT NOT NULL,     -- JSON: {script|model, date, config_version, batch_id}
    computed_at   TEXT DEFAULT (datetime('now')),
    PRIMARY KEY (canonical_uid, metric)
);
-- 热路径由触发器/重算脚本同步到 canonical_problem 缓存列；
-- 本表是唯一事实源，缓存列只是镜像
```

P5 的 6,752 条首批迁入；vitality 月度重算每次先写本表再刷缓存列，历史值进 3.3。

### 3.2 M13 难度体系三表（收编本地 jsonl）

```sql
CREATE TABLE m13_attempt (          -- 一次引擎对一题的求解尝试
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_uid TEXT NOT NULL,
    engine       TEXT NOT NULL,      -- 'glm-5.3' | 'dsr' | 'kimi-k3' | 'dsv4pro'
    attempt_json TEXT NOT NULL,      -- 完整尝试（思路/结论/自评）
    config       TEXT,               -- JSON：温度/max_tokens/截断参数（伪影追溯！）
    batch_id     TEXT,
    created_at   TEXT DEFAULT (datetime('now'))
);

CREATE TABLE m13_verdict (          -- 裁决：该尝试到了哪一步
    attempt_id   INTEGER NOT NULL REFERENCES m13_attempt(id),
    judge        TEXT NOT NULL,      -- 裁决引擎或 'human:<name>'
    level        INTEGER NOT NULL,   -- 1..5（五级量表）
    version      TEXT NOT NULL,      -- 'v1' | 'v2' | ...（量表版本，不同版本不可混算）
    note         TEXT,
    created_at   TEXT DEFAULT (datetime('now'))
);

CREATE TABLE engine_skill (         -- BT 拟合产物：引擎能力 θ
    engine       TEXT NOT NULL,
    fit_batch    TEXT NOT NULL,      -- 拟合批次（哪批 verdicts 拟的）
    theta        REAL NOT NULL,
    n_problems   INTEGER NOT NULL,   -- 拟合样本量（小样本必须带，如 v2 的 36）
    artifact_note TEXT,              -- 伪影标注：'qianfan-32k-truncation' 等
    corr_check   REAL,               -- 拟合质量（v1 -0.975 / v2 -0.761）
    computed_at  TEXT DEFAULT (datetime('now')),
    PRIMARY KEY (engine, fit_batch)
);
-- 题目难度 β 走 canonical_metric(metric='difficulty_beta')，不另建表
```

**纪律**：不同 version 的 verdict 不可混入同一次 fit（v1/v2 量表改过）；artifact_note 非空的 θ 值前端禁用、仅研究参考——千帆截断伪影这类坑必须永远跟着数据走。

### 3.3 metric_series：指标时序（活力月度重算、状态变迁的研究素材）

```sql
CREATE TABLE metric_series (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type TEXT NOT NULL,       -- 'canonical' | 'paper'
    entity_id   TEXT NOT NULL,
    metric      TEXT NOT NULL,       -- 'vitality' | 'n_citations' | ...
    value_num   REAL NOT NULL,
    provenance  TEXT NOT NULL,
    computed_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX idx_ms ON metric_series(entity_type, entity_id, metric, computed_at);
```

**这张表是"问题的一生"研究视角的直接数据源**：vitality 每月一个点、引用量每次抓取一个点，导师的猜想发生学研究和年代×状态趋势图都从这里出。

### 3.4 pairwise_comparison（继承 RATING_DESIGN_NOTE §三，一字不改）

```sql
CREATE TABLE pairwise_comparison (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    voter      TEXT NOT NULL,        -- 匿名 id；领域背景另记（per-rater 扩展预留）
    winner_uid TEXT NOT NULL,
    loser_uid  TEXT NOT NULL,
    relation   TEXT NOT NULL,        -- 'win' | 'near' | 'tie'（三档，不做比例输入）
    context    TEXT,                 -- 'difficulty' | 'importance'
    created_at TEXT DEFAULT (datetime('now'))
);
```

### 3.5 小表两张（零 API，顺手落）

```sql
CREATE TABLE msc_name (              -- R2：MSC 码 → 人话分支名
    code TEXT PRIMARY KEY,           -- '42B25'
    name_en TEXT NOT NULL,
    name_zh TEXT                     -- '调和分析（极大函数/奇异积分）'
);

CREATE TABLE stats_snapshot (        -- 领域结构统计快照（DATA_WORKPLAN §三产物）
    snapshot_date TEXT NOT NULL,
    stat_name      TEXT NOT NULL,    -- 'msc_distribution' | 'status_by_year' | 'journal_profile'
    payload        TEXT NOT NULL,    -- JSON
    PRIMARY KEY (snapshot_date, stat_name)
);
```

---

## 四、重算与生命周期策略

| 指标 | 重算频率 | 触发方式 |
|---|---|---|
| vitality / 引用时序 | 每月 | cron + 引用抓取后（DATA_WORKPLAN §二.4） |
| P5 重要性 | canonical 大变动后（新批次归并完成） | 手动触发，全量重算 |
| BT 难度/引擎能力 | verdicts 每 +50 条；平台期每日 | 半自动 |
| 领域结构快照 | 每季度 + 导师汇报前 | 手动 |
| nap 分诊 / difficulty_hint | 新卡批次后增量 | 管线挂接 |

**指标快照导出**：canonical_metric + metric_series + engine_skill 每季度导出 JSONL 进 git（与 V1 §五版本化一致）；实验性指标（exp_ 前缀 metric 名）不导出、随时可清。

---

## 五、落地顺序（依赖关系已排好）

1. **本批（不依赖定稿）**：R1 卡片视图 join（纯导出动）；named_problem_seed 818 条人工过表后入 named_problem 表（V2 DDL 已有）
2. **V3 DDL 定稿后**：§三全部新表落库；P5 6,752 条迁入 canonical_metric；M13 jsonl 收编三表；nap_triage 回填 problems.triage
3. **归一收官后**：vitality 月度重算部署 node01 cron；current_status 四步回填（V2 §3.3）
4. **平台期**：pairwise_comparison 接"今日二选一"UI；metric_series 出"问题的一生"时间线页
5. **V3 排期**：R3 prerequisites（schema 变更，随 V3 统一落，不打补丁——AUDIT_ADVERSARIAL 已警告过 schema 分叉）

## 六、待决（提请导师/安安——均为 visibility 发布层决策，一律不阻塞收编入库）

1. P5 的 disputed 437 条：visibility 怎么定（internal 留档 / research 供导师研究 / 标低置信升 public 发 band）？
2. engine_skill 的 θ 值：升 research 对导师开放吗？（引擎能力对比本身是 AI×数学研究素材）
3. metric_series 保留粒度：vitality 每月一点够吗，还是引用抓取每次都记？
