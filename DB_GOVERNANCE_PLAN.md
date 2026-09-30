# 数据库治理与运维方案（DBA 视角，讨论稿）

> 2026-09-29 · 基于 DB_DESIGN_V1/V2 + EXTERNAL_SOURCES_PLAN + 现有管线实测（9,223 卡 / canonical 6,868 / 裁决 2,305 对）
> 状态：讨论稿——与 V2、EXTERNAL_SOURCES_PLAN 一并交导师过目
> 覆盖四大问题域：**重复归并、卡片冲突、数据库管理、权限**，外加审计回滚与质量门禁。目标是：在任何事故（错并、污染、密钥泄漏、误删、schema 变更踩坑）发生之前，路径已经铺好。

---

## 一、工程铁律（全方案的前提，六条）

1. **可逆优先于正确**：任何写操作必须能回滚。归并可拆、状态有事件链、卡片永不物理删除（tombstone）、外部注入整批可撤。
2. **单写者**：阶段 A 任何时刻只有一个进程持有 DB 写权。多车道并行只并行"算"，不并行"写"（计算结果落 jsonl，由单一 ingestor 串行入库）。
3. **先落证据，后改结论**：原始卡、原文 quote、外部源原文永不可变；所有"结论类"字段（status、statement_rewritten、canonical 归并）都是可重算、可覆盖的派生层。
4. **门禁前置**：垃圾（低质量卡、AI 幻觉、未验证外部状态）在入库闸口拦截，不进公开检索；`review_state` 是唯一通行证。
5. **一切留痕**：机器决策记 reason，人工决策记人名，批量操作记 batch_id。没有 audit_log 的操作等于没做过。
6. **实验不碰生产**：实验/原型一律影子表或副本库（`archive_db_v1_polluted.sqlite3` 的教训：库曾被实验数据污染，只能整体归档重来）。

---

## 二、重复与归并治理（Dedup & Merge）

### 2.1 三级重复模型（先分清敌人是谁）

| 级别 | 重复形态 | 实测证据 | 危害 |
|---|---|---|---|
| L1 同卡重复 | 同篇论文同一问题被重抽/重跑产生两张卡 | intra_paper 种子 same=4/60（0808.2952×1、0707.2340×2、math/0210111×1） | 计数虚胖、裁决对数爆炸 |
| L2 跨卡同问题 | 不同论文提到同一猜想（正常归并对象） | 裁决 2,305 对中 same=673（29%） | 社区看到一个问题的多个碎片条目 |
| L3 跨源重复 | 外部注入与本库、外部源之间的重复（Erdős 问题会从 UnsolvedMath/Formal Conjectures/erdosproblems 进三次） | EXTERNAL_SOURCES_PLAN §六.3 | 注入后 canonical 总量虚高 |

**原则：L1 在入库闸口消灭，L2 由归并管线处理（这是功能不是 bug），L3 由对撞归并处理。**

### 2.2 防线一：入库防重（写入时 dedup，零 LLM 成本）

```
INSERT 前三级短路检查：
1. 论文级：  (arxiv_id, source_anchor) 已存在 → 跳过（重跑幂等）
2. 内容级：  statement_hash = sha1(normalize(verbatim_quote))
            normalize = lower + 去空白/LaTeX 控制序列 + 去标点
            hash 命中同论文 → 跳过；命中跨论文 → 正常入库但预标
            merge_hint='content_dup'（喂给归并管线当高优先候选对）
3. 外部注入：content_hash 或 source_id（A2 原生带 content_hash）幂等跳过
```

**落库要求**：`problems` 表加 `statement_hash` 列（回填一次历史数据，唯一索引不加——hash 相同但语义不同的情况允许共存，交给 L2 管线判）。

### 2.3 防线二：归并判定（现有管线 + 加固）

现有链路（V2 §二）已实测：bge-m3 召回（cos>0.80 → 3,392 对）→ LLM 裁决（same/distinct/unsure）→ union-find 只吃 same。**在此基础上加固三点**：

1. **二裁机制常态化**（已有 `canon_verdicts_2nd` 表与 `canon_second_opinion.py` 原型）：
   - unsure 全部二裁（50 对实测：二裁后仅剩 5 对仍 unsure）
   - **一裁 same × 二裁 distinct 的矛盾对**（实测 84 对中 37 对被二裁翻案）→ 全部进人工队列，这是错并率的主要来源
   - distinct 侧随机抽 10% 复查漏并（V2 §七已定，Kimi 自信度偏高的教训）
2. **归并质量双指标**（每批归并跑完必报）：
   - 错并率 = 抽检中被判"应拆"的组数 / 抽检组数（目标 < 2%）
   - 漏并率 = distinct 复查中被判"应并"的对数 / 复查对数（目标 < 5%，宁缺勿滥允许偏高）
3. **合并即生成，拆分留痕迹**：

```sql
CREATE TABLE merge_log (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    action       TEXT NOT NULL,        -- merge | split
    card_id      TEXT NOT NULL,
    from_uid     TEXT,                 -- split 时的原 uid
    to_uid       TEXT,                 -- merge 时的目标 uid
    actor        TEXT NOT NULL,        -- 'pipeline:canon_judge_v2' | 'human:导师' | 'pipeline:external_ingest'
    verdict      TEXT,                 -- same / unsure / manual
    reason       TEXT,                 -- LLM reason 或人工备注
    batch_id     TEXT,
    created_at   TEXT DEFAULT (datetime('now'))
);
-- 拆并 = 读 merge_log 反向回放；卡片本身永远不动，只改 canonical_uid 指针
```

### 2.4 防线三：拆并工具（SOP，不等出事再写）

- `canon_split.py <uid> <card_id...>`：把指定卡从 canonical 摘出，新建独立 uid，写 merge_log(action=split)，重算两边 statement/vitality/MSC
- `canon_merge.py <uid_a> <uid_b>`：B 组全部卡改指 A，B 的 uid 保留为墓碑（`canonical_problem.merged_into` 列），外部引用 B 的旧链接 301 到 A——**uid 永不复用、永不失效**（V1 "uid 永不变"的精确语义）
- 两个命令都必须 `--dry-run` 先行，输出影响面（几张卡、几个关系、几条 status_event）再执行

---

## 三、卡片冲突治理（Card Conflict）

### 3.1 冲突分类法（八类，全部实测或高概率预见）

| # | 冲突 | 实例 | 默认处理 |
|---|---|---|---|
| C1 | 同 canonical 内状态矛盾 | 组内一卡 open_at_paper_time、另一卡 solved_in_paper（Eremenko 案例：2009 open / 2025 solved——**这是正常时间线不是冲突**） | 仅当**同年同状态矛盾**才算冲突：进 conflict_queue |
| C2 | 本库 vs 外部源 status 矛盾 | 本库推 open，MathDB/erdosproblems 说 solved | 只落 external_source 事件，不改 status，进人工队列（EXTERNAL_SOURCES_PLAN §一.5） |
| C3 | 同名不同题 | "Berry conjecture" 出现在物理与数论两处 | named_problem 别名挂多 uid（alias_norm+lang 主键允许一对多），检索端消歧 |
| C4 | 同题异名 | RH = Riemann Hypothesis = 黎曼猜想 | named_problem 字典收敛，抽取卡的原 label 保留为证据 |
| C5 | canonical 陈述互相覆盖 | 多次重跑 statement_build 覆盖已人工改过的陈述 | 人工改过的行加锁：`statement_locked=1`，管线跳过 |
| C6 | MSC 标注分歧 | 同组卡挂不同 MSC | 取组内众数进 msc_primary，其余进 msc_secondary，分歧>2 个进抽检 |
| C7 | 重抽版本漂移 | 同一论文换 prompt 重抽，卡数/内容变化 | 新批次不删旧卡：旧卡 tombstone + superseded_by 指向新卡 |
| C8 | AI 声称解决 vs 文献无据 | OpenConjecture/ProofAtlas 的 GPT 声称 solved | event_type=claimed_solved（V2 §3.3 已定），永不直接改 status |

### 3.2 conflict_queue：统一冲突队列（新表）

```sql
CREATE TABLE conflict_queue (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    conflict_type TEXT NOT NULL,       -- C1..C8
    canonical_uid TEXT,
    card_ids     TEXT,                 -- JSON 数组
    detail       TEXT,                 -- JSON：双方值、来源、证据
    detected_by  TEXT NOT NULL,        -- 'rule:<规则名>' | 'pipeline:<脚本>' 
    status       TEXT NOT NULL DEFAULT 'open',
        -- open | auto_resolved | adjudicated | human_queue | resolved | wont_fix
    resolution   TEXT,                 -- 处理结论 + 依据
    resolved_by  TEXT,
    created_at   TEXT DEFAULT (datetime('now')),
    resolved_at  TEXT
);
```

**检测 = 一组 SQL 视图/定时脚本**（每日巡检顺带跑，零 LLM）：
- C1：`SELECT canonical_uid FROM problems GROUP BY canonical_uid, pub_year HAVING count(distinct paper_time_status in (open,solved)) > 1`（伪码，落地时按真实列名）
- C2：status_event 中 external_source 事件与推导 status 不一致的 uid
- C5：statement_locked=1 与管线待写集合的交集（应为空，非空即有人绕过锁）
- C7：同 arxiv_id 多 batch_id 的卡集

### 3.3 处理路由（按成本升序，能自动绝不人工）

```
冲突进队列
  ├─ 规则可解（C2/C8 默认保留本库结论、C4 字典收敛）→ auto_resolved，写 resolution
  ├─ LLM 二裁（C1/C3/C6，单对单呼，走 team2 额度）→ adjudicated + verdict 存档
  └─ 必须人工（二裁仍矛盾、涉有名问题、涉状态翻转）→ human_queue
       └─ 对接 HUMAN_REVIEW_BACKLOG.md，老师批量裁决时段统一处理
```

**红线**：human_queue 里带"有名问题"（named_problem 命中）的条目优先级最高——错一个 RH 比错一百个无名问题代价大。

---

## 四、数据库管理（DBA 运维）

### 4.1 写路径白名单（阶段 A 全部写入入口，就这四个）

| 写路径 | 频率 | 说明 |
|---|---|---|
| `run_pilot.py`（抽取 ingestor） | 批次 | 唯一往 problems 写新卡的入口 |
| `canon_judge.py` → union-find ingestor | 批次 | 唯一改 canonical_uid 的入口（二裁/人工也通过它回放，不直接改库） |
| 状态/评分回填脚本（status_events、p5、vitality） | 批次 | 只写派生表，不碰原始卡 |
| 人工工具（canon_split/merge、review 回填） | 按需 | 全部经 merge_log/audit_log |

任何新脚本要写库 → 先在本文白名单登记。多车道并行（GLM slice1 / 千帆 slice2）只并行抽取**计算**，入库由单 ingestor 串行消费 jsonl——现有架构已是这样，固化为纪律。

### 4.2 备份策略（现状：仅 2 份手动备份，**这是当前最大运维缺口**）

目标 **3-2-1**（3 份、2 种介质、1 份异地）：

| 层 | 内容 | 频率 | 保留 |
|---|---|---|---|
| 热备 | node01 上 `sqlite3 db.sqlite3 ".backup backups/db_$(date +%F_%H%M).sqlite3"`（cron） | 每日 04:00 | 本地留 14 天 |
| 异地 | scp 热备回本机 `open_problem_db/backups/` | 每日（热备后） | 本机留 90 天 |
| 逻辑导出 | 全表 JSONL → git 仓 commit（batch_id 前缀） | 每次跑批后 | 永久（git 历史即时间机） |
| 快照 | 重大变更前手动快照（`db.m13_snapshot.sqlite3` 模式，已有先例） | 按需 | 永久 |

落地动作：写一个 `backup_daily.sh`（热备+scp+旧备份清理）挂 node01 cron，替代手动。**RPO ≤ 24h，RTO ≤ 4h**（从 git JSONL 全量重建 + 最近热备校验）。

### 4.3 健康巡检（固化每日 automation，已有雏形）

每日巡检项（按序，任一失败即告警）：
1. `PRAGMA integrity_check;` → 必须 ok
2. 行数对账：papers / problems / canonical / verdicts 环比（昨日 → 今日），负增长即异常
3. 孤儿检查：`canonical_uid IS NOT NULL AND canonical_uid NOT IN (SELECT uid FROM canonical_problem)`（归并脚本 bug 探针）
4. 队列水位：conflict_queue open 数、flag_for_human 数、human_queue 数（超阈值提醒老师档期）
5. 磁盘与体积：db 文件大小、WAL 文件大小（>500MB 触发 checkpoint）
6. 进程真空：管线进程清单 vs 预期（防止僵尸车道写库）

### 4.4 Schema 版本化与迁移纪律

```sql
CREATE TABLE IF NOT EXISTS schema_migrations (
    version     TEXT PRIMARY KEY,     -- 'v001_add_statement_hash'
    applied_at  TEXT DEFAULT (datetime('now')),
    note        TEXT
);
```

变更流程（不可跳步）：**讨论稿修订 → 导师过目 → 手动快照 → 幂等迁移脚本（`IF NOT EXISTS` 全程，可重跑）→ 迁移后 integrity + 行数对账 → git 导出 commit**。回滚预案 = 恢复快照（SQLite 无原生 DDL 回滚，不赌）。

### 4.5 索引与体积维护 SOP

- 每月或每 +5k 卡：`ANALYZE;` + `PRAGMA wal_checkpoint(TRUNCATE);`
- FTS5：新增批次后增量索引；重建（`INSERT INTO fts(fts) VALUES('rebuild')`）仅在大批量注入后
- embedding：新增卡补算（bge-m3 批量 API），全量重建只在换模型时（换模型 = 新列 `embedding_v2`，新旧并存到归一验证通过，**不原地覆盖**）
- `VACUUM` 仅在大规模 tombstone 清理后，且必须停机 + 快照先行（VACUUM 重写全库）

### 4.6 SQLite → PostgreSQL 迁移触发条件（阶段 B 前夜）

触发任一即启动：① 出现并发写需求（平台上线用户提交）；② 单表 > 50 万行；③ 需要行级权限/角色。路径：`sqlite3 .dump` → pgloader → 双写校验一周 → 切流。FTS5 → pg_trgm/Meilisearch 的检索替换在阶段 B 方案里另议，uid 与表结构保持 1:1 映射（V1 §五已定）。

### 4.7 污染隔离（从 archive_db_v1_polluted 学到的）

- 实验表一律 `exp_` 前缀，或干脆副本库（`canon_prototype/canon_db.sqlite3` 模式，已正确）
- 外部注入每个 batch 独立 commit，整批回滚 = 按 batch_id 删卡 + 摘 uid + 导出 revert（EXTERNAL_SOURCES_PLAN §四）
- AI 生成字段（外部源综述、LLM label）与原始证据**分列存放**，污染扩散面最小化

---

## 五、权限体系

### 5.1 阶段 A（现在）：文件系统即权限

| 资产 | 控制 |
|---|---|
| API keys | KEYS_LEDGER 别名制；`.glm_key`/`.team2_key`/`.qianfan_key` 等一律 `chmod 600`，node01 与本机同规；**key 永不入库、永不进 git、聊天不贴明文**（用户既定纪律） |
| DB 文件 | node01 仅管线账户可写；本机副本只读分析 |
| git 导出仓 | 推送前 secret scan（`git grep -E 'sk-|gho_|AIza'` 等模式跑一遍）；导出脚本默认剔除任何 `*_key`/`.env` 邻接文件 |
| 巡检/自动化 | automation 账户只读 DB（SELECT only 的连接串） |

### 5.2 阶段 B（平台）：RBAC + 字段级写权限

| 角色 | 能做什么 | 不能做什么 |
|---|---|---|
| visitor | 检索、阅读 published | 一切写 |
| member（注册） | 评论（讨论层）、提交 user_submitted 条目（draft）、给关系投票 | 改 canonical 任何字段 |
| curator（管理员任命） | 合并/拆分、改 statement_rewritten、打标签 | 改 status、删卡 |
| reviewer（老师/专家） | 改 status（写 status_event + human_verified）、裁决 human_queue、publish | 删库级操作 |
| admin | 迁移、备份恢复、角色授予 | 绕过 audit_log（无此路径） |

**状态迁移权限矩阵**（review_state）：

```
machine_extracted ──(curator 抽检)──> draft ──(reviewer)──> human_verified ──(reviewer)──> published
       │                                  ▲                                     │
       └── 任何角色可降级回上一态 ──────────┘      published 回退需 admin + 理由（audit）
```

### 5.3 双人规则（发布闸口）

- 有名问题（named_problem 命中）的 status 变更：**reviewer 一人提议、另一 reviewer 或 admin 确认**才落 published
- 外部源声称 solved → published 之间**必须**有 human_verified 环节，AI 声称永远不能直接翻转公开状态（MathDB/VibeMathed 的前车之鉴：数学界已在批评未验证 AI 声称泛滥）

### 5.4 对外策略

- 公开导出 = 只读 API / 定期 dump，按 uid 引用；CC BY-SA 4.0 建议（数据），verbatim_quote 不发（V1 §七版权决议：发布版只用改写陈述）
- robots/AI 抓取政策：允许抓 published 层并附署名要求；draft 层不出网

### 5.5 AI 内容展示纪律（V1 §九定位宣言的执行条款，阶段 B 界面/接口必须遵守）

1. **署名不可混淆**：任何页面上的内容必须能被一眼区分"人写的 / 机器生成的"。AI 内容带模型名+生成时间+验证等级三件套；缺一件不许渲染。
2. **验证等级可视化**：借鉴 ProbXiv 四级（unverified / LLM-verified / formalized / human-endorsed），映射本库 review_state。等级跃迁只能由机器检验（Lean 等）或 reviewer 完成；AI 自述的"我证明了"永远停在 unverified。
3. **解释权独占**：status（open/solved/…）的最终裁定、canonical 陈述的 published 版、问题页的"权威解释"位，只接受 human_verified 内容。AI 的解读可以存在，但永远排在人的内容之后、视觉上次级。
4. **讨论区防灌水**：AI 生成帖子默认折叠+标色；同一账户高频 AI 味内容触发 curator 复核；研究者（实名/机构认证）内容享有排序优先。这条是定位本体，不是 UX 细节——讨论氛围毒化 = 项目失败（MathDB 前车之鉴）。

---

## 六、审计与回滚

### 6.1 统一审计表（所有写操作的终点）

```sql
CREATE TABLE audit_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    actor      TEXT NOT NULL,       -- 'pipeline:<script>@<host>' | 'human:<name>' | 'automation:<id>'
    action     TEXT NOT NULL,       -- insert_card | merge | split | status_change | statement_edit | publish | ingest_batch | rollback ...
    target     TEXT NOT NULL,       -- 'card:<id>' | 'uid:<uid>' | 'batch:<id>' | 'table:<name>'
    before     TEXT,                -- JSON 快照（改前值）
    after      TEXT,                -- JSON 快照（改后值）
    reason     TEXT,
    batch_id   TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX idx_audit_target ON audit_log(target, created_at);
```

merge_log / conflict_queue / status_event 是审计的**领域视图**，audit_log 是总账。四者并存不冗余：领域表支撑业务查询，audit_log 支撑"这行数据这辈子经历了什么"。

### 6.2 可逆性核对清单（每条都有对应机制）

| 操作 | 回滚方式 |
|---|---|
| 错误归并 | canon_split + merge_log 反向回放 |
| 错误状态 | status_event 追加纠正事件（事件链不删改） |
| 错误陈述 | statement 改前快照在 audit_log，恢复 + 加锁 |
| 外部注入整批事故 | 按 batch_id 删卡 + 摘 uid + git 导出 revert |
| schema 迁移踩坑 | 恢复变更前手动快照 |
| 库物理损坏 | 最近热备 + git JSONL 全量重建（RPO 24h） |

### 6.3 灾难恢复演练

每季度一次：随机挑一天的热备恢复到临时库 → integrity_check + 行数对账 + 抽 10 个 uid 人工比对。**没演练过的备份等于没有备份。**

---

## 七、质量门禁与抽检（把已有机制串成体系）

1. **入库门禁**（已有）：quality_score 低于阈值 → review_state=blocked（RH 主簇 5 张背景卡被正确拦截的正面案例）；`validate_cards.py` 为闸口实现
2. **分诊门禁**（已有）：nap_prefilter 把 not_a_proposition 卡分流，restated_open 翻回独立队列
3. **抽检 SOP**（每个大批量动作后）：归并 5% 组查验 / distinct 10% 漏并复查 / 外部注入批 5% / 有名问题全量人查
4. **人工队列统一入口**：HUMAN_REVIEW_BACKLOG.md（文档）→ 逐步表化进 conflict_queue(status=human_queue)，老师一个界面看全部待裁
5. **指标上报**：每周一报（错并率、漏并率、队列水位、外部源冲突数）进周记，导师可见

---

## 八、分阶段落地表

| 阶段 | 动作 | 前置 |
|---|---|---|
| **现在（定稿前）** | 本文 + V2 + EXTERNAL_SOURCES_PLAN 交导师；备份自动化脚本 backup_daily.sh（不依赖定稿，纯运维） | 无 |
| **定稿后第一批** | statement_hash 列 + 入库防重（§2.2）；merge_log/audit_log/conflict_queue/schema_migrations 四表落 DDL；canon_split/merge 工具 | DDL 定稿 |
| **归一收官时** | 二裁常态化 + 双指标报告（§2.3）；矛盾对 84 对进 human_queue | 全量裁决完成 |
| **外部注入前** | 冲突检测规则上线（§3.2）；每批注入整批回滚演练一次 | P0 注入启动 |
| **阶段 B 前夜** | RBAC 落地 + PG 迁移 + 灾难恢复演练制度化 | 平台选型 |

## 九、待决问题（提请导师/安安拍板）

1. published 状态的对外许可：CC BY-SA 4.0 是否可接受？（影响讨论层内容归属）
2. reviewer 双人规则的人员池：除导师外是否需要第二位专家？
3. human_queue 的裁决节奏：每周固定时段还是攒批？
4. 本机副本的只读纪律是否接受（分析一律打副本，不直连 node01 生产库）？
