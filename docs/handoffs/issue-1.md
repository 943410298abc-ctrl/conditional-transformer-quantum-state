# Issue #1 — 第12题基准、近简并机制与选题复核

- Updated: 2026-10-19 (Asia/Shanghai)
- Driver: Codex，受 Bian-M-X 授权研究和推送；没有代替其他成员署名或独立评审。
- Branch: `issue/1-topic12-audit`
- Issue: https://github.com/Bian-M-X/conditional-transformer-quantum-state/issues/1
- Status: needs-review
- Core implementation commit: `3bddd74`; primary training code commit: `3ef2378429d628772fd5a7935d1b1112122c9da7`
- 正式研究结论仍未提升至 STATE confirmed。

## 目标和验收

建立满足手册第12题的可审计最小训练/泛化对照，确认训练失败与外推失败的区别；梳理通向ICLR贡献的剩余门槛。12个预指定任务全部保留，每组600步，2架构×2训练方式×3种子；不把ED结果用于训练或选择。

## 已完成（observed / derived）

- 读取手册第1–3、26–27页；目视核对第26–27页；原PDF保持本地，哈希见 `docs/course_requirements.md`。
- 两份ZIP逐项哈希清点；抽查旧指标，但**没有声称重跑历史二维训练**。见 `docs/audit/`。
- 实现 `src/ctqs/{physics,models}.py`；模型使用显式condition token、右移、mask、零dropout；增加同源lookup、偶宇称、两种Ritz控制。
- 所有主运行索引见 `experiments/round1_index.json`（12 runs, 900 rows）；代码commit、命令、seeds、选中步数、实际成本见每个manifest。
- 谱任务：`20261019T134113946160Z-spectral-mechanism-s0`，N=4/6/8的全空间/偶扇区间隙。
- 同机重跑：`20261019T135122926770Z-replay-transformer-even-s17`，与主任务seed17的75条指标、12条训练记录精确一致。它不增加统计seed数，也不算跨成员复现。
- `docs/round1_report.md/.pdf` 为6页中文初筛报告；`docs/results/round1/` 为完整CSV/JSON/表格/图片；图由脚本生成。
- 10项单元测试通过（无skip）；报告所有6页渲染目检通过。额外物理结果检查脚本 `scripts/verify_round1.py`。
- 文献排查新增主动EC、FNEH近邻工作；理论记录能量-保真度界、Ritz错误扇区条件、残差反例和P参数协变。

## 核心结果与不支持的结论

- 普通MLP在训练h=0.2的F=0.5214–0.5350；偶宇称训练F>=0.999675。说明当前错误不能全归为未见参数泛化。
- 偶宇称Transformer外推平均失真：direct 0.001240，lookup 0.006582；三个配对初值都改善。内插有一个初值direct更差，不支持全面优势。
- 普通MLP的parity-Ritz在h=0.2三个种子全部选错扇区，能量降低不保证保真度。
- 不支持新采样算法、完整TQS复现、架构效率排名、大系统规模结论或ICLR投稿就绪。

## 实际命令和环境

工作目录为仓库根；主要命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/run_round1.py
.\.venv\Scripts\python.exe scripts/run_round1.py --arch transformer --mode even --seed 17 --tag replay
python scripts/check_spectral_mechanism.py
.\.venv\Scripts\python.exe scripts/summarize_round1.py
.\.venv\Scripts\python.exe scripts/verify_round1.py
python scripts/validate_workspace.py
```

Python3.13.9、torch2.14.1+cpu、numpy2.3.5、scipy1.16.3；所有训练CPU float64、PyTorch单线程。主要12组记录的run段总耗时24.625秒，不含安装/测试/工具启动。没有使用GPU或付费服务。PDF重建使用Codex自带Python/reportlab和Windows宋体，脚本支持另传CJK字体。

## 失败/阻塞与解决方式

- GitHub连接器读权限可用，但创建Issue返回403；本机已认证gh成功创建Issue。sandbox外网DNS失败，授权升级后git push成功。没有修改代理。
- 初建venv的ensurepip被sandbox临时目录权限阻止，升级权限后成功；第一次全测试因Anaconda MKL与PyTorch OpenMP冲突退出。局部安装标准NumPy/SciPy wheels后10测试全部通过，未启用KMP_DUPLICATE_LIB_OK。
- PyPI主下载停滞，官方PyTorch索引缺SciPy；随后同版本清华镜像下载成功。依赖仅写项目venv。
- 基础测试临时目录受sandbox限制时，将该命令的TEMP/TMP设为本仓库tmp后通过。
- 批量训练工具会话完成所有输出后仍显示running；额外系统进程检查未发现run_round1.py在运行，独立重跑命令正常exit0。以独立manifest/指标和重跑核查作证据，不虚构批量工具返回的exit code。

## 下一位成员：先做这一条

在新环境按README安装依赖，并确保tracked文件已提交，然后：

```bash
python scripts/run_round1.py --arch transformer --mode even --seed 17 --tag independent
```

与主运行 `20261019T135010710747Z-round1-transformer-even-s17` 比较所有75行指标和训练轨迹。
同环境期望精确一致；跨平台允许浮点差异但应先报告最大差值，建议绝对容差1e-8作为排查阈值，不能据此直接宣布泛化结论复现。
不要覆盖首轮index，把新run和比较结果独立提交。完成后再审阅PDF的结论是否被数据支持。

## 下一轮研究（planned）

先补种子和优化预算曲线，随后预先定义新的lambda双侧任务并加入P协变对照。
在匹配总成本下比较固定uniform/log/random、残差greedy、EC/FNEH风格和继续训练基准。
核心待检验问题是新增参数点与已有点状态修复之间的资源选择；仍需新颖性核查。
旧测试点已经打开，不可继续称盲测。尚未实现主动采样，也未训练跨物理族模型。

## 人类协作与风险

成员实际分工、文献阅读、人工核查和答辩尚需本人补充；本轮不代填。新方法贡献目前未确立。
主要风险为训练失败混入泛化、参数协变捷径、谱oracle泄漏、种子数少、未收敛、全枚举不具规模性与基准成本不公平。
每次继续工作请保留这些限制；不得因PDF排版完整而称论文完成。
