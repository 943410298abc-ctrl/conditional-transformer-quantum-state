# 文献边界与新颖性排查（2026-10-19）

本轮为有边界的定向检索，不是系统综述或首创性证明。正文只使用可打开的一手来源。
检索关键词包括 conditional transformer quantum states、neural quantum states active learning Hamiltonian parameters、eigenvector continuation active learning。
检索发现会影响研究选择，但不会自动证明尚有可发表空白。

| 文献/一手入口 | 本轮实际阅读范围 | 对本项目的约束 |
|---|---|---|
| Zhang & Di Ventra, [PRB 107, 075147 (2023), arXiv v4](https://arxiv.org/html/2208.01758v4) | 方法 II、图1说明、TFIM III.1、附录 D/G.2 | 条件自回归、跨参数预测及错误临界行为均已有；原文 TFIM 使用对称性，不能将无对称小网络失败归为完整 TQS 失败。 |
| Rende et al., [Nature Communications 16, 7213 (2025)](https://www.nature.com/articles/s41467-025-62098-x) | 公开正文/摘要，未独立复现实验 | 多哈密顿量 FNQS、未见耦合和 fidelity susceptibility 已有；统一网络或参数导数本身不新。 |
| Chen et al., [NeurIPS 2022](https://papers.neurips.cc/paper_files/paper/2022/hash/3173c427cb4ed2d5eaab029c17f221ae-Abstract-Conference.html) | 官方论文页和摘要 | 对称投影、变分子空间与 Lanczos 改善已有；本轮 Ritz 是强基准。 |
| Frame et al., [Eigenvector continuation with subspace learning](https://arxiv.org/abs/1711.07090) | 原作者 arXiv 元数据/摘要 | 参数态张成低维空间再变分对角化已有；本轮 train-span 不是新方法。 |
| Sarkar & Lee, [PR Research 4, 023214 (2022)](https://arxiv.org/html/2107.13449v2) | 引言、约束残差估计、主动选点方法 | 主动误差驱动 EC 已有。其训练点解精确/忠实、局部误差估计假设是与有限预算变分 NQS 比较时必须明确的区别。 |
| Zhang, Jiang & Luo, [Foundation Neural Effective Hamiltonian, arXiv:2608.14208v1](https://arxiv.org/html/2608.14208v1) | 引言、式1–6、图1–2说明 | 已将 FNQS 不同参数态张成子空间并修正相边界。属于预印本；不能声称该组合是本项目首创，也不能用本轮 dense Ritz 冒充其完整采样实现。 |
| [Symmetry Constraints Regularize Neural Quantum State Learning, arXiv:2608.08798](https://arxiv.org/abs/2608.08798) | 元数据/摘要核验，全文细节待读 | 对称性改善训练几何已有近期工作，当前不就其具体定理作结论。 |
| [Topology Obstructs Pure Foundation Neural Quantum States, arXiv:2609.07591](https://arxiv.org/abs/2609.07591) | 元数据/摘要核验，全文细节待读 | 拓扑障碍不能与本项目有限尺寸、正实振幅、近简并机制混为一谈。 |

## 由检索得到的判断（inference）

“做一个条件 Transformer”“使用对称投影”“用训练态做 Ritz”“依赖残差主动选点”均不足以单独构成新颖性叙事。
仍可研究、但**未证实新颖**的问题是：训练点解本身不精确时，残差/后处理收益能否辨别“参数覆盖不足”和“错误本征态分支”，并在相同总预算下选择新增参数点或继续优化已有点。

该问题的危险反例是方差为零的错误本征态：把残差当采集分数可能完全看不到它。
下一轮应比较固定网格、随机、对数/混合网格、残差贪心、EC/FNEH 风格方法，以及已知参数协变对照。
任何候选必须计入查询和再训练成本；若只依靠 ED gap 才奏效，只能成为 oracle 上限。

## ICLR 的工作标准

[ICLR 2026 官方 Reviewer Guide](https://iclr.cc/Conferences/2026/ReviewerGuide) 强调具体问题、文献定位、技术正确性、实验严谨性、可复现性及贡献价值，不要求所有论文都创 SOTA。
这里把它作为研究质量参照，不声称目标投稿年份已确定或格式已经合规。具体投稿时应再核对当届作者指南。
当前不足：系统/种子规模小，缺跨哈密顿量训练、采样估计与总成本匹配，未证明新算法或新的普遍结论，也未有独立人员复现。

## 学习与核查问题

1. 对照 TQS 图1/式1：为什么右移与因果掩码都需要？condition token 可以被所有自旋位置读取吗？
2. 原文图4/G.2 的相变误判与本轮训练点保真度失败是同一种问题吗？哪些证据能区分？
3. EC 的训练基底、FNEH 的神经基底、纯条件推断分别查询了哪些信息、支付了哪些成本？
4. 残差误差估计何时依赖谱分离？“找到一个本征态”和“找到基态”差在哪里？

上述是实际检索/阅读记录，不代表三位人类成员已经阅读或理解；答辩前需各自完成并补充自己的解释。
