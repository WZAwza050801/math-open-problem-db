# 对抗性审查报告：评分系统与数据库完成情况

> 2026-09-28 · 审查方法：不看任何交接/报告结论，直接溯源到 SQLite 快照（db.m13_snapshot.sqlite3，integrity ok）、
> 服务器实库（node01 db.sqlite3）、原始运行产物（runs/*/judgments_*.jsonl 共 9,487 行）、脚本源码逐行阅读。
> 审查基准：SCORING_PIPELINE_SOP.md v1.0（M0-M13）+ DB_DESIGN_V1/V2。

---

## 一、真实完成（每项都有可复核产物）

| # | 声称 | 溯源证据 | 结论 |
|---|---|---|---|
| 1 | 818 篇 / 7,471 卡 / 39,426 引用 | 快照库 papers=818, problems=7471, citations=39426 | ✅ 属实 |
| 2 | 2,305 对裁决 parse_fail=0 | canon_verdicts: same 673/distinct 1582/unsure 50；每条带 reason+engine+judged_at | ✅ 属实，provenance 真实 |
| 3 | 6,868 canonical、uid 100% 回填 | canonical_problem=6868；problems.canonical_uid 填充率 7471/7471=100%；簇分布（singleton 93.2%、max 12、multi-paper 61）逐项吻合 | ✅ 属实 |
| 4 | P2 陈述合成 6,868 | canonical_statement：draft 6401/verified 354/ungraded 80/blocked 33；带 statement_hash | ✅ 属实 |
| 5 | P3 特征快照 6,868 | objective_feature_snapshots=6868，原始值+分位数+feature_hash 齐全，msc_top/era_bucket 分布健全 | ✅ 属实 |
| 6 | P4 pilot + P0 金标盲测 | gold_set.json、runs/p0、runs/p4 服务器在档；rubric_v11.txt 存在 | ✅ 存在（但见二.6） |
| 7 | P5 全量 6,755 主审 + 2,702 二审 + 30 重跑 | 服务器 runs/p5/judgments_*.jsonl 实测行数 6755/2702/30；ranking 6,752 行存完整五档概率+mu+entropy+margin+80%区间+fuzzy_block | ✅ 属实，聚合算法忠实于 SOP §8 |
| 8 | 锚点库 137 | anchor_bank_v0_final.jsonl=137（I1=5/I2=24/I3=48/I4=52/I5=8；stratum A6/B30/C30/D29/E30/ext12） | ✅ 存在（但见二.4） |
| 9 | M13 150 attempts | attempts/ 实测 150 文件，模型构成 glm×91/dsr×57/kimi×2 与声称逐字吻合；两个 >190KB 文件真实存在 | ✅ 属实 |
| 10 | batch400 ~722 卡 | 服务器实库 problems=8190（+719 卡）、papers=926（+108 篇=GLM 61+Qwen 47） | ✅ 基本属实（差 3 卡） |
| 11 | 备份链 | backups/ 多个带日期快照、integrity ok | ✅ 属实 |

**总体判断：数字层面没有造假。** 报告声称的每个关键数字都能在原始产物中找到，包括不利细节（两个 190k+ 复读文件、33 blocked 簇、80 ungraded）都被如实记录。

## 二、名义完成 / 有水分（代码级实锤）

1. **`provenance: "100%"` 是硬编码字符串**（full_score.py phase_report metrics 字典里直接写死）。
   实际上每条 judgment 确实存了 prompt_sha+usage，结论大概率成立，但这个指标从未被计算过——metrics 里所有数字都是真的，唯独这个是装的。

2. **P4 GATE 布尔逻辑有优先级 bug**：
   `gate = (n>=8 and w1/n>=0.9 and rn==0 or keep/rn>=0.9 and parse_fail<=5)`
   and 优先级高于 or，实际语义与设计不符。全量运行时探针 n=0、第一个条件永假，仅靠重跑保持率就打印 "P4 GATE: PASS"——**这道门在 P5 全量时形同虚设**。

3. **P5 全量不带探针**（代码注释自认 "FULL RUN: ... no probes"），metrics 诚实显示 probe 0/0。
   即全量 6,755 条评分过程中没有任何 in-run 质量哨兵，质量完全依赖 P4 pilot 的外推。

4. **锚点选取偏离 SOP 且有系统性中档偏置**：`sel.sort(key=lambda a: abs(a["tier"]-3))`
   ——每个条目看到的锚点是"离 I3 最近的"那批，I5/I1 锚极少进入 prompt。理论上会把评分往 I3 压缩。
   缓解事实：P0 盲测和 P4 探针都是在同一逻辑下通过的；但这也意味着"验证通过"和"风险暴露"用的是同一把尺子。
   另外锚点 schema 缺 SOP 要求的 dimension/gold_tier/rationale/reviewers/rubric_version 字段，"AI 共识判档"替代人工定档（ADR 已记录）。

5. **升级二审的 40% 封顶是按列表顺序截断，不是按优先级**：2,702 = 6,755×40.0% 整，
   说明触发条件命中的条目数超过上限，超出部分被静默砍掉——部分高风险条目没得到二审。

6. **checkpoint 恢复 bug**：done 集合把失败记录也当成已完成 → 失败永不重试。
   P5 那条 parse_fail 就是这么留下的。M13 verdicts 里 17 条 level=None 混在 done 集，同类问题。

7. **boundary 的 display_label 生成逻辑可疑**（srt.index 用法混乱），且 boundary/disputed 的 display_tier=None——
   **65.5% 的库（4,426 boundary + 437 disputed）没有可用显示档位**。产品视角：系统对三分之二的条目没有给出判断。

## 三、未完成（设计文档承诺、实际不存在）

**数据库侧（对照 DB_DESIGN_V1/V2）：**
1. **V2 DDL 一张都没落地**：status_event、problem_relation、named_problem、ingest_batch 全部不存在。
   实际 canonical_problem 表只有 6 列（uid/rep_card_id/n_cards/n_distinct_papers/review_state/created_at），
   与设计的 statement_en/status/origin_year/msc/vitality_score 完全不同——**设计 schema 与运行时 schema 已经分叉，代码实际查的是 canonical_statement/snapshots 原型表**。
2. **embedding 没进库**：V2 说"不再后置"，实测 problems 无 embedding 列；embeddings.npy 只躺在文件系统（7,471² 召回实验用它，但归一主流程 2,305 对是 FTS+规则召回的）。
3. **current_status 全 unknown（7,471/7,471）**，status_event 回填管线没做。
4. M3 的两个关键质检指标没做：`sampled_merge_precision` / `sampled_split_recall`（SOP 明确要求抽检验证 63% distinct 的松紧）——**归并质量目前无独立证据**。
5. M3 放行条件"不存在未解决的矛盾三元组"严格来说不满足：84 对矛盾 → 33 簇 blocked，是挂起不是解决。

**评分侧（对照 SOP）：**
6. **api_job/model_judgment 作业队列基建没建**（SOP §6 核心）：评分结果只存在于 jsonl 文件，不在 DB——断电/误删无法从库内恢复，评分与 canonical 版本对齐靠文件名约定。
7. **B/R/A 三维度是半成品**：prompt 要了、原始 obj 存了，聚合阶段完全丢弃——评分系统实际只有 importance 一个维度上线。
8. **κ/ECE 人工校准（M7-gate）、Top-K 人工审计（M12）被跳过**（老板拍板，风险知情）——P0 的 25 题金标是 AI 出题+AI 判，裁判选手同源。
9. P(i>j)≥0.8 概率支配（SOP §9.2）未实现，只有 fuzzy block 近似。
10. 版权改写陈述、正交标签词表、别名字典（V1 §四/§六 补抽清单）均未启动。

**抽取侧（今日新发现）：**
11. **千帆线正在烧时间**：今天 14:43 起有会话用千帆 tokenplan 端点跑 batch400 剩余 281 篇，已成功 68 篇，但最近连续失败——
    `finish=length content_len≈36万`（glm-5.3 输出被 max_tokens 截断），每篇干耗 40-70 分钟产 0 卡。这是 M13/canon 阶段踩过的同一个坑（推理模型 token 饥饿），没修就上了全量。

## 四、技术路径 PM 评价

**做对了的：**
- 可溯源性是这个项目最强的资产：每步有 hash、备份链完整、runs 目录规范、脏数据清除前必备份。归并"证据型可逆"的数据模型判断正确。
- 评分设计（五档概率+锚点+模糊排序+确定性聚合）本身是先进且诚实的——它宁可输出"boundary 无档位"也不造假精确名次。
- 快节奏下仍有 gate 意识（P0/P4 两道门），且 gate 数据真实。

**最大的三个风险（按严重度）：**
1. **校准真空**：全库 I1-I5 分数没有任何人工真值锚定。I1 有 1,070 条"confident"——抽查一下就知道，这个库真有 15% 的问题达到"定义领域"级别吗？还是 falm guard 失效+锚点中档偏置的产物？目前无法回答，这是发布前的一票否决项。
2. **单引擎裁决面过大**：全库 72% 条目只有 GLM 一票（二审被 40% 截断+锚点同源），模型自偏好无法检测。
3. **双 schema 漂移**：设计文档与实际库已分叉，新会话的 agent 按文档写代码会直接查错表。建议要么补一版 V3"实际 schema"，要么把 V2 标记为"目标态未实施"。

**建议的最短闭环（按投入产出排序）：**
1. 修千帆线 length 截断（max_tokens+thinking disabled，1 小时内可修）；
2. M13 收尾：剔除 17 条 level=None 重跑 + 出统计（本周）；
3. 抽 30 条 confident 人工快检（半小时人力），先回答"I1=1,070 是否虚高"；
4. 把 P5 jsonl 入库 + 冻结 schema 为 V2.5 实际版（半天）；
5. 补 sampled_merge_precision 抽检（1 天）。

---

*审查产物：_audit_db_inspect.py / _audit_db_inspect2.py（pilot/ 下可复跑）*
