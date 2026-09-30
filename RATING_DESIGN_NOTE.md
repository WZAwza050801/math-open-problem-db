# 难度/重要性评分系统 · 可行性分析（基于 JevProject 笔记）

> 2026-09-26 ｜ 输入：Desktop/JevProject(1).pdf（Place Pulse + Chatbot Arena 的 Bradley–Terry 方案，18 页）
> 结论先行：**可行，且强烈建议做**——但有三处必须修正细节（见 §四）。

---

## 一、强支持证据：两条独立路线已经收敛

1. **先例完全对口**。Chatbot Arena（LLM 排名）、Place Pulse 2.0（城市颜值）、TrueSkill（游戏匹配）解决的都是同一族问题：*主观、无 ground truth、绝对分不可靠、两两比较容易*。数学问题的难度/重要性正好落在这族。
2. **你自己已经独立拍板过一次**。ai_math_recommend 的 **ADR-006**（2026-08-27 Accepted）白纸黑字："专家标注以成对比较为主标签形式……未来 Learning to Rank 以成对偏好为主监督信号（Bradley–Terry 基线）"。两个项目互不知情的情况下收敛到同一方案——这比任何外部论证都硬。

## 二、逐维可行性

| 维度 | 评估 | 依据 |
|---|---|---|
| 理论适配 | ✅ | 心理测量学成熟：人类比较判断的可靠性远高于绝对打分（ADR-006 的立项理由） |
| 规模 | ✅ | canonical 归一后条目几百~2k；active sampling 每条目 10-20 次有效比较即可出稳定分，总比较量 1-5 万次 |
| 实现 | ✅ | arena-rank（Apache-2.0）全套：L-BFGS、bootstrap、sandwich 方差；笔记 §7 已给出 PairDataset/BradleyTerry 接口，我们只需加一张比较表 + 打分脚本 |
| AI 评分定位 | ⚠️ 有条件 | AI 只能做**先验/协变量**（Jev §1.1 的 D_i 槽位），不能当标签——见 §四.2 |

## 三、与现有资产的对接（具体到表）

```
已有                              新增
─────────────────────           ─────────────────────────────
problems.difficulty_hint  ──→   保留，标 provenance（模型/日期/配置）
citations + paper_vitality ──→  作为 importance 的客观协变量进 D_i
canonical_problem         ──→   +difficulty_band / +importance_band（公开显示）
                                +difficulty_score / +importance_score（后台，不公开）
                                新表 pairwise_comparison：
                                  voter(匿名), winner_uid, loser_uid,
                                  relation(win|near|tie), context, created_at
```

与 ai_math_recommend **共用一套两两比较 UI 和 Review Schema**（其 pairwise_preference 结构已定义）——两个项目一个采样组件，两份数据。

## 四、三处必须修正的细节（风险与缓解）

### 1. "给出比例"这个输入方式要砍掉
直接问"黎曼猜想比普通问题重要几成"= 绝对评分换皮，个体尺度不可校准（这正是 ADR-006 否决绝对分的原因）。**改为三档：A 明显胜 / 接近 / B 明显胜**（lmarena 同款）。比例感不需要用户报告——BT 分差自动表达（Elo 差 400 分 = 10:1 胜率）。

### 2. AI 难度评分必须带 provenance，且永不直接发布
"AI 尝试后给出的难度"有两个结构性问题：agent 能力会升级（同一题 GLM-5.3 做不出、下一代秒解，分数漂移不可追溯）；同族模型审计盲区。**规则**：AI 评分永远存 `model + date + 尝试配置` 三元组，只进 D_i 先验槽位，前端永远不显示。库里 difficulty_hint 已经是这个定位（缺 31 张，无妨）。

### 3. 冷启动：绝不发布无比较支撑的分数
- 0 比较的条目显示"未评级"，不显示任何分
- 初期只评 **top 100 热点**（你+同学+导师 5-20 人 × 50 次 = 千级比较，刚够）
- 难度还有个特殊性：**不是全序**——组合题对组合专家易、对几何学家难。Jev §5 的 per-rater 扩展（q^(k) 依赖 R_k）正是解法；最低成本版：记录投票者领域背景，分领域出分再聚合
- 前端永远显示 band（★~★★★★），连续分只存后台（ADR-006 §13.2）

## 五、路线图

| 阶段 | 时点 | 内容 | 成本 |
|---|---|---|---|
| 0 | 现在 | V2 schema 预留 4 列 + pairwise_comparison 表；Jev 笔记归档进 open_problem_db | 零 |
| 1 | canonical 后 | AI 多模型交叉打 difficulty_hint（带 provenance）；top100 人工种子比较 | 少量 API |
| 2 | 平台上线 | 页面内嵌"今日二选一"，BT 每日重算，band 显示 | 服务器 |
| 3 | 数据积累后 | pairwise 偏好做 Learning to Rank 监督（对接 ai_math_recommend Phase 4） | — |

## 六、一句话结论

方案本质是把"主观排序"从"人人打架的绝对分"转移到"人人都能答对的两两比较"，这正是 Place Pulse 和 Arena 被验证过的路，也是你 8 月在 ai_math_recommend 已经拍板过的路。**可行性没有问题；要改的只是三个执行细节：比例输入改三档、AI 分降为先验、冷启动只评热点。**
