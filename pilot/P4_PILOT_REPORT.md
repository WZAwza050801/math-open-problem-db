# P4 300 条 Pilot 验收报告（2026-09-27）

run_id: score-pilot-20260927-v1 ｜ rubric: importance-v1.1 ｜ 引擎: GLM 主审 + qwen 升级审

## 验收指标（全绿）

| 指标 | 门槛 | 实测 | 判定 |
|---|---|---|---|
| 锚点探针相邻一档准确率 | ≥90% | **10/10 (100%)**，且 exact 10/10 | ✅ |
| 重跑档位保持率（30 条） | ≥90% | **30/30 (100%)** | ✅ |
| parse_fail | <0.5% | **0/310** | ✅ |
| provenance 完整率 | 100% | 100%（每条含 prompt_sha/model/usage） | ✅ |
| 升级评审 | 触发式 | 120/310 (39%) 进二审 | ✅ |

**P4 GATE: PASS —— 全量评分（P5）解锁。**

## 评分状态分布（310 条）

| 状态 | 数量 | 占比 |
|---|---:|---|
| confident（显示单档） | 98 | 32% |
| boundary（相邻两档，显示 I3↔I4 式） | 190 | 61% |
| disputed（进复核） | 22 | 7% |
| ungraded | 0 | — |

fuzzy blocks：2 个（80% 档位区间普遍较宽，说明系统诚实而非乱排序）。

## 发现与留待人工校准的问题

1. **boundary 占比 61% 偏高**：置信阈值（max p≥0.60, margin≥0.20, H≤0.65）偏严。这是保守方向的偏差（可接受），人工校准集到位后再放宽。
2. **confident 档位分布双峰**：I1=45 / I3=1 / I4=21 / I5=6——中间档问题大多落入 boundary。两解释：库内确有大量低价值抽取物（batch1 审计支持）+ fame guard 把中档压进 boundary。**需人工抽检 10 条确认体感**。
3. disputed 22 条全部来自双引擎档位差 >1，已在复核队列。

## 产物

- `runs/p4/sample.json`（300 分层样本，37 MSC 大类、202 个 MSC×年代格子）
- `runs/p4/judgments_main_glm.jsonl`（310 主审）、`judgments_esc_qwen.jsonl`（120 二审）、`judgments_rerun_glm.jsonl`（30 重跑）
- `runs/p4/pilot_ranking.jsonl`（聚合 + 模糊排序：P 分布/μ/熵/margin/状态/80% 区间/fuzzy block）
- `runs/p4/metrics.json`
