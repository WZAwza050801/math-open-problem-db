# 数学开放问题库 · 数据库设计 v2（讨论稿）

> 2026-09-26 · 基于 DB_DESIGN_V1（2026-09-23 讨论稿）+ 五大刊跑批收官实测 + 归一原型实测
> 状态：讨论稿——导师定稿后落 DDL。V1 的需求决议、路线图、标签体系、技术栈全部继承，本文不重复，只写**变更与新增**。

---

## 一、V1 → V2 的变更驱动（全部来自实测，不是拍脑袋）

| 实测事实 | 对设计的驱动 |
|---|---|
| 卡量定格 **7,471**（818 论文），`paper_time_status` 四类分布实测（open 2,183 / solved 2,179 / not_a_prop 2,090 / bg_known 1,019） | canonical 归并规模假设从"573 卡"更新为 ~7.5k 卡；归并候选对数量级 ~O(10⁷)，**必须分层召回**，不能全对全 LLM |
| `current_status` 全 unknown；1,869 卡自标 flag_for_human | status_event 的回填必须设计为**管线可跑的批量任务**，不是手工 |
| citations.jsonl 39,426 条已挂接（806/818 篇有引用，表 `citations` + `paper_cite_stats` 已在服务器库落地，integrity ok） | 生命力指标可以直接从 `paper_cite_stats` 聚合，canonical 表需要预留 `vitality` 缓存列 |
| FTS5 召回原型（9 种子）：关键词 OR 查询召回**太宽**（Milnor 猜想种子召回的 12 候选 0 命中，全是同领域词汇共振） | 归一召回 = **短语级 FTS5 + embedding（bge-m3，SiliconFlow key 实测可用）双通道**，纯关键词路线否决 |
| SiliconFlow key 可用 bge-m3 / Qwen3-Embedding / Reranker 全家 | embedding 列设计进 V2（每卡一存，7.5k × 1024 维 ≈ 30MB，SQLite 无压力），**不再后置** |
| 32 篇 2000 年论文无 TeX 全文（PDF 扫尾待做） | source_kind 已有 pdf 字段；canonical 的 origin 追溯要容忍"仅有 PDF 证据"的卡 |

---

## 二、归一管线（canonical 判定的标准流程）

```
7,471 张卡
   │
   ▼ ① 候选召回（双通道，各取 top-k，并集）
   ├─ FTS5 短语通道：self_contained 的 4-gram 关键短语（非单词 OR）
   └─ embedding 通道：bge-m3 余弦 top-k（1024 维，卡级预计算）
   │
   ▼ ② LLM 裁决（降级链：glm-5.3 → Token Plan qwen3.8-max → SF Kimi-K2.6）
   │   verdict ∈ {same, distinct, unsure} + reason + confidence
   │   成本核算：原型 12 候选/次 ≈ 3k in + 5k out ≈ 每卡 1 次调用
   │
   ▼ ③ 分组（union-find）
   │   same 边合并；unsure 挂起不合并（宁缺勿滥原则，V1 §六.1）
   │
   ▼ ④ canonical 生成
   │   每组选代表卡（最长 self_contained 且 open_at_paper_time 优先）
   │   statement_rewritten 由 LLM 改写，挂 review_state=draft
   │
   ▼ ⑤ 人工抽检（老师介入点）
       每批抽 5% 组查验：错并（拆）/漏并（合）
```

**关键决策（原型实测后修正）**：
- 单词 OR 的 FTS5 查询召回噪声过高（同领域卡共享太多词汇），改用**关键短语**（从 self_contained 抽 3-5 个名词短语做 phrase MATCH）+ embedding 双通道互补
- `unsure` 不合并：V1 的"宁缺勿滥"落地为 union-find 只吃 `same` 边
- embedding 预计算一次全量 ~7.5k 卡（bge-m3 批量 API，实测成本极低）

**召回实验定稿（2026-09-26，RECALL_EXPERIMENT_REPORT.md）**：
- bge-m3 暴力余弦（7,471² 全算，numpy 秒级）碾压 FTS5 word-OR：RH recall@20 44% vs 2.2%（20×）
- **裁决预算落定：cos>0.80 → 3,392 对 ≈ 5.1 万积分，一周 GLM 额度内可跑完全量**；
  从 0.80 起步，人工抽检 0.70-0.80 区间样本决定是否下探
- bge-m3 全量 embedding 已完成（196s / 31MB，embeddings.npy 断点可续）

---

## 三、DDL v2（SQLite，阶段 A 直接落地）

### 3.1 canonical_problem

```sql
CREATE TABLE canonical_problem (
    uid             TEXT PRIMARY KEY,        -- 'op-2026-000001'，永不变
    statement_en    TEXT NOT NULL,           -- 规范化陈述（发布版）
    statement_zh    TEXT,                    -- 中文陈述（后置翻译）
    status          TEXT NOT NULL DEFAULT 'open',
        -- open | solved | partially_solved | controversial
        -- 由 status_event 最新事件推导，此列是缓存
    origin_arxiv_id TEXT,                    -- 首次提出处（关联 papers）
    origin_year     INTEGER,
    msc_primary     TEXT,                    -- MSC2020 二级码，如 '14J60'
    msc_secondary   TEXT,                    -- JSON 数组
    vitality_score  REAL,                    -- 生命力缓存（见 3.5），定期重算
    review_state    TEXT NOT NULL DEFAULT 'machine_extracted',
        -- machine_extracted | draft | human_verified | published
    origin_type     TEXT NOT NULL DEFAULT 'journal_mined',
        -- 见 §5 origin_type 规范
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT
);
```

### 3.2 problem_card（即现有 problems 表的挂接视图，卡一 张不丢）

```sql
-- 现有 problems 表不动，只加一列：
ALTER TABLE problems ADD COLUMN canonical_uid TEXT REFERENCES canonical_problem(uid);
-- 归并=填 uid；拆并=清空 uid。全部历史可逆。
ALTER TABLE problems ADD COLUMN verdict_note TEXT;  -- 归并时 LLM 的 reason 存档
```

### 3.3 status_event

```sql
CREATE TABLE status_event (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_uid TEXT NOT NULL REFERENCES canonical_problem(uid),
    event_type   TEXT NOT NULL,
        -- proposed_at_paper | solved_in_paper | claimed_solved | disputed |
        -- background_known_open | human_verified | external_source
    source_arxiv_id TEXT,                    -- 依据哪篇论文
    source_card_id  TEXT,                    -- 依据哪张卡（可空：外部来源）
    source_url      TEXT,                    -- 外部来源（arXiv abs 页/维基等）
    year         INTEGER,                    -- 事件发生年（citation 网络可推）
    note         TEXT,
    created_at   TEXT DEFAULT (datetime('now'))
);
CREATE INDEX idx_se_uid ON status_event(canonical_uid, year);
```

**回填流程（管线化）**：
1. `proposed_at_paper`：从 origin 卡直接生成（每组 1 条）
2. `solved_in_paper` / `background_known_open`：从组内其他卡的 paper_time_status 生成（时间线 = 各卡 pub_year）
3. `external_source`：current_status 校对阶段，按 canonical 的引用网络查后续声称解决的论文（OpenAlex cited_by 检索），LLM 判真伪，挂 `claimed_solved`（不直接改 status）
4. `human_verified`：审计阶段老师回填

### 3.4 problem_relation / named_problem / ingest_batch（继承 V1，落 DDL）

```sql
CREATE TABLE problem_relation (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    from_uid  TEXT NOT NULL REFERENCES canonical_problem(uid),
    to_uid    TEXT NOT NULL REFERENCES canonical_problem(uid),
    kind      TEXT NOT NULL,
        -- specializes | generalizes | equivalent_to | implies |
        -- motivated_by | appears_in
    evidence_card_id TEXT,                   -- 哪张卡/哪篇论文说的
    source_arxiv_id  TEXT,
    review_state TEXT NOT NULL DEFAULT 'machine_extracted',
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE named_problem (
    alias     TEXT NOT NULL,                 -- 'Poincare conjecture' / '庞加莱猜想'
    alias_norm TEXT NOT NULL,                -- lower/去重音/去标点，检索键
    lang      TEXT NOT NULL DEFAULT 'en',    -- en | zh | abbrev
    canonical_uid TEXT REFERENCES canonical_problem(uid),
    source    TEXT,                          -- wikipedia | polymath | manual
    PRIMARY KEY (alias_norm, lang)
);

CREATE TABLE ingest_batch (
    batch_id   TEXT PRIMARY KEY,             -- 'ar5iv-5journal-2026-09' / 'oeis-2027-01'
    dataset    TEXT NOT NULL,                -- ar5iv_5j | oeis | polymathwiki | manual | ...
    note       TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
ALTER TABLE problems ADD COLUMN batch_id TEXT DEFAULT 'ar5iv-5journal-2026-09';
```

### 3.5 生命力指标（vitality_score，从 paper_cite_stats 聚合）

```
vitality = log1p(n_total) + 2·log1p(n_2021_2026)     -- 近五年权重加倍
         + 1.0 × (latest_citing == strftime('%Y','now'))
```
按 canonical 的全部成员卡所涉论文求和。只做排序提示，不做权威声明。

---

## 四、embedding 方案（V1 后置 → V2 落地）

- 模型：**bge-m3**（SiliconFlow，1024 维，中英双语，实测 key 可用）
- 存储：`problems.embedding BLOB`（float32 × 1024 = 4KB/卡，全量 ~30MB）
- 生成：批量 API，7,471 卡一次全量（约几百万 token，成本可忽略）
- 用途：归一召回通道二、"找相似问题"（发布后刚需）、关系抽取辅助

---

## 五、origin_type 标注规范（新增字段，多数据集注入的准入标记）

| origin_type | 定义 | 审核策略 |
|---|---|---|
| `journal_mined` | 五大刊管线抽取（当前 7,471 卡） | review_state 从 machine_extracted 起步 |
| `external_import` | OpenConjecture / ProofAtlas / Wikipedia 等批量导入 | 强制 review_state=draft，先人工抽检再 published |
| `user_submitted` | 平台上线后用户添加 | review_state=draft，社区/老师审核后 published |
| `manual_curated` | 管理员手建 | 直接 human_verified |

## 六、ProofAtlas / OpenConjecture 字段映射（初稿，调研待落稿核对）

> **2026-09-29 更新**：外部数据源全景调研已完成并落成独立方案文档 **`EXTERNAL_SOURCES_PLAN.md`**（UnsolvedMath / OpenConjecture / DeepMind Formal Conjectures / erdosproblems / Open Problem Garden / MathDB 等 20+ 源，含优先级排期 P0-P2、统一 ingest 管线设计与风险清单）。本节下方映射表为其 OpenConjecture/ProofAtlas 部分的初稿，注入落地以该文档为准。

| 本库字段 | OpenConjecture | ProofAtlas（Top 500 形式化库） |
|---|---|---|
| uid | conjecture_id | atlas_id |
| statement_en | statement (plain) | formal_statement (Lean 4) |
| status | status (open/proved/disproved) | proof_status (formalized?) |
| origin_year | first_proposed | —（以文献为准，本库优先）|
| msc_primary | subject tags | subject classification |
| problem_relation | related_conjectures | dependency/implication 图 |
| —（本库强项） | — | formal_proof 链接（存 note/source_url）|

**互补层定位**（继承用户 2026-09 研究侧规划）：本库 = 文献挖掘层（提出处/引用网络/状态史）；OpenConjecture = 社区层；ProofAtlas = 形式化层。三者以 uid + DOI 互链，不重复建条目，`origin_type=external_import` + `source_url` 指向对方即可。

---

## 七、原型实测结果（2026-09-26 完成，详见 canon_prototype/CANON_PROTOTYPE_REPORT.md）

- **9 种子 × 12 候选 = 108 对裁决**：same=5（4.6%）/ unsure=0 / distinct=103，零调用失败
- **famous 种子 3/4 颗粒无收**（Milnor/RH/Hodge 的 same=0）：单词 OR 的 FTS5 召回是"同领域词汇共振"，不是同一问题本体 → §二的双通道改版依据坐实
- **intra_paper 种子 same=4/60（6.7%）**：同篇拆卡重复真实存在（0808.2952×1、0707.2340×2、math/0210111×1），是全量归一第一批要处理的重复
- **裁决成本**：平均 in 2.8k / out 4.5k tokens/次（9 次调用，SF Kimi-K2.6 Pro）；qwen3.8-max thinking 模式 >6min/次只配保底
- **unsure=0 的警示**：Kimi 自信度偏高，全量归一时 distinct 侧需随机抽 10% 复查漏并
- 5 对 same 已列详情供人工查验（报告 §二）；GLM 额度 9/29-9/30 重置后全量归一切回 glm-5.3

---

## 八、待办（V2 定稿前）

> **2026-09-29 更新**：归并/冲突/运维/权限的完整工程方案见 **`DB_GOVERNANCE_PLAN.md`**（merge_log/audit_log/conflict_queue/schema_migrations 四张新表 DDL、备份 3-2-1、RBAC 与双人规则、分阶段落地表）；外部数据源注入见 **`EXTERNAL_SOURCES_PLAN.md`**；指标层（P5/vitality/M13 难度/BT 拟合/时序）收编规划见 **`DB_METRICS_PLAN.md`**。三份与本文一并交导师。

1. [ ] 原型跑完 → 回填 §七，按实测修召回参数
2. [ ] 交导师过目 §三 DDL + §五 origin_type
3. [ ] 定稿后：服务器库落 DDL（幂等脚本，不动现有表）
4. [ ] bge-m3 全量 embedding 预计算
