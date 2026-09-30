# 猜想级语义影响力指标 · 现状核查与设计草案

> 2026-09-29 ｜ 起因：导师新建议——重要性评分不能只看论文被引（OpenCitations 口径），
> 要判断 **conjecture 本身**是否对后续研究产生了实质影响。
> "论文被引"是"猜想被引"的充分不必要条件：论文被引可能是引技术/其他结果，
> 猜想本身并未进入后续研究的推理链。这需要语义分析，OpenCitations 做不到。

---

## 一、现状核查：库里有什么、缺什么

### 已有（全是论文级，不区分猜想）

| 资产 | 内容 | 位置 |
|---|---|---|
| citations | 39,426 条被引边（COCI：citing DOI → 我方 DOI + 日期），**无引用上下文、无语义** | 服务器 citations 表 / pilot/citations.jsonl |
| paper_cite_stats | 被引计数聚合（806/818 篇有引用，总被引 39,294、篇均 48、max 396） | 服务器表 |
| vitality | log1p(n_total) + 2·log1p(n_2021_2026)，论文级生命力 | DB_DESIGN_V2 §3.5 |
| S2 enrich | 只对 823 篇本源论文补过 arxiv_id/abstract，**没碰过引用方论文** | pilot/s2_enrich*.jsonl |
| P5 重要性 | 五维概率向量，纯模型判断，不基于引用证据 | p5_ranking_assigned.jsonl |

### 缺的（导师要的这一层）

- 引用方论文（39,426 条 citing DOI）的**元数据/摘要**：从未抓取
- **引用上下文**（citation context：引文出现的那几句话）：COCI 根本不提供
- **猜想级归因**：一篇论文含多个命题，引它≠引其中某个猜想——这层消歧完全没有
- DB_METRICS_PLAN 指标清单、DATA_WORKPLAN 引用加工计划（被引分布/co-citation）全部是论文级网络指标

**结论：猜想级语义影响力 = 纯空白，需新建一条管线。**

## 二、导师意图的形式化

对 canonical 猜想 C（出自论文 P），遍历 P 的每篇引用论文 Q，判定 Q 与 C 的关系：

| 档位 | 类型 | 判定标准（语义） | 是否计"猜想被引" |
|---|---|---|---|
| A | 实质推进 | 解决/部分解决/推翻/改进 C 的界或情形 | ✅ 强 |
| B | 直接继承 | 推广 C、提出 C 的变体、以 C 为核心动机或工具 | ✅ |
| C | 名义提及 | 引言/相关工作里列举式提到，后续论证与 C 无关 | ❌ |
| D | 与 C 无关 | 引 P 是为了技术、其他定理、背景 | ❌ |

导师口径下的影响力：**A/B 的计数与质量**；C/D 正是"论文被引但猜想没被引"。
论文级被引与猜想级影响的**差值本身**是研究素材（"高被引低影响" vs "低被引高影响"猜想）。

## 三、管线设计（沿用已验证的三段式：召回 → LLM 裁决 → 人工查验）

**Stage 1 · 引用方富化（元数据 + 弱标签）**
- 39,426 条 citing DOI → Semantic Scholar Graph API 批量拉取：
  `title, abstract, tldr, year, venue, intents, isInfluential, contexts`
- S2 的 `contexts`（引用句）+ `intents`（background/methodology/result）+ `isInfluential`
  正好是这个问题的**现成弱标签**，可先免费白嫖一层粗判
- 覆盖率风险：COCI 的 citing DOI 中 S2 未收录的（预计 <15%），降级到 OpenAlex 摘要重建（inverted index）

**Stage 2 · 猜想-引用对粗筛（降本）**
- 每对 (C, Q)：bge-m3 embedding 相似度（statement × Q.abstract/tldr）——已有全套 embedding 基建
- 相似度高 / S2 intent=methodology|result / isInfluential=true 的送 LLM；明显无关的直接落 D
- 预估：39k 对粗筛后送裁决约 1–1.5 万对，GLM 四线配额内

**Stage 3 · LLM 语义裁决（A/B/C/D 四级）**
- 输入：C.statement + Q.title/abstract/tldr + Q.contexts（引用句，有则给）
- 引用句是消歧关键：一句话直接看出引的是哪个命题、引去干嘛
- 输出：档位 + 一句话理由 + confidence；低置信进人工查验队列（沿用 review_state 流程）

**Stage 4 · 指标物化**
- `canonical_metric(metric='semantic_influence')`：A 数、B 数、加权分（建议 A=3/B=1.5）
- `canonical_metric(metric='citation_gap')`：论文被引数 − 猜想被引数（导师论点的直接量化）
- 全部带 provenance 三元组，默认 visibility=internal（DB_METRICS_PLAN §二.4 纪律继承）

## 四、验证与风险

| 项 | 内容 |
|---|---|
| 校准集 | 抽 100 对人工裁决（安安+导师），LLM 一致率 ≥80% 才放量 |
| 风险 1 | S2 contexts 覆盖率不全 → 无 context 的对只能靠摘要判，置信度标注区分 |
| 风险 2 | 一论文多猜想归因错误 → 引用句消歧为主，同名猜想（RH 类）优先用 named_problem 别名表 |
| 风险 3 | A 档（实质推进）误判最贵 → A 档全部强制人工复核（量小，预计百级） |
| 成本 | S2 免费；LLM 约 1–1.5 万对 × ~1k token，四线编队一次窗口可跑完 |

## 五、落地顺序

1. 写 S2 citing 批量富化脚本（可断点续跑，复用 s2_enrich 的 opener/UA 模式）— 本机跑，服务器出不了网
2. 拉完后出覆盖率报告（有 abstract/contexts 的比例），再定粗筛阈值
3. 100 对校准 → 放量裁决 → 物化进 canonical_metric
4. 与 paper 级被引并列导出对比表，作为导师汇报素材（"猜想级影响 vs 论文级被引"首次量化）

> 待导师确认：① A/B/C/D 四档定义是否合意；② 加权分权重；③ 是否把 citation_gap 作为独立研究产出。
