# 服务器部署手册（数学开放问题库 · 采集+提取管线）

> 面向：在服务器上跑**全量**采集与提取。
> 相关文档：`RESUME.md`（断点续跑与已知问题）、`../.gitignore`（哪些不该传）

---

## 0. 五分钟快速路径

```bash
# ① 取代码（二选一，见 §1）
# ② 配密钥
cd pilot && cp .env.example .env && vi .env      # 填 GLM_KEY，或直接 export

# ③ 探活（必须先做，别跳）
python3 probe_keys.py

# ④ 先小跑 20 篇验证链路
PER_JOURNAL=4 python3 harvest.py          # 重建候选（小）
PILOT_WORKERS=4 python3 run_pilot.py

# ⑤ 确认无误后跑全量（后台 + 可断点续跑）
tmux new -s opb
PER_JOURNAL=100000 CANDIDATES_PER_QUERY=2000 python3 harvest.py
PILOT_WORKERS=12 python3 run_pilot.py 2>&1 | tee run_full.log
```

---

## 1. 把代码弄到服务器上（两条路）

### 路 A：git clone（推荐，方便后续更新）

前提：仓库已建远程（**当前尚未创建**，见 §7）。建好后：

```bash
git clone https://github.com/<owner>/open_problem_db.git
cd open_problem_db/pilot
```

### 路 B：打包上传（无需远程仓库，立刻可用）

在**本地**执行，生成一个只含已跟踪文件的干净包（自动排除 `.env`、缓存、数据库）：

```bash
git -C D:/数学研究平台开发/open_problem_db archive \
    --format=tar.gz -o D:/数学研究平台开发/open_problem_db/deploy_opb.tar.gz HEAD
```

然后上传：

```bash
scp deploy_opb.tar.gz user@server:~/
# 服务器上
tar xzf deploy_opb.tar.gz -C ~/open_problem_db && cd ~/open_problem_db/pilot
```

> **`.env` 不在包里**（被 gitignore 拦截），这是故意的。
> 密钥必须**单独**配置，见 §2。

---

## 2. 配置凭据

**代码里没有任何密钥**，只会从两个地方读，优先级：**环境变量 > `.env` 文件**。

```bash
cd pilot
cp .env.example .env
vi .env     # 填 GLM_KEY=...
chmod 600 .env        # 顺手收紧权限
```

或者不用文件、直接注入（更适合容器/systemd）：

```bash
export GLM_KEY="你的key"
```

**验活**（这一步不能跳，能提前发现 key 失效 / 出网被墙）：

```bash
python3 probe_keys.py
```

期望输出 `200`。注意：GLM 的 `reply=''` 是**正常的**——
`max_tokens=10` 被 `reasoning_tokens=10` 吃光了（思考型模型的固有行为），
只要 HTTP 200 就说明 key 和网络都通。

---

## 3. 依赖：**不需要装任何第三方包**

整套管线**只用 Python 标准库**（`urllib` / `tarfile` / `gzip` / `sqlite3` / `json`）。
没有 `requirements.txt`，不需要 `pip install`，不需要虚拟环境。

只需确认 Python 版本：

```bash
python3 --version      # 需要 3.10+，实测环境为 3.13
```

服务器无外网 pip 也能跑，这点在受限环境里很关键。

---

## 4. 全量采集：改语料范围靠环境变量

**默认是试跑规模（每刊 8 篇）**。跑全量**不要改代码**，用环境变量：

```bash
PER_JOURNAL=100000 CANDIDATES_PER_QUERY=2000 python3 harvest.py
```

| 变量 | 默认 | 作用 |
|---|---|---|
| `PER_JOURNAL` | `8` | 每刊保留多少篇。跑全量设成一个大数 |
| `CANDIDATES_PER_QUERY` | `200` | 每条形如 `jr:"Invent. Math."` 的查询取多少 arXiv 结果。**它决定查全率上限**：只有落在这个池子里的论文才能和 Crossref 对上 |

`CANDIDATES_PER_QUERY` 的硬上限是 **2000**（arXiv 单次请求上限）。

想加 `--refresh-toc` 会重新拉 Crossref 全量目录（4437 篇，较慢）。
**如果 `crossref_toc.json` 已在包里，就不用加这个参数。**

### 期望产出（实测口径）

| 指标 | 值 |
|---|---|
| 五大刊 2000–2025 总篇数 | **4437** |
| 其中有 arXiv 全文可抓的 | **≈711（16%）**，IHÉS 低到 6.6% |
| 所以全量提取目标是 | **≈711 篇**，不是 4437 |

> 剩下 84% 缺口是硬约束（不是抓取失败），需要在方案里如实写明，
> 后续靠机构订阅 / zbMATH 摘要 / 出版社 TDM 接口补，**不能假装能拿到**。

---

## 5. 全量提取：并发与耗时

```bash
PILOT_WORKERS=12 python3 run_pilot.py 2>&1 | tee run_full.log
```

### 并发到底能开到多少：先理解瓶颈

| 环节 | 是否并行 | 说明 |
|---|---|---|
| **LLM 提取** | ✅ 并行 | `PILOT_WORKERS` 控制。**这才是提速杠杆** |
| **arXiv 下载** | ❌ 全局串行 | 有全局锁 + `ARXIV_GAP` 秒间隔。arXiv 对突发请求会惩罚，且它**本来就不是瓶颈** |
| 本地解包/截断 | ✅ 并行 | 占用极低 |

所以「多线并行」的正确理解是：**并行在 API 等待上，不在下载上**。
把 `PILOT_WORKERS` 往上加，直到供应商开始限流（表现为 429 或大量超时），再退一档。

### 实测吞吐与投影

| 实测 | 数值 |
|---|---|
| 40 篇 / 6311s / 6 workers | **22.8 篇/小时**，单篇墙钟 158s |
| 11 篇 / 2332s / 4 workers | 17.0 篇/小时（折合 6 workers ≈ 25.5） |

| `PILOT_WORKERS` | 约吞吐 | 全量 711 篇耗时 |
|---|---|---|
| 6（保守） | ~23 篇/小时 | **~31 小时** |
| 12（推荐） | ~39 篇/小时 | **~18 小时** |
| 16（激进） | ~52 篇/小时 | **~14 小时** |

> 并发超过 6 之后的加速按 85% 效率折算（假设部分请求会互相排队）。
> 实际以服务器上的第一次实测为准，跑 20 篇就能校准。

### 另外三个可调参数

| 变量 | 默认 | 什么时候动 |
|---|---|---|
| `ARXIV_GAP` | `5`（秒） | 服务器出网干净、arXiv 没报 406/429 时可降到 `3` |
| `MAX_CHARS` | `260000` | **成本杠杆**。调小直接省钱；代价是长论文中段被截得更多 |
| `TAIL_FRACTION` | `0.35` | 尾部保留比例。开放问题集中在引言和结论，别调太低 |

---

## 6. 费用

按 GLM-5.3 官方价（**8 元/M 输入，28 元/M 输出**），实测成功单篇：

```
91k 输入 + 41k 输出  =  ¥1.87/篇      （输入占 39%，输出占 61%）
```

| 规模 | 费用 |
|---|---|
| 先跑 **100 篇**验证 | **¥187** |
| 冷启动 70 篇 | ¥131 |
| **全量 711 篇** | **¥1,328** |
| 全量走 **Batch API**（五折） | **¥664** |

> ⚠️ **必须提醒**：早期文档里的「全量 ¥165」是**错的**（按输出/输入 1.6 倍的旧口径估的），
> 贵了约 6.8 倍。给导师汇报请用 **¥1,300 上下**。
>
> 对比：同等时长的服务器租金（4核8G 按量）约 **¥15–30**，
> **占总成本 2% 左右**。钱花在 API 上，不在机器上。

---

## 7. 后台长跑：别让 SSH 断开搞死任务

### 推荐：tmux（可随时回来看）

```bash
tmux new -s opb
cd ~/open_problem_db/pilot
PILOT_WORKERS=12 python3 run_pilot.py 2>&1 | tee run_full.log
# Ctrl-B 然后 D 脱离；回来用 tmux attach -t opb
```

### 或者 nohup

```bash
nohup env PILOT_WORKERS=12 python3 run_pilot.py > run_full.log 2>&1 &
echo $! > run.pid
```

### 看门狗（崩溃自愈）

任务跑 18 小时，中途崩一次很亏。用一个循环自动续跑：

```bash
nohup bash -c 'while true; do
  PILOT_WORKERS=12 python3 run_pilot.py >> run_full.log 2>&1
  rc=$?
  echo "[watchdog] exit=$rc $(date)" >> run_full.log
  [ $rc -eq 0 ] && break
  sleep 30
done' > /dev/null 2>&1 &
```

> **为什么这样可以**：`run_pilot.py` 跳过所有已提取的论文，问题卡 ID 由内容派生。
> 重跑**不会重复扣钱**，只会补做失败的部分。全文有本地缓存（`latex_cache/`）。
> 这三点是「随便断、随便续」的基础。

### 监控（跑着的时候也能看）

```bash
python3 status.py          # 只读面板：进度、卡数、token 账、待办清单
tail -f run_full.log       # 实时日志
```

---

## 8. 跑完之后

```bash
python3 make_review.py      # 生成 exports/REVIEW_v3.md + problems_v3.jsonl
python3 validate_cards.py   # 机械校验：引文可核验率、标签合规、重复检测
```

**验收线**（试跑已达标，全量应保持）：

| 指标 | 应有值 |
|---|---|
| 引文可核验率 | ≥ 99% |
| `quote MISSING` | **0**（出现即人工复核） |
| 标签 / 状态 / 格式违规 | **0** |
| 同篇近似重复对 | 0 |

然后把 `exports/` 拉回本地归档：

```bash
scp user@server:~/open_problem_db/pilot/exports/*.{md,jsonl} ./
```

---

## 9. 已知问题（别以为跑完就全好了）

| 问题 | 影响 | 状态 |
|---|---|---|
| **同篇同题重复计数** | 同一主题可能出多张「变体卡」 | ❌ 未修好，必须靠 L3 归一层（向量相似 + LLM 两两仲裁），尚未开工 |
| **状态追踪层** | `current_status` 全是 `unknown` | ⏸ 设计上后置，等更强 API |
| `future_application` 占比 23% | 偏高，与 `real_open` 27% 接近 | ⚠️ 需人工判断是否收紧标签定义 |
| 覆盖率天花板 16% | 4437 篇里只有 ~711 篇有 arXiv 全文 | ⚠️ 硬约束，如实汇报 |

---

## 10. 常见故障速查

| 症状 | 真因 | 处理 |
|---|---|---|
| `502 Bad Gateway` 一批失败 | 出网代理/隧道抖动，**不是代码 bug** | **原样重试**。实测 11 篇失败里 10 篇是它 |
| `URLError: Tunnel connection failed` | 同上 | 同上 |
| `finish=length` + `content_len=0` | 思考 token 吃光预算 | 已修：自动跳下一个模式，不用管 |
| `content_len>0` 但解析失败 | 转义偶发写坏 | 已修：会自动原地重试一次 |
| `arxiv.org/src` 返回 **406** | 该 (host,path,id) 三元组没服务过 | 已修：主通道改用 `export.arxiv.org/e-print` |
| `missing credential GLM_KEY` | 没配密钥 | 见 §2 |
| 速率限制 429 | 并发开太高 | 降 `PILOT_WORKERS`，或加大重试间隔 |

> **排查第一步永远是分辨错误类型**：`error` 字段会把"网络抖动"和"真 bug"混在一起。
> 先看是 `URLError` 还是 `finish=... content_len=...`，再决定要不要动代码。
