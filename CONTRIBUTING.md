# 协作规范（3 位研究者 + Agent）

## 任务轮换而非固定分工

| 角色 | 职责 | 是否固定给某人 |
| --- | --- | --- |
| 当前执行者 (Driver) | 负责 Issue、分支、实验和交接文档 | 否 |
| 独立审核者 (Reviewer) | 复核科学有效性、代码与复现说明 | 否 |
| 接力研究者 (Next Driver) | 按交接记录续做；可以是第三人 | 否 |

一个 Issue 在任一时点只指定一个 Driver；Reviewer 尽量由未参与该任务的人担任。成员与 Agent 可以轮换角色。涉及主结论的更改应有一位不同成员独立复现。

## GitHub 操作流程

1. 新建 Issue，写明研究问题、所需输入、验收标准和时间/算力预算；指派当前 Driver。
2. 建立 `issue/NN-short-name` 分支，频繁提交可读的小 commit，及时推送，防止 Agent 会话中断时丢失进度。
3. 实验生成独立 run 目录，避免三个 Agent 同时编辑中央 CSV 或同一个 notebook。共享代码变更应尽早开 Draft PR，沟通接口。
4. 每次中断或轮换，更新 `docs/handoffs/issue-NN.md`。PR 模板中链接 Issue、handoff 和 run_id。
5. Reviewer 检查实际命令、物理假设、随机种子、预算公平、结果是否真实和是否引入数据泄漏。建议合并前要求一位其他成员批准。
6. 合并后，若产生了**新的已复现共识**才更新 `docs/STATE.md`；重要不可轻易撤销的决定单独新增 ADR。

## 冲突预防

- 不将整个研究拆成三个永久归属模块；以小 Issue 为单位协作。
- 避免并行编辑同一个实验输出。每次训练都有独一无二的 `run_id`。
- `docs/STATE.md` 只记当前共识；日常实验写运行清单；中断过程写 handoff；决定为何这样做写 ADR。不要三处重复维护完整结果。
- 出现结论冲突时保留各自 run；新建 Issue 复核，不覆盖先前失败记录。
- Agent 没有仓库写权限时：保存 patch/文件包、在 Issue 提供明确变更内容，由有权限的人提交；不要冒充已推送。

## 建议标签

`research-question`, `literature`, `experiment`, `reproduction`, `bug`, `documentation`, `decision-needed`, `blocked`。

## 推荐的初始 Issue

1. 清点已有两份 ZIP：逐一登记脚本、依赖、数据出处、运行命令与现有输出；不修改原档。
2. 精确对角化参照测试：6/8 自旋 TFIM + 局域纵场；验证宇称、能隙、保真度和模型定义。
3. 训练预算/评测接口：统一 `seed / split / gradient_steps / H_evals / time / metrics`。
4. 复现条件 MLP、条件 Transformer、RBM 与对称性投影基准。
5. 主动采样最小实验：均匀采样、对数采样和无 oracle 的自适应采样；先做小规模反例。
