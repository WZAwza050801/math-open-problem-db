# 试跑报告 v3：五大刊开放问题提取（Crossref 权威语料）

> 引擎：glm-5.3（GLM Coding Plan 团队版）｜全文：arXiv `/src/` LaTeX → ar5iv HTML 双通道
> 采集：Crossref 按 ISSN 枚举期刊完整目录（2000–2025），再与 arXiv 按 DOI / 标题连接
> 提示词：v2 六分类标签 + 双状态字段 + 条件保全 + 自包含硬化 + 符号级自检

## 总览

- 成功提取论文：**39** 篇
- 候选问题卡：**377** 条（其中 `real_open` 核心产出 **100** 条）
- 消耗 token：输入 3,930,637 / 输出 1,738,570

### 标签分布

| 标签 | 数量 | 含义 |
|------|-----:|------|
| 🟢 `real_open` | 100 | 论文自己提出的真开放问题（核心产出） |
| ⚪ `future_application` | 85 | 应用展望/品味评论（非命题） |
| 🔴 `solved_in_paper` | 74 | 论文内已解决 |
| 🔵 `background_open` | 63 | 引用的著名背景开放问题 |
| 🟠 `method_obstruction` | 53 | 方法/估计失效，但未正式提问 |
| 🟡 `uncertain` | 2 | 上下文不足 |

### 分刊统计

| 期刊 | 试跑提取论文 | 候选卡 | real_open |
|------|-------------:|-------:|----------:|
| Annals of Mathematics | 8 | 76 | 10 |
| Acta Mathematica | 8 | 79 | 28 |
| Inventiones Mathematicae | 8 | 74 | 20 |
| Journal of the American Mathematical Society | 8 | 91 | 35 |
| Publications Mathématiques de l'IHÉS | 7 | 57 | 7 |

### 抓取与提取状态

| 状态 | 数量 |
|------|-----:|
| `extracted` | 39 |
| `extract_failed` | 1 |

Crossref↔arXiv 连接方式：`doi` 36，`title-exact` 3，`title-fuzzy` 1

### 全文通道与提取模式

| 指标 | 分布 |
|------|------|
| 全文通道 | cache-latex: 40 |
| 提取模式 | reasoning: 27，fast: 12 |

---

## 逐篇明细

# Annals of Mathematics

## `2303.15347` — Fundamental groups and the Milnor conjecture
- 权威出处：**Annals of Mathematics** 2025，DOI `10.4007/annals.2025.201.1.4`
- 连接方式：`doi`｜全文 190,172 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟢 `OP-BA4A19EC920D` — `real_open` | MSC 53C20 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.1 (Main Results on Fundamental Groups), Question 1.2 (second question environment)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> If $(M^n,g,p)$ satisfies $\Ric\geq 0$ with the universal cover $\tilde M$ noncollapsed, i.e. $\Vol(B_r(\tilde p))\geq v r^n>0$ for all $r>0$, then is $\pi_1(M)$ finitely generated?

**自包含改写**：Question posed by the paper: if (M^n, g, p) is a pointed Riemannian manifold satisfying Ric ≥ 0 whose universal cover M̃ (with the lifted metric, and p̃ a lift of the basepoint p) is noncollapsed in the sense that Vol(B_r(p̃)) ≥ v·rⁿ > 0 for all r > 0 for some constant v > 0 — where B_r(p̃) is the metric ball of radius r about p̃ and Vol denotes Riemannian volume — then is π₁(M) finitely generated? Context: the paper notes its 7-dimensional counterexamples to Milnor's conjecture are 'quite collapsed in nature' and that 'the issue of finite generation is still open in the noncollapsed setting'.

**判定理由**：Explicitly posed open question by this paper; the noncollapsed-universal-cover case is untouched by the paper's collapsed construction.

**关联卡**：Noncollapsed variant of the Milnor conjecture (see card 1). Related background cited by the paper: Li (if Vol(B_r(p)) ≥ v rⁿ for all large r then π₁ is uniformly finite), Anderson (if b₁(M) ≥ k and Vol(B_r(p)) ≥ v r^{n−k} then π₁ finitely generated), Sormani (small linear diameter growth), Pan (unique metric tangent cone at infinity implies finite generation).

### 🟢 `OP-D6214D93990D` — `real_open` | MSC 53C20 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.1 (Main Results on Fundamental Groups), Question 1.1 (first question environment, after Theorem 1.1)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> If $M^n$ satisfies $\Ric\geq 0$ with $n=4,5$, or $6$, then is $\pi_1(M)$ finitely generated?

**自包含改写**：Question posed by the paper: if M^n is a Riemannian n-manifold satisfying Ric ≥ 0 (nonnegative Ricci curvature) with n = 4, 5, or 6, must the fundamental group π₁(M) be finitely generated? Context: the paper's standing objects are complete smooth manifolds; finite generation was previously known for n ≤ 3 (Cohn-Vossen for n = 2; Schoen–Yau, Liu, Pan for n = 3), while this paper's counterexample to Milnor's conjecture occurs in n = 7, leaving n = 4, 5, 6 open. The authors add: 'The techniques of this paper need to be extended to work in lowest dimensions, and so the above are important open questions.'

**判定理由**：Explicitly posed as an open question by this paper ('We are left with the following open question'); a decidable mathematical statement unresolved at the time of writing.

**关联卡**：Remaining cases of the Milnor conjecture (see card 1) after this paper's 7-dimensional disproof; the authors explicitly state their techniques need extension to lowest dimensions.

**存疑**：The question as literally posed omits an explicit completeness hypothesis; the paper's standing convention (abstract, introduction) is to discuss complete manifolds with Ric ≥ 0.

### 🔵 `OP-44EC9EEC022C` — `background_open` | MSC 53C20 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), background discussion before Section 1.1
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Fukaya and Yamaguchi went on to conjecture in \cite{FukayaYamaguchi} that in the nonnegative sectional context a manifold should have almost abelian fundamental group with the index of the abelian subgroup dimensionally bounded.  An interesting example of Wei \cite{Wei} shows this conjecture cannot hold for manifolds with nonnegative Ricci curvature, though the conjecture remains open for spaces with nonnegative sectional curvature.

**自包含改写**：Fukaya–Yamaguchi conjecture (cited as background): if M^n is a manifold with nonnegative sectional curvature, then π₁(M) is almost abelian, i.e. contains an abelian subgroup of finite index, and the index of this abelian subgroup is bounded by a constant depending only on the dimension n. Wei's example (cited) shows this fails if the hypothesis is weakened from nonnegative sectional curvature to nonnegative Ricci curvature (Ric ≥ 0); per this paper, the conjecture remains open for spaces with nonnegative sectional curvature.

**判定理由**：Famous open conjecture cited purely as background/motivation about sectional curvature; it is not this Ricci-curvature paper's own target.

**关联卡**：Contrasts with the Milnor conjecture card (Ricci ≥ 0 setting), which this paper disproves only in dimension 7; here Wei's example already refuted the Ricci analogue long ago, while the sectional-curvature case remains open.

### 🟠 `OP-7A9A7D31ECBC` — `method_obstruction` | MSC 53C20 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 3 (Inductive Construction), Remark following the Equivariant Mapping Class Group theorem on S³×S³ (Theorem 3.2)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> However for an arbitrary element of the mapping class group we cannot necessarily keep track of the behavior of an isometric action.

**自包含改写**：On S³ × S³ with the standard product metric g_{S³×S³}: the paper proves (Lemma 1.2) that for every diffeomorphism φ ∈ Diff(S³×S³) there is a smooth family of metrics g_t, t ∈ [0,1], with strictly positive Ricci curvature, g_0 = g_{S³×S³} and g_1 = φ*g_0 (the mapping-class-group orbit of the standard metric lies in one connected component of the space of positive-Ricci metrics), and (Theorem 3.2) an equivariant refinement: for each integer k there exist a diffeomorphism φ and a family of metrics with Ric > 0, each invariant under the (1,k)-Hopf circle action θ·_{(1,k)}(s₁,s₂) = (θ·s₁, kθ·s₂) for θ ∈ S¹ (· denoting left Hopf rotation of S³), such that g_1 = φ*g_0 and φ(θ·_{(1,k)}(s₁,s₂)) = θ·_{(1,0)}φ(s₁,s₂). Stated limitation: this equivariant control is established only for specific diffeomorphisms; for an arbitrary element of the mapping class group π₀Diff(S³×S³) the authors cannot necessarily keep track of the behavior of an isometric action. This is a limitation of the method, not a formally posed open problem.

**判定理由**：The remark states a limitation of the equivariant technique (equivariance trackable only for specific mapping-class elements, not arbitrary ones); no open problem is formally posed.

**关联卡**：Complements the paper's solved results: the non-equivariant statement for any mapping-class element (Lemma 1.2, proved in Section 9) and the equivariant statement for the (1,k)-Hopf action with explicit diffeomorphisms φ_k (Theorem 3.2, proved in Section 6, e.g. φ₁(s₁,s₂) = (s₁, s₁⁻¹s₂)).

### 🔴 `OP-25908A15349E` — `solved_in_paper` | MSC 53C20 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Abstract (restated as Theorem 1.1 in Section 1)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> It was conjectured by Milnor in 1968 that the fundamental group of a complete manifold with nonnegative Ricci curvature is finitely generated.  The main result of this paper is a counterexample, which provides an example $M^7$ with $\Ric\geq 0$ such that $\pi_1(M)=\dQ/\dZ$ is infinitely generated.

**自包含改写**：Milnor's 1968 conjecture: if M^n is a complete Riemannian manifold with nonnegative Ricci curvature (Ric ≥ 0), then the fundamental group π₁(M) is finitely generated. This paper disproves the conjecture in dimension n = 7: Theorem 1.1 proves that for any subgroup Γ ≤ ℚ/ℤ ⊆ S¹ — in particular for Γ = ℚ/ℤ, which is not finitely generated — there exists a smooth complete Riemannian manifold (M⁷, g) with Ric ≥ 0 and π₁(M) = Γ.

**判定理由**：The conjecture is this paper's titular target; Theorem 1.1 constructs a complete 7-manifold with Ric ≥ 0 and π₁ = ℚ/ℤ, disproving it as originally stated (no dimension restriction).

**关联卡**：The disproof leaves open refinements posed by this paper: dimensions 4, 5, 6 (Question card 3) and the noncollapsed-universal-cover variant (Question card 4). Background cited: the conjecture was known for n ≤ 3 (Cohn-Vossen n=2; Schoen–Yau, Liu, Pan n=3) and Wilking showed any counterexample must arise from an abelian action.


## `1912.03657` — Eisenstein–Kronecker classes, integrality of critical values of Hecke $L$-functions and $p$-adic interpolation
- 权威出处：**Annals of Mathematics** 2025，DOI `10.4007/annals.2025.202.1.1`
- 连接方式：`title-exact`｜全文 434,008 字符 via `cache-latex`｜提取模式 `reasoning`

### 🔵 `OP-470106CE03B5` — `background_open` | MSC 11G15 | 难度 hard

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, subsection 'The main results' (sentence immediately after the Kufner result)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Conjecturally, these are all CM motives of rank one.

**自包含改写**：Folklore conjecture: every CM motive of rank one arises in the cohomology of an abelian variety; equivalently, the rank-one CM motives arising in the cohomology of abelian varieties — for which Kufner, using this paper's main theorem, settled Deligne's conjecture — exhaust all rank-one CM motives. The paper cites this only as background ('Conjecturally'); it is the missing ingredient to extend the settled cases of Deligne's conjecture to all rank-one CM motives, and the paper does not adopt it as its own research target.

**判定理由**：Explicitly flagged as conjectural but only as background context, not as the paper's own target; still a decidable-ish mathematical statement.

**关联卡**：Residual open part of the Deligne conjecture card: combined with Kufner's theorem it would settle Deligne's conjecture for all rank-one CM motives.

**存疑**：The paper does not elaborate; the referent of 'these' (rank-one CM motives arising in the cohomology of abelian varieties exhausting all rank-one CM motives) is taken from the immediately preceding sentence.

### 🔵 `OP-65975987478C` — `background_open` | MSC 11G15 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, subsection 'The main results'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Kufner \cite{Kufner} has recently been able to deduce the full Deligne conjecture from our main result, so that the Deligne conjecture for CM motives of rank one arising in the cohomology of abelian varieties is now completely settled.

**自包含改写**：Deligne's conjecture (1979) on critical values: for a critical motive M over Q, the critical L-values of M normalized by the Deligne period c^±M (times powers of 2*pi*i) are algebraic numbers. Background status reported by the paper: proved for Hecke L-functions of CM fields by Blasius; Harder and Schappacher announced an approach via Harder's Eisenstein cohomology with full published results only for quadratic extensions of CM fields; Kufner deduced the full conjecture for rank-one CM motives arising in the cohomology of abelian varieties from this paper's main theorem. The conjecture is cited as background and motivation, not posed as this paper's own open target (the paper proves only a weak form).

**判定理由**：Famous conjecture cited as background/motivation; the paper itself proves only a weak form and attributes the full rank-one CM-motive case to Kufner.

**关联卡**：The paper proves its weak form (Corollary*); the residual open part is whether all rank-one CM motives arise from abelian varieties (separate card).

**存疑**：Status as reported within the paper (Blasius, Harder-Schappacher, Kufner); the current literature status cannot be verified from the paper alone.

### 🟠 `OP-0C2BA2E803EB` — `method_obstruction` | MSC 11G15 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, subsection 'Overview of the approach to the theorems'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> This approach of Shimura and Katz breaks down for arbitrary extensions $L$ of $K$ of degree $n$ as the natural habitat of the Eisenstein series in question is the locally symmetric space associated to the arithmetic group $\GL_n(\sO_K)$, which is not hermitian and hence can not be the $\C$-valued points of an algebraic variety.

**自包含改写**：Obstruction: the Shimura-Katz strategy — proving algebraicity of real-analytic Eisenstein series on the Hilbert modular variety (the C-valued points of an algebraic variety, associated to the totally real subfield F of the CM field K) via the q-expansion principle and the Maass-Shimura operators — does not extend to extensions L/K of degree n >= 2: the relevant Eisenstein series then live naturally on the locally symmetric space of the arithmetic group GL_n(O_K), which is not hermitian and hence cannot be the C-valued points of an algebraic variety, so algebraicity cannot be verified geometrically. The paper circumvents this by working equivariantly on the abelian scheme with CM itself (following Bannai-Kobayashi); no open problem is posed here.

**判定理由**：The paper explains why the Shimura-Katz method fails for degree-n extensions (non-hermitian symmetric space of GL_n(O_K)) without formally posing an open problem.

**关联卡**：Motivates the paper's alternative approach via equivariant coherent cohomology on the abelian scheme, which yields the solved integrality and interpolation theorems.

### 🔴 `OP-279A08DF5057` — `solved_in_paper` | MSC 11G15 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, subsection 'Critical values of Hecke L-functions'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> The general case where $L$ is an arbitrary extension of degree $n:=[L:K]$ of an arbitrary CM field $K$ was still open.

**自包含改写**：Let L be a totally complex number field which is a finite extension of arbitrary degree n=[L:K] of an arbitrary CM field K (a totally imaginary quadratic extension of a totally real field), and let chi be a critical algebraic Hecke character of L of conductor frf ('critical' as defined in the paper: the infinity type mu in Z[J_L] is lifted, mu = N_{L/K}^*(mu_0), from a character mu_0 of I_K satisfying mu_0(sigma_0) + mu_0(conjugate of sigma_0) = w for some integer w and all sigma_0 in a CM type Sigma_K of K, and the set {sigma in J_L : mu(sigma) < 0} is a CM type of L). Then for every integral ideal fr c of L coprime to frf there is a number field k with ring of integers O_k such that (chi(frc)·N(frc) - 1)·L(chi,0)/Omega^chi belongs to O_k[1/(frf·N(frc)·d_L)], where d_L is the discriminant of L and Omega^chi is an explicit product of powers of 2*pi*i and periods of abelian varieties with CM by O_L over O_k[1/(frf·N(frc)·d_L)] attached to chi; in particular the algebraicity of L(chi,0)/Omega^chi (the generalization of Shimura's formula suggested by Katz, proved in the paper as Corollary 'cor:Katz-formula') holds. Before this paper the statement was open beyond the case L=K a CM field (Shimura, Katz) and beyond certain extensions of imaginary quadratic fields (Colmez; Bergeron-Charollois-Garcia).

**判定理由**：Paper identifies this general case as open and then proves integrality of the regularized L-values divided by explicit periods (Theorem 'thm:special-values'), including Katz's suggested generalization of Shimura's formula.

**关联卡**：p-adic counterpart is the interpolation Theorem 'thm_p-adic-interpolation'; main tool is the Eisenstein-Kronecker class; the weak Deligne conjecture is a corollary of this result.

**存疑**：The supplied source omits roughly 174,000 characters from the middle of the paper (much of Sections 3-5, including the statement of Theorem 'thm:special-values' and surrounding remarks), so any open problems stated only there could not be extracted.

### 🔴 `OP-4713CF88F0D5` — `solved_in_paper` | MSC 11G15 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, subsection 'The main results', Corollary* (Weak Deligne conjecture, = Corollary 'cor:deligne-conjecture')
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> But we can prove with our methods easily (we thank Blasius for pointing this out) a weak form of Deligne's conjecture \cite{Deligne-conj}: One has \frac{L(\chi,0)}{c^{+} R_{L/\Q}M(\chi)}\in\Qbar^{\times}, where ${c^{+} R_{L/\Q}M(\chi)}$ is the period of the motive $R_{L/\Q}M(\chi)$ defined by Deligne in \cite{Deligne-conj}.

**自包含改写**：For every critical algebraic Hecke character chi of a totally complex number field L (an arbitrary finite extension of a CM field, in the setting of the paper's main theorem), one has L(chi,0) / (c^+ R_{L/Q} M(chi)) in (algebraic closure of Q)^times, where c^+ R_{L/Q} M(chi) is the period of the motive R_{L/Q} M(chi) defined by Deligne. This is the weak (algebraicity-only) form of Deligne's conjecture on critical values for these Hecke characters; proved in the paper as Corollary 'cor:deligne-conjecture', written before Kufner's full deduction became available.

**判定理由**：The paper explicitly states and proves this weak form of Deligne's conjecture with its own methods (Corollary 'cor:deligne-conjecture').

**关联卡**：Weak version of the background card on Deligne's conjecture; the full statement for rank-one CM motives from abelian varieties was deduced by Kufner from this paper's main theorem.

### 🔴 `OP-C0C0283C16FB` — `solved_in_paper` | MSC 11G10 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, subsection 'The main results', Theorem* (Eisenstein-Kronecker class); see Section 2.3 (subsection:Eisenstein-Kronecker-class)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $\cA$ be an abelian scheme over $\cR:=\Spec R$ of relative dimension $d$ and $\Gamma\subset \Aut_{\cR}(\cA)$. Then for any integers $a,b\ge 0$ there is an \emph{Eisenstein-Kronecker class} $\Eis_{\Gamma}^{b,a}(f,x)\in H^{d-1}(\Gamma,H^{0}(\cR,\TSym^{a}(\omega_{\cA/\cR})\otimes\TSym^{b}(\sH)\otimes \omega^{d}_{\cA/\cR} ))$, depending on a $\Gamma$-invariant function $f$ on $\cD$ and a torsion section $x\in (\cA\smallsetminus \cD)(\cR)$.

**自包含改写**：Let A be an abelian scheme of relative dimension d over an affine base R = Spec R, with an action of a subgroup Gamma of Aut_R(A); let D be a finite étale closed subscheme of A consisting of torsion sections (in the paper, D = ker(delta) or ker(delta) minus the unit section for an étale isogeny delta with étale dual), let f be a Gamma-invariant function on D with trace zero (f in R[D]^{0,Gamma}), and let x be a torsion section in (A minus D)(R) fixed by Gamma. Then for all integers a, b >= 0 there exists the Eisenstein-Kronecker class Eis_Gamma^{b,a}(f,x) in H^{d-1}(Gamma, H^0(R, TSym^a(omega_{A/R}) tensor TSym^b(H) tensor omega^d_{A/R})), where omega_{A/R} = e^* Omega^1_{A/R} is the sheaf of invariant differentials, H = Hom(H^1_dR(A/R), O_R) is isomorphic to H^1_dR(A^vee/R), and TSym is the tensor symmetric power algebra. The class is obtained from an equivariant coherent class EK_Gamma(f) in H^{d-1}(A minus D, Gamma; completed Poincaré bundle tensor Omega^d_{A/R}), extended to the universal vector extension with its integrable connection, differentiated a times and evaluated at x via the moment map; the paper also computes it explicitly in terms of generalized Eisenstein-Kronecker series (following Levin). Existence, construction and explicit computation are all proved in the paper.

**判定理由**：The existence, construction and explicit computation of this new equivariant coherent class are carried out and proved in the paper itself; it is the paper's main tool, not an open problem.

**关联卡**：Main tool for the integrality and p-adic interpolation theorems; the paper remarks the class is actually equivariant for the larger group GL_{O_K}(O_L) on O_L tensor A_0 and highlights GL_n(Z), GL_n(O_L) cases as interesting.

### 🔴 `OP-D5536202D8E3` — `solved_in_paper` | MSC 11G15 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, subsection 'The main results', Theorem* (p-adic interpolation); precise version Theorem 'thm_p-adic-interpolation' in Section 5
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $\Sigma$ be a CM type of $L$, which is ordinary for the prime number $p$ (see Section \ref{sec:p-adic-geometric-setup}). For every fractional ideal $\frf$ there exists a $p$-adic measure $\mu_{\frf}$ on $\Gal(L(p^\infty\frf)/L)$ with the following interpolation property: For every critical algebraic Hecke character $\chi$ of attached CM type $\Sigma$ and conductor dividing $p^\infty\frf$, we have

**自包含改写**：Let L be a totally imaginary number field, let Sigma be a CM type of L (lifted from a CM subfield K) which is ordinary for the prime p (as defined in the paper's p-adic geometric setup), and let frf be a fractional ideal of L coprime to p. Construct a p-adic measure mu_frf on Gal(L(p^infinity·frf)/L) such that for every critical algebraic Hecke character chi with attached CM type Sigma and conductor dividing p^infinity·frf, writing the infinity type as mu = beta - alpha with beta in I^+_{conjugate Sigma} and alpha - 1 (the all-ones element) in I^+_Sigma, one has (1/(Omega_p^alpha · (Omega_p^vee)^beta)) · integral of chi over Gal(L(p^infinity frf)/L) d mu_frf = ((alpha-1)!·(2*pi*i)^|beta| / (Omega^alpha·(Omega^vee)^beta)) · Local(chi,Sigma) · prod_{primes p in Sigma_p}(1 - chi(p^{-1})/N p) · prod_{conjugate primes p in conjugate Sigma_p}(1 - chi(p)) · L_frf(chi,0), where Omega, Omega^vee are the complex periods and Omega_p, Omega_p^vee the p-adic periods of a fixed abelian variety with CM by O_L (the p-adic ones depending only on the infinity type), Local(chi,Sigma) is an explicit local factor, Sigma_p denotes the primes of L above p lying in Sigma, and L_frf(chi,0) is the Hecke L-function with Euler factors at primes dividing frf removed. This generalizes Katz's p-adic L-function from CM fields to arbitrary totally complex fields; previously known only for CM fields (Katz) and certain extensions of imaginary quadratic fields (Colmez-Schneps).

**判定理由**：Previously open in general; the paper constructs the measure and proves the interpolation formula (Theorem 'thm_p-adic-interpolation'), extending Katz and Colmez-Schneps.

**关联卡**：p-adic counterpart of the integrality theorem; built from the Eisenstein-Kronecker class and the infinitesimal trivialization of the Poincaré bundle.

### ⚪ `OP-262C0908A3AF` — `future_application` | MSC 11G10 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, subsection 'The main results' (discussion preceding the Eisenstein-Kronecker class Theorem*)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We use the case of an abelian scheme with CM by the ring of integers $\sO_L$ in the number field $L$ and where $\Gamma\subset\sO_L^{\times}$ is a subgroup of finite index, but there are many other interesting cases. For example for an abelian scheme $\cA/\cS$ one can consider the $n$-fold product $\cA^{n}$ of $\cA$ over $\cS$, which has an action of $\GL_n(\Z)$, or if $\cA$ has already CM by $\sO_L$, by $\GL_n(\sO_L)$. We point out that for these groups no arithmetic moduli space exists, but the following theorem contains a construction of group cohomology classes with values in sections of certain algebraic bundles associated to $\cA$.

**自包含改写**：Not a mathematical proposition: a taste/outlook comment. The authors note that beyond the case used for applications to Hecke L-values (Gamma a subgroup of finite index in the units O_L^times acting on an abelian scheme with CM by O_L), there are 'many other interesting cases' of automorphism groups for which their Eisenstein-Kronecker group-cohomology classes are defined — e.g. the n-fold product A^n of an abelian scheme A/S with its GL_n(Z)-action, or with GL_n(O_L)-action when A has CM by O_L — and that although no arithmetic moduli space exists for these groups, their theorem still produces group cohomology classes in sections of algebraic bundles associated to A. (A remark in Section 1 similarly notes the constructed class is actually equivariant for the larger group GL_{O_K}(O_L) acting on O_L tensor_{O_K} A_0, though this is not used for the main results.)

**判定理由**：Explicit value judgement ('many other interesting cases') about future uses of the construction; not a posed open mathematical problem.

**关联卡**：Extends the Eisenstein-Kronecker class card: the paper's theorem already constructs the classes for these groups; further exploration is only suggested.


## `2401.02003` — Naked singularity censoring with anisotropic apparent horizon
- 权威出处：**Annals of Mathematics** 2025，DOI `10.4007/annals.2025.201.3.3`
- 连接方式：`title-exact`｜全文 346,957 字符 via `cache-latex`｜提取模式 `reasoning`

### 🔵 `OP-5B2420F4C5F1` — `background_open` | MSC 83C57 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), Conjecture 1.1 (Weak cosmic censorship conjecture)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> For generic asymptotically flat initial data, the maximal development of Einstein's field equations possesses a complete future null infinity $\mathcal{I}^+$ and hides the possibly formed singularities in a (black hole) region causally disconnected from $\mathcal{I}^+$.

**自包含改写**：Weak cosmic censorship conjecture (Penrose 1969, with the qualifier 'generic' added by Christodoulou 1999): for generic asymptotically flat initial data for Einstein's field equations, the maximal Cauchy development possesses a complete future null infinity I^+, and any singularities that may form in the evolution are hidden inside a black hole region that is causally disconnected from I^+. The paper states this is 'one of the greatest open problems in classic general relativity' and proves an anisotropic censoring mechanism (Theorems 1.1, 1.2) in a characteristic, naked-singularity setting, without attacking the full conjecture.

**判定理由**：Famous open conjecture quoted verbatim as background/motivation; the paper explicitly calls it one of the greatest open problems and does not adopt it as its own target.

**关联卡**：The paper's anisotropic censoring and co-dimension 2k instability theorems provide supporting evidence in a special setting; see also the card on weak cosmic censorship for the spherically symmetric Einstein-Maxwell-charged scalar field system.

### 🔵 `OP-845E502B89B1` — `background_open` | MSC 83C57 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1.5.2 (Related Results: Weak Cosmic Censorship within Spherical Symmetry and Naked Singularity Formation)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The Einstein-Maxwell-charged (complex) scalar field system is the next to be considered. However, the corresponding weak cosmic censorship has remained open since the late 1990s.

**自包含改写**：Open problem (surveyed as related work, not this paper's target): weak cosmic censorship for the spherically symmetric Einstein-Maxwell-charged (complex) scalar field system has remained open since the late 1990s. The paper lists three specific difficulties/questions: (1) the charge Q is non-constant, so almost all previously employed monotonicity formulas (critically used in Christodoulou's Q=0 BV-extension, trapped-surface-formation, and instability arguments) fail, and 'A new strategy to incorporate non-constant charge Q remains to be developed'; (2) for the trapped-surface formation criterion, with eta the initial mass input and delta the small deformation parameter, Christodoulou (uncharged case) needs eta >= C delta log(1/delta), whereas the An-Lim charged-case result requires eta >= delta^{1-omega/2} (> delta log(1/delta)) for a constant 0 < omega << 1, but Christodoulou's 'blue-shift' gamma in the instability argument is of order log(1/delta) rather than delta^{-omega/2} — the paper asks 'How to reconcile?'; (3) 'Can one obtain the same sharp arguments as Christodoulou did?' for the instability theorems. The paper reports that a companion preprint (An-Tan, in preparation) addresses these questions and shows weak cosmic censorship holds, in Christodoulou's sense, for this system.

**判定理由**：Known open problem since the 1990s, surveyed in the Related Results section with posed sub-questions; not this paper's own research target (reported addressed in companion preprint An-Tan).

**关联卡**：Sub-case of the general weak cosmic censorship conjecture (Conjecture 1.1); the three sub-questions (non-constant charge strategy, reconciling eta >= delta^{1-omega/2} with blue-shift gamma ~ log(1/delta), sharp Christodoulou-style instability arguments) are folded into this single card as difficulties of one problem.

**存疑**：Could arguably be labeled real_open since the paper rhetorically poses 'How to reconcile?' and 'Can one obtain the same sharp arguments as Christodoulou did?'; however these arise in a background survey and the paper itself reports companion preprint An-Tan resolving them, so background_open was chosen; current_status left 'unknown' per protocol.

### 🔴 `OP-FB2790F16FB4` — `solved_in_paper` | MSC 83C57 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), motivating question preceding the statement of Theorem 1.1
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Can we relax this requirement by only placing a small anisotropic-in-angle perturbation? If it is possible, this may also significantly raise the co-dimensions of the instability theorems. In this article, we give such an anisotropic result.

**自包含改写**：Question (posed and answered in this paper): Christodoulou's 1999 instability theorem for his spherically symmetric naked-singularity solution of the 3+1-dimensional Einstein-scalar field system required a spherically symmetric perturbation, i.e., a global condition in all angles on the 2-spheres. Can this requirement be relaxed to only a small anisotropic-in-angle perturbation, and if so, can the co-dimensions of the instability theorems be significantly raised? The paper answers affirmatively: prescribing Christodoulou's naked-singularity data on the incoming cone {u_bar = 0, -1 <= u <= 0} and suitable short-pulse data on the outgoing cone H_{-1} for 0 <= u_bar <= delta (upper bound B on up to 5 angular and 3 u_bar derivatives of the shear and of the scalar-field derivative, lower-bound profile f(omega, u_bar) with 0 <= f <= 1 on S^2 x (0,delta] and f >= m on a geodesic ball B_p(epsilon), m in (0,1), epsilon in (0,pi/2), with delta = delta(B) sufficiently small), the Einstein-scalar field system has a unique regular solution in the region 0 <= u_bar <= delta, u_bar <= |u| Omega^{2-delta_tilde}(u,0) <= 1, a unique MOTS M_{u_bar} on each incoming cone H_{u_bar} (0 < u_bar <= delta) forming an achronal apparent horizon that censors the central singularity, and for every k in Z^+ the naked-singularity solution has at least co-dimension 2k nonlinear instability under outgoing characteristic perturbations (Theorem 1.1, Theorem 1.2, and their BV and C^0 versions in the instability-theorems section, the latter allowing perturbations of size g(u_bar) ~ [ln(ln 1/u_bar)]^{-1/2} tending to 0 as u_bar -> 0+).

**判定理由**：Explicit question posed in the introduction and affirmatively resolved by the paper's main theorems (anisotropic apparent-horizon censoring plus arbitrarily high co-dimensional instability).

**关联卡**：Answered by Theorems 1.1 and 1.2 (Section 1) together with their BV/C^0 refinements (Theorems labeled 'main thm section 14' and 'main thm 2 section 14'); background context is the weak cosmic censorship conjecture card.

### ⚪ `OP-37CE79FD10FB` — `future_application` | MSC 83C57 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 2 (Setting), subsection 'An Approach of Bootstrap', Remark (label: small scale critical norm) and its footnote
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The proof strategy and the main theorems of this paper also hold for perturbed Christodoulou's initial data prescribed along $\ub=0$.

**自包含改写**：Claim/outlook (asserted in a remark with footnote-level justification, not proven as a theorem in the main body): the proof strategy and main theorems extend from Christodoulou's exact naked-singularity data to spherically symmetric perturbed initial data on the incoming cone u_bar = 0. Precisely, with Omega_hat(u,0) = Omega(u,0) the lapse and Gamma_hat(u,0) in {(d_u r)/r, (d_{u_bar} r)/r, d_u phi, d_{u_bar} phi} (r the radius function, phi the scalar field), and subscript c denoting the corresponding values of Christodoulou's naked-singularity solution along u_bar = 0, the strategy extends to data satisfying |Omega_hat(u,0)/Omega_hat_c(u,0)| <= 1 + Omega_hat_c(u,0)^{delta_tilde}/a^{1/3} and |Gamma_hat(u,0)/Gamma_hat_c(u,0)| <= 1 + Omega_hat(u,0)^{delta_tilde}/a^{1/3}, for constants 0 < delta_tilde << 1 and a >= 1 (note the first tolerance uses Omega_hat_c^{delta_tilde}, the second uses Omega_hat^{delta_tilde}). A footnote of the same remark further states: 'The methods developed in this paper also allow non-spherically-symmetric initial data prescribed along u_bar=0, the author will provide the details in a separate paper.' This is a stated research direction, not a formally posed proposition.

**判定理由**：Extension claim deferred to footnotes and a separate paper; an outlook on method robustness and future work rather than a posed open problem.

**⚠️ 人工复核标记**：The quantitative perturbed-data claim (with the asymmetric tolerances Omega_hat_c^{delta_tilde} vs Omega_hat^{delta_tilde}) is asserted via the remark plus seven explanatory footnotes rather than proved as a theorem; the non-spherical case is deferred entirely to a future paper.

**关联卡**：Same spirit as the generalization outlook for other Einstein equations (Section 1 remark); both are non-proposition outlooks on the reach of the method.

**存疑**：Borderline between future_application and a mathematical claim: the spherically symmetric perturbation extension is partially justified by footnotes in the proof, but the main theorems are only stated and proved for exact Christodoulou data.

### ⚪ `OP-612ECFDDB9C4` — `future_application` | MSC 83C57 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1, unnumbered remark following the remarks after Theorem 1.2
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The proofs of above two theorems and the approach we demonstrate here have the potential to be generalized to other Einstein field equations. For the hyperbolic part, we employ $\O(u, 0)\rightarrow 0$ as $u\rightarrow 0$. For the elliptic part, we utilize $\O\omb(u, 0)=-\partial_u \log\O(u, 0)/2>0$, which also holds for Rodnianski-Shlapentokh-Rothman's naked-singularity in \cite{R-S} for the Einstein vacuum equations.

**自包含改写**：Outlook statement (not a mathematical proposition): the paper's proof approach has the potential to be generalized to other Einstein field equations; the hyperbolic part relies on Omega(u,0) -> 0 as u -> 0 (Omega the lapse function of the double-null foliation (u, u_bar)), and the elliptic part relies on Omega*omega_underbar(u,0) = -d/du log Omega(u,0) / 2 > 0 (omega_underbar = -(1/2) grad_3 log Omega the incoming connection coefficient evaluated on u_bar = 0), a property the paper notes also holds for the Rodnianski-Shlapentokh-Rothman naked-singularity solution of the Einstein vacuum equations. This is an applicability/taste comment about extending the method; no proposition is posed or proven.

**判定理由**：Value judgment about generalization potential of the method; no concrete mathematical proposition is stated, so it is an application outlook, not an open problem.

**关联卡**：Complements the outlook on perturbed/non-spherical initial data along u_bar = 0 (Remark in 'An Approach of Bootstrap'); both concern the generality of the paper's method.


## `2204.07007` — Symplectic monodromy at radius zero and equimultiplicity of $\mu$-constant families
- 权威出处：**Annals of Mathematics** 2024，DOI `10.4007/annals.2024.200.1.4`
- 连接方式：`doi`｜全文 593,126 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟢 `OP-419415C530A1` — `real_open` | MSC 14B05 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.3, paragraph following Corollary 1.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The \emph{non-isolated} case of Question \ref{q:Zariski}, even for families, remains open, too.

**自包含改写**：Open problem left by this paper: the family version of Zariski's multiplicity question without the isolation hypothesis. Precisely: let f_t:(C^n,0)→(C,0), t∈[0,1], be a continuous family of germs of hypersurface singularities, possibly with non-isolated singularities, whose embedded topological type is independent of t. Is the multiplicity ν(f_t) independent of t? The paper proves the isolated case (Theorem 1.2); for non-isolated germs only special cases are known (Lê-constant families, and topologically constant families of aligned singularities — see related card), so the general non-isolated family version remains open.

**判定理由**：Genuine unresolved mathematical proposition explicitly declared open by this paper, marking the boundary of its main theorem; distinct statement (families, non-isolated) within the scope of Zariski's Question.

**关联卡**：Partial resolutions (Corollary cor:non-isolated, due to Massey using the paper's theorem) are recorded on a separate solved card; the general problem is a consequence-direction of Zariski's Question (background card).

### 🔵 `OP-211341E8D7AA` — `background_open` | MSC 14B05 | 难度 hard

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 8 (Proof of Theorem 1.2), Remark rem:tangent-cone
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The above equality can be seen as an evidence for \cite[Conjecture 1.7]{BBLN_contact-loci}, which asks whether the homotopy type of the Milnor fiber of the tangent cone is a topological invariant.

**自包含改写**：Conjecture (cited from [BBLN_contact-loci, Conjecture 1.7]; external to this paper): the homotopy type of the Milnor fiber of the tangent cone of a hypersurface singularity germ f:(C^n,0)→(C,0) — i.e. of F^in = {in(f)=1}, where in(f) is the initial (lowest-degree homogeneous) part of f — is an invariant of the topological type of f. The paper provides evidence: for a μ-constant family (f_s) of isolated hypersurface singularities, the proof of its Theorem 1.2 shows HF_*(φ_s^ν,+) ≅ H^BM_{*+3n-1-2ν}(F_s^in) (ν the constant multiplicity), hence H^BM_*(F_s^in) is independent of s; however the projectivized tangent cones {in(f_s)=0} ⊂ P^{n-1} may fail to be homotopy equivalent within such a family (cited counterexample).

**判定理由**：External conjecture cited as background; the paper only contributes supporting evidence (Borel–Moore homology invariance) and does not pose or resolve it.

**关联卡**：The proven statement H^BM_*(F_s^in)=H^BM_*(F_0^in) for μ-constant families follows from the paper's main theorem (solved card).

### 🔵 `OP-959EAA7C15B2` — `background_open` | MSC 32S30 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1.3, remark following Corollary 1.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We remark that the question whether every $\mu$-constant family has constant topological type has positive answer if $n\neq 3$ \cite{Le-Ramanujam}, and is open if $n=3$, i.e.\ for families of surface singularities.

**自包含改写**：Open problem (recalled from Lê–Ramanujam context): let (f_t)_{t∈[0,1]}, f_t:(C^3,0)→(C,0), be a μ-constant family of hypersurface germs with isolated surface singularities (all Milnor numbers μ(f_t) finite and equal). Is the topological type of f_t independent of t? For families of isolated hypersurface germs in (C^n,0) with n≠3 the answer is positive (cited to Lê–Ramanujam); the case n=3, i.e. families of surface singularities, is open.

**判定理由**：Well-known open problem (Lê–Ramanujam, 1970s) mentioned as a background remark; not the paper's own target and not addressed by its methods.

**关联卡**：Background to the paper's Corollary 1.3 (topologically constant families are equimultiple); the paper's main theorem does not need this n=3 case since it works directly with μ-constancy.

**存疑**：The paper attributes the n≠3 positive answer to Lê–Ramanujam (which technically covers n≥4; n=1,2 were known by other results); the claim is reproduced as stated in the source.

### 🔵 `OP-D942B25520B1` — `background_open` | MSC 53D40 | 难度 hard

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1.3, closing paragraph; recalled in Section 7.1, Remark rem:chosen_H
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Recently, Nero Budur, L\^e Quy Thuong, Honc Duc Nguyen and the first author have conjectured that the fixed point Floer cohomology of the $m$-th iterate of the monodromy coincides with the compactly supported cohomology of the $m$-th restricted contact locus \cite[Conjecture 1.5]{BBLN_contact-loci}.

**自包含改写**：Arc–Floer conjecture (posed in Budur–Lê–Nguyen–Fernández de Bobadilla, cited as [BBLN_contact-loci, Conjecture 1.5]; not posed by the present paper): for a hypersurface singularity with symplectic monodromy φ and its m-th iterate φ^m, the fixed point Floer (co)homology satisfies HF_*(φ^m,+) ≅ H_c^*(X_m), where X_m is the m-th restricted contact locus. The paper notes this 'might suggest an algebraic approach' to its Theorem 1.2 via variation of contact loci in μ-constant families, but adds 'this problem does not seem easy at all'.

**判定理由**：Conjecture posed in a different paper (even though the first author is a co-author), cited here only as motivation and a possible alternative route; not adopted as this paper's target.

**关联卡**：The paper's Section 7.1 remark on vanishing of Floer differentials in its spectral sequence is presented as compatible with this conjecture (separate card).

### 🔵 `OP-E71557E2785C` — `background_open` | MSC 14B05 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1.3 (A brief history of the Zariski multiplicity conjecture), Question 1.1 (q:Zariski)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Let $f,g\colon (\C^n,0)\to (\C,0)$ be holomorphic germs of the same topological type. Is it true that $f$ and $g$ have the same multiplicity?

**自包含改写**：Zariski's Multiplicity Question: let n≥1 and let f,g:(C^n,0)→(C,0) be holomorphic function germs of the same topological type, i.e. there exists a germ of homeomorphism Φ:(C^n,0)→(C^n,0) with Φ(V(f))=V(g), where V(f) denotes the zero set of f (no isolation hypothesis). Is it true that f and g have the same multiplicity (order at the origin)? The paper proves the positive answer only for continuous families of isolated hypersurface singularities with constant topological type; the non-family version (two arbitrary topologically equivalent isolated germs) and the non-isolated case remain open.

**判定理由**：Famous question posed by Zariski, cited as the paper's motivation; the paper resolves only the μ-constant-family case for isolated singularities, not the question as stated.

**关联卡**：The paper states that after its Corollary 1.3 'the non-family version remains open' — i.e. the isolated-germ special case of this Question; its Example (ex:not-in-a-family) exhibits topologically equivalent isolated hypersurface germs not connected by any μ-constant family, so the family case does not imply the non-family case. The non-isolated case, even for families, is a separate card.

### 🟠 `OP-CD654AA81D12` — `method_obstruction` | MSC 53D40 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.1 (Summary of our approach), discussion of the radius degeneration problem
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> This cobordism is known to be topologically trivial if $n\geq 4$ \cite{Le-Ramanujam}, but proving its symplectic triviality seems hard.

**自包含改写**：Method obstruction identified by the paper: given a μ-constant family (f_t)_{t∈[0,1]} of isolated hypersurface singularities in (C^n,0) and Milnor radii ε_0, ε_t (0 < t ≪ 1, ε_t < ε_0) of f_0 and f_t, the pair (closure of B_{ε_0}∖B_{ε_t}, (closure of B_{ε_0}∖B_{ε_t}) ∩ f_t^{-1}(0)) is a symplectic cobordism between the contact pair of f_t and a pair contactomorphic to that of f_0. It is topologically trivial for n≥4 (Lê–Ramanujam), but its symplectic triviality is not known and 'seems hard'; relatedly, it is not known whether the Milnor radius ε_t can be chosen independent of t (possibly ε_t→0 as t→0), and even Liouville-domain isotopy of the Milnor fibers 'seems hard'. This obstructs the direct comparison of the Floer cohomologies of the monodromies of f_t and f_0 via symplectic isotopy; no formal open problem is posed — the paper bypasses the obstruction with its radius-zero model.

**判定理由**：The paper shows the naive isotopy-comparison method is obstructed by unknown symplectic triviality of the cobordism and possible Milnor-radius degeneration, without formally posing an open problem.

**关联卡**：This is why the paper could not use McLean's contact-pair invariance directly and instead constructs the symplectic monodromy at radius zero (its Steps 1–3).

### 🔴 `OP-0208602CB7A0` — `solved_in_paper` | MSC 14B05 | 难度 medium

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 8 (Proof of Theorem 1.2), Corollary (Massey) cor:non-isolated
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let  $f_t\colon (\C^n,0)\to (\C,0)$ be a continuous family of germs of hypersurface singularities, possibly non-isolated. Assume that $(f_t)$ satisfies one of the following conditions.

**自包含改写**：Corollary proved in the paper (observed by David Massey, using the paper's Theorem 1.2): let f_t:(C^n,0)→(C,0), t∈[0,1], be a continuous family of germs of hypersurface singularities, possibly non-isolated. Assume either (i) for some coordinate system on C^n, all Lê numbers of f_t (Massey's invariants generalizing the Milnor number to non-isolated singularities) are independent of t; or (ii) the embedded topological type of f_t is independent of t and each f_t has aligned singularities (singular locus admits a stratification satisfying the Thom a_f condition whose stratum closures are smooth at the origin). Then the multiplicity of f_t is independent of t.

**判定理由**：Proved within the paper (attributed to Massey), combining the paper's main theorem with Massey's results; it resolves crucial special cases of the open non-isolated family problem.

**关联卡**：Crucial partial case of the open non-isolated family version of Zariski's question (related card); the quote's two enumerated conditions are restated verbatim in meaning in self_contained.

### 🔴 `OP-F0BAD05F0A66` — `solved_in_paper` | MSC 14B05 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), Theorem 1.2 (theo:Zariski)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $(f_t)$ be a continuous family of power series. If the Milnor number $\mu(f_t)$ is independent of $t$ and finite then the multiplicity $\nu(f_t)$ is also independent of $t$.

**自包含改写**：Main theorem (proved in the paper): let (f_t)_{t∈[0,1]} be a continuous family of formal power series f_t ∈ C[[z_1,…,z_n]] (each coefficient a_ι(t) continuous in t). If the Milnor number μ(f_t) = dim_C C[[z_1,…,z_n]]/⟨∂f_t/∂z_1,…,∂f_t/∂z_n⟩ is finite and independent of t, then the multiplicity ν(f_t) (the largest ν with f_t ∈ m^ν, m the maximal ideal of C[[z_1,…,z_n]]) is independent of t. Since μ is a topological invariant (Milnor), it yields Corollary 1.3: a continuous family of holomorphic germs of isolated singularities f_t:(C^n,0)→(C,0), t∈[0,1], whose topological type is independent of t, has multiplicity independent of t — a positive answer to Zariski's Question for families of isolated singularities.

**判定理由**：The paper's main theorem, proved via a symplectic structure on the A'Campo space at radius zero and a generalized McLean spectral sequence; it resolves the family version of Zariski's question.

**关联卡**：Directly answers the family+isolated case of Zariski's Question (related card). Corollary 1.3 (topological-type formulation) and the characteristic-zero algebraic version (Remark rem:algebraic_Zariski, via Lefschetz principle) follow from it; per rule on duplicates these consequences are folded into this card.

### 🟡 `OP-696480EEA513` — `uncertain` | MSC 53D40 | 难度 medium

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Commented-out Question (label q:HF-for-Artal-example) following Example ex:not-in-a-family, Section 8
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Is it true that $\HF_{*}(\phi_0^m,+)=\HF_{*}(\phi_1^{m},+)$ for every $m\geq 1$?

**自包含改写**：Question appearing ONLY in commented-out (%) source text after the paper's example of two isolated hypersurface singularities f_i = g_i + z^2 + w^2 ∈ C[[x,y,z,w]] (double suspensions of the du Bois–Michel plane curve germs g_0, g_1, which have the same integral Seifert form but different embedded topological type): f_0 and f_1 are topologically equivalent but not connected by any μ-constant family. The question asks: for symplectic monodromies φ_0, φ_1 of the Milnor fibrations (in the tube) of f_0 and f_1, is HF_*(φ_0^m,+) = HF_*(φ_1^m,+) for every m ≥ 1? The commented text notes HF_*(φ_i,+) = 0 and HF_*(φ_i^2,+) = Z_2 ⊕ Z_2 (degrees 10, 11) by the paper's formulas, that equality would follow from a μ-constant family connection (which fails), and that the differing Denef–Loeser zeta functions suggest a negative answer (in view of the Arc–Floer conjecture).

**判定理由**：The question occurs only inside commented-out LaTeX in the provided source; it cannot be confirmed as part of the published paper, so context is insufficient to classify definitively.

**⚠️ 人工复核标记**：This question is commented out (%) in the provided LaTeX source; verify whether it appears in the published version before treating it as a question posed by the paper.

**关联卡**：Concerns the pair f_0, f_1 of Example ex:not-in-a-family, which demonstrates that the paper's family result does not imply the non-family Zariski question (related card).

**存疑**：If the question is part of the paper, it is open at paper time (the source's own notes show only m=1,2 computable and a heuristic toward a negative answer); if it was removed before publication, this card should be discarded.

### ⚪ `OP-6E2A99C205C5` — `future_application` | MSC 53D40 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 7, Remark rem:McLean-5.41 (comparison with McLean's model resolution)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Moreover, with minor modifications one can formulate a result analogous to Proposition \ref{prop:monodromy}\ref{item:B_i-boundary},\ref{item:B_i-covering} for a degeneration of projective varieties. In this setting, the Conley--Zehnder index computation in Proposition \ref{prop:monodromy}\ref{item:B_i-CZ} can be carried out, too, provided $\phi$ admits a grading: this happens when fibers are Calabi--Yau.

**自包含改写**：Extension outlook, NOT a formally posed problem: the radius-zero monodromy formalism — the dynamical properties of the fixed-point components B_i (boundary decomposition ∂B_i = ∂^F B_i ⊔ ∂^+B_i with ∂^-B_i = ∅, and diffeomorphisms B_i∖∂^+B_i → B_i° over the m_i-fold coverings ν_i: B_i° → D_i°), and the Conley–Zehnder index formula CZ(B_i) = 2(m/m_i)(a_i+1) − 2m for an m-separating log resolution with multiplicities m_i and discrepancies a_i — extends 'with minor modifications' to degenerations of projective varieties; the Conley–Zehnder index computation carries over provided the monodromy φ admits a grading, which happens when the fibers are Calabi–Yau.

**判定理由**：Feasibility/outlook remark on extending the paper's construction to projective degenerations (Calabi–Yau case); not a conjecture or posed problem.

**关联卡**：Concrete instance of the general outlook that the hybrid technique 'may be useful for other degeneration problems' (related card).

### ⚪ `OP-E0729C0E69D2` — `future_application` | MSC 53D40 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 7.1, Remark rem:chosen_H (dependence on the resolution and ample divisor)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Since the limit $\HF_{*}(\phi^{m},+)$ does not depend on $h$ and $H$, flexibility of these choices suggests that some Floer differentials in \eqref{eq:spectral-sequence-monodromy} should be zero.

**自包含改写**：Heuristic research direction, NOT a formal conjecture: the first page E^1_{p,q} = ⊕_{i∈S_{m,p}} H^BM_{n-1+p+q+2(m/m_i)(a_i+1)-2m}(B_i°) of the paper's spectral sequence converging to HF_*(φ^m,+) depends on the choice of an m-separating log resolution h (if i≠j and D_i∩D_j ≠ ∅ then m_i+m_j > m) and of an ample divisor H = Σ b_i D_i (b_i < 0 on exceptional components), where D = (f∘h)^{-1}(0) = Σ_{i∈P}D_i + Σ_{i∈E}m_iD_i, K_X = Σ a_iD_i, S_{m,p} = {i : m_i|m, p = (m/m_i)b_i}, and B_i° are the associated covering pieces; since the limit does not depend on h and H, the paper suggests some Floer differentials should vanish. Proven partial support: since the action functional decreases along Floer trajectories and the action of B_i° is governed by b_i/m_i, all differentials from H^BM_*(B_i°) to H^BM_*(B_j°) vanish whenever b_i/m_i < b_j/m_j (e.g. for irreducible plane curve germs when D_i lies closer to the root than D_j); in the opposite direction vanishing cannot be guaranteed, and the cusp example (f = x^2−y^3, m = 6) exhibits non-zero differentials.

**判定理由**：Heuristic expectation ('suggests ... should be zero'), a taste remark rather than a formal conjecture; the proven action-monotonicity vanishing is only partial support.

**关联卡**：The remark presents this as compatible with the external Arc–Floer conjecture HF_*(φ^m,+) ≅ H_c^*(X_m) (separate background card).

### ⚪ `OP-E98B1A6D5931` — `future_application` | MSC 53D40 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.1, Step 2 of the proof strategy
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> As we explain below, this step gets rather involved, and creates a technique that may be useful for other degeneration problems in algebraic geometry.

**自包含改写**：Application outlook, NOT a proposition: the paper's technique — performing a real oriented (Kato–Nakayama) blowup, multiplying strata over intersections of components of D = (f∘h)^{-1}(0) by dual-complex faces with 'tropical' coordinates, and choosing an explicit smoothing with a fiberwise symplectic form realizing the radius-zero symplectic monodromy — 'may be useful for other degeneration problems in algebraic geometry'. The construction is carried out in generality covering a holomorphic f: Y→C on a Stein space Y (with exhaustive strictly plurisubharmonic function) such that Y and f^{-1}(0) have only isolated singularities (with rational homology sphere links if dim_C Y = 2).

**判定理由**：Explicit 'may be useful' value judgement about the new hybrid/tropical technique; not a mathematical proposition.

**关联卡**：Related to the Calabi–Yau/projective-degeneration extension outlook (separate card), which is the concrete instance of this outlook mentioned in Section 7.

### ⚪ `OP-F064DA8B98F3` — `future_application` | MSC 14B05 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.3, concluding remarks of the history section
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Nonetheless, even in the curve case ($n=2$), no purely algebraic proof of this statement is known.

**自包含改写**：Stated research direction, NOT a decidable mathematical proposition (so not taskified): Theorem 1.2 (equimultiplicity of μ-constant families) reduces to a purely algebraic statement — each coefficient a_ι(t) a polynomial in t, formulable over any field — yet no purely algebraic proof is known even for plane curve singularities (n=2); the only known proof over C proceeds by topological triviality of μ-constant curve families plus the known positive answer to Zariski's question for n=2. Finding an algebraic proof (a historical motivation for developing the computer algebra system Singular) remains a methodological goal; over algebraically closed fields of characteristic zero the statement itself does follow via Lefschetz principle (Remark rem:algebraic_Zariski, proved in the paper).

**判定理由**：Not a proposition ('purely algebraic proof' is not a decidable statement); it is a stated methodological gap/research direction, hence not taskified.

**关联卡**：Related to the Zariski question card (the n=2 non-family case is known positively); the char-0 field version of Theorem 1.2 is solved in the paper via Lefschetz principle.


## `2307.02749` — The local-global conjecture for Apollonian circle packings is false
- 权威出处：**Annals of Mathematics** 2024，DOI `10.4007/annals.2024.200.2.6`
- 连接方式：`doi`｜全文 76,037 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟢 `OP-BE3D0EE36F16` — `real_open` | MSC 11D99 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.2, paragraph following the Ω(√N) theorem; cf. Section 2 (strip/bug-eye exceptions) and the 'open' column of the main table (Theorem thm:mainthm)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> While Conjecture \ref{conj:old-local-global} is false in general, it may still hold for some packings.

**自包含改写**：For a primitive integral Apollonian circle packing A, a positive curvature c is missing if curvatures ≡ c (mod 24) occur in A but c does not. The admissible residue set R(A) mod 24 is one of six sets; its type is (x,k) with x=|R(A)| (6 or 8) and k the smallest positive residue in R(A) coprime to 24. The paper defines packing-wide invariants: χ₂(A)∈{±1} (in the simplest case χ₂(A) = Kronecker symbol (b/a) for tangent circles of coprime curvatures a,b) and, for types (6,1) and (6,17), χ₄(A)∈{1,i,−1,−i} with χ₄(A)²=χ₂(A) (quartic residue symbol over Z[i]); the extended type is (x,k,χ₂) or (x,k,χ₂,χ₄). Open question left by this paper: does the local-global conjecture (finitely many missing curvatures) still hold for packings of extended type (6,1,1,1) — e.g. the strip packing with root quadruple (0,0,1,1) — or type (8,11,1) — e.g. the bug-eye packing with root quadruple (−1,2,2,3) — where no reciprocity obstruction is found? And for other extended types, does it hold in the residue classes listed as still open: (6,5,1): 5,20,21; (6,5,−1): 5,8,20,21; (6,13,1): 4,12,13,16,21; (6,13,−1): 13,21; (6,17,1,1) and (6,17,1,−1): 8,17,20; (6,17,−1): 17,20; (8,7,1): 7,10,15,18,19,22; (8,7,−1): 3,6,7,10,15,19,22; (8,11,−1): 11,14,15,23 (all modulo 24)? Computations up to 10^10 suggest, e.g., every positive integer ≡5 (mod 24) occurs in the packing (−3,5,8,8), every one ≡13 (mod 24) in (−3,4,12,13), and every one ≡11,14,23 (mod 24) in (−1,2,2,3).

**判定理由**：The paper explicitly leaves the local-global question open for packings of types (6,1,1,1)/(8,11,1) and for the residue classes listed 'open' in its main table; a decidable unresolved question.

**关联卡**：Companion to the disproof card: the exceptional types (6,1,1,1) and (8,11,1) include the strip packing (0,0,1,1) and bug-eye packing (−1,2,2,3); near misses: (0,0,1,1) misses only curvature 241 up to 10^10 in class 1 mod 24, and (−1,2,2,3) misses only 13154 up to 10^10 in class 2 mod 24.

### 🟢 `OP-C5ED6F9541B9` — `real_open` | MSC 11D99 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.2, Conjecture (conj:newlocalglobal)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The set $S_{\cpack}$ is finite.

**自包含改写**：Let A be a primitive integral Apollonian circle packing; a positive curvature c is missing if curvatures ≡ c (mod 24) occur in A but c does not. For u,d>0 set S(d,u)={u·n^d : n∈Z}; S(d,u) is a reciprocity obstruction to A if infinitely many of its elements are admissible mod 24 in A yet no element occurs as a curvature. The paper proves the following obstruction families by extended type (x,k,χ₂[,χ₄]). Quadratic S(2,u), u∈{1,2,3,6}: type (6,1) with χ₂=−1: u∈{1,2,3,6}; (6,5) with χ₂=1: u∈{2,3}, χ₂=−1: u∈{1,6}; (6,13) with χ₂=1: u∈{2,6}, χ₂=−1: u∈{1,3}; (6,17) with χ₂=1: u∈{3,6}, χ₂=−1: u∈{1,2}; (8,7) with χ₂=1: u∈{3,6}, χ₂=−1: u=2; (8,11) with χ₂=1: none, χ₂=−1: u∈{2,3,6}. Quartic S(4,u), u∈{1,4,9,36}: type (6,1) with χ₄∈{−1,i,−i}: all four u; (6,17) with χ₄=1: u∈{9,36}, χ₄=−1: u∈{1,4}, χ₄=±i: all four u. Define the sporadic set S(A) = set of missing curvatures of A not lying in any of these quadratic or quartic obstruction classes for its type. New conjecture posed in this paper: S(A) is finite. Computational evidence: sporadic sets computed (C and PARI/GP) up to N in the range [10^10, 10^12] for three small root quadruples of each of the 14 extended types, with N/(largest sporadic curvature found) exceeding 10.

**判定理由**：New conjecture formulated by this paper (abstract: 'we formulate a new conjecture'), supported by computation but not proven; a genuine open proposition.

**关联卡**：Replacement for the original local-global conjecture card; implies the obstruction lists of the main theorem are complete up to finitely many exceptions (see completeness/method card and the 'other u' card).

### 🟢 `OP-DD275065FEA0` — `real_open` | MSC 11D99 | 难度 easy

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 3.2 (Quadratic forms), after the definition of f_C
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> For the rest of the paper we will assume that $n\neq 0$ for convenience. The results should still hold for $n=0$, but as this only corresponds to the strip packing $(0, 0, 1, 1)$, it will be of no use here.

**自包含改写**：The paper associates to each circle C of non-zero curvature n in a primitive Apollonian circle packing a primitive integral positive definite binary quadratic form f_C of discriminant −4n² (via the bijection (a,b,c,d) ↦ (a+b)x²+(a+b+c−d)xy+(a+c)y²), so that the curvatures of circles tangent to C are exactly the properly represented values f_C(x,y)−n with gcd(x,y)=1; throughout the paper n≠0 is assumed. The authors assert the results 'should still hold' for n=0, which corresponds only to the strip packing with root quadruple (0,0,1,1); this case is not proved in the paper. Open (minor) question left by the paper: do the definitions and results (χ₂, obstruction theorems, tangent-curvature representation) extend to curvature n=0, i.e. to the strip packing?

**判定理由**：A small but genuine decidable extension question the paper explicitly leaves unproven (asserted only as 'should still hold') for n=0 / the strip packing.

**关联卡**：The n=0 case is the strip packing, which is also a type (6,1,1,1) exceptional case in the open-cases card.

**存疑**：Phrased by the authors as an expectation ('should still hold') and dismissed as 'of no use here'; treated as a minor open extension question rather than a formally posed problem.

### 🔵 `OP-F529AAC0628D` — `background_open` | MSC 11A55 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1, Introduction, first paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Apollonian circle packings (Figure~\ref{fig:ACP}) have served as a quintessential example in the study of thin groups, alongside problems such as Zaremba's conjecture for continued fractions (see \cite{Kont13}).

**自包含改写**：Zaremba's conjecture, cited in this paper only as a companion example in the study of thin groups (thin orbits in Z expected to satisfy local-global), and not a target of this paper. Standard formulation (the paper names but does not state it): there exists a fixed bound B (conjecturally B=5) such that every positive integer n occurs as the denominator of a finite continued fraction all of whose partial quotients (after the integer part) are at most B. The paper also notes, citing [Kont13], that there are no congruence obstructions for Zaremba's conjecture.

**判定理由**：Famous open problem mentioned only as background/motivation for thin-group local-global questions; not this paper's own target.

**⚠️ 人工复核标记**：The paper names but never states Zaremba's conjecture; the self-contained formulation is the standard one supplied from the general literature, not from this source.

**关联卡**：Contrast cited in the same section: local-global holds for Soddy sphere packings [Kont19], a solved background result, not extracted as a problem.

### 🟠 `OP-11AF40466527` — `method_obstruction` | MSC 11D99 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 4, Remark at end of section (after the proposition on type (8,k) quadratic obstructions)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It is reasonable to ask if the results in this section can be extended to other values of $u$. The proof will work for larger values of $u$ that have no prime divisors other than $2$ or $3$, but these obstructions are already contained in those with $u\mid 6$. If $u$ has a prime divisor $p\geq 5$, then the Kronecker symbol $\kron{p}{n}$ is not uniquely determined from $n\pmod{24}$. It will rule out $uw^2$ from appearing tangent to a subset of the circles in $\cpack$, but this is not enough to cover the entire packing.

**自包含改写**：For u>0 let S(2,u)={u·n²: n∈Z}; the paper proves quadratic obstructions S(2,u) for u∈{1,2,3,6} in primitive Apollonian packings of suitable extended type. The paper raises the question of extending to other u and shows: (i) the same proof works for u with no prime divisors other than 2 or 3, but the resulting obstructions are already contained in the u|6 cases (nothing new); (ii) if u has a prime divisor p≥5, the Kronecker symbol (p/n) is not uniquely determined by n mod 24, so the method only rules out u·w² from appearing tangent to a subset of the circles of the packing — insufficient to cover the entire packing. Thus the method cannot decide whether such S(2,u) are genuine complete obstructions (the paper's new finite-sporadic-set conjecture predicts they are not, up to finitely many exceptions).

**判定理由**：The paper shows its Kronecker-symbol method fails for u with a prime factor ≥5 and yields nothing new for 2,3-smooth u; no formal open problem is posed.

**关联卡**：A complete obstruction S(2,u) with u having a prime factor ≥5 would contradict the new finite-sporadic-set conjecture card; see also the partial-obstructions card drawn from the same remark.

### 🟠 `OP-900BE951991F` — `method_obstruction` | MSC 11D99 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 4, paragraph following the proposition on quadratic obstructions for type (6,k)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Note that not listing a value of $u$ as a quadratic obstruction in the table does not imply that it cannot be an obstruction, only that this proof method does not rule it out. The completeness of these lists is discussed in Section \ref{sec:computations}.

**自包含改写**：For a primitive Apollonian circle packing A, the paper proves quadratic obstructions S(2,u)={u·n²: n∈Z}, u∈{1,2,3,6}, by showing that a curvature u·w² occurring in A would force, for a tangent circle of curvature n coprime to 6uw², the Kronecker-symbol identity (u/n)=χ₂(A) (type (6,k)) or (2u/n)=χ₂(A) (type (8,k)), where n is determined modulo 24. Limitation stated by the paper: the absence of a value of u from the obstruction table does not imply that S(2,u) fails to be an obstruction for A — only that this proof method does not rule it out. Completeness of the obstruction lists is discussed only computationally (Section 6) and is implied, up to finitely many exceptions, by the new conjecture that the sporadic set is finite.

**判定理由**：Documents that the tabulated obstruction lists are method-limited rather than asserted complete; no formal open problem is posed here beyond the new conjecture.

**关联卡**：Completeness of the obstruction lists is, up to finitely many sporadic exceptions, equivalent to the new finite-sporadic-set conjecture card.

### 🔴 `OP-40E00C28E796` — `solved_in_paper` | MSC 11D99 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1.2, Conjecture (conj:old-local-global), attributed to [GLMWY02, FS11]
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes (disproven in general for infinitely many packings; open for types (6,1,1,1) and (8,11,1))

**原文引文**

> The number of missing curvatures in $\cpack$ is finite.

**自包含改写**：Let A be a primitive integral Apollonian circle packing (generated by a Descartes quadruple (a,b,c,d) of integers with gcd(a,b,c,d)=1). A positive curvature c is called missing in A if some curvature congruent to c modulo 24 appears in A but c does not. Conjecture (Graham–Lagarias–Mallows–Wilks–Yan 2002, revised by Fuchs–Sanden 2011): the number of missing curvatures in A is finite, i.e. every sufficiently large integer in an admissible residue class modulo 24 occurs as a curvature. This paper disproves it in general: it proves there exist infinitely many primitive Apollonian circle packings for which the number of missing curvatures up to N is Ω(√N), and that the conjecture fails in at least one residue class modulo 24 for every primitive packing not of extended type (6,1,1,1) or (8,11,1), via quadratic obstructions {u·n² : n∈Z}, u∈{1,2,3,6}, and quartic obstructions {u·n⁴ : n∈Z}, u∈{1,4,9,36}, determined by the packing's extended type. For packings of extended type (6,1,1,1) and (8,11,1) the question remains open (tracked in a separate card).

**判定理由**：The paper's main theorem disproves this prior conjecture for infinitely many packings (Ω(√N) missing curvatures); it remains unresolved only for the exceptional types (6,1,1,1) and (8,11,1).

**⚠️ 人工复核标记**：The universal conjecture is disproven, but the per-packing statement is still open for packings of extended type (6,1,1,1) and (8,11,1); prior best positive result was Bourgain–Kontorovich: missing curvatures up to N at most O(N^(1-η)) for some effectively computable η>0.

**关联卡**：Same conjecture historically called the 'Strong Density Conjecture'; its open remainder is the 'exceptions' card; its replacement is the new sporadic-set conjecture card.

### ⚪ `OP-0D31D8EF4698` — `future_application` | MSC 11B99 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 4, final Remark (same remark as the 'other values of u' discussion)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Interestingly, this suggests that there may be ``partial'' obstructions: quadratic families whose members appear less frequently than other curvatures of the same general size.

**自包含改写**：The authors speculate there may be 'partial' obstructions: quadratic families {u·n²} (in particular those with u having a prime divisor ≥5, for which the complete-obstruction method fails) whose members appear as curvatures less frequently than other curvatures of the same general size in a primitive Apollonian circle packing. This is a speculative research direction inferred from the method's partial coverage; it is not a formal conjecture or precisely stated proposition, so it is not taskified here.

**判定理由**：A speculative phenomenon ('may be partial obstructions') suggested by the method's partial coverage; not a formal mathematical proposition.

**关联卡**：Drawn from the same Section 4 Remark as the 'other values of u' method-obstruction card.

### ⚪ `OP-7CE90B7ED9EB` — `future_application` | MSC 20H10 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.3, 'Reciprocity obstructions in thin groups'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Despite this, one expects other instances of thin groups or semigroups to produce reciprocity obstructions; another example is studied in the follow-up paper \cite{RickardsStangeTwo}.

**自包含改写**：Background philosophy: thin orbits in Z (orbits of thin groups such as the Apollonian group) were expected to satisfy a local-global principle — congruence restrictions only, with all sufficiently large admissible integers occurring; this paper shows reciprocity obstructions violate it for Apollonian packings. As a general research direction, the authors state that despite settings with no congruence obstructions (Zaremba's setting) or where local-global holds (Soddy sphere packings), one expects other instances of thin groups or semigroups to produce reciprocity obstructions; another example is studied in their follow-up paper (Rickards–Stange). This is an expectation/outlook, not a formal conjecture or precisely posed problem.

**判定理由**：A general expectation about thin group/semigroup orbits producing reciprocity obstructions; a research outlook, not a posed proposition.

**关联卡**：General thin-group outlook containing this paper's result (disproof card) as an instance; the follow-up paper studies another example.

### ⚪ `OP-A1C49008FACE` — `future_application` | MSC 11B99 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 6 (Computations), Remark
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> An intrepid observer of the raw sporadic sets may remark that, toward the tail end, the sporadic curvatures are disproportionately multiples of $5$.  In fact, they generally prefer prime divisors which are $1 \pmod{4}$.  We speculate that this is another local phenomenon:  a result of certain symmetries of the distribution of curvatures in the orbit of quadruples modulo $p \equiv 1 \pmod{4}$ (similar to \cite[Figures 3 and 4]{FS11}).

**自包含改写**：In the computational data (sporadic sets S_A(N), i.e. missing unobstructed curvatures up to N, computed with C and PARI/GP up to N between 10^10 and 10^12 for many small root quadruples), the sporadic curvatures toward the tail end are disproportionately multiples of 5 and generally favor prime divisors p ≡ 1 (mod 4). The authors speculate this is another local phenomenon, arising from certain symmetries of the distribution of curvatures in the orbit of Descartes quadruples modulo p ≡ 1 (mod 4). This is a speculation about observed data with a heuristic explanation, not a formal conjecture or precisely stated proposition.

**判定理由**：A 'we speculate' heuristic about computational data and a proposed local explanation; not a formal mathematical proposition.

**关联卡**：Concerns the sporadic set of the new local-global conjecture card.

### ⚪ `OP-B9DCB5260F3F` — `future_application` | MSC 52C26 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 2, Remark following Corollary cor:discovery
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It is quite possible that quadratic obstructions occur in these packings, which share many features with the present case.  The existence of quartic obstructions is less likely, as it arises because $K=\QQ(i)$.  The family of packings studied in \cite{FSZ19} are also governed by quadratic forms (this was the essential feature needed for the positive density results of that paper), and include the $K$-Apollonian packings; these are likely subject to quadratic obstructions as well.  It would also be interesting to ask the same question about an even wider class of packings studied by Kapovich and Kontorovich \cite{KK23}.

**自包含改写**：Research directions on generalizations, stated as plausibility judgments rather than formal conjectures: (a) K-Apollonian packings, defined for each imaginary quadratic field K (the Q(i)-Apollonian case is this paper's subject): the authors judge it 'quite possible' that quadratic reciprocity obstructions occur in these; quartic obstructions are judged 'less likely' since the quartic mechanism relies on K=Q(i); (b) the family of packings studied in [FSZ19], which are governed by quadratic forms and include the K-Apollonian packings, are 'likely subject to quadratic obstructions as well'; (c) the authors state it 'would also be interesting to ask the same question' (whether reciprocity obstructions occur) about the even wider class of packings studied by Kapovich and Kontorovich [KK23].

**判定理由**：Plausibility judgments ('quite possible', 'less likely', 'likely') and an 'interesting to ask' direction about generalized packings; not formal propositions.

**关联卡**：Generalizes the obstruction phenomenon of the disproof card; the follow-up paper Rickards–Stange (see thin-groups card) studies another example.

### ⚪ `OP-E70AD86D648F` — `future_application` | MSC 52C26 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1, Introduction, closing paragraph of the opening discussion
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In this paper, we demonstrate that, for infinitely many (and perhaps most, in a suitable sense) Apollonian circle packings, the local-global conjecture is nevertheless false.

**自包含改写**：The paper proves the local-global conjecture fails for infinitely many primitive Apollonian circle packings, and adds the parenthetical speculation that it fails for 'perhaps most' packings 'in a suitable sense' — i.e. that some (unspecified) density or counting statement on the space of packings might show that a majority of packings carry reciprocity obstructions. The 'suitable sense' is not defined anywhere in the paper, so this is a value judgment / research outlook about prevalence, not a formal mathematical proposition, and is not taskified here.

**判定理由**：Parenthetical speculation ('perhaps most, in a suitable sense') about the prevalence of the failure; the sense is undefined, so not a proposition.

**关联卡**：Vague prevalence counterpart of the 'infinitely many packings' disproof card; the proven part (infinitely many, Ω(√N)) is tracked there.


## `2012.01307` — Characterizing finitely generated fields by a single field axiom
- 权威出处：**Annals of Mathematics** 2023，DOI `10.4007/annals.2023.198.3.4`
- 连接方式：`doi`｜全文 116,346 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟢 `OP-037160777182` — `real_open` | MSC 03C60 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Abstract
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Our
  solution is conditional on resolution of singularities in
  characteristic two and unconditional in all other characteristics.

**自包含改写**：Open remainder of the main result: for a finitely generated field K (function field of an integral Z-scheme of finite type) with char(K) = 2 and Kronecker dimension dim(K) > 3 — i.e., since char(K) > 0 we have dim(K) = td(K), the absolute transcendence degree, so td(K) >= 4 — prove, without any resolution-of-singularities hypothesis, that there exists a first-order sentence theta_K in the language of rings such that every finitely generated field L satisfies theta_K if and only if L is isomorphic to K. Equivalently, remove the paper's dependence (via Jannsen's Theorem 0.10 for n = 2, which is conditional) on 'resolution of singularities above F_2', namely: (i) every proper integral F_2-variety X admits a proper birational morphism from a smooth (equivalently regular) F_2-variety; (ii) every affine smooth F_2-variety U has an open immersion into a projective smooth F_2-variety X with X \ U a simple normal crossings divisor. The same unconditional question concerns the bi-interpretability of such K with the ring Z.

**判定理由**：The abstract explicitly concedes that in characteristic two the solution is only conditional; the unconditional existence of theta_K for char(K)=2, dim(K)>3 is a genuine unresolved proposition left open by this paper.

**⚠️ 人工复核标记**：This is a formalization of the abstract's stated conditionality; the paper never lists it as a numbered open problem. Note that the paper does treat char 2 with dim(K) <= 3 unconditionally, since resolution is known up to dimension three.

**关联卡**：Would follow from 'resolution of singularities above F_2' (background card) together with Theorem 1.1 (solved card); it is exactly the case excluded unconditionally from Theorems 1.1, 1.2 and 1.3.

**存疑**：The paper gives no indication whether an unconditional proof avoiding resolution of singularities might be easier than resolution of singularities itself.

### 🔵 `OP-635A163AAD82` — `background_open` | MSC 03C60 | 难度 medium

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), paragraph immediately after Theorem 1.2
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Note that while this completely characterizes the 
definable sets in $K$, certain questions of uniformity 
across the class of finitely generated fields are left 
open, see e.g. \cite[Question~1.8]{PoonenUniform}.

**自包含改写**：The paper observes that although bi-interpretability with Z completely characterizes the definable sets of an infinite finitely generated field K, certain questions of uniformity of first-order definitions across the entire class of finitely generated fields are left open, citing Question 1.8 of B. Poonen, 'Uniform first-order definitions in finitely generated fields', Duke Math. J. 138 (2007). The present paper's Theorem 1.3 gives uniformity of the prime-divisor-defining formulas val_d only over fields of a fixed Kronecker dimension d satisfying Hypothesis (H_d), and does not address the cited question.

**判定理由**：Open uniformity questions imported from Poonen's earlier paper and cited as still open; this paper neither restates nor adopts nor resolves them, so they are background.

**⚠️ 人工复核标记**：Poonen's Question 1.8 is not restated in this paper; its precise content must be checked in Duke Math. J. 138 (2007) before this card's target is reused.

**关联卡**：Contrasts with the fixed-d uniformity established in the Theorem 1.3 card.

**存疑**：The exact content of the uniformity questions said to be left open is external to this source.

### 🔵 `OP-691FA8457A2D` — `background_open` | MSC 14E15 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 2 (Preliminaries), definition of 'resolution of singularities above F_2'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Following \nmnm{Jannsen}, see \cite[Definition 4.18]{Ja}, 
we say that 
%
\emph{resolution of singularities holds above $\mathbb{F}_2$} if 
the following hold: 
\vskip2pt 
\itm{32}{
\item[(i)$\,$] For any proper integral $\lvF_2$-variety $X$, there 
is a proper birational morphism $\tilde X \to X$, where $\tilde X$ 
is a smooth (or equivalently regular) $\lvF_2$-variety. 
\vskip2pt 
\item[(ii)] Every affine smooth $\lvF_2$-variety $U$ has an
open immersion $U \hookrightarrow X$, where $X$ is a 
projective smooth $\lvF_2$-variety, and $X\backslash U$ 
is a simple normal crossings divisor.

**自包含改写**：Resolution of singularities above F_2 (following Jannsen, Definition 4.18): (i) for any proper integral F_2-variety X there is a proper birational morphism X~ -> X where X~ is a smooth (equivalently regular) F_2-variety; (ii) every affine smooth F_2-variety U has an open immersion U -> X into a projective smooth F_2-variety X with X \ U a simple normal crossings divisor. Status reported in the paper: this is well known for surfaces and holds in dimension three (in general) by Cossart-Piltant (J. Algebra 321 (2009)); in dimension >= 4 it is open. If it holds, every finitely generated field of characteristic two has a smooth proper model over F_2. The present paper assumes it in Hypothesis (H_d) exactly when char(K) = 2 and d > 3, so its Theorems 1.1-1.3 are conditional on it in that case.

**判定理由**：Famous open problem (resolution of singularities in positive characteristic, here in the F_2 formulation); adopted only as a hypothesis, not posed or attacked as this paper's own target.

**⚠️ 人工复核标记**：The paper's background claim that resolution 'holds in dimension three (in general)' by Cossart-Piltant — in particular whether this covers condition (ii), the SNC compactification — is a secondary-source assertion; verify its scope if relied upon.

**关联卡**：This is Hypothesis (H_d)'s assumption for char 2, d > 3 in the Theorem 1.1/1.2/1.3 cards; proving it would close the real_open unconditional characteristic-2 card.

### 🔵 `OP-CBD121627E0B` — `background_open` | MSC 14F42 | 难度 hard

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 2 (Preliminaries), paragraph introducing the cohomological local-global principles
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> proposed that for ``arithmetically significant'' fields $K$ with 
$\dim(K)=d$, e.g.\ for finitely generated fields, there should 
hold similar LGPs for $\HHx{d+1} K d$, see  \nmnm{Kato}'s 
seminal paper~\cite{Kato_LGP}, in particular 
%
for
%
how Milnor K-theory plays into the bigger picture. In the same paper,
\nmnm{Kato} proved several forms of such LGPs for finitely 
generated fields $K$ with $\dim(K)=2$. There was/is steady 
progress on Kato's conjectures, see \nmnm{Kerz-Saito}
\cite{K-S} and \nmnm{Jannsen}~\cite{Ja}, where both more
literature and an account of previous results can be found.

**自包含改写**：Kato's proposed higher-dimensional local-global principle (background conjecture, from K. Kato, 'A Hasse principle for two-dimensional global fields', J. reine angew. Math. 366 (1986)): for 'arithmetically significant' fields K of Kronecker dimension d — in particular for finitely generated fields, where dim(K) = td(K)+1 if char(K)=0 and dim(K) = td(K) if char(K)>0 — there should hold local-global principles for the cohomology groups H^{d+1}(K, Z/n(d)) (where Z/n(i) = mu_n^{\otimes i} if char(K) does not divide n, and Z/m(i) \oplus W_r \Omega^i_log[-i] if n = m p^r with (m,p)=1 and char(K) = p), analogous to the Brauer-Hasse-Noether injectivity for the Brauer group of a global field, with the role of Milnor K-theory part of the bigger picture. Kato proved several such LGPs for finitely generated fields with dim(K) = 2; the paper reports steady progress (Kerz-Saito Theorem 8.1; Jannsen Theorem 0.4, unconditional for n = 2 and char(K) \neq 2; Jannsen Theorem 0.10, for n = 2 in characteristic 2 conditional on resolution of singularities above F_2) and uses these n = 2 instances as established facts.

**判定理由**：Kato's conjectures are cited as the source of the paper's cohomological tools and remain open in general; they are not this paper's own target.

**⚠️ 人工复核标记**：The paper only says there 'was/is steady progress on Kato's conjectures'; it does not delimit which cases remain open, so this card's openness refers to the general conjecture.

**关联卡**：Supplies the Facts 2.1-2.3 (Jannsen, Kerz-Saito) underpinning the Theorem 1.3, 1.1 and 1.2 cards; its characteristic-2 instance (Jannsen Theorem 0.10) depends on the resolution-of-singularities-above-F_2 card.

### 🔴 `OP-02DFF40F116C` — `solved_in_paper` | MSC 03C60 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), Theorem 1.1 (\label{thm1})
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $K$ be a finitely generated field. If $\chr(K) = 2$ and 
$\dim(K)>3$, assume that resolution of singularities above 
$\lvF_2$ holds. Then there exists a sentence $\theta_K$ 
in the language of rings such that any finitely generated 
field $L$ satisfies $\theta_K$ if and only if $L \cong K$.

**自包含改写**：The strong Elementary Equivalence versus Isomorphism Problem (EEIP), current since the 1970s (first posed explicitly in F. Pop, Invent. Math. 150 (2002)): determine whether the first-order theory of a finitely generated field K (a field that is the function field of an integral Z-scheme of finite type) determines its isomorphism type within this class. Proven here in the strong form: for every finitely generated field K there exists a first-order sentence theta_K in the language of rings such that every finitely generated field L satisfies theta_K if and only if L is isomorphic to K. Here Kronecker dimension is dim(F) := td(F)+1 if char(F)=0 and dim(F) := td(F) if char(F)>0, where td(F) is the absolute transcendence degree. The only conditional case: if char(K)=2 and dim(K)>3, the proof assumes that resolution of singularities above F_2 holds, in the sense of Jannsen [Ja, Definition 4.18]: (i) every proper integral F_2-variety X admits a proper birational morphism X~ -> X with X~ a smooth (equivalently regular) F_2-variety; (ii) every affine smooth F_2-variety U has an open immersion U -> X into a projective smooth F_2-variety X such that X \ U is a simple normal crossings divisor.

**判定理由**：Theorem 1.1 is proved here, resolving the strong EEIP (hence the EEIP) for all finitely generated fields; only the characteristic-2, dim(K)>3 case rests on the resolution hypothesis, tracked separately.

**关联卡**：The unresolved unconditional characteristic-2 remainder is the real_open card quoting the abstract; the hypothesis itself is the resolution-of-singularities card; intermediate proven statements are Theorem 1.3 (uniform definability of geometric prime divisors) and Theorem 1.2 (bi-interpretability with Z). Theorem 1.1 follows from Theorem 1.2 via [AKNS, Proposition 2.28].

### 🔴 `OP-07EC1FF6E719` — `solved_in_paper` | MSC 03C60 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), Theorem 1.3 (\label{thm2})
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $d \geqslant 3$.
The geometric prime divisors of fields satisfying $(\HH_d)$ are uniformly first-order
  definable. In other words, there exists a formula $\val_d(X, \underline Y)$ in the language of rings such that for every field $K$ satisfying $(\HH_d)$ and every geometric prime divisor $\mathcal{O}$ of $K$ there exists a tuple $\underline y$ in $K$ such that
  \[ \mathcal{O} = \{ x \in K \colon K \models \val_d(x, \underline y) \}, \]
  and conversely, for every tuple $\underline y$, the subset of $K$ defined above is either a geometric prime divisor or empty.

**自包含改写**：For each integer d >= 3 there exists a formula val_d(X, Y) in the language of rings such that: for every field K satisfying Hypothesis (H_d) — i.e., K is finitely generated with dim(K) = d (dim(F) = td(F)+1 if char(F)=0, dim(F) = td(F) if char(F)>0, td = absolute transcendence degree), and if char(K) = 2 and d > 3, resolution of singularities above F_2 is assumed to hold — and for every geometric prime divisor O of K (a discrete valuation of K, identified with its valuation ring, whose residue field Kv satisfies dim(Kv) = dim(K) - 1 and char(Kv) = char(K)), there is a tuple y in K with O = { x in K : K satisfies val_d(x, y) }; and conversely, for every tuple y in K, the set { x in K : K satisfies val_d(x, y) } is either a geometric prime divisor of K or empty. This was the key missing step toward the strong EEIP, by Scanlon's reduction; the cases dim(K) = 1, 2 were previously known (Rumely 1980; Pop 2017).

**判定理由**：Theorem 1.3, the paper's chief technical result, is proved in Sections 3-4; uniform definability of geometric prime divisors was previously established only for Kronecker dimension at most 2.

**关联卡**：Main technical ingredient for the Theorem 1.1 and Theorem 1.2 cards; its uniformity is only for fixed Kronecker dimension d, cf. the Poonen uniformity card.

### 🔴 `OP-A13A1433AADE` — `solved_in_paper` | MSC 03C60 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), Theorem 1.2 (unlabeled theorem between Theorems 1.1 and 1.3)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $K$ be an infinite finitely generated field. If $\chr(K) = 2$
and $\dim(K)>3$, assume that resolution of singularities 
above $\mathbb{F}_2$ holds. Then $K$ is bi-interpretable 
with $\Z$ (where both $K$ and $\Z$ are considered as 
structures in the language of rings).

**自包含改写**：For every infinite finitely generated field K (as a structure in the language of rings), if char(K) = 2 and Kronecker dimension dim(K) > 3 (dim(F) = td(F)+1 if char(F)=0, dim(F) = td(F) if char(F)>0), assume resolution of singularities above F_2 holds — i.e., (i) every proper integral F_2-variety X admits a proper birational morphism from a smooth (equivalently regular) F_2-variety, and (ii) every affine smooth F_2-variety U has an open immersion into a projective smooth F_2-variety X with X \ U a simple normal crossings divisor — then K is bi-interpretable with the ring of integers Z (both taken as structures in the language of rings). Bi-interpretability with Z entails that the class of definable sets of K is as rich as possible (cf. Aschenbrenner-Khelif-Naziazeno-Scanlon, Lemma 2.17).

**判定理由**：Theorem 1.2 is proved in Section 5, completing the bi-interpretability program initiated by Scanlon (2008), whose original argument had a gap in the prime-divisor definability recipe (2011 erratum).

**关联卡**：Proved from the uniform definability of geometric prime divisors (Theorem 1.3 card) plus [AKNS, Theorem 3.1] on finitely generated domains and Scanlon's reduction; implies the Theorem 1.1 card via [AKNS, Proposition 2.28]. Its unconditional characteristic-2 case is part of the real_open card.

### ⚪ `OP-C37E61E877ED` — `future_application` | MSC 03C60 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.1 (Short historical note and the genesis of this article)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It would also be interesting to treat the EEIP for fields which are finitely generated
over natural base fields such as $\mathbb{C}$, $\mathbb{R}$ and $\mathbb{Q}_p$, cf.~\cite{PoonenPop}.

**自包含改写**：Not a formal proposition — an outlook: the authors state it 'would also be interesting' to treat the Elementary Equivalence versus Isomorphism Problem (whether the first-order theory, in the language of rings, of a field determines its isomorphism type within the class considered) for fields that are finitely generated over base fields such as the complex numbers C, the real numbers R, and the p-adic numbers Q_p, referring to B. Poonen and F. Pop, 'First-order characterization of function field invariants over large fields', LMS Lecture Note Series 350 (2007). No conjecture or precise question is posed.

**判定理由**：'It would also be interesting' is an application outlook/taste comment, not a posed proposition; per the no-taskification rule it is labeled future_application and not turned into a task.

**关联卡**：Analogue of the Theorem 1.1 card (EEIP for finitely generated fields) for fields finitely generated over C, R, or Q_p.

### ⚪ `OP-F1DE042AA81D` — `future_application` | MSC 03C60 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.1 (Short historical note and the genesis of this article)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Finally, in this note the authors do not discuss the natural
question of the complexity of the formulas describing
prime divisors, thus the sentences characterizing the isomorphism 
type.

**自包含改写**：Not a formal mathematical proposition — a stated research direction: the authors explicitly do not treat the 'natural question' of the complexity (e.g., length or quantifier structure) of the first-order formulas val_d defining the geometric prime divisors of finitely generated fields satisfying Hypothesis (H_d), and consequently of the sentences theta_K that characterize a finitely generated field up to isomorphism within the class of finitely generated fields. No precise question, conjecture, or complexity measure is formulated in the paper.

**判定理由**：Taste/outlook remark flagging an undiscussed aspect (formula complexity); no decidable proposition is stated, so per the no-taskification rule it is not converted into an open problem.

**关联卡**：Quantitative refinement of the Theorem 1.3 card (formulas val_d) and the Theorem 1.1 card (sentences theta_K).


## `1910.04947` — Dimension formulae and generalised deep holes of the Leech lattice vertex operator algebra
- 权威出处：**Annals of Mathematics** 2023，DOI `10.4007/annals.2023.197.1.4`
- 连接方式：`doi`｜全文 212,588 字符 via `cache-latex`｜提取模式 `reasoning`

### 🔵 `OP-5080ECA8C718` — `background_open` | MSC 17B69 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 3.3 (Orbifold Construction), paragraph on the module category of V^G
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> This proves a conjecture by Dijkgraaf, Vafa, Verlinde and Verlinde \cite{DVVV89} who stated it for arbitrary finite $G$.

**自包含改写**：Conjecture of Dijkgraaf–Vafa–Verlinde–Verlinde, cited as background: for a strongly rational, holomorphic vertex operator algebra V over ℂ and an arbitrary finite group G of automorphisms of V, the module category of the fixed-point vertex operator subalgebra V^G is the twisted group double D_ω(G) of G. The paper records that the cyclic case G ≅ ℤ_n is proved (in [EMS20a]), with the 3-cocycle [ω] ∈ H³(G, ℂ*) ≅ ℤ_n determined by the type t ∈ ℤ_n of a generator; the original statement for arbitrary finite G is not proved in this paper.

**判定理由**：DVVV conjecture cited as background; only the cyclic case is recorded as proved; the originally stated general-finite-group case is left unaddressed here.

**⚠️ 人工复核标记**：The openness of the arbitrary-finite-group case is implied by the sentence, not explicitly asserted as open; confirm current status from the literature.

**存疑**：The paper does not itself treat the general-finite-group case; this card infers the general case remains the open target of the cited conjecture.

### 🔵 `OP-FDF841BDD206` — `background_open` | MSC 17B69 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 6.4 (Classification of Generalised Deep Holes), first paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Recall that the Moonshine module $V^\natural$ is a \strathol{} \voa{} $V$ of central charge $24$ with $V_1=\{0\}$ and conjecturally the only such \voa{} up to isomorphism.

**自包含改写**：Background conjecture: the Moonshine module V^♮ is, up to isomorphism, the unique vertex operator algebra V over ℂ that is strongly rational (rational, C_2-cofinite, self-contragredient, of CFT type) and holomorphic (V is its only irreducible module), has central charge 24, and has trivial weight-1 space V_1 = {0}. The paper treats this as conjectural and notes elsewhere that the identification V_Λ^{orb(g)} ≅ V^♮ for its rank-0 generalised deep holes 'would immediately follow' from it, but bypasses it via Carnahan's results.

**判定理由**：Famous background conjecture (uniqueness of the Moonshine module among central-charge-24 strongly rational holomorphic VOAs) cited as context, not this paper's own target.

**关联卡**：Connected to the classification of generalised deep holes: the 38 rank-0 generalised deep holes of V_Λ have orbifold isomorphic to V^♮, which the paper notes would follow immediately from this uniqueness conjecture.

**存疑**：A second passage (proof of the Moonshine-orbifold proposition in Section 6.4) states the identification 'would immediately follow if it were known' that V^♮ is unique; both passages refer to the same conjecture.

### 🟠 `OP-4C4828A5FFBF` — `method_obstruction` | MSC 17B69 | 难度 easy

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 5.3 (Dimension Bounds), remark immediately after the Deligne-bound theorem
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes (the order-14 extremal examples are established in the paper)

**原文引文**

> We remark that the theorem does not extend to the non-prime case. For example, there are extremal orbifolds of order $14$ (see Table \ref{table:70}).

**自包含改写**：The obstruction of the Deligne-bound theorem (R(g) ≥ 24, excluding extremality for prime-order g with X_0(p) of positive genus) does not extend to automorphisms of composite order n: the paper exhibits extremal orbifold constructions of composite order n = 14 (of the Leech lattice VOA V_Λ, among the 70 generalised deep holes listed in its table, which includes orders 14 for cycle shape 2^{12}). Thus the prime-order hypothesis is necessary for this Deligne-bound obstruction; no formal open problem about composite orders is posed.

**判定理由**：Paper demonstrates a hypothesis (prime order) is needed for the obstruction to work, exhibiting a counterexample at composite order 14; no open problem is formally posed.

**关联卡**：Limitation of the Deligne-bound theorem card; shows the genus-based obstruction is genuinely a prime-level phenomenon.

### 🔴 `OP-6683A2894BE0` — `solved_in_paper` | MSC 17B69 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, paragraph on the history of the dimension formula (result proved as Second Dimension Formula, Section 5.2)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> The dimension formula was first proved by Montague for $n=2,3$ \cite{Mon94}, then generalised to $n=5,7,13$ \cite{Moe16} and finally to all $n>1$ such that $\Gamma_0(n)$ has genus~$0$ in \cite{EMS20b}. The previous proofs all used explicit expansions of the corresponding Hauptmoduln. We show here that the dimension formula is an obstruction coming from the Eisenstein space.

**自包含改写**：Dimension formula (Second Dimension Formula): Let V be a strongly rational (rational, C_2-cofinite, self-contragredient, CFT-type), holomorphic vertex operator algebra of central charge 24 over ℂ, and g ∈ Aut(V) an automorphism of order n > 1 of type 0 (the conformal weight ρ(V(g)) of the unique irreducible g-twisted V-module V(g) lies in (1/n)ℤ) such that V^g satisfies the positivity condition (every irreducible V^g-module W ≇ V^g has ρ(W) > 0). Then dim(V_1^{orb(g)}) = 24 + Σ_{m|n} c_n(m)·dim(V_1^{g^m}) − R(g), where the rationals c_n(m) (m | n) are defined by Σ_{m|n} c_n(m)·gcd(t,m) = n/t for all t | n, and R(g) = Σ_{γ∈D, q(γ) ≢ 0 mod 1} d_n(γ)·dim(W^{γ}_{1−r_γ}) with D = ℤ_n × ℤ_n, q((i,j)) = ij/n mod 1, r_γ ∈ (0,1) with r_γ ≡ −q(γ) mod 1, W^γ the n² irreducible V^g-modules, and explicit non-negative coefficients d_n(γ); in particular R(g) ≥ 0, so dim(V_1^{orb(g)}) ≤ 24 + Σ_{m|n} c_n(m)·dim(V_1^{g^m}). Previously known only for n = 2, 3; n = 5, 7, 13; and all n > 1 with X_0(n) of genus 0 (n ∈ {2,3,4,5,6,7,8,9,10,12,13,16,18,25}); this paper proves it for all n > 1.

**判定理由**：Formula was open for general order n > 1 before this paper (known only for n = 2,3,5,7,13 and genus-0 levels); the paper proves it for all n > 1.

**关联卡**：The Deligne-bound theorem strengthens the rest term for prime order p with g(X_0(p)) > 0; the 'further restrictions' outlook card generalises the same pairing mechanism. The First Dimension Formula and both dimension bounds are corollaries of the same circle of results (not separate cards).

### 🔴 `OP-B95AC4082F53` — `solved_in_paper` | MSC 17B69 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, paragraph on Schellekens' 1993 result
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes (existence part only; uniqueness part settled earlier by others)

**原文引文**

> He conjectured that all potential Lie algebras are realised and that the $V_1$-structure fixes the \voa{} up to isomorphism.

**自包含改写**：Schellekens' conjecture (1993): for a strongly rational, holomorphic vertex operator algebra V of central charge 24 over ℂ (whose weight-1 space V_1 is a reductive Lie algebra with at most 71 possible isomorphism classes on Schellekens' list), (i) every Lie algebra on the list is realised as V_1 of such a VOA (existence; equivalently all 70 non-zero ones), and (ii) V is determined up to isomorphism by its V_1-structure (uniqueness). The paper states the full result 'is now proved' by the work of many authors, and itself proves part (i) uniformly: for each of the 70 non-zero Lie algebras 𝔤 on Schellekens' list there exists a generalised deep hole g ∈ Aut(V_Λ) of the Leech lattice VOA V_Λ with (V_Λ^{orb(g)})_1 ≅ 𝔤 (Uniform Construction theorem), generalising the Conway–Parker–Sloane/Borcherds deep-hole construction of the Niemeier lattices.

**判定理由**：The paper proves the existence half uniformly as a main result; the full conjecture is recorded as already settled by many authors. Only the existence part is proved here.

**关联卡**：The existence half is the paper's Uniform Construction theorem; together with the Holy Correspondence it underlies the classification of generalised deep holes. The motivating special case (deep holes of Λ giving the 23 Niemeier lattice VOAs) is proved in Section 6.1.

**存疑**：The uniqueness half of the conjecture is not proved in this paper; the paper cites the complete classification (by many authors) as background input.

### 🔴 `OP-BFA1ECADDC83` — `solved_in_paper` | MSC 17B69 | 难度 medium

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 5.3 (Dimension Bounds), Theorem (thm:delignebound)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $V$ be a \strathol{} \voa{} of central charge $24$ and $g\in\Aut(V)$ of prime order~$p$ and type~$0$ such that $V^g$ satisfies the positivity condition. If $g(X_0(p))>0$, then $R(g)\geq24$ and hence $g$ cannot be extremal.

**自包含改写**：Let V be a strongly rational, holomorphic vertex operator algebra of central charge 24 over ℂ and g ∈ Aut(V) an automorphism of prime order p, of type 0 (ρ(V(g)) ∈ (1/p)ℤ), such that V^g satisfies the positivity condition. Let R(g) be the rest term of the Second Dimension Formula, R(g) = Σ_{γ∈D, q(γ) ≢ 0 mod 1} d_n(γ)·dim(W^{γ}_{1−r_γ}), with D = ℤ_p × ℤ_p, q((i,j)) = ij/p mod 1, r_γ ∈ (0,1), r_γ ≡ −q(γ) mod 1, W^γ the irreducible V^g-modules. If the modular curve X_0(p) has positive genus, then R(g) ≥ 24; hence g is not extremal (dim(V_1^{orb(g)}) < 24 + Σ_{m|p} c_p(m)·dim(V_1^{g^m}), with c_p(m) defined by Σ_{m|p} c_p(m)·gcd(t,m) = p/t for all t | p) and consequently g is not a generalised deep hole of V. Proved in the paper via pairing the character of V^g with the lift of a Hecke eigenform in S_2(Γ_0(p))^− and Deligne's bound |a(m)| ≤ σ_0(m)√m.

**判定理由**：Theorem proved in the paper: Deligne's bound on cusp-form coefficients forces R(g) ≥ 24 under the stated prime-order, positive-genus hypotheses, excluding extremality.

**关联卡**：Limitation noted in the immediately following remark (separate card): the conclusion fails for composite order.

### 🔴 `OP-D0033F938ACC` — `solved_in_paper` | MSC 17B69 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 6.4 (Classification of Generalised Deep Holes), Theorem (thm:class)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> There are exactly $108$ algebraic conjugacy classes of \gdh{}s $g$ of the Leech lattice \voa{} $V_\Lambda$ (see \autoref{table:11})

**自包含改写**：Classification of generalised deep holes: the generalised deep holes g of the Leech lattice vertex operator algebra V_Λ — by definition automorphisms of finite order n > 1, of type 0 (ρ(V_Λ(g)) ∈ (1/n)ℤ), with V_Λ^g satisfying the positivity condition, that are extremal (dim((V_Λ^{orb(g)})_1) = 24 + Σ_{m|n} c_n(m)·dim((V_Λ^{g^m})_1), with c_n(m) defined by Σ_{m|n} c_n(m)·gcd(t,m) = n/t for all t | n) and rank-minimal (rk((V_Λ^{orb(g)})_1) = rk((V_Λ^g)_1)), together with the identity by convention — comprise exactly 108 algebraic conjugacy classes (conjugacy classes of cyclic subgroups of Aut(V_Λ)): 70 classes with rk((V_Λ^g)_1) > 0, whose orbifold constructions yield the 70 strongly rational, holomorphic vertex operator algebras of central charge 24 with V_1 ≠ {0}, and 38 classes with rk((V_Λ^g)_1) = 0, whose orbifold constructions all yield the Moonshine module V^♮. Proved in the paper.

**判定理由**：Full classification theorem proved in the paper, combining the Holy Correspondence, the community classification of central-charge-24 VOAs, and Carnahan's orbifold constructions of V^♮.

**关联卡**：Builds on the Holy Correspondence and the Uniform Construction; the rank-0 part relies on Carnahan's orbifold constructions of V^♮ and connects to the Moonshine-uniqueness conjecture (background card). The auxiliary theorem identifying the 11 cycle shapes in O(Λ) is part of this classification package.

**存疑**：The proof uses as background inputs the classification of strongly rational holomorphic VOAs of central charge 24 with V_1 ≠ 0 (work of many authors) and Carnahan's constructions of the Moonshine module.

### 🔴 `OP-F426D76BC174` — `solved_in_paper` | MSC 17B69 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 6.3 (Uniform Construction of Schellekens' List), Theorem 'Holy Correspondence' (thm:main2)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> The cyclic orbifold construction $g\mapsto V_\Lambda^{\orb(g)}$ defines a bijection between the algebraic conjugacy classes of \gdh{}s $g\in\Aut(V_\Lambda)$ with $\rk((V_\Lambda^g)_1)>0$ and the isomorphism classes of \strathol{} \voa{}s $V$ of central charge $24$ with $V_1\neq\{0\}$.

**自包含改写**：Holy Correspondence: the cyclic orbifold construction g ↦ V_Λ^{orb(g)} defines a bijection between (a) algebraic conjugacy classes (conjugacy classes of cyclic subgroups ⟨g⟩ ≤ Aut(V_Λ)) of generalised deep holes g of the Leech lattice vertex operator algebra V_Λ — i.e. automorphisms of finite order n > 1, of type 0 (ρ(V_Λ(g)) ∈ (1/n)ℤ), with V_Λ^g satisfying the positivity condition, that are extremal (dim((V_Λ^{orb(g)})_1) = 24 + Σ_{m|n} c_n(m)·dim((V_Λ^{g^m})_1), with c_n(m) defined by Σ_{m|n} c_n(m)·gcd(t,m) = n/t for all t | n) and satisfy rk((V_Λ^{orb(g)})_1) = rk((V_Λ^g)_1) — with rk((V_Λ^g)_1) > 0, and (b) isomorphism classes of strongly rational, holomorphic vertex operator algebras V of central charge 24 with V_1 ≠ {0}. Proved in the paper using inverse orbifolding and an averaged version of Kac's very strange formula; generalises the Conway–Parker–Sloane/Borcherds deep-hole–Niemeier-lattice correspondence.

**判定理由**：Main theorem (Holy Correspondence) proved in the paper, establishing the bijection that generalises the deep-hole/Niemeier correspondence to Schellekens' list.

**关联卡**：Together with the Uniform Construction theorem (existence half of Schellekens' conjecture) it yields the 70 positive-rank classes in the classification of generalised deep holes.

**存疑**：Generalised deep holes are a notion introduced in this same paper, so the bijection is a new theorem about a new notion rather than a pre-existing open problem.

### ⚪ `OP-A01EA876CC02` — `future_application` | MSC 17B69 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 6.4, remark after the theorem on the 11 cycle shapes (thm:main4)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> This shows that we recover the decomposition of the genus of the Moonshine module described by Höhn in \cite{Hoe17}. There is probably an automorphic proof of this result (cf.\ \cite{Sch17}).

**自包含改写**：The paper proves (Theorem thm:main4) that under the natural projection Aut(V_Λ) → O(Λ) the 70 algebraic conjugacy classes of generalised deep holes g with rk((V_Λ^g)_1) > 0 map to exactly 11 algebraic conjugacy classes in O(Λ), with cycle shapes 1^{24}, 1^8 2^8, 1^6 3^6, 2^{12}, 1^4 2^2 4^4, 1^4 5^4, 1^2 2^2 3^2 6^2, 1^3 7^3, 1^2 2^1 4^1 8^2, 2^3 6^3 and 2^2 10^2, recovering Höhn's decomposition of the genus of the Moonshine module. The extracted item is the authors' remark that there probably exists an automorphic(-forms) proof of this result — a proof-strategy outlook, not a formal open problem.

**判定理由**：Taste comment on a probable alternative (automorphic) proof of a result the paper proves by other means; not a formal open problem or proposition.

**关联卡**：Concerns Theorem thm:main4, the projection of the 70 positive-rank generalised deep holes onto 11 cycle shapes in O(Λ), part of the classification package.

**存疑**：'This result' refers to the recovery of Höhn's genus decomposition, i.e. Theorem thm:main4.

### ⚪ `OP-ACFDE545F5DE` — `future_application` | MSC 17B69 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 6.3, paragraph after the Holy Correspondence theorem
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> This shall be addressed in a forthcoming publication \cite{MS21} using geometric properties of \gdh{}s.

**自包含改写**：Announced research direction (forthcoming publication by the authors, cited as [MS21]): classify the strongly rational, holomorphic vertex operator algebras of central charge 24 with non-trivial weight-1 space by classifying the generalised deep holes g ∈ Aut(V_Λ) with rk((V_Λ^g)_1) > 0, using geometric properties of generalised deep holes. This is an outlook/announcement of future work, not a mathematical proposition.

**判定理由**：Announcement of forthcoming work; a research direction (geometric classification route), not a decidable mathematical proposition posed here.

**关联卡**：Alternative route to the classification achieved in this paper (Theorem thm:class); the present paper instead proceeds from the VOA classification to the generalised deep holes.

**存疑**：[MS21] is announced as forthcoming at the time of writing; its content is not available in this source.

### ⚪ `OP-CE2FE17F8354` — `future_application` | MSC 17B69 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, paragraph on the history of the dimension formula
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Pairing the character of $V^g$ with other modular forms for the dual Weil representation we can obtain further restrictions.

**自包含改写**：Method outlook: for V a strongly rational, holomorphic vertex operator algebra of central charge 24 over ℂ and g ∈ Aut(V) of finite order n and type 0 with V^g satisfying the positivity condition, the character Ch_{V^g}(τ) = Σ_{γ∈D} ch_{W^γ}(τ) e^γ (with D = ℤ_n × ℤ_n, q((i,j)) = ij/n mod 1, W^γ the irreducible V^g-modules) is a vector-valued modular form of weight 0 for the Weil representation ρ_D of SL_2(ℤ); the paper's dimension formula arises by pairing it with one specific weight-2 Eisenstein series for the dual Weil representation ρ̄_D, and the authors state that pairing it with other modular forms for ρ̄_D can yield further restrictions on V and g. No specific further restriction is formulated; this is a value judgement about the method, not a proposition.

**判定理由**：Method outlook on extending the pairing mechanism beyond the chosen Eisenstein series; no specific proposition or open problem is formulated.

**关联卡**：Generalises the pairing mechanism behind the dimension formula card; the paper also proves the Deligne-bound obstruction by pairing with a cusp-form lift, one instance of this outlook.

**存疑**：The sentence expresses potential of the method; the Deligne-bound theorem in the paper realises one instance (cusp forms of Fricke eigenvalue −1).


## `2007.15644` — Higher uniformity of bounded multiplicative functions in short intervals on average
- 权威出处：**Annals of Mathematics** 2023，DOI `10.4007/annals.2023.197.2.3`
- 连接方式：`doi`｜全文 318,546 字符 via `cache-latex`｜提取模式 `fast`

### 🟢 `OP-00299DAB0BBD` — `real_open` | MSC 11L41 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1, after Corollary 1.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It is natural to conjecture that such uniform bounds extend to all $\theta>0$, but this seems well beyond the reach of the methods in this paper.

**自包含改写**：Let λ denote the Liouville function. For k ≥ 0 and 0 < θ < 1, conjecture that sup_{x ∈ [X,2X]} ||λ||_{u^{k+1}([x,x+H])} = o(1) as X → ∞, where H = X^θ. Currently this is proven for θ > 2/3.

**判定理由**：The paper explicitly poses extending uniform (non-averaged) bounds on the weak Gowers norms of λ to all θ > 0.

**关联卡**：The paper proves the averaged version (Corollary 1.3) but not the uniform version.

### 🟢 `OP-54EF27611822` — `real_open` | MSC 11N37 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.2
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Thus, in order to prove the logarithmic Chowla conjecture, it would suffice to bridge the gap between $H\geq X^{\eta}$ (which is the range where Corollary~\ref{cor: mult-pret} is valid) and $H\leq (\log X)^{\eta}$ in Proposition~\ref{entropy}.

**自包含改写**：Open problem: Extend the estimate ∫_X^{2X} ||λ||_{U^{k+1}([x,x+H])} dx = o(X) (or its logarithmic version) from the range H ≥ X^η down to H ≤ (log X)^η, bridging the gap between Corollary 1.6 and Proposition 1.10, which would then imply the logarithmic Chowla conjecture.

**判定理由**：The paper explicitly identifies this gap-bridging as the remaining task to prove logarithmic Chowla.

**关联卡**：Related to Tao's Conjecture 1.6 from [TaoEq] and Proposition 1.10.

### 🟢 `OP-C1E59233E4F5` — `real_open` | MSC 11L41 | 难度 medium

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1, after Theorem 1.4
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The upper bound $H \leq X^{1-\theta}$ here is for minor technical reasons and it is likely that one can replace it with $H \leq X$; however our main interest is in the opposite regime when $H$ is as small as possible.

**自包含改写**：Minor open problem: In Theorem 1.4 (non-pretentious multiplicative functions do not correlate with polynomial phases on short intervals on average), replace the upper bound H ≤ X^{1-θ} with H ≤ X.

**判定理由**：A specific technical improvement the authors identify as likely but do not prove.

### 🔵 `OP-34EA82EBA327` — `background_open` | MSC 11N37 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1.3.1
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Theorem~\ref{superpolynomial} can be viewed as progress towards a conjecture of Sarnak in~\cite{sarnak} that the Furstenberg systems of the Liouville function have positive entropy (so that in particular $s(k)\gg c^k$ for some $c>1$).

**自包含改写**：Sarnak's conjecture: The Furstenberg systems of the Liouville function have positive entropy, implying s(k) ≫ c^k for some c > 1, where s(k) is the number of sign patterns of length k in the Liouville sequence.

**判定理由**：Sarnak's positive entropy conjecture is cited as motivation; this paper proves only s(k) ≫_A k^A.

**关联卡**：The paper's Theorem 1.11 proves the weaker bound s(k) ≫_A k^A.

### 🔵 `OP-4B4510D590D1` — `background_open` | MSC 11N37 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1, after Corollary 1.6
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> This partially verifies~\cite[Conjecture 1.6]{TaoEq}, which asserted that this estimate (or more precisely, a slightly weaker logarithmically averaged version of this estimate) held whenever $H = H(X)$ went to infinity as $X \to \infty$.

**自包含改写**：Conjecture (Tao): For the Liouville function λ, for all k ≥ 1 and all H = H(X) → ∞ as X → ∞, we have ∫_1^X ||λ||_{U^{k+1}[x,x+H]} / x dx = o(log X). This would imply the logarithmically averaged Chowla and Sarnak conjectures.

**判定理由**：This is Tao's conjecture from a previous paper, cited as a target the present paper partially verifies.

**关联卡**：The paper proves this for H ≥ X^θ (Corollary 1.6).

### 🔵 `OP-92C33B498882` — `background_open` | MSC 11N37 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1.2
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The logarithmically averaged Sarnak conjecture in turn is the statement that
\begin{align*}
\sum_{n\leq x}\frac{\lambda(n)a(n)}{n}=o(\log x)
\end{align*}
for every bounded, deterministic sequence $a \colon \N \to \C$ (in the sense that $a$ has zero topological entropy).

**自包含改写**：The logarithmically averaged Sarnak conjecture: For every bounded deterministic sequence a: ℕ → ℂ with zero topological entropy, ∑_{n≤x} λ(n)a(n)/n = o(log x) as x → ∞.

**判定理由**：Famous open conjecture cited as motivation.

### 🔵 `OP-9504E27870CE` — `background_open` | MSC 11N37 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1.3.2, after Corollary 1.13
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Taking $h$ bounded in Corollary~\ref{cor_chowla} would amount to settling Chowla's conjecture.

**自包含改写**：Chowla's conjecture: For the Liouville function λ, for all k ≥ 1 and all distinct integers a_1,…,a_k ≥ 0, we have E_{n≤X} λ(n+a_1)⋯λ(n+a_k) = o(1) as X → ∞. This would follow from Corollary 1.13 by taking h bounded.

**判定理由**：Chowla's conjecture is a famous open problem; the paper proves an averaged version.

**关联卡**：Corollary 1.13 proves the averaged version E_{h≤X^ε}|E_{n≤X} λ(n+a_1h)⋯λ(n+a_kh)| = o(1).

### 🔵 `OP-9DDBED47A0DE` — `background_open` | MSC 11N37 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1.2
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The logarithmically averaged Chowla conjecture states that
\begin{align*}
\sum_{n\leq x}\frac{\lambda(a_1n+b_1)\cdots \lambda(a_kn+b_k)}{n}=o(\log x)    
\end{align*}
whenever $a_i,b_i$ are natural numbers with $a_ib_j\neq a_jb_i$ for $i\neq j$.

**自包含改写**：The logarithmically averaged Chowla conjecture: For all k ≥ 1, all natural numbers a_i, b_i with a_i b_j ≠ a_j b_i for i ≠ j, we have ∑_{n≤x} λ(a_1 n + b_1)⋯λ(a_k n + b_k)/n = o(log x) as x → ∞.

**判定理由**：Famous open conjecture cited as motivation; not this paper's own target.

### 🟠 `OP-815DB1D9831F` — `method_obstruction` | MSC 11L41 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.2
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Handling the regime $H\in [(\log X)^{\eta}, (\log X)^{\eta^{-1}}]$, at the very least, would likely necessitate an entirely new idea for several reasons.

**自包含改写**：Open problem/obstruction: Extending Theorem 1.6 to H ∈ [(log X)^η, (log X)^{η^{-1}}] requires entirely new ideas. Three specific obstructions are identified: (1) even under GRH, cancellation in short Dirichlet polynomials ∑ χ(p)p^{it} is known only for H ≫ (log X)^{(2+κ)ε^{-1}}; (2) the approximate functional equation method requires the modulus to be much larger than X; (3) the entropy decrement method is restricted to H ≤ (log X)^η.

**判定理由**：The paper explains why current methods fail for this range without formally posing a new problem.

**关联卡**：Related to the gap-bridging problem between H ≥ X^η and H ≤ (log X)^η.

### ⚪ `OP-1967581D72E2` — `future_application` | MSC 11L41 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 5, Remark (rem: loweringH)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It seems plausible that the proof of Theorem~\ref{mult-pret}, combined with the quantitative work in Section~\ref{sec: lowering} for lowering the value of $H$, would allow lowering the length of the intervals to $H\geq \exp((\log X)^{1-\delta})$ for some $\delta>0$. We do not pursue this further here, however, as that would further lengthen this paper.

**自包含改写**：Research direction: combine the nilsequence proof of Theorem 1.6 with the quantitative methods of Section 7 to prove the Gowers norm uniformity result for H ≥ exp((log X)^{1-δ}) for some δ > 0.

**判定理由**：A plausible extension explicitly not pursued; not a formally posed proposition.

**关联卡**：Same as the earlier remark after Theorem 1.8 in Section 1.2.

### ⚪ `OP-24398C281EAB` — `future_application` | MSC 11N37 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 6.2, after Theorem 6.2, remark on generalization to general 1-bounded multiplicative functions
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We leave the details of this generalization to the interested reader.

**自包含改写**：Exercise/direction: generalize Theorem 6.2 (superpolynomial value patterns for multiplicative functions taking values in roots of unity) to any 1-bounded multiplicative function g: ℕ → ℂ with inf_{|t|≤X^{k+1}} D(g^j, χ(n)n^{it}; X) → ∞ as X → ∞ for all j ≥ 1.

**判定理由**：An explicitly stated extension left to the reader with essentially the same proof; not a new open problem.

### ⚪ `OP-BC3892CD59E8` — `future_application` | MSC 11N37 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.3.1
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In this connection, it would be very interesting to say more about the frequency of the superpolynomially many patterns produced by Theorem~\ref{superpolynomial}.

**自包含改写**：Research direction: understand the frequency (density of occurrence) of the superpolynomially many sign patterns of the Liouville function that are guaranteed to exist by Theorem 1.11, rather than just their count.

**判定理由**：A value judgement about what would be interesting; not a precise mathematical proposition.

### ⚪ `OP-DB6473622577` — `future_application` | MSC 11L41 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.2, after Theorem 1.8
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It is conceivable that a careful reworking of the nilsequence part of our arguments in Section~\ref{nilseq} would yield a similar regime $H\geq \exp((\log X)^{1-\delta})$ for Theorem~\ref{mult-pret}; we do not pursue this here, however

**自包含改写**：Research direction: adapt the nilsequence arguments to extend Theorem 1.6 (non-pretentious multiplicative functions are Gowers uniform on short intervals on average) from H ≥ X^θ down to H ≥ exp((log X)^{1-δ}) for some δ > 0.

**判定理由**：This is a plausible extension the authors choose not to pursue; not a formally posed open proposition.

**关联卡**：See also Remark 6.x (rem: loweringH) which makes a similar comment.


# Acta Mathematica

## `2205.09102` — The structure of isoperimetric bubbles on $&amp;#92;mathbb{R}^n$ and $&amp;#92;mathbb{S}^n$
- 权威出处：**Acta Mathematica** 2025，DOI `10.4310/acta.2025.v234.n1.a2`
- 连接方式：`doi`｜全文 399,616 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟢 `OP-17E8808448C9` — `real_open` | MSC 49Q20 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1, Conjecture* (Multi-Bubble Isoperimetric Conjecture on $\R^n$), originating with Sullivan (1990s)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no (only the sub-range $2 \le q \le \min(5,n+1)$)

**原文引文**

> For all $2 \leq q \leq n+2$, a standard bubble uniquely minimizes total perimeter among all $q$-clusters $\Omega$ on $\R^n$ of prescribed volume $V(\Omega) = v \in \interior \Delta^{(q-1)}_{\infty}$.

**自包含改写**：On Euclidean space $\R^n$ ($n \geq 2$) with Lebesgue measure $V$: for every integer $q$ with $2 \leq q \leq n+2$ and every prescribed volume vector $v$ in the interior of $\Delta^{(q-1)}_\infty := \R^{q-1}_+ \times \{\infty\}$ (i.e. arbitrary positive volumes for the $q-1$ bounded cells), the standard $(q-1)$-bubble -- the stereographic projection onto $\R^n$ (from a North pole in the open cell $\Omega_q$) of the $q$-cluster on $\S^n$ obtained by intersecting $\S^n$ with the Voronoi cells of $q$ equidistant points on $\S^n \subset \R^{n+1}$ -- uniquely minimizes the total perimeter $P(\Omega) = \sum_{1 \leq i < j \leq q} V^{n-1}(\Sigma_{ij})$ (sum of the $(n-1)$-dimensional measures of the interfaces $\Sigma_{ij} = \partial^* \Omega_i \cap \partial^* \Omega_j$) among all $q$-clusters (partitions of $\R^n$ into pairwise disjoint locally-finite-perimeter cells with $V(\Omega) = v$). The case $q=2$ is classical and included for completeness. THIS paper proves the conjecture for all $2 \leq q \leq \min(5,n+1)$ (double bubble $n \geq 2$, triple bubble $n \geq 3$, quadruple bubble $n \geq 4$; the double-bubble case and the planar triple-bubble case $q=4$, $n=2$ were previously known, as was the equal-volume triple-bubble case on $\R^3$ announced by Lawlor). Still open after this paper: $6 \leq q \leq n+1$ for $n \geq 5$ (for $q=6$ the authors announce the minimality/inequality part, but not uniqueness, without proof), and the maximal case $q = n+2$ for $n \geq 3$.

**判定理由**：Sullivan's 1990s conjecture adopted as the paper's main target; proved here only for $q \le \min(5,n+1)$, so $6 \le q \le n+1$ and $q=n+2$ remain genuinely unresolved.

**关联卡**：Companion card for the $\S^n$ conjecture. The $q=6$ uniqueness gap on $\R^n$ noted in the quintuple card is precisely the $q=6$ instance of this conjecture.

### 🟢 `OP-7E8C13EB70C5` — `real_open` | MSC 49Q20 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.4 (Further extensions), Theorem 1.6 [Conditional verification assuming pseudo conformal flatness]
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Fix $n \geq 6$ and $7 \leq q \leq n+1$. Assume that for every $v \in \Delta^{(q-1)}_1$, there exists an isoperimetric minimizing $q$-cluster $\Omega$ on $\S^n$ with $V(\Omega) = v$ so that $\Omega$ is pseudo conformally flat. Then the multi-bubble conjecture for $p$-clusters on $\S^n$ holds for all $2 \leq p \leq q$.

**自包含改写**：Open hypothesis left by this paper (verifying it would prove the spherical multi-bubble conjecture for all $2 \leq p \leq q$): for fixed dimension $n \geq 6$ and integer $q$ with $7 \leq q \leq n+1$, is it true that for every volume vector $v \in \Delta^{(q-1)}_1$ (interior of the probability simplex in $\R^q$) there exists an isoperimetric minimizing $q$-cluster $\Omega$ on $\S^n$ with $V(\Omega) = v$ that is pseudo conformally flat? Here, for a spherical Voronoi cluster with quasi-center parameters $\{\mathbf{c}_i\}_{i=1}^q \subset \R^{n+1}$ and curvature parameters $\{\mathbf{k}_i\}_{i=1}^q \subset \R$ (normalized by $\sum_i \mathbf{c}_i = 0$, $\sum_i \mathbf{k}_i = 0$, with cells $\Omega_i = \{ p \in \S^n \, ; \, \arg\min_j \langle \mathbf{c}_j, p \rangle + \mathbf{k}_j = \{i\} \}$), pseudo conformally flat means there exists $\xi \in \R^{n+1}$ with $\langle \mathbf{c}_i, \xi \rangle + \mathbf{k}_i = 0$ for all $i = 1, \ldots, q$, i.e. the closed polyhedra defining the cells share a common point. Note: the conditional theorem itself is also stated without proof in this paper (proof deferred to a separate work), and the authors were not able to establish the hypothesis in full generality.

**判定理由**：The paper explicitly leaves its hypothesis -- existence of a pseudo conformally flat minimizer for every prescribed volume -- unverified; a decidable statement that would settle the $\S^n$ conjecture.

**⚠️ 人工复核标记**：Both the hypothesis and the conditional implication are stated without proof here; both await the companion publication.

**关联卡**：Conditional route to the Multi-Bubble Conjecture on $\S^n$ card for $7 \le q \le n+1$; the obstruction context is in the PDI/MPDI method-obstruction card.

### 🟢 `OP-E2BA5EB32E6D` — `real_open` | MSC 49Q20 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1, Conjecture* (Multi-Bubble Isoperimetric Conjecture on $\S^n$), originating with Sullivan (1990s)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no (only the sub-range $2 \le q \le \min(5,n+1)$)

**原文引文**

> For all $2 \leq q \leq n+2$, a standard bubble uniquely minimizes total perimeter among all $q$-clusters $\Omega$ on $\S^n$ of prescribed volume $V(\Omega) = v \in \interior \Delta^{(q-1)}_{1}$.

**自包含改写**：On the unit sphere $\S^n$ ($n \geq 2$), canonically embedded in $\R^{n+1}$, endowed with normalized Haar measure $V$ (total mass $1$): for every integer $q$ with $2 \leq q \leq n+2$ and every $v$ in the interior of the probability simplex $\Delta^{(q-1)}_1 = \{ v \in \R^q_+ \, ; \, \sum_{i=1}^q v_i = 1 \}$, a standard $(q-1)$-bubble -- a stereographic projection onto $\S^n$ of a standard bubble on $\R^n$, equivalently any Möbius image of the equal-volume bubble obtained by intersecting $\S^n$ with the Voronoi cells of $q$ equidistant points on $\S^n \subset \R^{n+1}$ -- uniquely minimizes the total perimeter $P(\Omega) = \sum_{1 \leq i < j \leq q} V^{n-1}(\Sigma_{ij})$ among all $q$-clusters $\Omega$ on $\S^n$ with $V(\Omega) = v$. The case $q=2$ is classical. THIS paper proves the conjecture for all $2 \leq q \leq \min(5,n+1)$; this includes the previously open double-bubble case on $\S^n$ for $n \geq 3$ (before, only almost-equal-volume cases such as $\max_i |v_i - 1/3| \leq 0.04$ were known). The equal-volume case $v_i = 1/q$ was previously known for all $2 \leq q \leq n+2$ via the Gaussian multi-bubble theorem, and the double/triple-bubble cases on $\S^2$ ($n=2$) were previously known. The authors additionally state without proof (deferred to a companion work) that the quintuple case $q=6$ holds on $\S^n$ for all $n \geq 5$. Remaining open after this paper: $7 \leq q \leq n+1$ (and $q = 6$ pending the unproven announcement) and the maximal case $q = n+2$ for $n \geq 3$ (e.g. the quadruple bubble $q=5$ on $\S^3$).

**判定理由**：The paper's central target on $\S^n$; proved only for $q \le \min(5,n+1)$ (with $q=6$ merely announced), leaving $q \geq 6$ up to $n+1$ and $q = n+2$ unresolved.

**关联卡**：Companion card for the $\R^n$ conjecture; the announced quintuple and conditional pseudo-conformal-flatness cards are partial routes to this conjecture.

### 🔵 `OP-461B533E3126` — `background_open` | MSC 49Q20 | 难度 hard

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1.3, Remark after Theorem 1.4
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> An interesting question of Almgren \cite[Problem 1]{OpenProblemsInSoapBubbles96} is whether there is a stable cluster $\Omega$ of bubbles in $\R^3$ with some bubble $\Omega_i$ being topologically a torus.

**自包含改写**：Almgren's question (Problem 1 in the 1996 soap-bubble open-problems list): does there exist a stable cluster $\Omega$ of bubbles in $\R^3$ -- i.e. a cluster that is stationary for the first variation and stable, meaning the second-variation index-form satisfies $Q(X) \geq 0$ for all smooth compactly supported vector-fields $X$ with vanishing first variation of the cells' volumes -- such that some bubble (cell) $\Omega_i$ is topologically a torus? The paper does not resolve this; it records partial constraints: for stable $q$-clusters in $\R^n$ with $\S^0$-symmetry and $4 \leq q \leq n+1$, Theorem 1.4 implies the cells are connected and are stereographic projections of $P_i \cap \S^n$ for convex $\S^0$-symmetric polyhedra $P_i$ with at most $q-1$ facets, limiting the cells' topological complexity.

**判定理由**：Pre-existing open question of Almgren cited as background in a remark; the paper neither adopts it as a target nor resolves it, only noting partial structural constraints.

**关联卡**：Contrasts with the solved Heppes connectedness card: stability without minimality is much less rigid.

### 🟠 `OP-01F61B4C7701` — `method_obstruction` | MSC 49Q20 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.5, closing technical discussion (referring to Sections on bounded curvature and non-physical fields)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Consequently, we do not know how to rigorously approximate a non-physical scalar-field by a physical vector-field as above in general, but are able to do so in two cases -- in an averaged sense, so that the contribution to $Q$ of the boundary integral at the triple-points vanishes; and without averaging, but only after establishing that the cluster has locally bounded curvature.

**自包含改写**：Method limitation, not a posed open problem: for a stationary regular $q$-cluster $\Omega$, a scalar-field $f = \{f_{ij}\}$ on the interfaces (oriented, $f_{ji} = -f_{ij}$, satisfying the Dirichlet--Kirchhoff condition $f_{ij} + f_{jk} + f_{ki} = 0$ at triple points) is called physical if $f_{ij} = X^{\mathbf{n}_{ij}}$ on $\Sigma_{ij}$ for a single global smooth compactly supported vector-field $X$ ($\mathbf{n}_{ij}$ the unit normal from $\Omega_i$ to $\Omega_j$). Because of $C^{1,\alpha}$-only regularity at quadruple points, possible curvature blow-up near the quadruple set $\Sigma^3$, the singular set $\Sigma^4$, and non-simplicial minimal cones in dimensions $\geq 4$ (which permit linear dependencies among interface normals when $\geq 6$ cells meet), the authors do not know how to approximate a general non-physical Lipschitz scalar-field by physical vector-fields while controlling the index-form $Q$ and the volume variations; they succeed only (i) in an averaged (traced) sense, eliminating the boundary contribution to $Q$ at triple points, and (ii) without averaging, once the cluster has locally bounded curvature.

**判定理由**：General approximation of non-physical scalar-fields by physical vector-fields is beyond the authors' methods; achieved only in two special cases. A hypothesis/limitation, not a posed problem.

**关联卡**：The locally-bounded-curvature approximation result is the tool whose future usefulness is flagged in the future_application card.

### 🟠 `OP-5124225637FA` — `method_obstruction` | MSC 49Q20 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.5 (Method of proof and comparison with previous approaches)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Contrary to the Gaussian setting, $Q(W_\theta)$ does not have a clear sign, and in fact we suspect that it is not always negative semi-definite on a general cluster (even though, a-posteriori, we can show that $Q(W_\theta) \leq 0$ for a stable $q$-cluster when $q \leq n+1$). For this reason, contrary to the Gaussian setting, we are not able to handle the case when $q$ is maximal according to the conjectures, i.e. $q= n+2$, and restrict our analysis to $q \leq n+1$.

**自包含改写**：Method limitation, not a posed open problem: on $\R^n$ and $\S^n$ (unlike Gaussian space), the stability index-form $Q(X) := \delta^2_X A - \langle \lambda, \delta^2_X V \rangle$ (second variation of total perimeter minus Lagrange-multiplier pairing with second variation of volume) evaluated on the $(n+1)$-dimensional family of Möbius vector-fields $\{W_\theta\}$ (the conformal Killing fields generating the Möbius group modulo isometries) has no a-priori sign on a general cluster; the authors suspect $Q(W_\theta)$ is not always negative semi-definite on a general cluster, although a-posteriori $Q(W_\theta) \leq 0$ holds for stable $q$-clusters when $q \leq n+1$. Without this sign, the method cannot handle the maximal case $q = n+2$ of the multi-bubble conjectures, and the analysis is restricted to $q \leq n+1$.

**判定理由**：Explains why the Gaussian-style argument fails and why the needed hypothesis ($Q(W_\theta) \leq 0$ in general) is unavailable; no formal open problem is posed.

**关联卡**：Explains the $q = n+2$ gap in both Multi-Bubble Conjecture cards.

### 🟠 `OP-59A04F7E60D2` — `method_obstruction` | MSC 49Q20 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.5, item (3) of the proof outline for Theorem 1.2 (double/triple/quadruple bubble theorem)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> the number of the possible adjacency graphs grows super-exponentially with $q$, and furthermore, the classification of minimizing cones is only available in dimensions $2$ and $3$ thanks to Taylor's work \cite{Taylor-SoapBubbleRegularityInR3}, and so we can only determine if a meeting point of several bubbles is illegal when it involves at most $5$ cells. This explains why we cannot at present extend Theorem \ref{thm:intro-234} to handle arbitrary $q \leq n+1$.

**自包含改写**：Method limitation, not a posed open problem: the final, global step of the proof excludes spherical Voronoi clusters with missing interfaces by enumerating cell-adjacency graphs and testing singular meeting points against the classification of area-minimizing cones. Since Taylor's classification of minimizing cones is available only in dimensions $2$ and $3$ (non-simplicial minimizing cones exist in dimensions $4$ and higher), a meeting point of several bubbles can be certified illegal only when it involves at most $5$ cells; moreover the number of possible $2$-connected adjacency graphs on $q$ vertices grows super-exponentially with $q$. Consequently the paper cannot at present extend Theorem 1.2 (the multi-bubble conjectures for $2 \leq q \leq \min(5,n+1)$) to arbitrary $q \leq n+1$. A classification of area-minimizing cones in dimensions $\geq 4$ (a known open problem, not posed here) would remove part of the obstruction.

**判定理由**：Explains the barrier (unclassified minimizing cones in dimensions $\geq 4$, graph explosion) to extending the main theorem to $q \geq 6$; limitation stated, not a posed problem.

**关联卡**：Explains why the Multi-Bubble Conjecture cards are resolved only up to $q = 5$ within the range $q \leq n+1$.

### 🟠 `OP-5CEC84428089` — `method_obstruction` | MSC 49Q20 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.5 (Method of proof and comparison with previous approaches)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Lastly, we don't know how to derive a reasonable PDE for the model profile on $\R^n$ (even after modding out homogeneity to reduce to a compact set); and while it is possible to derive a corresponding PDE for the model profile on $\S^n$, we were not able to establish a sharp PDI for the actual isoperimetric profile on $\S^n$ in full generality (only conditionally, yielding Theorem \ref{thm:intro-conditional}, whose proof will be presented in a separate work). Consequently, \textbf{we do not invoke any MPDI argument in this work}.

**自包含改写**：Method limitation, not a posed open problem: the authors' earlier Gaussian multi-bubble proof relied on a sharp matrix-valued partial differential inequality (MPDI) satisfied by the Gaussian isoperimetric profile. In the present $\R^n$/$\S^n$ setting, the authors do not know how to derive a reasonable PDE for the model profile (the isoperimetric profile of the conjectured standard-bubble minimizer) on $\R^n$, even after modding out homogeneity to reduce to a compact set; on $\S^n$ such a PDE for the model profile is derivable, but a sharp PDI for the actual isoperimetric profile on $\S^n$ could not be established in full generality (only conditionally, yielding the pseudo-conformal-flatness theorem, itself stated without proof). Hence no MPDI argument is invoked in this paper.

**判定理由**：States that a needed estimate (sharp PDI for the isoperimetric profile on $\R^n$/$\S^n$) is out of the authors' reach; a method failure, not a formally posed problem.

**关联卡**：Provides the obstruction context for the conditional pseudo-conformal-flatness card.

### 🔴 `OP-6FA9A5859154` — `solved_in_paper` | MSC 49Q20 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1.3 (Main results), paragraph preceding Theorem 1.4; 'the latter range' is $q \leq n+1$
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes (for $q \le n+1$)

**原文引文**

> This resolves a conjecture of A.~Heppes \cite[Problem 5]{OpenProblemsInSoapBubbles96} and the open question of whether there can be empty chambers trapped by minimizing bubbles \cite[Chapter 13]{MorganBook5Ed} in the latter range.

**自包含改写**：Heppes' conjecture (Problem 5 in the 1996 soap-bubble open-problems list): each cell of an isoperimetric minimizing cluster in $\R^n$ (a partition of $\R^n$ into $q$ locally-finite-perimeter cells minimizing total perimeter at prescribed volumes) is necessarily connected; in particular the unbounded exterior cell $\Omega_q$ is connected, i.e. no empty chambers are trapped by the bubbles (this latter was a separate open question recorded in Morgan's book). The paper resolves both questions in the range $q \leq n+1$ and extends them to $\S^n$: Theorem 1.4 proves that for $M^n \in \{\R^n, \S^n\}$, any isoperimetric minimizing $q$-cluster with $q \leq n+1$ is $\S^0$-symmetric, perpendicularly spherical Voronoi, and all of its open cells (including the unbounded one when $M^n = \R^n$, if non-empty) are equatorial and connected. The case $q = n+2$ (e.g. the quadruple bubble $q=5$ on $\R^3$ or $\S^3$) is not covered by the paper's theorem.

**判定理由**：The paper proves connectedness of all cells, including the unbounded one, for minimizers on $\R^n$ and $\S^n$ in the crucial range $q \le n+1$, resolving Heppes' conjecture and the empty-chamber question there.

**关联卡**：The empty-chamber question (connectedness of the unbounded cell) is the special case of Heppes' question for $\Omega_q$; both are resolved simultaneously by Theorem 1.4, so a single card is emitted. The range $q = n+2$ remains outside the theorem.

**存疑**：Heppes' original formulation is known here only as reported by this paper; if it imposed no restriction on $q$, the paper's resolution covers $q \le n+1$ only.

### ⚪ `OP-02C5FBE2453E` — `future_application` | MSC 49Q20 | 难度 easy

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.5, item (1) of the proof outline, followed by the displayed identity
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no (the identity is proved in the paper; this card records only the interest remark)

**原文引文**

> In the case of $\R^n$, we also need to employ the following remarkable isotropicity of a minimizing cluster's boundary $\Sigma^1 = \bigcup_{i<j} \Sigma_{ij}$ (regardless of the volumes of the cells or their number!), which may be of independent interest (see Remark \ref{rem:isotropic}):

**自包含改写**：Not a mathematical proposition: an interest flag on the identity $\int_{\Sigma^1} \mathbf{n} \otimes \mathbf{n} \, dp = \frac{1}{n} \int_{\Sigma^1} \mathrm{Id} \, dp$, where $\Sigma^1 = \bigcup_{i<j} \Sigma_{ij}$ is the union of interfaces of an isoperimetric minimizing cluster in $\R^n$ and $\mathbf{n}$ the outward unit normal; the identity holds regardless of the cells' volumes or their number. The identity itself is asserted/proved in the paper (body sections); the 'may be of independent interest' clause is a taste remark about possible applications, not a research task.

**判定理由**：Value judgement ('may be of independent interest') attached to a proven identity; explicitly not a proposition, per no-taskification rule.

**存疑**：The identity's proof (Remark on isotropicity) lies in the middle portion of the source not included in the provided excerpt; the identity is stated as established in the introduction.

### 🟡 `OP-55EC4EBC2677` — `uncertain` | MSC 49Q20 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.4 (Further extensions), theorem stated without proof, and the remark following it
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> With some additional (considerable) work, which we leave for another occasion, we can also obtain the following results, which we only state here without proof: [...] The quintuple bubble conjecture (case $q=6$) holds on $\S^n$ for all $n \geq 5$.

**自包含改写**：Claimed by the authors but NOT proved in this paper (proof deferred to a companion work): the multi-bubble isoperimetric conjecture in the quintuple-bubble case $q = 6$ (six cells) holds on $\S^n$ for all $n \geq 5$, i.e. for every $v$ in the interior of the probability simplex $\Delta^{(5)}_1$, the standard quintuple bubble on $\S^n$ uniquely minimizes total perimeter among all $6$-clusters of prescribed volume $v$. The accompanying remark derives from this (via scale-invariance and approximation of small clusters in $\R^n$ by clusters in $\S^n$) that a standard quintuple bubble in $\R^n$, $n \geq 5$, is an isoperimetric minimizer (the quintuple-bubble inequality on $\R^n$), but uniqueness is lost in the approximation, so the authors 'cannot exclude the existence of additional quintuple-bubble minimizers on $\R^n$'.

**判定理由**：Proposition asserted true but explicitly 'stated here without proof'; its resolution cannot be verified from this source alone.

**⚠️ 人工复核标记**：Announced result without proof in this paper; verify against the companion publication before marking the $q=6$ spherical case resolved.

**关联卡**：Instance $q=6$ of the Multi-Bubble Conjecture on $\S^n$ card; the companion $\R^n$ uniqueness gap for $q=6$ is part of the open $\R^n$ conjecture card.

**存疑**：Proof 'will be presented in a separate work' per the authors; whether the quintuple case counts as resolved must be confirmed from that companion work.

### ⚪ `OP-E326DAD0CA05` — `future_application` | MSC 49Q20 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 3 (Non-physical scalar-fields vs. physical vector-fields), introductory bullet list
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no (underlying approximation theorem is proved; this card records only the outlook remark)

**原文引文**

> On a stationary regular cluster with \emph{locally bounded curvature}, we obtain a very useful general approximation result in Subsection \ref{subsec:scalar-fields-bounded-curvature}, which should also prove useful for subsequent investigations.

**自包含改写**：Not a mathematical proposition: an outlook statement that the paper's approximation theorem on clusters of locally bounded curvature -- for every Delta-Lipschitz scalar-field $f$ and $\epsilon > 0$ there exists a smooth compactly supported vector-field $Y_\epsilon$ with matching first variation of volume and $Q^1(Y_\epsilon) \leq Q^0(f) + \epsilon$ -- should prove useful for subsequent investigations. The underlying approximation result is proved in the paper; only the usefulness claim is an outlook.

**判定理由**：Taste/outlook comment on the future usefulness of a proven tool; explicitly not a proposition, hence not turned into a research task.

**关联卡**：Relates to the non-physical-fields method-obstruction card: this is the bounded-curvature case where the obstruction is overcome.


## `2202.08861` — Bounded $t$-structures on the category of perfect complexes
- 权威出处：**Acta Mathematica** 2024，DOI `10.4310/acta.2024.v233.n2.a2`
- 连接方式：`title-fuzzy(0.978)`｜全文 127,111 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟢 `OP-955DFB21506C` — `real_open` | MSC 14F08 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：End of Section 5 ('Bounded t-structures on D^b_coh(X), without dualizing complexes'), immediately after Remark R997.3333098
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Presumably the equivalence of the bounded \tstr s on $\dcohs Z(X)$ holds in a generality greater than we can prove now.

**自包含改写**：Let X be a finite-dimensional noetherian scheme and Z ⊂ X a closed subset; let D^b_{coh,Z}(X) denote the bounded derived category of coherent sheaves on X with cohomology supported on Z (this category has at least one bounded t-structure for every X, namely the standard one). Two t-structures (T_1^{≤0},T_1^{≥0}) and (T_2^{≤0},T_2^{≥0}) on a triangulated category are called equivalent if there exists an integer n>0 with T_1^{≤−n} ⊂ T_2^{≤0} ⊂ T_1^{≤n}. Conjecture posed by this paper: all bounded t-structures on D^b_{coh,Z}(X) are mutually equivalent under hypotheses strictly weaker (more general) than the three sufficient conditions proved in the paper, namely (i) Z contained in the regular locus of X, (ii) X admits a dualizing complex, (iii) X is separated and quasiexcellent and Z = X; plausibly for all finite-dimensional noetherian X and all closed Z ⊂ X.

**判定理由**：A genuine conjecture left open by this paper ('Presumably...'), beyond the special cases (i)-(iii) it proves.

**关联卡**：Same problem as the introduction's formulations: 'It is therefore natural to ask what is true about D^b_{coh,Z(X)---which has at least one bounded t-structure for every X' and 'It seems eminently plausible that the results about D^b_{coh,Z}(X) are not best possible. They are all we can prove at the moment.' The solved cases (i)-(iii) are recorded in a separate solved_in_paper card.

**存疑**：The source formulates the conjecture vaguely as holding 'in a generality greater than we can prove now' without specifying the target generality; the maximal reading (all finite-dimensional noetherian X, all closed Z) is an interpretation, and the safe statement is: equivalence holds under hypotheses strictly weaker than (i)-(iii).

### 🟠 `OP-45C68C500782` — `method_obstruction` | MSC 14F08 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Remark R27.2, Section 6 (S27, 'The standard t-structure is in the preferred equivalence class')
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Theorem~\ref{T27.1}(i) fails in general; the compact objects are always perfect, but for general enough algebraic stacks the converse is false.

**自包含改写**：Theorem 27.1(i) asserts: for X a quasicompact, quasiseparated scheme and Z ⊂ X a closed subset with quasicompact complement, the compact objects of D_{qc,Z}(X) (complexes of O_X-modules with quasicoherent cohomology, acyclic on X−Z) are precisely the perfect complexes on X whose cohomology is supported on Z. The paper notes this identification fails for general algebraic stacks: compact objects are always perfect, but for general enough algebraic stacks there exist perfect complexes that are not compact (by results of Hall-Rydh); the same remark also notes that for stacks with infinite stabilizers there is rarely a single compact generator of D_{qc,Z}(X). Hence the scheme hypothesis is necessary and the results do not extend verbatim to stacks.

**判定理由**：Documents that the scheme hypothesis is needed: Theorem 27.1(i) fails for general algebraic stacks (prior knowledge of Hall-Rydh); scope limitation, not a posed problem.

**存疑**：The failure for stacks was known prior to this paper (Hall-Rydh 2013/2015, cited in Remark R27.2); the card records the scope limitation of Theorem 27.1 rather than an open problem of this paper, which is why paper_time_status is given as not_a_proposition.

### 🟠 `OP-49185207684D` — `method_obstruction` | MSC 14F08 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Remark R400.3, Section 8 (S400)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> By contrast the known proof, that $\Dqc(X)$ is approximable for separated $X$, is by reduction to the case where $X$ is projective. Reducing to the projective case is technically more involved, and forces on us the assumption that $X$ is separated.

**自包含改写**：Methodological note, not a proposition: the known proof that the derived category D_{qc}(X) of complexes of O_X-modules with quasicoherent cohomology is approximable, for separated X, proceeds by reduction to the case where X is projective; this reduction technique is technically more involved and is what currently forces the separatedness hypothesis on X. By contrast, the paper's weak approximability of D_{qc,Z}(X) (Theorem 27.1(iv), for X quasicompact quasiseparated and Z ⊂ X closed with quasicompact complement) is proved by reduction to the affine case, avoiding separatedness. No formal open problem is posed.

**判定理由**：Identifies a hypothesis (separatedness) forced by the current proof method for approximability of D_{qc}(X), without posing an open problem.

**关联卡**：Related to the non-approximability observation (Remark R400.1) and to the approximability of D_{qc}(X) for separated X cited from [Neeman17A, Section 3].

### 🟠 `OP-A647AF11D2DF` — `method_obstruction` | MSC 14F08 | 难度 medium

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Remark R400.1, Section 8 (S400, 'More about approximable and weakly approximable triangulated categories')
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Thus we cannot usually find an integer $n$ such that, for every $F\in\Dqcs Z(X)^{\leq0}$, there exists a triangle $E\la F\la D$ with $E\in\Coprod_n^{}\big(B[-n,n]\big)$ and with $D\in\Dqcs Z(X)^{\leq-1}$.

**自包含改写**：Let X = Spec R be affine, Z ⊂ X a closed subset whose quasicompact complement is covered by D(f_i), i = 1..r, with f_1,...,f_r ∈ R; let I = (f_1,...,f_r) be the ideal they generate, and let B = ⊗_{i=1}^r (R →^{f_i} R) (degrees −r..0) be the Koszul-type compact generator of D_{qc,Z}(X); let Coprod_1(B(-∞,∞)) = Add(B(-∞,∞)) and Coprod_{n+1}(B(-∞,∞)) = Coprod_1(B(-∞,∞)) ⋆ Coprod_n(B(-∞,∞)) (extension-closed iterates). The paper proves: I^n annihilates every object of Coprod_n(B(-∞,∞)); hence any triangle E → F → D with E ∈ Coprod_n(B[-n,n]), F ∈ D(R)^{≤0}, D ∈ D(R)^{≤−1} forces I^n H^0(F) = 0, which fails for F = R/I^{n+1} unless I^n = I^{n+1}. Consequently D_{qc,Z}(X) is not approximable in general (Theorem 27.1(iv) yields only weak approximability): in general there is no integer n such that every F ∈ D_{qc,Z}(X)^{≤0} admits a triangle E → F → D with E ∈ Coprod_n(B[-n,n]) and D ∈ D_{qc,Z}(X)^{≤−1}; approximability can only be expected for special Z ⊂ X (e.g. I = 0, i.e. Z = X).

**判定理由**：The paper proves a negative/obstruction result: the approximability condition fails in general; no formal open problem is posed.

**关联卡**：Contrasts with Theorem 27.1(iv) (weak approximability of D_{qc,Z}(X), proved in the paper) and with the known fact that D_{qc}(X) is approximable when Z = X and X is separated [Neeman17A, Section 3]; the induction I^n·Coprod_n(B(-∞,∞)) = 0 was re-derived and checks out.

### 🔴 `OP-54913D9D15E0` — `solved_in_paper` | MSC 14F08 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Remark R997.3333098 (summary at end of Section 5), under the standing hypotheses of Remark R997.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> The bounded \tstr s on the category $\dcohs Z(X)$ are all equivalent if any of the following holds: \be \item $Z$ is contained in the regular locus of $X$. \item $X$ admits a dualizing complex. \item $X$ is separated and quasiexcellent, and the inclusion $Z\subset X$ is an equality. \ee

**自包含改写**：Let X be a finite-dimensional noetherian scheme and Z ⊂ X a closed subset; D^b_{coh,Z}(X) = bounded derived category of coherent sheaves on X with cohomology supported on Z; two t-structures (T_1^{≤0},T_1^{≥0}), (T_2^{≤0},T_2^{≥0}) are equivalent iff there exists an integer n>0 with T_1^{≤−n} ⊂ T_2^{≤0} ⊂ T_1^{≤n}. Theorem (proved in this paper): all bounded t-structures on D^b_{coh,Z}(X) are equivalent if any of the following holds: (i) Z is contained in the regular locus of X; (ii) X admits a dualizing complex; (iii) X is separated and quasiexcellent and the inclusion Z ⊂ X is an equality (i.e. Z = X). Case (ii) is Theorem 31.3 combined with Remark 31.999; case (iii) is Theorem 3.3 combined with Remark 31.999; case (i) follows since then D^perf_Z(X) = D^b_{coh,Z}(X) and Lemma 1.3 makes all bounded t-structures equivalent.

**判定理由**：Summary proposition proved by the paper itself (Theorems 31.3 and 3.3 with Remark 31.999); it is the solved portion of the broader equivalence conjecture.

**⚠️ 人工复核标记**：For case (i) the source cites 'the discussion preceeding (\ref{ST897.3.1})', but the label ST897.3.1 is undefined in the provided source (dangling reference, likely left over from an earlier draft). The standing hypotheses (X finite-dimensional noetherian, Z closed) come from the preceding Remark R997.3 and must be carried along.

**关联卡**：These are the solved special cases of the 'Presumably...' conjecture card; the paper also notes case (i) follows from case (ii) for J-1 schemes.

### 🔴 `OP-E574C99E55A8` — `solved_in_paper` | MSC 14F08 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction (Section 0), discussing [Antieau-Gepner-Heller19, Conjecture 1.5]
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> it predicted that, if $X$ is a finite-dimensional, noetherian scheme, then the category $\dperf X$ has a bounded \tstr\ if and only if $X$ is regular. In this article we prove a major generalization.

**自包含改写**：Conjecture (Antieau-Gepner-Heller 2019): if X is a finite-dimensional, noetherian scheme, then the derived category D^perf(X) of perfect complexes on X has a bounded t-structure if and only if X is regular. (A t-structure (T^{≤0},T^{≥0}) on a triangulated category T with suspension Σ is bounded if for every object X of T there exists an integer n>0 with Σ^n X ∈ T^{≤0} and Σ^{-n} X ∈ T^{≥0}.) This paper proves a strict generalization (Theorem 0.1): for X a noetherian, finite-dimensional scheme and Z ⊂ X a closed subset, letting D^perf_Z(X) be the category of perfect complexes on X whose cohomology is supported on Z, the category D^perf_Z(X) has a bounded t-structure if and only if Z is contained in the regular locus of X. The conjecture is the special case Z = X.

**判定理由**：The AGH conjecture was open; this paper proves Theorem 0.1, a strict generalization (case Z=X), thereby settling the conjecture.

**关联卡**：Theorem 0.1 is proved via Lemma 1.3 together with Theorems 27.1 and 29.1; see also the card on finding obstructions beyond negative K-theory (Remark 0.3).

### ⚪ `OP-8D67083D3350` — `future_application` | MSC 18G80 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Concluding sentence, Section 8 (S400)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Needless to say: it remains to explore the wider implications of the results developed here, to other approximable or nearly-approximable triangulated categories.

**自包含改写**：Research outlook, not a proposition: the author states that the wider implications of the paper's results (compact generation by a single perfect complex, the standard t-structure lying in the preferred equivalence class, and weak approximability of D_{qc,Z}(X) for X quasicompact quasiseparated and Z ⊂ X closed with quasicompact complement) for other approximable or nearly-approximable triangulated categories remain to be explored.

**判定理由**：Explicitly an outlook ('it remains to explore'), not a decidable mathematical statement.

**关联卡**：Same Remark R400.3 also states: 'The theory of approximable triangulated categories should be viewed as work-in-progress, with extensions and modifications encouraged. The theory should evolve to apply more widely, with this article being a manifestation.'

### ⚪ `OP-9687F464127B` — `future_application` | MSC 14F08 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Remark R400.3, Section 8 (S400); cf. also the Acknowledgements
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> And Section~\ref{S28} was prompted by an application unrelated to anything in the current article: the weak approximability of $\Dqcs Z(X)$ turns out to be relevant to a question studied by Canonaco and Stellari.

**自包含改写**：Application outlook, not a proposition: the weak approximability of D_{qc,Z}(X) (Theorem 27.1(iv), for X a quasicompact quasiseparated scheme and Z ⊂ X a closed subset with quasicompact complement) is stated to be relevant to a question studied by Canonaco and Stellari, to be addressed in a separate article of the author. The question itself is not stated in this paper, so no self-contained mathematical proposition can be extracted from it.

**判定理由**：Pure application outlook; the underlying Canonaco-Stellari question is not stated, so no mathematical proposition is extractable.

**关联卡**：The Acknowledgements state: '...this refinement, of an earlier incarnation of Theorem 27.1, is useful in addressing a question that Canonaco and Stellari asked. This will appear as a separate article.'

**存疑**：The content of the Canonaco-Stellari question is not given in the provided source.

### ⚪ `OP-CAD382D76A2E` — `future_application` | MSC 14F08 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, Remark 0.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Thus negative \kth\ most definitely isn't the only obstruction to the existence of bounded \tstr s, and it becomes interesting to figure out what other obstructions there are, in a generality that goes beyond $\dperfs ZX$. This should be studied.

**自包含改写**：Research outlook, not a mathematical proposition: the paper observes that negative K-theory (the obstruction of Antieau-Gepner-Heller to the existence of bounded t-structures on the category D^perf_Z(X) of perfect complexes with cohomology supported on a closed subset Z of a noetherian finite-dimensional scheme X) is not the only obstruction to the existence of bounded t-structures, and calls for identifying what other obstructions exist, in a generality going beyond the categories D^perf_Z(X). No specific decidable conjecture is formulated.

**判定理由**：'This should be studied' is an exhortation/value judgement; no decidable proposition is formulated; kept as outlook, not taskified.

**关联卡**：Motivated in Remark 0.3 by the fact that many singular schemes (e.g. all singular zero-dimensional schemes) have vanishing negative K-theory, so the K-theoretic obstruction vanishes while Theorem 0.1 still forbids bounded t-structures.


## `1904.03585` — Lie, associative and commutative quasi-isomorphism
- 权威出处：**Acta Mathematica** 2024，DOI `10.4310/acta.2024.v233.n2.a1`
- 连接方式：`doi`｜全文 128,643 字符 via `cache-latex`｜提取模式 `fast`

### 🟢 `OP-10C71EDA0154` — `real_open` | MSC 18M70 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Remark on general Koszul duality, Section 4 (sect:thmb)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> One stumbling block is that one would need an analogue of the deformation complex, which would be a dg Lie algebra whose Maurer--Cartan elements are conilpotent (or locally finite) $\infty$-coalgebra structures and whose gauges are locally finite $\infty$-isotopies which are moreover weak equivalences. It is far from clear {to us} that such an object even exists, given the indirect manner in which weak equivalences are defined.

**自包含改写**：Open existence question: does there exist a dg Lie algebra whose Maurer--Cartan elements are conilpotent (or locally finite) ∞-coalgebra structures on a chain complex, and whose gauge equivalences are locally finite ∞-isotopies that are moreover weak equivalences (weak equivalence of coalgebras being defined indirectly via the cobar functor)? The authors state it is far from clear to them that such an object exists.

**判定理由**：A genuine, decidable mathematical existence question explicitly raised; not resolved in the paper.

**关联卡**：Obstruction to extending the paper's method to the problem of whether U reflects quasi-isomorphisms.

### 🟢 `OP-1E44B9004B87` — `real_open` | MSC 18M70 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 4 (sect:thmb), §'failure of rectification'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> if two cocommutative coalgebras are quasi-isomorphic as $\Coo$-coalgebras, then there is no reason for them to also be quasi-isomorphic as cocommutative coalgebras.\footnote{We do not actually have an example where property (3) fails, so the statement should be interpreted merely as saying that the usual proof of property (3) for $\infty$-algebras breaks down for $\infty$-coalgebras.}

**自包含改写**：Open question: if two conilpotent cocommutative dg coalgebras are quasi-isomorphic as C-infinity-coalgebras (in the sense of the paper: ∞-morphisms of coalgebras over the Koszul resolution of the Com operad), must they be quasi-isomorphic as (strict) cocommutative dg coalgebras? The authors have no counterexample and no proof; the standard rectification argument for ∞-algebras breaks down.

**判定理由**：Explicitly flagged as unknown whether property holds or fails; no example either way.

**关联卡**：Same issue underlies the inability to prove C(g) and C(h) quasi-isomorphic as cocommutative coalgebras in the proof of Theorem B.

### 🟢 `OP-B1580ECFF619` — `real_open` | MSC 18M70 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Remark on general Koszul duality, Section 4 (sect:thmb), item (ii)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The problem whether the universal enveloping algebra functor reflects quasi-isomorphisms is equivalent to the problem whether the forgetful functor from cocommutative conilpotent dg coalgebras to coassociative conilpotent dg coalgebras reflects weak equivalences.

**自包含改写**：Open problem (stated as a problem): does the universal enveloping algebra functor from dg Lie algebras over a field of characteristic zero to associative dg algebras reflect quasi-isomorphisms (i.e. if U(g) -> U(h) is a quasi-isomorphism, is g -> h a quasi-isomorphism)? The paper notes this is equivalent, via Koszul duality, to asking whether the forgetful functor from conilpotent cocommutative dg coalgebras to conilpotent coassociative dg coalgebras reflects weak equivalences (weak equivalence = morphism whose image under the cobar functor is a quasi-isomorphism).

**判定理由**：Explicitly posed as a problem; only the Koszul-dual of Theorem A (for coalgebras) is settled, not this reflection statement.

**关联卡**：The paper also notes a stumbling block for adapting its proof: existence of a deformation complex for locally finite ∞-coalgebra structures (see next card).

### 🟢 `OP-C77F00CF6F63` — `real_open` | MSC 17B55 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, §0.4
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Unfortunately we are not able to prove this statement (and it is not clear if one should expect it to be true), since Koszul duality is not an equivalence

**自包含改写**：Conjectural statement (left open by the paper): if two dg Lie algebras g and h over a field of characteristic zero have universal enveloping algebras U(g) and U(h) that are quasi-isomorphic as associative dg algebras, then g and h are themselves quasi-isomorphic as dg Lie algebras — i.e. Theorem B without any homotopy-completeness hypothesis. The authors cannot prove it and are unsure whether it is expected to be true.

**判定理由**：The paper explicitly states it as an unproved statement it would like; it proves only the homotopy-complete version.

**关联卡**：The paper proves the weakened version (Theorem B) with homotopy completions; the footnote suggests a version of Koszul duality that is a genuine equivalence might help.

### 🔵 `OP-A2F613EC6F07` — `background_open` | MSC 17B35 | 难度 hard

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, §0.1
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Let us suppose that we are only given $U\g$ as an associative algebra --- is it still possible to recover the Lie algebra $\g$? This question is in fact an open problem, which seems to have been first stated in print by Bergman

**自包含改写**：Bergman's problem: given a Lie algebra g over a field, is g determined up to isomorphism by its universal enveloping algebra U(g), considered only as an associative algebra (without the bialgebra/coalgebra structure)? In full generality this remains open over fields of characteristic zero.

**判定理由**：Long-standing problem of Bergman cited as motivation; the paper only proves the nilpotent case, not the general statement.

**关联卡**：The nilpotent special case is solved in this paper (see Corollary 'classical Thm B' card).

### 🟠 `OP-A9F193475ADE` — `method_obstruction` | MSC 18M70 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 6 (sect:background), discussion after Theorems quasi-inverse coalgebras / minimal coalgebras
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We are not aware of any useful analogue of the Homotopy Transfer Theorem in the category of locally finite $\P_\infty$-coalgebras.

**自包含改写**：The paper notes that the Homotopy Transfer Theorem (used to prove minimal models and existence of quasi-inverses for ∞-coalgebras) relies on infinite sums over trees that need not converge in the category of locally finite P-infinity-coalgebras (for a Koszul operad P over a field of characteristic zero with finite-dimensional P(n)), and no useful analogue of the Homotopy Transfer Theorem in that category is known to the authors. No formal open problem is stated; this is a documented method obstruction.

**判定理由**：Documents a failure of the standard method in the locally finite setting without formally posing a problem.

**关联卡**：Reason the paper works with general (non-locally-finite) ∞-coalgebras despite all its examples being conilpotent.

**存疑**：Could be read as an implicit open problem, but no formal proposition is stated.

### 🔴 `OP-165781CE1654` — `solved_in_paper` | MSC 17B55 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Theorem B, Introduction; restated in Section 4 (sect:thmb)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $\g$ and $\h$ be dg Lie algebras over a field of characteristic zero. If their universal enveloping algebras $U\g$ and $U\h$ are quasi-isomorphic as associative dg algebras then the homotopy completions $\hc\g$ and $\hc\h$ are quasi-isomorphic as dg Lie algebras.

**自包含改写**：Theorem B (proved in the paper): Let g and h be dg Lie algebras over a field of characteristic zero. If their universal enveloping algebras U(g) and U(h) are quasi-isomorphic as associative dg algebras, then the homotopy completions g^{h∧} and h^{h∧} (completions with respect to the lower central series filtration of a cofibrant replacement, e.g. the bar-cobar resolution) are quasi-isomorphic as dg Lie algebras.

**判定理由**：Main theorem proved in the paper; the completeness-free version remains open.

**关联卡**：Weakened (homotopy-complete) form of the real_open statement in the introduction; implies the nilpotent case via the homotopy completeness theorem.

### 🔴 `OP-4C4D4C72ADB1` — `solved_in_paper` | MSC 13D10 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Theorem A, Introduction; restated in Section 3 (sect:thma)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $A$ and $B$ be two commutative dg algebras over a field of characteristic zero. Then, $A$ and $B$ are quasi-isomorphic as  associative dg algebras if and only if they are also quasi-isomorphic as commutative dg algebras.

**自包含改写**：Theorem A (proved in the paper): Let A and B be two commutative differential graded algebras over a field of characteristic zero. Then A and B are quasi-isomorphic as associative dg algebras if and only if they are quasi-isomorphic as commutative dg algebras (quasi-isomorphic = linked by a zig-zag of morphisms inducing homology isomorphisms in the respective category).

**判定理由**：The folklore problem is settled completely in characteristic zero by the paper's main theorem.

**关联卡**：Generalization to split injections of Koszul operads stated as Theorem 'generalization'; proof details left to the reader but claimed not to be difficult.

### 🔴 `OP-B0017BD78640` — `solved_in_paper` | MSC 17B55 | 难度 medium

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, §0.7 (harper-hess-criterion paragraph)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> It is natural to ask for simple conditions ensuring this.

**自包含改写**：Partially resolved in the paper: the paper asks for simple conditions ensuring that a dg Lie algebra g over a field of characteristic zero is homotopy complete (i.e. quasi-isomorphic to the completion of a cofibrant replacement), and proves that g is homotopy complete if either (i) g is nilpotent (lower central series bounded below in each homological degree) and concentrated in nonnegative homological degree, or (ii) g is concentrated in strictly negative homological degree; it also recovers Harper--Hess's result that dg Lie algebras concentrated in positive homological degrees are homotopy complete. Finding further general conditions remains open in general.

**判定理由**：The paper proves its stated sufficient conditions; the general question of characterizing homotopy completeness is only partially addressed.

**关联卡**：Combines with Theorem B to give the nilpotent Lie algebra corollary.

**存疑**：The 'natural ask' is open-ended; only specific sufficient conditions are proved.

### 🔴 `OP-D19A62B6EAC1` — `solved_in_paper` | MSC 17B35 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, Corollary (classical Thm B)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> The universal enveloping algebras $U\g$ and $U\h$ are isomorphic as associative algebras if and only if $\g$ and $\h$ are isomorphic as Lie algebras.

**自包含改写**：Let g and h be nilpotent Lie algebras over a field of characteristic zero. Then the universal enveloping algebras U(g) and U(h) are isomorphic as associative algebras if and only if g and h are isomorphic as Lie algebras.

**判定理由**：The paper proves this statement, resolving Bergman's problem in the nilpotent case.

**关联卡**：Special case of Bergman's general problem (background_open card), and classical specialization of Theorem B.

### ⚪ `OP-68F95A239CA0` — `future_application` | MSC 17B35 | 难度 easy

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, §0.10
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> One could ask whether our methods could be simplified if we only wanted to give a proof of \cref{classical Thm B}, so that we could give a more direct argument in this special case. We do not believe that this is possible.

**自包含改写**：A taste/methodological comment, not a mathematical proposition: the authors state their belief that no simpler or more direct proof of the nilpotent case (isomorphism of nilpotent Lie algebras from isomorphism of their universal enveloping associative algebras over a field of characteristic zero) is possible via their approach, since the argument necessarily passes to the Koszul dual dg setting. This is a value judgement about proof strategies, not an open problem.

**判定理由**：Comment on proof strategy and belief; not a decidable proposition.

**关联卡**：Relates to the solved-in-paper nilpotent case of Bergman's problem.


## `1904.12262` — The Fuglede conjecture for convex domains is true in all dimensions
- 权威出处：**Acta Mathematica** 2022，DOI `10.4310/acta.2022.v228.n2.a3`
- 连接方式：`doi`｜全文 127,456 字符 via `cache-latex`｜提取模式 `reasoning`

### 🔵 `OP-F46F4B649B52` — `background_open` | MSC 42B10 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1.1 (Introduction), paragraph discussing counterexamples to Fuglede's conjecture
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The conjecture is still open in dimensions $d=1$ and $2$ in both directions.

**自包含改写**：Fuglede's conjecture (1974): a bounded measurable set Ω ⊂ ℝ^d of positive Lebesgue measure is spectral — i.e., there exists a countable set Λ ⊂ ℝ^d such that the exponentials e_λ(x) = e^{2πi⟨λ,x⟩}, λ ∈ Λ, form an orthogonal basis of L²(Ω) — if and only if Ω tiles ℝ^d by translations — i.e., there is a countable set Λ' ⊂ ℝ^d such that {Ω + λ' : λ' ∈ Λ'} partitions ℝ^d up to measure zero. Counterexamples in both directions exist for d ≥ 3 (built from finitely many unit cubes); as of this paper the conjecture remains unresolved for general (not necessarily convex) sets in dimensions d = 1 and d = 2, in both directions (spectral ⇒ tiling and tiling ⇒ spectral).

**判定理由**：Famous Fuglede conjecture for general (non-convex) sets, cited as background; the paper notes it remains open only in dimensions d = 1 and 2. Not this paper's own target.

**关联卡**：Same conjecture whose convex-body case is the target of the card 'Theorem 1.1 (Fuglede for convex bodies)'; the paper settles only the convex-body case and leaves the general d = 1, 2 case untouched. The Introduction's broad motivating question 'Which other sets Ω can be spectral?' refers to the same program and is subsumed here.

### 🟠 `OP-A7346FB347D8` — `method_obstruction` | MSC 52C22 | 难度 easy

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.3 (Introduction), remark following Theorem 1.4 (thmA11)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We observe that the weak tiling conclusion cannot be strengthened to proper tiling without imposing extra assumptions on the set $\Om$, since there exist examples of spectral sets which cannot tile by translations.

**自包含改写**：For general bounded measurable sets Ω ⊂ ℝ^d of positive measure (not assumed convex), the paper's Theorem 1.4 gives only a weak tiling necessary condition for spectrality: there exists a positive, locally finite measure μ on ℝ^d with 1_Ω * μ = 1_{ℝ^d∖Ω} a.e. The paper observes that this conclusion cannot be strengthened to a proper tiling — i.e., μ need not be of the form Σ_{λ∈Λ} δ_λ for a locally finite set Λ, which would mean the translated copies {Ω+λ} partition the complement up to measure zero, i.e., that Ω tiles ℝ^d by translations — without imposing extra assumptions on Ω, because spectral sets which cannot tile by translations are known to exist (counterexamples in d ≥ 3). This is a scope limitation of the method, not a posed problem.

**判定理由**：Observation that the weak-tiling necessary condition cannot be strengthened to proper tiling for general bounded measurable sets without extra assumptions; a hypothesis/scope limitation, not a posed open problem.

**关联卡**：Complements the main theorem card: for convex bodies the paper supplies the extra structure (Theorems 4.1 and 6.1) under which the weak tiling of the complement becomes a proper tiling.

**存疑**：The underlying fact (existence of spectral non-tiling sets) is prior background knowledge cited by the paper (Tao 2004 and subsequent counterexamples); the sentence itself is an observation, not a new result of this paper.

### 🟠 `OP-CFB6B1DE985C` — `method_obstruction` | MSC 42B10 | 难度 easy

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 3.4, concluding remark after the proof of Theorem 3.3 (thmB1)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> On the other hand, if $\Om$ is a convex body in $\R^d$, then there exists no set $S$ satisfying the conditions \ref{thmA2.1}, \ref{thmA2.2} and \ref{thmA2.3} in \thmref{thmA2}. So in order to study  the spectrality problem for convex bodies, we must use the weak tiling condition $\1_\Om \ast \mu = \1_{\Om^\cm}$ a.e.\ in a stronger way.

**自包含改写**：The paper's Theorem 3.2 gives a non-spectrality criterion: a bounded measurable set Ω ⊂ ℝ^d cannot be spectral if there exists a measurable set S ⊂ ℝ^d with (i) m(S) > 0; (ii) m(S ∩ Ω) = 0; (iii) for every x ∈ ℝ^d, if m((Ω+x) ∩ S) > 0 then m((Ω+x) ∩ Ω) > 0 (m denotes Lebesgue measure). The paper asserts that if Ω is a convex body in ℝ^d (compact convex set with nonempty interior), then no measurable set S satisfying conditions (i)-(iii) exists, so this criterion is vacuous for convex bodies; consequently the weak tiling condition 1_Ω * μ = 1_{ℝ^d∖Ω} a.e. must be exploited in a stronger way, which the paper carries out in Sections 4-6. This is a methodological remark, not a posed open problem.

**判定理由**：The paper shows its simple non-spectrality criterion (Theorem 3.2) is vacuous for convex bodies, requiring stronger use of weak tiling; a method limitation, with no open problem formally posed.

**⚠️ 人工复核标记**：The non-existence of a set S with properties (i)-(iii) for a general convex body is asserted in the source without proof; treated as an obvious observation motivating the stronger method.

**关联卡**：Motivates the stronger analysis of the weak tiling condition in Sections 4-6 that yields the main theorem (Theorem 1.1) recorded in the solved_in_paper card.

**存疑**：The assertion is stated without proof in the source; it is plausible but is presented as an observation rather than a lemma.

### 🔴 `OP-6A9E9F47265C` — `solved_in_paper` | MSC 42B10 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1.1 (Introduction), Theorem 1.1 (thmA15)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $\Om$ be a convex body in $\R^d$. If $\Om$ is a spectral set, then $\Om$ must be  a convex polytope, and it  tiles the space face-to-face by translations along a lattice.

**自包含改写**：Let Ω ⊂ ℝ^d be a convex body (a compact convex set with nonempty interior), in arbitrary dimension d. If Ω is spectral — i.e., L²(Ω) has an orthogonal basis of exponentials e_λ(x) = e^{2πi⟨λ,x⟩}, λ ∈ Λ, for some countable Λ ⊂ ℝ^d — then Ω must be a convex polytope, and it tiles ℝ^d face-to-face by translations along a lattice. Combined with the previously known converse for convex bodies (a translation-tiling convex body is a centrally symmetric polytope admitting a face-to-face lattice tiling whose dual lattice is a spectrum), this is equivalent to: a convex body Ω ⊂ ℝ^d is spectral if and only if it tiles the space by translations, i.e., Fuglede's conjecture for convex bodies in all dimensions. Before this paper, the 'spectral implies tiling' direction was known only in ℝ² (Iosevich–Katz–Tao 2003) and in ℝ³ under the a priori assumption that Ω is a convex polytope (Greenfeld–Lev 2017); in higher dimensions it was completely open, even for polytopes.

**判定理由**：This direction was completely open in dimensions d ≥ 4 (even for polytopes) before this paper; the paper proves it in all dimensions, fully settling Fuglede's conjecture for convex bodies.

**关联卡**：Proof components proved in the paper: Theorem 1.2 (a spectral convex body must be a convex polytope), Theorem 1.3 (a spectral, centrally symmetric convex polytope with centrally symmetric facets has every belt consisting of 4 or 6 facets), and Theorem 1.4 (spectrality implies the complement ℝ^d∖Ω admits a weak tiling by translates of Ω), combined with known results of Kolountzakis (central symmetry), Greenfeld–Lev (centrally symmetric facets), and the Venkov–McMullen tiling characterization.

### ⚪ `OP-4F4448A98FC1` — `future_application` | MSC 42B10 | 难度 easy

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.3 (Introduction), paragraph following the weak tiling discussion of Theorem 1.4
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The potential applications of \thmref{thmA11} are not limited to the class of convex bodies in $\R^d$.

**自包含改写**：The paper's Theorem 1.4 states that if a bounded measurable set Ω ⊂ ℝ^d (of positive measure) is spectral, then its complement ℝ^d ∖ Ω admits a weak tiling by translates of Ω, i.e., there exists a positive, locally finite measure μ on ℝ^d with 1_Ω * μ = 1_{ℝ^d∖Ω} a.e. The quoted sentence is an outlook/value judgement stating that the potential applications of this theorem go beyond the class of convex bodies in ℝ^d; within the paper itself, two such applications are realized (a geometric non-spectrality criterion, Theorem 3.2, and the result that the boundary of a bounded open spectral set has Lebesgue measure zero, Theorem 3.3). This is explicitly not a mathematical proposition.

**判定理由**：Explicit value judgement on potential applications of the weak-tiling theorem beyond convex bodies; not a mathematical proposition, hence future_application.

**关联卡**：Refers to Theorem 1.4, the key new tool behind the main theorem (Theorem 1.1) recorded in the solved_in_paper card; the applications mentioned as examples (Theorems 3.2 and 3.3) are proved in the paper.

### ⚪ `OP-63F1F963A6F4` — `future_application` | MSC 42B10 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 3.1, remark immediately after the statement of Theorem 3.1 (thmA8)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> A similar result can be proved in the more general context of locally compact abelian groups, but in this paper we work in the euclidean setting only.

**自包含改写**：The paper's Theorem 3.1 states: if Ω ⊂ ℝ^d is bounded, measurable and spectral, then there exists a measure γ on ℝ^d that is (a) positive and translation-bounded; (b) supported in the set of zeros of the Fourier transform of the indicator function 1_Ω together with {0}; (c) equal to δ_0 in some open neighborhood of the origin; (d) has Fourier transform γ̂ which is also a positive, translation-bounded measure; and (e) γ̂ = m(Ω)·δ_0 on the set Δ(Ω) = {x ∈ ℝ^d : m(Ω ∩ (Ω+x)) > 0}. The quoted remark — an outlook/scope statement, without proof in this paper — asserts that a similar result can be proved with ℝ^d replaced by a general locally compact abelian group. This is explicitly not a formally posed mathematical problem.

**判定理由**：Outlook remark asserting, without proof, that Theorem 3.1 extends to locally compact abelian groups; a scope/taste comment rather than a posed problem (no-taskification rule).

**关联卡**：Extends the autocorrelation/diffraction construction (Theorem 3.1) underlying Theorem 1.4, the key tool behind the main theorem recorded in the solved_in_paper card.

**存疑**：The authors assert provability of the locally compact abelian group analogue without giving a proof or reference in this paper; hence it is recorded as an outlook remark, not as an open or solved proposition.


## `1812.00309` — The directed landscape
- 权威出处：**Acta Mathematica** 2022，DOI `10.4310/acta.2022.v229.n2.a1`
- 连接方式：`doi`｜全文 245,954 字符 via `cache-latex`｜提取模式 `fast`

### 🟢 `OP-1A2DBE85DBA3` — `real_open` | MSC 60K35 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 10 (Open questions), Conjecture 10.2
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The function $\scrH$ is an Airy sheet.

**自包含改写**：Let $\scrA$ be the parabolic Airy line ensemble and define $\scrH:\R^2 \to \R$ as follows: for $x>0$, $\scrH(x,\cdot)$ is defined by the Busemann-type limit $\lim_{k\to\infty}\big\langle(-\sqrt{k/(2x)},k)\LP z\big\rangle-\big\langle(-\sqrt{k/(2x)},k)\LP y\big\rangle = \scrH(x,z)-\scrH(x,y)$ (where $\langle\cdot\LP\cdot\rangle$ denotes last passage across $\scrA$); set $\scrH(0,y)=\scrA_1(y)$; and for $x>0$ define $\scrH(-x,y)$ by applying the same formulas to the reflected ensemble $\scrA_\cdot(-\,\cdot)$. Conjecture: $\scrH$ is an Airy sheet (i.e. has the law of the unique object from Definition 8.1).

**判定理由**：Posed by this paper as its own conjecture (a decidable mathematical statement), though the paper notes the authors resolved it in the companion preprint dauvergne2021scaling.

**⚠️ 人工复核标记**：The paper states: 'Since the first version of this paper appeared, we proved Conjecture 10.2, see Theorem 1.21 in \cite{dauvergne2021scaling}' — the conjecture is resolved in a companion paper, not this one.

**关联卡**：Distinct from the card on the fine error term of the Airy line ensemble last passage problem; that card concerns conjecture 10.3.

### 🟢 `OP-6E2366C6054F` — `real_open` | MSC 60K35 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 10 (Open questions), Conjecture 10.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> There exists a deterministic function $a:\R^+\times \N\to \R$ so that for every $x>0$, almost surely as $k\to\infty$ we have
$$
\scrA[(-\sqrt{k/(2x)},k)\LP (0,1)]-a(x,k) \to \scrS(x,0).
$$

**自包含改写**：Let $\scrA$ be the parabolic Airy line ensemble, $\scrS$ the Airy sheet, and $\scrA[(p,k)\LP(q,1)]$ the last passage value in $\scrA$ from point $(p,k)$ to $(q,1)$. Conjecture: there exists a deterministic function $a:\R^+\times\N\to\R$ such that for every $x>0$, almost surely as $k\to\infty$, $\scrA[(-\sqrt{k/(2x)},k)\LP(0,1)]-a(x,k)\to\scrS(x,0)$. The paper notes this would follow from improving its bound $\scrA[(0,k)\LP(x,1)]=2\sqrt{2kx}+o(\sqrt{k})$ to an error of order $O(k^{-1/6})$, in which case $a(x,k)=\E\scrA_1(0)-\E\scrA_k(0)-\sqrt{2kx}$.

**判定理由**：An explicitly posed conjecture of this paper; a decidable mathematical statement, unresolved within this paper.

**关联卡**：Directly tied to the next card (the believed $O(k^{-1/6})$ error term), which implies it; emitted separately since the error-term statement is a distinct, stronger refinement.

### 🟢 `OP-70831898C7E1` — `real_open` | MSC 60K35 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 10 (Open questions), Conjecture 10.6
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Consider the process $\eta_t:[0,1/2]\to \R$ defined by
$$\eta_t(s)=\Pi(t+s)-\Pi(t).$$
Let $0\le t<u<1/2$.  The law of $\eta_t$ and $\eta_u$ are mutually absolutely continuous if and only if $t>0$.

**自包含改写**：Let $\Pi$ be the directed geodesic in the directed landscape from $(0,0)$ to $(0,1)$, and define $\eta_t:[0,1/2]\to\R$ by $\eta_t(s)=\Pi(t+s)-\Pi(t)$. Conjecture: for $0\le t<u<1/2$, the laws of $\eta_t$ and $\eta_u$ are mutually absolutely continuous if and only if $t>0$.

**判定理由**：Explicitly stated conjecture of this paper; a decidable probabilistic statement not resolved in the paper.

**关联卡**：The paper says 'we believe that the beginning of geodesics are special.'

### 🟢 `OP-7BEA9F0AFD6B` — `real_open` | MSC 60K35 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 10 (Open questions), Problem 10.4
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Find a formula for the probability that $\Pi_{0,0}$ and $\Pi_{x,y}$ intersect.

**自包含改写**：In the directed landscape $\scrL$, let $\Pi_{x,y}$ denote the (almost surely unique) directed geodesic from spacetime point $(x,0)$ to $(y,1)$, for $x,y\in\R$. By invariance of the directed landscape, the probability that $\Pi_{0,0}$ and $\Pi_{x,y}$ intersect depends only on two parameters. Problem: find a formula for this probability.

**判定理由**：An explicitly stated open problem (formula request) posed by this paper.

### 🟢 `OP-81F215614B8F` — `real_open` | MSC 60K35 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 10 (Open questions), Problem 10.5
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> (a) Find the distribution of $\Pi(s)$ for all $s$.

(b) Find the distribution of $\max_s \Pi(s)$.

**自包含改写**：Let $\Pi=\Pi_{0,0}$ be the directed geodesic in the directed landscape from $(0,0)$ to $(0,1)$, viewed as a random continuous function $\Pi:[0,1]\to\R$. Problem: (a) find the distribution of $\Pi(s)$ for all $s\in[0,1]$; (b) find the distribution of $\max_{s\in[0,1]}\Pi(s)$. The paper notes Proposition 9.4 gives tail bounds on these quantities of the form $e^{-x^3}$.

**判定理由**：Explicitly stated open problem asking for unknown distributions.

**关联卡**：Part (a) 'depends only on two Airy processes, so it should be doable using continuum statistics' per the paper.

### 🟢 `OP-AE440398E010` — `real_open` | MSC 60K35 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 10 (Open questions), Question 10.7
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Let $h: \R^2 \to \R$ be a smooth function with compact support. Define the $h$-shift $\scrL'$ of the directed landscape $\scrL$ by the length formula:
$$
\int d \scrL' \circ \pi =\int d \scrL \circ \pi + \int h(\pi(t),t)\,dt
$$
Is the distribution of $\scrL'$ absolutely continuous with respect to the directed landscape? If so, what is the density?

**自包含改写**：Let $\scrL$ be the directed landscape and define path length $\int d\scrL\circ\pi = \inf_{k}\inf_{t=t_0<\dots<t_k=s}\sum_i \scrL(\pi(t_{i-1}),t_{i-1};\pi(t_i),t_i)$ for continuous $\pi:[t,s]\to\R$. For a smooth compactly supported $h:\R^2\to\R$, define the $h$-shift $\scrL'$ by the length formula $\int d\scrL'\circ\pi = \int d\scrL\circ\pi + \int h(\pi(t),t)\,dt$. Question: is the distribution of $\scrL'$ absolutely continuous with respect to the directed landscape? If so, what is the density?

**判定理由**：Explicitly posed question (a Girsanov-type statement for the 1-2-3 scaling); a precise open mathematical proposition.

**关联卡**：Motivated by the paper's remark that 'there should be a stochastic calculus for the 1-2-3 scaling.'

### 🟢 `OP-B163D2280AE7` — `real_open` | MSC 60K35 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 6, discussion after Theorem 6.4 and repeated in Section 10 (Open questions) before Conjecture 10.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We believe that the correct error term here is $O(k^{-1/6})$, as in Brownian last passage percolation.

**自包含改写**：Let $\scrA$ be the parabolic Airy line ensemble and $\langle(0,k)\LP x\rangle = \scrA[(0,k)\LP(x,1)]$ the last passage value from line $k$ at time $0$ to line $1$ at time $x>0$. Conjecture: $\langle(0,k)\LP x\rangle = 2\sqrt{2kx} + O(k^{-1/6})$ as $k\to\infty$ (mirroring the $k^{-1/6}$ fluctuation scale in Brownian last passage percolation). The paper proves the weaker bound $|\langle(0,k)\LP x\rangle - 2\sqrt{2kx}|$ is $o(k^{3/7}\log^d k)$ in a summability sense, and states that improving this to $o(1)$ would be of interest.

**判定理由**：A believed mathematical statement (error order) posed by the paper, not proven here; the paper's methods do not achieve it.

**⚠️ 人工复核标记**：The paper itself remarks 'even our most optimistic heuristic proofs of the above theorem did not yield this error.'

**关联卡**：Implies Conjecture 10.3 (previous card); related to the 'It would be of interest to improve the above result to get a bound that is $o(1)$' remark.

### 🟠 `OP-984542551A31` — `method_obstruction` | MSC 60K35 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 6, discussion after Theorem 6.4
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> While the $o(k^{3/7}\log^d k)$ error we get could be improved by a more careful application of our methods, even our most optimistic heuristic proofs of the above theorem did not yield this error.

**自包含改写**：For the Airy line ensemble last passage value $\langle(0,k)\LP x\rangle$ (last passage in the parabolic Airy line ensemble from $(0,k)$ to $(x,1)$, $x>0$), Theorem 6.4 shows a summable tail bound for $(\langle(0,k)\LP x\rangle-2\sqrt{2kx})/(k^{3/7}\log^d k)$; the paper states its methods cannot reach the believed $O(k^{-1/6})$ error scale — a method limitation, not a formally posed problem.

**判定理由**：The paper shows its method's limitation in improving the error bound without formally posing a separate open problem (the associated conjecture is captured on the $O(k^{-1/6})$ card).

**关联卡**：Methodological counterpart of the $O(k^{-1/6})$ conjecture card and Conjecture 10.3.

### ⚪ `OP-62256824A0D9` — `future_application` | MSC 60K35 | 难度 frontier

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Remark after Definition 1.2 (Airy sheet), item 3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We expect it to be a universal limit object in the Kardar-Parisi-Zhang (KPZ) universality class, see \cite{corwin2016kardar} for an informal description.

**自包含改写**：The authors express the expectation (a value judgement / research outlook, not a formal proposition here) that the Airy sheet and directed landscape are universal limit objects for the KPZ universality class, beyond the Brownian and classical integrable models they establish.

**判定理由**：Universality expectation stated informally; not posed as a formal open proposition in this paper.

**关联卡**：Repeated for the directed landscape in Remark 1.6, item 2.

### ⚪ `OP-A504110C47AF` — `future_application` | MSC 60K35 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), concluding paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The focus of this paper is to construct the limiting objects, and we do not explore their properties in detail here. However, our description makes several natural questions about the directed landscape accessible. We will analyze the geometry of this object in future work.

**自包含改写**：The authors state an intention to analyze the geometry of the directed landscape in future work — a research-direction remark, not a mathematical proposition.

**判定理由**：Explicitly a statement about future work, not a posed problem.


## `1707.02959` — Mirror symmetry for very affine hypersurfaces
- 权威出处：**Acta Mathematica** 2022，DOI `10.4310/acta.2022.v229.n2.a2`
- 连接方式：`doi`｜全文 178,700 字符 via `cache-latex`｜提取模式 `fast`

### 🟢 `OP-3CE2A149C3A7` — `real_open` | MSC 53D20 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 2.3 (LG model)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Of course, we expect that any other reasonable construction of such a pair from $W$ 
will be deformation equivalent to ours, in particular giving the same Fukaya category.

**自包含改写**：Expectation (not proven here): given a Laurent polynomial W: (C*)^n -> C with Newton polytope Delta^vee, any reasonable construction of a Liouville pair (D, F cap D) from W (D a Liouville subdomain of (C*)^n completing to it, F a symplectic hypersurface) is deformation equivalent to the pair constructed in the paper via Mikhalkin patchworking, and in particular yields the same wrapped Fukaya category.

**判定理由**：An explicitly stated expectation not proven in the paper, though phrased informally ('we expect').

**存疑**：Borderline between real_open and future_application; 'we expect... will be deformation equivalent' is a decidable mathematical claim posed as expectation, so treated as real_open.

### 🟢 `OP-60517DCDA2D4` — `real_open` | MSC 14M25 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 5.2 (The skeleton of F_Sigma), Remark after Definition of PC fan
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> So far, no fan is known to us not to be PC; nor, however, do we know any compelling reason why all fans should be PC.

**自包含改写**：A fan Sigma is called PC if there exists a convex piecewise-linear function alpha: Delta^vee -> R inducing the regular triangulation of Delta^vee defined by Sigma, such that the polytope Pi^0_Sigma (the component of M_R \ Pi_Sigma dual to the zero cone) is perfectly centered. Open question: does there exist a fan that is not PC, and is every fan PC? (A polytope P is perfectly centered if for each nonempty face F of P, the normal cone of F, transported to M^vee_R by an inner product, meets the relative interior of F.)

**判定理由**：Authors explicitly state they do not know whether all fans are PC nor a counterexample; this hypothesis is used in the paper.

**关联卡**：The PC hypothesis is used in Theorem on skeleton of F_Sigma; the paper notes (citing Zhou) that this hypothesis can be removed.

### 🟢 `OP-7BB5A62C33AF` — `real_open` | MSC 53D20 | 难度 medium

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 2.4 (Sheaves), footnote
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> To deduce Kontsevich's statement from \cite{GPS2}, 
one would want to know further that appropriate open covers 
of the skeleton lift to sectorial covers.  It is expected that such a lifting is not difficult to construct
in general.  In the case of relevance to this article, it is likely possible to construct such a cover by hand, 
though we will not do it here, as we do not invoke this result (instead we use \cite{GPS3}).

**自包含改写**：Expected but unproven lifting statement: for a Weinstein manifold, appropriate open covers of the skeleton (as in Kontsevich's localization conjecture of a cosheaf of categories on the skeleton recovering the wrapped Fukaya category) lift to sectorial covers in the sense of Ganatra-Pardon-Shende, from which Kontsevich's statement would follow via sectorial descent; in the case relevant to this article (covers of the boundary FLTZ skeleton of a toric stack) such a lift is likely constructible by hand.

**判定理由**：An expected mathematical statement the paper leaves unproven, tied to Kontsevich's localization conjecture.

**关联卡**：Related to the Remark in Section 2.1: a lift of the cover of the skeleton in Cor. cover1 to a sectorial cover 'would yield a proof hewing closer to the above illustration.'

**存疑**：Also related to a Remark in Section 2.1 expressing the same lifting as desirable; merged here per no-duplicate rule.

### 🟢 `OP-C1EBF0FBD568` — `real_open` | MSC 14M25 | 难度 medium

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 2.5, Remark after the bolded statement of the isomorphism Coh(partial T_Sigma) = mu sh(partial LL_Sigma)^c
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In fact such an isomorphism exists without the smoothness hypothesis.  We do not show this here but
briefly indicate how one can, see Remarks \ref{rem: Kuwagaki} and \ref{rem: blowdown}.

**自包含改写**：Claim (asserted, proof omitted): the isomorphism Coh(partial T_Sigma) \cong mu sh(partial LL_Sigma)^c between coherent sheaves on the toric boundary and compact wrapped microlocal sheaves on the Legendrian boundary of the FLTZ skeleton exists also without the smoothness hypothesis on the (stacky) fan Sigma; proof strategy indicated via a toric resolution, semiorthogonal decomposition on the B-side, and stop removal on the A-side.

**判定理由**：A stated mathematical claim the paper asserts but does not prove; adopted as target.

**关联卡**：Same assertion appears in Remark 'rem: blowdown' after Theorem ccc-infty.

### 🟢 `OP-D4D8BA9EE907` — `real_open` | MSC 53D20 | 难度 medium

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 4.3 (The skeleton of tailored pants), Remark
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It is presumably
true that the tailoring isotopy (recalled in Remark~\ref{rem:isodef} below from \cite[Section 4]{A1}) is an isotopy of Liouville manifolds, but we do not prove this
here.

**自包含改写**：Claim (presumed, unproven): the tailoring isotopy from the standard pants P_{n-1} (complement of a linear hypersurface in (C*)^n, a Stein submanifold with restricted Liouville form) to the tailored pants \tilde P_{n-1}, constructed via the formula f^{t,s} = sum_m t^{-alpha(m)}(1 - s phi_m(Log z)) z^m, is an isotopy of Liouville manifolds.

**判定理由**：A decidable mathematical assertion the authors believe true but explicitly do not prove.

**存疑**：Phrased with 'presumably'; still a concrete mathematical statement left unproven by this paper.

### 🟠 `OP-913AF47D9EFD` — `method_obstruction` | MSC 53D20 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 2.6 (Other related works)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The \cite{AAK} mirrors can also be approached directly by the methods of this paper. The main new difficulty in
carrying this out is that the amoebal complements have many bounded components, 
making it more difficult to find a contact-type hypersurface containing the skeleton.

**自包含改写**：Methodological gap: extending the paper's construction (identifying the skeleton of a very affine hypersurface with a boundary FLTZ skeleton and finding a contact-type hypersurface containing it) to the Abouzaid-Auroux-Katzarkov mirrors based on maximal subdivisions of Delta^vee is obstructed by the many bounded components of the amoeba complements; the paper suggests a higher-dimensional version of the inductive Pascaleff-Sibilla gluing argument could work, using the paper's microlocalization of Kuwagaki's theorem as gluing input.

**判定理由**：Identifies a specific difficulty/obstruction and possible route without formally posing a problem.

### ⚪ `OP-06462EF03569` — `future_application` | MSC 14J33 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 2.6 (Other related works)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> One could
try and compare algebraically the resulting categories.  For that matter, we have provided
here many mirrors, depending on the choice of point, and it should be interesting to understand
the derived equivalences between them in algebro-geometric terms.

**自包含改写**：Research direction: compare algebraically the mirror category of this paper (associated to a star-shaped triangulation of Delta^vee centered at one point) with the a priori different category of singularities mirror of Abouzaid-Auroux-Katzarkov (associated to a maximal subdivision of Delta^vee); and understand, in algebro-geometric terms, the derived equivalences between the many mirrors obtained from different choices of center point.

**判定理由**：Taste/interest remark ('should be interesting') and suggested comparison, not a posed proposition.

**关联卡**：Related to Corollary dereq, which proves existence of derived equivalences Coh(T_{Sigma_1}) = Coh(T_{Sigma_2}) but without an algebro-geometric formula.

### ⚪ `OP-8F15ED6374F4` — `future_application` | MSC 53D40 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), footnote 1
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It is a tautology that matching the limit categories
 matches their infinitesimal deformations, but it remains to identify the geometric meaning of these 
deformations in a satisfactory way -- we do not touch upon this question here.

**自包含改写**：Open direction: for the mirror symmetry established at the large-volume/complex-structure limit point (equivalence Coh(partial T_Sigma) = Fuk(F_W)), identify the geometric meaning of the infinitesimal deformations of the limit categories in a satisfactory way; the paper works only at the limit and does not address deformations away from it (e.g. holomorphic disks through the compactifying boundary divisor).

**判定理由**：A research direction about deforming away from the limit; the paper explicitly declines to formulate or address a proposition.

**关联卡**：Related to the concluding remark that studying this deformation 'is the Fukaya category which one knows how to deform away from the large volume limit... However, we do not take up the study of this deformation in the present work.'

### ⚪ `OP-B07773C1D5A9` — `future_application` | MSC 53D20 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 2.6 (Other related works), last paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The gluing result needed is exactly our microlocalization of the theorem of Kuwagaki.  We will return elsewhere
to the question of its interaction with deformations of the skeleton.

**自包含改写**：Announced future investigation: the interaction of the paper's functoriality result (microlocalization of Kuwagaki's coherent-constructible correspondence, i.e. restriction to toric orbit closures is mirror to microlocalization) with deformations of the skeleton, as needed for the gluing-based extension to AAK-type mirrors.

**判定理由**：Announced future-work direction, not a posed proposition.

**关联卡**：Related to the AAK method_obstruction card.

### ⚪ `OP-D27192A8A558` — `future_application` | MSC 14E30 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 7, after Corollary dereq
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> What the above argument does not yet give is a formula for the above equivalence.  In fact, there are many such 
derived equivalences, corresponding to monodromies (as we vary the coefficients of $f$) around the discriminant 
locus. We will describe these in future work.

**自包含改写**：Future target: give an explicit formula for the derived equivalences Coh(T_{Sigma_1}) \cong Coh(T_{Sigma_2}) between toric varieties from star-shaped triangulations Sigma_1, Sigma_2 of the same Newton polytope Delta of a Laurent polynomial W: (C*)^n -> C, including the equivalences corresponding to monodromies around the discriminant locus as the coefficients of f vary.

**判定理由**：Announced future work providing formulas; the existence is already proven (Cor. dereq), only the formula is open.

**关联卡**：Related to the 'compare algebraically the resulting categories' card; existence proven in Cor. dereq, formula deferred.

### ⚪ `OP-FBFA23FCCBAC` — `future_application` | MSC 14J33 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 7.1 (Non-Fano mirror symmetry)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Here we explain this discrepancy in an example; in future work, we plan to use the same ideas to
establish
the conjectures of \cite{BDFKK}.

**自包含改写**：Announced target: use the ideas of this paper (identification of FLTZ boundary skeleta with hypersurface skeleta, microlocalization of Kuwagaki's theorem) to establish the conjectures of Ballard-Diemer-Favero-Katzarkov-Kerr on non-Fano toric homological mirror symmetry (modifying the naive Hori-Vafa mirror of a non-Fano toric variety so that the coherent sheaf category is not a proper subcategory).

**判定理由**：Announced future work targeting external conjectures; the paper does not adopt these as its own open problem here.

**存疑**：Could also be read as background_open (BDFKK conjectures) adopted as target; labeled future_application because only a plan is stated.


## `1505.01790` — Gravitational instantons with faster than quadratic curvature decay. I
- 权威出处：**Acta Mathematica** 2021，DOI `10.4310/acta.2021.v227.n2.a2`
- 连接方式：`doi`｜全文 116,917 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟢 `OP-07D99020CAE5` — `real_open` | MSC 53C25 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, ALF discussion, item (2) on the ALF-D_k case
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It is conjectured that any ALF-$D_k$ instanton must be exactly the metric constructed by them. This conjecture has not been solved yet.

**自包含改写**：An ALF-D_k gravitational instanton is a complete hyperkähler 4-manifold (under the paper's standing assumption |Rm|(x) ≤ r(x)^{-2-ε}, ε > 0 small, say < 1/100) whose tangent cone at infinity is R^3/Z_2 and which is asymptotic to the standard ALF-D_k model: the Z_2-quotient of the trivial product (R^3 − B_R) × S^1 (case k = 2), or the quotient of the Taub-NUT metric with mass m (me < 0) outside a ball by the binary dihedral group D_{4|e|} of order 4|e| (case k = −e + 2). Conjecture (concerning the metrics constructed by Cherkis–Kapustin, whose formula for larger k was conjectured by Ivanov–Roček via the Lindström–Roček generalized Legendre transform and computed explicitly by Cherkis–Hitchin): any ALF-D_k instanton must be exactly (isometric to) the metric constructed by them. The paper proves partial progress, Main Theorem 3: there exists a holomorphic map from the twistor space of M to the total space of the O(4) bundle over CP^1 commuting with both the projection to CP^1 and the real structure (existence of the O(4) multiplet).

**判定理由**：Unsolved community conjecture explicitly adopted by this paper as target; the paper contributes the O(4)-multiplet step (Main Theorem 3) but not the conjecture.

**关联卡**：Special case k = 0 is the Atiyah–Hitchin metric; no ALF-D_k instantons exist for k < 0 (Biquard–Minerbe, background). Concrete instance of the paper's fundamental question 2 (uniqueness by end structure); partial progress is Main Theorem 3, whose motivating question is the twistor-space card.

### 🟢 `OP-6FA5C5686AAC` — `real_open` | MSC 53C25 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, enumerated fundamental question (2)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Given these end structures, to what extent, do we know these instantons globally and holomorphically? In other words, is gravitational instanton uniquely determined by its end structure?

**自包含改写**：Standing assumptions: (M^4, g) is a connected complete hyperkähler manifold with |Rm|(x) ≤ r(x)^{-2-ε}, r(x) the distance to a fixed base point o, ε > 0 small (say < 1/100); by the paper's Main Theorem 1 such M is asymptotic to one of the standard end models (ALE, ALF-A_k, ALF-D_k, ALG, ALH-splitting, ALH-non-splitting). Open question: is such a gravitational instanton uniquely determined by its end structure (i.e., globally and holomorphically determined by which standard model, with its parameters, it is asymptotic to)? The paper proves partial structural results (compactification of ALG and ALH-non-splitting instantons, Main Theorem 2; existence of the O(4) multiplet for ALF-D_k, Main Theorem 3) but leaves the uniqueness question open in general.

**判定理由**：The paper's own second fundamental question, explicitly left unresolved in general; a well-posed uniqueness question under the stated hypotheses.

**关联卡**：Concrete instance: the ALF-D_k classification conjecture card; ALE case settled by Kronheimer's Torelli-type theorem and ALF-A_k by Minerbe (background). Partial progress in this paper: Main Theorems 2 and 3.

**存疑**：The question is partly programmatic ('to what extent'); the crisp propositional part 'is gravitational instanton uniquely determined by its end structure?' is what is extracted.

### 🟢 `OP-ADEB10C88DB6` — `real_open` | MSC 53C25 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, paragraph after Main Theorem 1 discussing improved decay for ALF and ALH instantons
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We believe that there is a similar self improvement for ALG instantons, but we will leave it for future study.

**自包含改写**：For ALF gravitational instantons the paper (applying Minerbe's work) improves the curvature decay rate to O(r^{-3}) and the asymptotic rate to any δ < 1; for ALH-non-splitting instantons it proves exponential curvature decay |Rm| ≤ Ce^{-μr} and exponential convergence of the metric to the flat model. Belief left open for future study by this paper: an analogous self-improvement of the curvature decay rate and of the asymptotic order holds for ALG gravitational instantons, i.e., complete hyperkähler 4-manifolds with |Rm|(x) ≤ r(x)^{-2-ε} (ε > 0 small, say < 1/100) asymptotic to a standard ALG model (a flat torus bundle over the flat cone C_β with cone angle 2πβ, with (β, lattice Λ = Z|v_1| ⊕ Zτ|v_1|) one of: β = 1, Im τ > 0 (regular); β = 1/2, Im τ > 0 (I_0*); τ = e^{2πi/3}, β = 1/6 (II); τ = e^{2πi/3}, β = 5/6 (II*); τ = i, β = 1/4 (III); τ = i, β = 3/4 (III*); τ = e^{2πi/3}, β = 1/3 (IV); τ = e^{2πi/3}, β = 2/3 (IV*)), improving beyond the order-ε asymptotics given by Main Theorem 1.

**判定理由**：Authors' stated belief explicitly deferred to future study; a mathematical claim about improved asymptotics of ALG instantons, unresolved in this paper.

**关联卡**：Analogues proved in this paper: ALF (curvature decay improved to O(r^{-3}), asymptotic rate to any δ < 1) and ALH-non-splitting (exponential convergence to the flat model, exponential-asymptotics theorem).

**存疑**：'Similar self improvement' is not made precise in the paper: it does not specify whether the expected ALG improvement is polynomial (as for ALF, O(r^{-3})/δ < 1) or exponential (as for ALH).

### 🟢 `OP-E6E51DE6DD28` — `real_open` | MSC 53C25 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, paragraph on the converse problem (after Main Theorem 2)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We do not know whether one can repeat the Hein-Tian-Yau construction for general elliptic surface which is not algebraic.

**自包含改写**：Tian–Yau proved: for a quasi-projective surface M = M̄ ∖ D with M̄ smooth and D a smooth anticanonical divisor with D^2 ≥ 0, M carries a complete Ricci-flat Kähler metric with linear volume growth (ALH). Hein generalized this, constructing ALG gravitational instantons on complements M̄ ∖ D of anticanonical divisors on rational elliptic surfaces. Open question posed by this paper: can the Hein–Tian–Yau construction be repeated for a general compact elliptic surface M̄ (with anticanonical divisor D) which is not algebraic — i.e., does M̄ ∖ D admit a complete Ricci-flat Kähler metric (of ALG/ALH type) obtainable by that construction?

**判定理由**：Explicit 'we do not know' question posed by the authors: a definite unresolved existence/construction problem.

**关联卡**：Instance of the well-known converse problem stated just before it in the text ('Given a compact complex manifold M̄ and D an anti-canonical divisor, do we have complete Ricci-flat Kähler metric on M̄∖D?'), for which Tian–Yau and Hein give affirmative cases; immediately followed by the 'even harder' remark card.

### 🔵 `OP-6A05571AC4FB` — `background_open` | MSC 53C25 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, paragraph beginning 'For the second question'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In ICM 1978, Yau conjectured that every complete Calabi-Yau manifold can be compactified in the complex analytic sense

**自包含改写**：Yau's conjecture (ICM 1978): every complete Calabi-Yau manifold (complete Ricci-flat Kähler manifold) can be compactified in the complex analytic sense, i.e., is biholomorphic to the complement of a divisor in a compact complex manifold. Without curvature decay it fails: Anderson–Kronheimer–LeBrun constructed complete Ricci-flat Kähler manifolds of infinite topological type. This paper verifies the conjecture, under the faster-than-quadratic curvature decay |Rm|(x) ≤ r(x)^{-2-ε} (ε > 0 small, say < 1/100), for ALG and ALH-non-splitting gravitational instantons (Main Theorem 2: M is biholomorphic, for a suitable complex structure a_1I + a_2J + a_3K with (a_1, a_2, a_3) ∈ S^2, to M̄ ∖ D, where M̄ is a compact elliptic surface with a meromorphic function u: M̄ → CP^1 whose generic fiber is a torus, D = {u = ∞} regular if M is ALH, and regular or of type I_0*, II, II*, III, III*, IV, IV* if M is ALG). Haskins–Hein–Nordström verified it in dimension n ≥ 3 for asymptotically cylindrical metrics with exponentially decaying curvature. The conjecture in general remains open.

**判定理由**：Famous conjecture cited as motivation; the paper proves only special cases (ALG and ALH-non-splitting under curvature decay), not the general statement.

**关联卡**：Per no-duplicate rule, merged with its proved special case: this paper's Main Theorem 2 verifies the conjecture for ALG and ALH-non-splitting instantons; also connected to the fundamental question 2 card.

**存疑**：As literally stated (all complete Calabi-Yau manifolds) the conjecture is false by the Anderson–Kronheimer–LeBrun counterexamples; the open content concerns versions with curvature decay assumptions.

### 🟠 `OP-61DA9E8EB0DF` — `method_obstruction` | MSC 53C25 | 难度 easy

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, remark immediately after Main Theorem 1
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> We would like to remark that the curvature condition can not be weaken to $|\mathrm{Rm}|=O(r^{-2})$.

**自包含改写**：The standing curvature hypothesis of Main Theorem 1 — |Rm|(x) ≤ r(x)^{-2-ε}, with r(x) the distance to a fixed base point o and ε > 0 small (say < 1/100) — cannot be weakened to |Rm| = O(r^{-2}): Hein (2012), besides studying ALG and ALH instantons on rational elliptic surfaces, constructed two new classes of hyperkähler metrics on rational elliptic surfaces whose (volume growth, injectivity radius decay, curvature decay) rates are (r^{4/3}, r^{-1/3}, r^{-2}) and (r^2, (log r)^{-1/2}, r^{-2}(log r)^{-1}) respectively; these curvatures do not satisfy |Rm|(x) ≤ r(x)^{-2-ε} and these metrics do not belong to any of the four families ALE, ALF, ALG, ALH. So the faster-than-quadratic decay hypothesis is necessary; no open problem is posed.

**判定理由**：Shows the hypothesis of the classification theorem is necessary via counterexamples; a sharpness remark, not a posed open problem.

**关联卡**：Delimits the sharpness of Main Theorem 1 (the folklore conjecture card): with only |Rm| = O(r^{-2}) the four-family classification fails.

**存疑**：The counterexamples establishing the obstruction are due to Hein (J. Amer. Math. Soc. 2012), cited by this paper; the paper's contribution is the observation that they obstruct weakening the hypothesis.

### 🔴 `OP-478F5DAD352A` — `solved_in_paper` | MSC 53C26 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 4 (construction of holomorphic functions), subsection 'Twistor space of ALF-D_k instantons', opening paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> A natural question is, is there any relationship between those functions?

**自包含改写**：On an ALF-D_k gravitational instanton M (complete hyperkähler 4-manifold with |Rm|(x) ≤ r(x)^{-2-ε}, tangent cone at infinity R^3/Z_2), the paper constructs, for each compatible complex structure, a quadratic-growth global holomorphic function: an I-holomorphic u_1 + iv_1 asymptotic to (−x_3 + ix_2)^2, a J-holomorphic u_2 + iv_2 asymptotic to 4(x_1^2 − x_2^2) + 8ix_1x_2, and a K-holomorphic u_3 + iv_3 asymptotic to 4(x_3^2 − x_1^2) − 8ix_3x_1 (x_1, x_2, x_3 coordinates on the standard model R^3). Question: is there any relationship between those functions? Answer proved in the paper: there exist 6 harmonic functions u_i, v_i with 4u_1 = u_2 + u_3 such that z(p, ζ) = (u_1 + iv_1) − (1/2)(v_3 + iv_2)ζ + (1/2)(u_2 − u_3)ζ^2 + (1/2)(v_3 − iv_2)ζ^3 + (u_1 − iv_1)ζ^4 is a holomorphic map from the twistor space Z = M × S^2 (ζ the coordinate on CP^1) to the total space of the O(4) bundle over CP^1, commuting with the real structures (Main Theorem 3; the O(4) multiplet).

**判定理由**：Question posed and answered affirmatively within the paper; it is precisely the content of Main Theorem 3.

**关联卡**：Content of Main Theorem 3, which is partial progress toward the ALF-D_k classification conjecture card.

### 🔴 `OP-D76C3268045C` — `solved_in_paper` | MSC 53C25 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, fourth paragraph (after listing the known ALE/ALF/ALG/ALH examples)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> There is a folklore conjecture that when the curvature decay fast enough, any gravitational instantons must be asymptotic to one of the standard models of ends.

**自包含改写**：Let (M^4, g) be a connected complete hyperkähler manifold (a gravitational instanton) whose curvature satisfies |Rm|(x) ≤ r(x)^{-2-ε}, where r(x) is the Riemannian distance to a fixed base point o and ε > 0 is any small positive number, say < 1/100. Folklore conjecture: such M must be asymptotic to one of the standard models of ends, i.e., there exist a bounded domain K ⊂ M, a standard T^k-invariant end model (E, h) over a cone, and a diffeomorphism Φ: E → M∖K with Φ*g = h + O'(r^{-δ}) for some δ > 0 (O'(r^α) meaning all m-th derivatives are O(r^{α-m})). The paper proves this as Main Theorem 1: M is asymptotic to the standard metric of order ε, and consequently M is one of the four families ALE, ALF, ALG, ALH.

**判定理由**：Folklore conjecture explicitly posed and then proved by this paper as Main Theorem 1 (via the ALH-splitting, ALE, and standard-fibration theorems).

**关联卡**：Coincides with the paper's enumerated 'fundamental question 1' (differential and metric structure of the end); sharpness of the hypothesis is treated in the method_obstruction card about |Rm| = O(r^{-2}).

### ⚪ `OP-E1F0722C1940` — `future_application` | MSC 53C25 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, final sentence of the paragraph on the converse problem
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The complete understanding of ALG and ALH-non-splitting gravitational instantons is even harder.

**自包含改写**：Not a mathematical proposition: a value judgement by the authors that complete understanding (e.g., classification/uniqueness) of ALG and ALH-non-splitting gravitational instantons — complete hyperkähler 4-manifolds with |Rm|(x) ≤ r(x)^{-2-ε} (ε > 0 small, say < 1/100) asymptotic to the standard ALG / ALH-non-splitting end models — is harder than the converse/construction direction (Tian–Yau, Hein). No precise problem is posed.

**判定理由**：Taste/difficulty comment, not a proposition; per discipline rules it must not be taskified.

**关联卡**：Adjacent sentence to the Hein–Tian–Yau non-algebraic elliptic surface question card.


## `1701.00018` — The KPZ fixed point
- 权威出处：**Acta Mathematica** 2021，DOI `10.4310/acta.2021.v227.n1.a3`
- 连接方式：`doi`｜全文 250,475 字符 via `cache-latex`｜提取模式 `fast`

### 🟢 `OP-7019B2DB0365` — `real_open` | MSC 60K35 | 难度 medium

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Remark 'Domain Markov property', Section 4.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> One expects that $\mathcal{G}_{\partial\tsm A}$  actually equals $\sigma(\{ \fh(\ft,\fx), (\ft,\fx)\in \partial\tsm A\})$, but it is not immediately clear how to prove this.

**自包含改写**：For the KPZ fixed point h(t,x) on (t0, infinity) x R and a connected open subset A with regular boundary, the germ field G_{∂A} (defined as the intersection over open O ⊇ ∂A of sigma{h(t,x): (t,x) ∈ O}) is expected to equal sigma{h(t,x): (t,x) ∈ ∂A}, the sigma-algebra generated by the field on the boundary itself; no proof is given.

**判定理由**：Explicit expected mathematical identity left open by the paper.

**关联卡**：This sharp version would also give a stronger locality statement, per the Remark 'Locality'.

### 🟢 `OP-910388D1495B` — `real_open` | MSC 60K35 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Example 'Airy sheet', Section 4.4
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> While our methods leave open the question of uniqueness, this has been proved since the present article was submitted in \cite{dov}, see Rem. \ref{rem:dov}.

**自包含改写**：Uniqueness of the Airy sheet: subsequential 1:2:3-scaled limits of the TASEP Airy sheets A^eps(x,y) = h(1,y; -|·-x|) (TASEP height at y, time 1, from packed particles left of x, rescaled and recentered) exist and satisfy the variational formula h(t,x;h0) = sup_y{t^{1/3}A(t^{-2/3}x, t^{-2/3}y) - (x-y)^2/t + h0(y)}, but this paper's methods leave open whether the limit is unique. The paper notes uniqueness was subsequently proved in [Dauvergne-Ortmann-Virág].

**判定理由**：Genuine open question at the paper's time of writing; the paper itself records a later solution appeared after submission.

**关联卡**：The paper cites [dov] as having since proved uniqueness; current_status left for the tracking stage.

**存疑**：Paper explicitly states the problem was solved in a cited later work after submission.

### 🟢 `OP-94752AB7E2F1` — `real_open` | MSC 60K35 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Remark 'Uniqueness and strong KPZ universality conjectures', Section 4.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The KPZ fixed point is expected to be the unique non-trivial (i.e. non-zero) space-time field satisfying locality in the sense of \eqref{locality} and Thm.\,\ref{thm:sym}(\ref{123a},\ref{str},\ref{sis})  (the inviscid limit given by \eqref{eq:invbur} satisfies all but \eqref{str}).

**自包含改写**：Uniqueness conjecture for the KPZ fixed point: the KPZ fixed point is the unique non-trivial (non-zero) space-time field satisfying (a) locality in the sense that |P_{h0}(h(t,x_i) <= a_i, i=1,...,M) - P_{h0^delta}(h(t,x_i) <= a_i, i=1,...,M)| = o(t) as t -> 0 whenever h0, h0^delta are in the space UC of upper semicontinuous functions h: R -> [-infty,infty) with h(x) <= alpha + gamma|x| for some alpha, gamma < infinity and h0^delta(y) = h0(y) for |y - x_i| < delta for one of the i; and (b) the 1:2:3 scaling invariance, skew time reversibility, and stationarity in space symmetries. The inviscid Hopf-Lax solution satisfies all but skew time reversibility.

**判定理由**：A genuine expected-but-unproven uniqueness proposition posed by this paper as its own open target.

**关联卡**：Related to the locality estimate card; the locality bound proved here is evidence toward uniqueness.

### 🟢 `OP-CDE3D6B5EB23` — `real_open` | MSC 60K35 | 难度 medium

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Remark 'Locality', Section 4.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> More concretely, one could ask whether
\begin{equation}\label{locality}
\big|\pp_{\fh_0}(\fh(\ft,\fx_i) \le \fa_i, i=1,\ldots,M ) -\pp_{\fh_0^\delta}(\fh(\ft,\fx_i) \le \fa_i, i=1,\ldots,M )\big|=o(\ft)
\end{equation}
 as $\ft\to 0$
whenever $\fh_0^\delta\in\UC$ is such that $\fh^\delta_0(\fy) = \fh_0 (\fy)$ for $|\fy-\fx_i|<\delta$ for one of the $i$.

**自包含改写**：Question: for the KPZ fixed point h(t,x) with initial data h0, h0^delta in UC (upper semicontinuous h: R -> [-infty, infinity) with h(x) <= alpha + gamma|x|), with h0^delta(y) = h0(y) for |y - x_i| < delta for one of the observation points x_i, is |P_{h0}(h(t,x_i) <= a_i, i=1,...,M) - P_{h0^delta}(h(t,x_i) <= a_i, i=1,...,M)| = o(t) as t -> 0? The paper shows the left hand side is bounded by exp{-C delta^3 / t^2} via the variational formula, providing a strong locality statement, but the o(t) asymptotic itself is not established.

**判定理由**：A concrete posed question (the o(t) asymptotic); the paper proves a related exponential bound but not this precise statement.

**⚠️ 人工复核标记**：The paper proves exp{-C delta^3/t^2}, which is stronger for fixed delta but does not directly give o(t) uniformly; the exact o(t) question appears genuinely open here.

**关联卡**：Feeds into the uniqueness conjecture card.

### 🔵 `OP-49D3AB904ADC` — `background_open` | MSC 60K35 | 难度 hard

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1 (Introduction)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> These issues of the universality of the KPZ equation and its distributions comprise the \emph{weak KPZ universality conjecture}.

**自包含改写**：The weak KPZ universality conjecture: the KPZ equation ∂_t h = λ(∂_x h)^2 + ν∂_x^2 h + σξ (ξ space-time white noise), obtained from microscopic models via weakly asymmetric / intermediate disorder limits, is universal in the sense that its distributions (exact one-point distributions known for special initial data) describe the weak-asymmetry scaling limits across models in the KPZ class.

**判定理由**：Famous conjecture cited as background/motivation; not a target of this paper.

### 🔵 `OP-DACAF8477B8E` — `background_open` | MSC 60K35 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1 (Introduction) and Remark 'Uniqueness and strong KPZ universality conjectures' in Section 4.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The \emph{strong KPZ universality conjecture} states that the KPZ fixed point is the limit under the 1:2:3 scaling of all models in the KPZ universality class.

**自包含改写**：The strong KPZ universality conjecture: every model in the KPZ universality class (loosely characterized by (1) local dynamics, (2) a smoothing mechanism, (3) slope-dependent (lateral) growth rate, (4) space-time random forcing with rapid decay of correlations) converges, under the KPZ 1:2:3 scaling eps^{1/2} h(eps^{-3/2} t, eps^{-1} x) - C_eps t, to the KPZ fixed point constructed in this paper. The paper proves this only for TASEP.

**判定理由**：A famous wide-open conjecture explicitly called 'still wide open'; this paper proves only the TASEP case and provides evidence, not the general statement.

**关联卡**：The paper's Thm. (Convergence of TASEP) proves the conjecture only for TASEP; the conjecture itself remains open for other models.

### 🟠 `OP-5F2D51C6191F` — `method_obstruction` | MSC 60H15 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Footnote 21, Section 3 (Remark after eq. for rescaled TASEP height function)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It was recently proposed that the KPZ fixed point is given by $\partial_t h =  \lambda(\partial_x h)^2 -\nu(-\partial_x^2)^{3/2} h + \nu^{1/2}(-\partial_x^2)^{3/4}\xi$, $\nu>0$, the evidence being that formally it is invariant under the 1:2:3 KPZ scaling \eqref{123} and it preserves Brownian motion.  
Besides the non-physical non-locality, and the inherent difficulty of making sense of this equation,  one can see that it is \emph{not} correct because it has \emph{two} free parameters  instead of one.

**自包含改写**：The proposal that the KPZ fixed point is given by the non-local SPDE ∂_t h = λ(∂_x h)^2 - ν(-∂_x^2)^{3/2} h + ν^{1/2}(-∂_x^2)^{3/4} ξ, ν > 0, with ξ space-time white noise, is refuted as stated: the KPZ fixed point has one free parameter (λ) whereas the equation has two (λ and ν). The paper speculates it may converge to the KPZ fixed point as ν ↘ 0, possibly with renormalized λ.

**判定理由**：The paper demonstrates a proposed characterization fails (two free parameters instead of one) rather than posing an open problem.

**关联卡**：The locality Remark suggests such non-local SPDEs could be differentiated from the true fixed point via the locality estimate.

### 🟠 `OP-6A1EAB7918D9` — `method_obstruction` | MSC 60K35 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Remark after Lemma balkk, Appendix B (Trace norm convergence of the rescaled TASEP kernels)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Examining the argument, it is not hard to see that one should be able to get away with $\g(\fx) \ge -\gga - \g |\fx|^2$ if $\g$ is sufficiently small, depending on $\ft$.
From the variational formula \eqref{eq:var} it is clear that $\g=1/\ft$ is the physical barrier, but in fact the above argument breaks down at $\g= c/\ft$ with $c\approx 0.9$.
In fact, for $c/\ft <\g<1/\ft$ one has to do a very fine estimate on an oscillatory integral in order to control things.

**自包含改写**：The trace norm estimates for the approximating TASEP kernels are proved for initial data satisfying g(x) >= -alpha - gamma|x| (linear growth). Extending to quadratic lower bounds g(x) >= -alpha - gamma|x|^2 with gamma sufficiently small depending on t should be possible; the variational formula shows gamma = 1/t is the physical barrier (explosion), but the paper's argument breaks down already at gamma = c/t with c ≈ 0.9, requiring for c/t < gamma < 1/t a very fine estimate on an oscillatory integral. This extension is not pursued.

**判定理由**：The paper identifies where its method of trace norm estimation fails (gamma between ~0.9/t and 1/t) without formally posing an open problem.

**⚠️ 人工复核标记**：Note also Section 3.1 footnote: extending state space UC to h(x) <= alpha + gamma0|x|^2 up to time t = gamma0^{-1} is stated as possible 'with work' — related extension not carried out.

### 🟠 `OP-FCBEF195B282` — `method_obstruction` | MSC 60K35 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Example 'Airy sheet', Section 4.4 (Variational formulas)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The KPZ fixed point formula does \emph{not} give explicit joint probabilities $\pp(\aip(\fx_i,\fy_i)\le \fa_i, i=1,\ldots,m)$ for the Airy sheet, and we presently have no method to obtain them.

**自包含改写**：The paper's formulas do not yield explicit joint distributions P(A(x_i,y_i) <= a_i, i=1,...,m) of the Airy sheet A(x,y) := h(1,y; d_x) + (x-y)^2 (the KPZ fixed point at time 1 from a narrow wedge at x, plus parabola); the most general accessible formula is P(A_hat(x,y) <= f(x)+g(y), x,y ∈ R) = det(I - K^{hypo(-g)}_{1/2} K^{epi(f)}_{-1/2}) with A_hat = A - (x-y)^2, which for two (x_i,y_i) pairs only spans a 3-dimensional subspace of R^4 and does not determine the joint law.

**判定理由**：States that a method/explicit formula is lacking rather than posing a well-defined decidable proposition.

**关联卡**：Related to the Airy sheet uniqueness card; the directed landscape of [dov] later constructs the sheet non-explicitly.

### ⚪ `OP-AFB5A6B8D5F9` — `future_application` | MSC 60K35 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 2.4 (Integrability), footnote
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> One also has a formula for two-sided initial data, but because of the analytic extension it is cumbersome, and the proof is quite lengthy; moreover, it is not clear to us yet that the formula can be used for asymptotics. We leave it to a future paper.

**自包含改写**：A Fredholm determinant formula for the multipoint distribution of the TASEP height function with fully two-sided (not right-finite) initial data exists but is deferred: the authors state the formula is cumbersome due to an analytic extension, its proof lengthy, and its usefulness for asymptotics unclear, and leave its treatment to a future paper.

**判定理由**：A deferred research direction/announcement of future work, not a mathematical proposition posed here.

**关联卡**：Also referenced in Appendix B: the first-version two-sided formula 'does not seem to be usable' for trace norm control.

### ⚪ `OP-DD9B4E0CD003` — `future_application` | MSC 60K35 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Remark after Proposition 'Hölder 1/3− regularity in time', Section 4.5
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It should be measured instead in $\UC$, which we leave for future work.

**自包含改写**：Time continuity of the KPZ fixed point at t = 0 for non-Hölder-1/2 initial data (e.g., narrow wedge, where h(0,x) = -∞ for x ≠ 0 while h(t,x) > -∞) is not captured by pointwise Hölder estimates; the authors state measuring continuity at t = 0 in the UC (local hypograph/Hausdorff) topology is left for future work.

**判定理由**：Outlook on future work, not a sharply posed mathematical proposition.


# Inventiones Mathematicae

## `2107.14566` — On small breathers of nonlinear Klein-Gordon equations via exponentially small homoclinic splitting
- 权威出处：**Inventiones mathematicae** 2025，DOI `10.1007/s00222-025-01327-y`
- 连接方式：`doi`｜全文 324,938 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟢 `OP-05B083252BD8` — `real_open` | MSC 35L71 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction (Section 1), numbered comments on Theorem T:1, item 3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Theorem \ref{T:1} is only concerned with small {\it single-bump-in-$x$} breathers and it does not rule out possible small 
periodic-in-$t$ solutions which decay as $|x| \to \infty$ but with multiple bumps.

**自包含改写**：For the semilinear Klein-Gordon equation ∂_t²u − ∂_x²u + u − (1/3)u³ − f(u) = 0 with f in an open dense subset 𝒰 of F_r (real-analytic odd f(u)=Σ_{k≥2}f_k u^{2k+1}, Σ|f_k|r^{2k+1}<∞, r>0 fixed), the paper proves (Theorem T:1) that for every σ ∈ (0,1) there is ρ*>0 such that no (2π/ω)-periodic-in-t solution decaying to 0 as |x|→∞ (i.e. ||u(x,·)||_{H¹_t(−π/ω,π/ω)} + ||∂_x u(x,·)||_{L²_t(−π/ω,π/ω)} → 0) that is σ-single-bump in the ℓ₁ norm (i.e. NOT admitting x₁<x₂<x₃<x₄<x₅ with max_{j₁∈{1,3,5}}||u(x_{j₁},·)||_{ℓ₁} ≤ σ min_{j₂∈{2,4}}||u(x_{j₂},·)||_{ℓ₁}) and satisfying sup_x ||u(x,·)||_{ℓ₁} < min{1, ρ* ω^{1/2}} can exist. OPEN QUESTION left by the paper: can such small (sup_x ||u||_{ℓ₁} < min{1, ρ*ω^{1/2}}), time-periodic, spatially decaying solutions with multiple bumps in x (σ-multi-bump for some σ∈(0,1)) exist? The paper's Theorem T:main(2c) reduces existence of any small breather to whether the special weak-unstable/weak-stable solutions u_wk^u, u_wk^s (of size O(ε k^{-1/2})) remain small for all x and coincide after a translation in x; the exponentially small splitting is controlled only at the manifolds' first crossing (x=0), so intersections at later crossings — multi-bump breathers — are not excluded.

**判定理由**：Paper explicitly flags that its nonexistence theorem does not cover multi-bump small breathers; their existence/nonexistence for generic f is a well-defined decidable question left open.

**关联卡**：Echoed after Theorem 2.1 (maintheorem): the splitting is measured only at the first crossing with the section Σ, which 'does not exclude intersections at further crossings and thus existence of multi-bump breathers'; connected to the scattering-map outlook card.

### 🟢 `OP-78F89CDC47C5` — `real_open` | MSC 34E17 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 'The Stokes constant' (sec:Stokes), subsection 'A conjecture on the Stokes constant' (SS:Stokes), final Conjecture environment
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> \begin{conjecture}The constant $C_{\mathrm{in}}$ introduced in Theorem \ref{T:main} 
can be expressed as 
\[
C_{\mathrm{in}}
= - \pi \sum_{l=3}^\infty \frac {i^{l-1} \mu_3^{l-2}}{(l-1)!} 
\beta_{3,l}.
\] 
\end{conjecture}

**自包含改写**：Fix r>0 and let f belong to F_r, the Banach space of real-analytic odd functions f(u)=Σ_{k≥2} f_k u^{2k+1} on {|u|<r} with norm ||f||_r = Σ_{k≥2}|f_k| r^{2k+1} < ∞ (so f(u)=O(u^5) near 0). Consider the inner equation ∂_z²φ⁰ − ∂_τ²φ⁰ − φ⁰ + (1/3)(φ⁰)³ + f(φ⁰) = 0 for functions 2π-periodic and odd in τ, φ⁰ = Σ_{n≥1} φ⁰_n(z) sin(nτ). It admits (Theorem 'Inner' of the paper) solutions φ⁰,ᵤ and φ⁰,ₛ of the form −(2√2 i / z) sin τ + O(z⁻³) in the sectorial domains D^{u,in}_{θ,κ} = {z ∈ ℂ : |Im z| > tan θ · Re z + κ} and its reflection (0<θ<π/6, κ≥κ₀); their difference along the negative imaginary axis satisfies φ⁰,ᵤ(z)−φ⁰,ₛ(z) = e^{−iμ₃z}(C_in sin 3τ + O(1/z)), with μ₃ = √(3²−1) = 2√2, which defines the Stokes constant C_in = C_in(f) ∈ ℂ (analytic in f, nonzero on an open dense subset of F_r, both proven in the paper). Writing the mode equations as d²/dz² φ⁰₁ − (1/4)(φ⁰₁)³ = F₁(φ⁰) and d²/dz² φ⁰_n + μ_n² φ⁰_n = F_n(φ⁰) for n ≥ 3, μ_n = √(n²−1), where F_n contain the higher-order nonlinear terms, let F₃(φ⁰,ᵤ or ₛ)(z) ~ Σ_{j≥3} β_{3,j} z^{−j} (as |z|→∞ in suitable sectors) denote the associated formal Gevrey-1 series with coefficients β_{3,j}. CONJECTURE (left open): C_in = −π Σ_{l=3}^{∞} (i^{l−1} μ₃^{l−2}/(l−1)!) β_{3,l}, with μ₃ = 2√2. The paper states 'The proof of this conjecture is beyond this paper' and notes that, if proved, it would give an algorithm to compute C_in implementable by numerical computations.

**判定理由**：Explicitly labeled Conjecture; the paper says its proof 'is beyond this paper'. A definite identity for the Stokes constant — a genuine open proposition posed by this paper.

**⚠️ 人工复核标记**：The coefficients β_{3,l} are introduced only heuristically as coefficients of the formal Gevrey-1 series of the third-mode nonlinearity F₃ evaluated along φ⁰,ᵤ/φ⁰,ₛ (derived from a linear toy model and Borel–Laplace/resurgence heuristics); well-definedness of this coefficient sequence and the series identity is part of what the conjecture requires.

**关联卡**：Addresses the remark (Section 1, remarks item 1) that 'No simple closed formula has been identified for C_in in the literature'; complements the computer-assisted-verification outlook and the proven generic nonvanishing of C_in (Theorem prop:Stokesconstant).

**存疑**：Extraction based on the provided source, in which ~65,000 characters of mid-paper proofs were omitted; any statements there could not be checked.

### 🔵 `OP-7E6FF740CF8A` — `background_open` | MSC 35L71 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, Section 1.1, background discussion on integrability and breathers
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It is   a fundamental question to assert whether the  existence of breathers is a special phenomenon due to the integrability or it occurs more generally.

**自包含改写**：Background question (cited as motivation, not this paper's own target): whether spatially localized, time-periodic solutions (breathers) of nonlinear dispersive PDEs exist only as a consequence of complete integrability — e.g. the sine-Gordon equation ∂_t²u − ∂_x²u + sin(u) = 0 with its explicit breathers u^ω(x,t) = 4 arctan((m/ω)·sin(ωt)/cosh(mx)), m,ω>0, m²+ω²=1 — or whether they occur more generally in non-integrable models; the cited literature (Kruskal–Segur, Segur, Denzler, Birnir–McKean–Weinstein, etc.) indicates breather existence for non-integrable nonlinear wave equations is expected to be rare. The present paper resolves only the small-amplitude, single-bump, generic analytic odd nonlinearity case (Theorem T:1); the general question remains open.

**判定理由**：Famous general question cited as background/motivation; the paper's own target is only the small-amplitude single-bump generic portion.

**关联卡**：The paper's Theorem T:1 resolves the small-amplitude single-bump generic case; the small multi-bump case is left open (see multi-bump card).

### 🟠 `OP-736B8D934C53` — `method_obstruction` | MSC 35L71 | 难度 easy

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, Section 1.1, discussion following the rigidity results of Denzler and Birnir–McKean–Weinstein
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Even though for small amplitude, \eqref{kleingordonrev} might also be viewed as close to \eqref{sinegordon} in the $C^\infty$ class, 
it does not help much in the analysis of the exponential small obstruction to the existence of breathers (see Theorem \ref{T:main} below) since the nonlinearity of the former is not a perturbation to that of the latter in the analytic function class.

**自包含改写**：For small amplitudes, the Klein-Gordon equation ∂_t²u − ∂_x²u + u − (1/3)u³ − f(u) = 0 (f real-analytic odd, f(u)=O(u^5) near 0) is close to the sine-Gordon equation ∂_t²u − ∂_x²u + sin(u) = 0 in the C^∞ class (their Taylor expansions at u=0 agree through the cubic term); the paper notes that this C^∞ closeness does not help in analyzing the exponentially small obstruction to breather existence, because u − (1/3)u³ − f(u) is not a perturbation of sin u in the analytic function class — i.e., the analyticity hypothesis needed for perturbative/rigidity approaches to exponentially small phenomena is absent. Stated limitation of an approach; no open problem posed.

**判定理由**：Paper explains why the natural C^∞-perturbative viewpoint (closeness to sine-Gordon) fails: the perturbation is not analytic; no problem posed.

### 🟠 `OP-D0E81FC9A6B5` — `method_obstruction` | MSC 34E15 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, Section 1.3 (SS:BT-bifur), discussion of the eigenvalue-collision mechanism
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> However, if there are fast elliptic/oscillatory directions (as happens for the Klein-Gordon equation \eqref{eq:KLGtau}), then there does not necessarily exist a slow manifold and one cannot reduce $(P_{\al})$ to 2 dimensions.

**自包含改写**：In the general N-dimensional (N ≤ ∞) one-parameter system (P_α), α ∈ I ⊂ ℝ, with a steady state at 0 undergoing 'eigenvalue collision' at α=0 (exactly two eigenvalues ±λ(α) ~ ±√α near 0 crossing from the imaginary to the real axis), Bogdanov–Takens-type normal form ü − λ(α)²u + u^m = 0 (m ≥ 2) on the 2-dimensional eigenspace M, and a locally positive-definite first integral on the center manifold: if the fast dynamics transverse to M is hyperbolic, standard normally-hyperbolic invariant manifold theory gives a persistent 2-dimensional slow manifold M_α for 0 < α ≪ 1 and the analysis reduces to 2 dimensions; however, in the presence of fast elliptic/oscillatory directions — as for the Klein-Gordon spatial dynamics ω²∂_τ²u − ∂_x²u + u − (1/3)u³ − f(u) = 0 — a slow manifold need not exist and no 2-dimensional reduction is possible, forcing the search for intersections of low-dimensional stable/unstable manifolds in the full phase space (highly unlikely by dimension counting). Stated obstruction motivating the paper's inner-equation approach; no formal open problem posed.

**判定理由**：Paper states the standard normally-hyperbolic/slow-manifold reduction fails in the oscillatory (Klein-Gordon) regime; an obstruction, not a posed problem.

**关联卡**：This is the obstruction the paper overcomes via the outer parameterizations, inner equation, and matching (Theorems outerthm, innerthm, matchingthm).

### 🟠 `OP-F6221F3F969C` — `method_obstruction` | MSC 35L71 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 'Bifurcation analysis for ω ∈ I_k(ε₀)' (sec:OtherBifs), subsection SS:SU-I-k on local stable/unstable manifolds
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> On the one hand, usually the sizes of the local invariant manifolds are generally determined by the gap between the real parts of the eigenvalues. While $\nu_n \ge k^{-\frac 12}$ for $|n| \le k-1$, the weakest stable/unstable eigenvalues $\pm \nu_k =\OO(\e k^{-\frac 12})$ of \eqref{vnshorter3} are too small for the analysis of possible breathers of amplitude $\|u \|_{\ell_1} = O(k^{-\frac 12})$. On the other hand, the ``angles'' between the stable and unstable eigenfunctions in $\BFX$ of \eqref{vnshorter3} can be rather small for $n\sim k$.

**自包含改写**：For ω = √(1/(k(k+ε²))) ∈ I_k(ε₀), k ≥ 1, 0 < ε ≤ ε₀ ≤ 1/2, the spatial-dynamics Fourier-mode system of ω²∂_τ²u − ∂_x²u + u − (1/3)u³ − f(u) = 0 has eigenvalues ν_n = √(1 − n²ω²), with ν_n ≥ k^{-1/2} for |n| ≤ k−1 but weakest stable/unstable eigenvalues ±ν_k = O(ε k^{-1/2}), and the angles between stable and unstable eigenfunctions in the ℓ₁-based phase space X can be rather small for n ~ k. Consequently, the sizes and bounds on the local invariant manifolds furnished by standard invariant manifold theorems are insufficient for the analysis of possible breathers of amplitude ||u||_{ℓ₁} = O(k^{-1/2}); the paper must (and does) construct the stable/unstable manifolds W^s_ω(0), W^u_ω(0) with uniform estimates via strong stable fibers over a weak stable/unstable manifold (Proposition P:fibers). Stated obstruction; no open problem posed.

**判定理由**：Paper states that standard invariant-manifold theorems yield insufficient manifold sizes/bounds due to the small spectral gap and small angles; obstruction overcome ad hoc, no problem posed.

**⚠️ 人工复核标记**：Symbol check: ν_k = ε(k+ε²)^{-1/2} indeed gives ν_k = O(ε k^{-1/2}) as stated; consistent with the paper's eigenvalue list (E:e-values-1).

**关联卡**：Overcome in the same subsection by the Lyapunov–Perron fiber construction (Proposition P:fibers and Corollary C:fibers-2).

### 🔴 `OP-B9659BE16D53` — `solved_in_paper` | MSC 35L71 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, Section 1.1 (Non-existence of small amplitude breathers), discussion of Kruskal–Segur [KS87]
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> For the past more than thirty years, as far as the authors know, no rigorous justification 
of their leading order exponentially small asymptotics had been given for such nonlinear PDEs. A fundamental part of the proof of Theorem \ref{T:1} is to 
 provide a rigorous proof of  Kruskal and Segur's 
formal argument (for odd analytic nonlinearities) as well as rule out the existence of breathers for other frequencies (either close to other resonances or away from resonances).

**自包含改写**：Kruskal and Segur (1987) formally showed, for a class of nonlinear Klein-Gordon equations, the nonexistence of small O(ε)-amplitude breathers whose temporal frequency ω is ε²-close to the resonant frequency ω=1 (in the present normalization ω=(1+ε²)^{-1/2}, ε≪1), with the obstruction to breather existence exponentially small in ε. The problem of rigorously justifying their leading-order exponentially small asymptotics for such nonlinear PDEs was open for more than thirty years. The present paper proves it for real-analytic odd nonlinearities f(u)=O(u^5): Theorems T:main(2b)/maintheorem(2) identify the leading term (4√2/ε) e^{−√2 π/ε} C_in sin(3τ) of the stable/unstable splitting at the first crossing, with relative error O(1/log(1/ε)), where the Stokes constant C_in(f) is analytic in f and nonzero on an open dense set (Theorem prop:Stokesconstant); the paper also rules out small breathers away from resonances (Theorem T:main(1), ω ∈ J_k(ε₀)) and near all resonances k ≥ 1 (via reduction to the first bifurcation), yielding Theorem T:1.

**判定理由**：Long-standing open problem (since 1987); this paper itself provides the rigorous justification for odd analytic nonlinearities, plus the breather exclusion at all frequencies.

**关联卡**：Implements Theorem T:1 (generic nonexistence of small single-bump breathers) and Theorem T:main(2b)/Theorem maintheorem (splitting asymptotics); the conditional step C_in≠0 is closed by Theorem prop:Stokesconstant.

### ⚪ `OP-1CBE63436F20` — `future_application` | MSC 35L71 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction (Section 1), remarks following Proposition prop:generalized, item 1
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We expect that one should be able to develop a computer assisted proof to check the nonvanishing of $C_\mathrm{in}$ for given nonlinearities (following the ideas developed in \cite{BCGS21}  for a 3-dimensional Hopf-zero bifurcation).

**自包含改写**：NOT a mathematical proposition, but a stated research outlook (explicitly not taskified here): the authors expect that a computer-assisted proof could be developed to verify C_in(f) ≠ 0 for concretely given nonlinearities f in the class F_r of real-analytic odd functions f(u)=Σ_{k≥2}f_k u^{2k+1} with Σ|f_k|r^{2k+1}<∞ (f(u)=O(u^5) near 0), following the ideas of [BCGS21] developed for a 3-dimensional Hopf-zero bifurcation. This would extend the paper's genericity theorem (C_in analytic and nonconstant, hence nonzero on an open dense subset of F_r) to specific nonlinearities.

**判定理由**：Expectation/outlook about a possible computer-assisted proof; not a posed decidable proposition.

**关联卡**：Complements the Conjecture on an explicit formula for C_in; the paper already proves C_in ≠ 0 generically and for an explicit one-parameter family of nonlinearities except a discrete set of parameters, but not for arbitrary concrete f.

### ⚪ `OP-211FEF861CE0` — `future_application` | MSC 35L71 | 难度 frontier

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction (Section 1), remarks following Proposition prop:generalized, item 6
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In the generic case of $C_\mathrm{in}\neq 0$ provided by Theorem \ref{prop:Stokesconstant} which implies that \eqref{kleingordonrev} does not have small breathers, the asymptotic behavior of small solutions in the energy space $H_x^1 (\R) \times L_x^2 (\R)$  is a natural but intriguing question.

**自包含改写**：NOT a single decidable proposition, but a research direction stated by the paper (recorded as such, not taskified): in the generic case C_in(f) ≠ 0 — in which the equation ∂_t²u − ∂_x²u + u − (1/3)u³ − f(u) = 0 (f real-analytic odd, f(u)=O(u^5)) has no small breathers — describe the asymptotic behavior as t → ∞ of solutions with data small in the energy space H¹_x(ℝ) × L²_x(ℝ). The paper argues (same remark, k=1 case) that an exponential time scale is necessarily relevant: truncating the generalized breathers with exponentially small tails (Proposition prop:generalized) by a cutoff at distance O(ε^{-3} e^{√2 π/ε}) in x yields initial data of H¹_x×L²_x norm O(√ε) whose solutions remain time-periodic for |x|,|t| ≤ O(ε^{-3} e^{√2 π/ε}) (propagation speed 1).

**判定理由**：Broad research question flagged 'natural but intriguing'; no specific proposition posed, so recorded as a research direction.

**关联卡**：Relies on the generalized breathers with exponentially small tails constructed in Proposition prop:generalized / prop:FirstBif:Generalized.

### ⚪ `OP-57B4D1C07D86` — `future_application` | MSC 37J40 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, Section 1.3 (SS:BT-bifur), footnote attached to 'splitting distance'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It also sheds light for the future study of scattering maps \cite{DelshamsLS08}
induced by the homoclinic tube and multi-bump homoclinics.

**自包含改写**：NOT a proposition: a research outlook stating that the leading-order approximation of the exponentially small splitting distance between the stable and unstable manifolds (obtained in Theorem T:main(2ab) of the paper) should shed light on the future study of the scattering maps induced by the homoclinic tube (the finite-codimensional family of orbits homoclinic to the center manifold of the spatial dynamics, corresponding to generalized breathers) and on multi-bump homoclinics.

**判定理由**：Footnote outlook on future applications of the splitting asymptotics; not a mathematical proposition.

**关联卡**：The homoclinic tube is the one from Proposition prop:generalized / prop:FirstBif:Generalized; the outlook is directly tied to the open multi-bump breather question.


## `2112.02703` — The amplituhedron BCFW triangulation
- 权威出处：**Inventiones mathematicae** 2025，DOI `10.1007/s00222-025-01316-1`
- 连接方式：`doi`｜全文 436,410 字符 via `cache-latex`｜提取模式 `reasoning`

### 🔴 `OP-08749003B0B1` — `solved_in_paper` | MSC 14M15 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 9 'Consequences', subsection 'The Interior is a Ball', Theorem (thm:int_is_ball); context given in the section's opening paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $Z$ be an arbitrary positive $n\times (k+4)$ matrix. Then the interior of $\Ampl_{n,k,4}(Z)$ is homeomorphic to an open ball.

**自包含改写**：For the tree amplituhedron $\mathcal{A}_{n,k,4}(Z) = \{CZ : C \in \mathrm{Gr}^{\geq}_{k,n}\} \subset \mathrm{Gr}_{k,k+4}$ (in the paper's standing range $k \geq 1$, $n \geq k+4$), where $Z$ is an arbitrary positive $n\times(k+4)$ real matrix (all maximal minors positive): the interior of $\mathcal{A}_{n,k,4}(Z)$ is homeomorphic to an open ball. Before this paper this was known only for one special choice $Z_* = Z_*^{n,k,m}$ (Galashin–Karp–Lam proved $\mathcal{A}_{n,k,m}(Z_*)$ is a closed ball for general $m$); this paper extends it to every positive $Z$ in the case $m=4$, as a consequence of the BCFW triangulation and the injectivity of the amplituhedron map on $\bigcup_{D\in\mathcal{CD}_{n,k}}\overline{S_D}\setminus S_{\partial\mathcal{A}}$.

**判定理由**：Previously open beyond a special Z (Galashin–Karp–Lam); this paper proves it for arbitrary positive Z when m=4.

**⚠️ 人工复核标记**：The theorem statement as printed does not restate the standing parameter range k≥1, n≥k+4; it is inferred from the paper's context. The analogous statement for general m and arbitrary Z is not posed or resolved here.

**关联卡**：Consequence of Card 1's machinery; extends the cited background theorem of Galashin–Karp–Lam (ball for a special Z_*, all m) to all positive Z at m=4.

### 🔴 `OP-4155FCAB9A69` — `solved_in_paper` | MSC 14M15 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), Theorem 1.6 (announced); proved in Section 3, subsection 'The Domino Theorem' (Theorem thm:domino), settling Conjecture A.7 of Karp–Williams–Zhang–Thomas
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Every point in a BCFW cell has a representative matrix in the domino form of that cell. Conversely, every domino matrix represents a point in the corresponding BCFW cell.

**自包含改写**：Conjecture A.7 of Karp, Williams, Zhang and Thomas (Appendix A of 'Combinatorial decompositions of the amplituhedron', 2020), settled by this paper: Let $D \in \mathcal{CD}_{n,k}$ be a chord diagram (a circle with $n$ markers labeled $1,\dots,n$ counterclockwise and $k$ noncrossing increasingly-oriented chords, no chord starting or ending on a marker, no chord starting before marker 1 or ending after marker $n-1$, no chord starting and ending on the same or adjacent segments, and no two chords starting on the same segment), and let $S \subset \mathrm{Gr}^{\geq}_{k,n}$ be its BCFW positroid cell (the cell of the decorated permutation $\pi = (T_1~U_1~V_1~W_1~n)\cdots(T_k~U_k~V_k~W_k~n)$). Then every point of $S$ has a $k\times n$ representative matrix in the domino form of $D$ — row $l$ has variables $(\alpha_l,\beta_l,\gamma_l,\delta_l)$ at the four positions of chord $c_l=(i_l,i_l+1,j_l,j_l+1)$, a fifth variable $\varepsilon_l$ at position $n$ if $c_l$ is a top chord, and an inherited domino $(\varepsilon_l\alpha_m,\varepsilon_l\beta_m)$ at the start positions of its parent $c_m$ otherwise, zeros elsewhere — satisfying the domino sign rules ($\alpha_l>0,\beta_l>0$; $(-1)^{\mathrm{below}(c_l)}\gamma_l>0$ and $(-1)^{\mathrm{below}(c_l)}\delta_l>0$ where below$(c_l)$ is the number of descendants; sign rules on $\varepsilon_l$ via behind$(c_l)=k-l$ or beyond$(c_l)=l-m-1$; $\delta_l/\gamma_l<\delta_m/\gamma_m$ if $c_l$ is a same-end child of $c_m$; $\beta_l/\alpha_l>\delta_m/\gamma_m$ if $c_l$ is head-to-tail after $c_m$); and conversely every matrix in this domino form satisfying the sign rules represents a point of $S$, uniquely up to rescaling each row by a positive number.

**判定理由**：The paper explicitly states 'we settle their Conjecture A.7' and proves it as Theorem thm:domino via the construct-matrix algorithm.

**⚠️ 人工复核标记**：The paper notes its domino sign rules 5 and 6 (the ratio inequalities $\delta_l/\gamma_l<\delta_m/\gamma_m$ and $\beta_l/\alpha_l>\delta_m/\gamma_m$) 'are not explicitly specified' in Karp–Williams–Zhang–Thomas's Appendix A; the exact match between the statement settled here and KWZ's original Conjecture A.7 wording depends on that source.

**关联卡**：Foundational tool for the main theorem (Card 1): domino parametrization of BCFW cells underlies the injectivity, separation, and boundary analysis.

### 🔴 `OP-5D97536D3B16` — `solved_in_paper` | MSC 14M15 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), Conjecture 1.2, attributed to Arkani-Hamed and Trnka; proved via Theorems 1.3–1.5 and Sections 5–8
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> For every $k \geq 1$ and $n \geq k+4$, the cells $\mathcal{BCFW}_{n,k}$ form a triangulation of the amplituhedron $\Ampl_{n,k,4}$.

**自包含改写**：Conjecture (Arkani-Hamed–Trnka 2013): For every integer $k \geq 1$ and $n \geq k+4$, the collection $\mathcal{BCFW}_{n,k}$ of $4k$-dimensional BCFW positroid cells in the nonnegative Grassmannian $\mathrm{Gr}^{\geq}_{k,n}$ (the $\tfrac{1}{k+1}\tbinom{n-3}{k}\tbinom{n-4}{k}$ cells arising from the Britto–Cachazo–Feng–Witten recurrence, equivalently indexed by noncrossing pairs of lattice walks in a $k \times (n-k-4)$ rectangle or by chord diagrams with $n$ markers and $k$ chords) forms a triangulation of the tree amplituhedron $\mathcal{A}_{n,k,4}(Z) = \{CZ : C \in \mathrm{Gr}^{\geq}_{k,n}\} \subset \mathrm{Gr}_{k,k+4}$, where $Z \in \mathrm{Mat}^{>}_{n\times(k+4)}$ is any real $n\times(k+4)$ matrix all of whose maximal $(k+4)\times(k+4)$ minors have positive determinant. Triangulation means, for every such positive $Z$: (i) Injectivity: the map $S \to \tilde{Z}(S)=\{CZ : C\in S\}$ is injective for every cell $S \in \mathcal{BCFW}_{n,k}$; (ii) Separation: $\tilde{Z}(S)$ and $\tilde{Z}(S')$ are disjoint for every two distinct cells $S \neq S'$ in $\mathcal{BCFW}_{n,k}$; (iii) Surjectivity: $\bigcup_{S\in\mathcal{BCFW}_{n,k}} \tilde{Z}(S)$ is an open dense subset of $\mathcal{A}_{n,k,4}(Z)$. This paper proves the conjecture in full, for every $k \geq 1$, $n \geq k+4$ and every positive $Z$.

**判定理由**：The paper's main result: Conjecture 1.2 is proved in full via Theorems 1.3 (injectivity), 1.4 (separation), and 1.5 (surjectivity).

**⚠️ 人工复核标记**：Two notes: (1) Theorem 1.4 as printed reads 'The images $\Z(S)$ and $\Z(S)$ are disjoint', an evident typo for $\Z(S)$ and $\Z(S')$. (2) The provided source omits ~176,410 characters from the middle (Sections 4–7: twistors/functionaries, injectivity, separation, boundary inequalities); any open problems stated there could not be extracted.

**关联卡**：The three triangulation properties are proved as Theorems 1.3–1.5; further consequences proven in the paper: the boundary of A_{n,k,4}(Z) equals the Z-image of the stratum S_{∂A} (Corollary on boundaries), the triangulation is 'good' (internal walls are images of shared boundary strata), and the interior is an open ball (see the card for Theorem thm:int_is_ball).

### ⚪ `OP-02AD69C3C45E` — `future_application` | MSC 81T18 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 9 'Consequences', introductory paragraph of the section (before subsection 'A High-Level Decomposition')
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> A consequence of this decomposition and other tools developed in this work is a mechanism to obtain triangulations of $\Ampl_{n,k,4}(Z)$ from various triangulations of amplituhedra of smaller $k$ and $n$. This includes many more collections of cells beyond those discussed in this work, such as those obtainable from different ways to apply the BCFW recursion. These further results will appear in a separate paper \cite{even2023cluster}.

**自包含改写**：Based on the paper's high-level decomposition of $\mathcal{A}_{n,k,4}(Z)$ (Theorem thm:geom_recursion: for all $k\geq0$, $n\geq k+4$, positive $Z$, the sets $\tilde{Z}(\pre_{n-1}\mathrm{Gr}^{>}_{k,[n]\setminus\{n-1\}})$, $\tilde{Z}(S_{1,n;0,k-1})$, and $\{\tilde{Z}(S_{j,n;k_1,k_2})\}$ over $k_1,k_2\geq0$ with $k_1+k_2=k-1$ and $k_1+2\leq j \leq n-k_2-4$ are disjoint with dense union in $\mathcal{A}_{n,k,4}(Z)$, where $S_{j,n;k_1,k_2}$ are middle-embedding images of products of positive Grassmannians), the authors announce a mechanism to produce triangulations of $\mathcal{A}_{n,k,4}(Z)$ from triangulations of amplituhedra with smaller $k$ and $n$, including many collections of cells beyond $\mathcal{BCFW}_{n,k}$ (e.g., from different ways to apply the BCFW recursion); these further results are deferred to a separate paper. This is an announcement of future work, not a mathematical proposition.

**判定理由**：Announcement of a separate paper deriving new triangulations; application outlook, not a proposition posed or resolved here.

**⚠️ 人工复核标记**：The high-level decomposition theorem itself (thm:geom_recursion) IS proved in this paper; only the further triangulation mechanism is deferred.

**关联卡**：Related to the card on other BCFW-recursion conventions; the underlying decomposition theorem is proven here as part of the paper's results.

### ⚪ `OP-B1F607CD3210` — `future_application` | MSC 81T18 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), in the paragraph defining the BCFW cells $\mathcal{BCFW}_{n,k}$
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> This definition corresponds to a standard way of applying the BCFW recurrence in planar $\mathcal{N}=4$ SYM theory. Other ways are treated in a subsequent paper with Parisi, Sherman-Bennett and Williams.

**自包含改写**：The paper's definition of the BCFW cells $\mathcal{BCFW}_{n,k}$ (the $\tfrac{1}{k+1}\tbinom{n-3}{k}\tbinom{n-4}{k}$ cells of $\mathrm{Gr}^{\geq}_{k,n}$ used to triangulate $\mathcal{A}_{n,k,4}$) follows one standard way of applying the BCFW recurrence in planar $\mathcal{N}=4$ supersymmetric Yang–Mills theory; the treatment of other ways of applying the BCFW recurrence (which yield other collections of positroid cells and, presumably, other triangulations of the m=4 amplituhedron) is deferred to a subsequent paper with Parisi, Sherman-Bennett and Williams. This is a research-direction pointer, not a mathematical proposition.

**判定理由**：Announcement of follow-up work on alternative BCFW-recursion conventions; a research plan, not a decidable proposition posed here.

**关联卡**：Related to the card on the mechanism for further triangulations (both concern cell collections from other BCFW-recursion choices).

### ⚪ `OP-E562359BA4AF` — `future_application` | MSC 14M15 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Remark at the end of Section 7 (boundary pairing analysis), referring to Agarwala–Marcott (agarwala2023cancellation)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Their techniques are very different from ours, but we believe that both techniques can be used to address either problem.

**自包含改写**：The authors state a belief, regarding Agarwala–Marcott's analysis of boundaries and their cancellation for another related physical model (indexed by a different class of chord diagrams/Wilson loop diagrams), that both that paper's techniques and the present paper's techniques can be used to address either problem (i.e., boundary cancellation for both models). This is a belief/taste remark about transferability of methods, not a mathematical proposition.

**判定理由**：A belief comment on cross-applicability of two methods; not a decidable mathematical statement posed by the paper.

**关联卡**：Loosely connected to the techniques-generalization outlook card; both concern exporting the paper's boundary-analysis machinery.

### ⚪ `OP-E937EAD4699E` — `future_application` | MSC 14M15 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), concluding paragraph after the proof overview
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Many of the techniques we develop generalize to other values of~$m$ and other triangulations and families of positroid cells. These are useful for manipulating functions of the amplituhedron's coordinates, showing injectivity of the amplituhedron map, separating between cells, and boundary cancellations.

**自包含改写**：The authors assert that many techniques developed in the paper — matrix operations ($\pre_i$, $\inc_i$, $x_i$, $y_i$, upper/lower embeddings) for recursively constructing positroid cells, and 'functionaries' (polynomials in the amplituhedron's twistor coordinates having constant sign on a cell's image) — generalize to amplituhedra $\mathcal{A}_{n,k,m}$ with values of $m$ other than 4, and to other triangulations and families of positroid cells, with applications to manipulating functions of the amplituhedron's coordinates, injectivity of the amplituhedron map, separation of cells, and boundary cancellations. This is an outlook/value statement, not a mathematical proposition.

**判定理由**：Taste/outlook comment on generality of methods; not a posed proposition with hypotheses and conclusion.

**关联卡**：Complements the cards on other BCFW conventions and on the announced separate paper on further triangulations.


## `2310.07926` — Dimension-free discretizations of the uniform norm by small product sets
- 权威出处：**Inventiones mathematicae** 2025，DOI `10.1007/s00222-024-01306-9`
- 连接方式：`doi`｜全文 89,836 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟢 `OP-C67F83E8339A` — `real_open` | MSC 41A17 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 2, subsection 'Sharp degree-dependence of the constant' (Question environment)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> What is the optimal dependence on $K$ in the constant in \eqref{ineq:remez-plain} of Theorem \ref{thm design}?

**自包含改写**：Question posed by this paper. Setting of Theorem 1: n ≥ 1, K ≥ 2, Y_n = ∏_{j=1}^n Z_j with each Z_j ⊂ D (complex unit disc) of cardinality K, uniformly separated via η = min_{1≤j≤n} min_{z≠z′∈Z_j} |z−z′| > 0 (η is necessarily bounded above since K points lie in D). Inequality (1.6): for every analytic polynomial f : D^n → C of total degree at most d and individual degree (max degree in any single variable) at most K−1, ‖f‖_{D^n} ≤ C(d,K)‖f‖_{Y_n}, where C(d,K) = C(K,η)^d; moreover C(d,K) ≤ (O(log K))^{2d} when all Z_j = Ω_K = {e^{2πik/K} : k = 0,…,K−1}. The paper proves exponential dependence on d is necessary (for Y_n = Ω_K^n, a univariate extremizer g of ‖g‖_T = C(K)‖g‖_{Ω_K} with C(K) > 1 for K ≥ 3, tensored as f(z) = ∏_{j=1}^{d/(K−1)} g(z_j), assuming K−1 divides d, forces C(d,K) ≥ D(K)^d with D(K) = C(K)^{1/(K−1)}, and this D(K) does not grow in K). Open question: what is the optimal dependence on K of the constant in (1.6) — can the (log K)^{2d} upper bound be improved toward the bounded-in-K lower bound D(K)^d?

**判定理由**：Formally posed Question by this paper; its own upper bound (O(log K))^{2d} and lower bound D(K)^d (D(K)>1 bounded in K) leave the optimal K-dependence genuinely unresolved.

**关联卡**：Introduced by the preceding sentence: 'It remains an interesting question to determine the optimal $K$-dependence of the constant in \eqref{ineq:remez-plain}.' Concerns the constant of the discretization inequality proved in this paper (inequality (1.4) card); the d-dependence is shown tight in the paper, only the K-dependence is open.

### 🟢 `OP-F0974E9A7D71` — `real_open` | MSC 46G25 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 2, subsection 'Consequences' (Question environment)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> What is the best constant for the cyclic-group Bohnenblust--Hille, $\mathrm{BH}_{\Omega_K}^{\leq d}$?
    As a starting point, is $\mathrm{BH}_{\Omega_K}^{\leq d}$ subexponential in $d$?

**自包含改写**：Question posed by this paper. Let Ω_K = {e^{2πik/K} : k = 0,1,…,K−1} and let BH_{Ω_K}^{≤d} denote the best (smallest) constant such that for every n ≥ 1 and every polynomial f : Ω_K^n → C of total degree at most d and individual degree (max degree in any single variable) at most K−1, (Σ_{|α|≤d} |f̂(α)|^{2d/(d+1)})^{(d+1)/(2d)} ≤ BH_{Ω_K}^{≤d}‖f‖_{Ω_K^n}, where f̂(α) are the Fourier coefficients and ‖·‖_{Ω_K^n} is the supremum norm. Known at paper time: BH_{{±1}}^{≤d} ≤ C^{√(d log d)} (hypercube, K = 2 [DMP]); BH_T^{≤d} ≤ C^{√(d log d)} (polytorus, K = ∞ [Bayart et al.]); and this paper proves BH_{Ω_K}^{≤d} ≤ (O(log K))^{2d}·BH_T^{≤d}, which is exponential in d for each fixed K ≥ 3. Open: (i) what is the best constant BH_{Ω_K}^{≤d} for intermediate K, 3 ≤ K < ∞; (ii) as a starting point, is BH_{Ω_K}^{≤d} subexponential in d?

**判定理由**：Formally posed Question by this paper for 3 ≤ K < ∞; the paper's bound remains exponential in d for fixed K ≥ 3, so even subexponentiality is unresolved.

**关联卡**：Specializes to cyclic groups the background problem of sharp BH degree-dependence (polytorus/hypercube card); the current best bound is this paper's (O(log K))^{2d}·BH_T^{≤d}.

**存疑**：The Question asks about subexponentiality 'in d' without literally fixing K; the surrounding text (contrast with K = 2 and K = ∞ bounds in d) indicates the regime 3 ≤ K < ∞ with d → ∞.

### 🔵 `OP-7DC1B7D1CFE4` — `background_open` | MSC 46G25 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1 (Introduction and motivation)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The sharp dependence on degree $d$ of the constants in \eqref{eq:og-BH-sketch} and \eqref{ineq:bh-sketch} are longstanding open problems; see \cite{DSP,DMP,Defant_García_Maestre_Sevilla-Peris_2019} for more.

**自包含改写**：Background open problem. Classical Bohnenblust-Hille (BH) inequality: for each d ≥ 1 there exists C(d) independent of the number of variables n such that every n-variate analytic polynomial f of total degree at most d on the polytorus T^n = {z ∈ C : |z| = 1}^n satisfies ‖f̂‖_{2d/(d+1)} ≤ C(d)‖f‖_{T^n} (eq. (1.1)); hypercube analogue: every f : {±1}^n → R of degree at most d satisfies ‖f̂‖_{2d/(d+1)} ≲_d ‖f‖_{{±1}^n} (eq. (1.2)), where f̂ is the sequence of Fourier coefficients and ‖·‖_X is the supremum norm. Open: determine the sharp dependence on d of the best constants in (1.1) and (1.2). At paper time the best known upper bounds were C^{√(d log d)} for the polytorus (Bayart et al.) and for the hypercube (DMP).

**判定理由**：Longstanding open problem about BH constants for the polytorus and hypercube, cited purely as background/motivation; not this paper's own target.

**关联卡**：This paper's comparison BH_{Ω_K}^{≤d} ≤ (O(log K))^{2d}·BH_T^{≤d} reduces the cyclic-group constant question (separate card) to the polytorus case of this background problem.

### 🟠 `OP-01E929C9C002` — `method_obstruction` | MSC 42B05 | 难度 easy

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 2, subsection 'Dimension-free discretization for L^p norms'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Note, however, that such a hypercontractivity argument does not work for $p=\infty$.

**自包含改写**：Methodological remark (no open problem posed). For 2 ≤ p < ∞ and f a degree-d function on Ω_K^n = {e^{2πik/K} : k = 0,…,K−1}^n, hypercontractivity on the polytorus yields the dimension-free L^p discretization chain ‖f‖_{L^p(T^n)} ≲_{d,p} ‖f‖_{L^2(T^n)} = ‖f‖_{L^2(Ω_K^n)} ≤ ‖f‖_{L^p(Ω_K^n)} (L^p norms with respect to uniform probability measures). The paper notes this hypercontractivity argument does not work at the endpoint p = ∞, which is why the uniform-norm (Bernstein-type) discretization of Theorem 1 required the paper's new interpolation-formula approach instead.

**判定理由**：The paper explicitly notes the standard hypercontractivity method fails at p = ∞, without posing an open problem; this motivated its new approach.

**关联卡**：Explains why the uniform-norm comparison (inequality (1.4) card) could not be obtained by the hypercontractivity route that works for finite p.

### 🟠 `OP-25832B7BF9CA` — `method_obstruction` | MSC 41A17 | 难度 easy

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 2, subsection 'Uniform separation'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> In fact, this is unavoidable; uniform separation (\emph{i.e.,} independence of $\eta$ from $n$) is \emph{required} to retain the dimension-freeness of the inequality of Theorem \ref{thm design}.

**自包含改写**：Necessity result proved in the paper (hypothesis demonstration, no open problem posed). In Theorem 1, the discretization ‖f‖_{D^n} ≤ C(K,η)^d‖f‖_{Y_n} (f of total degree ≤ d, individual degree ≤ K−1; Y_n = ∏Z_j, |Z_j| = K, Z_j ⊂ D) has a constant depending on the minimum pairwise separation η = min_{1≤j≤n} min_{z≠z′∈Z_j}|z−z′|. The paper shows this is unavoidable: if Y_n ⊂ D^n are sampling sets with coordinates 1 ≤ c(n) ≤ n whose coordinate projections P_n = {z_{c(n)} : z ∈ Y_n} satisfy |P_n| = K for all n but min_{z≠z′∈P_n}|z−z′| → 0 as n → ∞, then choosing A_n ⊂ P_n with |A_n| = K−1 and excluded point ζ_n^* with min_{ζ∈A_n}|ζ_n^*−ζ| ≤ ε_n → 0, the polynomials f_n(z) = ∏_{ζ∈A_n}(z_{c(n)}−ζ) satisfy ‖f_n‖_{D^n} ≥ 1 while ‖f_n‖_{Y_n} ≤ ε_n·2^{K−2} → 0; hence no discretization constant independent of n exists for such (Y_n)_{n≥1}. Uniform separation (η bounded away from 0 independently of n) is a necessary hypothesis.

**判定理由**：Paper demonstrates via an explicit example that a hypothesis — uniform separation of the Z_j independent of n — is necessary for dimension-free constants; no open problem posed.

**关联卡**：Delimits the hypotheses of Theorem 1 (see inequality (1.4) card); complementary to the open Question on the optimal K-dependence of the constant.

### 🟠 `OP-33EDFC65A3A4` — `method_obstruction` | MSC 46G25 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1 (Introduction and motivation)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> For example, if one tries to prove the BH inequality on $\Om_K^n$ (even for $K=3$) by repeating the argument that worked for both the polytorus and the hypercube, one quickly encounters trouble, as detailed in \cite[Appendix A]{SVZbh}.

**自包含改写**：Methodological obstruction (reported from prior work, no open problem posed here). Bohnenblust-Hille inequality on the discrete n-torus Ω_K^n = {e^{2πik/K} : k = 0,…,K−1}^n, i.e. for polynomials of total degree at most d and individual degree (max degree in one variable) at most K−1: ‖f̂‖_{2d/(d+1)} ≤ BH_{Ω_K}^{≤d}‖f‖_{Ω_K^n}. The paper reports, citing [SVZbh, Appendix A], that repeating the argument which proves BH on the polytorus (K = ∞) and the hypercube (K = 2) encounters trouble already at K = 3; the present paper bypasses this obstruction via discretization/interpolation, proving BH_{Ω_K}^{≤d} ≤ (O(log K))^{2d}·BH_T^{≤d} (improving the constant C(K)^{d^2} previously obtained in [SVZbh]).

**判定理由**：Statement that the standard BH proof method fails on Ω_K^n for K ≥ 3 (documented in cited [SVZbh, Appendix A]); a method-failure report, not a posed problem.

**关联卡**：The goal obstructed here (BH on Ω_K^n with good constants) is advanced by this paper; see the cyclic-group BH constant question card. The obstruction is bypassed, not refuted.

**存疑**：The obstruction itself is documented in the cited prior work [SVZbh, Appendix A], not demonstrated within this paper.

### 🔴 `OP-EB973FB6E323` — `solved_in_paper` | MSC 41A17 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1 (Introduction and motivation), immediately after equation (1.4)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> A proof of the inequality \eqref{ineq:sketch-comparison} and its generalizations are the subject of this work.

**自包含改写**：Paper's main target, proved in the paper. Inequality (1.4): does there exist, for each fixed d ≥ 1 and K ≥ 2, a constant C(d,K) independent of the number of variables n such that ‖f‖_{T^n} ≤ C(d,K)‖f‖_{Ω_K^n} for every analytic polynomial f on T^n = {z ∈ C : |z| = 1}^n of total degree at most d and individual degree (max degree in any single variable) at most K−1, where Ω_K = {e^{2πik/K} : k = 0,…,K−1}? (The paper notes naive attempts give constants exponential in n, and that (1.4) would imply a dimension-free spectral-projection (Figiel-type) bound and the BH inequality on Ω_K^n.) Solved here: Theorem 1 with Z_j = Ω_K for all j gives the stronger statement ‖f‖_{D^n} ≤ (O(log K))^{2d}‖f‖_{Ω_K^n} (D = unit disc), constant independent of n.

**判定理由**：The inequality is explicitly declared 'the subject of this work' and is proven as Theorem 1 with constant (O(log K))^{2d} for the roots-of-unity grid.

**关联卡**：Corollaries proved from it: Figiel-type spectral projection bound on Ω_K^n with constant (O(log K))^{2d}, the cyclic-group BH inequality, a real Remez-type corollary on the grid G_K^n ⊂ [−1,1]^n, and the L^p discretization (Theorem 5). Its optimality in K remains the open Question (separate card).

### ⚪ `OP-2C5B0DFA6A23` — `future_application` | MSC 41A05 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 2, subsection 'A new polynomial interpolation formula'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> As a result the linear combination \eqref{eq:interp} is not unique, and it is interesting to understand whether this flexibility can lead to sharpenings of Theorem \ref{thm design}.

**自包含改写**：Stated research direction, not a formal proposition. The paper's interpolation formula (Theorem 2): if Y_n = ∏_{j=1}^n Z_j with Z_j ⊂ D of cardinality K and separation η = min_{1≤j≤n} min_{z≠z′∈Z_j}|z−z′| > 0, then for each z ∈ D^n there exist coefficients {c_ξ^{(z)}}_{ξ∈Y_n} with Σ_{ξ∈Y_n}|c_ξ^{(z)}| ≤ C(K,η)^d (≤ (O(log K))^{2d} for Y_n = Ω_K^n) such that f(z) = Σ_{ξ∈Y_n} c_ξ^{(z)} f(ξ) for every polynomial f of total degree at most d and individual degree at most K−1. Since |Y_n| = K^n exceeds the dimension of this polynomial space, the representing linear combination is not unique. Direction raised (taste remark): understand whether this flexibility/non-uniqueness can lead to sharpenings of the constant C(d,K) in Theorem 1's discretization ‖f‖_{D^n} ≤ C(d,K)‖f‖_{Y_n}.

**判定理由**：'It is interesting to understand whether…' is a taste remark/research outlook about possible sharpenings, not a decidable proposition posed by the paper.

**关联卡**：Companion to the future-applications remark on the same interpolation formula; if realizable, it would affect the open Question on optimal K-dependence.

### ⚪ `OP-999A54419D8F` — `future_application` | MSC 41A05 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 2, subsection 'A new polynomial interpolation formula'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We hope this interpolation formula can have future applications and offer as a first example usage a short proof of a dimension-free discretization inequality for $L^p$ norms, $1\leq p <\infty$, as we describe next.

**自包含改写**：Application outlook, not a mathematical proposition: the authors hope that the new dimension-free polynomial interpolation formula (Theorem 2: f(z) = Σ_{ξ∈Y_n} c_ξ^{(z)} f(ξ) with Σ_ξ |c_ξ^{(z)}| ≤ C(K,η)^d independent of the number of variables n, valid for degree-d, individual-degree-(K−1) polynomials on product sets Y_n = ∏Z_j ⊂ D^n with |Z_j| = K and separation η > 0) can have future applications beyond those in the paper; as a first example usage the paper derives a dimension-free L^p discretization ‖f‖_{L^p(T^n)} ≤ C(d,K)‖f‖_{L^p(Ω_K^n)} with C(d,K) ≤ d(C_1 log K + C_2)^d for universal C_1, C_2 (Theorem 5, stated for 1 ≤ p ≤ ∞).

**判定理由**：Explicit hope/outlook for future applications of the interpolation formula; an application outlook, not a proposition.

**关联卡**：The announced first usage (L^p discretization) is itself proved in the paper (Theorem 5 in Section 5); note the hope sentence says 1 ≤ p < ∞ while Theorem 5 is stated for 1 ≤ p ≤ ∞.


## `2302.07794` — A priori bounds and degeneration of Herman rings with bounded type rotation number
- 权威出处：**Inventiones mathematicae** 2025，DOI `10.1007/s00222-025-01369-2`
- 连接方式：`doi`｜全文 225,555 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟢 `OP-10CE3F13C346` — `real_open` | MSC 37F10 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 9 'Unicritical Herman curves'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> For every bounded type $\theta$, the uniqueness of the parameter $c(\theta)$ will follow from the sequel \cite{Lim23}, in which we justify combinatorial rigidity.

**自包含改写**：Fix integers d_0, d_infty >= 2, d = d_0 + d_infty - 1, and a bounded type irrational theta in (0,1). For c in C* let F_c(z) := -c (sum_{j=d_0}^{d} binom(d,j) (-z)^j) / (sum_{j=0}^{d_0-1} binom(d,j) (-z)^j), the unique degree-d rational map with critical points at 0, infinity, and 1 of local degrees d_0, d_infty, and d, fixing 0 and infinity, with F_c(1) = c. Existence of a parameter c(theta) with F_{c(theta)} in HQ_{d_0,d_infty,theta} (Herman quasicircle of rotation number theta separating 0 and infinity with all free critical points on it) follows from this paper's realization theorem; the uniqueness of the parameter c(theta), i.e. combinatorial rigidity in this unicritical family, is left open by this paper and deferred to the sequel [Lim23].

**判定理由**：A decidable mathematical statement (uniqueness of c(theta)) explicitly left open here, adopted as the paper's own target via the announced sequel.

**关联卡**：This rigidity would complete the affirmative answer to whether every map in HQ_{d0,d_infty,theta} is a genuine limit of Herman rings (remark-part-2 card).

### 🟢 `OP-45ECAA35EF7D` — `real_open` | MSC 37F10 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 9 'Unicritical Herman curves', Conjecture conj:self-similarity
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> For every stationary type irrational number $\theta = [0;N,N,N,\ldots]$, the non-escaping locus $\mathcal{M}_{d_0,d_\infty}$ is asymptotically self-similar at $c(\theta)$. There is a hyperbolic renormalization operator associated to it.

**自包含改写**：Fix integers d_0, d_infty >= 2, d = d_0 + d_infty - 1. For c in C* let F_c(z) := -c (sum_{j=d_0}^{d} binom(d,j) (-z)^j) / (sum_{j=0}^{d_0-1} binom(d,j) (-z)^j), the degree-d rational map with critical points at 0, infinity, 1 of local degrees d_0, d_infty, d, fixing 0 and infinity, with F_c(1) = c. The non-escaping locus is M_{d_0,d_infty} := {c in C* : F_c^n(1) does not tend to 0 and F_c^n(1) does not tend to infinity}. For a bounded type irrational theta, c(theta) denotes a parameter such that F_{c(theta)} lies in HQ_{d_0,d_infty,theta}. Conjecture: for every stationary type irrational theta = [0; N, N, N, ...] (constant continued fraction digits), M_{d_0,d_infty} is asymptotically self-similar at c(theta), and there is a hyperbolic renormalization operator associated to it.

**判定理由**：Explicitly stated conjecture of this paper; the text itself says it 'remains open'.

**关联卡**：The paper notes numerical evidence (Figure parspace2) and that a follow-up [Lim24] constructs a hyperbolic renormalization operator associated to unicritical Herman curves, while stating that this conjecture remains open.

### 🟢 `OP-56ACFD83972D` — `real_open` | MSC 37F10 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.2 'On Herman curves'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In particular, we conjecture that the limit of degenerating Herman rings of bounded type is always a Herman curve.

**自包含改写**：Conjecture: if a sequence of rational maps with invariant Herman rings of bounded type rotation number degenerates (the conformal moduli of the rings tending to 0), then the limit map always carries a Herman curve, i.e. an invariant Jordan curve not contained in the closure of any rotation domain on which the map is conjugate to a rigid rotation. No restriction to the simplest-configuration space HR_{d_0,d_infty,theta}: the paper proves the statement only for rings in HR_{d_0,d_infty,theta} (where limits lie in HQ_{d_0,d_infty,theta}).

**判定理由**：Explicitly stated conjecture of this paper, going beyond what is proven (only the simplest-configuration case).

**关联卡**：Generalizes the case solved in this paper (Corollary 'limiting': HR*_{d0,d_infty,theta} is contained in HQ_{d0,d_infty,theta}); gives the conjectural bounded-type answer to intro question (1).

### 🟢 `OP-A67DDC6539E2` — `real_open` | MSC 37F10 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 2.2 'Herman quasicircles', same Remark
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We also do not know yet if every rational map in $\HQspace_{d_0,d_\infty,\theta}$ arises as a genuine limit of Herman rings.

**自包含改写**：Let HQ_{d_0,d_infty,theta} (d_0, d_infty >= 2, theta bounded type irrational in (0,1)) be the space of degree d_0+d_infty-1 rational maps having a Herman quasicircle of rotation number theta which separates the superattracting fixed points 0 (local degree d_0) and infinity (local degree d_infty) and contains every critical point other than 0 and infinity. Question: does every f in HQ_{d_0,d_infty,theta} arise as a locally uniform limit of maps in HR_{d_0,d_infty,theta} (rational maps with invariant Herman rings of rotation number theta in the simplest configuration)? This paper proves that limits realize every prescribed combinatorics (the map HR*_{d_0,d_infty,theta} -> C_{d_0,d_infty}, f -> comb(f), is a continuous surjection), but the literal 'every map' statement would additionally require combinatorial rigidity (uniqueness of the HQ-map with given combinatorics), which is deferred to the sequel [Lim23] and not proven here.

**判定理由**：Genuine proposition stated as unknown; Section 8 only proves realization of each combinatorics by some limit map; the full statement needs rigidity deferred to sequel.

**关联卡**：Specific version of intro question (2); complement of the solved remark-part-1 card; resolution requires the c(theta)-uniqueness / combinatorial rigidity card.

**存疑**：The remark says 'Some of these will be resolved in Section 8'; Section 8 resolves this only up to combinatorics (surjection onto C_{d0,d_infty}); deducing that every HQ-map is a limit needs rigidity announced for [Lim23], not proven in this paper.

### 🟢 `OP-C813D8A9A84A` — `real_open` | MSC 37F10 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.2, question (2) of the two 'natural questions'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> When is a Herman curve a limit of degenerating Herman rings?

**自包含改写**：General question: characterize when a Herman curve of a rational map — a forward invariant Jordan curve not contained in the closure of any rotation domain on which the map is conjugate to a rigid rotation — arises as a locally uniform limit of rational maps having invariant Herman rings whose conformal moduli degenerate to 0. The paper proves that any prescribed critical combinatorics (element of the combinatorial space C_{d_0,d_infty}) is realized by such a limit map (Theorem C), and states that a partial answer will be explored in the forthcoming sequel [Lim23]; the general characterization remains open.

**判定理由**：Posed as an open 'natural question'; the paper proves only realization of prescribed combinatorics and defers a partial answer to sequel [Lim23].

**关联卡**：Specific instance (whether every map in HQ_{d0,d_infty,theta} is a genuine limit) is the remark-part-2 card; the combinatorial rigidity needed there is the c(theta)-uniqueness card.

### 🟢 `OP-FB91970D1FE7` — `real_open` | MSC 37F10 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.2, question (1) of the two 'natural questions'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> When is a limit of degenerating Herman rings a Herman curve?

**自包含改写**：General question: given a sequence of rational maps, each possessing an invariant Herman ring, whose ring conformal moduli degenerate to 0 (degenerating Herman rings), characterize when the locally uniform limit map carries a Herman curve, i.e. a forward invariant Jordan curve not contained in the closure of any rotation domain on which the map is conjugate to a rigid rotation. The paper resolves only the special case where the rings lie in the space HR_{d_0,d_infty,theta} (simplest configuration: 0 and infinity superattracting fixed points of local degrees d_0, d_infty >= 2, invariant bounded-type ring of rotation number theta separating them, all other critical points on its boundary), where the limit always has a Herman quasicircle; the general characterization remains open.

**判定理由**：Posed as an open 'natural question' in full generality; only the simplest-configuration case is solved in this paper; the bounded-type general case is conjectured, not proven.

**关联卡**：Special case within HR_{d0,d_infty,theta} is solved in this paper (see remark-part-1 card); the general bounded-type answer is the 'limit of degenerating rings' conjecture card; companion question (2) has its own card.

### 🔵 `OP-B854CCE573BE` — `background_open` | MSC 37F10 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1.1 'On Herman rings' (historical survey of the near-degenerate regime)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> attained substantial progress in the primitive case of the MLC conjecture

**自包含改写**：The MLC conjecture (local connectivity of the Mandelbrot set) is a famous open problem in holomorphic dynamics; the paper cites Kahn-Lyubich's substantial progress in the primitive case purely as historical background on the near-degenerate regime (Quasi-Additivity Law, Covering Lemma). It is not a target of this paper.

**判定理由**：Famous open problem mentioned only as historical background for the near-degenerate method; not this paper's own problem.

### 🟠 `OP-6FFB628EDA7E` — `method_obstruction` | MSC 37F10 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.3 'Outline'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In the Herman scale, the techniques in \cite{DL22}, especially [Snake Lemma 2.12]{DL22}, are not applicable because, unlike in the Siegel scale, the geometry on both sides of $I$ is unknown.

**自包含改写**：In the near-degenerate analysis of a Herman ring of modulus mu (and of Herman quasicircles, mu = 0) with associated curve(s) Hq, a combinatorial piece I subset of Hq is at the Siegel scale if its combinatorial length |I| <= mu and at the Herman scale if |I| > mu. The Dudko-Lyubich techniques for bounded type quadratic Siegel disks [DL22], in particular their Snake Lemma, are not applicable at the Herman scale because, unlike at the Siegel scale, the conformal geometry on both sides of I is unknown. The paper develops replacement machinery (waves, spreading, trading, amplification) instead.

**判定理由**：Documents that a prior method (Dudko-Lyubich Snake Lemma) fails at the Herman scale; no open problem is formally posed.

**关联卡**：Companion method obstruction: Kahn's entropy argument card; both concern the Herman scale where prior near-degenerate tools are unavailable.

### 🟠 `OP-BBEDDDACFF10` — `method_obstruction` | MSC 37F10 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.3 'Outline'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> A key ingredient in the original push-forward argument is the positivity of the core entropy corresponding to primitive renormalization, which stands in contrast to the lack of entropy of the rotational action of $f$ on $\Hq$.

**自包含改写**：Kahn's push-forward argument for a priori bounds of infinitely renormalizable quadratic-like maps relies on positivity of the core entropy corresponding to primitive renormalization. For a rational map f with a Herman quasicircle Hq, the rotational action of f on Hq has no entropy, so this key ingredient is unavailable; the paper develops a replacement (the 'loss of horizontal width' Proposition pos-entropy) in Section 7.

**判定理由**：Documents that Kahn's entropy ingredient is unavailable for rotational dynamics; the paper constructs a replacement; no open problem is posed.

**关联卡**：Companion method obstruction: Dudko-Lyubich Snake Lemma card.

### 🔴 `OP-4B4C46039D6E` — `solved_in_paper` | MSC 37F10 | 难度 medium

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 8.1 'Precompactness', Remark generalization
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> With similar proof, we can show the compactness of the moduli space of rational maps in $\mathcal{X}_{d_0,d_\infty,\theta}$ as well as the moduli space of degree $d$ polynomials having a bounded type Siegel disk whose boundary contains all free critical points.

**自包含改写**：Assertion made without written proof ('with similar proof' to the precompactness Theorem of Section 8.1 for quotient spaces of maps with bounded-type Herman rings of modulus < mu and beta(theta) <= N): (a) the moduli space (up to conformal conjugacy) of rational maps in the space X_{d_0,d_infty,theta} is compact, and (b) the moduli space of degree d polynomials having a bounded type Siegel disk whose boundary contains all free critical points is compact.

**判定理由**：Author asserts these compactness results as shown by the same proof; no proof is written out and no problem is left open.

**⚠️ 人工复核标记**：The symbol X_{d_0,d_infty,theta} is never defined anywhere in the paper (possibly a typo for HQ_{d_0,d_infty,theta} or the union of the HR and HQ spaces); moreover the proofs of both compactness claims are omitted, only asserted as similar to Theorem 'precompactness' — treat 'solved_in_paper' with caution.

**关联卡**：Extends the precompactness theorem for quotient spaces of HR_{d0,d_infty,theta} with bounded rotation number and modulus.

**存疑**：Whether the asserted compactness claims count as proved in this paper is ambiguous since only the technique is indicated.

### 🔴 `OP-5B2164DCB666` — `solved_in_paper` | MSC 37F10 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1.2 'On Herman curves'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Eremenko asked whether or not there exist Herman curves that are not round circles.

**自包含改写**：For a rational map f, a Herman curve of rotation number theta is a forward invariant Jordan curve H not contained in the closure of any rotation domain (Siegel disk or Herman ring) such that f|_H is conjugate to the rigid rotation R_theta on the unit circle; it is a Herman quasicircle if H is a quasicircle, and trivial if it is a round circle or can be obtained from a round circle via quasiconformal surgery. Question (posed by Eremenko at the online conference 'On Geometric Complexity of Julia Sets II', [E20]): do there exist Herman curves that are not round circles, i.e. non-trivial Herman curves?

**判定理由**：The paper adopts and affirmatively answers this question: Theorem C realizes any prescribed critical combinatorics by maps in the limit space, and asymmetric combinatorics yields non-trivial Herman quasicircles.

**关联卡**：Independently answered by Yang Fei [Y22] (cubic map, smooth Herman curve, high type rotation number, positive-area Julia set); the present paper's examples are bounded type Herman quasicircles, generally non-smooth due to critical points.

### 🔴 `OP-CA87B426FA96` — `solved_in_paper` | MSC 37F10 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 2.1 'Herman rings' (goal restated from Section 1.1)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> In this paper, we would like to remove the dependency on the modulus $\mu$ for one of the simplest families of rational maps with Herman rings, namely $\HRspace_{d_0,d_\infty,\theta}$ defined in the introduction.

**自包含改写**：Fix integers d_0 >= 2 and d_infty >= 2 and an irrational theta in (0,1) of bounded type, i.e. beta(theta) := max_i a_i < infinity where theta = [0; a_1, a_2, ...] is its continued fraction expansion. Let HR_{d_0,d_infty,theta} be the space of degree d_0 + d_infty - 1 rational maps f such that: (I) 0 and infinity are superattracting fixed points of f with local degrees d_0 and d_infty; (II) f admits an invariant Herman ring H with bounded type rotation number theta; (III) H separates 0 and infinity; (IV) every critical point of f other than 0 and infinity lies on the boundary of H. Previously the dilatation of the boundary quasicircles of H was known to depend also on the conformal modulus mu = mod(H) (via Shishikura surgery and Zhang's Siegel disk bounds). Goal (proved in this paper as Theorem A): the boundary components of the Herman ring of every map in HR_{d_0,d_infty,theta} are quasicircles with dilatation depending only on d_0, d_infty, and beta(theta).

**判定理由**：The paper's central stated target; proved as Theorem A ('A priori bounds') via the near-degenerate regime and Amplification Theorem.

**关联卡**：This is Theorem A (main-theorem-01); its consequences Corollary B (degeneration to Herman quasicircles) and Theorem C (realization of arbitrary combinatorics) are also proved in the paper.

### 🔴 `OP-EA6BEA97AEF3` — `solved_in_paper` | MSC 37F10 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 2.2 'Herman quasicircles', Remark after Proposition bubble-structure
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Despite the striking similarity, a priori we do not know yet whether degenerating Herman rings in $\HRspace_{d_0,d_\infty,\theta}$ can converge to a limit in $\HQspace_{d_0,d_\infty,\theta}$.

**自包含改写**：Let d_0, d_infty >= 2 and theta in (0,1) be a bounded type irrational. Let HR_{d_0,d_infty,theta} be the space of degree d_0+d_infty-1 rational maps f such that 0 and infinity are superattracting fixed points with local degrees d_0 and d_infty, f has an invariant Herman ring of rotation number theta separating 0 and infinity, and every critical point of f other than 0 and infinity lies on the ring's boundary. Let HQ_{d_0,d_infty,theta} be the analogous space with a Herman quasicircle (quasicircle carrying a conjugacy of f to the rigid rotation R_theta, separating 0 and infinity, containing all free critical points) in place of the ring. Question: can a locally uniform limit of maps in HR_{d_0,d_infty,theta} with degenerating ring moduli lie in HQ_{d_0,d_infty,theta}? Resolved affirmatively in this paper (Section 8, Corollary 'limiting'): the limit space HR*_{d_0,d_infty,theta} is contained in HQ_{d_0,d_infty,theta}.

**判定理由**：Stated as unknown in Section 2.2 and resolved in Section 8: HR*_{d0,d_infty,theta} is contained in HQ_{d0,d_infty,theta}.

**关联卡**：This is the solved special case of intro question (1); the companion question in the same remark (whether every HQ-map is a genuine limit) remains open and has its own card.

### ⚪ `OP-625623869BB4` — `future_application` | MSC 37F10 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.2 'On Herman curves'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We expect that most of the methods in this paper can be extended to larger classes of Herman rings.

**自包含改写**：Expectation/outlook statement, not a mathematical proposition: the author expects most of the paper's near-degenerate machinery (waves, spreading, trading, amplification) to extend beyond the simplest-configuration space HR_{d_0,d_infty,theta} to larger classes of Herman rings.

**判定理由**：Taste/expectation about extending the methods; no mathematical proposition is posed.

**关联卡**：Immediately precedes and motivates the bounded-type degeneration conjecture card.

### ⚪ `OP-AAF9A9F0B213` — `future_application` | MSC 37F10 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 9 'Unicritical Herman curves'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In light of Corollary \ref{rescaled-limits}, we conduct a more rigorous study of the first return maps to prove various scaling properties for unicritical Herman quasicircles in \cite{Lim23}. These include universality and self-similarity about the critical point, similar to critical circle maps and quadratic Siegel disks.

**自包含改写**：Announced follow-up research program, not a proposition posed as open here: in the sequel [Lim23] the author will rigorously study first return maps of unicritical Herman quasicircles (for F_c in HQ_{d_0,d_infty,theta} with a unique free critical point at 1) to prove scaling properties including universality and self-similarity about the critical point, analogous to critical circle maps and quadratic Siegel disks. This paper contributes the precompactness of rescaled first return maps (Corollary rescaled-limits).

**判定理由**：Announced forthcoming results and research direction; not a proposition posed for resolution here.

**关联卡**：Builds on Corollary rescaled-limits proved in this paper; related to the parameter-space self-similarity conjecture card.

### ⚪ `OP-CDEED0301BCD` — `future_application` | MSC 37F10 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.2 (end of subsection)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> This serves as a motivation to further study the Renormalization Theory for Herman curves in the near future.

**自包含改写**：Research-direction statement, not a mathematical proposition: the results on rescaled limits of first return maps and the parameter-space self-similarity conjecture motivate further development of Renormalization Theory for Herman curves.

**判定理由**：Explicit outlook on future research program; not a decidable proposition.

**关联卡**：Same outlook repeated in Section 9 ('These will be further explored in the near future.'); connected to the self-similarity conjecture card and the sequel-scaling card.


## `2310.07681` — Murmurations
- 权威出处：**Inventiones mathematicae** 2025，DOI `10.1007/s00222-025-01347-8`
- 连接方式：`doi`｜全文 115,150 字符 via `cache-latex`｜提取模式 `fast`

### 🔵 `OP-996DB7C75490` — `background_open` | MSC 11M26 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, before Theorem 1.5
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> To address the asymptotic behavior of Figure \ref*{dr}, we also treat the case of smoothing by a characteristic function of an interval. For technical reasons, we need to assume RH and that $k \geq 6$ for our analysis, but these assumptions can likely be relaxed.

**自包含改写**：The Riemann Hypothesis for the Riemann zeta function zeta(s) (all non-trivial zeros have real part 1/2) is assumed as a hypothesis in the paper's proof of Theorem 1.5 on the asymptotic behavior of the sharp-cutoff smoothed murmuration function; it is a famous open problem, not resolved by this paper.

**判定理由**：RH is invoked as a conditional hypothesis, a famous open problem used as background for the paper's analysis, not a target of the paper.

**关联卡**：See card on relaxing Theorem 1.5 hypotheses.

**存疑**：Used only to obtain the tail estimate for the partial sums of Q(d) in Lemma 7.2.

### ⚪ `OP-0491D30FC06C` — `future_application` | MSC 11G05 | 难度 frontier

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, concluding remarks
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Murmurations for elliptic curves over $\Q$ are not explained by these results, as they constitute a very sparse subset of weight $2$ modular forms. We point out that the best fit curve to approximate the data of elliptic curve murmurations does not match the curve in Figure \ref*{dr}.

**自包含改写**：Not a proposition. The paper's theorems on murmuration densities M_k for families of weight k newforms of square-free level do not explain the originally observed murmurations for elliptic curves over Q ordered by conductor, since elliptic curves of fixed rank form a very sparse subset of weight 2 newforms, and the best-fit curve for elliptic curve murmuration data does not match the dyadic average curve of Theorem 1.2 (Figure 2). Direction: establish murmuration densities for families of elliptic curves over Q.

**判定理由**：An outlook noting the paper's results do not cover elliptic curve murmurations; a research direction, not a posed mathematical proposition.

**关联卡**：The ordering-sensitivity remark (ordering by naive height, j-invariant, or discriminant) accompanies this in the same paragraph and forms part of the same outlook.

### ⚪ `OP-38999162D5D5` — `future_application` | MSC 11F11 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, after Theorem 1.5 discussion
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Computing similar averages weighted "harmonically" (i.e., by the value at $1$ of the symmetric square $L$-function) by means of the Petersson formula reveals that with weights, this bias becomes much less pronounced: the resulting function grows like $y$, as opposed to $\sqrt{y}$, at the origin.

**自包含改写**：The paper reports (via the Petersson formula) that harmonically weighted averages (weighted by the value at 1 of the symmetric square L-function) of the root-number-correlated Fourier coefficients in the same family of weight k newforms yield a bias function growing like y at the origin, as opposed to the unweighted murmuration density M_k(y) which grows like sqrt(y) there. This is an observation/outlook on a variant of the main averages, not a formally stated theorem or problem.

**判定理由**：An unproved-in-detail observation about a variant family of averages; presented as an outlook/remark rather than a posed proposition.

**关联卡**：Contrasts with the growth rate sqrt(y) of M_k at the origin stated in the Introduction.

**存疑**：It is unclear from the source whether this computation is fully carried out or merely sketched; if proved elsewhere it would be mislabeled.

### ⚪ `OP-6B475901F6B8` — `future_application` | MSC 11F11 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Theorem 1.1, footnote 1
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We remark that the exponents in the statement are far from optimal, as our goal here is only to get a power saving error term in a range up to $X^a$ for some $a > 1$.

**自包含改写**：Not a proposition: a remark that the admissible parameter ranges in Theorem 1.1 (namely Y = (1+o(1))X^{1-delta_2}, P << X^{1+delta_1} with 0 < delta_1 < 1/11 and 2*delta_1 < delta_2 < (1/13)(4-18*delta_1)) for the average of sqrt(P)*lambda_f(P)*eps(f) over newforms f of square-free levels N in [X, X+Y] are far from optimal, and that the goal was merely a power-saving error term for P up to X^a for some a > 1. Implied direction: widen these ranges.

**判定理由**：A taste/method comment about non-optimality of exponents, not a formally posed proposition; it gestures at improving the ranges without stating one.

**关联卡**：Related to Theorem 1.1's parameter range; the paper proves the theorem only in the stated restricted range.

**存疑**：Borderline between future_application and an implicit real_open problem of extending the range; no explicit conjecture is stated.

### ⚪ `OP-981F15141257` — `future_application` | MSC 11F11 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Theorem 1.1, footnote 2
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The restriction to square-free levels is a technical one, as the trace formula simplifies greatly when the level is square-free. From the computations of Sutherland, it appears that the resulting density functions are slightly different when one considers all levels, but they share key properties with the ones above.

**自包含改写**：Not a proposition. The paper restricts its main theorem (Theorem 1.1: the root-number-weighted average of sqrt(P)*lambda_f(P) over Hecke bases H^new(N,k) of weight k newforms for Gamma_0(N) equals the weight k murmuration density M_k(y), y = P/X) to square-free levels N, for technical reasons (the Skoruppa-Zagier trace formula simplifies). Sutherland's computations suggest that for all levels (not just square-free) the resulting density functions differ slightly but share key properties. Direction: extend Theorem 1.1 to non-square-free levels.

**判定理由**：An outlook on extending results beyond the square-free technical restriction, supported by computational evidence but with no formal conjecture posed.

**关联卡**：Concerns removing a hypothesis of Theorem 1.1.

### ⚪ `OP-BBF478F60FCC` — `future_application` | MSC 11F11 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Discussion preceding Theorem 1.5 (Introduction)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> For technical reasons, we need to assume RH and that $k \geq 6$ for our analysis, but these assumptions can likely be relaxed.

**自包含改写**：Not a proposition. Theorem 1.5 states: assuming RH for zeta(s), for c > 1 and even weight k >= 6, the sharp-interval-smoothed murmuration function M^k_c(y) := (integral_1^c M_k(y/u) u^2 du/u)/(integral_1^c u^2 du/u), where M_k is the weight k murmuration density, is continuous on (0, infinity), vanishes at 0, and tends to 1/2 as y -> infinity. The author remarks these hypotheses (RH and k >= 6) can likely be relaxed. Direction: prove the same limit without RH and for all even k > 0.

**判定理由**：A stated belief that the hypotheses of Theorem 1.5 can likely be relaxed; a value judgement/outlook, not a formally posed problem.

**关联卡**：RH also appears as background_open in a separate card.


## `1505.02734` — An analytic invariant of $G_{2}$ manifolds
- 权威出处：**Inventiones mathematicae** 2025，DOI `10.1007/s00222-024-01310-z`
- 连接方式：`doi`｜全文 153,118 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟢 `OP-1695C5993F7F` — `real_open` | MSC 53C29 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, item (ii) in enumerated list of three questions
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> if so, whether the underlying homotopy classes of
$G_2$-structures are equal (up to spin diffeomorphism)?

**自包含改写**：Given two constructions of compact G₂-holonomy metrics that produce the same closed 7-manifold M up to diffeomorphism, are the underlying homotopy classes of the torsion-free G₂-structures equal up to spin diffeomorphism? Prior to this paper, no explicit examples of spin 7-manifolds admitting G₂-holonomy metrics in two distinct homotopy classes of G₂-structures were known.

**判定理由**：General question remains open; this paper provides the first explicit counterexample to the always-affirmative answer (Theorem 4.1) but does not resolve the general classification.

**关联卡**：This paper's Theorem 4.1 provides the first explicit examples (on a 2-connected 7-manifold with H⁴ ≅ ℤ⁹⁷ and p₁ = 4a) showing two G₂-holonomy metrics with non-homotopic G₂-structures on the same manifold. Related to cards 1 and 3.

### 🟢 `OP-4A6476D18F89` — `real_open` | MSC 53C29 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, item (iii) in enumerated list of three questions
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> if so, whether the two metrics lie in the same connected
component of the moduli space of $G_2$-holonomy metrics over the given class
  of $G_2$-structures?

**自包含改写**：Given two G₂-holonomy metrics on a closed 7-manifold M whose associated torsion-free G₂-structures are homotopic (up to spin diffeomorphism), do the two metrics necessarily lie in the same connected component of the moduli space of G₂-holonomy metrics over that homotopy class of G₂-structures?

**判定理由**：General question remains open; this paper provides the first explicit counterexample (Theorem 4.2) using the ν̄-invariant to distinguish moduli components.

**关联卡**：This paper's Theorem 4.2 provides the first example (on a 2-connected 7-manifold with H⁴ ≅ ℤ¹⁰⁹ and p₁ = 4a) where the moduli space has more than one component within a single homotopy class, detected by the new invariant ν̄. Related to cards 1 and 2.

### 🟢 `OP-6897A092FFC9` — `real_open` | MSC 53C29 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, item (i) in enumerated list of three questions
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> lead to the same closed $7$-manifold up to diffeomorphism?

**自包含改写**：Do different known constructions of closed G₂-holonomy 7-manifolds (such as Joyce's Kummer construction and the twisted connected sum construction of Kovalev and Corti–Haskins–Nordström–Pacini) ever produce 7-manifolds that are the same up to diffeomorphism? For the twisted connected sum construction this is answered affirmatively by examples in prior work [CHNP, Table 3] and [CrN3, Table 4], but the question for arbitrary pairs of constructions remains open.

**判定理由**：Posed by this paper as a guiding question; partially answered by prior work for twisted connected sums but not resolved for all construction types.

**关联卡**：Prior to this paper, answered affirmatively for twisted connected sums using classification results of Wilkens; general version for all constructions remains open. Related to cards 2 and 3 (Q2 and Q3).

### 🟢 `OP-F183700751CD` — `real_open` | MSC 53C29 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Matching problem environment, Section 2.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Given $\thet$, a pair of deformation families of ACyl Calabi-Yau 3-folds
and a configuration of their polarising lattices $N_\pm$, does there exist some
pair of members with a $\thet$-\hk rotation compatible with that configuration?

**自包含改写**：Given a gluing angle ϑ ∈ (0,π), a pair of deformation families of asymptotically cylindrical Calabi–Yau 3-folds V± (with asymptotic cross-sections S¹ × K3), and a configuration (i.e., a pair of embeddings of the polarising lattices N₊, N₋ into the K3 lattice L up to the action of O(L)), does there exist a pair of members from these deformation families and a ϑ-hyper-Kähler rotation r: K₊ → K₋ (i.e., an isometry satisfying r*ωᴵ_- + ir*ωᴶ_- = e^{iϑ}(ωᴵ_+ - iωᴶ_+) and r*ωᴷ_- = -ωᴷ_+) between their asymptotic K3 surfaces that realizes the given configuration of polarising lattices?

**判定理由**：Formally posed as a Matching problem environment; sufficient conditions known only in special cases, not resolved in general.

**关联卡**：Necessary conditions include condition (eq:preserve) in Definition 2.5 and {α⁺₁, α⁺₂, α⁺₃} = {0, 2ϑ, -2ϑ}. Sufficient conditions discussed in [CHNP, Section 6], [CrN3, Section 5], and [xtcs, Section 6] for special cases.

### 🟢 `OP-FAA74E515F19` — `real_open` | MSC 53C29 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Question (Qstn environment), Section 1, after Corollary 1.4 and the preceding paragraph on divisibility by 3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> What is the range of~$\bar\nu$ on arbitrary $G_2$-manifolds?
  Is it finite?

**自包含改写**：What is the set of possible values of the extended ν-invariant ν̄(M,g) = -24η(D_M) + 3η(B_M) as (M,g) ranges over all closed 7-manifolds M equipped with a torsion-free G₂-structure (equivalently, a metric of holonomy contained in G₂)? Is this set of values finite? For extra-twisted connected sums with k± ≤ 2, the values satisfy -75 < ν̄(M,g) < 75 and are always divisible by 3.

**判定理由**：Explicitly posed as a Question in this paper; the range is unknown beyond extra-twisted connected sums with k± ≤ 2.

**关联卡**：The paper proves boundedness for the restricted class of extra-twisted connected sums with k± ≤ 2 (Remark at end of paper). Computing ν̄ for Joyce's examples (card 6) would help address this. The sequel paper [GN] finds examples where 3 does not divide ν̄.

### 🟠 `OP-874AFE82ADD3` — `method_obstruction` | MSC 53C29 | 难度 

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Remark at end of paper (BarNuBoundedRem), Section 5
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> we cannot use the extra-twisted connected sum construction
with~$k_\pm\le 2$ to produce families of $G_2$-manifolds
with infinitely many different values of~$\bar\nu$

**自包含改写**：For extra-twisted connected sums with k± ≤ 2 (i.e., where the cyclic groups Γ± ≅ ℤ/k± satisfy k± ∈ {1,2}), the extended ν-invariant is bounded: one has -75 < -72ρ/π + 3m_ρ(L;N₊,N₋) < 75, where ρ = π - 2ϑ with ϑ ∈ (0,π) the gluing angle, L is the K3 lattice, N± ⊂ L are the polarising lattices, and m_ρ is defined via the configuration angles α⁻₁,…,α⁻₁₉ of Definition 2.6. Consequently, this restricted class of constructions cannot produce G₂-manifolds with infinitely many distinct ν̄ values.

**判定理由**：A proven limitation of the method for k± ≤ 2; not formally posed as an open problem but shows a hypothesis/bound that constrains the construction.

**关联卡**：Directly motivates card 4 (Question about range of ν̄). The sequel paper [GN] extends to k± > 2 where this bound may no longer apply.

### ⚪ `OP-7CEA0A99FE95` — `future_application` | MSC 53C29 | 难度 

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, immediately after the Question (Qstn) about the range of ν̄
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> To answer this question, it would be helpful to know the $\bar\nu$-invariant of Joyce's examples.

**自包含改写**：Computing the extended ν-invariant ν̄(M,g) for Joyce's examples of compact G₂-manifolds (constructed via the Kummer construction, i.e., resolutions of T⁷/Γ) would help determine the range of ν̄ on arbitrary G₂-manifolds.

**判定理由**：A value judgement about what would be helpful, not itself a mathematical proposition; identified as a research direction.

**关联卡**：Related to card 4 (range of ν̄). The paper cites Fornasin and Scaduto as working in this direction.


## `2304.07373` — Extensions of characters in type D and the inductive McKay condition, II
- 权威出处：**Inventiones mathematicae** 2025，DOI `10.1007/s00222-025-01354-9`
- 连接方式：`doi`｜全文 278,048 字符 via `cache-latex`｜提取模式 `fast`

### 🔵 `OP-0E0B8888C34A` — `background_open` | MSC 20C33 | 难度 hard

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 2, before the corollary answering Broué's question
- 自检：conditions_complete: yes | notation_self_contained: partial | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> See also Question (P) in \cite[Introduction]{TypeD1} for a more general problem.

**自包含改写**：Question (P) in the Introduction of Späth, 'Extensions of characters in type D and the inductive McKay condition, I' (Nagoya Math. J. 252), is a more general problem (on extendibility of characters in finite reductive groups) that generalizes Broué's question on d-cuspidal unipotent characters; it is cited as background and is not addressed as the paper's own target here.

**判定理由**：A question from a companion paper cited as background for a more general problem; not posed as this paper's own target.

**⚠️ 人工复核标记**：The precise statement of Question (P) is not reproduced in this source; only a reference is given.

**关联卡**：Generalizes the Broué question card; the Broué special case is solved in this paper.

**存疑**：The full content of Question (P) lies outside this source; only its existence and role as a more general problem are verifiable here.

### 🔵 `OP-80B0FC46E6ED` — `background_open` | MSC 20C15 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, before Theorem C
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Theorem \ref{thm1} also contributes to the general program to prove J. McKay's conjecture on character degrees for any prime $\ell$, see \cite{McK}.

**自包含改写**：McKay's conjecture: for every finite group X, every prime ℓ, and a Sylow ℓ-subgroup P of X, the groups X and N_X(P) have the same number of irreducible complex characters of degree prime to ℓ. The paper proves the case ℓ = 3 (Theorem C) but the conjecture for arbitrary ℓ remains a background open program.

**判定理由**：Famous open conjecture cited as motivation; the paper only contributes the ℓ = 3 case via Theorem C.

**关联卡**：The case ℓ = 2 was previously known [MS16]; the paper establishes ℓ = 3 via Theorem C.

### 🟠 `OP-C6F89129BABB` — `method_obstruction` | MSC 20C33 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> But devising a satisfactory uniqueness condition for quasi-simple groups $G$ of Lie type seems a quite difficult goal.

**自包含改写**：For quasi-simple groups G of Lie type (G = G_sc^F the universal covering of a finite simple group of Lie type), the existence of a Jordan decomposition of characters was known for groups \tilde G = \tilde{G}^F with connected center via the Digne–Michel uniqueness theorem; the paper notes that devising a satisfactory uniqueness condition for the quasi-simple groups themselves appears to be a quite difficult goal. The paper bypasses this via Condition A'(∞).

**判定理由**：A remark on the difficulty/limitation of the uniqueness-condition approach, without formally posing an open problem; the paper circumvents it with Theorem B.

**关联卡**：Circumvented by Theorem B, which constructs an Out(G)-equivariant Jordan decomposition without such a uniqueness condition.

### 🔴 `OP-4CB60522CC31` — `solved_in_paper` | MSC 20C33 | 难度 medium

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Remark after Corollary 6.11 (Section on EE(C))
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Another challenge is to find a conjugacy class $\cC\in \frakC_0$ such that $\EE(\cC)\neq \emptyset$.

**自包含改写**：In the framework where G = D_{l,sc}(p^m) with p odd, m even, l ≥ 4, D = ⟨F_0|_{G^F}, γ⟩ a non-cyclic 2-subgroup of E(G^F) with F ∈ ⟨F_0²⟩⁺ and [Z(G),F_0]=[Z(G),F]=1, and 𝔠_0 the set of semisimple conjugacy classes C of the dual group H = D_{l,ad}(F̄) with F_0(C) = γ(C) = C that contain a γ-stable H^{F_0}-class: the challenge was to exhibit a class C ∈ 𝔠_0 with EE(C) ≠ ∅ (a set of D-invariant, non-extendible characters in E(G^F,C)). The same remark then constructs such a class explicitly.

**判定理由**：The 'challenge' is resolved within the same remark, which constructs a class C ∈ 𝔠_0 with EE(C) ≠ ∅ (l = 2d+4a+4, q = q_0² with 4 | q_0−1).

**关联卡**：Related statement in the same remark: classes C with EE(C) ≠ ∅ exist for infinitely many l ≥ 4 (via [CS22, Rem. 3.6] and rank transfer).

### 🔴 `OP-7BBE679C7741` — `solved_in_paper` | MSC 20C33 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Theorem A (Introduction)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $G=\bG_{\mathrm{sc}}^F$ be the universal covering of a finite simple group of Lie type with $\wG$ and $E(G)$ as above, see also \ref{not}. Then there exists an $E(G)$-stable $\wG$-transversal $\TT$ in $\Irr(G)$ such that every character $\chi\in\TT$ extends to its stabilizer in $G E(G)$.

**自包含改写**：Condition A(∞): Let G = G_sc^F be the universal covering of a finite simple group of Lie type, realized as the fixed points of a simple simply connected algebraic group G_sc under a Frobenius endomorphism F, with \tilde G = \tilde{G}^F from a regular embedding G ≤ \tilde{G} (diagonal automorphisms) and E(G) the group of graph and field automorphisms. Then there exists an E(G)-stable \tilde G-transversal T in Irr(G) such that every character χ ∈ T extends to its stabilizer in G·E(G). Prior to this paper this was open exactly for groups of types D_l and ²D_l.

**判定理由**：The main result (Theorem A), proved by the paper, completing the previously open types D and ²D.

**关联卡**：This was the open target left by prior work in all other types; it implies Theorem B (equivariant Jordan decomposition) and contributes to Theorem C.

### 🔴 `OP-B1AC5C3FC79F` — `solved_in_paper` | MSC 20C15 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Theorem C (Introduction)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $X$ be a finite group, let $P$ be a Sylow 3-subgroup of $X$. Then $X$ and $\NNN_{X}(P)$ have the same number of irreducible characters of degree prime to 3.

**自包含改写**：For every finite group X and a Sylow 3-subgroup P of X, X and N_X(P) have the same number of irreducible complex characters of degree prime to 3 (the McKay conjecture for the prime 3), derived from the reduction theorem of Isaacs–Malle–Navarro plus Theorem A and the previously established conditions A(1), B(1), A(2), B(2).

**判定理由**：Theorem C proves the McKay conjecture for ℓ = 3 in this paper; the general conjecture remains open.

**关联卡**：Special case (ℓ = 3) of the McKay conjecture card above.

### 🔴 `OP-D8F4D4DB607A` — `solved_in_paper` | MSC 20C33 | 难度 medium

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 2, corollary after Theorem 2.5 (propunipext)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> A consequence of the above \Cref{propunipext} is the answer to a question of M. Brou\'e (see \cite{Broue}), originally on $d$-cuspidal unipotent characters.

**自包含改写**：Broué's question (private communication 2007, originally on d-cuspidal unipotent characters): for a connected reductive group G over a finite field with Frobenius endomorphism F and an F-stable Levi subgroup M of G, does maximal extendibility hold with respect to M^F ⊴ N_G(M)^F for the set Uch(M^F) of unipotent characters? The paper answers this affirmatively as a corollary of Theorem 2.5.

**判定理由**：The paper explicitly answers this question affirmatively via the corollary following Theorem 2.5.

**关联卡**：See also the related Question (P) in [TypeD1, Introduction], which is more general and cited as background.

### ⚪ `OP-980FF35F61B0` — `future_application` | MSC 20C33 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Remark after Proposition 3.16 (Section 3)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It would be clearly interesting to ask if similar labellings are possible whenever $\bG$ is a simply connected simple group of any type, at least when $E(\bG)$ is not cyclic.

**自包含改写**：The paper's labelling of (F_0, γ)-stable \tilde G^F-orbit sums in a geometric Lusztig series E(G^F, C) via unipotent characters (Theorem 'labelEGFFnull' etc.) is developed for simply connected simple groups of type D_l (l ≥ 4) over the algebraic closure of a field of odd characteristic. The remark asks whether similar labellings are possible when G is a simply connected simple group of any type, at least when E(G) (the group of field and graph automorphisms) is not cyclic. This is stated as a taste/research direction, not a formal conjecture.

**判定理由**：A value judgement ('clearly interesting to ask') pointing to a research direction, with no formal proposition stated.

**存疑**：Borderline between a genuine open question and a taste remark; the phrase 'similar labellings' is informal, so it is not treated as a formal open proposition.


## `2205.15621` — Relations on $\overline{\mathcal{M}}_{g,n}$ and the negative $r$-spin Witten conjecture
- 权威出处：**Inventiones mathematicae** 2025，DOI `10.1007/s00222-025-01351-y`
- 连接方式：`doi`｜全文 198,816 字符 via `cache-latex`｜提取模式 `fast`

### 🟢 `OP-2EB7BE572681` — `real_open` | MSC 37K20 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, Conjecture C (r-KdV integrability); restated as Conjecture 5.20 (conj:rKdV)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The descendant potential $ Z^{\Theta^r} $ is a tau function of the $ r $-KdV integrable hierarchy. Moreover, it coincides with the $ r $-spin Brézin--Gross--Witten tau function.

**自包含改写**：For an integer r >= 2, let Z^{Theta^r} be the descendant potential of the Theta class Theta^r (the CohFT on V = span_Q(v_1,...,v_{r-1}) defined as the rescaled pushforward of the top Chern class of the vector bundle V^{r,-1}_{g;a} = R^1 pi_* L over the moduli space of r-th roots of the anticanonical bundle on Mbar_{g,n}). Conjecture: Z^{Theta^r} is a tau function of the r-KdV (r-th Gelfand–Dickey) integrable hierarchy and coincides with the r-spin Brézin–Gross–Witten tau function Z^{r-BGW} (the KP tau function associated to the point H = span{Phi_1, Phi_2, ...} in the Sato Grassmannian built from the r-BGW matrix model). The paper proves this for r = 2 (Norbury's conjecture) and r = 3, and reduces the general case to the string equation H^r_{-r+2} Z^{r-BGW} = mu Z^{r-BGW} for some constant mu; the conjecture remains open for r >= 4.

**判定理由**：The paper's own integrability conjecture; proved only for r=2,3, open for r>=4.

**⚠️ 人工复核标记**：The paper proves the conjecture only for r=2 and r=3 (Theorem E / Theorem 5.24); the general r>=4 case remains the open part.

**关联卡**：The r=2 instance is Norbury's conjecture (separate solved card); the reduction to the string equation (Proposition 5.22) is an equivalent formulation, not a distinct problem.

### 🟢 `OP-60649AE350A9` — `real_open` | MSC 14H10 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 2.2.4, discussion after Corollary 2.18 (cor:vanishing)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Thus, it is an interesting line of investigation to ask whether our relations in \cref{cor:vanishing} imply Pixton's relations \cite{Pix13}. We leave this for future work.

**自包含改写**：Question: do the vanishing tautological relations [(R T w_{g,n})(v_{a_1}\otimes\cdots\otimes v_{a_n})]^d = 0 for d > D^r_{g;a} (except (g,n)=(g,0) and d=3g-3), obtained from the deformed Theta class Theta^{r,epsilon}, imply Pixton's relations in the tautological ring of Mbar_{g,n}? The authors explicitly leave this for future work.

**判定理由**：An explicitly posed question ('ask whether...'), decidable, left for future work by this paper.

**关联卡**：Converse implication (Pixton implies these relations) is a separate card.

### 🟢 `OP-6931369B31F1` — `real_open` | MSC 14H10 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, discussion after Theorem B
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Moreover, we expect them to be implied by Pixton's relations, although we do not have a proof of this statement.

**自包含改写**：The tautological relations [(R T w_{g,n})(v_{a_1}\otimes\cdots\otimes v_{a_n})]^d = 0 in H^{2d}(Mbar_{g,n}) for d > D^r_{g;a} (except (g,n)=(g,0), d=3g-3) produced in this paper from the deformed Theta class are expected to be implied by Pixton's relations in the tautological ring; the authors state this expectation without proof and note that Janda's result (limits from semisimple points to the discriminant of a generically semisimple Dubrovin–Frobenius manifold with flat unit) does not cover their situation, since their deformation is a family of Dubrovin–Frobenius manifolds collapsing to a nowhere-semisimple one and their unit is not flat.

**判定理由**：Decidable statement about tautological rings left explicitly open ('we do not have a proof').

**关联卡**：Complementary question of whether these relations imply Pixton's relations is a separate card.

### 🟢 `OP-B3D5BDECB4DF` — `real_open` | MSC 14H10 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, discussion after Theorem B (thm:intro:rels)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> While our result is not valid in Chow, as Teleman's result has not been extended to Chow field theories, we expect the above relations to hold in the Chow ring.

**自包含改写**：The tautological relations [(R T w_{g,n})(v_{a_1} \otimes \cdots \otimes v_{a_n})]^d = 0 in H^{2d}(Mbar_{g,n}) for d > D^r_{g;a} = ((r+2)(g-1)+n+sum_i a_i)/r (except (g,n)=(g,0) and d = 3g-3), obtained via Teleman reconstruction for the deformed Theta class Theta^{r,epsilon}, are expected to also hold in the Chow ring of Mbar_{g,n}; this is stated as an expectation without proof, since Teleman's reconstruction theorem has not been extended to Chow field theories.

**判定理由**：A decidable mathematical statement (vanishing in Chow) explicitly left open by the authors as an expectation without proof.

**⚠️ 人工复核标记**：Phrased as an expectation ('we expect') rather than a numbered conjecture; obstruction is the unextended Teleman theorem in Chow.

**关联卡**：Depends on extending Teleman's reconstruction theorem to Chow field theories (method obstruction noted in the same sentence).

### 🟢 `OP-D487C8B41740` — `real_open` | MSC 37K20 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 5.3.4, concluding remarks after Theorem 5.24
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We leave the proof of the string equation in general, equivalently the $ r $-KdV \cref{conj:rKdV}, to future work. Instead of finding a Kac--Schwarz operator that corresponds to the operator $ H^r_{-r+2} $, an alternative approach to proving the string equation is to use the Ward identities for the $ r $-BGW matrix model.

**自包含改写**：The proof of the string equation H^r_{-r+2} Z^{r-BGW} = mu Z^{r-BGW} for general r >= 4 (equivalently, by Proposition 5.22, the conjecture that the descendant potential Z^{Theta^r} of the Theta class equals the r-BGW tau function of the r-KdV hierarchy) is left to future work; the paper notes an alternative approach via Ward identities for the r-BGW matrix model. This is the same open problem as the r-KdV integrability conjecture for r >= 4, framed as a research direction with a suggested method.

**判定理由**：Explicitly deferred open statement, but equivalent to the main conjecture card; retained as the closing statement of the open problem with the suggested alternative approach.

**⚠️ 人工复核标记**：Duplicates (by the paper's own proved equivalence, Proposition 5.22) the general r-KdV integrability conjecture card; included mainly to record the suggested Ward-identity approach — flag for possible merge.

**关联卡**：Equivalent formulation of the r-KdV integrability conjecture (first card) via the string equation; the Ward-identity suggestion is a future_application element.

### 🔵 `OP-508A42B7D092` — `background_open` | MSC 14N35 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, subsection 'W-constraints and integrability'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Conversely, however, the answer to whether one can (and if so how to) obtain a global spectral curve from a given semisimple CohFT is unanswered in general.

**自包含改写**：General background question (not resolved for the general case in the literature): given a semisimple cohomological field theory, can one construct a global spectral curve (in the sense of Eynard–Orantin topological recursion) whose correlators encode the descendant theory of the CohFT, and if so how? The paper notes the partial answer of Dunin-Barkowski–Norbury–Orantin–Shadrin does not apply to Dubrovin–Frobenius manifolds without a flat unit; the paper solves its own instance (global spectral curve x(z)=z^r/r - epsilon z, y=-1/z for Theta^{r,epsilon}) but the general question remains open.

**判定理由**：A general open question in the literature cited as motivation; this paper resolves only its special instance.

**关联卡**：The paper's own instance (Theorem 3.14 / Theorem D) is proved in the paper; only the general question is background.

### 🟠 `OP-959F7C414DCE` — `method_obstruction` | MSC 81R12 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 5.3.4, footnote in the discussion before Theorem 5.24
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> While \cite{MMS96} sketches an argument to prove the string equation for any $ r $, there is a gap in the proof there that we were unable to resolve.

**自包含改写**：The paper reports that the sketch in Mironov–Morozov–Semenoff (hep-th/9607247) purporting to prove the string equation H^r_{-r+2} Z^{r-BGW} = mu Z^{r-BGW} for the r-BGW tau function for any r contains a gap that the present authors were unable to resolve; hence no existing method proves the string equation for r >= 4. This is a statement that the available method/argument fails, not a newly posed problem.

**判定理由**：Documents that a prior proof attempt fails (gap), explaining why the string equation (and hence the r-KdV conjecture) remains open for r >= 4.

**关联卡**：Obstruction to the general r-KdV integrability conjecture card.

### 🟠 `OP-9EEA7B21AF5D` — `method_obstruction` | MSC 81R12 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 5.3.2, preamble to Theorem 5.15 (thm:KS:operators)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We start using the analysis done in \cite{MMS96}, but the operators found there do not uniquely specify the tau function. For $ r =2 $ and $ r = 3 $, we find Kac--Schwarz operators that uniquely specify the tau function and produce the $ \mathcal{W} $-constraints we are looking for, but we are unable to do so for  $ r \geq 4 $.

**自包含改写**：For the r-BGW tau function Z^{r-BGW}, the Kac–Schwarz operators available from Mironov–Morozov–Semenoff do not uniquely specify the tau function; the paper constructs Kac–Schwarz operators (a = z^r/r, b, c conjugated by e^{-S}, S(z) = -hbar^{-1/2} z^{r-1}/(r-1) - (1/2)log(z^{r-1})) that uniquely determine Z^{r-BGW} only for r = 2 and r = 3, and the authors state they are unable to achieve uniqueness for r >= 4. This is a limitation of the method (no proposition posed).

**判定理由**：Documents the failure/limitation of the Kac–Schwarz method for r >= 4 without formally posing a problem.

**关联卡**：Method obstruction underlying the open general r-KdV integrability conjecture.

### 🔴 `OP-EAB1133120E8` — `solved_in_paper` | MSC 81R12 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Abstract; also Introduction, Theorem E and Section 5.3.4 (thm:r23)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Using this result for $ r = 2 $, we prove Norbury's conjecture which states that the descendant potential of $ \Theta^2 $ coincides with the Brézin--Gross--Witten tau function of the KdV hierarchy.

**自包含改写**：For r = 2, the descendant potential Z^{Theta^2} of the Theta class Theta^2 (Norbury's Theta class) coincides with the Brézin–Gross–Witten tau function of the KdV (2-KdV) integrable hierarchy; the paper also proves the analogous statement for r = 3 (Z^{Theta^3} equals the 3-BGW tau function of the 3-KdV hierarchy).

**判定理由**：Theorem E / Theorem 5.24 proves the conjecture for r = 2 and r = 3.

**关联卡**：Special case of the general r-KdV integrability conjecture (separate card); not a duplicate because the r=2 case is Norbury's previously open conjecture, resolved here.

### ⚪ `OP-707A90B157B2` — `future_application` | MSC 14H10 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 2.2.4, Remark after Theorem 2.13 (thm:dTheta)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> One can find an alternative expression for the deformed Theta class $ \Theta^{r,\epsilon} $ in terms of tautological classes using Chiodo's Grothendieck--Riemann--Roch formula in \cite{Chi08+}. It would be interesting to compare this expression with the one that we find in \cref{thm:dTheta}.

**自包含改写**：Not a proposition: the authors remark that an alternative expression for the deformed Theta class Theta^{r,epsilon} in terms of tautological classes can be obtained from Chiodo's Grothendieck–Riemann–Roch formula, and that comparing it with their Teleman-reconstruction expression 'would be interesting' — a value judgement about a possible computation, not a posed open problem.

**判定理由**：Taste comment ('would be interesting to compare'), no mathematical proposition posed.

### ⚪ `OP-E025712610F6` — `future_application` | MSC 14H70 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, subsection 'W-constraints and integrability'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It is intriguing that the $ R $-matrix for the deformed Theta class (\cref{thm:intro:rels}) essentially matches the $ R $-matrix for the $ e_1 $-shifted Witten class studied in \cite{PPZ19}. From the perspective of the topological recursion, \cref{intro:thm:TR} provides an explanation for this occurrence: the function $ x(z) $ for the spectral curve is exactly the same in both cases \cite{CCGG24}. However, we do not know  of a purely algebro-geometric reason for this phenomenon and this deserves further investigation.

**自包含改写**：Not a proposition: the authors state they do not know a purely algebro-geometric explanation for why the R-matrix of the deformed Theta class Theta^{r,epsilon} essentially matches the R-matrix of the e_1-shifted Witten r-spin class of Pandharipande–Pixton–Zvonkine, and that this 'deserves further investigation' (a research direction, not a decidable mathematical statement).

**判定理由**：A taste/research-direction comment, not a posed proposition.

**关联卡**：Repeated in Section 2.2.3 ('We do not know of a good algebro-geometric reason for this occurrence and this deserves further investigation.'); the same remark, not duplicated.


# Journal of the American Mathematical Society

## `2108.10256` — Eremenko’s conjecture, wandering Lakes of Wada, and maverick points
- 权威出处：**Journal of the American Mathematical Society** 2025，DOI `10.1090/jams/1049`
- 连接方式：`doi`｜全文 161,630 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟢 `OP-1C63750ED7F7` — `real_open` | MSC 37F10 | 难度 medium

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, Remark 1.9(i) (rmk:Jcomponents)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We do not know whether in Theorem~\ref{thm:main} one can additionally ensure that every connected component of $\partial K$ is a connected component of $J(f)$. This would only be possible if $f$ had multiply connected wandering domains limiting on $\partial K$.

**自包含改写**：Theorem 1.7 of the paper: for K a full compact subset of C (C \ K connected) and Z_I, Z_BU disjoint finite or countably infinite subsets of K such that no connected component of the interior of K intersects both Z_I and Z_BU, there exists a transcendental entire function f with: boundary of K contained in the Julia set J(f) (complement of the Fatou set); f^n(K) pairwise disjoint for n != m; every component of int(K) a wandering Fatou domain; Z_I contained in the escaping set I(f) = {z : f^n(z) -> infinity} and Z_BU contained in the bungee set BU(f) = {z not in I(f) : limsup |f^n(z)| = infinity}. Open question posed by the paper: can f additionally be chosen so that every connected component of the boundary of K is a connected component of J(f)? The authors note this would only be possible if f had multiply connected wandering domains limiting on the boundary of K.

**判定理由**：'We do not know whether...' - a genuine open question posed by this paper about strengthening its own theorem.

**关联卡**：The paper notes the meromorphic analogue is achieved (any compact set K realised with each component of the boundary a component of J(f)) in Marti-Pete-Rempe-Waterman, Math. Ann. 2024, Theorem 1.3.

### 🟢 `OP-3E8E15F3BDD5` — `real_open` | MSC 37F10 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, question following Theorem 1.11 (generalizing a question of Bishop 2014)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Let $U$ be a simply connected wandering domain of a transcendental entire function. Does the set of maverick points in $\partial U$ have zero logarithmic capacity when seen from $U$? That is, let $\phi\colon\DD\to U$ be a conformal isomorphism between the unit disc $\DD$ and $U$, and consider the set $\Xi\subseteq \partial\DD$ of points at which the radial limit of $\phi$ exists and is a maverick point. Does $\Xi$ have zero logarithmic capacity?

**自包含改写**：Let f be a transcendental entire function and U a simply connected wandering Fatou domain. A point z in the boundary of U is maverick if there is a sequence (n_k) with f^{n_k}(z) -> w in the Riemann sphere as k -> infinity while w is not a limit function of f^{n_k} restricted to U (equivalently limsup_{n} of the spherical distance between f^n(z) and f^n(w') is positive for w' in U). Question, generalizing a question of Bishop for escaping wandering domains: let phi: D -> U be a conformal isomorphism from the unit disc D onto U, and let Xi be the subset of the unit circle of points at which the radial limit of phi exists and is a maverick point. Must Xi have zero logarithmic capacity? The paper proves the set of maverick points has harmonic measure zero (Theorem 1.11) and that zero logarithmic capacity is best possible: by Theorem 1.13, for any compact Xi of zero logarithmic capacity on the unit circle there is such an f (with U escaping or oscillating) for which every point of Xi is maverick.

**判定理由**：Formal question posed by this paper; it proves sharpness (Theorem 1.13) and harmonic measure zero, but not the capacity answer.

**关联卡**：Theorem 1.13 shows zero logarithmic capacity cannot be improved: any compact zero-capacity set can be realized as maverick points; Theorem 1.14 shows the maverick set can have positive Lebesgue measure.

### 🟢 `OP-495A9AA22BFF` — `real_open` | MSC 37F10 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, 'Further questions' subsection (Question 1.17, qu:invariant)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Let $f$ be a transcendental entire function and suppose that $U$ is an invariant Fatou component of $f$. Must every connected component of $\C\setminus \overline{U}$ intersect~$\J(f)$?

**自包含改写**：Let f be a transcendental entire function, U an invariant Fatou component (f(U) contained in U), J(f) the Julia set (complement of the Fatou set). Question posed by the paper: must every connected component of C \ (closure of U) intersect J(f)? A positive answer would imply that a transcendental entire function has at most one completely invariant Fatou component (a component U with f^{-1}(U) = U, for which the boundary of U equals J(f)). Motivation: it appears much more difficult, if at all possible, to construct invariant Fatou components with Lakes of Wada boundaries.

**判定理由**：Formal question posed in 'Further questions' concerning invariant Fatou components.

**关联卡**：Strengthened for bounded U in the companion 'simple closed curve' question card.

### 🟢 `OP-49D4B26B0420` — `real_open` | MSC 37F10 | 难度 medium

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, 'Further questions' subsection (Question 1.16, qu:bocthalernew)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Suppose that $U$ is a bounded simply connected Fatou component of a transcendental entire function, and let $K=\Fill(\overline{U})$. Is it true that $\partial U = \partial K$?

**自包含改写**：Let U be a bounded simply connected Fatou component (connected component of the Fatou/equicontinuity set) of a transcendental entire function f, and let K = fill(closure of U), i.e., the complement in C of the unbounded connected component of C \ (closure of U). Question posed by the paper: is the boundary of U equal to the boundary of K? A positive answer, combined with Theorem 1.7 of the paper, would imply that a bounded simply connected domain U can arise as a Fatou component of an entire function if and only if the boundary of U equals the boundary of fill(closure of U).

**判定理由**：Formal question posed in 'Further questions' as a modification of Boc Thaler's question in light of Theorem 1.7.

**关联卡**：Successor of Boc Thaler's Question 1.7 card (answered negatively in this paper).

### 🟢 `OP-82794928D1DD` — `real_open` | MSC 37F10 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, 'Further questions' subsection, first question
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Can $I(f)$ have a bounded connected component if $f\in \mathcal B$ has infinite order, or if $f\notin\B$ has finite order?

**自包含改写**：Let f be a transcendental entire function, I(f) = {z in C : f^n(z) -> infinity as n -> infinity} its escaping set, B the Eremenko-Lyubich class (transcendental entire functions whose set S(f) of singular values is bounded), and 'order' the growth order of f. It is known (Rottenfusser-Ruckert-Rempe-Schleicher, Theorem 1.6) that Eremenko's conjecture holds for all functions of finite order in class B. Question posed by the paper: can I(f) have a bounded connected component if f is in B and has infinite order, or if f is not in B and has finite order? The paper's own counterexample function is of infinite order and not in class B.

**判定理由**：Formal question posed in 'Further questions', asking whether one hypothesis (finite order, or class B) can be omitted.

**关联卡**：Refines the Eremenko conjecture card: the conjecture is now false in general, but these two regimes (B with infinite order; finite order outside B) remain open.

### 🟢 `OP-CF40AEC1E6A1` — `real_open` | MSC 37F10 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, 'Further questions' subsection (final question)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Let $f$ be an entire function and suppose that $U$ is a bounded invariant Fatou component of $f$. Must $\partial U$ be a simple closed curve?

**自包含改写**：Let f be an entire function (as stated; the interesting case is transcendental entire) and U a bounded invariant Fatou component of f, i.e., f(U) is contained in U and U is bounded as a subset of C, where a Fatou component is a connected component of the Fatou set (equicontinuity set of the iterates). Question posed by the paper: must the boundary of U be a simple closed curve? This strengthens the companion question (must every component of C \ (closure of U) intersect the Julia set?) for bounded U, motivated by polynomial results such as Roesch-Yin (immediate basins of bounded polynomial Fatou components are Jordan domains).

**判定理由**：Formal question posed in 'Further questions', strengthening the previous question for bounded invariant Fatou components.

**关联卡**：Strengthening of the invariant-Fatou-component question card (Question 1.17).

### 🟢 `OP-F464CFB4C8A1` — `real_open` | MSC 37F10 | 难度 medium

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, subsection 'Meromorphic functions'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It is plausible that Theorem~\ref{thm:maverick} is true also for general wandering domains of transcendental meromorphic functions, but this requires further investigation.

**自包含改写**：Theorem 1.11 of the paper: if f is a transcendental entire function and U a wandering Fatou domain, then the set of maverick points of U (points z in the boundary of U for which some subsequence f^{n_k}(z) converges to w in the Riemann sphere while w is not a limit function of f^{n_k} on U) has harmonic measure zero with respect to U. The same proof works for a transcendental meromorphic function f: C -> Riemann sphere having a wandering domain whose orbit consists only of simply connected Fatou components. Open question raised by the paper: does the conclusion (maverick points have harmonic measure zero) also hold for general wandering domains of transcendental meromorphic functions?

**判定理由**：A decidable mathematical extension statement the paper explicitly leaves open ('plausible... requires further investigation').

**⚠️ 人工复核标记**：Hedged phrasing ('It is plausible...') rather than a formal question environment; classified real_open because it asserts a specific unresolved mathematical proposition.

**关联卡**：Extension of the paper's Theorem 1.11 (maverick points have harmonic measure zero); the simply-connected-orbit case follows with the same proof.

**存疑**：Borderline between real_open and future_application due to hedged wording; the underlying proposition is well-defined.

### 🔵 `OP-03AA84001319` — `background_open` | MSC 37F10 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, remarks following Question 1.5 (recalled in the remark after the proof of Theorem 1.11, Section 7)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> One should note the distinction with \emph{orbitally bounded} wandering domains: wandering domains whose points have bounded orbits. The existence of orbitally bounded wandering domains is a famous open problem; see~\cite[Problem~2.67]{hayman-lingham19}.

**自包含改写**：Does there exist a transcendental entire function f with an orbitally bounded wandering domain, i.e., a wandering Fatou component U (a Fatou component that is neither periodic nor preperiodic) all of whose points z in U have bounded orbits (sup_n |f^n(z)| < infinity)? (Contrast: a bounded wandering domain is bounded as a subset of the plane.) Cited as a famous open problem, Problem 2.67 in Hayman-Lingham, Research Problems in Function Theory.

**判定理由**：Famous open problem cited as background distinction; not this paper's own target.

**关联卡**：Mentioned twice: in the introduction near Question 1.5 and in Section 7's remark (same problem; one card).

### 🔵 `OP-04CB72BAD446` — `background_open` | MSC 37F10 | 难度 hard

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, discussion following Question 1.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The problem whether the \emph{whole} Julia set can be a Lakes of Wada continuum is related to \emph{Makienko's conjecture} concerning completely invariant domains and buried points of rational functions; compare~\cite{sun-yang03} and~\cite{cmmr09}.

**自包含改写**：For a rational function f on the Riemann sphere, with Fatou set the equicontinuity set of the iterates and Julia set J(f) its complement: can the whole Julia set J(f) be a Lakes of Wada continuum, i.e., the common boundary of three or more disjoint domains? This problem is related to Makienko's conjecture concerning completely invariant domains and buried points of rational functions.

**判定理由**：Background open problem (with Makienko's conjecture) cited for context; not targeted by this paper.

**关联卡**：Same Lakes-of-Wada theme as Fatou's Question 1.3 card, but for the whole Julia set of rational maps.

### 🔵 `OP-7BF34FE904DD` — `background_open` | MSC 37F10 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, paragraph on the Eremenko-Lyubich and Speiser classes
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> it was shown that a stronger version of Eremenko's conjecture, also stated in~\cite{eremenko89}~-- that every escaping point can be connected to infinity by a curve consisting of escaping points~-- holds for a large subclass of $\B$, but fails for general $f\in\B$. According to Bishop (personal communication), the question whether such counterexamples can also be constructed in~$\mathcal{S}$ was one of the original motivations for his technique of quasiconformal folding~\cite{bishop15}, which has revolutionised the study of the classes $\B$ and $\mathcal{S}$.

**自包含改写**：The strong Eremenko conjecture (Eremenko 1989): every escaping point of a transcendental entire function f can be connected to infinity by a curve consisting of escaping points, i.e., a curve in I(f) = {z in C : f^n(z) -> infinity}. It holds for a large subclass of the Eremenko-Lyubich class B (transcendental entire functions with bounded singular value set) but fails for general f in B (Rottenfusser-Ruckert-Rempe-Schleicher). Open question, attributed to Bishop (personal communication) and cited as background motivation: can such counterexamples (functions with escaping points not connectable to infinity by a curve in I(f)) also be constructed in the Speiser class S (transcendental entire functions with finitely many singular values)?

**判定理由**：External question (Bishop) cited as background motivation for quasiconformal folding; not this paper's own target.

**关联卡**：Strong-Eremenko context of the Eremenko conjecture card; this paper also gives new (simpler) counterexamples to the strong conjecture for general entire functions (Theorem on full continua), but not in class S.

### 🔵 `OP-E65A91FCFC3F` — `background_open` | MSC 37F10 | 难度 hard

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, discussion of Siegel disc boundaries following Question 1.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Both problems remain open for polynomials of degree at least three, but it seems reasonable to expect that, for polynomials and rational maps, the answer to Question~\ref{qu:fatou} is negative.

**自包含改写**：Let f be a polynomial of degree at least three (or a rational map of the Riemann sphere), with Fatou set the equicontinuity set of its iterates (spherical distance) and Fatou components its connected components. Two problems: (1) Fatou's 1920 question: if f has more than two Fatou components, can two of them share the same boundary (a common, Lakes-of-Wada-type boundary)? (2) Siegel disc boundary topology: if Delta is a Siegel disc of f (a periodic Fatou component conjugate to an irrational rotation), is f injective on the orbit of the closure of Delta (ruling out Lakes of Wada boundaries)? Dudko-Lyubich announced injectivity for quadratic polynomials with no restriction on rotation number, answering (1) negatively for quadratics. Both problems remain open for polynomials of degree at least three; the authors state it seems reasonable to expect that, for polynomials and rational maps, the answer to Fatou's question is negative.

**判定理由**：Open problems of Fatou (1920) and Siegel-disc topology cited as context; not this paper's own target (it targets entire functions).

**⚠️ 人工复核标记**：Referent of 'Both problems' inferred from the preceding sentences: (1) Fatou's shared-boundary question and (2) injectivity of f on the orbit of a Siegel disc closure / Siegel disc boundary topology.

**关联卡**：Companion card: Fatou's Question 1.3, answered positively by this paper for transcendental entire functions.

### 🔴 `OP-590B28C4C511` — `solved_in_paper` | MSC 37F10 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, Question 1.7 (qu:boc-thaler), from Boc Thaler 2021
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Is it true that the closure of any bounded simply connected Fatou component of an entire function has a connected complement?

**自包含改写**：Let U be a bounded simply connected Fatou component (connected component of the equicontinuity/Fatou set) of an entire function f. Boc Thaler's question: is the complement C \ (closure of U) connected? The paper answers negatively: the Fatou components from Theorem 1.4 have a Lakes of Wada continuum as common boundary, so the complement of the closure of such a component has at least two connected components.

**判定理由**：Question explicitly answered negatively by the paper's Lakes of Wada example.

**关联卡**：Refined by the paper's own Question 1.16 (fill card) in light of Theorem 1.7.

### 🔴 `OP-631BB8D33D13` — `solved_in_paper` | MSC 37F10 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, Question 1.3 (qu:fatou), quoting Fatou 1920 pp. 51-52
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> If $f$ has more than two Fatou components, can two of these components share the same boundary?

**自包含改写**：For f a rational self-map of the Riemann sphere (Fatou's 1920 setting) or a transcendental entire function f: C -> C, let the Fatou set F(f) be the largest open set on which the iterates of f are equicontinuous with respect to spherical distance; its connected components are the Fatou components. Fatou's question: if f has more than two Fatou components, can two of these components share the same boundary? The paper gives a positive answer in the transcendental entire setting (Theorem 1.4: there exists a transcendental entire f with an infinite collection of Fatou components all sharing the same boundary, which is a Lakes of Wada continuum). The original rational-function version remains open (see companion card on polynomials of degree at least three).

**判定理由**：Famous 1920 question; the paper proves the positive transcendental-entire analogue, which it explicitly adopts as its target.

**⚠️ 人工复核标记**：Solved only in the transcendental entire setting; Fatou's original rational-function version remains open for polynomials of degree at least three (companion card).

**关联卡**：Companion cards: 'Both problems remain open for polynomials of degree at least three' and Boc Thaler's question, answered by the same construction.

### 🔴 `OP-799E232D9EFB` — `solved_in_paper` | MSC 37F10 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, Conjecture 1.1 (conj:eremenko)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Every connected component of the escaping set of a transcendental entire function is unbounded.

**自包含改写**：Let f be a transcendental entire function and I(f) = {z in C : f^n(z) -> infinity as n -> infinity} its escaping set. Eremenko's conjecture (1989): every connected component of I(f) is unbounded. The paper disproves it: Theorem 1.2 shows that for every non-empty full (i.e., C \ X connected) and connected compact set X in C there exists a transcendental entire function f such that X is a connected component of I(f).

**判定理由**：Central conjecture explicitly targeted and disproved by the paper's Theorem 1.2 counterexamples.

**关联卡**：Related cards: remaining finite-order/class-B cases (Further-questions card) and the strong Eremenko conjecture in the Speiser class card.

### 🔴 `OP-E81FE6DFFEA5` — `solved_in_paper` | MSC 37F10 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, Question 1.5 (qu:rippon), from Hayman-Lingham Problem 2.94
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> If $U$ is a bounded escaping wandering domain of a transcendental entire function $f$, is $\partial U\subseteq \I(f)$?

**自包含改写**：Let f be a transcendental entire function, I(f) = {z in C : f^n(z) -> infinity as n -> infinity} its escaping set, and U a wandering Fatou component (a Fatou component that is neither periodic nor preperiodic). U is a bounded escaping wandering domain if U is bounded as a subset of C and U is contained in I(f). Rippon's question: is the boundary of U contained in I(f)? The paper answers negatively: Theorem 1.6 constructs a transcendental entire function f with a bounded escaping wandering domain U such that the boundary of U is not contained in I(f); the set of non-escaping boundary points can even have positive planar Lebesgue measure.

**判定理由**：Question explicitly answered in the negative by Theorem 1.6 of this paper.

**关联卡**：Motivates the maverick-point questions; the constructed boundary points are maverick points (logarithmic-capacity card).


## `2210.09581` — Sticky Kakeya sets and the sticky Kakeya conjecture
- 权威出处：**Journal of the American Mathematical Society** 2025，DOI `10.1090/jams/1067`
- 连接方式：`doi`｜全文 290,639 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟢 `OP-13B956F37963` — `real_open` | MSC 28A75 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), Conjecture \ref{stickyKakeyaConj}, immediately after Definition \ref{defnStickyKakeya} of sticky Kakeya sets; reiterated in the abstract ('We propose a special case of the Kakeya conjecture ... We prove this conjecture in three dimensions.')
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes (no numeric ranges; universally quantified over n) | solved_in_this_paper: partially — n=3 proved (Theorem mainThm), n≥4 open

**原文引文**

> Every sticky Kakeya set in $\RR^n$ has Hausdorff and Minkowski dimension $n$.

**自包含改写**：A compact set K ⊂ ℝ^n is a sticky Kakeya set if there is a set L of (affine) lines in ℝ^n, of packing dimension n−1 (packing dimension with respect to the metric d(ℓ,ℓ′) = |p−p′| + ∠(u,u′) on the space of lines, where u,u′ are unit vectors parallel to ℓ,ℓ′ and p,p′ are the unique points of ℓ,ℓ′ with p ⊥ u, p′ ⊥ u′), that contains at least one line in each direction and such that ℓ ∩ K contains a unit interval for every ℓ ∈ L. Conjecture (posed by this paper): every sticky Kakeya set in ℝ^n has both Hausdorff and Minkowski dimension n, for every n. Status within the paper: the case n = 3 is proved (the paper's Theorem \ref{mainThm}: 'Every sticky Kakeya set in ℝ³ has Hausdorff dimension 3', which also forces Minkowski dimension 3 since Hausdorff dimension ≤ lower/upper Minkowski dimension ≤ n); the case n = 2 follows from Davies' theorem quoted in the paper; the cases n ≥ 4 are left open.

**判定理由**：Central conjecture posed by this paper; proved here only for n = 3 and previously known for n = 2; the full statement (all n, in particular n ≥ 4) is a genuine unresolved proposition.

**关联卡**：Special case of the background Kakeya set conjecture card. Its n = 3 instance is Theorem mainThm, and its quantitative strengthening for sets η-close to sticky is Theorem mainThm′ ('For all ε>0 there is η>0 such that every Kakeya set K ⊂ ℝ³ that is η-close to being sticky satisfies dim_H K ≥ 3−ε'), both proved in the paper; the open n ≥ 4 cases connect to the higher-dimensional outlook card.

**存疑**：Conjecture/theorem numbering in the compiled article may differ from the LaTeX labels quoted here; items are identified by their label names (stickyKakeyaConj, mainThm, etc.).

### 🟢 `OP-84B660E0C081` — `real_open` | MSC 28A75 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.2 ('The sticky Kakeya conjecture versus the Kakeya conjecture'), Conjecture \ref{extremalIsStickyConj}, introduced by 'The following version of Katz and Tao's conjecture says that Kakeya sets that are nearly extremal are close to being sticky.'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Suppose the Kakeya conjecture in $\RR^n$ is false, i.e. $\inf \dim_H K = d<n$, where the infimum is taken over all Kakeya sets in $\RR^n$. Then for all $\eps>0$, there exists $\eta>0$ so that the following holds. Let $K\subset\RR^n$ be a Kakeya set with $\dim_H(K)\leq d+\eta$. Then $K$ is $\eps$-close to being sticky.

**自包含改写**：A Kakeya set in ℝ^n is a compact set containing a unit line segment in every direction; dim_H denotes Hausdorff dimension; a Kakeya set K ⊂ ℝ^n is ε-close to being sticky if there is a set of lines L with packing dimension at most n−1+ε that contains at least one line in each direction, such that ℓ ∩ K contains a unit interval for each ℓ ∈ L. Conjecture (this paper's numbered formulation of a 2014 conjecture of Nets Katz and Terence Tao from Tao's blog): if the Kakeya conjecture in ℝ^n is false, i.e. if d := inf{dim_H K : K a Kakeya set in ℝ^n} < n, then for all ε > 0 there exists η > 0 such that every Kakeya set K ⊂ ℝ^n with dim_H K ≤ d + η is ε-close to being sticky.

**判定理由**：Numbered conjecture stated and adopted by this paper, reformulating Katz–Tao's blog conjecture; unresolved at paper time and explicitly set aside ('We will not discuss Conjectures ... further').

**关联卡**：The paper proves this conjecture for n = 3, combined with its Theorem mainThm′, would imply the Kakeya conjecture in ℝ³; the underlying issue is stated as 'it is unclear whether K must be sticky'; the SL₂ example of Katz–Zahl (not itself a Kakeya set) is cited as evidence that far-from-sticky sets must also be understood. Linked to the far-from-sticky research-direction card.

### 🟢 `OP-C1EE6A0F3AFB` — `real_open` | MSC 28A75 | 难度 medium

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.2, Conjecture \ref{sl2Conj}, preceded by 'We conjecture that lines from this set cannot be used to construct a counter-example to the Kakeya conjecture.' and followed by the note 'Added November 3, 2022: Fässler and Orponen \cite{FO} have recently proved Conjecture \ref{sl2Conj}.'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no (external resolution announced in the paper's added note)

**原文引文**

> Let $K\subset\RR^3$ be compact, and suppose there is a set of lines $L\subset \mathcal L_{SL_2}$ that contains at least one line in each direction, so that $\ell\cap K$ contains a unit interval for each $\ell\in L$. Then $K$ has Hausdorff and Minkowski dimension 3.

**自包含改写**：Let 𝓛_{SL₂} be the set of lines in ℝ³ that can be written either in the form (a,b,0) + ℝ(c,d,1) with ad − bc = 1, or in the form (0,0,0) + ℝ(c,d,0); equivalently, 𝓛_{SL₂} is the set of horizontal lines in the first Heisenberg group. Conjecture (posed by this paper): if K ⊂ ℝ³ is compact and there exists a set of lines L ⊂ 𝓛_{SL₂} containing at least one line in each direction such that ℓ ∩ K contains a unit interval for each ℓ ∈ L, then K has Hausdorff and Minkowski dimension 3. The paper's added note (November 3, 2022) records that Fässler and Orponen have since proved this conjecture.

**判定理由**：Decidable proposition posed by this paper as its own conjecture; open when posed; the announced resolution is external (Fässler–Orponen), so it is not 'solved in paper'.

**⚠️ 人工复核标记**：The source contains an added note dated November 3, 2022 stating that Fässler–Orponen [FO, Bull. Lond. Math. Soc. 55(5):2195–2204, 2023] have proved this conjecture; the label reflects its status when posed, and the literature-tracking stage should mark it resolved via [FO].

**关联卡**：Motivated by the research-direction card on studying Kakeya sets far from sticky (the SL₂ example); structurally analogous to the sticky Kakeya conjecture, with the (n−1)-dimensional line family replaced by 𝓛_{SL₂}.

**存疑**：Label ambiguity: the conjecture is posed by this paper, but the paper itself records an external resolution in an added note; no taxonomy label exactly captures 'posed here, solved elsewhere during revision'.

### 🔵 `OP-6EC65C806115` — `background_open` | MSC 42B25 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), first paragraph, together with display Equation (1.1) (\label{KakeyaMaximalFnEstimate}).
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes (range 1≤d≤n and exponent n/d−1+ε copied from source) | solved_in_this_paper: no

**原文引文**

> There is also a slightly more technical, single-scale variant of this conjecture, which is called the Kakeya maximal function conjecture: let $\delta>0$ and let $\tubes$ be a set of $1\times\delta$ tubes in $\RR^n$ whose coaxial lines point in $\delta$-separated directions. Then the tubes must be almost disjoint, in the sense that for every $1\leq d\leq n$ and every $\eps>0$, there exists $C=C(n,d,\eps)$ (independent of $\delta$) so that \Big\Vert \sum_{T\in\tubes}\chi_T \Big\Vert_{\frac{d}{d-1}} \leq C\Big(\frac{1}{\delta}\Big)^{\frac{n}{d}-1+\eps}\Big(\sum_{T\in\tubes}|T|\Big)^{\frac{d-1}{d}}.

**自包含改写**：For δ > 0, let 𝕋 be a set of 1×δ tubes in ℝ^n whose coaxial lines point in δ-separated directions. The Kakeya maximal function conjecture asserts: for every 1 ≤ d ≤ n and every ε > 0 there exists C = C(n,d,ε), independent of δ, such that ‖Σ_{T∈𝕋} χ_T‖_{L^{d/(d−1)}} ≤ C (1/δ)^{(n/d)−1+ε} (Σ_{T∈𝕋} |T|)^{(d−1)/d}, where |T| denotes tube volume. Proved for n = 2 by Córdoba; open for n ≥ 3 at the time of writing; quoted by this paper only as background.

**判定理由**：Classic single-scale companion conjecture quoted purely as background; known for n=2 (Córdoba), open for n≥3; not posed or targeted by this paper.

**关联卡**：Companion background conjecture to the Kakeya set conjecture card; the paper's Proposition smallL3Norm / Corollary bigL3Norm are twisted-projection analogues of this type of estimate used to prove σ₃ = 0.

### 🔵 `OP-AD21B77E29EC` — `background_open` | MSC 28A75 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), first paragraph; the status 'The conjectures remain open in three and higher dimensions' is stated a few sentences later.
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> A compact set $K\subset\RR^n$ is called a \emph{Kakeya set} if it contains a unit line segment pointing in every direction. A surprising construction by Besicovitch \cite{bes} shows that such sets can have measure 0. The Kakeya set conjecture asserts that every Kakeya set in $\RR^n$ has Hausdorff and Minkowski dimension $n$.

**自包含改写**：A Kakeya set in ℝ^n is a compact set K ⊂ ℝ^n that contains a unit line segment pointing in every direction (Besicovitch: such sets can have Lebesgue measure 0). The Kakeya set conjecture asserts that every Kakeya set in ℝ^n has Hausdorff and Minkowski dimension n. It was known for n = 2 (Davies) and open for all n ≥ 3 at the time of writing; the paper cites it purely as background/motivation and attacks only the sticky special case.

**判定理由**：Famous open problem cited as background and motivation; the paper works only on the sticky subclass and never adopts the full conjecture as its own target.

**关联卡**：The paper's sticky Kakeya conjecture is a special case; the paper proves that the Katz–Tao extremal-is-sticky conjecture (for n = 3) combined with its Theorem mainThm′ would imply this conjecture for n = 3.

### 🟠 `OP-0EE2C39AFC20` — `method_obstruction` | MSC 28A75 | 难度 easy

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 4 ('The global grains slope function is C²'), Remark immediately after Theorem \ref{SWThm}.
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes (the ℂ-counterexample is constructed in the paper's remark)

**原文引文**

> Note that the statement of Theorem \ref{SWThm} makes sense over $\CC$ (with all exponents doubled), but the theorem is false. To construct a counter-example, let $\Omega \subset\CC^2$ be a neighbourhood of the origin and let $F=G=\{(z,\bar z)\colon z\in\CC\}\cap \Omega$; these are $(\delta, 2, O(1))$-sets.

**自包含改写**：Theorem SWThm (proved in the paper over ℝ) states: for all ε>0 there exist η,δ₀>0 such that for all δ∈(0,δ₀], if F,G ⊂ [0,1]² are (δ,1,δ^{−η})-ADsets, then either (A) there are orthogonal lines ℓ, ℓ^⊥ with δ-covering numbers 𝓔_δ(N_δ(ℓ)∩F) ≥ δ^{ε−1} and 𝓔_δ(N_δ(ℓ^⊥)∩G) ≥ δ^{ε−1}, or (B) for every ℋ ⊂ F×G×G with 𝓔_δ(ℋ) ≥ δ^{η−3} there exist ρ ≥ δ and an interval I with |I| ≥ δ^{−η}ρ such that 𝓔_ρ(I ∩ {a·(b₁−b₂) : (a,b₁,b₂) ∈ ℋ}) ≥ (|I|/ρ)^{1−ε}. The paper shows that the analogous statement over ℂ (all exponents doubled) is FALSE, via F = G = {(z, z̄) : z ∈ ℂ} ∩ Ω for a neighborhood Ω of the origin in ℂ²: (A) fails since 𝓔_δ(N_δ(ℓ)∩F) ≤ δ^{−1} ≪ δ^{−2+ε} for every complex line ℓ, and (B) fails since {ω·(ζ₁−ζ₂)} ⊂ {z : Im z = 0}. This marks precisely where the proof of the sticky Kakeya conjecture in ℝ³ uses the field ℝ (through Bourgain's discretized sum-product) and distinguishes ℝ³ from the complex Heisenberg group example.

**判定理由**：The paper constructs an explicit counterexample showing the ℂ-analogue of its key dot-product dichotomy fails — the real-field hypothesis is shown necessary; no open problem is posed.

**关联卡**：Companion observations in the paper: the analogue of Proposition weakNonConcentrationOnLinesImpliesConclusionBProp 'is not true if we replace the field ℝ by ℂ' (it relies on Bourgain's discretized sum-product), whereas Lemma largeDotProductThinTubesProp does hold over ℂ; together these pinpoint where the field ℝ is essential.

### 🟠 `OP-9DD292E0DA6B` — `method_obstruction` | MSC 28A75 | 难度 easy

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 7 ('Proof of Theorem SWThm'), subsection 'Grabbing the bootstraps', remark between Corollary \ref{quarterThinTubesCor} and Lemma \ref{lem: liushen}.
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes (σ∈[1/4,1−ε] and the λ-versus-ζ constraint copied from source) | solved_in_this_paper: yes (the failure is demonstrated in the remark)

**原文引文**

> It is tempting to avoid Lemma \ref{lem: liushen} by instead iterating Proposition \ref{bootstrapLem}$'$ multiple times starting with $\sigma = \beta = \zeta$ rather than $\sigma = \beta = 1/4$. Unfortunately, this would require $O_{\zeta,\eps}(1)$ iterations, and this in turn would mean that the quantity $\lambda=\lambda(\eps)$ from Proposition \ref{weakNonConcentrationOnLinesImpliesConclusionBProp} would also have to be sufficiently small  depending on $\zeta$ (in particular, much smaller than $\zeta$). This is not acceptable, because in our application below we must use a value of $\lambda$ that is at least as large as $\zeta$.

**自包含改写**：In the proof of the dot-product dichotomy (Theorem SWThm′), the bootstrapping device (Proposition bootstrapLem′) says: if G₁,G₂ ⊂ [0,1]² are (δ,1,C)-Frostman sets with dist(G₁,G₂) ≥ 1/2 and both ordered pairs (G₁,G₂), (G₂,G₁) have δ-discretized (σ,K,1−c)-thin tubes, then for any ε>0 and σ ∈ [1/4, 1−ε] both pairs have (σ+τ,K′,1−3c)-thin tubes for some τ = τ(ε) > 0. The paper documents that the tempting simplification of iterating this bootstrapping starting from σ = ζ (instead of σ = 1/4), so as to avoid the auxiliary Lemma liushen, fails: it would force the parameter λ = λ(ε) of the radial-projection proposition (Proposition weakNonConcentrationOnLinesImpliesConclusionBProp) to be much smaller than ζ, whereas the application requires λ ≥ ζ. Hence this route cannot dispense with the extra real-field input.

**判定理由**：The paper documents that a natural simplification of its bootstrapping argument fails for a parameter-dependence reason; no open problem is posed.

**关联卡**：Internal obstruction within the proof of Theorem SWThm (Section 7); complements the ℂ-falsity method-obstruction card.

### ⚪ `OP-0FCA737BE865` — `future_application` | MSC 28A75 | 难度 frontier

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.1 ('A sketch of the proof'), Step 1: Discretization and multi-scale self-similarity (describing Section 2, 'Discretization').
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no (outlook only)

**原文引文**

> The technical details of this procedure are new; in particular, we explain how to replace each $1\times\delta$ tube by a reasonably large subset (called a shading), so that key statistics of the Kakeya set are maintained after successive refinements. We hope that this setup will be useful when studying the sticky Kakeya conjecture in higher dimensions.

**自包含改写**：Not a mathematical proposition — an application outlook, explicitly stated as hope. The authors express the expectation that the paper's multi-scale discretization machinery for the sticky Kakeya problem (replacing each 1×δ tube by a shading, i.e., a union of δ-cubes of reasonably large size inside the tube, arranged so that key statistics of the Kakeya set are preserved under successive refinements) will be useful for attacking the sticky Kakeya conjecture — that every sticky Kakeya set in ℝ^n has Hausdorff and Minkowski dimension n — in dimensions n ≥ 4, where it remains open.

**判定理由**：Explicit hope/taste statement about future usefulness of a technical framework; not a decidable proposition, so it must not be taskified.

**关联卡**：Points toward the open n ≥ 4 cases of the sticky Kakeya conjecture card.

### ⚪ `OP-1273D77E88A2` — `future_application` | MSC 28A75 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 3 ('Extremal families of tubes and multi-scale structure'), unnumbered Remark immediately after the proof of Proposition \ref{multiScaleStructureExtremal}.
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes (scale range ρ∈[δ^{1−ε},δ^ε] and multiplicity exponents copied from source) | solved_in_this_paper: no (outlook only)

**原文引文**

> The conclusions of Lemma \ref{existenceOfExtremalFamilies} and Proposition \ref{multiScaleStructureExtremal} are the only consequences of stickiness that we will use to prove Theorem \ref{mainThm}. In particular, if Lemma \ref{existenceOfExtremalFamilies} and Proposition \ref{multiScaleStructureExtremal} hold for some other class of Kakeya sets, then it should be possible to prove the analogue of Theorem \ref{mainThm} in that setting as well.

**自包含改写**：Not a mathematical proposition — a methodological outlook. The authors observe that the only consequences of stickiness used in proving their main theorem (every sticky Kakeya set in ℝ³ has Hausdorff dimension 3) are: Lemma existenceOfExtremalFamilies (for all ε,δ₀ > 0 there exists an ε-extremal pair (𝕋,Y)_δ of δ-tubes with shadings for some δ ∈ (0,δ₀]) and Proposition multiScaleStructureExtremal (for all ε > 0 there exist η,δ₀ > 0 such that every η-extremal (𝕋,Y)_δ admits, for each ρ ∈ [δ^{1−ε}, δ^ε], a refinement and a balanced ε-extremal cover by ρ-tubes, with per-point tube multiplicities at most ρ^{−σ_n−ε} at the coarse scale and (δ/ρ)^{−σ_n−ε} at the fine scale). They state the expectation ('it should be possible') that if these two statements hold for some other class of Kakeya sets, then the analogue of the main theorem can be proved in that setting.

**判定理由**：Conditional 'it should be possible' expectation about transferring the method to other classes of sets; not posed as a proposition.

**关联卡**：Describes the minimal structural inputs (existence of extremal tube families plus multi-scale self-similarity) behind the paper's proof of the sticky Kakeya conjecture in ℝ³; related to the higher-dimensional outlook card.

### ⚪ `OP-9BB24E8A4CA0` — `future_application` | MSC 28A75 | 难度 frontier

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.2 ('The sticky Kakeya conjecture versus the Kakeya conjecture'), paragraph following the introduction of the SL₂ example (between Conjectures \ref{extremalIsStickyConj} and \ref{sl2Conj}).
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes (no numeric ranges) | solved_in_this_paper: no (direction only)

**原文引文**

> The $SL_2$ example is not a counter-example to Conjecture \ref{extremalIsStickyConj} (nor to the Kakeya conjecture) because it is not a Kakeya set in $\RR^3$. Nonetheless, the existence of the $SL_2$ example suggests that in order to resolve the Kakeya conjecture in $\RR^3$, it will be necessary to study Kakeya sets that are far from sticky.

**自包含改写**：Not a mathematical proposition — a programmatic research direction. The SL₂ example of Katz and Zahl (cited as [KZ]) is a Kakeya-like object built from the line family 𝓛_{SL₂} = {(a,b,0) + ℝ(c,d,1) : ad − bc = 1} ∪ {(0,0,0) + ℝ(c,d,0)} (equivalently, the horizontal lines of the first Heisenberg group) that has small volume at certain scales and is not sticky; it is not itself a Kakeya set in ℝ³. The authors assert the research direction that, because of this example, resolving the Kakeya conjecture in ℝ³ (every Kakeya set in ℝ³ has Hausdorff and Minkowski dimension 3) will require studying Kakeya sets that are far from sticky — i.e., going beyond the sticky regime handled by this paper.

**判定理由**：Programmatic statement of necessity ('it will be necessary to study'); a research direction/outlook, not a decidable proposition.

**关联卡**：Directly motivates the SL₂-line conjecture card (sl2Conj, resolved by Fässler–Orponen per the paper's added note) and complements the Katz–Tao extremal-is-sticky conjecture card.


## `2001.10425` — Purity in chromatically localized algebraic 𝐾-theory
- 权威出处：**Journal of the American Mathematical Society** 2024，DOI `10.1090/jams/1043`
- 连接方式：`doi`｜全文 99,442 字符 via `cache-latex`｜提取模式 `fast`

### 🟢 `OP-9A156286FE51` — `real_open` | MSC 19D55 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 4.2, Remark after the corollary on K(BP⟨n⟩) → K(E(n))
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Whether or
ot  this sequence is a fibre sequence (after replacing the rings with their
$p$-completions) was asked by Rognes, the $n=1$ case being a theorem of
Blumberg--Mandell \cite{BM}, and the $n=0$ case being a classical theorem of
Quillen's.

**自包含改写**：For n≥0 (with p-completions taken), is the sequence K(BP⟨n-1⟩) → K(BP⟨n⟩) → K(E(n)) of nonconnective algebraic K-theory spectra a fibre sequence? Here BP⟨n⟩ denotes the nth truncated Brown–Peterson spectrum and E(n) the nth Johnson–Wilson spectrum, both p-completed. Known cases: n=0 (Quillen), n=1 (Blumberg–Mandell); for n≥2 Antieau–Barthel–Gepner showed the sequence is NOT a fibre sequence after rationalization. This paper proves it becomes a fibre sequence after T(i)-localization for i≥n+1.

**判定理由**：A question of Rognes explicitly adopted and discussed by this paper; the integral statement remains open for n≥2, though the paper proves the T(i)-local (i≥n+1) version.

**⚠️ 人工复核标记**：The paper itself only proves the T(i)-local version for i≥n+1, not the integral statement; the integral question's status is not settled here.

**存疑**：The original question's precise formulation (e.g., connective vs nonconnective K-theory) is summarized here from the paper's paraphrase of Rognes.

### 🟢 `OP-A6CD7CCD2377` — `real_open` | MSC 19D55 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 3, Question (immediately after Remark on CMNN-argument)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> For a ring spectrum $A$ and for $n \geq 2$, does the map $A \to L_{K(n-1) \oplus K(n)} A$ induce an equivalence on $K(n)$-local $K$-theory?

**自包含改写**：For a fixed prime p, n≥2, a ring spectrum A (E_1-ring spectrum), and Morava K-theories K(i) at the implicit prime p, does the canonical map A → L_{K(n-1)⊕K(n)}A induce an equivalence on K(n)-local algebraic K-theory, i.e. is L_{K(n)}K(A) → L_{K(n)}K(L_{K(n-1)⊕K(n)}A) an equivalence? The paper notes this would follow from showing that A → L_nA induces an equivalence on L_{K(n)}K(-) for n≥2 (L_n being Bousfield localization at K(0)⊕…⊕K(n)).

**判定理由**：Formally posed Question in the paper, left unresolved; a K(n)-local (harmonic) analog of the paper's T(n)-local purity theorem.

**⚠️ 人工复核标记**：The original Question is posed only for n≥2 (not n=1); the suggested reduction via L_n-localization is also stated for n≥2.

**关联卡**：K(n)-local counterpart of the T(n)-local Purity Theorem proved in this paper.

### 🔵 `OP-A04316FCD069` — `background_open` | MSC 55U35 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 2.1, remark after Lemma 'basicproperties'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We remark that the converse of statement (iv) (for $n\geq 1$) is the content of the telescope conjecture. It is known \cite{Mahowald,
Miller} 
to be true in height $n=1$ and was recently disproved at all higher heights and all primes
\cite{BHLS}.

**自包含改写**：The telescope conjecture: for n≥1, any K(n)-acyclic spectrum is T(n)-acyclic (i.e., K(n)- and T(n)-localizations agree); true at height 1 (Mahowald, Miller) and disproved at all heights n≥2 and all primes (Burklund–Hahn–Levy–Schlank).

**判定理由**：Classical background conjecture cited for context; known true at n=1 and famously disproved at higher heights; not a target of this paper.

**⚠️ 人工复核标记**：The paper states the conjecture is already disproved at heights ≥2 at time of writing, so this card records settled background rather than an open problem.

### 🟠 `OP-106E4472848B` — `method_obstruction` | MSC 19D55 | 难度 medium

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction and Remark 'purity:optimal'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> The purity theorem is optimal in the sense that the functor $A \mapsto L_{T(n)} K(A)$ does not factor through either $A \mapsto L_{T(n-1)}A$ or $A \mapsto L_{T(n)}A$
(see \Cref{purity:optimal} below).

**自包含改写**：For n≥1 and a fixed prime p, the functor A ↦ L_{T(n)}K(A) on ring spectra does not factor through either A ↦ L_{T(n)}A or A ↦ L_{T(n-1)}A: examples from Hahn–Wilson and Yuan give T(n)-acyclic ring spectra A with L_{T(n)}K(A)≠0, and if all T(n−1)-equivalences induced equivalences on L_{T(n)}K(−), the square-zero extensions S⊕Σ^rM (M connective, T(n−1)-acyclic, not T(n)-acyclic) would force colim_r Ω^r fib(K(S⊕Σ^rM)→K(S)) to be T(n)-acyclic, contradicting its identification with ΩM via topological Hochschild homology.

**判定理由**：Shows the purity localization L_{T(n-1)⊕T(n)} cannot be weakened; not a posed open problem but a sharpness/obstruction result.

**关联卡**：Establishes optimality of the solved purity question (main question of the paper).

### 🟠 `OP-D0170B792ADF` — `method_obstruction` | MSC 19D55 | 难度 medium

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 4.4, Remark 'TC-version-of-question'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> The analog of Corollary~\ref{cor:K1local-truncating} for topological cyclic homology does not hold:

**自包含改写**：The TC-analog of the statement 'for a K(1)-acyclic ring spectrum A, L_{K(1)}K(A) = L_{K(1)}K(A[1/p])' fails: TC(Z[1/p]) vanishes p-adically (hence T(1)-locally), but L_{K(1)}TC(Z) ≠ 0, since for odd p, Bökstedt–Madsen computed the connective cover of TC(Z)^_p as j ⊕ Σj ⊕ Σ^3 ku^_p (j the connective cover of the K(1)-local sphere), and nonvanishing at p=2 follows from Rognes's filtration.

**判定理由**：The paper demonstrates that a natural method transfer (TC replacing K) fails, without posing a new problem.

### 🔴 `OP-0F7FBEFF6C78` — `solved_in_paper` | MSC 19D55 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, after the discussion of Bhatt--Clausen--Mathew
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> For general height $n$, to what extent does the $T(n)$-local $K$-theory of a ring spectrum $A$  depend only on telescopic localizations of $A$ ?

**自包含改写**：For a fixed prime p and n≥1, determine to what extent the T(n)-localization of the (nonconnective) algebraic K-theory K(A) of a ring spectrum A (E_1-ring spectrum) depends only on telescopic localizations L_{T(i)}A of A; here T(n) denotes the telescope of a v_n-self map on a type n finite complex, with T(0)=S[1/p].

**判定理由**：The main goal of the paper; answered completely at all heights n≥1 by Theorem A and the Purity Theorem.

**关联卡**：Resolved by the Purity Theorem (card for Theorem A / Purity Theorem); the optimality of the answer is recorded in a separate method_obstruction card.

### 🔴 `OP-3D4BE6F76A28` — `solved_in_paper` | MSC 19D55 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, Redshift Theorem
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> For an $\E_\infty$-ring $R$ with $\hgt(R) \geq 0$, we have  $\hgt(K(R)) = \hgt(R)+1$.

**自包含改写**：For an E_∞-ring spectrum R with height ht(R) = inf{n≥−1 : R⊗T(n+1)=0} ≥ 0, the height of its algebraic K-theory satisfies ht(K(R)) = ht(R)+1. The paper proves the inequality ht(K(R)) ≤ ht(R)+1 (Theorem B); the converse inequality follows from Yuan's result ht(K(E_n)) ≥ ht(E_n)+1 for Lubin–Tate theories E_n and Burklund–Schlank–Yuan's higher chromatic Nullstellensatz.

**判定理由**：The paper proves the upper bound (Theorem B) and assembles the full redshift statement citing Yuan and Burklund–Schlank–Yuan for the converse; stated as a theorem.

**⚠️ 人工复核标记**：Only the inequality ht(K(R))≤ht(R)+1 is proved within this paper; the reverse inequality relies on external works [Yuan], [BSY] that postdate the first version.

**关联卡**：The paper's own contribution is Theorem B: ht(K(R)) ≤ ht(R)+1 for any E_∞-ring R, proved from the Purity Theorem.

### 🔴 `OP-4B39D0DECA76` — `solved_in_paper` | MSC 19D55 | 难度 medium

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 4.2, remark after Corollary 'truncatedsphere'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Ben Antieau has already shown previously that a certain quantitative version of Proposition~\ref{prop:E(n)-local-K-theory} implies $L_{T(n)}K(\tau_{\leq m}\bbS) = 0$ at least for all $n$ such that $4p-4\geq n$, where $p$ is the implicit prime in $T(n)$, and conjectured that \Cref{truncatedsphere} is true.

**自包含改写**：For any n≥0 and any m≥0, the algebraic K-theory of the mth Postnikov truncation τ_{≤m}S of the sphere spectrum vanishes T(i)-locally for all i≥2 (p any prime, implicit in T(i)); previously conjectured by Ben Antieau, who had proved it for n (height of localization) with 4p−4≥n.

**判定理由**：Corollary 'truncatedsphere' in the paper proves exactly the conjectured vanishing for all n≥0 and i≥2.

**⚠️ 人工复核标记**：Note the paper's Corollary states i≥2 while Antieau's prior partial result is stated with condition 4p−4≥n on the localization height; these are consistent formulations of the same vanishing.


## `2309.07123` — Descent and cyclotomic redshift for chromatically localized algebraic 𝐾-theory
- 权威出处：**Journal of the American Mathematical Society** 2024，DOI `10.1090/jams/1052`
- 连接方式：`doi`｜全文 207,040 字符 via `cache-latex`｜提取模式 `fast`

### 🟢 `OP-5D3B3852797B` — `real_open` | MSC 19D55 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, Section 1.1 (Background)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It is known that \cref{CMNN1} may fail for arbitrary finite groups $G$ (e.g.\ of order prime to $p$), but the question of whether \cref{CMNN2} holds in this generality is still open.

**自包含改写**：Let p be a prime, n >= 0, and let R -> S be a T(n)-local G-Galois extension of ring spectra in the sense of Rognes, where G is an arbitrary finite group (not necessarily a finite p-group). Clausen--Mathew--Naumann--Noel proved that if G is a finite p-group, then there is a canonical isomorphism L_{T(n+1)} K(R) ≅ (L_{T(n+1)} K(S))^{hG}. It is open whether this isomorphism holds for arbitrary finite groups G. (Note: the analogous statement for actions on categories, L_{T(n+1)} K(C^{hG}) ≅ L_{T(n+1)} K(C)^{hG} for L_n^f-local C, is known to fail for general finite G, e.g. of order prime to p.)

**判定理由**：The paper explicitly states that this descent question for arbitrary finite groups is still open at the time of writing.

**关联卡**：Related to the second card: this is the finite-group special case of the broader profinite Galois hyperdescent question.

### 🟢 `OP-618703851DCA` — `real_open` | MSC 19D55 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, Section 1.1 (Background)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> More generally, one can ask to what extent chromatically localized algebraic $K$-theory satisfies \textit{hyperdescent} for profinite Galois extensions. Of particular interest is the case of the Lubin--Tate spectrum $E_n$, which is a profinite Galois extension of the $K(n)$-local sphere with Morava stabilizer Galois group $\GG_n$. Namely, it is natural to ask whether the functor $U\mapsto \LTnp K(E_n^{hU})$ on open subgroups $U \le \GG_n$ corresponds to a hypersheaf on the site of continuous finite $\GG_n$-sets.

**自包含改写**：Let p be a prime, n >= 0, let E_n be the Lubin--Tate (Morava E-theory) spectrum of height n, and let Γ_n be the Morava stabilizer group, so that E_n is a profinite Γ_n-Galois extension of the K(n)-local sphere. Question: does the functor U ↦ L_{T(n+1)} K(E_n^{hU}), defined on open subgroups U ≤ Γ_n, correspond to a hypersheaf on the site of continuous finite Γ_n-sets? More generally, to what extent does chromatically localized algebraic K-theory satisfy hyperdescent for profinite Galois extensions?

**判定理由**：The paper poses this hypersheaf question as a natural open question; it proves special cases (cyclotomic hyperdescent for K(n+1)-localized K-theory) but not this one.

**⚠️ 人工复核标记**：The paper notes that even on the pro-p part of Γ_n the hypersheaf condition does not follow from the sheaf condition (citing Clausen--Mathew--Naumann--Noel, Example 4.17).

**关联卡**：Generalization of the first card; the paper's cyclotomic hyperdescent (Theorem 1.9 / Knp-hyper) resolves only the cyclotomic-tower case, not the full Γ_n question.

### 🟢 `OP-9393A9B7386C` — `real_open` | MSC 19D55 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, Section 1.4 (Hyperdescent and the Telescope Conjecture)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It is natural to ask whether the hyperdescent along the cyclotomic tower holds already on the level of telescopic localizations, or, equivalently, whether $\LTnp K(R)$ is cyclotomically complete for every $\Tn$-local ring spectrum $R$.

**自包含改写**：Let p be a prime, n >= 0, and R a T(n)-local ring spectrum. Question: is L_{T(n+1)} K(R) cyclotomically complete for every such R (i.e., is the cyclotomic completion map L_{T(n+1)}K(R) → R^{cyсл} L_{T(n+1)}K(R) an isomorphism), equivalently, does L_{T(n+1)}-localized K-theory satisfy hyperdescent along the cyclotomic tower of every T(n)-local ring? The companion work of Burklund--Hahn--Levy--Schlank constructs counterexamples for every n >= 1 and every prime, so the answer is negative in general.

**判定理由**：Genuine mathematical question posed in the paper; the negative answer is obtained in the cited companion paper [Telefalse], not proven in this paper itself.

**⚠️ 人工复核标记**：The paper states the counterexamples (for every n ≥ 1 and every prime) come from [Telefalse], a companion work, not from this paper.

**关联卡**：Combined with Theorem 1.9 (cyclotomic hyperdescent for K(n+1)-localized K-theory, solved in this paper), these counterexamples disprove the telescope conjecture at height 2 and above.

**存疑**：Status at paper time: the paper itself cites the negative resolution, so this question was already answered negatively by the companion paper when this paper was written; labeling kept as real_open since the paper poses it as its own target and uses it centrally.

### 🔵 `OP-8F51108079C0` — `background_open` | MSC 19D55 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, Section 1.1 (Background)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Based on computational evidence in chromatic height $1$, Ausoni--Rognes \cite{AR02, ausoni2008chromatic} formulated the far-reaching redshift conjecture, out of which emerged a wider philosophy, predicting the interaction of algebraic $K$-theory with chromatic height.
The conjecture states roughly that the process of categorification increases chromatic height by one.

**自包含改写**：The redshift conjecture of Ausoni--Rognes: roughly, the process of categorification (algebraic K-theory) increases chromatic height by one; i.e., if a ring spectrum or stable infinity-category has chromatic height n, its algebraic K-theory has chromatic height n+1. Cited as the motivating background philosophy for the paper.

**判定理由**：Famous background conjecture motivating the paper; the paper proves related descent/redshift statements but not the redshift conjecture itself.

**关联卡**：The paper's Theorem 1.6 (Cyclotomic Redshift) is a precise instance of this philosophy for cyclotomic extensions.

### 🔵 `OP-C23B50D357B2` — `background_open` | MSC 55P42 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, Section 1.4 (Hyperdescent and the Telescope Conjecture)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Ravenel originally conjectured that  $\SpKn = \SpTn$ for all heights and primes, but while it is known to hold for $n = 0,1$, it was soon suspected to be false for higher chromatic heights.

**自包含改写**：Ravenel's telescope conjecture: for every prime p and height n ≥ 0, the K(n)-local category of spectra coincides with the T(n)-local category (Sp_{K(n)} = Sp_{T(n)}). Known to hold for n = 0, 1; the paper explains that combining its Theorem 1.9 with the counterexamples of [Telefalse] disproves it at height 2 and above.

**判定理由**：Famous long-standing conjecture cited as background; its disproof relies on the companion paper [Telefalse], not on results proved here.

**⚠️ 人工复核标记**：The paper claims this paper's results combined with [Telefalse] disprove the telescope conjecture at height ≥ 2; the disproof itself is in the companion work.

**关联卡**：Closely tied to the third card: the failure of telescopic cyclotomic hyperdescent versus its K(n+1)-local counterpart is precisely the mechanism of disproof.

### 🟠 `OP-5AB3813083C1` — `method_obstruction` | MSC 19D55 | 难度 medium

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, Section 1.1 (Background)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It is known that \cref{CMNN1} may fail for arbitrary finite groups $G$ (e.g.\ of order prime to $p$),

**自包含改写**：The descent isomorphism L_{T(n+1)} K(C^{hG}) ≅ L_{T(n+1)} K(C)^{hG} for L_n^f-local stable infinity-categories C, which holds for finite p-groups G, is known to fail for arbitrary finite groups G, e.g. finite groups of order prime to p.

**判定理由**：Statement that a method/estimate fails beyond a hypothesis; no new open problem is posed here, but it delimits the p-group assumption as necessary.

**关联卡**：Contrasts with the first card: the category-level statement fails for general finite G, while the ring-level Corollary 1.3 generalization remains open.


## `2201.08152` — Computing Riemann–Roch polynomials and classifying hyper-Kähler fourfolds
- 权威出处：**Journal of the American Mathematical Society** 2023，DOI `10.1090/jams/1016`
- 连接方式：`doi`｜全文 128,809 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟢 `OP-1E6E9881268E` — `real_open` | MSC 14C20 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), Conjecture 1.5 (following the sentence 'We are naturally led to asking whether this conclusion still holds without assuming the existence of the Lagrangian fibration f.')
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Let $X$ be a \hk\ manifold of dimension $2n$ with  classes $\lll,\mm\in H^2(X,\Z)$ such that $\int_X\lll^{2n}=0\quad\textnormal{and}\quad\int_X\lll^n\mm^n=n!.$ Then the Huybrechts--Riemann--Roch polynomial of $X$  satisfies $\forall k\in\Z\qquad P_{RR,X}(2k)=\chi(\P^n,\cO_{\P^n}(k+1))=\binom{k+1+n}{n}$.

**自包含改写**：Conjecture posed by this paper: Let X be a hyper-Kähler manifold of complex dimension 2n and let λ, μ ∈ H²(X, Z) be integral degree-2 classes such that ∫_X λ^{2n} = 0 and ∫_X λ^n μ^n = n!. Then the Huybrechts–Riemann–Roch polynomial P_{RR,X} of X — the degree-n rational polynomial defined by χ(X, L) = P_{RR,X}(q_X(c₁(L))) for every line bundle L on X, where q_X is the Beauville–Bogomolov–Fujiki form — satisfies, for every integer k, P_{RR,X}(2k) = χ(P^n, O_{P^n}(k+1)) = binom(k+1+n, n). The paper proves the case n = 2 (i.e., ∫λ⁴ = 0 and ∫λ²μ² = 2) as Theorem 4.3 (= Theorem 1.7); the conjecture in general dimension 2n remains open. The paper notes this conjecture is not strictly implied by Theorem 3.1 plus the SYZ conjecture, since semi-ampleness only guarantees that some positive power of L is globally generated.

**判定理由**：Conjecture explicitly formulated by this paper; only the dimension-4 case (n = 2) is proved (Theorem 4.3 / Theorem 1.7), the general dimension case is left open.

**关联卡**：The special case n = 2 (∫λ⁴ = 0, ∫λ²μ² = 2) is solved in the paper (Theorem 4.3 / Theorem 1.7) and is the input to Theorem 1.3 and Theorem 1.6; see also the card on the Kamenova–Verbitsky global-generation question, which marks the logical gap between this conjecture and the SYZ conjecture.

### 🟢 `OP-2593ABC35B53` — `real_open` | MSC 53C26 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 8.2, final paragraph of the paper (discussion following Theorem 8.3)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Moreover, by~\cite[Proposition 5.6]{bs}, \cite[Conjecture 1.2]{bs} would imply that the Fujiki constant $c_X$ is either~$3$ or~$9$. In particular, the second case in~\ref{enum:th43b} should not occur.

**自包含改写**：Open question left by this paper (with predicted negative answer): Theorem 8.3(b) states that a hyper-Kähler fourfold X with classes λ, μ ∈ H²(X, Z) such that ∫_X λ⁴ = 0 and a := (1/2)∫_X λ²μ² = 4 has the Chern and Hodge numbers of the Hilbert square of a K3 surface and either (i) q_X(λ, μ) = 2, c_X = 3, q_X even, P_{RR,X}(T) = binom(T/2 + 3, 2) — realized on K3^[2]-type fourfolds with μ divisible by 2 — or (ii) q_X(λ, μ) = 1, c_X = 12, P_{RR,X}(T) = binom(T + 3, 2). Whether case (ii) is realized by any hyper-Kähler fourfold is left open; the paper predicts, on the basis of Conjecture 1.2 of Beckmann–Song [bs] (which via [bs, Proposition 5.6] would force the Fujiki constant c_X to be 3 or 9), that this second case should not occur.

**判定理由**：Occurrence of the second a=4 case of Theorem 8.3 is left undecided; the paper predicts non-occurrence, conditionally on the background Beckmann–Song conjecture.

**关联卡**：Companion to the a = 3 realizability card; the predicted non-occurrence rests on Conjecture 1.2 of Beckmann–Song [bs] concerning generalized Fujiki constants, cited here as background (the paper does not restate that conjecture).

**存疑**：The predicted non-occurrence is conditional on the Beckmann–Song conjecture; the paper itself does not prove non-occurrence of the second case.

### 🟢 `OP-87E73B1584D1` — `real_open` | MSC 53C26 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 8.2 ('Low values of a for hyper-Kähler fourfolds'), remark following Theorem 8.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> As we saw in Example~\ref{ex:Kumn},  the first item of the case $a=3$ in Theorem~\ref{th43} is realized by \hk\ fourfolds  of generalized Kummer deformation type;  we do not know whether the other two items occur.

**自包含改写**：Open question left by this paper: Theorem 8.3 states that a hyper-Kähler fourfold X with classes λ, μ ∈ H²(X, Z) such that ∫_X λ⁴ = 0 and a := (1/2)∫_X λ²μ² ∈ {2, …, 8} must have a = 3 or a = 4. In the case a = 3 one has q_X(λ, μ) = 1, c_X = 9, P_{RR,X}(T) = 3·binom(T/2 + 2, 2), q_X even, and (b₂(X), b₃(X), b₄(X)) ∈ {(7,8,108), (6,4,102), (5,0,96)}. The possibility (7,8,108) is realized by generalized Kummer fourfolds; the paper explicitly leaves open whether the other two Betti-number possibilities, (b₂, b₃, b₄) = (6,4,102) or (5,0,96), are realized by some hyper-Kähler fourfold with a = 3.

**判定理由**：'We do not know whether the other two items occur' — an explicit existence/realizability question the paper itself leaves open.

**关联卡**：Companion to the a = 4 realizability card (second case of Theorem 8.3(b)); both arise from the paper's '(incomplete) analysis' of small a in Section 8.2.

### 🔵 `OP-6142FD5C0C11` — `background_open` | MSC 53C26 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), paragraph following Conjecture 1.2
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It is conjectured that the base $B$ of any Lagrangian fibration is  smooth, and in fact $\P^n$; note that $B$ is smooth if and only if $f$ is flat.

**自包含改写**：Conjecture (background): If f : X → B is a Lagrangian fibration on a hyper-Kähler manifold X of complex dimension 2n (so B is a normal projective variety of dimension n by Matsushita's results), then the base B is smooth — equivalently, f is flat — and in fact B ≅ P^n. Known partial results: if B is smooth then B ≅ P^n (Hwang for X projective; Greb–Lehn in general); if X is projective and n = 2 (dimension 4), then B ≅ P² unconditionally (Ou; Huybrechts–Xu).

**判定理由**：General field conjecture on bases of Lagrangian fibrations, cited as background; the paper neither poses nor resolves it (its theorems produce bases already known to be P²).

### 🔵 `OP-79A4F0BF5954` — `background_open` | MSC 53C26 | 难度 hard

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), discussion following Conjecture 1.5
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The question of whether $L$ is generated by global sections, if a power induces a Lagrangian fibration, was recently studied  in~\cite{kv}, where the authors give  a sufficient condition for this to happen; unfortunately, their result does not apply in our situation.

**自包含改写**：Background open question (studied by Kamenova–Verbitsky in [kv]): if L is a nef line bundle on a hyper-Kähler manifold such that some positive tensor power L^{⊗m} is generated by global sections and its sections induce a Lagrangian fibration, must L itself be generated by global sections? The paper records that the sufficient condition proved in [kv] does not apply in the paper's situation (triples with a = (1/n!)∫_X λ^n μ^n = 1), which is why Conjecture 1.5 of the paper is not strictly implied by Theorem 3.1 plus the SYZ conjecture.

**判定理由**：Question originates in [kv] and is cited as context; the paper notes the known sufficient condition fails to apply here but neither poses nor resolves the question itself.

**关联卡**：Marks the logical gap between the paper's Conjecture 1.5 (Riemann–Roch polynomial card) and the SYZ conjecture: SYZ gives semi-ampleness (a power globally generated), whereas Conjecture 1.5 in the nef line bundle setting would need L itself globally generated.

### 🔵 `OP-7E278403F123` — `background_open` | MSC 53C26 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), Conjecture 1.2 ('hyper-Kähler SYZ conjecture')
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Let $X$ be a \hk\ manifold of dimension~$2n$. Any nontrivial nef line bundle $L$ on $X$ such that $\int_X c_1(L)^{2n}=0$ is semi-ample.

**自包含改写**：Conjecture (background, the hyper-Kähler SYZ conjecture): Let X be a hyper-Kähler manifold of complex dimension 2n over the complex numbers (simply connected smooth compact Kähler manifold with a nowhere-degenerate holomorphic 2-form unique up to scalar). Then any nontrivial nef line bundle L on X such that ∫_X c₁(L)^{2n} = 0 is semi-ample (i.e., some positive tensor power of L is generated by global sections). Known for the known deformation types (K3^[n], generalized Kummer, OG10, OG6) when c₁(L) is primitive (Theorem 1.2 of the paper); proved in this paper for fourfolds whose λ = c₁(L) admits μ ∈ H²(X, Z) with ∫λ⁴ = 0 and ∫λ²μ² = 2; open in general.

**判定理由**：Named field-wide conjecture quoted as motivation; the paper proves only the dimension-4 case under its additional topological hypothesis (Theorem 1.6), not the general statement.

**关联卡**：Theorem 1.6 (separate card) proves this conjecture for hyper-Kähler fourfolds with the extra assumptions ∫_X λ⁴ = 0 and ∫_X λ²μ² = 2; Theorem 1.2 records the known cases for the known deformation types with primitive c₁(L).

### 🔵 `OP-B411F7CC986E` — `background_open` | MSC 53C26 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), Conjecture 1.1
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Any \hk\ manifold can be deformed into a \hk\ manifold with a Lagrangian fibration.

**自包含改写**：Conjecture (background): Every hyper-Kähler manifold — over the complex numbers, i.e., a simply connected smooth compact Kähler manifold carrying a nowhere-degenerate holomorphic 2-form unique up to multiplication by a nonzero constant, of arbitrary complex dimension 2n — can be deformed into a hyper-Kähler manifold that admits a Lagrangian fibration. No hypothesis beyond the definition of hyper-Kähler. The paper verifies this only for fourfolds X carrying classes λ, μ ∈ H²(X, Z) with ∫_X λ⁴ = 0 and ∫_X λ²μ² = 2 (via its Theorems 1.3 and 1.6).

**判定理由**：One of the field's 'two key conjectures' quoted as background; the paper proves only dimension-4 instances under extra topological hypotheses, so the general proposition remains open.

**关联卡**：Companion to the Conjecture 1.2 (hyper-Kähler SYZ) card and to the Theorem 1.6 card, where the paper verifies both conjectures in dimension 4 under the topological assumption ∫λ⁴=0, ∫λ²μ²=2.

### 🔴 `OP-3E395DA27B63` — `solved_in_paper` | MSC 53C26 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), Theorem 1.6
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $X$ be a \hk\ fourfold and let $L$ be  a nef line bundle on $X$. Set $\lll\coloneqq c_1(L) \in H^2(X,\Z)$ and assume that there exists $\mm\in H^2(X,\Z)$ such that     $\int_X \lll^4=0$ and $\int_X\lll^2\mm^2=2$. There exists a Lagrangian fibration $f\colon X\to\P^2$ with $f^*{\cO_{\P^2}}(1)\isom L$.

**自包含改写**：Theorem proved in this paper (the hyper-Kähler SYZ conjecture in dimension 4 under a topological hypothesis): Let X be a hyper-Kähler fourfold and L a nef line bundle on X. Set λ := c₁(L) ∈ H²(X, Z) and assume there exists μ ∈ H²(X, Z) such that ∫_X λ⁴ = 0 and ∫_X λ²μ² = 2. Then there exists a Lagrangian fibration f : X → P² with f*O_{P²}(1) ≅ L. The paper also proves an intermediate weaker statement (Corollary 5.6) asserting only the existence of a Lagrangian fibration f : X → P² with f*O_{P²}(1) ≅ L^{⊗k_L} for some positive integer k_L.

**判定理由**：This is the previously open dimension-4 case (under the topological hypothesis) of the SYZ conjecture; the paper proves it completely, with k_L = 1.

**关联卡**：Crucial special case of the background Conjecture 1.2 (hyper-Kähler SYZ conjecture) card; the proof relies on Theorem 4.3 (the dimension-4 case of Conjecture 1.5), Proposition 5.7 (case C2), and the classification in Section 7; the weaker Corollary 5.6 allows f*O(1) ≅ L^{k_L}.

### 🔴 `OP-492ABEE791F6` — `solved_in_paper` | MSC 14J35 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), Corollary 1.4 ('O'Grady's conjecture'); originally conjectured in O'Grady, Commun. Contemp. Math. 10 (2008)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> A \hk\ fourfold   of  $\mathrm{K3}^{[2]}$ numerical type  is of~K3$^{[2]}$ deformation type.

**自包含改写**：O'Grady's conjecture (2008), proved in this paper as Corollary 1.4: if X is a hyper-Kähler fourfold of K3^[2] numerical type — i.e., for some K3 surface S there exists an isomorphism of abelian groups ψ : H²(X, Z) → H²(S^[2], Z) such that ∫_X α⁴ = ∫_{S^[2]} ψ(α)⁴ for all α ∈ H²(X, Z) (equivalently, the lattices (H²(X,Z), q_X) and (H²(S^[2],Z), q_{S^[2]}) are isometric and the Fujiki constants coincide) — then X is of K3^[2] deformation type (deformation-equivalent to the Hilbert square of a K3 surface).

**判定理由**：Pre-existing conjecture of O'Grady that this paper proves (Corollary 1.4), as a consequence of the stronger Theorem 1.3 under weaker hypotheses.

**关联卡**：Deduced from Theorem 1.3 of the paper: a hyper-Kähler fourfold with classes λ, μ ∈ H²(X,Z) satisfying ∫_X λ⁴ = 0 and ∫_X λ²μ² = 2 is of K3^[2] deformation type.

### ⚪ `OP-FE3EA32AE43B` — `future_application` | MSC 53C26 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 5.3, remark following Corollary 5.6
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We include the proof since it does not use the results of Section~\ref{sec:OGrady} and  might apply to more general situations.

**自包含改写**：Not a mathematical proposition — a methodological outlook by the authors. They include the proof of Corollary 5.6 (which gives, for a hyper-Kähler fourfold X with a nef line bundle L, λ := c₁(L), ∫_X λ⁴ = 0, and some μ ∈ H²(X, Z) with ∫_X λ²μ² = 2, a Lagrangian fibration f : X → P² with f*O_{P²}(1) ≅ L^{⊗k_L} for some positive integer k_L) because that proof avoids the classification results of Section 7 and might apply to more general situations. No specific target statement is formulated.

**判定理由**：Value judgement about potential wider applicability of a proof technique; not a decidable proposition, hence not taskified.

**关联卡**：Refers to the weaker version (Corollary 5.6) of the fully solved Theorem 1.6 card; difficulty_hint is not applicable since this is not a proposition.

**存疑**：Difficulty hint is not meaningful here (non-proposition); included only to comply with the schema.


## `2012.05888` — Stable Big Bang formation for Einstein’s equations: The complete sub-critical regime
- 权威出处：**Journal of the American Mathematical Society** 2023，DOI `10.1090/jams/1015`
- 连接方式：`doi`｜全文 396,618 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟢 `OP-29354032E703` — `real_open` | MSC 83C75 | 难度 medium

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1, subsection 'Overview of our proof' (low order estimates part), Remark 'How large does N need to be?' (label rem:N)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The following natural question emerges from the above discussion: how large does $N$ need to be for the above scheme to work?

**自包含改写**：Quantitative question raised (and only partially answered) by the paper: in its bootstrap scheme for perturbations of a sub-critical Kasner solution, N (the number of commuted transported spatial derivatives; k in H^N(Sigma_t), n in H^{N+1}(Sigma_t)) must be chosen sufficiently large in a non-explicit manner depending on N_0 (the number of sharply L^infinity-controlled derivatives, any integer N_0 >= 1), the time-weight exponent A_* >= 1, the spatial dimension D, and constants q and sigma fixed by 0 < 2*sigma < 2*sigma + max_{I,J,B in {1,...,D}, I<J} {|q_B|, q_I + q_J - q_B} < q < 1 - 2*sigma (q_I the background Kasner exponents). The paper's interpolation inequality (with delta_N ~ 1/N, delta_N -> 0 as N -> infinity) 'already suggests' the rough sufficient bounds N on the order of 1/sigma (and N on the order of N_0/sigma for N_0 derivatives in L^infinity), and shows qualitatively that the needed N tends to infinity as max_I q_I -> 1 or as max_{I<J}{q_I+q_J-q_B} -> 1; the precise minimal (sharp) largeness of N is left undetermined.

**判定理由**：An explicitly posed 'natural question'; the paper gives only heuristic/non-explicit sufficient bounds, so the precise quantitative answer is genuinely left open.

**⚠️ 人工复核标记**：The qualitative/rough version is answered in the paper (finite N suffices, heuristically N ~ 1/sigma); only the sharp quantitative threshold is open -- verify whether this borderline labeling is acceptable for the downstream tracker.

**关联卡**：Companion quantitative question to the 'size of A_* / cancellations' card (both concern explicit bookkeeping of the borderline constants C_*, A_*, N).

### 🟢 `OP-77F1B9FCA3A2` — `real_open` | MSC 83C75 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1, subsection 'Overview of our proof' (low order estimates part), Remark 'Refined estimates with a different frame?' (label rem:diag.frame)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> However, to close a bootstrap argument with a refined frame, such as a frame that is adapted to the eigenvectors of $k$, one would have to overcome serious technical difficulties, such as a potential loss of derivatives for the frame. It would be interesting to understand whether such an approach is viable for solutions without symmetry, i.e., whether the entire proof can be carried out using a refined frame.

**自包含改写**：Question raised by the paper: is the entire stable-Big-Bang-formation proof (for perturbations of sub-critical Kasner solutions without symmetry) viable using a 'refined' orthonormal spatial frame -- e.g., a frame adapted to the eigenvectors of the second fundamental form k of the CMC slices Sigma_t, such as the asymptotically eigenvector-adapted frames used by Ringstrom in his work on the geometry of silent big bang singularities -- which might yield sharper asymptotic estimates for the spatial frame and connection coefficients than the Fermi-Walker-transported frame actually used? The paper notes serious technical difficulties (e.g., a potential loss of derivatives for the frame) and that, as of writing, the only known way to close the top-order estimates is with a Fermi-Walker-transported frame, which is not generally aligned with the eigenvectors of k.

**判定理由**：Explicitly posed viability question ('whether the entire proof can be carried out using a refined frame'); decidable-ish and open, though phrased with 'interesting'.

**关联卡**：The same question appears in Section 1.5.3 ('It would be interesting to explore whether a change of frames could yield more refined estimates for the spatial frame and connection coefficients'); cf. also the paper's remarks that no regular rescaled limit is obtained for the frame components (R:NOLIMITFORFRAME) and that only a Fermi-Walker frame is known to close top-order estimates (R:FRAMEFREEDOM). Companion outlook: 'sharper asymptotics' card.

### 🟢 `OP-7D02BF897AB2` — `real_open` | MSC 83C75 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1, subsection 'Beyond Hawking's singularity theorem', Remark titled 'Open problem' (label R:OPENPROBLEM)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In light of the above discussion, we would like to highlight the following open problem, brought to our attention by Mihalis Dafermos: construct \underline{any} open set of initial data without symmetry for the Einstein-vacuum equations in $1+3$ dimensions such that the maximal development exhibits a spacelike singularity.

**自包含改写**：Open problem explicitly highlighted by the paper (attributed to Mihalis Dafermos): construct ANY open set of initial data, without any symmetry assumption, for the Einstein-vacuum equations in 1+3 spacetime dimensions, such that the maximal globally hyperbolic development exhibits a singularity along a spacelike hypersurface. Context supplied by the paper: in 1+3 vacuum every Kasner background violates the sub-criticality condition max over I<J of {q_I + q_J - q_B} < 1 on Kasner exponents (which satisfy q_1+q_2+q_3 = q_1^2+q_2^2+q_3^2 = 1), so the paper's stability techniques do not apply without symmetry; and, as of the paper's writing, the Dafermos-Luk near-Kerr (asymptotically flat, non-cosmological) solutions were the only symmetry-less 1+3 vacuum solutions with precisely understood geodesic incompleteness.

**判定理由**：Explicitly flagged 'open problem' in a remark; a well-defined construction problem for the 1+3 Einstein-vacuum equations; unresolved at paper time and not solved here.

**关联卡**：The polarization-condition method gap (heur.omega.cond card) and the BKL instability expectations explain the difficulty; the obstruction-identification remark (R:IDENTIFYOBSTRUCTION) pinpoints the dangerous terms (distinct-index structure coefficients).

### 🟢 `OP-A2444DAD9567` — `real_open` | MSC 83C75 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1, subsection 'Overview of our proof', Remark 'The size of A_*' (label rem:A)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In fact, in the near-FLRW regime (where all Kasner exponents are nearly equal), the last two authors \cite{RodSp1,RodSp2} showed that striking cancellations take place, and $\blowupexp$ can in fact be taken very small, i.e., $C_*=C\varepsilon$. It is not known to us whether such cancellations exist for perturbations of highly anisotropic background Kasner solutions.

**自包含改写**：In the paper's top-order energy estimates for perturbations of Kasner solutions, borderline error terms contribute an integral C_* times the integral from t to 1 of E_N(s)^2 / s ds, where C_* is a constant independent of the derivative parameter N, of the L^infinity-control parameter N_0, and of the time-weight exponent parameter (denoted \blowupexp in the source, i.e. A_* >= 1, which appears in the t^(A_*+1)-weighted high-order energies); closing the bootstrap requires A_* > C_*. In the near-FLRW regime (all background Kasner exponents nearly equal, i.e. q_1 approximately q_2 approximately q_3 approximately 1/3 with B = sqrt(2/3)), Rodnianski-Speck previously showed striking cancellations occur so that C_* = C*epsilon (epsilon the small bootstrap parameter) and A_* can be taken very small. Question left open by the paper: do such cancellations of the borderline terms occur for perturbations of highly anisotropic background Kasner solutions (so that C_*, and hence A_*, could be taken small)?

**判定理由**：Explicit 'It is not known to us' statement: a genuine question left open by the paper about borderline-term cancellations for highly anisotropic Kasner backgrounds.

**关联卡**：Same remark also notes an explicit upper bound for C_* (hence the required A_*) could in principle be computed but is not provided; related to the 'how large does N need to be' card.

**存疑**：'Such cancellations' is informal; it refers to cancellations making C_* = C*epsilon so that A_* can be chosen small. The question is mathematically meaningful but not stated as a formal conjecture.

### 🔵 `OP-847EC8CE25DF` — `background_open` | MSC 83C75 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1, subsection 'Beyond Hawking's singularity theorem', discussion of the BKL picture
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In a more modern language, \cite{BKL} proposed that there are families of cosmological solutions that \textbf{i)} contain all gravitational degrees of freedom (e.g., $4$ functional degrees of freedom for the Einstein-vacuum equations in $1+3$ dimensions) and \textbf{ii)} exhibit Big Bang formation along a spacelike hypersurface. Moreover, the authors argued that ``generically'' (the meaning of ``generic'' was not rigorously defined), solutions that exhibit Big Bang formation ``should'' -- unlike the Kasner solutions -- be highly oscillatory in time as the singularity is approached.

**自包含改写**：The BKL conjecture (Belinski-Khalatnikov-Lifshitz, 1971), as summarized by the paper: for cosmological (compact spatial topology) solutions of Einstein's equations -- in particular the Einstein-vacuum equations in 1+3 dimensions -- there are 'general' families of solutions that (i) contain all gravitational degrees of freedom (e.g. 4 functional degrees of freedom in 1+3 vacuum) and (ii) exhibit Big Bang formation along a spacelike hypersurface; moreover 'generically' (no rigorous definition given), such singularity-forming solutions should be highly oscillatory in time as the singularity is approached (the 'Mixmaster scenario'), unlike the Kasner solutions. Cited as background; the paper's own results concern the complementary non-oscillatory sub-critical regime, and it notes Dafermos-Luk's conditional work shows some basic qualitative BKL assertions fail for near-Kerr data.

**判定理由**：Famous BKL conjecture described as background/motivation; not this paper's own target (the paper proves the complementary sub-critical stability regime).

**关联卡**：Related to the Dafermos open problem (1+3 vacuum spacelike singularity without symmetry) and to the obstruction-identification remark card.

### 🔵 `OP-91EB52A6A57F` — `background_open` | MSC 83C75 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1.3, 'Remarks on Strong Cosmic Censorship'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It therefore remains possible that a revised version of the Strong Cosmic Censorship conjecture is true, in which ``generically, geodesic incompleteness is tied to breakdown at the boundary of the maximal development,'' where ``breakdown'' is defined to be any loss of regularity that is sufficiently strong to prevent one from extending the solution as a weak solution to Einstein's equations.

**自包含改写**：Strong Cosmic Censorship (background conjecture; original formulation attributed to Penrose, modern versions to Christodoulou and Chrusciel): 'generically' the maximal globally hyperbolic development of initial data for Einstein's equations is inextendible, roughly due to the formation of some kind of singularity. The paper notes the C^0 formulation is not generically true (Dafermos-Luk proved C^0-extendibility of the metric across the Cauchy horizon for an open set of near-Kerr solutions), and entertains a revised version: 'generically, geodesic incompleteness is tied to breakdown at the boundary of the maximal development', where 'breakdown' is any loss of regularity strong enough to prevent extension even as a weak solution. The paper's own contribution is only that its near-Kasner solutions are C^2-inextendible past the Big Bang (via curvature blowup), and it cites Luk-Oh's large-data spherical result supporting the revised version.

**判定理由**：Strong Cosmic Censorship (and its revised weak-solution formulation) is cited as background; the paper only verifies C^2-inextendibility for its own solutions.

**关联卡**：The paper's curvature-blowup results give C^2-inextendibility for its solutions, a (solved-in-paper) piece of evidence in this setting.

### 🔵 `OP-DB49A457C750` — `background_open` | MSC 83C75 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1.3, footnote attached to the discussion of Dafermos-Luk's Kerr Cauchy horizon result (label FN:CONDITIONALKERR)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> A full justification that these data are induced by open sets of black hole solutions that are settling down to a Kerr black hole relies on forthcoming works by various authors. In particular, the justification relies on a quantitative version of the dynamic stability of the exterior region of Kerr, and there have been a series of works that seem to be building towards a definitive proof its stability.

**自包含改写**：Background open problem (stated in a footnote): a quantitative version of the dynamic stability of the exterior region of Kerr is still needed to fully justify that the initial data used in Dafermos-Luk's C^0-stability theorem for the Kerr Cauchy horizon are induced by open sets of black hole solutions settling down to a Kerr black hole; at the time of writing, a series of works seemed to be building towards a definitive proof of Kerr stability. Famous open problem cited as a conditional hypothesis/background, not a target of the present paper.

**判定理由**：Kerr exterior stability is a famous open problem cited as the missing conditional ingredient for Dafermos-Luk; not this paper's own target.

**关联卡**：Conditions the interpretation of the Dafermos-Luk result discussed in the Strong Cosmic Censorship card.

### 🟠 `OP-36CA6DE6E862` — `method_obstruction` | MSC 83C75 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1, subsection 'Beyond Hawking's singularity theorem', Remark 'Sharply identifying possible obstructions to stability: Three distinct indices' (label R:IDENTIFYOBSTRUCTION)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Thus, for perturbations of Kasner solutions, the only structure coefficients $\upgamma_{IJB} + \upgamma_{JBI}$ (with $I < J$) that in principle could serve as an obstruction to stable Big Bang formation are those such that the sum $\widetilde{q}_I + \widetilde{q}_J - \widetilde{q}_B$ is greater than $1$, and this is possible only when all three indices are distinct; the stability condition \eqref{Kasner.stability.cond} is the assumption that this obstruction is absent.

**自包含改写**：Method observation (not a posed problem): for perturbations of a Kasner solution with background exponents q_1,...,q_D (satisfying sum_I q_I = 1, sum_I q_I^2 = 1 - B^2; and max_I |q_I| < 1 except the trivial flat case of one exponent equal to 1), the structure coefficients S_IJB := gamma_IJB + gamma_JBI, where gamma_IJB = g(nabla_{e_I} e_J, e_B) are the connection coefficients of the Fermi-Walker-transported g-orthonormal spatial frame {e_I}, satisfy an approximately diagonal evolution equation d/dt (S_IJB) = -((q_I + q_J - q_B)/t) S_IJB + ... (no summation on underlined indices). Hence the only structure coefficients that could obstruct stable Big Bang formation are those with q_I + q_J - q_B > 1, possible only when I, J, B are pairwise distinct; the sub-criticality condition max_{I<J}{q_I+q_J-q_B} < 1 is precisely the assumption that this obstruction is absent. The paper adds that in regimes violating the condition (e.g., 1+3 Einstein-vacuum without symmetry, where every Kasner solution violates it), any instabilities would have to arise from the combinations S_IJB with distinct indices; actual instability is not proven.

**判定理由**：The paper pinpoints candidate obstruction terms (distinct-index structure coefficients) and thereby shows why the sub-criticality hypothesis is needed, without posing an instability problem.

**关联卡**：Underlies the sharpness claim of the main theorem card and motivates the Dafermos open problem card and the polarized U(1) results (where distinct-index coefficients vanish).

### 🟠 `OP-BF70020CC45F` — `method_obstruction` | MSC 83C75 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1, subsection 'Background on Kasner-like behavior: Heuristics', paragraph after the Frobenius-theorem discussion
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> However, the condition \eqref{heur.omega.cond} refers to the structure of the metric ``at the singularity'' (i.e., since \eqref{metric.heur} is only supposed to capture the asymptotic structure of the metric, \eqref{heur.omega.cond} is a statement about the structure of the asymptotic behavior of the metric near the singularity), and we are not aware of any ``general method'' for solutions without symmetry that allows one to ensure the validity of \eqref{heur.omega.cond} via assumptions on the initial data on $\Sigma_1$.

**自包含改写**：Methodological gap noted by the paper (not a posed problem): in 1+3 vacuum, for a Kasner-like metric ansatz g approximately -dt x dt + sum_I t^{2 q_I(x)} theta^I(x) x theta^I(x) with the (unique) negative exponent q_-(x) < 0, the spatial Ricci estimate needed for AVTD-type analysis holds if the polarization-type condition theta^- wedge d theta^- = 0 holds (d = exterior derivative; by Frobenius this is equivalent to integrability of the 2-planes annihilated by theta^-, and to the existence of functions u, v: T^3 -> R with theta^- = u dv). This condition concerns the metric 'at the singularity', and the authors state they are aware of no general method, for solutions without symmetry, that ensures theta^- wedge d theta^- = 0 via assumptions on the initial data on the slice Sigma_1. For polarized U(1)-symmetric solutions the condition automatically holds.

**判定理由**：Authors note no known method ensures the polarization condition from initial data; a stated hypothesis gap, not a formally posed open problem.

**关联卡**：This gap is the heuristic reason the Dafermos open problem (1+3 vacuum spacelike singularity without symmetry) is hard; the Fournodavlos-Luk construction (cited in the paper) produces Sobolev solutions satisfying the polarization condition.

### 🔴 `OP-2BB03DB82390` — `solved_in_paper` | MSC 83C75 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Abstract (results stated precisely as Theorems labeled thm:rough, thm:precise, thm:precise.U1)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> In this paper, we prove that the Kasner singularity is dynamically stable for \emph{all} sub-critical Kasner exponents, thereby justifying the heuristics in the literature in the full regime where stable monotonic-type curvature-blowup is expected.

**自包含改写**：The paper proves a heuristic going back over 50 years (Belinski-Khalatnikov, Barrow, Damour-Henneaux-Spindel, etc.): the Big Bang singularity of a generalized Kasner solution -- the explicit solution on (0,infinity) x T^D with metric -dt dt + sum_{I=1}^D t^{2 q_I} dx^I dx^I and scalar field B*log t, where the constants q_1,...,q_D, B satisfy sum_I q_I = 1 and sum_I q_I^2 = 1 - B^2 -- is dynamically stable under perturbations (in suitably high-order Sobolev spaces, without symmetry) of its initial data on the CMC slice Sigma_1 = {t=1} = T^D, whenever the exponents are sub-critical: max over I,J,B in {1,...,D}, I<J, of {q_I + q_J - q_B} < 1. This covers the Einstein-scalar field system for all D >= 3 and, when B = 0, the Einstein-vacuum equations for D >= 10 (in vacuum the condition is algebraically impossible for D <= 9). Perturbed solutions have Kretschmann scalar blowing up like t^{-4} as t -> 0 and exhibit AVTD behavior. Additionally, in 1+3 vacuum (T^3 topology, B=0, max_I q_I < 1, excluding the trivial case of a single exponent equal to 1), ALL Kasner solutions are stable under polarized U(1)-symmetric perturbations, even though all violate the sub-criticality condition. This extends the prior results of Rodnianski-Speck (FLRW, q_1=q_2=q_3=1/3; and vacuum D >= 38 with max_I |q_I| < 1/6).

**判定理由**：This is the paper's main theorem, resolving the long-standing heuristic prediction of stable monotone Big Bang formation throughout the sub-critical regime.

**关联卡**：Answers affirmatively the 'standout question' card in the crucial cases; the sharpness of the regime is tied to the obstruction-identification remark card.

### 🔴 `OP-5B7D18E12437` — `solved_in_paper` | MSC 83C75 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1, subsection 'Beyond Hawking's singularity theorem', paragraph beginning 'A standout question, then, is:'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> A standout question, then, is: besides the explicit Kasner solutions (which we describe in Sect.\,\ref{subsec:models}), are there \emph{any} other cosmological solutions to Einstein's equations -- in particular ones with spatial dependence -- that are asymptotic to a metric of the form ${\bf g}_{\textnormal{Limiting}}$ and thus exhibit monotonic-type Big Bang formation?

**自包含改写**：Question posed in the introduction: besides the explicit spatially homogeneous Kasner solutions, do there exist any other cosmological (compact spatial topology) solutions of Einstein's equations -- in particular ones with spatial dependence -- whose spacetime metrics are asymptotic, as t -> 0, to a metric of the form g_Limiting(t,x) = -dt x dt + sum_{I=1}^D t^{2 q_I(x)} theta^I(x) x theta^I(x), where theta^I(x) = theta^I_a(x) dx^a are one-forms and the exponents satisfy the vacuum analogs sum_I q_I(x) = sum_I q_I(x)^2 = 1, and which therefore exhibit monotonic-type Big Bang formation (blowup of the Kretschmann scalar along a spacelike hypersurface)? The paper proves the crucial cases: for all sub-critical Kasner backgrounds (Einstein-scalar field D>=3, vacuum D>=10, no symmetry) and for all singular Kasner solutions in 1+3 vacuum under polarized U(1)-symmetry, open sets of initial data yield spatially dependent solutions with monotonic curvature blowup like t^{-4}, AVTD behavior, and well-defined Lipschitz 'final Kasner exponents' q_I^{(infinity)}(x).

**判定理由**：Explicitly posed question; the paper proves the crucial cases (sub-critical without symmetry; polarized U(1) in 1+3 vacuum), though not the precise asymptotic form with time-independent one-forms.

**⚠️ 人工复核标记**：The paper proves monotonic-type curvature blowup and existence of final Kasner exponents, but does NOT prove the metric is asymptotic to the precise form g_Limiting with a time-independent co-frame (cf. its Remark R:TIMEDEPENDENTFRAMES: 'we are able to close our estimates without showing that the metric is asymptotic to a metric of the form (1.5)'). Prior Fuchsian works (Andersson-Rendall; Damour-Henneaux-Rendall-Weaver; Klinger; Fournodavlos-Luk) had already constructed Kasner-like singular solutions without symmetry, so only the stability aspect is new here. Label 'solved_in_paper' means: crucial special cases proven.

**关联卡**：The unsolved finer asymptotics are the subject of the 'sharper asymptotics' and 'refined frame' cards; the existence part was previously addressed by Fuchsian constructions cited in the paper.

### ⚪ `OP-98B33FF7EBA7` — `future_application` | MSC 83C75 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1, subsection 'Applicability of the method', subsubsection 'Potential further applications', bullet 'Black hole interior'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> For the latter solutions, it would be interesting to see whether Kasner-like blowup holds for perturbations of solutions (in some class other than spherical symmetry, which was handled in \cite{Christ2,Christ3}). Compared to our work here, the difference in topology might pose additional analytical difficulties. Moreover, one would have to grapple with the question of whether the initial data given only in the interior of a black hole could arise as induced data of solutions to the global Cauchy problem.

**自包含改写**：Not a precisely formulated proposition -- a research direction containing an embedded informal question: for black-hole spacetimes with a spacelike singularity in the interior, such as the spherically symmetric Einstein-scalar field collapse solutions of Christodoulou, the paper asks (a) whether Kasner-like blowup holds for perturbations of these solutions in some class other than spherical symmetry (the perturbation class is not specified), noting the difference in spatial topology may pose additional analytical difficulties; and (b) whether initial data prescribed only in the interior of a black hole can arise as data induced by solutions of the global Cauchy problem. Because the perturbation class is unspecified, this is treated as outlook rather than an open proposition.

**判定理由**：Direction with an explicitly vague perturbation class ('in some class other than spherical symmetry') plus an informal embedded realizability question; outlook, not a decidable proposition as stated.

**⚠️ 人工复核标记**：If a grader wishes to promote the embedded question (b) -- realizability of prescribed black-hole-interior data by solutions of the global Cauchy problem -- to a real_open item, note it is stated only informally ('one would have to grapple with the question of whether...').

**关联卡**：Companion to the general 'potential further applications' card; also connects to the Alexakis-Fournodavlos Schwarzschild-interior stability work discussed in the paper.

### ⚪ `OP-9E39B97D8C8A` — `future_application` | MSC 83C75 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 6.1 (statement of the theorems), Remark 'Sharper asymptotics' (label R:SHARPERASYMPTOTICS)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Although Theorems~\ref{thm:precise} and \ref{thm:precise.U1} yield the most interesting and salient features of the stable blowup, by using the estimates provided by the theorems, one could try to derive sharper asymptotics for the solution by treating the evolution equations as ODEs (with derivative-losing source terms), perhaps also employing a different gauge for the already constructed singular solution.

**自包含改写**：Not a proposition -- a stated research direction/outlook: using the a priori estimates provided by the paper's main theorems (stable Big Bang formation without symmetry for sub-critical Kasner backgrounds, and for polarized U(1)-symmetric perturbations in 1+3 vacuum), one could try to derive sharper asymptotics for the constructed singular solutions by treating the evolution equations as ODEs with derivative-losing source terms, possibly employing a different gauge for the already-constructed singular solution. The paper notes sharper metric-component asymptotics are known in some symmetric regimes (polarized axi/U(1)-symmetry via Alexakis-Fournodavlos; polarized T^2-symmetry via areal foliations by Ames-Beyer-Isenberg-Oliynyk), whereas its theorems yield no regular rescaled limits for the orthonormal-frame components.

**判定理由**：'One could try to derive sharper asymptotics' is a taste/outlook remark about follow-up research, not a mathematical proposition.

**关联卡**：Companion to the 'refined frame' card (the sharper asymptotics might require a different frame/gauge); also connected to the unresolved part of the 'standout question' card (asymptotics to the precise limiting Kasner-like form).

### ⚪ `OP-C1DB7E5BF60A` — `future_application` | MSC 83C75 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1, subsection 'Applicability of the method', subsubsection 'Potential further applications', opening sentence (followed by the bullets on the stiff-fluid model and on non-explicit backgrounds)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Our approach could likely be adapted to prove stable Big Bang formation in other models that are not, strictly speaking, covered in the present paper. We mention here some interesting cases.

**自包含改写**：Not a proposition -- an application outlook stated by the paper: its approach could likely be adapted to prove stable Big Bang formation in models not strictly covered, specifically: (i) the Einstein-stiff-fluid system for D >= 3 spatial dimensions (this matter model reduces to the scalar field model when vorticity vanishes; the FLRW case D = 3 with q_1 = q_2 = q_3 = 1/3 was previously treated by Rodnianski-Speck); and (ii) perturbations of fixed, non-explicit singular backgrounds, or of solutions with large spatial dependence such as those constructed by Fuchsian methods -- where spatial derivatives falling on the background need not be small -- possibly by posing data on a slice Sigma_{t_Data} with t_Data > 0 small (chosen depending on the largeness of the data) close to the expected singularity, which the paper says could also produce open sets of singularity-forming solutions with 'substantial x-dependence'.

**判定理由**：'Could likely be adapted' is an outlook on method transfer, not a mathematical proposition; per rule 5 it must not be taskified.

**关联卡**：The separate 'black hole interior' bullet from the same subsection is extracted as its own card.


## `2105.15167` — Minimal nondegenerate extensions
- 权威出处：**Journal of the American Mathematical Society** 2023，DOI `10.1090/jams/1023`
- 连接方式：`doi`｜全文 318,249 字符 via `cache-latex`｜提取模式 `fast`

### 🟢 `OP-6F0A7604ED8E` — `real_open` | MSC 18M20 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 4.3 (sec:Tan), Conjecture at end
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We have therefore outlined a proof of the following conjecture, subject to the assumptions made above.
\begin{conjecture}The obstruction class $O_4(\cB)$ induces an isomorphism
\begin{equation} \label{eq:obsbos2}
\Obs(\Rep(G)) \cong \coker\bigl(\Witt \to \Witt(\Rep(G))\bigr) \cong \H^4(\rB G; \bk^\times). 
\end{equation}
\end{conjecture}

**自包含改写**：Conjecture (Tannakian case, over an algebraically closed characteristic-zero field k, for a finite group G): the obstruction class O_4(B) (the fourth cohomological obstruction to minimal nondegenerate extensions) induces an isomorphism Obs(Rep(G)) ≃ coker(Witt → Witt(Rep(G))) ≃ H^4(BG; k×), where Obs(Rep(G)) is the complete obstruction group for minimal nondegenerate extensions of braided fusion categories with Müger centre Rep(G). The proof is outlined but relies on unproven assumptions from higher Morita theory of fusion higher categories.

**判定理由**：Formally labelled Conjecture in the paper; only a conditional proof sketch is given.

**⚠️ 人工复核标记**：The paper 'outlines' a proof subject to unverified higher-Morita assumptions; the Tannakian obstruction-injection part is also known from prior work cited (Theorem 4.8 of 1712.07097).

**关联卡**：Super-Tannakian analogue is the final conjecture of Section 4.4.

### 🟢 `OP-7D68A5621C72` — `real_open` | MSC 18M20 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Remark rem:strongerversionLag, after Theorem thm.BCs
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> we expect the following stronger version of Theorem~\ref{thm.BCs} to be true: For any nondegenerate braided fusion $2$-category $\mathcal{C}$, there is an equivalence between the $2$-groupoid of fusion $2$-categories $\cA$ equipped with an equivalence $\cZ(\cA) \cong \mathcal{C}$ and the $2$-groupoid of ``general'' Lagrangian braided monoidal objects in $\mathcal{C}$ (i.e.\ 
rigid braided monoidal objects $A$ fulfilling condition~\ref{Lag2alg:conditionnondeg} of Definition~\ref{defn:Lag2alg} but instead of condition~\ref{Lag2alg:connectivity} only requiring the unit $u:I \to A$ to be simple).

**自包含改写**：Conjecture (stronger version of the stated Theorem): for any nondegenerate braided fusion 2-category C (over an algebraically closed characteristic-zero field k), the 2-groupoid of fusion 2-categories A equipped with a braided monoidal equivalence Z(A) ≃ C is equivalent to the 2-groupoid of 'general' Lagrangian braided monoidal objects in C, i.e. rigid braided monoidal objects A whose Müger centre (in the sense of transparent 1-morphisms I → A) is trivial and whose unit u: I → A is simple (but not necessarily fully faithful). Consequently, if C = ΣB for a braided fusion 1-category B, there should be an equivalence between the 2-groupoid of braided fusion categories M with a (not necessarily fully faithful) braided monoidal functor B → M and the 2-groupoid of fusion 2-categories A with Z(ΣB) ≃ Z(A).

**判定理由**：Explicit conjecture ('we expect ... to be true') of a mathematical proposition, not proved here.

**⚠️ 人工复核标记**：The statement relies on Definition ref numbers in the source; conditions were inlined from Definition defn:Lag2alg.

**关联卡**：Strengthens Theorem thm.BCs, whose one-directional version is proved in the paper; also discussed as expected 'if and only if' in Remark rem:BCs citing higher Morita work.

### 🟢 `OP-882979EB96A3` — `real_open` | MSC 18M20 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.3, paragraph after Corollary cor.unitary
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The more general question (also asked in \cite{MR1990929}) of whether every super-modular category admits a minimal modular extension remains open. We expect it can be settled with similar techniques.

**自包含改写**：Does every super-modular category (a slightly degenerate braided fusion category, over an algebraically closed characteristic-zero field k, equipped with a chosen ribbon structure — not assumed pseudo-unitary) admit a minimal modular extension, i.e. an extension to a nondegenerate braided fusion category with a compatible ribbon/modular structure whose centralizer condition is minimal? This remains open at the time of writing; the authors expect similar techniques will settle it.

**判定理由**：Explicitly stated open question left unresolved by the paper (only the pseudo-unitary case is solved).

**关联卡**：Generalizes the solved pseudo-unitary Corollary (card 2); originally asked in Müger's paper.

### 🟢 `OP-AF96B7065561` — `real_open` | MSC 18M20 | 难度 medium

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 2.2, before the Lemma that Z(ΣB) is braided fusion
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In particular, we expect that $\cZ(\cA)$ will be a fusion $2$-category whenever $\cA$ is. For the purposes of this paper we will need only:

**自包含改写**：Conjecture: for any fusion 2-category A (over an algebraically closed characteristic-zero field k), the Drinfel'd centre Z(A) (the braided monoidal 2-category of endomorphisms of A as an A-bimodule) is again a fusion 2-category. Only the special case A = ΣB for a braided fusion 1-category B is proved in this paper.

**判定理由**：Explicitly stated expectation of a general proposition; the paper proves only the special case needed.

**关联卡**：The special case Z(ΣB) is proved as an unnumbered Lemma in Section 2.2 (solved_in_paper for that case).

### 🟢 `OP-BE5B6E1E6BB0` — `real_open` | MSC 18M20 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 4.4 (sec:superTan), final Conjecture
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Subject to our assumptions, this yields a sketch of a proof of the following conjecture. 
 \begin{conjecture}The obstruction group $\Obs(\sRep(G, \varpi))$ is isomorphic to 
\begin{equation} \label{eqn.superobstruction} \coker\left(\vphantom{\SH^{\id }}\Witt \to \Witt\left(\sRep(G, \varpi)\right)\right)\cong \coker \left( \varpi^*:  \SH^{\id+4}(K(\bZ_2, 2)) \to \SH^{\varpi + 4} (\rB G) \right).
\end{equation}
Moreover, $\Mext(\sVec) \cong \SH^{\id+4}(K(\bZ_2, 2))$ and there is a left exact sequence
\begin{equation} \label{eqn.supermext}
0 \to  \SH^{\varpi+3}(\rB G) \to \Mext(\sRep(G, \varpi)) \to \Mext(\sVec) \to[\varpi^*] \SH^{\varpi+4}(\rB G).
\end{equation}
\end{conjecture}

**自包含改写**：Conjecture (super-Tannakian case, over an algebraically closed characteristic-zero field k): for a finite group G with 2-cocycle ϰ ∈ H^2(BG; Z_2), the obstruction group Obs(sRep(G,ϰ)) for minimal nondegenerate extensions of braided fusion categories with Müger centre sRep(G,ϰ) is isomorphic to coker(Witt → Witt(sRep(G,ϰ))) ≃ coker(ϰ*: SH^{id+4}(K(Z_2,2)) → SH^{ϰ+4}(BG)), where SH denotes extended supercohomology. Moreover Mext(sVec) ≃ SH^{id+4}(K(Z_2,2)) and there is a left exact sequence 0 → SH^{ϰ+3}(BG) → Mext(sRep(G,ϰ)) → Mext(sVec) →[ϰ*] SH^{ϰ+4}(BG).

**判定理由**：Formally labelled Conjecture; proof only sketched subject to unverified higher-Morita assumptions.

**关联卡**：Super-analogue of the Tannakian conjecture (card on Obs(Rep(G)) ≃ H^4(BG;k×)).

### 🟢 `OP-F4C6F44A9AC7` — `real_open` | MSC 18M20 | 难度 medium

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Remark after Definition defn:rigidobject, Section 2.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In characteristic zero, we expect that every rigid monoidal object in a fusion $2$-category is automatically separable, generalizing the fact that every multifusion $1$-category is automatically separable.

**自包含改写**：Conjecture: over a field k of characteristic zero, every rigid monoidal object A in a fusion 2-category (rigid in the sense that the multiplication 1-morphism m: A ⊁ A → A has a right adjoint Δ as an A–A bimodule 1-morphism) is automatically separable, i.e. the counit ev_m: m ∘ Δ ⇒ id_A admits a section as an A–A bimodule 2-morphism. This would generalize the theorem that multifusion 1-categories are separable.

**判定理由**：Explicit expectation of an unproved mathematical proposition.

### 🟢 `OP-FFA658EC02FA` — `real_open` | MSC 18M20 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Remark rem:Lagrangian, Section 2.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We expect nondegeneracy of $\cC$ to be equivalent to triviality of its M\"uger sylleptic centre. In other words, $\cC$ should present a ``3+1D topological order'' as axiomatized in~\cite{1405.5858,KWZ1,2003.06663}. In this nondegenerate case, we expect condition~\ref{Lag2alg:conditionnondeg} of Definition~\ref{defn:Lag2alg} to be equivalent to the stronger condition of triviality of the $2$-category of braided $A$-module objects

**自包含改写**：Conjectures: (i) for a braided fusion 2-category C, nondegeneracy (invertibility of the framed S-matrix / components pairing) is equivalent to triviality of the Müger sylleptic centre of C; (ii) for a nondegenerate braided fusion 2-category C, condition (2) of the Definition of Lagrangian braided monoidal objects (triviality of the Müger centre of A as transparent 1-morphisms I → A) for a strongly connected rigid braided monoidal object A is equivalent to triviality of the 2-category of braided A-module objects of A.

**判定理由**：Explicit 'we expect' statements of decidable mathematical equivalences, not proved here.

**关联卡**：Related to the general S-matrix nondegeneracy criterion cited as future work [Smatrix].

### 🔵 `OP-0878CE4979B9` — `background_open` | MSC 18M20 | 难度 hard

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1.1, Introduction
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Generalizing the group case, M\"uger asked in \cite{MR1990929} whether every braided fusion category admits a minimal nondegenerate extension.

**自包含改写**：Müger's original question: does every braided fusion 1-category B (over an algebraically closed characteristic-zero field) admit a minimal nondegenerate extension? The paper notes the answer is 'No' via Drinfeld's unpublished counterexample and cohomological obstructions, reducing the general problem to the slightly degenerate case.

**判定理由**：Historical background question from a cited paper; already resolved negatively before this paper by Drinfeld's counterexample.

**关联卡**：The slightly degenerate case of this question is the paper's Main Theorem (card 1).

**存疑**：current_status is 'unknown' per instructions; the paper itself states the answer is negative via counterexample.

### 🔵 `OP-F7DDD66CB7AA` — `background_open` | MSC 18M20 | 难度 hard

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1.3, parenthetical in the definition discussion
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The underlying braided fusion category of such a category is pseudo-unitary and has a unique positive $*$-structure~\cite{MR3239112, 1906.09710}, but it remains open whether every pseudo-unitary braided fusion category admits a positive $*$-structure.

**自包含改写**：For k = C: does every pseudo-unitary braided fusion category (i.e. one admitting a positive ribbon structure for which all quantum dimensions are positive) admit a positive *- (dagger) structure whose underlying braided fusion category is the given one? Stated as open background, attributed to prior literature.

**判定理由**：Cited open problem from other works, used as motivation/contrast, not this paper's target.

### 🔴 `OP-7BAC24993933` — `solved_in_paper` | MSC 18M20 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Corollary 1.2 (cor.unitary), Section 1.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Every pseudo-unitary super-modular category admits a pseudo-unitary minimal modular extension.

**自包含改写**：Over k = C: every pseudo-unitary super-modular category (i.e. a slightly degenerate pseudo-unitary braided fusion category equipped with its unique positive ribbon structure) admits a minimal modular extension which is again pseudo-unitary with its unique positive ribbon structure extending that of B.

**判定理由**：Corollary of the Main Theorem, proved in Section 1.3 via dimension identities.

**关联卡**：Special (pseudo-unitary) case of the Main Theorem; distinct from the open general super-modular question.

### 🔴 `OP-9E359677E198` — `solved_in_paper` | MSC 18M20 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Main Theorem, Section 1.1 (Introduction)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Every slightly degenerate braided fusion category admits a minimal nondegenerate extension.

**自包含改写**：Over a fixed algebraically closed field k of characteristic zero: every slightly degenerate braided fusion 1-category B (i.e. its Müger centre Z_2(B) is equivalent as a symmetric fusion category to sVec, the category of finite-dimensional super vector spaces) admits an inclusion B ⊂ M into a nondegenerate braided fusion category M (Z_2(M) ≃ Vec) such that the canonical inclusion Z_2(B) ⊂ Z_2(B ⊂ M) is an equivalence.

**判定理由**：This is the paper's Main Theorem, proved constructively in Section 3.

**关联卡**：Resolves the long-standing problem appearing as Question 5.15 of DMNO-type literature, Conjecture 3.9 of the 16-fold way paper, and Conjecture 1.1 of a later reference; generalizes Corollary on pseudo-unitary super-modular categories.

### 🔴 `OP-E706E300863C` — `solved_in_paper` | MSC 18M20 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1.1, Introduction
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> In that same section, we also explain a complete ``supercohomological'' obstruction theory for the general non-Tannakian case, thereby answering a question asked by~\cite{OstrikMCA}.

**自包含改写**：The question (asked by Ostrik, cited as [OstrikMCA]) of providing a supercohomological obstruction theory for minimal nondegenerate extensions in the non-Tannakian (super-Tannakian) case. The paper claims to answer it by explaining a complete supercohomological obstruction theory, with the obstruction to minimal nondegenerate extensions of a slightly degenerate B being a class in H^5(K(Z_2,2); k×) ≃ Z_2 which the paper shows always vanishes.

**判定理由**：The paper claims to answer this cited question via its supercohomological obstruction theory and vanishing computation.

**⚠️ 人工复核标记**：The full super-Tannakian obstruction theory (Section 4.4) is conditional on unverified higher-Morita assumptions; the slightly degenerate vanishing itself is unconditional.

**关联卡**：Underlies the Main Theorem and the final conjecture of Section 4.4.

### ⚪ `OP-B8B75BEA225D` — `future_application` | MSC 18M20 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 2.6, preceding proof of Theorem thm:componentcount
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> To keep our proofs in this paper elementary, we will somewhat reverse the narrative and conclude Theorem~\ref{thm:componentcount} from well-known results about braided fusion $1$-categories, and then use it in \S\ref{sec:Smatrix} to show that the $S$-matrix of $\cZ(\Sigma \cB)$ is nondegenerate.

**自包含改写**：Research direction: the authors state that versions of the component-counting theorem hold for all nondegenerate braided fusion 2-categories and more generally fusion n-categories with trivial centre, via a nondegenerate S-matrix pairing on higher looping of components, to be developed in cited future work [Smatrix]. The present paper proves only the case of Z(ΣB), by reversing the narrative.

**判定理由**：Announcement of future work and general framework, not a formally posed proposition in this paper.

**关联卡**：The S-matrix nondegeneracy for Z(ΣB) itself (Theorem thm:invertibleSmatrix) is proved in the paper.


## `1608.00499` — Endotrivial modules for finite groups via homotopy theory
- 权威出处：**Journal of the American Mathematical Society** 2022，DOI `10.1090/jams/994`
- 连接方式：`doi`｜全文 279,043 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟢 `OP-1BCC0C11F080` — `real_open` | MSC 20D20 | 难度 medium

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 3.3, Remark after Corollary 3.6 (on C^{p'} groups)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> bounding its size is an interesting and
  so far apparently unexplored group theoretical
  question about $p'$--actions.

**自包含改写**：For a finite group G, define C^{p'}(G) = ⟨x ∈ G | p divides |C_G(x)|⟩, the subgroup generated by elements with centralizer of order divisible by p. The open question is to bound the size of the quotient G/C^{p'}(G) in terms of p-local information, an unexplored group-theoretic question about p'-actions.

**判定理由**：Explicitly stated as an unexplored and interesting mathematical question by the paper, with the authors studying it in separate joint work.

**关联卡**：Authors note they study this in joint work in progress with Geoffrey Robinson.

### 🟢 `OP-2FED88BA50A5` — `real_open` | MSC 20C20 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, Section 1.5 (Computational results), final paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Based on available data, it
may be that $\pi_1(\Oep(G)) \xrightcong (G_0)_{p'}$ when the
$p$--rank is at least three? This would imply $T_k(G,S) \cong
\Hom(G_0,k^\times)$ under that assumption.

**自包含改写**：Let G be a finite group, p a prime dividing |G|, S a Sylow p-subgroup, and G_0 = <N_G(Q) | 1 < Q <= S>. The question is whether the fundamental group of the orbit category O_p^*(G) (objects G/P for non-trivial p-subgroups P, morphisms G-maps) is isomorphic to (G_0)_{p'} = G_0/<g in G_0 | g has finite p-power order>, whenever the p-rank of G (the rank of the largest elementary abelian p-subgroup) is at least 3. This would imply T_k(G,S) ≅ Hom(G_0, k^×) for k a field of characteristic p.

**判定理由**：A concrete mathematical conjecture posed by the paper itself, decidable for each finite group, left unresolved.

**关联卡**：Related to the bound on r in the Carlson--Thévenaz conjecture (see card about r=3).

### 🟢 `OP-32CF27A32E93` — `real_open` | MSC 20C20 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 5.4 (p-solvable groups)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It would obviously be interesting to have an identification of the
right-hand side with $\Hom(G,k^\times)$, when $A$ has rank at least
$2$, via a proof which did
not use
the classification of finite simple groups.

**自包含改写**：For G = AH with A a non-trivial elementary abelian p-group of rank at least 2 and H a normal p'-group, the isomorphism T_k(G,S) ≅ lim^0_{V ∈ F_{A_p(A)}} Hom(C_H(V), k^×) is known (via the classification of finite simple groups). The paper poses the problem of proving this identification equals Hom(G, k^×) without using the classification of finite simple groups.

**判定理由**：A concrete mathematical goal posed by the paper: prove a known result without CFSG dependence.

**关联卡**：The result is known via CFSG; the question is about a proof independent of CFSG.

### 🟢 `OP-48DDE401E26B` — `real_open` | MSC 20C20 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 4, Remark 4.2 (CT-bound-rem)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We do not know of an example where one
  cannot take $r=3$. In fact, to the best of our knowledge,
  in all finite groups where $\TS$ has been calculated either $\rho^3(S) =
  N_{A^{p'}(G)}(S)$ (and hence $\TS = \Hom(G,k^\times)$), or $\calS_p(G)$ is $G$--homotopy equivalent to a $1$--dimensional
  complex.

**自包含改写**：Let G be a finite group with Sylow p-subgroup S. Define ρ^1(Q) = A^{p'}(N_G(Q)) where A^{p'}(H) = O^{p'}(H)[H,H], and ρ^i(Q) = ⟨N_G(Q) ∩ ρ^{i-1}(R) | 1 < R ≤ S⟩ ⊇ ρ^{i-1}(Q). The question is whether for all finite groups G one can always take r=3 in the formula T_k(G,S) ≅ Hom(N_G(S)/ρ^r(S), k^×), i.e., whether ρ^3(S) always equals ρ^∞(S). No counterexample is known.

**判定理由**：The paper explicitly notes no example is known where r=3 fails, posing the question whether r=3 universally suffices.

**关联卡**：Refines the Carlson--Thévenaz conjecture proven in this paper; the paper proves r can be bounded by nilpotency class of S plus 1.

### 🟢 `OP-5043D7B8EFE1` — `real_open` | MSC 20C20 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 3, Remark 3.6 (general-inverse-remark)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Its size in general, and the
 precise image given via Theorem~\ref{sylowss}, is at present
  unclear.

**自包含改写**：Consider the class of kG-modules M (for G a finite group, k a field of characteristic p dividing |G|) satisfying the condition that the stable endomorphism ring _Hom_G(M,M) ≅ k (where _Hom denotes Hom modulo maps factoring through projectives). This class contains all endotrivial modules and all simple modules. The paper leaves open: what is the size of this class in general, and what is the precise image of this class under the bijection of Theorem 3.5 (sylowss) between Sylow-semi-simple modules without projective summands and finitely generated kπ_1(O_p^*(G))-modules?

**判定理由**：The paper explicitly states this is 'at present unclear', posing a concrete question about a class of modules.

**关联卡**：Connected to candidates for images of simple modules under self-equivalences of the stable module category.

### 🟢 `OP-CC3B342C2FE6` — `real_open` | MSC 20C20 | 难度 medium

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 4, Remark 4.2 (CT-bound-rem)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> As far as we know, this poset could have a
uniform dimension
bound in general, independent of the finite group $G$.

**自包含改写**：Let G be a finite group and let C be the smallest collection of p-subgroups closed under passage to p-radical overgroups and containing all p-subgroups P where N_G(P)/P admits an exotic Sylow-trivial module. The question is whether there exists a uniform bound, independent of G, on the dimension of the poset |C| (viewed as a simplicial complex).

**判定理由**：A concrete question about the existence of a uniform bound on a dimension, explicitly posed as a possibility the authors cannot confirm or deny.

**关联卡**：Related to bounding r in the Carlson--Thévenaz filtration.

### 🔵 `OP-0FDD182A204D` — `background_open` | MSC 20D06 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 5.4 (p-solvable groups)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Aschbacher also conjectured the simple
connectivity in \cite{aschbacher93}, and reduced the claim to where
$H=F^*(G)$ is a direct product of simple components being permuted
transitively by $A$

**自包含改写**：For G = AH a p-solvable group (A a non-trivial elementary abelian p-group, H a normal p'-group), Aschbacher conjectured that |S_p(G)| is simply connected (when the p-rank is at least 2), and reduced this conjecture to the case where H = F^*(G) is a direct product of simple components transitively permuted by A.

**判定理由**：Aschbacher's conjecture is cited as background motivation for the p-solvable case, not posed by this paper.

**关联卡**：Closely related to Quillen's Cohen--Macaulay conjecture for p-solvable groups.

### 🔵 `OP-4AB605B628E5` — `background_open` | MSC 20G40 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 5.2 (Finite groups of Lie type)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Away from the characteristic the $p$--subgroup complex is also
expected to be simply
connected, if $G$ is ``large enough'', but this is not known in general.
Stronger yet, the $p$--subgroup complex appears often to be
Cohen--Macaulay

**自包含改写**：Let G be a finite group of Lie type (e.g., GL_n(q), Sp_{2n}(q)) and p a prime not dividing q. It is expected (as a background conjecture, not proven) that |S_p(G)| is simply connected when G is 'large enough' (e.g., has p-rank at least 3), and stronger, that |S_p(G)| is Cohen--Macaulay. This has been verified in a number of cases by Das but is not known in general.

**判定理由**：This is a background belief/expectation from the literature, not posed by this paper, used as motivation.

**关联卡**：The paper proves special cases via Theorem E (Spn) for symplectic groups.

### 🔵 `OP-6F5C0FD9101C` — `background_open` | MSC 20J06 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 5.4 (p-solvable groups)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Quillen
\cite[Prob.~12.3]{quillen78} conjectures that $\calS_p(G)$ should in fact be
Cohen--Macaulay, and in particular simply connected when $A$ has
$p$--rank at least $3$, and proved this when $G$ is actually solvable
\cite[Thm.~11.2(i)]{quillen78}.

**自包含改写**：Let G = AH where A is a non-trivial elementary abelian p-group and H is a normal p'-group (G is p-solvable). Quillen's conjecture [Prob. 12.3, quillen78] states that the order complex |S_p(G)| of non-trivial p-subgroups of G should be Cohen--Macaulay. In particular it should be simply connected when the p-rank of A is at least 3. Quillen proved this when G is actually solvable.

**判定理由**：Quillen's conjecture is cited as background motivation, not posed by this paper; the paper uses it as a potential route to results.

**关联卡**：Related to Aschbacher's conjecture on simple connectivity.

### 🟠 `OP-72E3DDE430FA` — `method_obstruction` | MSC 20C20 | 难度 easy

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, Section 1.3 (Carlson--Thévenaz conjecture)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Computer calculations announced in \cite{CT15},  say this is
not the case for $G_2(5)$ when $p=3$.

**自包含改写**：The paper notes that the naive guess that one could always take r=2 in the Carlson--Thévenaz formula T_k(G,S) ≅ Hom(N_G(S)/ρ^r(S), k^×) fails: computer calculations show this is not the case for G = G_2(5) when p = 3. Specifically, ρ^2(S) ≠ ρ^3(S) = ρ^∞(S) = N_G(S) for this group.

**判定理由**：Shows the hypothesis r=2 fails in general, illustrating that a naive simplification of the method does not work; not a formally posed open problem.

**关联卡**：The paper itself calculates T_k(G_2(5),S) = 0 in Proposition 5.3 (G_25p3), confirming the failure.

### ⚪ `OP-701DC8E7C878` — `future_application` | MSC 20J06 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 3.1, Remark 3.2 (boundarymap)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> This extension class may deserve closer study.

**自包含改写**：Let G be a finite group with Sylow p-subgroup S and G_0 = <N_G(Q) | 1 < Q ≤ S>. There is an exact sequence 1 → π_1(S_p(G_0)) → π_1(T_p^*(G)) → G_0 → 1, whose abelianization has an extension class [α] ∈ H^2(G_0; H_1(S_p(G_0))). The paper states this extension class (which controls the boundary map ∂ in the subgroup complex sequence) may deserve closer study.

**判定理由**：A value judgement suggesting further study of a mathematical object, not a specific decidable proposition.

### ⚪ `OP-87F22D146686` — `future_application` | MSC 20C20 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 5.4 (p-solvable groups), final paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> one may hope to get vanishing results for $\pi_1(\Oep(G))$ for
any finite group $G$ by reducing to simple groups, by suitably generalizing the $p$--solvable case.

**自包含改写**：The paper states as a research direction the hope of proving vanishing results for π_1(O_p^*(G)) (equivalently, T_k(G,S) ≅ Hom(G,k^×)) for any finite group G by reducing the question to finite simple groups via the structural properties of π_1(O_p^*(G)) given in the paper, suitably generalizing the p-solvable case and using the generalized Fitting subgroup F^*(G).

**判定理由**：A broad strategy/hope for future work rather than a specific conjecture with stated hypotheses.

**关联卡**：Related to Aschbacher's conjecture about reducing simple connectivity to simple groups.

### ⚪ `OP-9A5C2E8F562C` — `future_application` | MSC 20C20 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 3.2, Remark after Corollary 3.4 (on LT17)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It would be interesting to rework and extend this result
  in light of the methods of the present paper.

**自包含改写**：The paper cites a result of Lynd and Tent [Thm. 1.1, LT17] reducing the problem of describing Sylow-trivial modules for arbitrary p'-extensions to that of central p'-extensions (for upper bounds), whose proof uses the classification of finite simple groups. The paper poses the research direction of reworking and extending this result using the homotopy-theoretic methods of the present paper.

**判定理由**：A research direction about applying the paper's methods to extend a known result, not a specific open proposition.

### ⚪ `OP-9BAA00E7644D` — `future_application` | MSC 20C20 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, Section 1.5 (Computational results)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It  should be possible to fill in the remaining gaps in the existing sporadic
group computations using similar arguments, though this is
outside the scope of the present paper.

**自包含改写**：The paper states that it should be possible to fill in the remaining gaps in the existing sporadic group computations of Sylow-trivial modules T_k(G,S) (left open in the literature, e.g., in LM15sporadic) using the methods of this paper, though carrying this out is outside the scope of the present paper.

**判定理由**：A value judgement about what should be possible with the methods, not a specific mathematical proposition; the authors note this was subsequently done by David Craven.

**关联卡**：The Monster case at primes 3,5,7,11,13 is computed in the paper (Theorem 5.1); remaining sporadic groups were done by Craven.

### ⚪ `OP-9D7C32E4C6E2` — `future_application` | MSC 20C20 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, Further vistas
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> it is natural to wonder about further
representation theoretic significance of the finite $p'$--groups
$\pi_1(\bO_p^*)$, $\pi_1(\bO_p^c)$, $\pi_1(\calF^c_p)$, and
$\pi_1(\calF_p^*)$, and the higher
homotopy and homology groups,
yet to be found?

**自包含改写**：The paper poses the informal research direction of finding further representation-theoretic significance of the finite p'-groups π_1(O_p^*(G)), π_1(O_p^c(G)), π_1(F_p^c(G)), and π_1(F_p^*(G)), and their higher homotopy and homology groups, beyond the connection to Sylow-trivial modules established in the paper.

**判定理由**：A broad research direction and value judgement about potential future significance, not a specific decidable mathematical proposition.


# Publications Mathématiques de l'IHÉS

## `2006.04987` — Langevin dynamic for the 2D Yang–Mills measure
- 权威出处：**Publications Mathématiques de l'IHÉS** 2022，DOI `10.1007/s10240-022-00132-0`
- 连接方式：`doi`｜全文 596,734 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟢 `OP-3C99431102B5` — `real_open` | MSC 81T13 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.3 'Open problems', first paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> A possible approach would be to show that the gauge-covariant lattice dynamic for the discrete YM measure converges to the solution to the SYM equation~\eqref{eq:SYM} identified in this paper.

**自包含改写**：Proposed open target: show that the gauge-covariant Langevin lattice dynamic for the discrete (2D) Yang–Mills measure (lattice approximation of T^2 with compact structure group G; the lattice model is cited but not defined in this paper) converges, as the lattice mesh tends to 0, to the renormalised solution of the stochastic Yang–Mills equation ∂_t A_i = ΔA_i + ξ_i + C A_i + [A_j, 2∂_j A_i − ∂_i A_j + [A_j, A_i]] on T^2 (i ∈ {1,2}, ξ_1, ξ_2 i.i.d. g-valued space-time white noises, C = C̄) constructed in this paper, viewed as an (Ω^1_α)^sol-valued process (α ∈ (2/3,1)) or via its projection to the orbit space. Combined with a gauge-fixing procedure as in [Chevyrev18YM] and a Bourgain-type argument along the lines of [HM18], this convergence would prove the invariant-measure conjecture (and strong regularity properties of the YM measure from the orbit-space description). Stated main difficulty: 'the lack of general stochastic estimates for the lattice which are available in the continuum thanks to [CH16]'.

**判定理由**：Explicitly proposed, decidable convergence statement adopted by the paper as its route to proving the invariant-measure conjecture; not proven here.

**关联卡**：Implementation step toward the invariant-measure conjecture card (with gauge fixing [Chevyrev18YM] and a Bourgain argument [Bourgain94, HM18] it 'would prove the result').

**存疑**：The 'gauge-covariant lattice dynamic for the discrete YM measure' is referenced without a precise definition in this paper; the lattice model must be taken from the cited literature.

### 🟢 `OP-5F3AE5A8895A` — `real_open` | MSC 81T13 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.2 'Relation to previous work'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It is not clear, however, how to extract from these works a space of gauge orbits with a well-defined probability measure, which is somewhat closer to the physical interpretation of the measure.

**自包含改写**：Open question: from the 2D Yang–Mills measure as constructed in earlier works (Driver 1989, Sengupta 1997, Lévy 2003/2006) — i.e. a stochastic process indexed by gauge-invariant observables such as Wilson loops, with explicit representations for general compact manifolds and principal bundles — extract a space of gauge orbits equipped with a well-defined probability measure (the YM measure on an orbit space), described in the paper as a non-linear analogue of Kolmogorov's problem of realising a consistent family of finite-dimensional distributions on a space of 'sufficiently regular' functions. The paper also notes this loop-indexed setting is ill-suited for the Langevin dynamic since it is far from clear how to interpret a realisation of such a stochastic process as an initial condition for a PDE. The present paper solves the orbit-space half (the Polish space O_α = Ω^1_α / G^{0,α} of gauge orbits of distributional g-valued 1-forms on T^2, α ∈ (2/3,1), with orbits determined by conjugacy classes of holonomies); endowing such an orbit space with the YM measure remains open.

**判定理由**：A genuine open question the paper engages with; it constructs the orbit-space half but not the measure-on-orbit-space half, which links to the invariant-measure conjecture.

**关联卡**：The orbit-space half is solved in this paper (see solved_in_paper card); the measure-identification half is exactly the content of the invariant-measure conjecture card, approached via the Langevin dynamic rather than via the loop constructions.

### 🟢 `OP-8D2A6C095B09` — `real_open` | MSC 81T13 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.3 'Open problems', third paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> However, an important result missing in~\cite{CCHSPrep} in comparison to this article is the existence of a gauge group which acts transitively on the gauge orbits.

**自包含改写**：In the 3D companion paper [CCHSPrep] the SPDE ∂_t A_i = ΔA_i + ξ_i + C A_i + [A_j, 2∂_j A_i − ∂_i A_j + [A_j, A_i]], i ∈ {1,2,3}, on R_+ × T^3 (G compact, ξ_i i.i.d. g-valued space-time white noises) is analysed: solutions take values in a suitable state space of distributional connections to which gauge equivalence extends canonically, the same gauge-covariance in law as in the present 2D article is shown, and a Markov process on the corresponding orbit space is constructed. Open problem (stated as a result missing in [CCHSPrep] compared to this article, in the context of 'it is also unclear how to extend all the results of this paper to the 3D setting'): the existence of a gauge group which acts transitively on the gauge orbits of that 3D state space — in 2D the analogue is the continuous action of G^{0,α} (closure of C^∞(T^2,G) in C^α) on Ω^1_α whose orbits are exactly the gauge-equivalence classes (determined by conjugacy classes of holonomies).

**判定理由**：A specific, decidable existence statement identified as the mathematical gap for the 3D extension; not resolved in this paper or (per this paper's statement) in the companion.

**关联卡**：3D counterpart of the 2D state-space/group-action construction solved in this paper (see solved_in_paper card); related remark 2.4 also notes that unlike in 2D, a divergent mass counterterm is needed in 3D.

**存疑**：'Acts transitively on the gauge orbits' is quoted as-is; by analogy with the 2D statement it means that any two gauge-equivalent connections in the 3D state space are related by an element of such a group, so equivalence classes coincide with group orbits.

### 🟢 `OP-BF3651062640` — `real_open` | MSC 60H15 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.3 'Open problems', first paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It is natural to conjecture that the Markov process constructed in this paper possesses a unique invariant measure, for which the associated stochastic process indexed by Wilson loops agrees with the YM measure constructed in~\cite{Sengupta97, Levy03,Levy06}.

**自包含改写**：Let G be a compact Lie group with Lie algebra g and work on the two-dimensional torus T^2. The paper constructs, for each α ∈ (2/3, 1), the Banach space Ω^1_α of distributional g-valued 1-forms (closure of smooth 1-forms in a norm controlling increments along line segments with exponent α), the gauge group G^{0,α} (closure of C^∞(T^2, G) in C^α), the Polish orbit space O_α = Ω^1_α / G^{0,α}, and a canonical time-homogeneous Markov process on the extended orbit space O_α ⊔ {cemetery}, obtained as the mollifier-independent limit (with a distinguished mass constant C = C̄) of solutions of the renormalised stochastic Yang–Mills equation ∂_t A_i = ΔA_i + ξ_i + C A_i + [A_j, 2∂_j A_i − ∂_i A_j + [A_j, A_i]], i ∈ {1,2}, where ξ_1, ξ_2 are i.i.d. g-valued space-time white noises. Conjecture: this Markov process possesses a unique invariant probability measure, and under this measure the stochastic process indexed by Wilson loop observables (holonomies hol(A, γ), well-defined on Ω^1_α for loops γ ∈ C^{1,β} with β ∈ (2/α − 2, 1]) agrees with the 2D Yang–Mills measure on T^2 constructed by Sengupta and Lévy.

**判定理由**：Explicit conjecture in the dedicated 'Open problems' section: uniqueness of the invariant measure and identification of its Wilson-loop process with the 2D YM measure; not resolved by the paper.

**关联卡**：The proposed lattice-convergence route (separate card) would prove this; the same target via the opposite route (extracting an orbit-space measure from the Wilson-loop constructions) is a separate card; non-explosion of the orbit-valued Markov process would follow from this conjecture plus strong Feller and irreducibility (see non-explosion card).

### 🟢 `OP-DAC38A3AC139` — `real_open` | MSC 60H15 | 难度 hard

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 1.3 'Open problems', second paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It would be of interest to determine whether the solution to SYM survives almost surely for all time for any initial condition.

**自包含改写**：Consider the renormalised stochastic Yang–Mills (SYM) equation in DeTurck form on R_+ × T^2 (G compact Lie group, g its Lie algebra): ∂_t A_i = ΔA_i + ξ_i + C A_i + [A_j, 2∂_j A_i − ∂_i A_j + [A_j, A_i]], i ∈ {1,2}, where ξ_1, ξ_2 are i.i.d. g-valued space-time white noises and C ∈ L_G(g,g) is the distinguished constant C = C̄ for which the paper constructs the Markov process on gauge orbits; the solution is the ε → 0 limit of mollified equations. The paper proves local existence with values in (Ω^1_α)^sol, α ∈ (2/3,1), but its results do not exclude finite-time blow-up, not even after projection to the quotient/orbit space. Open question: does the solution survive almost surely for all time (no finite-time blow-up) for any initial condition? Note the paper's caveat: since gauge orbits are unbounded, non-explosion of the Ω^1_α-valued solution is strictly stronger than non-explosion of the orbit-valued Markov process; the weaker Markov-process case would follow from the invariant-measure conjecture combined with the strong Feller property and irreducibility, both of which the paper notes hold in this setting. (The analogous non-explosion result is known for the Φ^4_d SPDE in d = 2, 3; long-time existence of the deterministic YM heat flow in d = 2, 3 is also known, but the paper states it is not clear how to adapt those deterministic methods to the stochastic setting.)

**判定理由**：Explicitly posed open question about a.s. global-in-time existence for the SYM equation; the paper proves only local existence and explicitly acknowledges it cannot exclude blow-up.

**关联卡**：The weaker orbit-valued case would follow from the invariant-measure conjecture card plus strong Feller [HM16] and irreducibility [HS19]; the paper also notes the deterministic-method obstruction (Råde, CG13) as context.

### 🔵 `OP-BCDCE8B4DD9E` — `background_open` | MSC 81T13 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1, Introduction (opening paragraph)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The YM measure plays a fundamental role in high energy physics, constituting one of the components of the Standard Model, and its rigorous construction largely remains open, see~\cite{JW06, Chatterjee18} and the references therein.

**自包含改写**：Background famous problem: the Euclidean Yang–Mills measure, formally dμ_YM(A) = Z^{-1} exp[−S_YM(A)] dA with S_YM(A) = ∫_M |F_A(x)|^2 dx (A a connection on a principal G-bundle P → M over a space-time manifold M, G a compact Lie group, F_A the curvature 2-form, dA a formal Lebesgue measure, Z a normalisation constant), has no rigorous construction in general (notably in higher dimensions, in particular d = 3, 4). It is cited here only as motivation; the 2D case is already rigorously constructed by other methods (Driver, Sengupta, Lévy), and the present paper studies the 2D Langevin dynamic.

**判定理由**：Famous open problem cited as background/motivation; not this paper's own target (it works in 2D where the measure is known).

**关联卡**：Motivates the whole program; the 2D instance of the measure (via Sengupta/Lévy) is the object in the invariant-measure conjecture card.

### 🔴 `OP-351B5F6AB76D` — `solved_in_paper` | MSC 60H15 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1, Introduction (paragraph preceding Section 1.1)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Our goal is to show the existence of a natural space of gauge orbits such that (appropriately renormalised) solutions to~\eqref{eq:SYM} define a canonical Markov process on this space.

**自包含改写**：Stated goal of the paper (achieved): for a compact Lie group G with Lie algebra g, on T^2, construct a natural space of gauge orbits on which appropriately renormalised solutions of the stochastic Yang–Mills equation ∂_t A_i = ΔA_i + ξ_i + C A_i + [A_j, 2∂_j A_i − ∂_i A_j + [A_j, A_i]] (i ∈ {1,2}; ξ_1, ξ_2 i.i.d. g-valued space-time white noises; C ∈ L_G(g,g)) define a canonical Markov process. Proven in the paper: (a) for α ∈ (2/3,1) the Banach space Ω^1_α of distributional g-valued 1-forms on which holonomies along C^{1,β} curves (β ∈ (2/α − 2, 1]) are well-defined and continuous, with a continuous action of the gauge group G^{0,α} and a separable complete orbit space O_α = Ω^1_α/G^{0,α}; (b) convergence as ε → 0 of the mollified renormalised equations to an (Ω^1_α)^sol-valued solution with no divergent mass counterterm; (c) existence of an essentially unique constant C̄ (for non-anticipative mollifiers) making the projected dynamics gauge-covariant in law and independent of the mollifier; (d) existence and uniqueness of the induced time-homogeneous Markov process on O_α ⊔ {cemetery}.

**判定理由**：This is the paper's own stated target and it is proved by its main theorems (state space, local existence, gauge covariance in law, Markov process on orbits).

**关联卡**：This constructed Markov process is the object of the invariant-measure conjecture, the non-explosion question, and the lattice-convergence target; its 3D analogue minus the transitive gauge group action is the 3D open problem.

**存疑**：Theorem numbers are not cited since the numbering is not fully visible in the provided source; theorems are identified by content (state space, local existence, gauge covariance, Markov process).

### ⚪ `OP-38BC649D1786` — `future_application` | MSC 60H15 | 难度 

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Remark 2.2 (rem:holonomy_param_indep) following the state-space theorem, Section 2
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> This is done in Definition~\ref{def:pvar} which might be of independent interest.

**自包含改写**：Not a mathematical proposition (value judgement): the authors suggest that Definition def:pvar — a parametrisation-independent way of measuring path regularity via the quantity |γ; γ̄|_α built from areas of triangles spanned by the path (relating to C^{1,β} curves with β ∈ (1,2) in the way p-variation relates to Hölder regularity for β ≤ 1) — 'might be of independent interest'.

**判定理由**：Value judgement about a definition being of independent interest; not a research proposition.

**关联卡**：The introduction (Section 1.1) describes this parametrisation-free regularity notion as a byproduct of the Ω^1_α construction.

### ⚪ `OP-3EB2678D7B53` — `future_application` | MSC 60H15 | 难度 

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.4 'Outline of the paper'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We expect this framework to be useful in for a variety of systems of SPDE whose natural formulation involve vector-valued noise

**自包含改写**：Not a mathematical proposition (value judgement / application outlook): the authors expect the basis-free regularity-structure framework developed in the paper for systems (∂_t − L_t) A_t = F_t(A, ξ), t ∈ L_+, with vector-valued noises ξ and solutions taking values in vector spaces W_t (smooth local nonlinearities), which builds the regularity structure and renormalised equations without choosing bases of W_t, to be useful for a variety of SPDE systems naturally formulated with vector-valued noise; in the paper's own application it yields renormalisation counterterms for the stochastic Yang–Mills equation directly in terms of Lie brackets and exploits symmetry from Ad-invariance of the noises. The abstract echoes the same expectation ('we expect this framework to be of independent interest').

**判定理由**：Expectation of usefulness for other systems — a taste/value judgement, not a decidable proposition posed by the paper.

**关联卡**：Abstract contains the same sentiment ('of independent interest'); merged here to avoid duplication.

**存疑**：Quote preserves the source's typo 'useful in for a variety'.

### ⚪ `OP-539D6E63049A` — `future_application` | MSC 81T13 | 难度 

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Remark following the state-space theorem, Section 2 (after Theorem thm:state_space)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Analogous spaces could be defined on any manifold, but it is not clear whether higher dimensional versions are useful for the study of the stochastic YM equation.

**自包含改写**：Not a mathematical proposition (taste/outlook remark): analogues of the Banach spaces Ω^1_α of distributional connections on which holonomies are well-defined (constructed in the paper on the torus T^2) could be defined on any manifold, but the authors state it is not clear whether higher-dimensional versions of these spaces would be useful for the study of the stochastic Yang–Mills equation.

**判定理由**：Uncertainty/taste comment on the usefulness of a possible extension; no mathematical proposition is posed.

**关联卡**：Context for the 3D-extension open problem card.


## `1908.07812` — Stationary characters on lattices of semisimple Lie groups
- 权威出处：**Publications Mathématiques de l'IHÉS** 2021，DOI `10.1007/s10240-021-00122-8`
- 连接方式：`doi`｜全文 177,029 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟠 `OP-2D3FC04419CD` — `method_obstruction` | MSC 22E40 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), remark following Theorem C
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> We point out that our approach requires that all simple factors of $G$ have real rank at least two (as in the notation), while Peterson's character rigidity result holds more generally when $G$ is a property (T) connected semisimple Lie group with trivial center, no nontrivial compact factor and real rank at least two.

**自包含改写**：The approach of this paper — proving that μ0-characters on a lattice Γ are genuine characters and classifying characters of irreducible lattices via Furstenberg probability measures μ0 ∈ Prob(Γ) and a noncommutative Nevo–Zimmer structure theorem for stationary actions on von Neumann algebras — requires the hypothesis that every simple factor of the ambient group G (a connected semisimple Lie group with finite center and no nontrivial compact factor) has real rank at least two. By contrast, Peterson's character rigidity result (any extreme point in the character space of an irreducible lattice Γ < G is almost periodic or the Dirac character δ_e) holds under the weaker hypothesis that G is a property (T) connected semisimple Lie group with trivial center, no nontrivial compact factor and (total) real rank at least two, which permits rank-one simple factors. Hence the paper's method does not cover lattices in products involving rank-one factors, and no extension of the method to that case is posed.

**判定理由**：States a hypothesis (all simple factors of real rank at least two) needed by the paper's method, contrasted with Peterson's weaker hypotheses; no open problem is posed.

**关联卡**：Companion to the card on Peterson's character rigidity (Theorem C): records the gap between this paper's hypotheses and Peterson's general theorem.

### 🟠 `OP-70D58F64309D` — `method_obstruction` | MSC 46L10 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 5, discussion preceding Lemma 5.6 (lem:NZ2)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Unfortunately, in the general noncommutative case, the state $\psi$ need not be faithful on $\cN$, and Mautner's phenomenon fails. The equality $\cN^s = \cN^{W_{\theta,s}}$ does not hold.

**自包含改写**：Let A be a separable unital C*-algebra carrying a continuous action of a minimal parabolic subgroup P of a connected semisimple Lie group G, let ψ be a P-invariant state on A, let N = π_ψ(A)'' be the GNS von Neumann algebra (so the P-action extends to a ψ-preserving continuous action on N), and let q ∈ N be the support projection of ψ (q need not equal 1). For θ ⊊ Δ a proper subset of the simple roots Δ, let s ∈ S'_θ be a split-torus element whose Ad(s) is contracting on the unipotent radical V_θ and whose Ad(s)^{-1} is contracting on the opposite radical, and set W_{θ,s} = s^Z ⋉ V_θ ⊲ P; denote by N^s and N^{W_{θ,s}} the fixed-point von Neumann subalgebras. In the commutative case (N abelian), ψ is faithful and Mautner's phenomenon yields N^s = N^{W_{θ,s}}, which is P-invariant; in the general noncommutative case, ψ need not be faithful on N, Mautner's phenomenon fails, and the equality N^s = N^{W_{θ,s}} does not hold. The paper shows the equality survives after taking the corner with the central support q_{θ,s} of q in N^{W_{θ,s}}: for every y ∈ N^s one has y q_{θ,s} = q_{θ,s} y and y q_{θ,s} ∈ N^{W_{θ,s}}.

**判定理由**：Explicit method failure: Mautner's phenomenon and the fixed-point equality N^s = N^{W_{θ,s}} fail for noncommutative algebras with non-faithful states; no open problem posed.

**关联卡**：Second obstruction (after the stabilizer-map card) in the proof of Theorem 5.1; the paper resolves it via the corner construction (Lemma 5.6, lem:NZ2) rather than removing the failure.

### 🟠 `OP-A10B80FCF59A` — `method_obstruction` | MSC 46L10 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 5 (A noncommutative Nevo–Zimmer theorem), discussion preceding the proof of Theorem 5.1 (thm:NZ)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Unfortunately, there is no analogue of such a stabilizer map for actions of $G$ on arbitrary von Neumann algebras, so it is hopeless to prove Theorem \ref{thm:NZ} by simply translating Nevo--Zimmer's proof in noncommutative terms.

**自包含改写**：Nevo–Zimmer's structure theorem for stationary actions of a connected semisimple Lie group G on probability measure spaces (Ann. of Math. 156 (2002)) is proved using the 'Gauss map' and the associated stabilizer map, i.e., the G-equivariant measurable map X → Sub(G), x ↦ Stab(x), into the space Sub(G) of closed subgroups of G endowed with the Chabauty topology. For actions of G on arbitrary (noncommutative) von Neumann algebras there is no analogue of such a stabilizer map, so the noncommutative Nevo–Zimmer theorem (Theorem 5.1 of the paper: for G connected semisimple with finite center, no nontrivial compact factor, all simple factors of real rank at least two, μ a K-invariant admissible Borel probability measure, and (M, φ) an ergodic (G, μ)-von Neumann algebra, either φ is G-invariant or there exist a proper parabolic P ⊂ Q ⊊ G and a G-equivariant normal unital *-embedding Θ : L^∞(G/Q, ν_Q) → M with φ ∘ Θ = ν_Q) cannot be proved by simply translating Nevo–Zimmer's proof; the same passage notes that the analogue of the mixing condition on the minimal-parabolic P-action used in Nevo–Zimmer (1999) is not guaranteed. The paper circumvents these obstructions with von Neumann techniques (essential values into noncommutative algebras, disintegration, and the Ge–Kadison and Strătilă–Zsidó slice/splitting theorems), ultimately reducing to the commutative Nevo–Zimmer theorem.

**判定理由**：Explicit method failure: no stabilizer-map analogue exists for von Neumann algebra actions, blocking direct translation of Nevo–Zimmer's proof; no open problem posed.

**关联卡**：Concerns Theorem 5.1 (thm:NZ), the main engine behind Theorems A–F; the same paragraph also records the missing mixing condition, which is folded into this card. The paper works around the obstruction rather than removing it.

### 🟠 `OP-EF29F015EBCB` — `method_obstruction` | MSC 46L10 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 2.1 (Group actions on von Neumann algebras), discussion of the advantages of the C*- versus von Neumann categories
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In this respect, our noncommutative Nevo--Zimmer theorem, Theorem \ref{thm:NZ} below, does not have a $\rC^*$-analogue.

**自包含改写**：The paper's noncommutative Nevo–Zimmer theorem (Theorem 5.1: for G a connected semisimple Lie group with finite center and no nontrivial compact factor, all of whose simple factors have real rank at least two, μ ∈ Prob(G) a K-invariant admissible Borel probability measure (K a maximal compact subgroup), and (M, φ) an ergodic (G, μ)-von Neumann algebra, either the stationary normal state φ is G-invariant, or there exist a proper parabolic subgroup P ⊂ Q ⊊ G and a G-equivariant normal unital *-embedding Θ : L^∞(G/Q, ν_Q) → M with φ ∘ Θ = ν_Q) is asserted to have no analogue in the category of separable unital C*-algebras with continuous C*-actions. This reflects a stated category trade-off: the C*-category provides weak*-compactness of the state space (whereas normal states on a von Neumann algebra are not weak*-closed, indeed weak*-dense in the whole state space), while the von Neumann category's measurable nature is what the theorem's proof exploits. This is a stated framework limitation, not a posed problem.

**判定理由**：Asserts the main structure theorem has no C*-algebra analogue; a limitation of the framework/proof technique stated without posing an open problem.

**关联卡**：Refers to Theorem 5.1 (thm:NZ), the same theorem discussed in the stabilizer-map obstruction card.

**存疑**：The paper does not elaborate in what precise sense a C*-analogue is absent (unformulable statement versus unavailable proof technique); the remark is kept as a method limitation.

### 🔴 `OP-45F54ED8A705` — `solved_in_paper` | MSC 22D10 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), Theorem C
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $G$ be as in the notation and assume moreover that $G$ has trivial center. Let $\Gamma < G$ be any irreducible lattice. Then any extreme point $\varphi$ in the space of characters of $\Gamma$ is either almost periodic or $\varphi = \delta_e$.

**自包含改写**：Let G be a connected semisimple Lie group with finite center and no nontrivial compact factor, all of whose simple factors have real rank at least two, and assume moreover that G has trivial center. Let Γ < G be any irreducible lattice. Then any extreme point φ in the weak*-compact convex space of characters of Γ (a character being a positive definite, conjugation-invariant function φ : Γ → C with φ(e) = 1) is either almost periodic (i.e., the GNS representation of φ is finite dimensional) or φ = δ_e, the Dirac character at the identity element e. This is Peterson's character rigidity result; the paper proves it as Theorem C by a new route, applying its structure theorem for ergodic (Γ, μ0)-von Neumann algebras (μ0 a Furstenberg probability measure on Γ, i.e., supp(μ0) = Γ, μ0 * ν_P = ν_P, and (G/P, ν_P) the Poisson boundary of the μ0-random walk) to the noncommutative Poisson boundary, under the stronger hypothesis that all simple factors of G have real rank at least two.

**判定理由**：The paper itself proves Theorem C (a special case of Peterson's theorem, previously established in preprint form in greater generality) with a new proof.

**关联卡**：Peterson's original preprint (2014) predates this paper and covers all property (T) connected semisimple Lie groups with trivial center, no compact factor and real rank at least two; see the method_obstruction card on the rank hypothesis for the gap in this paper's approach.

### 🔴 `OP-C156C4C4916F` — `solved_in_paper` | MSC 22E40 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), paragraph preceding Corollary F
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> The next corollary provides a topological analogue of Stuck--Zimmer's rigidity result \cite{SZ92} and answers positively a question raised by Glasner--Weiss (see \cite[Problem 5.4]{GW14}).

**自包含改写**：Glasner–Weiss's question (Problem 5.4 in 'Uniformly recurrent subgroups', Contemp. Math. 631, 2015): must every uniformly recurrent subgroup (URS) of a higher-rank lattice be finite? A URS of a countable group Γ is a closed minimal Γ-invariant subset of the compact metrizable space Sub(Γ) of subgroups of Γ (Chabauty topology) under the conjugation action γ·Λ = γΛγ⁻¹. The paper answers it positively as follows: let G be a connected semisimple Lie group with finite center and no nontrivial compact factor, all of whose simple factors have real rank at least two, and assume moreover that G has trivial center; let Γ < G be any irreducible lattice. Then for any minimal action Γ ↷ X on a compact metrizable space, either X is finite or the action is topologically free (i.e., for every γ ≠ e, Fix(γ) = {x ∈ X | γx = x} has empty interior in X); in particular, any URS of Γ is finite.

**判定理由**：Question posed by Glasner–Weiss (2015), open before this paper; Corollary F answers it positively for irreducible lattices in center-free higher-rank semisimple Lie groups.

**关联卡**：Proved as Corollary F, using the paper's Theorems A/B (stationary characters and the structure theorem for ergodic (Γ,μ0)-von Neumann algebras), Margulis' normal subgroup theorem, and Stuck–Zimmer.

**存疑**：The exact wording of Glasner–Weiss's Problem 5.4 is not reproduced in this paper; the statement above is taken from Corollary F, which the paper presents as the positive answer.

### ⚪ `OP-507EF9AFF891` — `future_application` | MSC 46L10 | 难度 frontier

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), first paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Connes suggested that there should be a rich analogy between the embedding of a lattice in its ambient Lie group and the embedding of a lattice in its ambient group von Neumann algebra (see \cite{Jo00}).

**自包含改写**：Connes suggested (as recorded in V. F. R. Jones's 'Ten problems', 2000) that there should be a rich analogy between the embedding of a lattice Γ in its ambient semisimple Lie group G and the embedding of Γ in its ambient group von Neumann algebra L(Γ); in particular, an operator algebraic version of Margulis's superrigidity theorem was expected to hold. This is a research-vision/taste statement, not a decidable proposition on its own. The specific superrigidity expectation within it had already been confirmed before this paper by Bekka (for PSL_n(Z), n ≥ 3) and by Peterson (for irreducible lattices in property (T) connected semisimple Lie groups with trivial center and real rank at least two); the present paper continues the program by proving stationary-character rigidity and giving a new proof of character rigidity for such lattices.

**判定理由**：Not a proposition: a programmatic vision/taste remark of Connes cited as motivation; its concrete expectation (operator algebraic superrigidity) was already confirmed by Bekka and Peterson.

**关联卡**：Background motivation for the paper's Theorem C lineage (Bekka's and Peterson's operator algebraic superrigidity results); related to the Peterson character-rigidity card.

**存疑**：As a vision statement it is not a single decidable proposition; the card records it because it is a stated research direction, per the extraction brief.


## `1602.04705` — Double ramification cycles on the moduli spaces of curves
- 权威出处：**Publications Mathématiques de l'IHÉS** 2017，DOI `10.1007/s10240-017-0088-x`
- 连接方式：`doi`｜全文 112,732 字符 via `cache-latex`｜提取模式 `reasoning`

### 🔵 `OP-07107D689B5F` — `background_open` | MSC 14H10 | 难度 hard

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, Section 0.2.3, paragraph after Theorem 2
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Pixton \cite{PixDR} has further proposed a twist of the formula for $\P_g^d(A)$ by $k\in \Z$. The codimension $g$ class in the $k=1$ case has been (conjecturally) related to the moduli spaces of meromorphic differential in the Appendix of \cite{FarP}.

**自包含改写**：Pixton proposed a $k$-twisted version $P_g^{d,k}(A)$ of his formula, defined for $k\in\mathbb{Z}$ and $A=(a_1,\ldots,a_n)$ with $\sum_i a_i=k(2g-2+n)$ via stable graphs with $k$-weightings mod $r$ (vertex condition $\sum_{v(h)=v}w(h)=k(2g(v)-2+n(v))$ mod $r$), vertex factors $e^{-k^2\kappa_1(v)}$, leg factors $e^{a_i^2\psi_{h_i}}$, and the usual edge factors, evaluated at $r=0$. The codimension-$g$ class in the $k=1$ case, $P_g^{g,1}(A)$, is conjecturally related to the moduli spaces of meromorphic differentials (strata of differentials with prescribed divisor $\sum_i a_i p_i$); the precise conjecture is stated in the Appendix of [FarP] (Farkas-Pandharipande, with appendix by the present authors) and is not restated or targeted in this paper.

**判定理由**：Conjectural relation proposed in another paper ([FarP] Appendix), cited only as context for the k-twisted theory; not this paper's own target.

**⚠️ 人工复核标记**：The precise formulation of the conjecture relating the k=1 codimension-g class to strata of meromorphic differentials lives in the Appendix of [FarP]; only an informal mention appears here.

**关联卡**：The k-twisted classes are defined in Section 1 of this paper; their vanishing for d>g is proven for all k (see vanishing card).

**存疑**：Conjecture stated in a different paper ([FarP] appendix); adopted there, not here.

### 🔵 `OP-E3CFF21D8898` — `background_open` | MSC 14H10 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, Section 0.1 'Tautological rings', first paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The recent results \cite{J,PP,PPZ} concerning relations in $R^*(\oM_{g,n})$, conjectured to be {\em all} relations \cite{P}, may be viewed as parallel to the presentation

**自包含改写**：Background conjecture of Pixton [P]: the relations in the tautological ring $R^*(\overline{M}_{g,n})\subset A^*(\overline{M}_{g,n})$ (the $\mathbb{Q}$-subalgebra generated by $\kappa$ and $\psi$ classes and push-forwards of their products along boundary gluing maps) that were proven in [J] (via equivariant Gromov-Witten theory of $\mathbb{P}^1$), [PP], and [PPZ] (via 3-spin structures) are conjectured to constitute ALL relations of $R^*(\overline{M}_{g,n})$, i.e., to give a complete presentation analogous to the Chern/Segre presentation of the Chow ring of a Grassmannian. Cited here only as motivation; not a target of this paper.

**判定理由**：Famous conjecture (Pixton's complete set of tautological relations, [P]) cited as background/parallel; not addressed by this paper.

### 🟠 `OP-44811C3C99D8` — `method_obstruction` | MSC 14N35 | 难度 easy

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, Section 0.2.2 'Basic properties', remark following Proposition 2 (Faber-Pandharipande, $\DR_g(A)\in R^g(\oM_{g,n})$)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The proof of \cite{FP} provides an algorithm to calculate $\DR_g(A)$ in the tautological ring, but the complexity of the method is too great: there is no apparent way to obtain an explicit formula for  $\DR_g(A)$ directly from \cite{FP}.

**自包含改写**：Methodological limitation: the algorithm of Faber-Pandharipande [FP], which proves that the double ramification cycle $DR_g(A)\in A^g(\overline{M}_{g,n})$ (for double ramification data $A=(a_1,\ldots,a_n)$, $\sum_i a_i=0$, defined via stable maps to rubber) lies in the tautological ring $R^g(\overline{M}_{g,n})$, has complexity too great to yield an explicit formula; there is no apparent way to obtain an explicit formula for $DR_g(A)$ directly from [FP]. No open problem is formally posed; the paper instead derives the explicit formula by different methods (Chiodo's r-th root Chern classes and localization on $(\mathbb{P}^1[r],\infty)$).

**判定理由**：Statement that the prior [FP] localization method cannot yield an explicit formula; a hypothesis/method failure noted without posing a problem.

**关联卡**：Motivates the main theorem card, which obtains the explicit formula by new methods.

### 🔴 `OP-29EB92A146B6` — `solved_in_paper` | MSC 14H10 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, Section 0.2.3 'Pixton's conjecture', Proposition 3 [Pixton \cite{PixDR2}]; proofs of Propositions 3', 3'' in Appendix A
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> For fixed $g$, $A$, and $d$, the class $$\P_g^{d,r}(A) \in R^d(\oM_{g,n})$$ is polynomial in $r$ (for all sufficiently large $r$).

**自包含改写**：For fixed genus $g\geq 0$, fixed double ramification data $A=(a_1,\ldots,a_n)$ with $\sum_i a_i=0$, and fixed degree $d$, the class $P_g^{d,r}(A)\in R^d(\overline{M}_{g,n})$ (the stable-graph sum over weightings mod $r$, with factor $r^{-h^1(\Gamma)}$ and $\xi_{\Gamma}$ push-forwards of products of $e^{a_i^2\psi_{h_i}}$ and edge factors $\frac{1-e^{-w(h)w(h')(\psi_h+\psi_{h'})}}{\psi_h+\psi_{h'}}$) is a polynomial in the integer $r$ for all sufficiently large $r$, so its value at $r=0$ (constant term) is well-defined. Proven by Pixton [PixDR2] and proved self-containedly in the paper's Appendix via Ehrhart-type polynomiality for totally unimodular vertex-edge matrices of bipartite graphs plus $p$-adic divisibility by $r^{h^1(\Gamma)}$; the deeper polynomiality in the parts $a_i$ is cited to [PixDR2].

**判定理由**：Fundamental regularization property needed to state Pixton's conjecture; proven in this paper's Appendix (by Pixton).

**关联卡**：Structural ingredient underlying the main theorem card; the same polynomiality holds for the k-twisted classes $P_g^{d,r,k}(A)$ (Propositions 3' and 3'' of Sections 1-2).

### 🔴 `OP-3353B6B7C408` — `solved_in_paper` | MSC 14H10 | 难度 medium

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, Section 0.2.4 'Degree 0', Corollary 3 (\ref{xzz}); preceded by 'No such expressions were known before.'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> For $g\geq 1$, we have $$\lambda_g = (-2)^{-g}\, \xi_*\, \Lambda_{g-1}^{g-1}(0,\ldots,0)\ \in R^g(\oM_{g,n})\ .$$

**自包含改写**：For $g\geq 1$ (and markings as in the ambient discussion, with stability $2g-2+n>0$), let $\lambda_g$ be the top Chern class of the Hodge bundle $\mathbb{E}\to\overline{M}_{g,n}$, let $\xi:\overline{M}_{g-1,n+2}\to\overline{M}_{g,n}$ be the boundary map associated to the divisor of curves with a nonseparating node (gluing the last two markings), and let $\Lambda_{g-1}^{g-1}(0,\ldots,0)\in R^{g-1}(\overline{M}_{g-1,n+2})$ be the explicit tautological class obtained from Pixton's formula at zero double ramification data $A=(0,\ldots,0)$ (only stable graphs without separating edges contribute). Then $\lambda_g=(-2)^{-g}\xi_*\Lambda_{g-1}^{g-1}(0,\ldots,0)$ in $R^g(\overline{M}_{g,n})$. Previously only the existence of some Chow class $\gamma_{g-1,n+2}\in A^{g-1}(\overline{M}_{g-1,n+2})$ with $\lambda_g=\xi_*\gamma_{g-1,n+2}$ was known; no explicit tautological such expression was known before.

**判定理由**：Explicit tautological boundary expression for lambda_g, resolving a previously unknown desideratum, proven as Corollary 3 of the main theorem.

**关联卡**：Degree-zero specialization of the main theorem, using $DR_g(0,\ldots,0)=(-1)^g\lambda_g$.

### 🔴 `OP-96F98877B3D6` — `solved_in_paper` | MSC 14H10 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, Section 0.2.3 'Pixton's conjecture', Theorem 1 (\ref{FFFF}); also announced in the abstract
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> For $g\geq 0$ and double ramification data $A$, we have $$\DR_g(A) = 2^{-g}\, \P_g^g(A)\, \in R^g(\oM_{g,n}).$$

**自包含改写**：Let $\overline{M}_{g,n}$ be the moduli space of Deligne-Mumford stable genus $g$ curves with $n$ markings (stability $2g-2+n>0$; Chow groups with $\mathbb{Q}$-coefficients). For double ramification data $A=(a_1,\ldots,a_n)\in\mathbb{Z}^n$ with $\sum_i a_i=0$, let $\mu$ and $\nu$ be the partitions given by the positive and negated negative parts, let $D=|\mu|=|\nu|$, and let $I$ be the markings with $a_i=0$; the double ramification cycle is $DR_g(A)=\epsilon_*[\overline{M}_{g,I}(\mathbb{P}^1,\mu,\nu)^{\sim}]^{vir}\in A^g(\overline{M}_{g,n})$, the push-forward of the virtual fundamental class of the moduli space of stable maps to rubber. Let $P_g^d(A)\in R^d(\overline{M}_{g,n})$ be the degree-$d$ component of Pixton's formula, i.e. the value at $r=0$ of the polynomial $P_g^{d,r}(A)=\sum_{\Gamma\in G_{g,n}}\sum_{w\in W_{\Gamma,r}}\frac{1}{|Aut(\Gamma)|}\frac{1}{r^{h^1(\Gamma)}}\xi_{\Gamma*}[\prod_{i=1}^n e^{a_i^2\psi_{h_i}}\prod_{e=(h,h')}\frac{1-e^{-w(h)w(h')(\psi_h+\psi_{h'})}}{\psi_h+\psi_{h'}}]$, a sum over stable graphs of genus $g$ with $n$ legs and weightings mod $r$. Pixton's 2014 conjecture, proved here: for all $g\geq 0$ and all double ramification data $A$, $DR_g(A)=2^{-g}P_g^g(A)$ in $R^g(\overline{M}_{g,n})$.

**判定理由**：Pixton's 2014 conjectural explicit formula for the double ramification cycle is the paper's main theorem; the paper proves it.

**关联卡**：This theorem answers Eliashberg's 2001 question (separate card); the vanishing Theorem 2 (d>g) and Corollary 3 (lambda_g formula) are companion solved statements.

### 🔴 `OP-B23F29691863` — `solved_in_paper` | MSC 14H10 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Abstract
- 自检：conditions_complete: no | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> The result answers a question of Eliashberg from 2001 and specializes to Hain's formula in the compact type case.

**自包含改写**：The paper states that its main result — the proof of Pixton's explicit formula $DR_g(A)=2^{-g}P_g^g(A)$ for the double ramification cycle on the Deligne-Mumford compactification $\overline{M}_{g,n}$ (defined via the virtual fundamental class of the moduli space of stable maps to rubber, $DR_g(A)=\epsilon_*[\overline{M}_{g,I}(\mathbb{P}^1,\mu,\nu)^{\sim}]^{vir}$ for $A=(a_1,\ldots,a_n)$, $\sum_i a_i=0$) — answers a question posed by Y. Eliashberg in 2001 concerning double ramification cycles (regarding the extension of the double ramification locus/cycle to the moduli of stable curves). The precise formulation of Eliashberg's question is not reproduced in the paper.

**判定理由**：A question (Eliashberg 2001) that the paper claims its main theorem answers; resolved by this paper's result.

**⚠️ 人工复核标记**：Eliashberg's 2001 question is not stated verbatim anywhere in the paper; the card records only the paper's claim that the main theorem answers it.

**关联卡**：Answered by the main theorem card (Theorem 1).

### 🔴 `OP-FE26348C5439` — `solved_in_paper` | MSC 14H10 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, Section 0.2.3, Theorem 2 [Clader-Janda \cite{cj}] (\ref{Thm:van}), introduced by 'for $d>g$, the following vanishing conjectured by Pixton is now established.'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> For all $g\geq 0$, double ramification data $A$, and $d>g$, we have $$\P_g^d(A) = 0 \, \in R^d(\oM_{g,n}) .$$

**自包含改写**：For all $g\geq 0$, all double ramification data $A=(a_1,\ldots,a_n)\in\mathbb{Z}^n$ with $\sum_i a_i=0$, and all integers $d>g$, the degree-$d$ component $P_g^d(A)\in R^d(\overline{M}_{g,n})$ of Pixton's formula (the $r=0$ constant term of the stable-graph sum over weightings mod $r$) vanishes: $P_g^d(A)=0$. This was Pixton's vanishing conjecture; it is established by Clader-Janda [cj] and reported here as Theorem 2, together with its extension to all twists $k\in\mathbb{Z}$ of the $k$-twisted classes $P_g^{d,k}(A)$ (defined for $\sum_i a_i=k(2g-2+n)$ via $k$-weightings mod $r$).

**判定理由**：Pixton's vanishing conjecture for d>g, reported as established (Theorem 2 of Clader-Janda); not open at paper time, though the proof is in companion work.

**⚠️ 人工复核标记**：Theorem 2 is credited to Clader-Janda [cj] (arXiv:1601.02871); this paper reports but does not itself prove the vanishing, so 'solved_in_paper' reflects the paper's reporting status only.

**关联卡**：Companion to the main Theorem 1; complements the d<g classes, which lack a known geometric interpretation (separate card).

**存疑**：Proof located in the companion preprint [cj]; its correctness is not verified within this paper.

### ⚪ `OP-2B873394DF50` — `future_application` | MSC 14N35 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, Section 0.2.3 'Pixton's conjecture', closing paragraph of the subsection
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In a forthcoming paper \cite{forth}, we will generalize Pixton's formula to the situation of maps to a ${\mathbb{P}}^1$-rubber bundle over a target manifold~$X$.

**自包含改写**：The authors announce, in a forthcoming paper [forth], a generalization of Pixton's formula for double ramification cycles to the situation of maps to a $\mathbb{P}^1$-rubber bundle over a target manifold $X$. This is an announced research program, not a mathematical proposition; no hypotheses or parameter ranges beyond the target geometry are specified in the paper.

**判定理由**：Announcement of future work; an outlook statement, not a proposition.

**关联卡**：Same forthcoming paper [forth] as the announced study of the rubber over the A_n-singularity resolution (other card).

### ⚪ `OP-9D1629BC0A2A` — `future_application` | MSC 14N35 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 4.3 'Local theory of curves', final paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In the forthcoming paper \cite{forth}, we will study the Gromov-Witten theory of the rubber over the resolution of the $A_n$-singularity where the full structure is needed.

**自包含改写**：The authors announce, in the forthcoming paper [forth], a study of the Gromov-Witten theory of the rubber over the resolution of the $A_n$-singularity, a setting in which the full (non-compact-type) structure of the double ramification cycle proven in this paper is needed (by contrast, the local-curves computation in Section 4.3 of this paper only required Hain's compact-type formula). This is an announced research direction, not a mathematical proposition.

**判定理由**：Outlook on future application of the paper's result; not a proposition.

**关联卡**：Companion announcement to the rubber-bundle-over-X generalization (same forthcoming paper [forth]).

### ⚪ `OP-D278795EC47D` — `future_application` | MSC 14H10 | 难度 hard

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, Section 0.2.3 'Pixton's conjecture', paragraph preceding Theorem 2
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> For $d<g$,  the classes $\P_g^d(A)$ do not yet have a geometric interpretation.

**自包含改写**：For double ramification data $A=(a_1,\ldots,a_n)$ with $\sum_i a_i=0$ and codimensions $d<g$, the tautological classes $P_g^d(A)\in R^d(\overline{M}_{g,n})$ (degree-$d$ components of Pixton's formula, defined as the $r=0$ constant term of the weighted stable-graph sum over weightings mod $r$) have no known geometric interpretation. This is a stated research direction (find a geometric construction of these classes), not a mathematical proposition; the paper formulates no conjecture about it.

**判定理由**：An interpretation gap/taste remark, not a decidable proposition; explicitly not taskified per discipline rules.

**关联卡**：Complementary to the vanishing Theorem 2: for d>g the classes vanish, for d<g they lack geometric meaning, and for d=g the class equals 2^g DR_g(A).


## `1311.2374` — Riemann-Hilbert correspondence for holonomic D-modules
- 权威出处：**Publications Mathématiques de l'IHÉS** 2016，DOI `10.1007/s10240-015-0076-y`
- 连接方式：`doi`｜全文 302,914 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟠 `OP-4809CCF571F0` — `method_obstruction` | MSC 32C38 | 难度 easy

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, §1.5 (final sentence)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Since $\drt_X(\she^\varphi_{X\setminus Y|X}) \simeq \drt_X(\she^{2\varphi}_{X\setminus Y|X})$, one cannot reconstruct $\shm$ from $\drt_X(\shm)$.

**自包含改写**：Let X be a complex manifold, Y ⊂ X a closed hypersurface, φ ∈ Γ(X; O_X(*Y)) a meromorphic function with poles on Y, U = X∖Y, and ℰ^φ_{U|X} the exponential D_X-module generated by e^φ. Let DRt_X(ℳ) = Ω^t_X⊗^L_{D_X}ℳ be the tempered de Rham complex, where Ω^t_X = Ω_X⊗^L_{O_X}O^t_X and O^t_X is the ind-sheaf of tempered holomorphic functions. The paper proves DRt_X(ℰ^φ_{U|X}) ≅ Rℐhom(ℂ_U, 'ind-lim'_{a→+∞} ℂ_{{x ∈ U : −Re φ(x) < a}})[dim_ℂ X], from which DRt_X(ℰ^φ_{U|X}) ≅ DRt_X(ℰ^{2φ}_{U|X}). Consequently a holonomic D_X-module ℳ cannot in general be reconstructed from DRt_X(ℳ): tempered de Rham data on X alone are insufficient and an enhancement (an extra real variable) is required. Demonstrated obstruction; not a posed problem.

**判定理由**：The paper demonstrates that the tempered de Rham complex still loses information (cannot distinguish exponentials e^φ and e^{2φ}); a method failure, no problem posed.

**关联卡**：Second motivating obstruction for the main theorem card; shows the intermediate tempered de Rham functor DRt_X is still insufficient and motivates the enhancement by an extra t-variable.

**存疑**：Consistency check performed: by the displayed formula, the ind-limits for φ and 2φ agree via the cofinal reparametrization a ↦ a/2 of the index a→+∞, so the quoted isomorphism is sound.

### 🟠 `OP-69BDC35C68EF` — `method_obstruction` | MSC 32C38 | 难度 easy

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, §1.4
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Since $\dr_X(\shm) \simeq \dr_X(\shm_\reg)$, it follows that $\shm$ cannot be reconstructed from $\dr_X(\shm)$.

**自包含改写**：Let X be a complex manifold of complex dimension d_X, ℳ an irregular holonomic D_X-module, DR_X(ℳ)=Ω_X⊗^L_{D_X}ℳ its holomorphic de Rham complex, and Ψ_X(L)=Thom(D_X L, O_X)[d_X] the reconstruction functor of the classical Riemann-Hilbert correspondence (Thom = holomorphic functions tempered along the indicated ℝ-constructible sheaf; D_X L = RHom(L, ω_X) the dual). Setting ℳ_reg := Ψ_X(DR_X(ℳ)), a regular holonomic D_X-module, one has DR_X(ℳ) ≅ DR_X(ℳ_reg); consequently ℳ cannot be reconstructed from DR_X(ℳ): the ordinary de Rham functor discards irregularity data. This negative statement is derived in the paper as motivation; no open problem is posed.

**判定理由**：The paper demonstrates that the classical de Rham functor loses irregularity information; a method failure stated as motivation, with no open problem formally posed.

**关联卡**：Motivating obstruction for the main theorem card; shows the classical target (constructible sheaves via DR_X) cannot detect irregularity.

**存疑**：This insufficiency of the de Rham functor is classical, implicit in Kashiwara's 1984 regular Riemann-Hilbert correspondence; the paper restates it as motivation.

### 🔴 `OP-1DB038934A22` — `solved_in_paper` | MSC 32C38 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, §1.6
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> In this paper, we will show that $\shm$ can be reconstructed from the tempered de Rham complex $\drt_{X\times \PP}(\shm \detens \she_{\C|\PP}^{-\tau})$, an object of $\BDC(\iCfield_{X\times\PP})$.

**自包含改写**：Let X be a complex manifold, ℳ ∈ D^b_hol(D_X) a holonomic D_X-module, ℂP^1 the complex projective line with affine coordinate τ ∈ ℂ ⊂ ℂP^1, and ℰ^{-τ}_{ℂ|ℂP^1} the exponential D_{ℂP^1}-module generated by e^{-τ}. For a complex manifold N let DRt_N(−)=Ω^t_N⊗^L_{D_N}(−) be the tempered de Rham complex, with Ω^t_N=Ω_N⊗^L_{O_N}O^t_N and O^t_N the ind-sheaf complex of tempered holomorphic functions. The statement, announced in the introduction and proved by the paper's arguments (the case where X is a complex curve was outlined earlier in D'Agnolo–Kashiwara 2012), is that ℳ can be reconstructed from the tempered de Rham complex DRt_{X×ℂP^1}(ℳ ⊠^D ℰ^{-τ}_{ℂ|ℂP^1}), an object of D^b(I ℂ_{X×ℂP^1}); indeed, for i : X×ℝ_∞ → X×ℂP^1 the natural morphism, DR^E_X(ℳ) ≅ i^! DRt_{X×ℂP^1}(ℳ ⊠^D ℰ^{-τ}_{ℂ|ℂP^1})[1] and the paper proves ℳ ≅ Ψ^E_X(DR^E_X(ℳ)).

**判定理由**：A specific reconstruction theorem announced in the introduction; its general proof follows from this paper's arguments (curve case previously in D'Agnolo–Kashiwara 2012), so solved here.

**⚠️ 人工复核标记**：Announced in the introduction; the paper says the general-case proof 'follows from the arguments in the present paper' (a consequence of the numbered enhanced reconstruction theorem) rather than isolating it as a separately numbered theorem.

**关联卡**：Implementation/consequence of the main enhanced Riemann-Hilbert theorem card; differs in that reconstruction is asserted inside D^b(I ℂ_{X×ℂP^1}) before passing to the enhanced quotient category.

### 🔴 `OP-BCF04E3F2B6A` — `solved_in_paper` | MSC 32C38 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, §1.2
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> The problem of extending the Riemann-Hilbert correspondence to cover the case of holonomic $\D$-modules with irregular singularities has been open for 30 years.

**自包含改写**：Let X be a complex manifold, D_X its sheaf of differential operators, D^b_rh(D_X) the bounded derived category of regular holonomic D_X-modules and D^b_c(ℂ_X) that of ℂ-constructible sheaves; the classical Riemann-Hilbert correspondence (Kashiwara 1984) has quasi-inverse functors the de Rham functor DR_X(ℳ)=Ω_X⊗^L_{D_X}ℳ and Ψ_X(L)=Thom(D_X L, O_X)[d_X]. The problem—open for the 30 years preceding this paper—was to extend this correspondence to holonomic D_X-modules which are not necessarily regular. The paper resolves it: it introduces the triangulated category E^b(ℂ_X) of enhanced ind-sheaves (a quotient of D^b(I ℂ_{X×ℝ_∞}), where ℝ_∞=(ℝ, ℝ∪{+∞,−∞}) is a bordered space), its full subcategory E^b_Rc(ℂ_X) of ℝ-constructible objects, the enhanced de Rham functor DR^E_X(ℳ)=Ω^E_X⊗^L_{D_X}ℳ and the reconstruction functor Ψ^E_X(K)=ℋom^E(D^E_X K, O^E_X)[d_X], and proves: (i) DR^E_X : D^b_hol(D_X) → E^b(ℂ_X) is fully faithful and takes values in E^b_Rc(ℂ_X); (ii) ℳ ≅ Ψ^E_X(DR^E_X(ℳ)) functorially in ℳ ∈ D^b_hol(D_X), so any holonomic complex ℳ can be reconstructed from DR^E_X(ℳ).

**判定理由**：The paper's own central target, explicitly open for thirty years; the paper proves it: full faithfulness and reconstruction for the enhanced de Rham functor on all holonomic D-modules.

**⚠️ 人工复核标记**：Two notes: (a) the paper proves full faithfulness and reconstruction but not essential surjectivity of DR^E_X onto E^b_Rc(k_X), and never poses essential surjectivity as an open problem; (b) the provided source omits ~42,914 characters from the middle (region of Sections 3–5); extraction is based on the visible portions.

**关联卡**：Resolves the problem motivating the obstruction cards on DR_X and DRt_X below; the reconstruction-from-tempered-de-Rham-on-X×P^1 card records the concrete mechanism announced in the introduction.

### ⚪ `OP-CE6D15978DAD` — `future_application` | MSC 32C38 | 难度 easy

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 2 (Notations and complements), opening of §2.1
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In this paper, we take a field $\field$ as base ring. However, after minor modifications, one can take any regular ring as base ring.

**自包含改写**：The paper develops its theory of sheaves, ind-sheaves, bordered spaces, enhanced ind-sheaves and holonomic D-modules over a base field k (sheaves of k-vector spaces). The authors remark that, after minor modifications, any regular ring can be taken as base ring instead of a field. This is a generality/extensibility comment about the framework, explicitly not a mathematical proposition posed or settled within the paper, and per the no-taskification rule it is not turned into a research task.

**判定理由**：Taste/generality remark on the base ring; not a mathematical proposition posed or resolved here, so labelled future_application per the no-taskification rule.


## `1410.0938` — Effectivity of Iitaka fibrations and pluricanonical systems of polarized pairs
- 权威出处：**Publications Mathématiques de l'IHÉS** 2016，DOI `10.1007/s10240-016-0080-x`
- 连接方式：`title-exact`｜全文 139,284 字符 via `cache-latex`｜提取模式 `reasoning`

### 🟢 `OP-330A878EA2E6` — `real_open` | MSC 14E30 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Section 4, opening paragraph of 'LMMP for generalized polarized pairs'
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> One can ask whether one can run an LMMP$/Z$ on $K_{X'}+B'+M'$ and whether it terminates. We cannot answer this question in such generality but we will put some extra assumptions under which the answer would be yes.

**自包含改写**：Let $(X',B'+M')$ be a $\mathbb{Q}$-factorial generalized lc polarized pair with data $X \overset{f}{\to} X' \to Z$ and $M$ (i.e., $f\colon X\to X'$ projective birational with $X$ normal, $X\to Z$ projective, $B'$ an $\mathbb{R}$-boundary, $M$ an $\mathbb{R}$-Cartier divisor on $X$ nef over $Z$, $M'=f_*M$, and $K_{X'}+B'+M'$ $\mathbb{R}$-Cartier; generalized lc means all generalized log discrepancies are $\ge 0$). Question posed in the paper: can one run a log minimal model program over $Z$ on $K_{X'}+B'+M'$, and does it terminate? The paper cannot answer this in such generality. Under extra assumptions (there is an $\mathbb{R}$-Cartier $A'\ge 0$, big over $Z$, with $K_{X'}+B'+M'+A'$ nef$/Z$ and condition (*) on klt perturbations), the paper shows the LMMP with scaling of $A'$ can be run but explicitly states termination is not known; termination is proved only under additional hypotheses (not pseudo-effective$/Z$ gives a Mori fibre space; pseudo-effective$/Z$ plus generalized klt plus $K_{X'}+(1+\alpha)B'+(1+\beta)M'$ $\mathbb{R}$-Cartier and big$/Z$ gives a semi-ample minimal model).

**判定理由**：Question explicitly posed and left open in this generality; termination remains unknown even where the paper shows the LMMP exists.

**关联卡**：Motivated by the method obstructions: an LMMP on $K_X+B+M$ may destroy the nef/Cartier property of $rM$, forcing generalized polarized pairs (see method_obstruction cards).

### 🟢 `OP-574AD9566101` — `real_open` | MSC 14E30 | 难度 frontier

- 论文当时状态：`open_at_paper_time` → 当前状态：`unknown`
- 出处：Introduction, Conjecture 1.1 ('Effective Iitaka fibration')
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Let $W$ be a smooth projective variety of dimension $d$ and Kodaira dimension $\kappa(W)\ge 0$. Then there is a natural number $m_d$ depending only on $d$ such that the pluricanonical system $|mK_W|$ defines an Iitaka fibration for any natural number $m$ divisible by $m_d$.

**自包含改写**：Conjecture (Effective Iitaka fibration; attributed to Hacon-McKernan): Let $W$ be a smooth projective variety over the complex numbers, of dimension $d$, with Kodaira dimension $\kappa(W)\ge 0$. Then there exists a natural number $m_d$ depending only on $d$ (not on $W$) such that for every natural number $m$ divisible by $m_d$, the pluricanonical linear system $|mK_W|$ defines an Iitaka fibration of $W$ (a rational map birationally equivalent to a fibration $W \dashrightarrow X$ with $\dim X = \kappa(W)$ and very general fibre of Kodaira dimension $0$). Known previously for $\dim W \le 3$; this paper proves only the variant (Theorem A) where $m$ also depends on two fibre invariants $b_F, \beta_{\widetilde F}$, so the conjecture with $m_d$ depending only on $d$ is left open.

**判定理由**：Formally stated conjecture, the paper's central target; only a weakened version with extra fibre invariants is proved, so it remains open here.

**关联卡**：Theorem A (solved_in_paper card) proves the bounded-invariant version; the abundance conjecture (background_open card) is identified as the likely obstruction to removing the extra assumptions.

### 🔵 `OP-2DAB61359DD2` — `background_open` | MSC 14E30 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, discussion immediately after Conjecture 1.1
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Without these extra assumptions the above conjecture seems out of reach at the moment because most likely one needs the abundance conjecture to deal with the very general fibres. For example, when $\kappa(W)=0$, the conjecture is equivalent to the effective nonvanishing $h^0(W,m_dK_W)\neq 0$ which is obviously related to the abundance conjecture.

**自包含改写**：The abundance conjecture (a standard open problem of the minimal model program; usual form: if $(X,B)$ is a projective lc pair with $K_X+B$ nef then $K_X+B$ is semi-ample) is cited as background: proving the effective Iitaka fibration conjecture without extra boundedness assumptions on invariants of the very general fibres would most likely require abundance for those fibres; in particular, when $\kappa(W)=0$ the conjecture is equivalent to the effective nonvanishing $h^0(W,m_dK_W)\neq 0$, which is related to abundance. The abundance conjecture itself is not attacked in this paper.

**判定理由**：Abundance conjecture cited only as motivation/obstruction; the paper neither poses nor solves it.

**关联卡**：Identified obstruction to Conjecture 1.1 (real_open card) without the bounded fibre invariants.

**存疑**：The abundance conjecture is not formulated precisely in this source; the standard statement is supplied for self-containedness.

### 🔵 `OP-8E66776DF30F` — `background_open` | MSC 14E30 | 难度 hard

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Introduction, discussion after Conjecture 1.1
- 自检：conditions_complete: no | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Note that there is also a log version of the conjecture for pairs: see [\ref{HX}, Conjecture 1.2, Theorem 1.4] and the references therein, where the authors confirmed this log version when the boundary divisor is big over the generic point of the base of the log Iitaka fibration.

**自包含改写**：A logarithmic (pair) analogue of the effective Iitaka fibration conjecture exists (formulated in Hacon-Xu, Conjecture 1.2, arXiv:1410.8187); this paper cites it only as related background, noting that Hacon-Xu confirmed this log version in the case where the boundary divisor is big over the generic point of the base of the log Iitaka fibration. The precise statement of the log conjecture is not reproduced in this source, so its full hypotheses cannot be inlined here.

**判定理由**：Conjecture of Hacon-Xu cited as related background; neither adopted as this paper's target nor solved here.

**⚠️ 人工复核标记**：Precise formulation of the log conjecture must be retrieved from [Hacon-Xu, Conjecture 1.2]; this source only describes its known partial resolution.

**关联卡**：Log analogue of Conjecture 1.1 (real_open card).

**存疑**：The source gives only a citation-level description; the card reflects only what this paper states.

### 🟠 `OP-AC553ECF5395` — `method_obstruction` | MSC 14E30 | 难度 

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, 'About this paper' paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Since the statement of Theorems \ref{t-bir-bnd-M}, \ref{t-acc-glct}, and \ref{t-global-acc} involve nef divisors which may not be semi-ample (or effectively semi-ample), there does not seem to be any easy way to reduce them to the traditional versions (i.e. without nef divisors) proved in [\ref{HMX2}] or to mimic the arguments in [\ref{HMX2}].

**自包含改写**：Methodological obstruction (not a posed problem): the paper's main theorems (effective birationality of $|m(K_X+B+M)|$ for projective lc pairs $(X,B)$ with $K_X+B+M$ big; ACC for generalized lc thresholds; global ACC for generalized lc pairs with $K_{X'}+B'+M'\equiv 0$) all involve nef divisors $M$ which may not be semi-ample or effectively semi-ample. Consequently there is no easy reduction of these statements to the traditional versions without nef parts proved by Hacon-McKernan-Xu, nor can the arguments of that work be directly mimicked; new ideas occupy most of the paper.

**判定理由**：States that a method (reduction to or mimicry of Hacon-McKernan-Xu arguments) fails because nef parts may not be semi-ample; no open problem posed.

**关联卡**：Companion obstruction: Section 3 notes an LMMP on $K_X+B+M$ may lose the nef/Cartier property of $rM$ (see other method_obstruction card).

### 🟠 `OP-D4FFD67E41A9` — `method_obstruction` | MSC 14E30 | 难度 

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 3, introductory paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In contrast if one runs an LMMP on $K_X+B+M$, the nef and Cartier properties of $rM$ may be lost, hence one needs to consider generalized polarized pairs which will be discussed in later sections.

**自包含改写**：Methodological observation (not a posed problem): let $(X,B)$ be a projective lc pair, $r$ a natural number, and $rM$ a nef Cartier divisor. Running a log minimal model program on $K_X+B+M$ may destroy the nefness and the Cartier property of $rM$; by contrast, running the LMMP on $K_X+B+nM$ with $n/r$ sufficiently large preserves them, by Kawamata's boundedness of the length of extremal rays, which is what allows applying Hacon-McKernan-Xu methods in that special case. This loss is the reason the paper introduces generalized polarized pairs.

**判定理由**：Observes an LMMP on $K_X+B+M$ can destroy the nef/Cartier properties of $rM$, motivating a new framework; no open problem posed.

**关联卡**：Concrete mechanism behind the introduction's obstruction about non-semi-ample nef divisors (see other method_obstruction card) and motivation for the LMMP question for generalized pairs (real_open card).

### 🔴 `OP-45844D95441B` — `solved_in_paper` | MSC 14E30 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Introduction, Theorem A; proof given at end of Section 8
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $W$ be a smooth projective variety of dimension $d$ and Kodaira dimension $\kappa(W)\ge 0$. Then there is a natural number $m(d, b_F, \beta_{\widetilde{F}})$ depending only on $d$, $b_F$ and $\beta_{\widetilde{F}}$ such that the pluricanonical system $|mK_W|$ defines an Iitaka fibration whenever the natural number $m$ is divisible by $m(d, b_F, \beta_{\widetilde{F}})$.

**自包含改写**：Theorem A (proved in the paper, answering the formulation of the effective Iitaka fibration problem in Viehweg-Zhang, Question 0.1): Let $W$ be a smooth projective variety over $\mathbb{C}$ of dimension $d$ with Kodaira dimension $\kappa(W)\ge 0$. Let $V\to X$ be an Iitaka fibration from a resolution $V$ of $W$ (so $\dim X=\kappa(W)$) and $F$ a very general fibre. Define $b_F=\min\{u\in\mathbb{N}\mid |uK_F|\neq\emptyset\}$, let $\widetilde F$ be a smooth model of the $\mathbb{Z}/(b_F)$-cover of $F$ ramified over the unique divisor in $|b_FK_F|$, let $d_F=\dim\widetilde F=\dim W-\kappa(W)$, and $\beta_{\widetilde F}=\dim H^{d_F}(\widetilde F,\mathbb{C})$. Then there is a natural number $m(d,b_F,\beta_{\widetilde F})$ depending only on $d$, $b_F$, $\beta_{\widetilde F}$ such that $|mK_W|$ defines an Iitaka fibration whenever $m\in\mathbb{N}$ is divisible by it. When $W$ is of general type, $m$ depends only on $d$. It is derived from Theorem 1.2: for a DCC set $\Lambda$ of nonnegative reals and $d,r\in\mathbb{N}$ there is $m(\Lambda,d,r)$ such that $|m(K_X+B+M)|$ defines a birational map for any projective lc pair $(X,B)$ of dimension $d$ with coefficients of $B$ in $\Lambda$, $rM$ nef Cartier, $K_X+B+M$ big, and $m$ divisible by $m(\Lambda,d,r)$.

**判定理由**：This is Theorem A, proved in the paper; it resolves the [VZ, Question 0.1] version of effective Iitaka fibration with bounded fibre invariants.

**关联卡**：Solves the bounded-invariant variant of Conjecture 1.1 (real_open card); the unconditional conjecture (m depending only on d) remains open.

### ⚪ `OP-E1AD97A9CEF5` — `future_application` | MSC 14E30 | 难度 

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Introduction, 'Generalized polarized pairs' paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In order to prove Theorems \ref{t-bir-bnd-M} and \ref{t-acc-glct} we need to generalize the definitions of pairs, singularities, lc thresholds, adjunction, etc. We develop this theory, which is of independent interest, in some detail in Section 4 but for now we only give the definition of generalized polarized pairs.

**自包含改写**：Value judgement (not a mathematical proposition): the generalized theory of pairs, singularities, log canonical thresholds, and adjunction developed in Section 4 of the paper - needed to prove the effective birationality theorem (Theorem on $|m(K_X+B+M)|$) and the ACC theorem for generalized lc thresholds - is described by the authors as being 'of independent interest', i.e., expected to be useful beyond this paper's proofs. No specific open problem or research task is stated.

**判定理由**：Taste comment ('of independent interest') about newly developed machinery; not a proposition, so it is not taskified.

**关联卡**：The theory in question underlies the LMMP question for generalized polarized pairs (real_open card).


## `1211.2678` — A proof of the Grothendieck–Serre conjecture on principal bundles over regular local rings containing infinite fields
- 权威出处：**Publications Mathématiques de l'IHÉS** 2015，DOI `10.1007/s10240-015-0075-z`
- 连接方式：`doi`｜全文 71,879 字符 via `cache-latex`｜提取模式 `reasoning`

### 🔵 `OP-45DD18C6F118` — `background_open` | MSC 14L30 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1.1 (History of the topic), first paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> In his 1958 paper Jean--Pierre Serre asked whether a principal bundle is Zariski locally trivial, once it has a rational section  (see~\cite[Remarque, p.31]{Se}). In his setup the group is any algebraic group over an algebraically closed field.

**自包含改写**：Serre's 1958 question: in his setup the group is any algebraic group over an algebraically closed field, and the question is whether a principal bundle for such a group is locally trivial in the Zariski topology once it has a rational section. Serre gave an affirmative answer when the group is PGL(n) and when the group is an abelian variety (both cited). This question is the historical origin of the Grothendieck-Serre conjecture (restated in this paper, see related card); the present paper resolves the reductive-group-scheme version over regular local rings containing infinite fields. The status of the original question for arbitrary (e.g., non-reductive) algebraic groups is not discussed in the paper.

**判定理由**：Serre's 1958 question recalled purely as historical motivation; the paper resolves only its reductive regular-local descendant, not the general question for arbitrary algebraic groups.

**⚠️ 人工复核标记**：The precise scope of Serre's original question (base of the bundle, non-reductive or non-connected groups) is only recalled historically and not delimited in this paper.

**关联卡**：Historical origin of the Grothendieck-Serre conjecture card; the same history section also recalls Grothendieck's variant for semi-simple group schemes over arbitrary regular schemes.

**存疑**：The base scheme/variety of the bundle in Serre's original question is not spelled out in this paper; the paper only recalls the question historically.

### 🔵 `OP-4C2BD20A02A4` — `background_open` | MSC 14L30 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), Conjecture 1 (the Grothendieck-Serre conjecture)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> Let $R$ be a regular local ring, let $K$ be its field of fractions. Let~$\bG$ be a reductive group scheme over $U:=\spec R$, let $\cG$ be a principal $\bG$-bundle. If~$\cG$ is trivial over $\spec K$, then it is trivial. Equivalently, the map of non-abelian cohomology pointed sets $H^1_{\text{\'et}}(R,\bG)\to H^1_{\text{\'et}}(K,\bG)$ induced by the inclusion of $R$ into $K$ has a trivial kernel.

**自包含改写**：Grothendieck-Serre conjecture in full generality: let R be a regular local ring (with no assumption that R contains a field) and let K be its field of fractions. Let G be a reductive group scheme over U = Spec R (G is affine and smooth as a U-scheme and its geometric fibers are connected reductive algebraic groups), and let C be a principal G-bundle over U. Conjecture: if C is trivial over Spec K, then C is trivial over U; equivalently, the map of non-abelian etale cohomology pointed sets H^1_et(R, G) -> H^1_et(K, G) induced by the inclusion of R into K has trivial kernel. At the time of this paper (version 3) the case where R contains a field was settled (infinite fields here; finite fields by Panin in the cited companion paper), while in mixed characteristic only the split case under strong conditions on R was known (Fedorov, cited); the general mixed-characteristic case was open.

**判定理由**：Famous conjecture attributed to Grothendieck and Serre, restated as motivating background; the paper proves only the case where R contains an infinite field, so the general conjecture (notably mixed characteristic) remains open.

**⚠️ 人工复核标记**：Labeling judgment call: the paper restates this famous conjecture and proves its infinite-field case; the open residue at paper time is the mixed-characteristic case (covered by cited Fedorov work only for split G under unspecified 'strong conditions on the local ring'), which could alternatively be filed as a problem left open by this paper.

**关联卡**：General form of the solved card (Theorem* / MainThm1 in this paper); the Serre-1958-question card is its historical origin; per the paper, Panin's cited companion work settles regular local rings containing finite fields, so after this paper the conjecture holds for all regular local rings containing a field, leaving mixed characteristic open.

**存疑**：Gabber's announced (unpublished) proof for group schemes coming from arbitrary ground fields is cited without verification; the 'strong conditions on the local ring' in the cited mixed-characteristic result of Fedorov are not specified in this paper.

### 🟠 `OP-D4501096E847` — `method_obstruction` | MSC 14L30 | 难度 easy

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 2 (Main results), item 3 of the unnumbered Remarks following the theorem with label MainThm2
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> On the other hand, if~$\bG$ is anisotropic, this restriction is not in general trivial. For an example see~\cite{FedorovExotic}.

**自包含改写**：Context: the paper's projective-line theorem (label MainThm2) assumes R is the semi-local ring of finitely many closed points on an irreducible smooth affine variety over an infinite field k, U = Spec R, G a simple simply-connected group scheme over U, Z a closed subscheme of P^1_U finite over U, Y a closed subscheme etale over U with G_Y := G x_U Y isotropic, and C a principal G-bundle over P^1_U trivial on P^1_U - Z. The remark notes that if G is isotropic one can take Y = {infinity} x U, so that the restriction of C to the affine line A^1_U is trivial (a partial case of a theorem of Panin-Stavrova-Vavilov); on the other hand, if G is anisotropic, this restriction is not trivial in general (a counterexample is given in the cited companion [FedorovExotic]). This documents that the isotropy hypothesis is needed; no open problem is posed.

**判定理由**：Shows the isotropy hypothesis is necessary: for anisotropic G the restriction to the affine line need not be trivial; counterexample cited, no open problem posed.

**⚠️ 人工复核标记**：The claimed counterexample is cited, not reproduced; its verification lies in the companion [FedorovExotic].

**关联卡**：Concerns necessity of the isotropy hypothesis in the theorem labelled MainThm2, a key input to the solved main-theorem card.

**存疑**：The negative example lives entirely in the cited companion [FedorovExotic]; this paper only asserts it, so paper_time_status 'not_a_proposition' reflects that the paper treats it as a known caveat, not an open target.

### 🔴 `OP-2768CF684915` — `solved_in_paper` | MSC 14L30 | 难度 medium

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 5 (An application), unnumbered corollary (corollary*) immediately after the theorem with label Norms
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Under the hypothesis of Theorem~\ref{Norms} let additionally the $K$-algebraic group $\bG_K$ be $K$-rational as a $K$-variety and let the ring $R$ be of characteristic $0$. Then the norm principle holds for all finite flat $R$-domains $S\supset R$. That is, if $S\supset R$ is such a domain, and $a\in\bT(S)$ belongs to $\mu(\bG(S))$, then the element $N_{S/R}(a)\in\bT(R)$ belongs to $\mu(\bG(R))$.

**自包含改写**：Hypotheses: R is a regular local ring containing an infinite field; G is a reductive R-group scheme; mu : G -> T is a group scheme morphism to an R-torus T, locally surjective in the etale topology on Spec R, with H := Ker(mu) reductive; K is the fraction field of R. Assume additionally that the K-algebraic group G_K is K-rational as a K-variety and that the ring R has characteristic 0. Conclusion (norm principle): for every finite flat R-domain S containing R and every element a in T(S) belonging to mu(G(S)), the norm element N_{S/R}(a) in T(R) belongs to mu(G(R)). Proved in the paper as a corollary of the norm theorem, using a result of Merkurjev.

**判定理由**：Corollary proved in the paper: the norm principle for finite flat R-domains under additional rationality and characteristic-zero hypotheses; follows from the norm theorem and Merkurjev's result.

**关联卡**：Direct corollary of the norm theorem card (theorem labelled Norms in the paper).

### 🔴 `OP-39B3F283D731` — `solved_in_paper` | MSC 14L30 | 难度 frontier

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 2 (Main results), theorem with label MainThm1; the Introduction's unnumbered Theorem* states the regular local ring special case
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $R$ be a regular semi-local domain containing an infinite field, and let $K$ be its field of fractions. If $\bG$ is a reductive group scheme over $R$, then the map $H^1_{\text{\'et}}(R,\bG)\to H^1_{\text{\'et}}(K,\bG)$ induced by the inclusion of $R$ into $K$ has a trivial kernel. In other words, under the above assumptions on $R$ and $\bG$, each principal $\bG$-bundle over $R$ having a $K$-rational point is trivial.

**自包含改写**：Let R be a regular semi-local domain containing an infinite field and let K be its field of fractions. If G is a reductive group scheme over R (affine and smooth over R, with connected reductive geometric fibers), then the map of non-abelian etale cohomology pointed sets H^1_et(R, G) -> H^1_et(K, G) induced by the inclusion of R into K has a trivial kernel; equivalently, each principal G-bundle over R having a K-rational point is trivial. In particular, for R a regular local ring containing an infinite field, every principal G-bundle trivial over Spec K is trivial (the Grothendieck-Serre conjecture in this case), and two principal G-bundles over Spec R that become isomorphic over Spec K are isomorphic.

**判定理由**：The paper's central theorem: proves the Grothendieck-Serre conjecture for regular semi-local domains containing an infinite field (hence for regular local rings containing infinite fields), previously open.

**关联卡**：Resolves the Grothendieck-Serre conjecture card in the case of rings containing infinite fields; proved via intermediate theorems labelled th:psv (affine line) and MainThm2 (projective line; see the method_obstruction card on the isotropy hypothesis). The paper also notes the result was new even for constant group schemes, for split groups of type E_8, and for Spin(A, sigma) with A a skew-field and sigma an orthogonal involution.

### 🔴 `OP-8E21481F42FB` — `solved_in_paper` | MSC 14L30 | 难度 medium

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Section 5 (An application), theorem with label Norms
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $R$ be a regular local ring containing an infinite field and $\bG$ be a reductive $R$-group scheme. Let $\mu:\bG\to\bT$ be a group scheme morphism to an $R$-torus $\bT$ such that $\mu$ is locally in the \'{e}tale topology on $\spec R$ surjective. Assume further that the $R$-group scheme $\bH:=\Ker(\mu)$ is reductive. Let $K$ be the fraction field of $R$. Then the group homomorphism $\bT(R)/\mu(\bG(R))\to\bT(K)/\mu(\bG(K))$ is injective.

**自包含改写**：Let R be a regular local ring containing an infinite field, G a reductive R-group scheme, and mu : G -> T a group scheme morphism to an R-torus T such that mu is locally surjective in the etale topology on Spec R; assume moreover that the R-group scheme H := Ker(mu) is reductive. Let K be the fraction field of R. Then the group homomorphism T(R)/mu(G(R)) -> T(K)/mu(G(K)) is injective. The paper proves this as a straightforward consequence of its main theorem and an exact sequence for etale cohomology, and states that it extends all previously known results of this form.

**判定理由**：Norm-type injectivity theorem, proved in the paper as an application of the main theorem; stated to extend all previously known results of this form.

**关联卡**：Companion to the norm-principle corollary card; both are applications of the solved main-theorem card; the paper cites [C-TO], [PS], [Z], [OPZ] as prior results of this form.

### ⚪ `OP-820411ADE86C` — `future_application` | MSC 14L30 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1.2 (Overview of the proof), final paragraph
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> The proof of Theorem~\ref{MainThm2} is inspired by the theory of affine Grassmannians. We do not use the affine Grassmannians explicitly in this paper, however, the interested reader is invited to look at~\cite{FedorovExotic}, where an alternative proof of our Theorem~\ref{MainThm2} is sketched.

**自包含改写**：Not a mathematical proposition (methodological outlook). The authors state that the proof of their projective-line theorem (label MainThm2; setting: R the semi-local ring of finitely many closed points on an irreducible smooth affine variety over an infinite field, U = Spec R, G simple simply-connected, Z closed finite over U, Y closed etale over U with G_Y isotropic; a principal G-bundle over P^1_U trivial off Z is trivial off Y) is inspired by the theory of affine Grassmannians, that affine Grassmannians are not used explicitly in this paper, and that an alternative proof of that theorem is sketched in the companion paper [FedorovExotic]. The paper also mentions an essentially equivalent proof based on formal loops. No open problem is posed.

**判定理由**：Value/methodological outlook, not a proposition: an alternative affine-Grassmannian-based proof of a key theorem is pointed to in a companion paper.

**关联卡**：Outlook on alternative proofs of the theorem labelled MainThm2, a key input to the solved main-theorem card; the formal-loops variant is mentioned in the organization subsection, citing [FedorovExotic, Sect. 6.2].


## `1303.2325` — Bilipschitz and quasiconformal rotation, stretching and multifractal spectra
- 权威出处：**Publications Mathématiques de l'IHÉS** 2015，DOI `10.1007/s10240-014-0065-6`
- 连接方式：`doi`｜全文 121,814 字符 via `cache-latex`｜提取模式 `fast`

### 🔵 `OP-8D9CE93F76F9` — `background_open` | MSC 30C62 | 难度 hard

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 5.4 (Factoring the logarithmic spiral)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> A basic open question in the study of  bilipschitz mappings (in $\R^n$)
 is whether such a map can be represented as a composition of $(1+\varepsilon)$-bilipschitz mappings, for any $\varepsilon >0$. The factoring is known only in dimension $n = 1$;  see \cite{FM} for  recent general results on this theme.

**自包含改写**：Open question: for n >= 2, can every L-bilipschitz map of R^n be written as a finite composition of (1+eps)-bilipschitz mappings for any eps > 0? The factoring is known only in dimension n = 1.

**判定理由**：Cited as a basic open question from the literature motivating the factoring analysis; not posed as this paper's own target.

**关联卡**：The paper proves Theorem 5.11, a solved special case: factoring the logarithmic spiral map s_gamma requires at least ceil(|gamma|/(L_0 - 1/L_0)) factors of L_0-bilipschitz maps.

### 🔵 `OP-C8DA85480FB0` — `background_open` | MSC 30C62 | 难度 frontier

- 论文当时状态：`background_known_open` → 当前状态：`unknown`
- 出处：Section 4.2 (Burkholder integrals)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> since then optimal integral identities related to $B_p$, and in particular its conjectured  quasiconcavity  (for $|p-1| \geqslant1 $) have been of wide interest.

**自包含改写**：Conjecture (Burkholder): the Burkholder functional B_p(A) = (1/2)(p det A + (2-p)|A|^2)|A|^{p-2} is quasiconcave for real parameters with |p-1| >= 1; i.e. the integral inequality with B_p holds for all weakly quasiregular mappings. This is a famous open problem cited as background.

**判定理由**：The quasiconcavity conjecture for Burkholder functionals is a well-known open problem from the literature, cited as motivation.

**关联卡**：The paper proves a partial quasiconcavity result for Burkholder-type functionals with complex parameter p, 1 <= |p-1| <= 1/k, within the class of principal k-quasiconformal deformations (Theorem 4.4).

**存疑**：The exact quasiconcavity formulation is reconstructed from context; the paper only references it as 'conjectured quasiconcavity'.

### 🔴 `OP-09FA9B890C3A` — `solved_in_paper` | MSC 30C62 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Theorem 1.1, Section 1 (Introduction)
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Suppose $f: \R^2 \to \R^2$ is $L$-bilipschitz and $\gamma$ is a real number such that $|\gamma|  \leqslant L - \frac{1}{L}$. Then 
\begin{equation}
\dim_{\mathcal H}\{ z \in \R^2: \gamma_f(z) = \gamma \} \;  \leqslant 2  \,-\, \frac{2L}{L^2-1}|\gamma|.
\end{equation}
Moreover, for every such $\gamma$ %$|\gamma|  \leqslant L - \frac{1}{L}$  
there exists an $L$-bilipschitz map $f: \R^2 \to \R^2$ for which the equality holds in \eqref{lipdim}.

**自包含改写**：For an L-bilipschitz map f: R^2 -> R^2 (i.e. (1/L)|x-y| <= |f(x)-f(y)| <= L|x-y|), with gamma_f(z) = limsup_{t->0} arg[f(z+t)-f(z)]/log t, the rotational multifractal spectrum satisfies dim_H{z in R^2 : gamma_f(z) = gamma} <= 2 - (2L/(L^2-1))|gamma| for every real gamma with |gamma| <= L - 1/L; and for each such gamma there is an L-bilipschitz map attaining equality.

**判定理由**：Complete theorem with sharp bound proved in the paper (Section 5 via quasiconformal multifractal spectrum with K = L^2, alpha = 1).

**关联卡**：Special case alpha = 1, K = L^2 of Theorem 4.5 (quasiconformal joint spectrum F_K).

### 🔴 `OP-6319CA0A4E78` — `solved_in_paper` | MSC 30C62 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Theorem 1.5, Section 1 (Introduction) / Section 4
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Suppose  $\Psi: \DD \times E \to \C$ is a holomorphic motion of a set $E \subset \C$ and  that $\alpha > 0$ and $\gamma \in \R$ are given.  

If $\lambda \in \DD$, assume that at every  
point $z \in E$ we have  scales $r_j \to 0$ along which $\Psi_\lambda(z)=\Psi(\lambda,z)$  stretches with exponent $\alpha$,
$$ \lim_{j\to\infty}\frac{\log |\Psi_\lambda(z+r_j)-\Psi_\lambda(z)|}{\log r_j} =  \alpha, \qquad z \in E,$$ 
 and simultaneously rotates with rate $\gamma$, 
$$ \lim_{j\to\infty}\frac{\arg (\Psi_\lambda(z+r_j)-\Psi_\lambda(z))}{\log |\Psi_\lambda(z+r_j)-\Psi_\lambda(z)|}=  \gamma,  \qquad z \in E.$$
Then 
\begin{equation}
\dim(E)\;  \leqslant \;   1+\alpha \,-\, \frac{1}{|\lambda|} \s…

**自包含改写**：If Psi: D x E -> C (D the unit disk) is a holomorphic motion of a set E in C, lambda in D, alpha > 0, gamma in R, and at every z in E there are scales r_j -> 0 with log|Psi_lambda(z+r_j)-Psi_lambda(z)|/log r_j -> alpha and arg(Psi_lambda(z+r_j)-Psi_lambda(z))/log|Psi_lambda(z+r_j)-Psi_lambda(z)| -> gamma, then dim(E) <= 1 + alpha - (1/|lambda|) sqrt((1-alpha)^2 + (1-|lambda|^2) alpha^2 gamma^2). The bound is sharp: equality is attained by some set E and holomorphic motion whenever the right hand side is nonnegative.

**判定理由**：Sharp dimension bound for holomorphic motions proved in the paper from the quasiconformal joint spectrum.

**关联卡**：Deduced from Theorem 4.5 (F_K) and Slodkowski's lambda-lemma with K(Psi_lambda) <= (1+|lambda|)/(1-|lambda|).

### 🔴 `OP-8EB63D8751D3` — `solved_in_paper` | MSC 30C62 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Corollary 1.3 (Corollary 4.8), Section 1 / Section 4.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Suppose  $f$ is a $K$-quasiconformal map on a domain $\Omega\subset\C$. Then
$$
e^{b |\arg f_z|}\in L^1_{loc}\quad {\rm for \; all}\;\;{\rm positive }\;\;   b< \frac{4K}{K^2-1}.
$$

**自包含改写**：If f is K-quasiconformal on a domain Omega in C, then exp(b|arg f_z|) in L^1_loc for all positive b < 4K/(K^2-1); this is optimal since integrability fails for b = 4K/(K^2-1) for the power map f(z) = (z/|z|)|z|^tau with tau = (1/2)(K + 1/K) + (i/2)(K - 1/K).

**判定理由**：Sharp exponential integrability of the argument proved in the paper.

**关联卡**：Special case of Theorem 4.7 with purely imaginary beta; bilipschitz analogue is Theorem 5.4.

### 🔴 `OP-937AED243275` — `solved_in_paper` | MSC 30C62 | 难度 hard

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Theorem 1.2 (Theorem 4.7), Section 1 / Section 4.3
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Suppose  $f$ is a $K$-quasiconformal map on a domain $\Omega\subset\C.$ Then for any exponent $\beta \in \C$ in the critical ellipse
\begin{equation} \label{aito37}
 |\beta| + |\beta -2| <  2\cdot \frac{K+1}{K-1}
 \end{equation}
we have 
\begin{equation*}
\left| f_{z}^\beta \right| \in L^1_{loc}(\Omega).
\end{equation*}

**自包含改写**：If f is K-quasiconformal on a domain Omega in C, then for every complex exponent beta with |beta| + |beta - 2| < 2(K+1)/(K-1) we have |f_z^beta| in L^1_loc(Omega). Sharp: the result fails for beta on or outside the boundary of the critical ellipse (tested with power maps f(z) = (z/|z|)|z|^tau).

**判定理由**：Main integrability theorem proved in the paper, including sharpness.

**关联卡**：Special cases: Corollary 1.3 (exponential integrability of arg f_z for quasiconformal maps) and Theorem 5.4 (bilipschitz case).

### 🔴 `OP-FC9B9895038B` — `solved_in_paper` | MSC 30C62 | 难度 medium

- 论文当时状态：`solved_in_paper` → 当前状态：`unknown`
- 出处：Theorem 5.11, Section 5.4
- 自检：conditions_complete: yes | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: yes

**原文引文**

> Let $s_\gamma \colon \bar{\mathbb{D}} \to \bar{\mathbb{D}}$ be factored as
$s_\gamma = f_N \circ f_{N-1} \circ \ldots f_1$, where each $f_i$ is an $L_0$-bilipschitz map of a closed Jordan domain in $\R^2$, $L_0 >1$. 
Then the  number of factors needed is at least
$ N \ge \left \lceil \frac{|\gamma|}{ L_0-\frac{1}{L_0}} \right \rceil .$

**自包含改写**：If the logarithmic spiral map s_gamma(z) = z|z|^{i gamma} on the closed unit disk is factored as s_gamma = f_N o ... o f_1, where each f_i is an L_0-bilipschitz map of a closed Jordan domain in R^2 with L_0 > 1, then N >= ceil(|gamma|/(L_0 - 1/L_0)). This is optimal: factoring into N iterates of s_{gamma/N} with gamma_0 = gamma/N achieves it. Improves the Freedman-He bound |gamma|/sqrt(L_0^2-1).

**判定理由**：Optimal factoring lower bound proved in the paper using sharp pointwise rotation estimates.

**关联卡**：Partial answer toward the general bilipschitz factoring question (background_open card).

### ⚪ `OP-36A34A056B66` — `future_application` | MSC 30C62 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1 (Introduction), after Theorem 1.5
- 自检：conditions_complete: no | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> It is clear that detailed combinatorial or topological information about specific dynamical systems, combined with the methods of Theorem \ref{holodim}, will improve the bounds above.

**自包含改写**：Not a proposition: an outlook stating that combining combinatorial/topological information from specific complex dynamical systems with the methods of the holomorphic-motion dimension bound could improve the bounds of Theorem on dim(E) <= 1 + alpha - (1/|lambda|) sqrt((1-alpha)^2 + (1-|lambda|^2) alpha^2 gamma^2).

**判定理由**：Application outlook for complex dynamics, not a mathematical proposition posed by this paper.

**关联卡**：Refers to the holomorphic motion dimension bound proved in the paper.

### ⚪ `OP-564E51D1D8E0` — `future_application` | MSC 30C62 | 难度 medium

- 论文当时状态：`not_a_proposition` → 当前状态：`unknown`
- 出处：Section 1 (Introduction)
- 自检：conditions_complete: no | notation_self_contained: yes | parameter_ranges_verbatim: yes | solved_in_this_paper: no

**原文引文**

> This reveals connections with Burkholder functionals and raises new questions regarding quasiconvexity.

**自包含改写**：Not a proposition: a general comment that the weighted analysis reveals new open questions about quasiconvexity of the Burkholder-type functionals introduced in the paper. No specific mathematical statement is formulated.

**判定理由**：Value/direction remark without a formal mathematical proposition.

**关联卡**：Related to the Burkholder quasiconcavity conjecture card.

**存疑**：The 'new questions' are never explicitly formulated in the paper.

