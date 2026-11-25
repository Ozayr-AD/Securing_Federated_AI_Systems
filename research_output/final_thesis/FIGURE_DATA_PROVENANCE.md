# Figure and Data Provenance

Generated when the thesis was built, from the figure registries written by the figure scripts, the data manifest `data/MANIFEST.csv` and the thesis text. Every data file below is a byte-identical copy of the recorded experiment output named next to it; the SHA-256 of each copy was verified against its source when it was collected. The branch named next to each source is the development branch that produced it; all of them are merged in this repository at the paths given. Charts are rendered with Matplotlib at 300 dpi (PNG) and as vector PDF; diagrams are drawn by `figures/scripts/make_diagrams.py` from the implemented design and contain no measured data.

## Figures

### Figure 2.1: `fl_overview`

- Caption: Federated averaging with a coordinating server. The server sends the global model to a cohort, each client trains locally, and the server averages the returned models weighted by sample counts.
- Files: `figures/png/fl_overview.png`, `figures/pdf/fl_overview.pdf`
- Kind: diagram; script: `figures/scripts/make_diagrams.py`
- Sources:
  - `conceptual; FedAvg as defined by McMahan et al. (2017)`
- Transformation: none

### Figure 3.1: `system_architecture`

- Caption: Implemented architecture. All components ran on one host in the evaluation.
- Files: `figures/png/system_architecture.png`, `figures/pdf/system_architecture.pdf`
- Kind: diagram; script: `figures/scripts/make_diagrams.py`
- Sources:
  - `src/fl_security/federated/flower_simulation.py`
  - `src/fl_security/mtd/controller.py`
  - `src/fl_security/smpc/{robust.py, mp_spdz.py, mp_spdz_party_service.py}`
  - `research_output/completion/FINAL_ARCHITECTURE.md`
- Transformation: none

### Figure 3.2: `round_sequence`

- Caption: Sequence of one robust secure round.
- Files: `figures/png/round_sequence.png`, `figures/pdf/round_sequence.pdf`
- Kind: diagram; script: `figures/scripts/make_diagrams.py`
- Sources:
  - `src/fl_security/federated/flower_simulation.py`
  - `src/fl_security/smpc/mp_spdz.py`
  - `research_output/completion/FINAL_ARCHITECTURE.md §2`
- Transformation: none

### Figure 3.3: `inmpc_defence`

- Caption: The robust aggregation inside SPDZ2k and the coordinator's output check.
- Files: `figures/png/inmpc_defence.png`, `figures/pdf/inmpc_defence.pdf`
- Kind: diagram; script: `figures/scripts/make_diagrams.py`
- Sources:
  - `src/fl_security/smpc/programs/spdz2k_robust_aggregate.mpc`
  - `src/fl_security/smpc/robust.py`
  - `docs/secure_robust_aggregation.md §3-5`
- Transformation: none

### Figure 3.4: `mtd_workflow`

- Caption: Secret cohort selection and the schedule-aware adversary.
- Files: `figures/png/mtd_workflow.png`, `figures/pdf/mtd_workflow.pdf`
- Kind: diagram; script: `figures/scripts/make_diagrams.py`
- Sources:
  - `src/fl_security/mtd/controller.py`
  - `src/fl_security/mtd/randomness.py`
  - `src/fl_security/mtd/exposure.py`
  - `docs/mtd_scheduling.md`
- Transformation: none

### Figure 3.5: `direction_screen`

- Caption: The moving-target direction screen.
- Files: `figures/png/direction_screen.png`, `figures/pdf/direction_screen.pdf`
- Kind: diagram; script: `figures/scripts/make_diagrams.py`
- Sources:
  - `src/fl_security/smpc/robust.py (direction_key, direction_indices, direction_screen)`
  - `src/fl_security/smpc/programs/spdz2k_robust_aggregate.mpc`
  - `src/fl_security/federated/flower_simulation.py`
- Transformation: none

### Figure 5.1: `party_service`

- Caption: Processing of one round inside an aggregation-party service.
- Files: `figures/png/party_service.png`, `figures/pdf/party_service.pdf`
- Kind: diagram; script: `figures/scripts/make_diagrams.py`
- Sources:
  - `src/fl_security/smpc/mp_spdz_party_service.py`
  - `docs/threat-model.md (failure behaviour)`
- Transformation: none

### Figure 5.2: `experiment_pipeline`

- Caption: Experiment orchestration and evidence pipeline.
- Files: `figures/png/experiment_pipeline.png`, `figures/pdf/experiment_pipeline.pdf`
- Kind: diagram; script: `figures/scripts/make_diagrams.py`
- Sources:
  - `src/fl_security/experiments/{grid.py, suite.py, analysis.py, report.py}`
  - `run_*.py`
  - `analyze_suite.py`
- Transformation: none

### Figure 6.1: `sum_only_correction`

- Caption: Sum-only SPDZ2k against FedAvg before and after the scale correction. (a) Accuracy of one seed-matched triple under scaled replacement. (b) Largest per-round accuracy difference to FedAvg for each of the 18 `smpc_only` runs.
- Files: `figures/png/sum_only_correction.png`, `figures/pdf/sum_only_correction.pdf`
- Kind: chart; script: `figures/scripts/make_charts.py`
- Sources:
  - `data/sum_only/scaled_replacement_baseline_s102_results.csv` (sha256 `ba7001cc80f8b5ba…`; from `research/spdz2k-secure-robust-aggregation`: `research_output/completion/experiments/runs/e1/e1__baseline__scaled_replacement__s102/e1__baseline__scaled_replacement__s102_results.csv`)
  - `data/sum_only/scaled_replacement_smpc_only_1e6_s102_results.csv` (sha256 `5202e46be7ddb8b2…`; from `research/spdz2k-secure-robust-aggregation`: `research_output/completion/experiments/runs/e1/e1__smpc_only__scaled_replacement__s102/e1__smpc_only__scaled_replacement__s102_results.csv`)
  - `data/sum_only/scaled_replacement_smpc_only_2p40_s102_results.csv` (sha256 `68802558c00635ca…`; from `research/sum-only-pow2-scale-fix`: `research_output/completion/experiments_pow2/runs/e1/e1__smpc_only__scaled_replacement__s102/e1__smpc_only__scaled_replacement__s102_results.csv`)
  - `data/sum_only/pow2_vs_fedavg.csv` (sha256 `22a24ed9de9ab31b…`; from `research/sum-only-pow2-scale-fix`: `research_output/completion/experiments_pow2/pow2_vs_fedavg.csv`)
- Transformation: global_accuracy per round as recorded; max_abs_accuracy_difference per run (pow2_vs_fedavg.py)

### Figure 6.2: `e1_backdoor_rounds`

- Caption: E1 under the boosted backdoor: clean accuracy (a) and attack success rate (b) per round; means over three seeds with 95% intervals.
- Files: `figures/png/e1_backdoor_rounds.png`, `figures/pdf/e1_backdoor_rounds.pdf`
- Kind: chart; script: `figures/scripts/make_charts.py`
- Sources:
  - `data/core/accuracy_over_rounds.csv` (sha256 `0282c83fb01fe251…`; from `research/spdz2k-secure-robust-aggregation`: `research_output/completion/experiments/summaries/accuracy_over_rounds.csv`)
- Transformation: rows study=e1, attack=backdoor, metric in {global_accuracy, backdoor_asr}, rounds 1-10; mean and ci95 columns plotted as recorded (CI clipped to [0,1])

### Figure 6.3: `backdoor_asr_by_defence`

- Caption: Final-round backdoor success per seed (dots) and mean (ticks): (a) boosted backdoor, (b) adaptive backdoor at 0.95 × the published threshold. The dotted line is a clean model's natural trigger response.
- Files: `figures/png/backdoor_asr_by_defence.png`, `figures/pdf/backdoor_asr_by_defence.pdf`
- Kind: chart; script: `figures/scripts/make_charts.py`
- Sources:
  - `data/core/all_rounds.csv` (sha256 `e326f45f0382f043…`; from `research/spdz2k-secure-robust-aggregation`: `research_output/completion/experiments/metrics/all_rounds.csv`)
- Transformation: per run: backdoor_asr of the last completed round; studies e1/e1x (attack backdoor) and e2 (adaptive_backdoor); reference = mean final ASR of e1 baseline without attack

### Figure 6.4: `e3mc_exposure`

- Caption: Compromise hit rate per schedule and adversary (E3-MC; 95% intervals over 200 trials; dotted line: random baseline K/N).
- Files: `figures/png/e3mc_exposure.png`, `figures/pdf/e3mc_exposure.pdf`
- Kind: chart; script: `figures/scripts/make_charts.py`
- Sources:
  - `data/mtd_exposure/exposure_summary_R10.csv` (sha256 `ad4f5cf92f61ee52…`; from `research/spdz2k-secure-robust-aggregation`: `research_output/completion/experiments/mtd_exposure/exposure_summary_R10.csv`)
- Transformation: rows metric=compromise_hit_rate, budgets 2 and 3; mean and ci95 columns as recorded

### Figure 6.5: `pilot_sign_agreement`

- Caption: Sign agreement with the majority of the other cohort members on a random 25% subset, for cohorts with exactly one attacker (pilot on 175 recorded runs).
- Files: `figures/png/pilot_sign_agreement.png`, `figures/pdf/pilot_sign_agreement.pdf`
- Kind: chart; script: `figures/scripts/make_charts.py`
- Sources:
  - `data/mtd_defence/pilot_scores.csv` (sha256 `b5f35133803735c2…`; from `research/mtd-direction-screen`: `research_output/mtd_defence/pilot/pilot_scores.csv`)
- Transformation: rows attackers_in_cohort = 1; column sign_agree_0.25_single split by the malicious flag; AUC by pairwise comparison (ties 0.5)

### Figure 6.6: `p3_paired`

- Caption: P3: final-round ASR per seed under four conditions with paired secrets; grey lines connect one seed, black ticks are means.
- Files: `figures/png/p3_paired.png`, `figures/pdf/p3_paired.pdf`
- Kind: chart; script: `figures/scripts/make_charts.py`
- Sources:
  - `data/mtd_defence/p3_runs.csv` (sha256 `e772d59eca307c47…`; from `research/mtd-direction-screen`: `research_output/mtd_defence/experiments/p3_runs.csv`)
- Transformation: final-round ASR per run as recorded; pivot by seed and condition

### Figure 6.7: `f1_spdz2k_framework`

- Caption: F1, the final framework inside SPDZ2k: final-round ASR (a) and clean accuracy (b) per seed.
- Files: `figures/png/f1_spdz2k_framework.png`, `figures/pdf/f1_spdz2k_framework.pdf`
- Kind: chart; script: `figures/scripts/make_charts.py`
- Sources:
  - `data/mtd_defence/f1_runs.csv` (sha256 `8949d6aa95f46045…`; from `research/mtd-direction-screen`: `research_output/mtd_defence/experiments/f1_runs.csv`)
- Transformation: final-round ASR and last-three-round accuracy per run as recorded

### Figure 6.8: `benchmark_scaling`

- Caption: SPDZ2k protocol time (a) and party traffic (b) per round against model size (logarithmic axes).
- Files: `figures/png/benchmark_scaling.png`, `figures/pdf/benchmark_scaling.pdf`
- Kind: chart; script: `figures/scripts/make_charts.py`
- Sources:
  - `data/benchmarks/benchmark_results.csv` (sha256 `a10354f6e8e9e60b…`; from `research/spdz2k-secure-robust-aggregation`: `research_output/completion/benchmarks/benchmark_results.csv`)
- Transformation: rows parties=3, mode=clip_screen, threshold=adaptive (the sum-only rows carry the same label columns); completed rows: protocol_seconds_max and global_data_sent_mb/1000; failed row marked at the timeout

### Figure 6.9: `e6_leakage`

- Caption: Share of the target client's images recovered near-exactly (SSIM ≥ 0.9) through a fully connected first layer, from its own update and from the SPDZ2k aggregate of four clients.
- Files: `figures/png/e6_leakage.png`, `figures/pdf/e6_leakage.pdf`
- Kind: chart; script: `figures/scripts/make_charts.py`
- Sources:
  - `data/leakage/leakage_raw.csv` (sha256 `c957f6028c1dfc2d…`; from `research/gradient-inversion-leakage`: `research_output/completion/experiments/leakage/evaluation/leakage_raw.csv`)
- Transformation: rows attack=fc_input; share of image records with ssim >= 0.9 per (model_state, view, batch_size)

### Figure 6.10: `attack_defence_layers`

- Caption: Attack classes and the framework's layers, as measured in this thesis (experiment identifiers in brackets).
- Files: `figures/png/attack_defence_layers.png`, `figures/pdf/attack_defence_layers.pdf`
- Kind: diagram; script: `figures/scripts/make_diagrams.py`
- Sources:
  - `research_output/completion/FINAL_VALIDATION_REPORT.md`
  - `research_output/mtd_defence/MTD_DEFENCE_REPORT.md`
  - `matrices/VERIFIED_METRICS.csv`
- Transformation: qualitative summary of measured verdicts

Registered but not used in the thesis: `direction_screen_cost`, `e3_schedule_predictability`, `e4_sweeps`, `m2_subset_types`, `overhead_in_training`

## Tables generated from data

Written by `tools/make_tables.py` to `build/tables/` and included in the thesis.

| Table | File | Sources | Transformation |
|---|---|---|---|
| A.1 | `build/tables/appendix_f1.md` | `data/mtd_defence/f1_runs.csv` (sha256 `8949d6aa95f46045…`; from `research/mtd-direction-screen`: `research_output/mtd_defence/experiments/f1_runs.csv`) | per-seed final-round ASR, accuracy and attacker rejection rate |
| 6.13 | `build/tables/direction_cost.md` | `data/mtd_defence/direction_benchmark.json` (sha256 `73864c9d63769b59…`; from `research/mtd-direction-screen`: `research_output/mtd_defence/direction_benchmark/benchmark_summary.json`) | means over two repetitions of protocol time, traffic and end-to-end time |
| 6.4 | `build/tables/e1_core.md` | `data/core/all_rounds.csv` (sha256 `e326f45f0382f043…`; from `research/spdz2k-secure-robust-aggregation`: `research_output/completion/experiments/metrics/all_rounds.csv`); `data/sum_only/pow2_all_rounds.csv` (sha256 `173ca7d46c41d460…`; from `research/sum-only-pow2-scale-fix`: `research_output/completion/experiments_pow2/metrics/all_rounds.csv`) | per run: mean accuracy of the last three recorded rounds and final-round ASR; mean and 95 % Student-t half-width over seeds; sum-only rows from the S = 2^40 rerun |
| 6.5 | `build/tables/e1_detection.md` | `data/core/summary_by_condition.csv` (sha256 `f4f64d0170471bae…`; from `research/spdz2k-secure-robust-aggregation`: `research_output/completion/experiments/summaries/summary_by_condition.csv`) | recorded per-condition means of the per-run rejection rates |
| 6.6 | `build/tables/e2_adaptive.md` | `data/core/all_rounds.csv` (sha256 `e326f45f0382f043…`; from `research/spdz2k-secure-robust-aggregation`: `research_output/completion/experiments/metrics/all_rounds.csv`) | final-round ASR per seed; mean and 95 % Student-t half-width; mean clean accuracy |
| 6.7 | `build/tables/e3_mtd.md` | `data/core/all_rounds.csv` (sha256 `e326f45f0382f043…`; from `research/spdz2k-secure-robust-aggregation`: `research_output/completion/experiments/metrics/all_rounds.csv`) | mean malicious participants per round, clean accuracy and final ASR; means and 95 % half-widths over seeds |
| 6.14 | `build/tables/e6.md` | `data/leakage/leakage_raw.csv` (sha256 `c957f6028c1dfc2d…`; from `research/gradient-inversion-leakage`: `research_output/completion/experiments/leakage/evaluation/leakage_raw.csv`) | share of trials with SSIM ≥ 0.9 and mean SSIM per batch size, model state and view (fc read-out) |
| 6.11 | `build/tables/f1.md` | `data/mtd_defence/f1_runs.csv` (sha256 `8949d6aa95f46045…`; from `research/mtd-direction-screen`: `research_output/mtd_defence/experiments/f1_runs.csv`) | mean, minimum and maximum final-round ASR; mean accuracy and rejection rates |
| 6.8 | `build/tables/m2.md` | `data/mtd_defence/m1_runs.csv` (sha256 `ccc7a63bda70fcca…`; from `research/mtd-direction-screen`: `research_output/mtd_defence/experiments/m1_runs.csv`); `data/mtd_defence/m2_runs.csv` (sha256 `3a5e308391eaca89…`; from `research/mtd-direction-screen`: `research_output/mtd_defence/experiments/m2_runs.csv`); `data/mtd_defence/m2b_runs.csv` (sha256 `14a9bc6be8272f3c…`; from `research/mtd-direction-screen`: `research_output/mtd_defence/experiments/m2b_runs.csv`) | means over seeds of final-round ASR and rejection rates; norm-only row combines M1 (seeds 101, 102) and M2b (103) |
| 6.12 | `build/tables/overhead.md` | `data/core/all_rounds.csv` (sha256 `e326f45f0382f043…`; from `research/spdz2k-secure-robust-aggregation`: `research_output/completion/experiments/metrics/all_rounds.csv`) | means over all rounds without attack of round time, MP-SPDZ protocol time and party traffic |
| 6.9 | `build/tables/p3.md` | `data/mtd_defence/p3_runs.csv` (sha256 `e772d59eca307c47…`; from `research/mtd-direction-screen`: `research_output/mtd_defence/experiments/p3_runs.csv`) | means over seeds 101–105 of the final-round ASR |
| 6.10 | `build/tables/p3_diff.md` | `data/mtd_defence/p3_paired_differences.csv` (sha256 `9eff93fb96fb19aa…`; from `research/mtd-direction-screen`: `research_output/mtd_defence/experiments/p3_paired_differences.csv`) | recorded paired differences and seed counts |
| 6.3 | `build/tables/validation.md` | `data/mtd_defence/scenario_summary_v20.csv` (sha256 `aa30e51bd6fea06d…`; from `research/mtd-direction-screen`: `research_output/mtd_defence/mpc_validation/scenario_summary.csv`) | one row per scenario; bit-exactness, accept bits and output check as recorded |

## Tables written in the text

| Table | Caption | Content taken from |
|---|---|---|
| 2.1 | Attacks on federated learning by adversary and goal. | literature review; every row cites its sources |
| 2.2 | Defence families compared. | literature review; every row cites its sources |
| 2.3 | Moving target defence in federated learning. | literature review; every row cites its sources |
| 3.1 | Adversaries, mitigations and residual risks. | design of the implemented framework: source code on research/mtd-direction-screen and docs/threat-model.md, FINAL_ARCHITECTURE.md (research/spdz2k-secure-robust-aggregation); Table 3.3 also the first prototype |
| 3.2 | Information revealed per robust round. | design of the implemented framework: source code on research/mtd-direction-screen and docs/threat-model.md, FINAL_ARCHITECTURE.md (research/spdz2k-secure-robust-aggregation); Table 3.3 also the first prototype |
| 3.3 | First prototype and final framework. | design of the implemented framework: source code on research/mtd-direction-screen and docs/threat-model.md, FINAL_ARCHITECTURE.md (research/spdz2k-secure-robust-aggregation); Table 3.3 also the first prototype |
| 4.1 | Software versions of the evaluation environment. | implementation on research/mtd-direction-screen: configuration classes, environment variables, scripts and measured run durations (run logs) |
| 4.2 | Environment variables. | implementation on research/mtd-direction-screen: configuration classes, environment variables, scripts and measured run durations (run logs) |
| 4.3 | Reproduction commands. | implementation on research/mtd-direction-screen: configuration classes, environment variables, scripts and measured run durations (run logs) |
| 4.4 | Common problems and remedies. | implementation on research/mtd-direction-screen: configuration classes, environment variables, scripts and measured run durations (run logs) |
| 5.1 | Modules of the `fl_security` package. | implementation on research/mtd-direction-screen: modules, MPC programs, attacks and test suite |
| 5.2 | Implemented attacks. | implementation on research/mtd-direction-screen: modules, MPC programs, attacks and test suite |
| 6.1 | Common experimental setting. | experiment grid and suite definitions (experiments/grid.py, experiments/suite.py) and run configurations |
| 6.2 | Studies of the evaluation (542 training runs, 157 of them in SPDZ2k). | run inventories of all studies (Appendix C, Table C.2) |
| 6.15 | What the evidence establishes and what it does not. | summary of the results of Sections 6.2–6.8 |
| 7.1 | The objectives and how they were addressed. | summary of Chapters 2–6 |
| B.1 | Compliance with the approved topic declaration. | approved topic declaration and this thesis |
| C.1 | Test results per branch. | test result files and run inventories of each branch (paths in the table) |
| C.2 | Location of the experimental evidence. | test result files and run inventories of each branch (paths in the table) |

## Data manifest

| File | Branch | Original path | SHA-256 | Bytes |
|---|---|---|---|---:|
| `data/core/accuracy_over_rounds.csv` | `research/spdz2k-secure-robust-aggregation` | `research_output/completion/experiments/summaries/accuracy_over_rounds.csv` | `0282c83fb01fe2517a7b853ef8e106c67780ac1373d0c9a67740e66153a6eef2` | 306475 |
| `data/core/summary_by_condition.csv` | `research/spdz2k-secure-robust-aggregation` | `research_output/completion/experiments/summaries/summary_by_condition.csv` | `f4f64d0170471bae8f7312e65149d566d5e275dda032aaaf59d42d752f058738` | 230594 |
| `data/core/paired_differences.csv` | `research/spdz2k-secure-robust-aggregation` | `research_output/completion/experiments/summaries/paired_differences.csv` | `376949ea7a191691e5e7a14413e31ee1db3d8cd1922e41d32a15178843aac6c5` | 19466 |
| `data/core/attack_defence_matrix.csv` | `research/spdz2k-secure-robust-aggregation` | `research_output/completion/experiments/summaries/attack_defence_matrix.csv` | `a4b13d71681a84936f9f98d8eddb300da02426baf957cccb1d4cbe1ad125cb4a` | 31545 |
| `data/core/equivalence_checks.csv` | `research/spdz2k-secure-robust-aggregation` | `research_output/completion/experiments/summaries/equivalence_checks.csv` | `160f3186fe9fd62a306bfb3278acf19118a011901f50ec08852fa2b923388f9a` | 5173 |
| `data/core/end_to_end_reference_check.csv` | `research/spdz2k-secure-robust-aggregation` | `research_output/completion/experiments/summaries/end_to_end_reference_check.csv` | `dfa9567888defd458fdfe7fa9d8a02d6cae352f80793594d6bb6512ab9498308` | 31083 |
| `data/core/key_results.md` | `research/spdz2k-secure-robust-aggregation` | `research_output/completion/experiments/summaries/key_results.md` | `a8a8a3c4f1f30b0d8a6bec7c38b4a5255b59134d87d5d4f5ae1932fd6f49f11b` | 10746 |
| `data/core/all_rounds.csv` | `research/spdz2k-secure-robust-aggregation` | `research_output/completion/experiments/metrics/all_rounds.csv` | `e326f45f0382f0432b4925a14230e5d5c9f39ba66fe662120d56bd95f9e41ecf` | 1563107 |
| `data/validation/scenario_summary_v13.csv` | `research/spdz2k-secure-robust-aggregation` | `research_output/completion/experiments/mpc_validation/scenario_summary.csv` | `c04f4f250e02ee974ef79d8d9efabd08fb9c11879db21b6faaf447ec5696a2bd` | 2397 |
| `data/mtd_exposure/exposure_summary_R10.csv` | `research/spdz2k-secure-robust-aggregation` | `research_output/completion/experiments/mtd_exposure/exposure_summary_R10.csv` | `ad4f5cf92f61ee52d79d97104e8494e1838f827a4746db808fd76ee9a0e316e1` | 20162 |
| `data/mtd_exposure/exposure_summary_R100.csv` | `research/spdz2k-secure-robust-aggregation` | `research_output/completion/experiments/mtd_exposure/exposure_summary_R100.csv` | `8a56e3b4e8b6fab3f6ced095199f61a17ccc65b088224a734d107c679b3b6270` | 19959 |
| `data/benchmarks/benchmark_results.csv` | `research/spdz2k-secure-robust-aggregation` | `research_output/completion/benchmarks/benchmark_results.csv` | `a10354f6e8e9e60bc655f07343ec7ad5f3fdf49b1c237f875058261624305468` | 10848 |
| `data/benchmarks/benchmark_summary.csv` | `research/spdz2k-secure-robust-aggregation` | `research_output/completion/benchmarks/benchmark_summary.csv` | `e15d6d990f843675522df34c08f3500f676637f80a35e3ed39579d9b0ea3b46c` | 4716 |
| `data/leakage/leakage_summary.csv` | `research/gradient-inversion-leakage` | `research_output/completion/experiments/leakage/evaluation/leakage_summary.csv` | `b9ef5c3f2ced3f6892e2f7e00f81711bdcee0e0f7bb3854528da96bed8ba0fab` | 20544 |
| `data/leakage/leakage_raw.csv` | `research/gradient-inversion-leakage` | `research_output/completion/experiments/leakage/evaluation/leakage_raw.csv` | `c957f6028c1dfc2db363e033732a70b685852a52683d1c8e483d6fd7f134f591` | 160359 |
| `data/leakage/leakage_table.md` | `research/gradient-inversion-leakage` | `research_output/completion/experiments/leakage/evaluation/leakage_table.md` | `77af3a949a5dab845eb3cc22046114bd8b73f5a76f6286963b4e6efb1757d6d3` | 4786 |
| `data/mtd_defence/pilot_scores.csv` | `research/mtd-direction-screen` | `research_output/mtd_defence/pilot/pilot_scores.csv` | `b5f35133803735c20ee5df83fba308dcec34adb6c5ff6e98232e676af111759c` | 2737892 |
| `data/mtd_defence/pilot_summary.csv` | `research/mtd-direction-screen` | `research_output/mtd_defence/pilot/pilot_summary.csv` | `d3379969192c2b67510fde9efbbb47b4edc2275fb2fdbc8b24f6963d335a58ea` | 3976 |
| `data/mtd_defence/scenario_summary_v20.csv` | `research/mtd-direction-screen` | `research_output/mtd_defence/mpc_validation/scenario_summary.csv` | `aa30e51bd6fea06d2e6131cd7800762b2b144cb7e7c26e52ac319b51664f069b` | 3721 |
| `data/mtd_defence/direction_benchmark.json` | `research/mtd-direction-screen` | `research_output/mtd_defence/direction_benchmark/benchmark_summary.json` | `73864c9d63769b597a598d2e156498f90f4ca9d4d6fb0bd5c7601893f0faa53b` | 4282 |
| `data/mtd_defence/p3_paired_differences.csv` | `research/mtd-direction-screen` | `research_output/mtd_defence/experiments/p3_paired_differences.csv` | `9eff93fb96fb19aaf55cd1be89f284f019789d7fc1f7e2e4aae12dab631ae032` | 873 |
| `data/mtd_defence/m1_runs.csv` | `research/mtd-direction-screen` | `research_output/mtd_defence/experiments/m1_runs.csv` | `ccc7a63bda70fccad7f62744d4a14f1965ecf671ae59b21b6fe66f2ffeab31a7` | 7946 |
| `data/mtd_defence/m1_summary.csv` | `research/mtd-direction-screen` | `research_output/mtd_defence/experiments/m1_summary.csv` | `94e14d884f5ecd334df9a8da02ec4aa24541ca1fdeb34a62701e356f5442640a` | 7592 |
| `data/mtd_defence/m2_runs.csv` | `research/mtd-direction-screen` | `research_output/mtd_defence/experiments/m2_runs.csv` | `3a5e308391eaca89cb3c14959293d9152c9d3a897e5d6f19385279363b9d864a` | 7475 |
| `data/mtd_defence/m2_summary.csv` | `research/mtd-direction-screen` | `research_output/mtd_defence/experiments/m2_summary.csv` | `c2b74da33302f1ca394b2e578b0e5a85b462d3e69ea7172b9f7f6c6ac74d3d1e` | 5554 |
| `data/mtd_defence/m2b_runs.csv` | `research/mtd-direction-screen` | `research_output/mtd_defence/experiments/m2b_runs.csv` | `14a9bc6be8272f3c7fd4dab97861a39bb88833a425206553fe0df3b82ef34161` | 612 |
| `data/mtd_defence/m2b_summary.csv` | `research/mtd-direction-screen` | `research_output/mtd_defence/experiments/m2b_summary.csv` | `afbd878b6ded9c8e9327b9f93db6f9fa1df60bd9fe8e2e89d848390871063adf` | 1167 |
| `data/mtd_defence/m3_runs.csv` | `research/mtd-direction-screen` | `research_output/mtd_defence/experiments/m3_runs.csv` | `be1ed7eecc3019daf8c7b452d829c45260dbf21dec1ef6b29e2ebdc3a5e18212` | 5814 |
| `data/mtd_defence/m3_summary.csv` | `research/mtd-direction-screen` | `research_output/mtd_defence/experiments/m3_summary.csv` | `331533080af8376d2f04d07864b39d3e9cb7bc57aebba3433ac01e780b400917` | 4002 |
| `data/mtd_defence/p3_runs.csv` | `research/mtd-direction-screen` | `research_output/mtd_defence/experiments/p3_runs.csv` | `e772d59eca307c4775a8a079047b66c02bb2f533fab81e2e4a436bf1457c1189` | 9604 |
| `data/mtd_defence/p3_summary.csv` | `research/mtd-direction-screen` | `research_output/mtd_defence/experiments/p3_summary.csv` | `9c39bc22bac50b6486598c47aa52fb2f5eb48faa99a2fbded7f23bf94ec22012` | 3995 |
| `data/mtd_defence/f1_runs.csv` | `research/mtd-direction-screen` | `research_output/mtd_defence/experiments/f1_runs.csv` | `8949d6aa95f460455f55552b9b8e464bbc1650b2e3d16534f7a432f4f05e4ae3` | 2140 |
| `data/mtd_defence/f1_summary.csv` | `research/mtd-direction-screen` | `research_output/mtd_defence/experiments/f1_summary.csv` | `5627158f7ba81d0fb429d2b3f5815a5aa7f4cfaef582528655e15e75c1defc0b` | 1815 |
| `data/sum_only/pow2_vs_fedavg.csv` | `research/sum-only-pow2-scale-fix` | `research_output/completion/experiments_pow2/pow2_vs_fedavg.csv` | `22a24ed9de9ab31b93ea7f872b4773f1dc24589aac562697b33b735b134985b2` | 2672 |
| `data/sum_only/pow2_accuracy_over_rounds.csv` | `research/sum-only-pow2-scale-fix` | `research_output/completion/experiments_pow2/summaries/accuracy_over_rounds.csv` | `cd36e01faa37dd00781fbbb62551f656d9ad5aea3e01f8decac5df98731809bc` | 38126 |
| `data/sum_only/pow2_summary_by_condition.csv` | `research/sum-only-pow2-scale-fix` | `research_output/completion/experiments_pow2/summaries/summary_by_condition.csv` | `8388a39134325a44a6a4be523c7b2158090e93543a4bdcfd0380c30cfb2cd525` | 34048 |
| `data/sum_only/pow2_all_rounds.csv` | `research/sum-only-pow2-scale-fix` | `research_output/completion/experiments_pow2/metrics/all_rounds.csv` | `173ca7d46c41d4608ad2713d049d140a024e4e188204ec17248e5f248b68c242` | 178642 |
| `data/sum_only/pow2_suite_progress.jsonl` | `research/sum-only-pow2-scale-fix` | `research_output/completion/experiments_pow2/suite_progress.jsonl` | `f08a976996e742629dd8ba0e6c5c9575e2698c5d10aefdfc8cd023454abbda0f` | 4796 |
| `data/sum_only/scaled_replacement_baseline_s102_results.csv` | `research/spdz2k-secure-robust-aggregation` | `research_output/completion/experiments/runs/e1/e1__baseline__scaled_replacement__s102/e1__baseline__scaled_replacement__s102_results.csv` | `ba7001cc80f8b5bafa495716e8001e1ed4bb3bcc0e786caef22966d768a979ef` | 2828 |
| `data/sum_only/scaled_replacement_smpc_only_1e6_s102_results.csv` | `research/spdz2k-secure-robust-aggregation` | `research_output/completion/experiments/runs/e1/e1__smpc_only__scaled_replacement__s102/e1__smpc_only__scaled_replacement__s102_results.csv` | `5202e46be7ddb8b2f0eea5eac9e9e2d7207d4e95f13ea1175af852e1ba7b0d90` | 3829 |
| `data/sum_only/scaled_replacement_smpc_only_2p40_s102_results.csv` | `research/sum-only-pow2-scale-fix` | `research_output/completion/experiments_pow2/runs/e1/e1__smpc_only__scaled_replacement__s102/e1__smpc_only__scaled_replacement__s102_results.csv` | `68802558c00635ca15feabeb08c5971ad1b114085f31fac8d57a909de1bbb0ae` | 3796 |
