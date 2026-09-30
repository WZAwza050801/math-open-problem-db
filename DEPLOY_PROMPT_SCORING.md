# 打分器部署 + 分级指标统计 · 完整执行提示词（2026-09-27）

> 用途：直接投喂给新会话的 AI agent，自包含执行所需全部上下文。
> 决策前提（安安已拍板）：**打分第一阶段全部由 AI 完成并判断**（模糊梯队制），
> 人类两两比较留到数据库成型后做校准，不是前置依赖。

---

## PROMPT（整段复制给 AI agent）

```
你是"数学开放问题数据库"项目的执行工程师。以下是完整上下文与任务，按顺序执行。

═══ 一、项目背景 ═══
五大顶刊（Annals/Inventiones/Acta/JAMS/IHÉS）823 篇论文（2000-2025）已抽取
7,471 张"问题卡"（SQLite，19 字段，核心字段 100% 填充）。当前阶段：把卡归并为
~6,000 个 canonical 条目（证据型归并、可逆），然后由 AI 对每个条目打分。
设计文档：D:\数学研究平台开发\open_problem_db\DB_DESIGN_V2.md（六张新表 DDL）
与 SCORING_DB_HANDOVER_2026-09-27.md（评分策略，含锚点法模糊梯队方案）。

═══ 二、服务器环境（固定工作区，严禁越界）═══
* 连接：ssh node01（本机 ~/.ssh/config 已配：10.70.225.223，user，
  IdentityFile ~/.ssh/id_ed25519_node01，加 -o BatchMode=yes 非交互）
* 工作区：/home/user/Wholeworks/wanganan/math_openproblem/pilot/
  （Wholeworks 下有 Guo/Li/xiong/oilsim 等他人目录，绝不触碰）
* 凭据：工作区 .env（600 权限）含 5 把 key：GLM_CODING_TEAM2_KEY（现役）、
  GLM_CODING_TEAM_KEY（9/29 08:05 重置）、GLM_CODING_LITE_KEY（9/30 重置）、
  BAILIAN_TOKENPLAN_KEY、SILICONFLOW_KEY
* 端点铁律：GLM 只走 https://open.bigmodel.cn/api/coding/paas/v4（扣套餐积分），
  绝不走 /api/paas/v4（按量余额）。额度墙签名：429 + "1310"/"使用上限"
* 跑批纪律：nohup 后台 + 日志重定向 + 断点续跑（幂等表）+ 停机前 integrity_check

═══ 三、现有资产（都在工作区）═══
* db.sqlite3：主库（papers 818 / problems 7,471 / citations 39,426 已挂接 /
  paper_vitality 已算 / status_events_pre 1,876 条中间表）
* pending_pairs.jsonl：2,305 对候选归并对（cos≥0.8 的 1,696 对 + 别名组内
  0.6-0.8 的 609 对，已冻结）
* canon_judge.py：裁决脚本（8对/批、4线程、断点续跑、三级降级链
  GLM→TokenPlan→SF）——⚠️ 已知两个 bug 待修：① worker 里 con.execute
  未持 con_lock（sqlite3.InterfaceError）② 模型回复解析失败时静默落
  verdict='unsure'（上一轮跑出 112 条可疑记录，需清理重跑）
* data_audit.py：库级体检（已跑过，报告 audit_report_20260926.txt）
* 本机 canon_prototype/embeddings.npy：7,471×1024 bge-m3 全量向量

═══ 四、执行步骤（按序）═══
1. 修 canon_judge.py 两个 bug：texts 查询包进 con_lock；JSON 解析失败时
   重试一次并把仍失败的批记 verdict='parse_fail'（与 unsure 区分）
2. 清脏数据：DELETE FROM canon_verdicts（112 条全部作废）
3. 启动裁决：nohup python3 canon_judge.py >> canon_judge.log 2>&1 &
   预计 289 次调用 / 数小时；完成后统计 same/distinct/unsure/parse_fail
4. union-find 分组（只吃 same 边，unsure/parse_fail 不合并——宁缺勿滥）：
   生成 canonical_problem 行（uid 规则 op-2026-NNNNNN）+ 回填
   problems.canonical_uid；≥10 卡的大簇单独导出人工复查清单
5. canonical 生成后：为每组选代表卡（self_contained 最长且
   open_at_paper_time 优先）填 statement_en 初稿，review_state='draft'

═══ 五、AI 打分器（核心新任务）═══
打分原则：第一阶段全部 AI 打分；输出 5 档梯队（★1~★5）+ 后台连续分 +
provenance（模型/日期/prompt版本）；任何分数可从输入重放；多模型交叉，
分歧大者标 low_confidence 待人工。

ai_importance（重要程度，每 canonical 条目一次）：
  输入给 LLM：条目规范陈述 + 客观信号包（vitality、被引数、近5年被引、
  支持卡数、跨论文数、是否在别名热点表、发表年份）+ 锚点名单
  （42 个跨论文热点中公认 top 的 ~10 个直接锁 ★5，不参与打分）
  要求 LLM 输出：{"tier": 1-5, "rationale": "<一句话>", "confidence": high|mid}
  多模型（glm-5.3 / qwen3.8-max / kimi-k2.6）各打一次，tier 全一致取之，
  不一致取中位并标 low_confidence
ai_difficulty（AI 感知难度，独立于人类难度，两维禁止互推）：
  第一步（便宜）：LLM 基于陈述本身估"需要多少背景才能读懂/尝试"，
  输出 tier + 所需背景领域清单
  第二步（贵，可选后置）：真让模型尝试求解 N 次记录成败率——仅对 tier 争议
  条目做，成本单列
人工难度（human_difficulty）：本轮不做，等平台比较数据（ADR-006），
  表结构预留。

═══ 六、指标统计清单（三级，全部落 SQLite 表 + JSONL 导出）═══
【L0 库级 · 工程质量】（已有 data_audit.py，每次跑批后重跑）
  integrity、孤儿卡、hash 重复、19 列字段矩阵、label×status×journal 交叉、
  年代×开放占比趋势、MSC top 分布
【L1 卡级 · 每张卡】（多数已有）
  label、paper_time_status、msc_primary/secondary、difficulty_hint、
  canonical_uid（裁决后）、embedding 向量、top-20 邻居（neighbors 表已有）
【L2 条目级 · 每个 canonical】（裁决后新增，打分器主战场）
  身份：uid、statement_en（代表卡初稿）、origin_arxiv_id/origin_year、
        origin_type='journal_mined'
  状态：current_status（由 status_events_pre 推导）、formalized
        （none|in_progress|verified，本轮全填 none，留 ProofAtlas 对接口）
  客观：vitality（组内论文求和）、n_total_citations、n_recent_citations、
        n_supporting_cards（组内卡数）、n_distinct_papers（跨论文数）、
        age_years、in_alias_hotlist（是否别名热点）
  AI 分：ai_importance_tier/score/confidence（多模型交叉）、
         ai_difficulty_tier/score/confidence、需要背景领域清单
  结构：n_relations（后续关系抽取填 0）、alias_names（挂接的别名）
【L3 集合级 · 分析视图】（SQL 视图即可）
  梯队分布（各档条目数）、梯队×MSC 交叉、梯队×年代交叉、
  锚点条目清单、low_confidence 清单、"开放且高重要性"清单（平台首页素材）

═══ 七、工程约束（安安原话）═══
防熵增：评分逻辑纯函数化（可从输入重放）；每轮跑批导出 JSONL 并 git commit；
中间脚本一律放 pilot/ 不散落；禁止在 /tmp 或他人目录留文件。
可解读：每个分数带 provenance；梯队判定理由存库。
可维护：脚本幂等可重跑；停机走"备份→integrity→停进程→留日志"流程。

═══ 八、汇报格式 ═══
每完成一个步骤用中文简报：做了什么/数字结果/遇到的坑/下一步。
全部完成后出汇总：canonical 条目数、梯队分布表、low_confidence 数量、
L0-L3 指标落地清单、与 SCORING_DB_HANDOVER_2026-09-27.md §二状态表的对照。
```

---

## 安安需要知道的三个决策点（提示词已内嵌默认值，不同意再改）

1. **梯队档数默认 5 档**（★1~★5），锚点 10 个锁 ★5——想改档数直接说数字
2. **ai_difficulty 第二步**（真让 AI 尝试求解记成败率）默认**后置**——只有争议条目才做，成本单列
3. **多模型交叉打分**会用掉 Token Plan/SF 额度（~6,000 条目 × 3 模型 × 2 维度），如果想省，可以只对 ★4/★5 和 low_confidence 条目做交叉，其余单模型——提示词里没写死，执行时 AI 会按"分歧大才交叉"理解
