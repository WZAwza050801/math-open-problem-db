# 断点交接记录（RESUME）

> 最后更新：2026-09-17 22:35 GMT+8
> 用途：随时中断、随时继续。下面每一条都是"下次回来照着做就行"。

---

## 一、现在是什么状态

**40 篇试跑完成**：成功 **39 篇**、失败 **1 篇**、落库 **377 张问题卡**。

失败经过与真相（重要）：
- 首轮 40 篇跑完，11 篇失败。其中 **10 篇是 `502 Bad Gateway`**（本机 HTTP 代理隧道瞬时抖动），
  **不是代码 bug**；重试后 **10/11 全部恢复**。
- 剩最后 1 篇 `1706.03152[ihes]`（403k 字符，超长论文）仍在重试中。

| | |
|---|---|
| 语料 | 五大刊各 8 篇，每篇都有 **Crossref DOI 背书**（刊名/年份可逐篇查证） |
| 全文 | **40/40 全部拿到 LaTeX 源码**，零失败 |
| 卡数 | **377 张**：`real_open` 100 (27%) / `future_application` 85 (23%) / `solved_in_paper` 74 (20%) / `background_open` 63 (17%) / `method_obstruction` 53 (14%) / `uncertain` 2 (1%) |
| 引文可核验率 | **375/377 = 99.5%**，**`quote MISSING = 0`**（真实伪造 0 条） |
| 标签/合规违规 | 全部 **0**（label / current_status / self_check / banned_phrase / MSC 全 0） |
| 重复 | **同篇近似重复对 0、引文重复组 0** |
| token | 输入 3.77M / 输出 1.68M（单篇 ≈ 97k in / 43k out） |
| 每篇卡数 | min 5 / 中位 10 / 均值 9.6 / max 16 |

### 两条新教训（都踩过）

**① `quote MISSING` 曾经有 2 条"疑似伪造"，查证后**全部不是伪造**，是两类转写损伤：**
- **`\n` 吃掉字母**：原文 `Whether or not`，模型把散文里的 "not" 当 LaTeX `\not` 写，
  JSON 解析时 `\n` 变成**真换行**，存成 `or<换行>ot` —— 字母 `n` 消失，永远匹配不上。
- **`\ref` 被改写**：原文 `In order to prove Theorem \ref{X}`，
  模型写成 `Theorems \ref{X} and \ref{Y}`（复数化 + 多插一个引用）。
  这是 `partial-edited`，**引文字段不忠实**，但底下的开放问题真实存在。

**② 修校验器时差点引入新 bug**：为了修①，我先后写了三版正则——
第一版 `\\(?=[a-zA-Z]) → 空格` **删掉了原文合法的 `\cite{BM}` 反斜杠**，
把一条本来能匹配的引文变成了不匹配。**最终只在引文侧、只针对 `字母+换行+小写字母` 做 `\n→" n"` 修复**，
且**绝不对全文做修复**（全文本来就有大量真实换行，动了就毁掉比对基准）。

> **教训**：修正则前先在**真实数据**上 diff 到"第一个分歧字符"，不要凭直觉迭代。
> 上面这个 bug 我盲改了 3 轮才定位到第 177 个字符。

---

## 二、下次回来，一行命令

```bash
cd D:/数学研究平台开发/open_problem_db/pilot
"C:/Users/31168/.workbuddy/binaries/python/versions/3.13.12/python.exe" status.py
```

看状态。要接着跑：

```bash
"C:/Users/31168/.workbuddy/binaries/python/versions/3.13.12/python.exe" resume.py
```

`resume.py` 会按顺序做：拉全文 → 提取 → 出报告 → 跑校验，跑完把摘要追加到 `runs.log`。
**它是幂等的，重复跑不会坏事、不会重复扣钱**（已提取的论文直接跳过，全文走本地缓存）。

> 注意：`status.py` / `resume.py` 必须用上面那个**完整 python 路径**。
> 本机 bash shim 缺 `cat`/`grep`/`head`/`rm`/`dirname` 等命令，不要用裸 `python` 或 shell 工具链。

> ⚠️ **别在上一轮还在跑的时候启动 `resume.py`**。先跑 `status.py`；如果"未尝试"的数字几分钟内
> 一直在下降，说明有进程在跑，等它结束再继续。（同时跑不会弄坏数据——ID 是内容派生的——
> 但会白花一次 API 调用。）

### 为什么可以随便中断

- `run_pilot.py` 跳过所有 `fetch_status='extracted'` 的论文，所以重跑只会补做**待处理 + 失败**的
- 全文缓存在 `latex_cache/`，重跑不再下载
- 问题卡 ID 由 `(arxiv_id + 引文)` 内容派生哈希，重跑**只覆盖自己那几行**，不会串篇
- 每次运行都往 `runs` 表和 `runs.log` 追加记录

---

## 三、目录里每个文件干什么

| 文件 | 作用 | 什么时候动 |
|---|---|---|
| `harvest.py` | **采集层**。Crossref 按 ISSN 枚举期刊目录 + arXiv 精确短语取池 + DOI/标题连接，产出 `candidates.json` | 只换语料时用，加 `--refresh-toc` 重拉目录 |
| `candidates.json` | 采集产物：40 篇候选，含权威刊名/DOI/年份/连接方式 | 生成物，别手改 |
| `crossref_toc.json` | Crossref 全量目录缓存（4437 篇，五刊 2000–2025） | 生成物 |
| `run_pilot.py` | **主流程**：全文下载 → glm-5.3 六分类提取 → SQLite | 续跑用它 |
| `resume.py` | 一键串起全链路 + 记日志 | **下次直接跑这个** |
| `status.py` | 看状态（只读，跑着的时候也能看） | 随时 |
| `validate_cards.py` | **机械校验器**（不用 LLM）：引文逐字核验、标签合规、重复检测等 | 每次重跑后必跑 |
| `make_review.py` | 生成人看的报告 `exports/REVIEW_v3.md` + `exports/problems_v3.jsonl` | 每次重跑后必跑 |
| `latex_cache/` | 全文缓存。`.tex` = LaTeX 源码，`.ar5iv.txt` = HTML 兜底（**两者不能混用**） | 生成物 |
| `export` / `probe_*` / `diag_*` / `test_parse.py` | 通道探测与诊断脚本，是当时定位问题用的，留作证据 | 排查时才用 |
| `db.sqlite3` | 主库：`papers` / `problems` / `runs` 三张表 | 生成物 |
| `archive_db_v1_polluted.sqlite3` | **v1 被污染的旧库**（23 篇里 14 篇是假刊），只作存档，不要用来出结果 | 存档 |

---

## 四、试跑跑完后必须做的两件事

1. **出报告 + 校验**
   ```bash
   python make_review.py && python validate_cards.py
   ```
   ✅ **已完成（2026-09-18）**：`exports/REVIEW_v3.md`（6486 行）+ `exports/problems_v3.jsonl`（377 行）。
   校验结果：可核验率 99.5%、`quote MISSING = 0`、所有违规计数 0。

2. **第三次第三方质检**
   质检提示词已写好：`exports/GPT_AUDIT_PROMPT_v2.md`。
   把 `REVIEW_v3.md` 全文贴进去，用来对比 v1 的 5.5/10 分数。
   v1 的原始质检报告存于 `exports/GPT_AUDIT_v1.md`。
   ⏸ **尚未执行** —— 这是下一步。

---

## 五、已知未修好的问题（别以为已经全好了）

| 问题 | 现状 | 该怎么办 |
|---|---|---|
| **同篇同题重复计数** | ⚠️ 部分好转：`quote_location` 重复组从 11 组降到 **0 组**，`near-duplicate card pairs = 0`；但模型仍可能在同一主题下出多张"变体卡"（提示词已要求用 `related_note` 标注） | 彻底解决仍需 **L3 归一层**（向量相似 + LLM 两两仲裁），尚未开工 |
| **`future_application` 占比偏高** | ⚠️ 23%（85/377），与 `real_open` 27% 接近 | 需人工判断是否值得入库，可能要收紧标签定义 |
| **2 条引文过短（<40 字符）** | ⚠️ `OP-C5ED6F9541B9` (31 字符)、`OP-1A2DBE85DBA3` (38 字符) | 人工看一眼，或在校验器里加自动重取 |
| **`partial-edited` 引文** | ⚠️ 1 条（`\ref` 被复数化+多插） | 引文字段不忠实，建议对该字段加"必须 substring 命中"的硬约束 |
| **状态追踪层** | ⏸ 设计上后置。`current_status` 100% 合规保持 `unknown`，机制在、数据没有 | 等接 GPT-5.6 级 API；`status_events` 表已在 schema 预留 |
| 覆盖率天花板 | ⚠️ 4437 篇分母里只有 **16%（≈711 篇）** 有 arXiv 全文 | 这是硬约束，要如实写进给导师的方案 |

---

## 五之二、跑批前必做的三件事（血的教训）

1. **先探网络**：`502` 会伪装成"提取失败"，一次能废掉四分之一的进度。
   ```bash
   python -c "import urllib.request;urllib.request.urlopen('https://open.bigmodel.cn/api/coding/paas/v4',timeout=15)"
   ```
   （返回 401 是**好的**——说明网络通了，只是没带 key；`502 Bad Gateway` 才是坏消息。）
2. **失败列表先看 `error` 类型，再看数量**：`URLError 502` → 重试即可；`finish=stop content_len=...` → 才是真 bug。
3. **跑批中途别改代码**：`run_pilot.py` 是长驻进程，改写文件不会生效，还会让下次重启的行为不一致。

---

## 六、关键配置与凭据位置

| 项 | 值 |
|---|---|
| 模型 | `glm-5.3`（GLM Coding Plan 团队版，**9-18 到期**） |
| Key 位置 | ⚠️ **仍然写死在本目录 `run_pilot.py` 第 45 行 `GLM_KEY` 常量** |
| 备胎 | DeepSeek（已探活） |
| 并发 | `PILOT_WORKERS` 环境变量，默认 6 |
| 全文预算 | `MAX_CHARS = 260_000`（头 65% + 尾 35%） |
| 缓存命名 | `.tex` = LaTeX 源码 / `.ar5iv.txt` = HTML 兜底 |

> ⚠️ **上服务器前必须先做**：把 `GLM_KEY` 挪到环境变量（`os.environ["GLM_KEY"]`），
> 否则一旦这台机器是课题组共用，或文件被 scp/截图/提交 git，key 就泄露了。
> 同样地，`candidates.json` / `crossref_toc.json` / `latex_cache/` / `db.sqlite3` 都是生成物，
> 上服务器时可以不带（`harvest.py` 能重建），**别把本地绝对路径写进任何上传的脚本**。

---

## 七、给导师汇报时可直接引用的数字

- **权威分母**：五刊 2000–2025 共 **4437 篇**（Annals 1328 / Inventiones 1837 / JAMS 737 / Acta 322 / IHÉS 213）。导师原估的 1.5 万偏高约 3.4 倍。
- **可获取语料**：有 arXiv 全文的只有 **≈711 篇（16%）**，IHÉS 低到 6.6%。
- **冷启动"三年"**：真实仅 **434 篇**分母，arXiv 可得约 70 篇——不是原以为的 1500 篇。
- **采集精度**：Crossref 背书，误判 0（旧方案查准率仅 39%）。
- 完整方案见 `D:\数学研究平台开发\ai_math_recommend\docs\OPEN_PROBLEM_DB_TECH_SPEC_v0.1.md`（§2 采集 / §4 架构 / §5 成本 / §6 里程碑均已按实测重写）。

### 成本（按 GLM-5.3 官方价 8 元/M 输入、28 元/M 输出实算）

| 口径 | 数值 |
|---|---|
| 单篇实测 | **¥1.87/篇**（≈91k in + 41k out），输入占 39%、输出占 61% |
| 40 篇试跑实际计费 | ¥62.75（含失败也计费），≈¥1.57/篇 |
| 全量 711 篇 | **≈¥1,115**（输入 ¥431 + 输出 ¥684） |
| 走 Batch API（五折） | ≈¥558 |
| 冷启动 70 篇 | ≈¥110 |

> ⚠️ 口径更正：早期用一篇 72k 字符的小论文测得"输出是输入 1.6 倍"，
> 放到真实语料上**结论相反**（输入才是大头）。原因：输入随论文长度线性增长，
> 输出（卡片数）有上限。方案 §5 已用表格更正。
