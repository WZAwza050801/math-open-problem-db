# GPT 网页版第三方质检报告（v1）

- **来源**：网页版 GPT（用户执行，使用 `docs/` 下的独立质检员提示词）
- **日期**：2026-09-17
- **被检对象**：第一批试跑 19 条问题卡（编号体系为旧版 `OP-PILOT-0001..0019`；新版流水线已改用内容派生 hash ID，需另行建立映射后复检）
- **检索截止**：2026-09-17
- **一句话结论**：引文真实性 19/19 无伪造、MSC 标签零错误；但存在 4 条 FAIL（3 条为后续文献已解决未更新、1 条为数学条件被错误加强），总体可信度 5.5/10

> 报告原文照录于下，未做删改。

---

核查口径：我逐字检索了 5 篇论文的 arXiv/PDF 全文，并用问题关键词、精确引文、后续论文题名和 MathOverflow 做了截至 2026-09-17 的检索。必须强调：搜索不到后续解答只能支持"未发现已解决证据"，不能严格证明仍开放。

**【OP-PILOT-0001】判定：PASS**

存在性：引文真实，位于论文引言，见 arXiv:2512.15202 全文。
开放状态：这不是有确定真假答案的开放问题，而是润滑理论的长期研究纲领。无法赋予"现在已解决/未解决"的二值状态。
自包含：改写基本忠实；"rigorously"比原文略强，但后文确实是严格渐近分析，不构成实质改意。
label 是否正确：not_real_open 正确。它是背景动机，不是论文提出的待解问题。
MSC 是否正确：76D08 正是润滑理论，准确。
一句话总结：真实引文、正确识别为领域背景，不应收入真正开放问题库。

**【OP-PILOT-0002】判定：PASS**

存在性：引文真实；同一段随后明确宣布论文将推导该模型。
开放状态：论文自己的 Theorem 6.4 已完成该目标；当前当然不能再标为开放。
自包含：方程、区域、边界条件及极限目标基本准确；与论文 (2.15)–(2.18) 一致。
label 是否正确：not_real_open 正确。这是"此前未研究"的创新性陈述，不是论文结束后留下的问题。
MSC 是否正确：35B27 为均匀化、奇异摄动等，适合作为该目标的主分类；也是原论文 MSC 之一。
一句话总结：典型的"研究空白随后在本论文解决"，提取方判断正确。

**【OP-PILOT-0003】判定：PASS**

存在性：引文真实，原文确实只限制在 Reynolds roughness，即 0<ℓ<1。
开放状态：我搜索了"micropolar + non-standard boundary + Stokes/high-frequency roughness"等组合；发现其他流体或其他边界条件下的结果，但未发现完全相同模型的结论。只能报告"精确变体无法验证是否仍开放"。
自包含：三个尺度区间及物理解释正确，也明确说明这是由范围限制推出来的方向，而非作者正式提问。
label 是否正确：uncertain 合理；若标 real_open 就会过度推断。
MSC 是否正确：35B27 合适。
一句话总结：作为"隐含方向"可以保留在 uncertain 区，不能进入已确认开放问题库。

**【OP-PILOT-0004】判定：SUSPECT**

存在性：引文真实。
开放状态："结果可用于数值模拟和工程实践"没有明确数学命题，谈不上当前开放状态。
自包含：有效模型的公式基本忠实，但改写将一句价值判断扩展成"开展数值模拟"的研究任务，已有轻微任务化加工。
label 是否正确：uncertain 过于宽松；更稳妥应是 not_real_open。这不是疑问、猜想或被指出的理论缺口。
MSC 是否正确：76A05 尚可，但若真讨论数值实现，76Mxx 会更直接。
一句话总结：真实的未来应用暗示被包装成候选问题，属于召回过度。

**【OP-PILOT-0005】判定：FAIL**

存在性：Remark 6.5 及其估计真实存在。
开放状态：我搜索了粗糙边界上非零条件的后续工作，找到粗糙底面、ribbed surface 和不同振幅/波长尺度下的相关结果，如 arXiv:2512.17837，但没有验证到卡片所述完全相同尺度和几何配置已被解决。因此当前状态只能说"未发现精确解答"，不能断言"仍开放"。
自包含：存在实质数学错误。由 Lip(n_ε)=O(ε^{1-2ℓ}) 只能在 ℓ>1/2 时推出发散；ℓ=1/2 时为常数量级，ℓ<1/2 时反而趋零。卡片把它改写成对所有 0<ℓ<1 都趋于无穷，偷偷扩大了条件。原论文本身的"hence diverging"也有同样疑点，提取系统不应无批判复制。
label 是否正确：real_open 过强。原文只证明现有估计方法失效，没有正式断言问题无解或提出 Open Problem。
MSC 是否正确：76A05 可接受，但 35B27/76D08 更能体现该具体问题。
一句话总结：引文是真的，但卡片同时把"方法受阻"升级为开放问题，并传播了一个明显的指数判断错误。

**【OP-PILOT-0006】判定：PASS**

存在性：引文真实，论文确实引用 Bernardes–Bonilla–Peris 的 Question 16；见 arXiv:2511.06207。
开放状态：我搜索了精确短语、"Question 16 mean Li-Yorke"和近年线性动力系统论文；2025 年这篇论文仍明确称其开放，未发现后来解决证据。当前可谨慎视为仍开放。
自包含：两种混沌的定义和问题方向正确：问 mean Li–Yorke chaos 是否蕴含 distributional chaos。
label 是否正确：not_real_open 符合当前提取口径——它是引用自 BBP2020 的背景问题，不是本论文自己的研究目标。若数据库收录"论文中出现的一切开放问题"，则应另设 background_open，而不是改成 real_open。
MSC 是否正确：47A16 即 cyclic/hypercyclic/chaotic operators，准确。
一句话总结：问题本身很可能仍开放，但正确识别为"引用的背景问题"。

**【OP-PILOT-0007】判定：PASS**

存在性：引文真实，紧接着就是"In our second main result, we solve this problem"；见 arXiv:2401.06053。
开放状态：已由本论文 Theorem B 解决，而且结果强到排除了 twisted groupoid von Neumann algebra。
自包含：L_ω(Λ) 与 amplification N^t 的解释足够；只有一个轻微语病"for no t is any amplification"，不影响数学含义。
label 是否正确：not_real_open 正确。
MSC 是否正确：46L35 对因子结构与分类合适。
一句话总结：成功识别"历史开放问题—本论文主定理解决"的结构。

**【OP-PILOT-0008】判定：SUSPECT**

存在性：引文真实；论文明确猜想 𝔠 单射，并称除 max-tb unknot 外仍开放，见 arXiv:2308.00043v3。
开放状态：我搜索了"injectivity of 𝔠"、论文引用与作者后续工作，未发现截至当前的普遍单射证明；可暂报"仍开放，未发现解决文献"。
自包含：主体清楚，但 𝕃-compressing system 的定义漏掉了重要条件：所选压缩圆盘必须两两不交，且圆盘与 conormal cone 的并必须是光滑 Lagrangian disk。遗漏会改变 Lag^c 的定义域。把单射直接解释为"存在 Hamiltonian diffeomorphism"也没有交代压缩系统如何对应。
label 是否正确：real_open 正确。
MSC 是否正确：53D12 准确，也是原论文 primary MSC。
一句话总结：开放问题抓对了，但自包含定义删掉了影响命题含义的条件。

**【OP-PILOT-0009】判定：SUSPECT**

存在性：引文真实；它描述的是论文主结果之前的状态。
开放状态：已被本论文 Theorem 1.1/Corollary 1.3 完全解决；摘要也明确说 resolves surjectivity。
自包含：问题方向正确，但以"with the same notation as above"开头，不满足严格的逐卡独立自包含要求；随后虽补了多数对象，仍没有完整定义 𝕃-compressing system。
label 是否正确：not_real_open 正确。
MSC 是否正确：53D12 正确。
一句话总结：状态判断正确，但卡片仍依赖上一张卡的记号和不完整定义。

**【OP-PILOT-0010】判定：PASS**

存在性：Remark 3.12 的引文真实。
开放状态：我搜索了"W(𝒞(𝔴)) non-degenerate"、weaves、(-1)-closures 及后续论文，未发现该一般非退化性已被证明；当前只能报告"未发现解决证据"。
自包含：QP、非退化性、curve configuration、plabic fence 与预期应用均解释得相当完整；符号虽密集，但研究生可以确定问题是什么。
label 是否正确：real_open 基本合理。虽然原文用"likely"而非"Conjecture"，但它给出了明确可证伪的数学命题及后果。
MSC 是否正确：16G20 对 quiver 表示是合理主标签；加 53D12 作为 secondary 会更完整。
一句话总结：这是本批中质量较高的"非正式但明确"的开放问题抽取。

**【OP-PILOT-0011】判定：PASS**

存在性：Remark 4.14 的引文真实。
开放状态：检索 arbitrary/general Legendrian link、augmentation variety、cluster structure 后，没有发现一般情形被解决。2024 年的 Positive microlocal holonomies are globally regular 给出任意 Legendrian link 上正微局部 holonomy 的全局正则性，但明确只是构造 cluster structures 的关键输入，不等于已构造一般 cluster structure。
自包含：基本忠实地区分了"先定义/证明 cluster structure"与"再实现全部 seed"两个阶段；但 affine scheme 与一般 derived stack 的关系仍略压缩。
label 是否正确：real_open 合理。
MSC 是否正确：53D12 可接受；若强调 derived/cluster 部分，可增加 14A30、13F60。
一句话总结：后续已有重要进展，但尚无证据表明卡片中的一般问题已解决。

**【OP-PILOT-0012】判定：FAIL**

存在性：引文真实，确实是原论文 Section 1.3 的首个猜想，见 arXiv:2006.04987。
开放状态：已经解决。Chevyrev–Shen, arXiv:2302.12160 的 Theorem 2.16 构造了与 Wilson-loop 2D YM measure 一致的轨道空间概率测度，并证明它是该 Markov 过程的唯一不变概率测度。
自包含：对原猜想的表述总体准确。
label 是否正确：论文发表时标 real_open 正确；作为"现在仍开放"的问题卡则错误，必须加 solved_after_publication 和解决文献。
MSC 是否正确：60H15 正确。
一句话总结：典型的时间状态失效——2023 年后续工作已经正面解决整条猜想。

**【OP-PILOT-0013】判定：FAIL**

存在性：引文真实。
开放状态：后续论文 arXiv:2302.12160 的 Theorem 2.12 证明一类 gauge-covariant lattice dynamics 收敛到正确质量重整化的连续 SYM；这正是原文提出的路线，并用于不变测度与 universality 结果。
自包含：有独立事实错误。标准格点规范场的基本 G-值变量放在有向边/link 上；plaquette 上的是边变量乘积形成的 holonomy/action。卡片写成"给每个 plaquette 分配 G-值变量"不正确。
label 是否正确：论文当时的 real_open 正确；当前状态必须改为已解决。
MSC 是否正确：81T25 对 lattice field theory 合适。
一句话总结：既漏掉了后续解决，又把格点规范场的边变量误写成 plaquette 变量。

**【OP-PILOT-0014】判定：SUSPECT**

存在性：引文真实。
开放状态：连接值 DeTurck–Zwanziger SYM 对任意初值的全局生存，在 arXiv:2302.12160 Remark 2.17 中仍明确称未知；但轨道层面的非爆炸已随唯一不变测度和遍历性工作取得解决。2026 年已有题为"global well-posedness of stochastic Yang–Mills–Higgs in two dimensions"的学术报告公告，但我没有检索到可核验的公开预印本，因此不能宣称核心问题已解决，也不能无保留地宣称仍开放。
自包含：很好地区分了连接值全局存在与轨道 Markov 过程非爆炸，这是重要优点；但"for every initial condition"应注明初值所在精确状态空间及解的规范选择。
label 是否正确：论文当时 real_open 正确；当前应标 status_unverified/possibly announced solved，等待公开证明。
MSC 是否正确：60H15 正确。
一句话总结：原卡数学上基本可靠，但 2026 年出现解决公告迹象，当前状态需要人工跟踪。

**【OP-PILOT-0015】判定：SUSPECT**

存在性：引文真实。
开放状态：3D companion paper arXiv:2201.03487 已构造状态空间、规范等价关系和局部 Markov 过程；arXiv:2503.03060 又证明了产生 gauge covariance 的质量重整化唯一性。检索未发现"存在一个在这些粗糙规范轨道上传递作用的具体 gauge group"已解决。
自包含：最大问题是把"把所有结果推广到 3D"打包成一个问题，而其中大部分列举项已经由 companion work 完成。真正未解决的核心应单独写成：构造并证明一个具体 3D 粗糙 gauge group 的轨道恰好等于既定义的 gauge-equivalence classes。
label 是否正确：对上述精确 transitivity 缺口，real_open 合理；对整张卡所列"全部 3D 扩展"，则过宽。
MSC 是否正确：60H15 可以；同时应有 81T13。
一句话总结：真实开放缺口存在，但卡片把已经完成和仍缺失的 3D 结果混在了一张卡里。

**【OP-PILOT-0016】判定：FAIL**

存在性：引文真实，准确描述了早期 loop-indexed 构造与轨道空间测度之间的缺口。
开放状态：已由 arXiv:2302.12160 Theorem 2.16 解决：在 O_α 上得到概率测度，其 loop 有限维分布等于 2D YM measure，并证明其为唯一不变测度。
自包含：原问题解释清楚，Kolmogorov 类比也忠实。
label 是否正确：论文写作时 real_open 可以；当前继续标开放错误。它与 OP-PILOT-0012 在解决后也几乎变成同一结果的两个表述。
MSC 是否正确：81T13 正确。
一句话总结：这是第二个被 Chevyrev–Shen 直接关闭的旧问题，还存在与 0012 重复计数。

**【OP-PILOT-0017】判定：SUSPECT**

存在性：Remark 2.2 引文真实。
开放状态："高维版本是否有用"没有可判定的数学结论，无法核查为已解决或未解决。
自包含：准确解释了状态空间的大意，但擅自加入"任意（紧）流形"；原文只说 any manifold，并未加紧致假设。
label 是否正确：uncertain 尚可作为候选筛选标签，但在最终开放问题库中应降为 not_real_open：它缺少明确对象、性质和成功判据。
MSC 是否正确：60H15 合理。
一句话总结：这是研究品味评论，不是可独立求解的开放问题。

**【OP-PILOT-0018】判定：SUSPECT**

存在性：引文真实；Yang–Mills–Higgs 确实在原文 Example 1.1 中作为框架适用例出现。
开放状态："框架将对多种系统有用"不是数学命题；不能进行现在开放状态核查。
自包含：对 basis-free regularity structures 的概括大体正确，但把一般适用性预期写成"stated future direction"，任务化程度偏高。
label 是否正确：uncertain 对候选阶段可以理解；最终应为 not_real_open。
MSC 是否正确：60H15 正确。
一句话总结：真实的应用前景陈述，但不该作为开放问题卡保留。

**【OP-PILOT-0019】判定：PASS**

存在性：引文真实。
开放状态：一般物理相关维度中的严格 Yang–Mills measure 构造仍是重大开放方向；二维情况已经严格构造，四维 Yang–Mills mass gap 仍在 Clay 问题之列。
自包含：正确加入了"二维已解决、一般高维仍开放"的限定，没有把本文的二维工作说成解决整个构造问题。
label 是否正确：not_real_open 正确。它是著名背景难题，不是本文自己的具体开放目标。
MSC 是否正确：81T13 准确。
一句话总结：著名开放背景被正确识别为背景，而非本论文提出的新任务。

## 汇总表

| 项目 | 数量 |
|------|------|
| 总条数 | 19 |
| PASS | 8 |
| SUSPECT | 7 |
| FAIL | 4 |

## 主要问题分类

| 错误类型 | 涉及卡片 | 说明 |
|---------|---------|------|
| 后续文献已解决但未更新 | 0012、0013、0016 | 均被 arXiv:2302.12160 实质解决 |
| 数学条件被错误加强 | 0005 | ε^{1-2ℓ} 并非对所有 0<ℓ<1 都发散 |
| 把方法失效升级成开放问题 | 0005 | 原文没有正式提出猜想 |
| 基础对象描述错误 | 0013 | lattice gauge variables 在 links/edges 上，不在 plaquettes 上 |
| 自包含定义漏条件 | 0008、0009 | 漏掉压缩圆盘两两不交等条件 |
| 把已完成与未完成任务捆绑 | 0015 | 3D 状态空间、Markov 过程等已有，真正缺口更窄 |
| 非命题式"方向"被收录 | 0004、0017、0018 | "可用于模拟""是否有用""预计有广泛用途"均无真假判据 |
| 重复问题 | 0012、0016 | 后者基本是前者不变测度猜想的测度实现部分 |
| 明显伪造引文 | 无 | 19 条引文均能在原文找到 |
| MSC 大类明显错误 | 无 | 标签总体是本系统表现最好的一项 |

**总体可信度评分：5.5/10。**

提取系统在"找到真实句子"和"识别论文内已解决目标"方面不错，但还不能直接产出可信的当前开放问题数据库；必须增加文献状态更新和数学条件审计。

## 改进建议

1. 建立 paper-time status 与 current status 两套字段，并按 arXiv ID、关键词和引用网络追踪后续论文。
2. 增加标签 background_open、method_obstruction、future_application、solved_after_publication，不要把所有内容压进三分类。
3. 对包含 O(ε^α)、参数区间和量词的改写做符号级一致性检查。
4. 每张卡独立展开定义，并保存原命题的全部假设；禁止 "same notation as above"。
5. 当前开放状态必须附"检索日期、查询式、候选解决文献、为何不构成解决"的审计记录。
