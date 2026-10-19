# Conditional Transformer Quantum State (CTQS)

**Research status: exploratory / early-stage validation.** 研究目标是考察**近简并区域中条件神经网络量子态的可靠泛化**，重点评估有限训练预算下的参数采样策略。当前结果是预研究，不代表已有新的投稿级算法。

**拟定题目**：近简并系统中条件神经网络量子态的可靠泛化与计算预算感知的自适应参数采样  
**English**: Reliable Generalization and Budget-Aware Adaptive Parameter Sampling for Conditional Neural Quantum States near Quasi-Degeneracies

## 开始协作（3 名研究者 + 各自 Agent；任务轮换）

不按成员永久划分研究主线；按 **GitHub Issue → 独立分支 → 实验记录 → PR → 合并** 轮换接力。每个 Issue 有一个当前负责人，但后续可交给任何成员及其 Agent。Agent 的对话历史不视为项目记录。

1. **进入工作前**依次阅读 [`AGENTS.md`](AGENTS.md)、[`docs/STATE.md`](docs/STATE.md)、[`docs/PROTOCOL.md`](docs/PROTOCOL.md)，然后阅读当前 Issue、对应交接记录及近期提交。
2. 从 GitHub Issues 认领一项任务；没有 Issue 先建 Issue。每位成员同时推进不超过一个需要合并的主要任务，避免竞争修改。
3. 从 `main` 新建 `issue/<编号>-<简述>` 分支，**禁止 Agent 直接推送 `main`**。
4. 每次正式实验创建一个**独立的** `experiments/runs/<run_id>/manifest.json`，记录配置、随机种子、commit、运行命令与预算。大文件及敏感文件不提交 Git。
5. 完成阶段工作时，把状态写到 `docs/handoffs/issue-<编号>.md`；在 PR 中说明做了什么、没做什么、怎么验证、下一步怎么接续。
6. 重要研究结论先经过独立复现，再写入 `docs/STATE.md`；设计决策写入新的 `docs/decisions/NNNN-*.md`。PR 经另一位成员审阅后合并。

**接力最短路径：** `AGENTS.md` → `docs/STATE.md` → 任务 Issue → `docs/handoffs/issue-N.md` → 指定实验 manifest → `git status` / `git log`。不要仅靠聊天记录交接。

## 仓库目录

```text
AGENTS.md                         # 所有 Agent 的共同工作约束与接力流程
README.md                         # 总入口
CONTRIBUTING.md                   # 人员协作、分支与评审规则
docs/
  STATE.md                        # 项目当前共识；只维护已核实信息
  PROTOCOL.md                     # 物理模型、指标、基准和公平预算
  RESEARCH_LOG.md                 # 重要阶段摘要（不记流水账）
  decisions/0001-collaboration.md # 不可变的决策记录，后续新增文件
  handoffs/_TEMPLATE.md          # Issue 对应的接力记录模板
experiments/
  README.md                       # 实验记录标准
  runs/<run_id>/manifest.json     # 每次运行的独立记录
src/                              # 后续模型、训练、评测模块
scripts/new_run.py                # 为一次实验创建记录
scripts/validate_workspace.py     # 校验仓库与实验记录结构
tests/                             # 不依赖 ML 框架的基础检查
.github/ISSUE_TEMPLATE/           # 任务模板
.github/PULL_REQUEST_TEMPLATE.md  # 评审模板
.github/workflows/                 # 轻量自动化检查
```

## 已有材料

此前上传的 `研究主题与预试验报告.docx`、`预实验1.zip`、`预实验2.zip` 暂保留于仓库根目录，**不会自动宣称其内容可复现**。第一项工程任务应清点两份 ZIP，提取源代码、依赖与原始指标，并建立 `experiments/runs/` 中的追溯链接。未经复核不得把 ZIP 内结果登记为 confirmed。

## 本地快速检查

需要 Python 3.10+，不需要先安装 PyTorch：

```bash
python scripts/validate_workspace.py
python -m unittest discover -s tests -v
python scripts/new_run.py --slug tfim-baseline --owner YOUR_GITHUB_ID --issue 1 --seed 0
```

最后一条只**创建实验记录，不会运行模型**。把 `--issue 1` 替换为真实 Issue 编号。

论文进度与待解决问题见 [`docs/STATE.md`](docs/STATE.md)。外部数据、权重、大型中间文件请使用受控存储，提交校验和、获取步骤与必要的聚合统计即可。
