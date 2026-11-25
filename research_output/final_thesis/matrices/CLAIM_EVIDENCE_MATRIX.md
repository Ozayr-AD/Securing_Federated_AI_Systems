# Claim–Evidence Matrix

Every main claim of the thesis, the section that makes it, the study behind it, the evidence, and how the
number was verified for this document.

**Verification codes**

- **R** – recomputed by `tools/verify_metrics.py` from the data copies in `data/`; the key in
  `matrices/VERIFIED_METRICS.csv` is given (`*` stands for all matching keys). All 668 recomputed values
  agree with the summaries of the original analyses where such a summary exists.
- **T** – computed by `tools/make_tables.py` from the data copies for the table named.
- **Rep** – taken from a report or log of the branch that produced it; not recomputed here. The thesis
  text says so where the claim is made.
- **D** – a design property, shown by construction, by the code and its tests, or by arithmetic.

Data copies are listed with their SHA-256 and original location in `data/MANIFEST.csv` and
`FIGURE_DATA_PROVENANCE.md`. Branches: TC = `research/spdz2k-secure-robust-aggregation`, UL = `research/gradient-inversion-leakage`,
SO = `research/sum-only-pow2-scale-fix`, MD = `research/mtd-direction-screen`.

## Correctness of the secure computation (Section 6.2)

| ID | Claim | Study | Evidence | Verification |
|---|---|---|---|---|
| C1 | The SPDZ2k program reproduced its exact plaintext reference in all 20 adversarial validation scenarios. | V (MD) | `data/mtd_defence/scenario_summary_v20.csv` | R `validation.v20.bit_exact` = 20/20 |
| C2 | The 13 scenarios without the direction screen were also bit-exact on TC, and again from a fresh clone. | V (TC) | `data/validation/scenario_summary_v13.csv`; fresh clone: TC `FINAL_VALIDATION_REPORT.md` §2–3 | R `validation.v13.bit_exact` = 13/13; fresh clone Rep |
| C3 | All 21 robust benchmark rounds (up to 100,000 parameters) and all 6 direction-screen benchmark rounds were bit-exact. | B, direction benchmark | `data/benchmarks/benchmark_summary.csv`, `data/mtd_defence/direction_benchmark.json` | R `bench.robust.completed_rounds`, `bench.robust.all_bit_exact`, `direction_bench.*.bit_exact` |
| C4 | Two colluding clients among four are caught by the output check (aggregate norm 1.42 > 1); among eight they pass (0.725) while exceeding their per-client bound. | V | `data/mtd_defence/scenario_summary_v20.csv` | R `validation.colluding_cancellation_k4.*`, `…k8.*`; injected norm 5.66 by construction of the scenario (D) |
| C5 | In the 70 SPDZ2k runs of the robust program in E1–E5 (700 rounds), the applied update differed from the exact reference by at most 2.4·10⁻⁷. | E1–E5 | `data/core/end_to_end_reference_check.csv` | R `reference.spdz2k_robust.*` |
| C6 | SPDZ2k and the plaintext execution of the same algorithm produced identical training trajectories (difference 0.0). | E1x/E4 | `data/core/equivalence_checks.csv` | R `reference.spdz2k_vs_plaintext_robust.*` |
| C7 | Every round of the 15 F1 runs matched the reference to 1.2·10⁻⁷. | F1 | MD `research_output/mtd_defence/MTD_DEFENCE_REPORT.md` | Rep |
| C8 | With S = 10⁶ all 18 `smpc_only` runs differed from FedAvg (accuracy difference up to 0.51); with S = 2⁴⁰ all 18 equal FedAvg in every recorded round (15 complete, 3 until the fail-closed abort). | sum-only rerun (SO) | `data/sum_only/pow2_vs_fedavg.csv` | R `sum_only.*` |
| C9 | Cause: values exactly halfway between two float32 numbers round differently with a decimal scale (129–192 parameters differ in round 1; 97 % at halfway values). | diagnostic (SO) | SO `research_output/completion/experiments/diagnostics/` | Rep |

## Core comparison and adaptive attackers (Sections 6.3–6.4)

| ID | Claim | Study | Evidence | Verification |
|---|---|---|---|---|
| C10 | No measurable clean-accuracy cost: 0.823–0.830 without attack in every configuration. | E1 | `data/core/all_rounds.csv`, `data/sum_only/pow2_all_rounds.csv` | R `e1.*.none.last3_mean_accuracy.mean`; T Table 6.4 |
| C11 | Secure sum-only aggregation alone does not stop poisoning: the backdoor reaches 0.921 as under FedAvg. | E1, sum-only rerun | as C8 and C10 | R `e1.baseline.backdoor.final_backdoor_asr.mean`, `sum_only.*`; T Table 6.4 |
| C12 | MTD alone is not a poisoning defence: under the backdoor, accuracy 0.317 (FedAvg + MTD) and 0.494 (sum-only + MTD) against 0.712 with static participation. | E1 | as C10 | R `e1.mtd_only.backdoor.*`, `e1.baseline.backdoor.*`; T Table 6.4 (sum-only + MTD from the rerun) |
| C13 | Static clipping bounds magnitude attacks (0.812, 0.760) but only halves the backdoor (ASR 0.467); a clipped attacker still contributes 0.31–0.35 of the aggregate. | E1 | `data/core/all_rounds.csv` | R `e1.smpc_clip.*` incl. `…malicious_share_effective` |
| C14 | The full framework mitigates every magnitude attack (0.821, 0.827, 0.817) and the boosted backdoor (ASR 0.921 → 0.017); the attackers' share of the aggregate falls from 0.41–0.62 to 0.000–0.161. | E1 | `data/core/all_rounds.csv` | R `e1.smpc_defence_mtd.*`, `e1.baseline.*.malicious_share_effective` |
| C15 | No honest participation was rejected in the 18 runs of the full framework; 37 % of honest participations were clipped. | E1 | `data/core/all_rounds.csv` | R `e1.smpc_defence_mtd.honest_rejected`, `…honest_clipped_share` |
| C16 | Rejection rates of the full framework: sign flip and scaled replacement 1.00, backdoor 0.83, noise 0.77, label flip 0.44 (means of per-run rates). | E1 | `data/core/all_rounds.csv`, `data/core/summary_by_condition.csv` | R `e1.smpc_defence_mtd.*.rejection_tpr` (pooled rates also recorded) |
| C17 | Label flipping is only partly mitigated (accuracy 0.724 ± 0.386). | E1 | as C10 | R `e1.smpc_defence_mtd.label_flip.*` |
| C18 | Secure screening and clipping match the plaintext detector against static attackers without the coordinator seeing an update. | E1x | `data/core/all_rounds.csv` | R `e1x.*` |
| C19 | An attacker at 0.95 × the published threshold is never rejected; against the full framework it is clipped in 30–70 % of its participations, contributes 0.27–0.30 and reaches ASR 0.167 (0.053–0.345); static clipping 0.304; detector 0.019. | E2 | `data/core/all_rounds.csv` | R `e2.*`, `e2.smpc_defence_mtd.s*.*`; T Table 6.6 |
| C20 | Attack strength and number of attackers (E4): ×1 backdoor not rejected (ASR 0.07/0.13 vs 0.38), from ×2 rejected (ASR 0.024–0.027); sign flip ×2 0.806 vs 0.700. | E4 | `data/core/all_rounds.csv`, `data/core/summary_by_condition.csv` | R `core.cells_checked` (all 170 E1–E5 accuracy and ASR cells, 0 mismatches); rejection shares at ×2–×16 from the analysis summary |
| C21 | Non-IID data (E5): 0.788 vs 0.783 clean; under the backdoor 0.775/0.750 with ASR 0.001/0.006; first honest rejection (0.069 in seed 102). | E5 | `data/core/all_rounds.csv`, `data/core/summary_by_condition.csv` | R `e5.*` (accuracy, ASR); honest rejection from the analysis summary |

## Moving target defence and direction screen (Sections 6.5–6.6)

| ID | Claim | Study | Evidence | Verification |
|---|---|---|---|---|
| C22 | Under the secret schedule every adversary's hit rate is 0.33 = K/N; a just-in-time adversary reaches 1.00 against static and deterministic schedules; a predictive one 0.52–0.59 against the deterministic schedule. | E3-MC | `data/mtd_exposure/exposure_summary_R10.csv` | R `e3mc.R10.*` |
| C23 | In training, the secret schedule reduced schedule-aware adversaries to 0.7–0.9 attackers per round and kept accuracy at 0.717/0.761, but did not stop the backdoor once an attacker was selected (ASR ≈ 0.5). | E3 | `data/core/all_rounds.csv` | T Table 6.7; accuracy and ASR cells R `core.cells_checked` |
| C24 | MTD defends against schedule prediction, not against poisoning as such. | E1, E3, E3-MC | C12, C22, C23 | interpretation of R-verified results |
| C25 | Magnitude does not separate the adaptive attacker: median norm 1.00 × the threshold (29 participations, 0.91–1.84) against the full framework. | pilot | `data/mtd_defence/pilot_scores.csv` | R `pilot.adaptive.smpc_defence_mtd.attacker_norm_over_T_median` |
| C26 | Sign agreement separates single attackers (AUC on a 25 % subset 0.98, 0.98, 0.83, 0.82, 0.70, 0.66) but not cohorts with two or more attackers; honest median 0.61, 5.3 % below 0.52. | pilot (175 runs, 6,308 participations) | `data/mtd_defence/pilot_scores.csv` | R `pilot.*` |
| C27 | At τ = 0.5 (M1) the screen rejected 5–10 % of the adaptive backdoor's participations and at most 5 % of the evasive attacker's, and raised label-flip rejection from 0.75 to 0.90. | M1 | `data/mtd_defence/m1_runs.csv` | R `m1.*` |
| C28 | At τ = 0.52 (M2) only the secret 25 % subset kept the adaptive backdoor low in every seed (0.040–0.064 vs 0.064–0.417); all coordinates defeat the evasive attacker (0.021); label flippers rejected 0.93 vs 0.77; honest false rejections 2.5 % (secret 25 %), 5 % (10 %), up to 11 %. | M2, M2b | `data/mtd_defence/m1_runs.csv`, `m2_runs.csv`, `m2b_runs.csv` | R `m2.*`; T Table 6.8 |
| C29 | Static cohorts of seven raise the adaptive backdoor to 0.49 (0.19 with cohorts of four); the unpaired M3 contrast (0.217 vs 0.628) is withdrawn because F1 gave 0.680 for the same combination. | M3, F1 | `data/mtd_defence/m3_runs.csv`, `f1_runs.csv` | R `m3.*`, `m2.baseline_norm_only.adaptive_backdoor.asr_mean`, `f1.adaptive_backdoor__jit4.asr_mean`; T Section 6.6 (text) |
| C30 | Paired secrets worked: both MTD conditions had identical attacker participations, and the static norm-only runs equal M3 exactly. | P3 | `data/mtd_defence/p3_runs.csv`, `m3_runs.csv` | R `p3.mtd_conditions_identical_exposure` = 1, `p3.static_norm_only_equals_m3` = 1 |
| C31 | Secret MTD + secret screen had the lowest mean ASR against every attacker (adaptive 0.132, evasive 0.067, just-in-time 0.568); the secret schedule cut the just-in-time adversary from 40 to 22–27 participations and restored accuracy from 0.66 to 0.82. | P3 | `data/mtd_defence/p3_runs.csv`, `p3_paired_differences.csv` | R `p3.*`; T Tables 6.9, 6.10, A.2 |
| C32 | Five seeds cannot establish significance: one-sided sign test p = 1/32 ≈ 0.031 at best; comparisons against secret MTD alone do not reach 5 %. | P3 | as C31 | R `p3.signs.*`; D (sign-test arithmetic) |
| C33 | Without attack: ASR ≈ 0.02, accuracy 0.833–0.835, honest rejection ≤ 2.2 % on average (7.1 % in one run). | P3 | `data/mtd_defence/p3_runs.csv` | R `p3.none.*`, `p3.honest_rejection.*` |
| C34 | The final framework in SPDZ2k kept accuracy 0.833, rejected 88 % of label flippers, partly mitigated the adaptive (0.217) and evasive (0.153) backdoors, and held the just-in-time adversary to 0.680 with almost no screen rejections (4.4 %). | F1 | `data/mtd_defence/f1_runs.csv` | R `f1.*`; T Tables 6.11, A.3 |
| C35 | An F1 run took 46 minutes; the whole host peaked at 7.7 GB. | F1 | MD F1 run logs (kept on the evaluation host) | Rep |

## Cost and leakage (Sections 6.7–6.8)

| ID | Claim | Study | Evidence | Verification |
|---|---|---|---|---|
| C36 | A round of the full framework takes 3.7 × a FedAvg round (32.5 s vs 8.79 s); static clipping 3.5 ×; MTD adds nothing measurable; the sum-only round is slower in wall time because its program is compiled every round (about 8.5 s). | E1 | `data/core/all_rounds.csv`, `data/benchmarks/benchmark_summary.csv` | R `overhead.e1.*`, `bench.sum_only.d2202.compile_seconds`; T Table 6.12 |
| C37 | Cost grows linearly with the model size: about 13 triples per coordinate (robust) and 5 (sum-only), 3,836 random bits independent of d; 5.9 ms and 1.26 MB per parameter (robust), 2.5 ms and 0.53 MB (sum-only); 592 s for 100,000 parameters; sum-only at 250,000 stopped by the timeout; two parties 1.77 × faster with a third of the traffic. | B | `data/benchmarks/benchmark_summary.csv`, `benchmark_results.csv` | R `bench.*` |
| C38 | A robust round for the 2.12-million-parameter CIFAR-10 CNN would take about 3.4 h and 2.7 TB on this host. | B | C37 | D (linear extrapolation, stated as not measured) |
| C39 | The secret 25 % direction screen costs about seven times the protocol time of the norm defence (147.6 s vs 21.1 s; 29.5 GB vs 4.3 GB). | direction benchmark | `data/mtd_defence/direction_benchmark.json` | R `direction_bench.*`; compiled triple and bit counts Rep (MD `MTD_DEFENCE_REPORT.md`) |
| C40 | From the aggregate of four clients, a curious coordinator recovers 75–100 % of the target's images near-exactly with one image per client and 3–28 % with eight; from an individual update nearly all. | E6 (UL) | `data/leakage/leakage_raw.csv` | R `e6.fc_input.*`; T Table 6.14 |
| C41 | Features: cosine 1.000 from an individual update, 0.96–0.97 from the aggregate; labels: precision 1.00 vs 0.29–0.71; optimisation-based inversion of the CompactCNN: best SSIM 0.44. | E6 | `data/leakage/leakage_raw.csv` | R `e6.fc_features.*`, `e6.labels.*`, `e6.optimisation.max_ssim` |

## Design and supporting claims (Chapters 3–5, Appendix C)

| ID | Claim | Where | Evidence | Verification |
|---|---|---|---|---|
| C42 | Every decision of the in-MPC defence uses the visible contribution, so wrap-around and weight-inverse inputs cannot pass a naive norm check; with one deviating client every applied round satisfies the per-client bound or is rejected. | 3.3 | `spdz2k_robust_aggregate.mpc`, `smpc/robust.py`, validation scenarios | D (proposition and code); exercised by C1 and C4 |
| C43 | With K = 4 the lower median is an honest norm whenever at most two norms are inflated; a random cohort of four contains two or more of three attackers with probability 117/495 ≈ 0.24. | 3.3, 3.4 | – | D (arithmetic) |
| C44 | The secret schedule and subsets are unpredictable without `FL_MTD_SECRET` (HMAC-SHA256 counter PRF, unbiased sampling). | 3.4, 3.5, 5.6 | `mtd/randomness.py`, `mtd/controller.py`, tests | D (construction on HMAC, RFC 2104); empirically C22 |
| C45 | SPDZ2k costs: about 3,100 triples per second for three parties; a 64-bit comparison costs about 126 triples and 63 random bits. | 3.3 | MD `docs/secure_robust_aggregation.md` | Rep (calibration on the host) |
| C46 | The first prototype's detector raised accuracy from 0.464 to 0.629 (5 seeds, 3 rounds). | 3.7 | earlier draft of the thesis | Rep (stated in the text as not re-verified) |
| C47 | Test suites: 131 + 1 skipped (TC), 143 (UL), 138 (SO), 159 (MD); real three-party integration test passed. | Appendix C | `test_results*.txt` files named in Table C.1 | recorded test logs |
| C48 | All 93 references were verified against independent bibliographic sources. | Appendix C | `matrices/REFERENCE_VERIFICATION.csv`, `.md` | verification record (OpenAlex, doi.org, official proceedings pages) |
| C49 | 542 recorded training runs, 157 of them in SPDZ2k. | abstract, Table 6.2 | run inventories (Table C.2) | Rep/D: 228 (E1–E5) + 36 (sum-only rerun) + 278 (M1, M2, M2b, M3, P3, F1) = 542; SPDZ2k 106 + 36 + 15 = 157 |
