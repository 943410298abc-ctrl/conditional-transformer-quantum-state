# ADR-0001: 按任务接力协作，而不是给三人固定分研究主线

- Date: 2026-10-19
- Status: Accepted as initial workflow; can be revised through a new ADR.

## Context

项目由三名研究者及各自 Agent 参与。人员和模型可能轮换；会话记忆、机器运行环境无法共享或完全可靠，研究目标和实验记录必须留在版本库。

## Decision

采用 Issue 驱动、一任务一分支一 PR、每 Issue 独立 handoff、每实验独立 manifest 的工作流。`docs/STATE.md` 是当前共识入口，不存放逐次训练日志。Reviewer 随任务轮换，原则上不由本任务作者独自批准主结论。

## Consequences

优点：便于任意成员及 Agent 接手、追责与独立复现；减少并行编辑冲突。代价：每项任务需短交接记录，结果归档略有额外工作。若流程过重，通过后续 ADR 简化，而不是绕过必要追溯。
