"""Recompute the thesis's key numbers from the copied evidence (data/).

    python research_output/final_thesis/tools/verify_metrics.py

Writes matrices/VERIFIED_METRICS.csv (one row per recomputed number, with the
source file and method) and matrices/VERIFICATION_LOG.txt (every comparison
with the value reported by the original analysis). Nothing in data/ is changed.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parents[1]
DATA = HERE / "data"
OUT = HERE / "matrices"
T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262}
ROWS: list[dict] = []
LOG: list[str] = []


def record(key, value, source, method, reported=None, tol=1e-3):
    status = "recomputed"
    if reported is not None and not (isinstance(reported, float) and math.isnan(reported)):
        diff = abs(float(value) - float(reported))
        status = "matches report" if diff <= tol else f"DIFFERS from report ({reported})"
        LOG.append(f"{key}: recomputed {value:.6g} vs reported {float(reported):.6g} -> {status}")
    ROWS.append({"key": key, "value": value, "source": source, "method": method, "status": status})


def mean_ci(values):
    values = np.asarray(values, dtype=float)
    n = len(values)
    mean = float(values.mean())
    half = float(T975[n - 1] * values.std(ddof=1) / math.sqrt(n)) if n > 1 else float("nan")
    return mean, half


def auc(honest, attacker):
    """P(honest score > attacker score) + 0.5 P(tie): low agreement flags attackers."""
    honest, attacker = np.asarray(honest), np.asarray(attacker)
    if len(honest) == 0 or len(attacker) == 0:
        return float("nan")
    greater = (honest[:, None] > attacker[None, :]).mean()
    ties = (honest[:, None] == attacker[None, :]).mean()
    return float(greater + 0.5 * ties)


# ---------------------------------------------------------------- E1-E5 from per-round records
def core_studies():
    rounds = pd.read_csv(DATA / "core/all_rounds.csv")
    summary = pd.read_csv(DATA / "core/summary_by_condition.csv")
    rounds = rounds.sort_values(["study", "condition", "attack", "seed", "round"])
    per_run = []
    for (study, cond, attack, seed), frame in rounds.groupby(["study", "condition", "attack", "seed"]):
        trained = frame[frame["round"] >= 1]
        per_run.append({
            "study": study, "condition": cond, "attack": attack, "seed": seed,
            "last3": float(trained["global_accuracy"].tail(3).mean()),
            "asr": float(trained["backdoor_asr"].iloc[-1]) if trained["backdoor_asr"].notna().any() else float("nan"),
            "round_seconds": float(trained["round_seconds"].mean()),
        })
    per_run = pd.DataFrame(per_run)
    checked = mismatched = 0
    for (study, cond, attack), frame in per_run.groupby(["study", "condition", "attack"]):
        for metric, column in (("last3_mean_accuracy", "last3"), ("final_backdoor_asr", "asr")):
            values = frame[column].dropna()
            if values.empty:
                continue
            mean, half = mean_ci(values)
            rep = summary[(summary.study == study) & (summary.condition == cond)
                          & (summary.attack == attack) & (summary.metric == metric)]
            if rep.empty:
                continue
            checked += 1
            rep_mean = float(rep["mean"].iloc[0])
            if abs(mean - rep_mean) > 5e-4:
                mismatched += 1
                LOG.append(f"MISMATCH {study}/{cond}/{attack}/{metric}: recomputed {mean:.4f} vs {rep_mean:.4f}")
            if study == "e1" or (study in ("e1x", "e2", "e5")):
                record(f"{study}.{cond}.{attack}.{metric}.mean", round(mean, 4), "data/core/all_rounds.csv",
                       f"per-run {'mean of rounds >=1 last three' if column == 'last3' else 'final-round'} value, mean over {len(values)} seeds",
                       rep_mean, tol=5e-4)
                record(f"{study}.{cond}.{attack}.{metric}.ci95_half", round(half, 4), "data/core/all_rounds.csv",
                       f"Student-t half-width, n={len(values)}")
    LOG.append(f"E1-E5 cells checked against summary_by_condition.csv: {checked}, mismatches: {mismatched}")
    record("core.cells_checked", checked, "data/core/all_rounds.csv", "condition x attack x metric cells recomputed")
    record("core.cells_mismatched", mismatched, "data/core/all_rounds.csv", "cells differing by > 5e-4")
    # overhead per round (E1, no attack)
    e1 = rounds[(rounds.study == "e1") & (rounds.attack == "none") & (rounds["round"] >= 1)]
    for cond, frame in e1.groupby("condition"):
        record(f"overhead.e1.{cond}.round_seconds", round(float(frame["round_seconds"].mean()), 2),
               "data/core/all_rounds.csv", "mean over 3 runs x 10 rounds")
        if "mpc_protocol_seconds_max" in frame and frame["mpc_protocol_seconds_max"].notna().any():
            record(f"overhead.e1.{cond}.protocol_seconds", round(float(frame["mpc_protocol_seconds_max"].mean()), 2),
                   "data/core/all_rounds.csv", "mean MP-SPDZ protocol seconds (max over parties)")
            record(f"overhead.e1.{cond}.traffic_mb", round(float(frame["mpc_global_data_sent_mb"].mean()), 0),
                   "data/core/all_rounds.csv", "mean MP-SPDZ global data sent per round (MB)")
    # full framework detection (E1)
    ff = rounds[(rounds.study == "e1") & (rounds.condition == "smpc_defence_mtd") & (rounds["round"] >= 1)]
    for attack, frame in ff.groupby("attack"):
        tp = frame["rejected_true_positives"].sum()
        fp = frame["rejected_false_positives"].sum()
        mal = frame["malicious_selected"].sum()
        honest = frame["honest_participants"].sum()
        if mal:
            record(f"e1.smpc_defence_mtd.{attack}.rejection_tpr_pooled", round(tp / mal, 3), "data/core/all_rounds.csv",
                   "pooled: rejected malicious participations / malicious participations over all seeds")
            per_seed = frame.groupby("seed").apply(
                lambda g: g["rejected_true_positives"].sum() / g["malicious_selected"].sum()
                if g["malicious_selected"].sum() else float("nan"), include_groups=False)
            rep = summary[(summary.study == "e1") & (summary.condition == "smpc_defence_mtd")
                          & (summary.attack == attack) & (summary.metric == "rejection_tpr")]
            record(f"e1.smpc_defence_mtd.{attack}.rejection_tpr", round(float(per_seed.mean()), 3),
                   "data/core/all_rounds.csv", "mean over seeds of the per-run rejection TPR (definition used in the thesis)",
                   float(rep["mean"].iloc[0]) if not rep.empty else None)
        if honest:
            record(f"e1.smpc_defence_mtd.{attack}.rejection_fpr", round(fp / honest, 3), "data/core/all_rounds.csv",
                   "rejected honest participations / honest participations")


# ---------------------------------------------------------------- pilot (direction screen)
def pilot():
    p = pd.read_csv(DATA / "mtd_defence/pilot_scores.csv")
    p = p[p.attack != "none"] if "none" in set(p.attack) else p
    for column in ("sign_agree", "sign_agree_0.25_single"):
        single = p[p.attackers_in_cohort == 1]
        for attack, frame in single.groupby("attack"):
            value = auc(frame.loc[~frame.malicious, column].dropna(), frame.loc[frame.malicious, column].dropna())
            record(f"pilot.{column}.auc.single_attacker.{attack}", round(value, 3), "data/mtd_defence/pilot_scores.csv",
                   "AUC (honest agreement > attacker agreement), cohorts with exactly one attacker")
        double = p[p.attackers_in_cohort >= 2]
        for attack, frame in double.groupby("attack"):
            value = auc(frame.loc[~frame.malicious, column].dropna(), frame.loc[frame.malicious, column].dropna())
            record(f"pilot.{column}.auc.multi_attacker.{attack}", round(value, 3), "data/mtd_defence/pilot_scores.csv",
                   "AUC, cohorts with two or more attackers")
        honest = p.loc[~p.malicious, column].dropna()
        record(f"pilot.{column}.honest_median", round(float(honest.median()), 3), "data/mtd_defence/pilot_scores.csv",
               "median agreement of honest participations")
        record(f"pilot.{column}.honest_p05", round(float(honest.quantile(0.05)), 3), "data/mtd_defence/pilot_scores.csv",
               "5th percentile of honest agreement")
        for tau in (0.5, 0.52):
            record(f"pilot.{column}.honest_fpr_tau{tau}", round(float((honest < tau).mean()), 3),
                   "data/mtd_defence/pilot_scores.csv", f"share of honest participations with agreement < {tau}")
    norms = p[(p.attack == "adaptive_backdoor") & p.malicious]
    norms = norms.assign(condition=norms.run.str.split("__").str[1])
    for condition, frame in norms.groupby("condition"):
        record(f"pilot.adaptive.{condition}.attacker_norm_over_T_median",
               round(float(frame["norm_over_threshold"].median()), 3), "data/mtd_defence/pilot_scores.csv",
               f"median norm / recomputed lower-median threshold of adaptive attackers in E2 {condition} runs "
               f"(n={len(frame)}, range {frame['norm_over_threshold'].min():.2f}-{frame['norm_over_threshold'].max():.2f})")
    record("pilot.runs", int(p.run.nunique()), "data/mtd_defence/pilot_scores.csv", "runs scored")
    record("pilot.participations", len(p), "data/mtd_defence/pilot_scores.csv", "client participations scored")
    multi = p.drop_duplicates(["run", "round"])
    record("pilot.cohort_rounds", len(multi), "data/mtd_defence/pilot_scores.csv", "distinct (run, round) cohorts")


# ---------------------------------------------------------------- MTD-defence studies
def mtd_studies():
    m1 = pd.read_csv(DATA / "mtd_defence/m1_runs.csv")
    m2 = pd.read_csv(DATA / "mtd_defence/m2_runs.csv")
    m2b = pd.read_csv(DATA / "mtd_defence/m2b_runs.csv")
    base = pd.concat([m1[m1.condition == "reference_defence"], m2b])
    for attack in ("adaptive_backdoor", "evasive_backdoor", "label_flip"):
        vals = base[base.attack == attack].sort_values("seed")
        record(f"m2.baseline_norm_only.{attack}.asr_mean", round(float(vals.asr.mean()), 3),
               "data/mtd_defence/m1_runs.csv + m2b_runs.csv", f"seeds {list(vals.seed)}")
        record(f"m2.baseline_norm_only.{attack}.rejection_tpr_mean", round(float(vals.rejection_tpr.mean()), 3),
               "data/mtd_defence/m1_runs.csv + m2b_runs.csv", "mean over 3 seeds")
    for (cond, attack), frame in m1.groupby(["condition", "attack"]):
        record(f"m1.{cond}.{attack}.asr_mean", round(float(frame.asr.mean()), 3), "data/mtd_defence/m1_runs.csv", "mean over 2 seeds")
        record(f"m1.{cond}.{attack}.rejection_tpr_mean", round(float(frame.rejection_tpr.mean()), 3), "data/mtd_defence/m1_runs.csv", "mean over 2 seeds")
    for label, frame in (("baseline_norm_only", base), ("reference_direction_secret_t52", m2[m2.condition == "reference_direction_secret_t52"])):
        adaptive = frame[frame.attack == "adaptive_backdoor"].asr
        record(f"m2.{label}.adaptive_backdoor.asr_seed_min", round(float(adaptive.min()), 3), "data/mtd_defence/m1/m2/m2b runs", "smallest per-seed ASR")
        record(f"m2.{label}.adaptive_backdoor.asr_seed_max", round(float(adaptive.max()), 3), "data/mtd_defence/m1/m2/m2b runs", "largest per-seed ASR")
    for (cond, attack), frame in m2.groupby(["condition", "attack"]):
        record(f"m2.{cond}.{attack}.asr_mean", round(float(frame.asr.mean()), 3), "data/mtd_defence/m2_runs.csv", "mean over 3 seeds")
        record(f"m2.{cond}.{attack}.rejection_tpr_mean", round(float(frame.rejection_tpr.mean()), 3), "data/mtd_defence/m2_runs.csv", "mean over 3 seeds")
        record(f"m2.{cond}.{attack}.direction_fpr_mean", round(float(frame.direction_fpr.mean()), 3), "data/mtd_defence/m2_runs.csv", "mean over 3 seeds")
    p3 = pd.read_csv(DATA / "mtd_defence/p3_runs.csv")
    reported = pd.read_csv(DATA / "mtd_defence/p3_paired_differences.csv")
    full = "reference_direction_secret_mtd_t52"
    for attack, frame in p3.groupby("attack"):
        table = frame.pivot_table(index="seed", columns="condition", values="asr")
        for cond in table.columns:
            record(f"p3.{cond}.{attack}.asr_mean", round(float(table[cond].mean()), 3), "data/mtd_defence/p3_runs.csv", "mean over 5 seeds")
        acc = frame.pivot_table(index="seed", columns="condition", values="accuracy")
        for cond in acc.columns:
            record(f"p3.{cond}.{attack}.accuracy_mean", round(float(acc[cond].mean()), 3), "data/mtd_defence/p3_runs.csv", "mean over 5 seeds")
        for other in [c for c in table.columns if c != full]:
            diff = (table[full] - table[other]).dropna()
            rep = reported[(reported.attack == attack) & (reported.versus == other)]
            record(f"p3.diff.{attack}.vs.{other}", round(float(diff.mean()), 3), "data/mtd_defence/p3_runs.csv",
                   "mean paired difference (full minus other)",
                   float(rep.mean_difference.iloc[0]) if not rep.empty else None)
            record(f"p3.signs.{attack}.vs.{other}", f"{int((diff < 0).sum())}/{int((diff > 0).sum())}",
                   "data/mtd_defence/p3_runs.csv", "seeds with lower / higher ASR for the full combination")
    exposure = p3[p3.condition.str.contains("mtd")].groupby(["attack", "seed", "condition"]).malicious_participations.first().unstack()
    same = bool((exposure.nunique(axis=1) == 1).all())
    record("p3.mtd_conditions_identical_exposure", int(same), "data/mtd_defence/p3_runs.csv",
           "1 if both MTD conditions had identical attacker participations in every (attack, seed)")
    f1 = pd.read_csv(DATA / "mtd_defence/f1_runs.csv")
    for attack, frame in f1.groupby("attack"):
        record(f"f1.{attack}.asr_mean", round(float(frame.asr.mean()), 3), "data/mtd_defence/f1_runs.csv", "mean over 3 seeds")
        record(f"f1.{attack}.asr_min", round(float(frame.asr.min()), 3), "data/mtd_defence/f1_runs.csv", "min over seeds")
        record(f"f1.{attack}.asr_max", round(float(frame.asr.max()), 3), "data/mtd_defence/f1_runs.csv", "max over seeds")
        record(f"f1.{attack}.accuracy_mean", round(float(frame.accuracy.mean()), 3), "data/mtd_defence/f1_runs.csv", "mean over 3 seeds")
        record(f"f1.{attack}.rejection_tpr_mean", round(float(frame.rejection_tpr.mean()), 3), "data/mtd_defence/f1_runs.csv", "mean over 3 seeds")
        record(f"f1.{attack}.rejection_fpr_mean", round(float(frame.rejection_fpr.mean()), 3), "data/mtd_defence/f1_runs.csv", "mean over 3 seeds")
    m3 = pd.read_csv(DATA / "mtd_defence/m3_runs.csv")
    for (cond, attack), frame in m3.groupby(["condition", "attack"]):
        record(f"m3.{cond}.{attack}.asr_mean", round(float(frame.asr.mean()), 3), "data/mtd_defence/m3_runs.csv", "mean over 3 seeds")


# ---------------------------------------------------------------- other evidence
def other():
    pow2 = pd.read_csv(DATA / "sum_only/pow2_vs_fedavg.csv")
    for variant, frame in pow2.groupby("variant"):
        for verdict, count in frame.verdict.value_counts().items():
            record(f"sum_only.{variant}.{verdict}", int(count), "data/sum_only/pow2_vs_fedavg.csv", "runs per verdict")
    original = pow2[pow2.variant.str.contains("10\\^6")]
    record("sum_only.original.max_abs_accuracy_difference", float(original.max_abs_accuracy_difference.max()),
           "data/sum_only/pow2_vs_fedavg.csv", "largest per-run max |accuracy difference| vs FedAvg at S=10^6")
    bench = json.loads((DATA / "mtd_defence/direction_benchmark.json").read_text())
    groups = {}
    for row in bench:
        label = row["scenario"].split("_")[1]
        stats = row["party_statistics"][0]
        groups.setdefault(label, []).append((stats["protocol_seconds"], stats["global_data_sent_mb"], row["end_to_end_seconds"], row["bit_exact"]))
    for label, values in groups.items():
        arr = np.array([v[:3] for v in values], dtype=float)
        record(f"direction_bench.{label}.protocol_seconds", round(float(arr[:, 0].mean()), 1), "data/mtd_defence/direction_benchmark.json", "mean of 2 repetitions (party 0)")
        record(f"direction_bench.{label}.traffic_gb", round(float(arr[:, 1].mean()) / 1000, 2), "data/mtd_defence/direction_benchmark.json", "mean global data sent, GB")
        record(f"direction_bench.{label}.end_to_end_seconds", round(float(arr[:, 2].mean()), 1), "data/mtd_defence/direction_benchmark.json", "mean of 2 repetitions")
        record(f"direction_bench.{label}.bit_exact", int(all(v[3] for v in values)), "data/mtd_defence/direction_benchmark.json", "1 if every repetition matched the reference")
    for name, path in (("v13", "validation/scenario_summary_v13.csv"), ("v20", "mtd_defence/scenario_summary_v20.csv")):
        frame = pd.read_csv(DATA / path)
        exact = frame.mpc_matches_reference_exactly.astype(str).str.lower().eq("true").sum()
        record(f"validation.{name}.bit_exact", f"{exact}/{len(frame)}", f"data/{path}", "scenarios whose MPC output equals the reference exactly")
    leak = pd.read_csv(DATA / "leakage/leakage_raw.csv")
    fc = leak[leak.attack == "fc_input"]
    for (state, view, batch), frame in fc.groupby(["model_state", "view", "batch_size"]):
        record(f"e6.fc_input.{state}.{view}.B{batch}.share_ssim_ge_0.9", round(float((frame.ssim >= 0.9).mean()), 2),
               "data/leakage/leakage_raw.csv", "share of target images with SSIM >= 0.9")
    opt = leak[leak.attack == "optimisation"]
    record("e6.optimisation.max_ssim", round(float(opt.ssim.max()), 3), "data/leakage/leakage_raw.csv", "maximum SSIM over all trials and views")
    exposure = pd.read_csv(DATA / "mtd_exposure/exposure_summary_R10.csv")
    hits = exposure[exposure.metric.str.contains("hit")]
    for _, row in hits.iterrows():
        record(f"e3mc.R10.b{row.budget}.{row.schedule}.{row.adversary}.{row.metric}", round(float(row["mean"]), 3),
               "data/mtd_exposure/exposure_summary_R10.csv", "mean over 200 trials")
    br = pd.read_csv(DATA / "benchmarks/benchmark_results.csv")
    ok = br[br.status == "completed"]
    record("bench.attempts", len(br), "data/benchmarks/benchmark_results.csv", "benchmark attempts")
    record("bench.completed", len(ok), "data/benchmarks/benchmark_results.csv", "completed attempts")


# ---------------------------------------------------------------- numbers of Chapter 6 beyond the tables
def _ids(value):
    if isinstance(value, str) and value.strip().startswith("["):
        return set(json.loads(value))
    return set()


def supplementary():
    """Attacker influence, clipping, reference errors and benchmark costs quoted in the text."""
    rounds = pd.read_csv(DATA / "core/all_rounds.csv", low_memory=False)
    summary = pd.read_csv(DATA / "core/summary_by_condition.csv")
    trained = rounds[rounds["round"] >= 1]
    # malicious share of the applied aggregate: mean over seeds of the per-run mean over rounds
    for cond in ("baseline", "smpc_clip", "smpc_defence_mtd"):
        for attack in ("label_flip", "sign_flip", "scaled_replacement", "random_noise", "backdoor"):
            frame = trained[(trained.study == "e1") & (trained.condition == cond) & (trained.attack == attack)]
            value = float(frame.groupby("seed").malicious_share_effective.mean().mean())
            rep = summary[(summary.study == "e1") & (summary.condition == cond) & (summary.attack == attack)
                          & (summary.metric == "mean_malicious_share_effective")]
            record(f"e1.{cond}.{attack}.malicious_share_effective", round(value, 3), "data/core/all_rounds.csv",
                   "mean over seeds of the per-run mean malicious share of the applied update",
                   float(rep["mean"].iloc[0]) if not rep.empty else None, tol=5e-4)
    # clipping of honest participations by the full framework (all 18 E1 runs)
    ff = trained[(trained.study == "e1") & (trained.condition == "smpc_defence_mtd")]
    honest_clipped = sum(len(_ids(c) - _ids(m)) for c, m in zip(ff.defence_clipped_client_ids, ff.malicious_client_ids))
    record("e1.smpc_defence_mtd.honest_clipped_share", round(honest_clipped / ff.honest_participants.sum(), 3),
           "data/core/all_rounds.csv", f"clipped honest participations / honest participations over {ff.run_id.nunique()} runs")
    record("e1.smpc_defence_mtd.honest_rejected", int(ff.rejected_false_positives.sum()), "data/core/all_rounds.csv",
           "rejected honest participations over all 18 runs")
    # adaptive attacker against the full framework (E2), per seed
    e2 = trained[(trained.study == "e2") & (trained.condition == "smpc_defence_mtd")]
    for seed, frame in e2.groupby("seed"):
        mal = frame.malicious_selected.sum()
        clipped = sum(len(_ids(c) & _ids(m)) for c, m in zip(frame.defence_clipped_client_ids, frame.malicious_client_ids))
        record(f"e2.smpc_defence_mtd.s{seed}.attacker_clipped_share", round(clipped / mal, 3), "data/core/all_rounds.csv",
               "clipped attacker participations / attacker participations")
        record(f"e2.smpc_defence_mtd.s{seed}.malicious_share_effective", round(float(frame.malicious_share_effective.mean()), 3),
               "data/core/all_rounds.csv", "mean malicious share of the applied update")
        record(f"e2.smpc_defence_mtd.s{seed}.attacker_rejected", int(frame.rejected_true_positives.sum()),
               "data/core/all_rounds.csv", "rejected attacker participations")
    # agreement of the applied update with the exact reference
    ref = pd.read_csv(DATA / "core/end_to_end_reference_check.csv")
    robust = ref[ref.path == "SPDZ2k robust program"]
    record("reference.spdz2k_robust.runs", len(robust), "data/core/end_to_end_reference_check.csv", "SPDZ2k runs of the robust program in E1-E5")
    record("reference.spdz2k_robust.rounds", int(robust.rounds_compared.sum()), "data/core/end_to_end_reference_check.csv", "rounds compared")
    record("reference.spdz2k_robust.max_abs_error", float(robust.max_abs_error.max()), "data/core/end_to_end_reference_check.csv",
           "largest absolute difference between applied update and exact reference")
    eq = pd.read_csv(DATA / "core/equivalence_checks.csv")
    same = eq[eq.comparison.str.startswith("SPDZ2k robust vs plaintext reference")]
    record("reference.spdz2k_vs_plaintext_robust.pairs", len(same), "data/core/equivalence_checks.csv", "seed pairs compared")
    record("reference.spdz2k_vs_plaintext_robust.max_difference",
           float(same[["max_abs_accuracy_difference", "max_abs_loss_difference", "max_abs_asr_difference"]].max().max()),
           "data/core/equivalence_checks.csv", "largest per-round difference in accuracy, loss and ASR")
    # cost against model size (three parties unless stated)
    bench = pd.read_csv(DATA / "benchmarks/benchmark_summary.csv")
    three = bench[bench.parties == 3]
    for variant, label in (("clip_screen_adaptive", "robust"), ("sum_only", "sum_only")):
        big = three[(three.variant == variant) & (three.dimension >= 50000) & (three.completed > 0)]
        record(f"bench.{label}.ms_per_parameter", round(float((big.protocol_seconds_max_mean / big.dimension).mean() * 1000), 2),
               "data/benchmarks/benchmark_summary.csv", "protocol seconds per parameter, mean over d = 50,000 and 100,000")
        record(f"bench.{label}.mb_per_parameter", round(float((big.global_data_sent_mb_mean / big.dimension).mean()), 3),
               "data/benchmarks/benchmark_summary.csv", "traffic per parameter, mean over d = 50,000 and 100,000")
        rows = three[three.variant == variant].sort_values("dimension")
        top = rows.iloc[-1]
        prev = rows[rows.dimension == 50000].iloc[0]
        record(f"bench.{label}.triples_per_coordinate", round(float((top.integer_triples - prev.integer_triples)
                                                                    / (top.dimension - prev.dimension)), 2),
               "data/benchmarks/benchmark_summary.csv", f"slope of compiled triples between d = 50,000 and {int(top.dimension):,}")
        record(f"bench.{label}.random_bits", int(rows.integer_bits.iloc[0]), "data/benchmarks/benchmark_summary.csv",
               "compiled random bits (independent of d)")
    robust100k = three[(three.variant == "clip_screen_adaptive") & (three.dimension == 100000)].iloc[0]
    record("bench.robust.d100000.total_seconds", round(float(robust100k.total_seconds_mean), 1),
           "data/benchmarks/benchmark_summary.csv", "end-to-end seconds of one robust round, d = 100,000")
    sum250k = three[(three.variant == "sum_only") & (three.dimension == 250000)].iloc[0]
    record("bench.sum_only.d250000.completed", int(sum250k.completed), "data/benchmarks/benchmark_summary.csv",
           "completed attempts at d = 250,000 (stopped by the round timeout)")
    two = bench[(bench.variant == "clip_screen_adaptive") & (bench.dimension == 2202)].set_index("parties")
    record("bench.robust.d2202.speedup_two_parties", round(float(two.loc[3, "protocol_seconds_max_mean"] / two.loc[2, "protocol_seconds_max_mean"]), 2),
           "data/benchmarks/benchmark_summary.csv", "protocol time three parties / two parties")
    record("bench.robust.d2202.traffic_ratio_two_parties", round(float(two.loc[2, "global_data_sent_mb_mean"] / two.loc[3, "global_data_sent_mb_mean"]), 3),
           "data/benchmarks/benchmark_summary.csv", "traffic two parties / three parties")
    robust_rows = bench[bench.variant != "sum_only"]
    record("bench.robust.completed_rounds", int(robust_rows.completed.sum()), "data/benchmarks/benchmark_summary.csv",
           "completed rounds of the robust variants (all model sizes and party counts)")
    record("bench.robust.all_bit_exact", int(robust_rows.bit_exact_all.astype(str).str.lower().eq("true").all()),
           "data/benchmarks/benchmark_summary.csv", "1 if every completed robust round matched the reference exactly")
    val = pd.read_csv(DATA / "mtd_defence/scenario_summary_v20.csv").set_index("scenario")
    for name in ("colluding_cancellation_k4", "colluding_cancellation_k8"):
        record(f"validation.{name}.aggregate_norm", round(float(val.loc[name, "aggregate_norm"]), 3),
               "data/mtd_defence/scenario_summary_v20.csv", "norm of the decoded aggregate")
        record(f"validation.{name}.output_check_passed", int(str(val.loc[name, "output_check_passed"]).lower() == "true"),
               "data/mtd_defence/scenario_summary_v20.csv", "1 if the coordinator's output check passed")
    sum2202 = three[(three.variant == "sum_only") & (three.dimension == 2202)].iloc[0]
    record("bench.sum_only.d2202.compile_seconds", round(float(sum2202.compile_seconds), 1),
           "data/benchmarks/benchmark_summary.csv", "compile time of the weighted-sum program, d = 2,202")
    # update leakage beyond the image read-out (E6)
    leak = pd.read_csv(DATA / "leakage/leakage_raw.csv")
    feat = leak[(leak.attack == "fc_features") & (leak.batch_size == 1)]
    for (view, state), frame in feat.groupby(["view", "model_state"]):
        record(f"e6.fc_features.{state}.{view}.B1.mean_cosine", round(float(frame.feature_cosine.mean()), 3),
               "data/leakage/leakage_raw.csv", "mean cosine of the best-matching recovered feature vector, one image per client")
    trials = leak.drop_duplicates(["model_state", "batch_size", "trial", "view"])
    cells = trials.groupby(["view", "model_state", "batch_size"]).label_precision.mean()
    for view in ("individual", "secure_aggregate"):
        record(f"e6.labels.{view}.precision_cell_min", round(float(cells[view].min()), 2), "data/leakage/leakage_raw.csv",
               "smallest mean label precision over (model state, B) cells")
        record(f"e6.labels.{view}.precision_cell_max", round(float(cells[view].max()), 2), "data/leakage/leakage_raw.csv",
               "largest mean label precision over (model state, B) cells")
    # exposure, accuracy and honest rejections in the paired study (P3)
    p3 = pd.read_csv(DATA / "mtd_defence/p3_runs.csv")
    jit = p3[p3.attack == "adaptive_backdoor__jit4"]
    record("p3.jit4.static.attacker_participations", int(jit[jit.condition == "reference_defence"].malicious_participations.max()),
           "data/mtd_defence/p3_runs.csv", "attacker participations over ten rounds, static cohorts (all seeds)")
    mtd = jit[jit.condition == "reference_defence_mtd"].malicious_participations
    record("p3.jit4.secret.attacker_participations_range", f"{int(mtd.min())}-{int(mtd.max())}", "data/mtd_defence/p3_runs.csv",
           "attacker participations over ten rounds, secret cohorts (range over seeds)")
    adaptive = p3[p3.attack == "adaptive_backdoor"].groupby("condition").malicious_participations.mean()
    record("p3.adaptive.secret.attacker_participations_mean", round(float(adaptive["reference_defence_mtd"]), 1),
           "data/mtd_defence/p3_runs.csv", "mean attacker participations, secret cohorts")
    record("p3.adaptive.static.attacker_participations_mean", round(float(adaptive["reference_defence"]), 1),
           "data/mtd_defence/p3_runs.csv", "mean attacker participations, static cohorts")
    clean = p3[p3.attack == "none"].groupby("condition").accuracy.mean()
    record("p3.none.accuracy_range", f"{clean.min():.3f}-{clean.max():.3f}", "data/mtd_defence/p3_runs.csv",
           "clean accuracy without attack, range of the condition means")
    record("p3.honest_rejection.max_condition_mean", round(float(p3.groupby(["condition", "attack"]).rejection_fpr.mean().max()), 3),
           "data/mtd_defence/p3_runs.csv", "largest mean honest rejection rate over (condition, attack)")
    record("p3.honest_rejection.max_single_run", round(float(p3.rejection_fpr.max()), 3), "data/mtd_defence/p3_runs.csv",
           "largest honest rejection rate of a single run")
    m3 = pd.read_csv(DATA / "mtd_defence/m3_runs.csv")
    key = ["attack", "seed"]
    a = p3[(p3.condition == "reference_defence") & p3.seed.isin([101, 102, 103])].set_index(key)[["asr", "accuracy"]].sort_index()
    b = m3[m3.condition == "reference_defence"].set_index(key)[["asr", "accuracy"]].sort_index()
    record("p3.static_norm_only_equals_m3", int(a.index.equals(b.index) and bool((a.values == b.values).all())),
           "data/mtd_defence/p3_runs.csv + m3_runs.csv", "1 if the static norm-only runs of P3 equal M3 exactly for seeds 101-103")


def main():
    OUT.mkdir(exist_ok=True)
    core_studies()
    pilot()
    mtd_studies()
    other()
    supplementary()
    with (OUT / "VERIFIED_METRICS.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["key", "value", "source", "method", "status"])
        writer.writeheader()
        writer.writerows(ROWS)
    (OUT / "VERIFICATION_LOG.txt").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    differs = [r for r in ROWS if r["status"].startswith("DIFFERS")]
    print(f"{len(ROWS)} values recomputed; {len(differs)} differ from the reported value")
    for r in differs:
        print("  ", r["key"], r["value"], r["status"])


if __name__ == "__main__":
    main()
