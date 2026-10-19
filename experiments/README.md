# Experiment Records

**每一个物理/机器学习运行拥有唯一目录** `experiments/runs/<run_id>/`；不要用一个共享 results.csv 存所有成员正在进行的运行，以免并行修改冲突。

创建记录（不执行实验）：

```bash
python scripts/new_run.py --slug tfim-uniform-baseline --owner YOUR_GITHUB_ID --issue 1 --seed 0
```

在生成的 `manifest.json` 中填写：

- `status`: `planned -> running -> completed | failed`；未实际运行不可写 `completed`。
- `command`: 可从仓库根目录重复的运行命令。
- `git_commit`: 对应代码的 commit；如果运行前尚未提交，完成时更新成实际 commit。
- `model`, `hamiltonian`, `parameter_split`, `budget`, `metrics`, `artifacts`：凡无法记录的字段写 `null`，**禁止编造**。
- `oracle_access`: 若训练、选择训练点或后处理使用精确对角化真值，必须写明。

完整运行记录、运行脚本和小体积的聚合数据可以提交 Git；大型 checkpoint、原始样本、缓存保留在外部存储并登记路径或校验和。待发表的重要结果必须能够由其他成员独立重跑。
