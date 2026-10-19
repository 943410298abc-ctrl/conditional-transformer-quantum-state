# Round 1 aggregate results

Mean +/- sample SD across **three seeds**; not confidence intervals. Within-seed means/maxima use the fixed parameter grid.

| Architecture | Train mode | Split | Predictor | Mean infidelity | Worst infidelity |
|---|---|---|---|---:|---:|
| mlp | raw | train | direct | 0.157194 +/- 0.00232 | 0.470113 +/- 0.0074 |
| mlp | raw | train | lookup | 0.157194 +/- 0.00232 | 0.470113 +/- 0.0074 |
| mlp | raw | train | even_projection | 0.000439646 +/- 7.66e-05 | 0.00101259 +/- 0.000254 |
| mlp | raw | train | parity_ritz | 0.333435 +/- 2.86e-05 | 1 +/- 0 |
| mlp | raw | train | train_span_ritz | 0.15707 +/- 0.00221 | 0.470179 +/- 0.00698 |
| mlp | raw | interpolation | direct | 0.169839 +/- 0.00547 | 0.422054 +/- 0.012 |
| mlp | raw | interpolation | lookup | 0.152187 +/- 0.00172 | 0.378089 +/- 0.00556 |
| mlp | raw | interpolation | even_projection | 0.00161758 +/- 0.000169 | 0.00294216 +/- 0.000487 |
| mlp | raw | interpolation | parity_ritz | 0.00161758 +/- 0.000169 | 0.00294216 +/- 0.000487 |
| mlp | raw | interpolation | train_span_ritz | 0.114105 +/- 0.00109 | 0.322338 +/- 0.00527 |
| mlp | raw | extrapolation | direct | 0.202674 +/- 0.00188 | 0.490172 +/- 0.00377 |
| mlp | raw | extrapolation | lookup | 0.194129 +/- 0.00286 | 0.475179 +/- 0.00713 |
| mlp | raw | extrapolation | even_projection | 0.00117799 +/- 0.000302 | 0.00280352 +/- 0.000623 |
| mlp | raw | extrapolation | parity_ritz | 0.400357 +/- 0.000199 | 1 +/- 0 |
| mlp | raw | extrapolation | train_span_ritz | 0.219689 +/- 0.00205 | 0.569702 +/- 0.00434 |
| mlp | even | train | direct | 0.000135267 +/- 3.33e-05 | 0.000261865 +/- 0.000107 |
| mlp | even | train | lookup | 0.000135267 +/- 3.33e-05 | 0.000261865 +/- 0.000107 |
| mlp | even | train | even_projection | 0.000135267 +/- 3.33e-05 | 0.000261865 +/- 0.000107 |
| mlp | even | train | parity_ritz | 0.000135267 +/- 3.33e-05 | 0.000261865 +/- 0.000107 |
| mlp | even | train | train_span_ritz | 0.000124134 +/- 3.11e-05 | 0.000237021 +/- 8.77e-05 |
| mlp | even | interpolation | direct | 0.00111446 +/- 0.000426 | 0.00221293 +/- 0.000685 |
| mlp | even | interpolation | lookup | 0.0029903 +/- 0.000101 | 0.00472246 +/- 0.000233 |
| mlp | even | interpolation | even_projection | 0.00111446 +/- 0.000426 | 0.00221293 +/- 0.000685 |
| mlp | even | interpolation | parity_ritz | 0.00111446 +/- 0.000426 | 0.00221293 +/- 0.000685 |
| mlp | even | interpolation | train_span_ritz | 0.000745103 +/- 7.55e-05 | 0.00161701 +/- 0.000168 |
| mlp | even | extrapolation | direct | 0.00183545 +/- 0.00121 | 0.00445019 +/- 0.00335 |
| mlp | even | extrapolation | lookup | 0.00678478 +/- 4.66e-05 | 0.0146498 +/- 1.83e-05 |
| mlp | even | extrapolation | even_projection | 0.00183545 +/- 0.00121 | 0.00445019 +/- 0.00335 |
| mlp | even | extrapolation | parity_ritz | 0.00183545 +/- 0.00121 | 0.00445019 +/- 0.00335 |
| mlp | even | extrapolation | train_span_ritz | 0.000583719 +/- 1.01e-05 | 0.00109458 +/- 5.84e-05 |
| transformer | raw | train | direct | 0.144237 +/- 0.0558 | 0.40676 +/- 0.141 |
| transformer | raw | train | lookup | 0.144237 +/- 0.0558 | 0.40676 +/- 0.141 |
| transformer | raw | train | even_projection | 0.000851287 +/- 0.00088 | 0.0018864 +/- 0.0022 |
| transformer | raw | train | parity_ritz | 0.111903 +/- 0.193 | 0.333745 +/- 0.577 |
| transformer | raw | train | train_span_ritz | 0.143639 +/- 0.0563 | 0.405268 +/- 0.142 |
| transformer | raw | interpolation | direct | 0.146919 +/- 0.0861 | 0.350806 +/- 0.176 |
| transformer | raw | interpolation | lookup | 0.146491 +/- 0.0647 | 0.337027 +/- 0.127 |
| transformer | raw | interpolation | even_projection | 0.00269119 +/- 0.000967 | 0.0073059 +/- 0.00305 |
| transformer | raw | interpolation | parity_ritz | 0.00269119 +/- 0.000967 | 0.0073059 +/- 0.00305 |
| transformer | raw | interpolation | train_span_ritz | 0.13067 +/- 0.0758 | 0.316799 +/- 0.142 |
| transformer | raw | extrapolation | direct | 0.17518 +/- 0.0446 | 0.440854 +/- 0.098 |
| transformer | raw | extrapolation | lookup | 0.169694 +/- 0.0571 | 0.411612 +/- 0.14 |
| transformer | raw | extrapolation | even_projection | 0.00158093 +/- 0.000846 | 0.0038051 +/- 0.00055 |
| transformer | raw | extrapolation | parity_ritz | 0.267624 +/- 0.231 | 0.668055 +/- 0.575 |
| transformer | raw | extrapolation | train_span_ritz | 0.184175 +/- 0.0574 | 0.469792 +/- 0.139 |
| transformer | even | train | direct | 8.23961e-05 +/- 9.31e-05 | 0.000144978 +/- 0.000182 |
| transformer | even | train | lookup | 8.23961e-05 +/- 9.31e-05 | 0.000144978 +/- 0.000182 |
| transformer | even | train | even_projection | 8.23961e-05 +/- 9.31e-05 | 0.000144978 +/- 0.000182 |
| transformer | even | train | parity_ritz | 8.23961e-05 +/- 9.31e-05 | 0.000144978 +/- 0.000182 |
| transformer | even | train | train_span_ritz | 6.35396e-05 +/- 6.23e-05 | 0.000119009 +/- 0.000137 |
| transformer | even | interpolation | direct | 0.00202202 +/- 0.00136 | 0.00481468 +/- 0.00328 |
| transformer | even | interpolation | lookup | 0.00277841 +/- 0.000312 | 0.00441094 +/- 0.000866 |
| transformer | even | interpolation | even_projection | 0.00202202 +/- 0.00136 | 0.00481468 +/- 0.00328 |
| transformer | even | interpolation | parity_ritz | 0.00202202 +/- 0.00136 | 0.00481468 +/- 0.00328 |
| transformer | even | interpolation | train_span_ritz | 0.000726697 +/- 0.000243 | 0.00160017 +/- 0.000534 |
| transformer | even | extrapolation | direct | 0.0012401 +/- 0.000327 | 0.00382068 +/- 0.000589 |
| transformer | even | extrapolation | lookup | 0.00658159 +/- 5e-05 | 0.0140849 +/- 0.000586 |
| transformer | even | extrapolation | even_projection | 0.0012401 +/- 0.000327 | 0.00382068 +/- 0.000589 |
| transformer | even | extrapolation | parity_ritz | 0.0012401 +/- 0.000327 | 0.00382068 +/- 0.000589 |
| transformer | even | extrapolation | train_span_ritz | 0.000522873 +/- 9.26e-05 | 0.00116121 +/- 0.000292 |

## Actual budgets

| Model | Mode | Seed | Selected step | Full steps | Training seconds | Total seconds |
|---|---|---:|---:|---:|---:|---:|
| mlp | raw | 17 | 600 | 600 | 2.69 | 2.71 |
| mlp | raw | 29 | 600 | 600 | 0.91 | 0.92 |
| mlp | raw | 43 | 600 | 600 | 0.82 | 0.84 |
| mlp | even | 17 | 600 | 600 | 0.92 | 0.93 |
| mlp | even | 29 | 600 | 600 | 0.91 | 0.93 |
| mlp | even | 43 | 600 | 600 | 0.97 | 0.99 |
| transformer | raw | 17 | 300 | 600 | 2.87 | 2.89 |
| transformer | raw | 29 | 300 | 600 | 2.75 | 2.78 |
| transformer | raw | 43 | 350 | 600 | 2.81 | 2.83 |
| transformer | even | 17 | 550 | 600 | 2.91 | 2.93 |
| transformer | even | 29 | 600 | 600 | 2.95 | 2.98 |
| transformer | even | 43 | 600 | 600 | 2.86 | 2.89 |
