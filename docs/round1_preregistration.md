# Round 1: frozen screening protocol

Status: planned before new training; Issue #1; 2026-10-19 (Asia/Shanghai).
This is a repository timestamped protocol, not an external preregistration.

## Questions and alternative explanations

1. Does direct conditional inference outperform interpolation of the **same learned training states** on unseen h?
2. Is low-field error primarily a support-distance effect, or can optimization into an incorrect parity mixture already cause training-point failure?
3. Does enforcing the known even sector during training remove this failure at the same update/H-action budget?

These are course-level mechanism questions. No proposed new algorithm or guaranteed publication claim.
Existing archived results informed the choice of stress regime. New runs are a prespecified screening, not a historically blind discovery test.

## Fixed configuration

`experiments/configs/round1.json` is authoritative: N=6, open TFIM, lambda=0,
train h={0.2,0.8,1.4}; validation={0.5,1.1}; five interpolation and five extrapolation points.
Both architectures, raw/even training, seeds 17/29/43: 12 jobs, 600 updates/job.
Adam lr=0.005, float64 CPU with one PyTorch thread. Dropout zero everywhere.
Checkpoint every 50 updates, select minimum mean **validation variational energy**;
never inspect exact validation/test labels to select epochs, architecture or hyperparameters.
Each job runs the full fixed budget, even if the selected checkpoint is earlier.
This is a lower-compute screening, not convergence or wall-time-matched architecture competition.

## Baselines and accounting

- Direct output; learned positive-amplitude interpolation, clamped beyond train support.
- Even projection (only valid because this experiment has lambda=0).
- Two-vector parity Rayleigh-Ritz (may select wrong sector if sector approximation error exceeds the true gap).
- Learned training-state span Rayleigh-Ritz (eigenvector-continuation-style control).
- ED only for scoring, no exact states in the interpolation/subspace tables.

Report per-spin energy error, fidelity, connected endpoint correlation error, Z1 error,
train versus held-out performance, each seed and mean/sample SD across seeds.
Parameter points are correlated; do not treat 3x10 points as 30 independent replications.
Ritz methods require extra target-H actions. Count those separately; do not call them free zero-shot inference.
No hypothesis test or CI justified by three seeds. Show all failures and no post-test retuning in this round.

## Numerical and stopping gates

N=4/6 normalization/causality tests; independent Kronecker H; parity covariance;
degenerate ground-space metric; Ritz rank deficiency and variational bound; gradient finite difference.
Per-job hard timeout 600 seconds; combined training cap 30 minutes. Failed jobs retained.
If trained states fail, report optimization/task mismatch before interpreting generalization.
No adaptive sampling performance claims in this round: establish trustworthy comparator first.

## Separate derived-mechanism check

Sweep ED at N=4/6/8 and h=0.2/0.35/0.8. Compare the full gap to the even-sector gap.
Use exact low eigenstates **explicitly as oracle counterexamples**, never in ML training.
Check energy/fidelity inequalities and a two-level residual false-negative example.
These are standard spectral arguments, not claims of new theorems.
