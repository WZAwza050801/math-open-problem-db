# 回填筛选报告 — 3,617 篇未筛论文（2026-09-27）

## 背景与结论

原 823 篇候选池是 arXiv 摘要级短语匹配的产物，Crossref 全目录（4,437 篇）中剩余
**3,617 篇从未做过含猜性筛查**。本轮回填用 OpenAlex-by-DOI 摘要筛选 + Semantic
Scholar 补全，结论：

> **新发现 886 篇阳性论文（命中率 24.5%），其中 600 篇有 arXiv 全文通道。**
> 问题池有近乎翻倍的扩充空间，抽取成本约等于再跑一次原始 823 篇管线。

## 筛选管线（全部免费，零 API 消耗）

```
Crossref TOC (4,437) - 823 已筛 = 3,617 未筛
  → OpenAlex DOI→摘要（6 线程，17min，0 错误）        覆盖 2,157 篇
  → Semantic Scholar 摘要抢救（1,352 篇无摘要）        覆盖 572 篇
  → 标记词正则（conjecture / open problem / we pose…）  摘要级 75% 覆盖
  → arxiv_id 补全（S2 by DOI，老式 math/NNNNNN 可查）
```

## 阳性清单（backfill_positives.json）

| 来源 | 数量 | 有 arxiv_id |
|---|---|---|
| 一轮：OpenAlex 摘要/标题命中 | 767 | 487* |
| 二轮：S2 摘要抢救后新增 | 119 | 117 |
| **合计** | **886** | **600** |

*含 S2 修复的 16 个 OpenAlex 垃圾 id；286 篇无 arXiv 版本（多为 JSTOR 早期论文）。

分布：annals ~370 / jams ~180 / inventiones ~280 / acta ~60 / ihés ~50，
2000-2025 每年均匀分布。抽查精度 8/8（提出/证明/条件引用猜想）。

## 成本估算（抽取阶段，待批）

- 886 篇 × ~80 积分/篇（按 823 篇实测 66,300 分折算）≈ **71k 积分**
- 建议加 GLM 摘要级预分类（~1-2k 积分）先砍 15-30% 条件引用噪声 → 实付 ~50-60k
- LaTeX 全文下载免费（本地，进行中，487 篇跑完后再补 113 篇第二轮）

## 遗留

- 888 篇（25%）无任何摘要来源，仅标题筛查——JSTOR 封闭时代论文，接受该缺口
- 286 篇阳性无 arXiv 版本：需走出版商渠道或人工处理（可后置）
- ar5iv 对 1999 年前后老式 id 覆盖差，下载失败率约 20%，可重试或用 export 镜像换时段

## 产物文件

- `backfill_matches.jsonl` — 3,617 篇逐篇筛选记录（含标记词证据）
- `backfill_positives.json` — 886 篇阳性终版（candidates.json 兼容格式）
- `s2_enrich.jsonl` — S2 补全记录（arxiv_id + 摘要）
- `backfill_precache.py` / `s2_enrich.py` / `match_backfill.py` — 可复用脚本

## 附：Qwen 全量智能预筛（2026-09-27 20:10-21:00 补充）

应老板"为什么不全部跑"的要求，对 2,754 篇有摘要论文全量过了 qwen3.8-max 智能判定
（pose/prove/use/no，Token Plan，10 分钟，0 错误）。抽查 prove 精度 10/10——
抓到大量正则漏掉的"回答了 XX 的问题"型论文（无 conjecture 关键词）。

- 预筛结果：pose 43 + prove 622 + use 34 + no 1365
- **最终抽取候选池：1,448 篇**（886 名单 + 562 预筛新增；1,432 为误算，103 篇重叠）
- 全文通道：894/1,448 有有效 arxiv_id（LaTeX 下载进行中）；554 篇无 arXiv 版本
- 抽取成本量级：~115k 积分（1,448 × ~80），建议 GLM 配额 9/29-30 重置后分 2-3 批
- 产物：extraction_candidates.json（主清单，1,448 条）、triage_qwen.jsonl（逐篇判定）、
  triage_relevant.jsonl（665 条 pose/prove）、s2_enrich_round3.jsonl（294 个新 id）
