# 执行计划 · M4-M8 微步标准化拆解（2026-09-27）

> 原则：每步 = 冻结输入 → 执行 → 输出落盘 `runs/<run_id>/` → 验收条件 → 不达标不前进。
> 全程只需 API + node01 服务器，**零外部数据**；人类判断压缩到最后一次 5 分钟抽检。
> 偏离 SOP 之处以 ADR 记录（本文件附 ADR-001/002 草案）。

## API 预算总表

| 阶段 | 调用量 | 引擎 | 预计耗时 |
|---|---:|---|---|
| P0 金标准盲测 | ~75 | 3 引擎各 25 题 | 10 分钟 |
| P1 锚点判档 v0 | ~378（可循环 +1 轮） | 3 引擎各 126 | ~40 分钟 |
| P2 规范陈述+核验 | ~1,600 | GLM 生成 + Kimi 核验 | 2-3 小时 |
| P3 特征快照 | 0 | 本地代码 | 分钟级 |
| P4 300 条 pilot | ~390 | GLM 主 + 升级链 | 1-2 小时 |
| P5 全量评分 | ~7,800 | 同上 | 过夜 |

---

## P0 金标准盲测（判卷闸门，SOP 之外的增补闸门）

| 步 | 内容 | 产物 | 验收 |
|---|---|---|---|
| S0.1 | 构建金标准集：静态硬编码 25 题（12 道 I5/I4 千禧年级 + 8 道 I1/I2 教科书级 + 5 道已解决著名题），每题附共识档位+一句依据；题目尽量映射到库内 canonical 取真实陈述 | `runs/p0/gold_set.json` | 25 题全部命中库内 canonical ≥ 20 |
| S0.2 | 三引擎盲测：GLM/SF-Kimi/TokenPlan 独立判 I1-I5 + 完整概率 + 理由，禁改 rubric | `runs/p0/judgments_*.jsonl` | 75 次调用全终态，parse_fail=0 |
| S0.3 | 计分：每引擎 within-one-tier 准确率、I5↔I1 灾难错误计数、三引擎一致性 | `runs/p0/report.md` | **聚合 within-one-tier ≥ 90% 且灾难错误 = 0** |
| S0.4 | 分支：达标 → P1；不达标 → AI 提出 rubric 修改案 → **唯一可能需要老板过目的点**（3 分钟）→ 重测 | 修订版 rubric | 同上 |

## P1 锚点库 v0（M6 的 AI 共识版）

| 步 | 内容 | 产物 | 验收 |
|---|---|---|---|
| S1.1 | 126 候选 × 3 引擎判档（与 S0.2 同一 rubric/代码路径），输入含证据档案（引用分位/跨论文/别名） | `runs/p1/judgments_*.jsonl` | 378 次调用全终态 |
| S1.2 | 等权意见池聚合 → μ/熵/margin/spread → confident/boundary/disputed | `score_aggregates` 表 | 概率数组全部长度 5 和为 1 |
| S1.3 | 收锚：confident/boundary 且 ≥2 引擎相邻档一致 → anchor_bank v0；disputed → 复核堆 | `anchor_bank_v0.jsonl` + `review_pile.md` | 复核堆 ≤ 40 |
| S1.4 | 配额检查：每档 ≥8、MSC 大类覆盖 ≥10 | 覆盖报告 | 任一档不足 → 从同信号带池外补抽 → 回 S1.1（最多 2 轮） |
| S1.5 | ADR-001 落档：锚点为 AI 共识 + 异步人工审计（偏离 SOP"双人独立分档"），v0→v1 升级路径 = 导师/同学复核 | ADR 文件 | — |

**老板任务（异步，不阻塞）：** 有空时扫 `review_pile.md`（约 20-40 条）+ 著名题档位抽查。不看不阻塞 P2-P4。

## P2 规范陈述与质量门禁（M4）

| 步 | 内容 | 产物 | 验收 |
|---|---|---|---|
| S2.1 | 确定性选代表卡（open_at_paper_time > 自含长度 > quote 可定位），识别需合成的多卡簇 | 待合成清单 | 单卡自含条目不调 API（直接复制+清洗） |
| S2.2 | GLM 生成 statement_en + source_ids + omitted_details + confidence（仅多卡簇） | raw 落盘 | parse_fail < 0.5% |
| S2.3 | 独立引擎三问核验（更强？丢条件？误写命题？）→ statement_quality 0..1 | 质量分表 | 核验与生成引擎不同族 |
| S2.4 | 门禁：quality<0.7 或簇有矛盾 → review_state=ungraded/blocked | statement 表 + hash | ungraded 不进评分 |

## P3 特征快照（M5，零 API）

| 步 | 内容 | 产物 | 验收 |
|---|---|---|---|
| S3.1 | MSC 大类 × 5 年窗 log1p 分位数标准化（组样本 <20 退化到 MSC → 全局） | `objective_feature_snapshots` 表 | 原值与标准化值同存 |
| S3.2 | missing flags + feature_hash；重切锚点池（修年代偏差） | 新候选差集 | 差集 > 20% 才补判增量 |

## P4 300 条 pilot（M7）

| 步 | 内容 | 产物 | 验收 |
|---|---|---|---|
| S4.1 | 分层抽样：MSC × 预估档 × 年代 × 簇形态 × 质量边界 | pilot 名单 300 | 覆盖矩阵无空格 |
| S4.2 | 主评分 300（一次请求全维度：importance/background/research/ai_pred+六特征）→ 自动升级二审 ~75 → 三审 ~15 | `runs/p4/` | parse_fail<0.5%、provenance 100% |
| S4.3 | 聚合 + 模糊排序代码（fuzzy block、Pareto 层）首跑 | 排序快照 | 无伪精确名次 |
| S4.4 | 自动验收：锚点 within-one-tier、重跑 50 条档位保持率、ECE（对锚点）、领域/年代残差 | pilot 报告 | 保持率≥90%、ECE≤0.10 |
| S4.5 | ADR-002：人工 weighted κ / Top-K 专家认可延后（无人工资源），v0 以锚点一致率+重跑稳定性替代 | ADR 文件 | — |

**老板任务（全程唯一必做）：** 读 pilot 报告 + 随机抽 10 条看档位是否体感离谱（5 分钟）。

## P5 全量评分（M8-M11）

同一套代码换 scope（6,868 → eligible），过夜跑。解锁条件：P4 验收全绿 + 老板看 pilot 报告点头。

---

## 失败处理总则（全阶段）

1. 429+1310 额度墙 → 熔断该引擎切下一家，绝不碰按量计费端点
2. parse_fail → 原模型重试 1 次 → 落盘 raw → 单独终态，绝不伪装 unsure
3. 任何 DELETE/迁移前：`.backup` 备份 + 输出影响行数
4. 每个 run：manifest.json（input hashes + rubric_version + model_version + code commit）
5. 人工复核堆只增不清空，处理与否不阻塞后续阶段
