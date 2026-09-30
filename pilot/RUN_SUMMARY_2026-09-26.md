# 跑批战役实验档案（RUN_SUMMARY）

日期：2026-09-26 ｜ 归档人：WorkBuddy Agent ｜ 状态：**收官**

## 一、最终产出

| 指标 | 数值 |
|---|---|
| 论文总数（papers 表） | 818（目标 823，5 篇为匹配期合并的重复条目） |
| **成功抽取** | **786 篇（96.1%）** |
| 无全文死账 | 32 篇（2000 年 Annals/JAMS，作者选择不公开 TeX 源码） |
| **题卡总数** | **7,471 张**（content_hash 幂等，零孤儿记录） |
| 引用网络 | 39,426 条（citations.jsonl，OpenCitations + OpenAlex） |
| 分刊分布 | inventiones 322 / annals 255 / jams 124 / acta 71 / ihes 14 |
| 数据完整性 | PRAGMA integrity_check = ok；本机异地副本校验 ok |

## 二、引擎编队与配置

| 线 | 位置 | 端点 | 模型 | 分片 | 备注 |
|---|---|---|---|---|---|
| glm | node01 | /api/coding/paas/v4 | glm-5.3 (thinking=enabled) | 1/4 | team key |
| qwen | node01 | /api/coding/paas/v4 | qwen3.8-max? (ENGINE_FLAVOR=glm) | 2/4 | team key |
| lite | node01 | /api/coding/paas/v4 | glm-5.3-lite | 4/4×1w | lite key |
| kimi | 本机 Windows | api.kimi.com/coding/v1 | kimi-for-coding (openai flavor) | 3/4 | 只接受 temperature=1（不发字段） |

架构要点：`ENGINE_SLICE=i/N` 基于 done_ids 重算互斥分片；SQLite WAL + busy_timeout=60000 多进程共写；卡片 ID=内容哈希 + INSERT OR REPLACE 幂等。

## 三、时间线

- **9/22 前**：单线 pilot，823 篇目标确定
- **9/24**：639 篇（78%）；发现 83 篇 crashed，四线编队上线
- **9/24 深夜**：crash 修复部署；备份机制建立；引用网络抓取完成
- **9/25**：kimi 服务器线全灭（出网封锁）→ 迁回本机；726→765 篇
- **9/26 凌晨**：kimi 切片 4/4 收官；extract_failed 清零
- **9/26 09:33**：归档 + 停机，extracted 定格 **786 / 卡片 7,471**

## 四、事故与修复记录（全部已解决）

1. **UnboundLocalError 'd'**（83 篇 crashed 根因）：配额墙期两档重试全败致 d 未赋值 → `d=None` + `(d or {}).get()` 防护
2. **1310 周额度墙不在签名**：白退避 10 分钟 → "使用上限" 加入 `_QUOTA_SIGNS`
3. **33 篇无缓存老文堵死 arXiv 全局锁**：`todo.sort()` 有缓存排前
4. **服务器出网封锁**：api.kimi.com 194 次超时 → kimi 线整体迁回本机
5. **kimi-for-coding temperature=1 限制**：openai flavor 不发 temperature 字段
6. **403 五小时窗口墙**：挂 sleep 定时任务等重置自动续跑
7. **pgrep/pkill 自匹配**（3 次）：`^...$` 锚定 + 排除自身 PID + /proc/exe 验证
8. **CRLF / sed 截 key / ssh 内联引号**：本地写 LF 脚本 + scp 模式定型
9. **合并回退风险**：增量导出（先取服务器 extracted 差集）+ 带保护合并

## 五、Token 消耗（可见日志尾部汇总）

- kimi 本机三轮：in 4.68M / out 0.82M tokens，产出 643 卡
- 服务器三线日志按批次滚动，全程走 Coding Plan 配额，**按量余额零消耗**（硬性约束达成）
- 9/25-10/7 高峰取消活动期间消耗减半

## 六、产物清单

**服务器** `/home/user/Wholeworks/wanganan/math_openproblem/pilot/`
- `db.sqlite3`（主库，818 论文 / 7,471 卡）
- `backups/db_final_2026-09-26_0933.sqlite3`（收官快照）
- `exports/cards_final_2026-09-26_0933.jsonl`（全量卡导出，7,471 行）
- `citations.jsonl`（39,426 条引用）
- `run_{glm,qwen,lite}.log` + `watchdog_daemon.sh` + `engine.sh`

**本机** `D:\数学研究平台开发\open_problem_db\pilot\`
- `backups/db_final_2026-09-26_0933.sqlite3`（异地副本，integrity ok）
- `exports/cards_final_2026-09-26_0933.jsonl`（异地副本）
- `run_kimi_local.log`（kimi 四轮全记录）
- `audits/batch1/`（Cursor 审计工作台：20 篇 × 367 卡）
- `latex_cache/`（884 篇 LaTeX 全文缓存）
- 工具脚本：`run_pilot.py` / `export_merge.py` / `archive_final.py` / `fetch_citations.py` / `make_audit_workspace.py` 等

## 七、遗留事项（按优先级）

1. **canonical 归一 10 条原型** ← 下一步主线
2. schema 定稿：ProofAtlas/OpenConjecture 字段映射 + origin_type 写入 DB_DESIGN_V1.md
3. batch1 人工审计（367 卡，Cursor + Grok 4.7）→ 幻觉率报告
4. 32 篇 PDF 多模态扫尾（Qwen3-VL，标 source_kind=pdf 低置信度）
5. team1（884fd）9/29 恢复后可作第五线备用
