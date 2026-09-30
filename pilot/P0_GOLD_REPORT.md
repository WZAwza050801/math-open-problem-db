# P0 金标准盲测报告（2026-09-27）

## 结论：PASS（rubric importance-v1.1）

| 引擎 | v1.0 within1 | v1.1 within1 | v1.1 exact | 灾难错误 |
|---|---|---|---|---|
| glm-5.3 (thinking off) | 24/25 | **25/25** | 19/25 | 0 |
| qwen3.8-max (thinking off) | 22/25 | **25/25** | 18/25 | 0 |
| 集成（均值档） | 88% ❌ | **100% ✅** | 21/25 | 0 |

金标准集：25 题（6×I5 千禧年、6×I4 领域级、5×I3 著名中档、8×I1/I2 合成平凡题），静态硬编码，零外部数据。

## 失败模式与修复

v1.0 失分全部是同一模式：**I3 著名开放问题被高估**（Furstenberg ×2×3 被双引擎判 I5；色数问题、Andrews-Curtis 被判 I4-I5）——即"名气通胀"，正是设计文档预言的"著名名词 ≠ 高档位"。无一起 I1/I2 误高估或 I5 误低估。

v1.1 修复 = FAME GUARD 段：名气/年代/朗朗上口不升档；I5 保留给"改变广阔领域工具箱或基础"的问题；每档给一个校准示例。修复后全部 25 题双引擎 within-one-tier。

## 引擎纪律（老板 2026-09-27 指示）

- **Kimi 只允许官方 coding plan**（api.kimi.com，k3）；SiliconFlow 等按量计费渠道一律禁用
- node01 出网受限：api.kimi.com 不通（智谱/阿里云通）→ v0 用双引擎集成（GLM + qwen3.8-max），收锚规则改为"两引擎相邻档一致"；Kimi 第三票待网络打通或本机中转后接入

## 产物

- `gold_set.json`（gold-v1.0）、`gold_judgments_*.jsonl`（v1.0 基线）、`gold_judgments_v11_*.jsonl`（正式）
- 生产 rubric 版本号：**importance-v1.1**
