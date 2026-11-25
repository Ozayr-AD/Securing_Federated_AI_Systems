"""Thesis tables generated from the copied evidence (data/) as pandoc Markdown.

    python research_output/final_thesis/tools/make_tables.py

Each table is written to build/tables/<name>.md; these are the tables printed in
the thesis, so no number in them is typed by hand.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "data"
OUT = ROOT / "build" / "tables"
T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571}
LABEL = {"baseline": "FedAvg (no defence)", "mtd_only": "FedAvg + MTD", "smpc_only": "SPDZ2k sum only",
         "smpc_mtd": "SPDZ2k sum only + MTD", "smpc_clip": "SPDZ2k + static clipping (τ = 4)",
         "smpc_defence_mtd": "**Full framework** (SPDZ2k + clip/screen + MTD)", "smpc_defence": "SPDZ2k + clip/screen, static cohort",
         "smpc_screen": "SPDZ2k + screening only", "plaintext_robust": "Plaintext detector (no SMPC)",
         "reference_defence": "Norm defence only", "reference_defence_mtd": "Secret MTD, norm defence only",
         "reference_direction_secret_t52": "Static cohort + secret screen",
         "reference_direction_secret_mtd_t52": "**Secret MTD + secret screen**",
         "reference_direction_all_t52": "+ screen, all coordinates", "reference_direction_public_t52": "+ screen, public 25 % subset",
         "reference_direction_secret10_t52": "+ screen, secret 10 % subset", "smpc_direction_mtd": "Final framework in SPDZ2k"}
ATTACK = {"none": "No attack", "label_flip": "Label flip", "sign_flip": "Sign flip", "scaled_replacement": "Scaled replacement",
          "random_noise": "Gaussian noise", "backdoor": "Backdoor", "adaptive_backdoor": "Adaptive backdoor",
          "evasive_backdoor": "Evasive backdoor", "adaptive_backdoor__jit4": "Just-in-time (4 corrupted)"}


def write(name: str, text: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.md").write_text(text.strip() + "\n", encoding="utf-8")


def table(header, rows, caption, align=None, widths=None):
    """Pipe table; `widths` are relative column widths (pandoc reads them from the dash counts)."""
    align = align or ["---"] + ["---:"] * (len(header) - 1)
    if widths:
        align = [("-" * (4 * w - 1) + ":") if a.endswith(":") else "-" * (4 * w) for a, w in zip(align, widths)]
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join(align) + "|"]
    lines += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(lines) + f"\n\nTable: {caption}\n"


def ci(values):
    v = np.asarray(values, dtype=float)
    if len(v) < 2:
        return float(v.mean()), float("nan")
    return float(v.mean()), float(T975[len(v) - 1] * v.std(ddof=1) / math.sqrt(len(v)))


def fmt(mean, half=None, digits=3):
    if half is None or (isinstance(half, float) and math.isnan(half)):
        return f"{mean:.{digits}f}"
    return f"{mean:.{digits}f} ± {half:.{digits}f}"


def per_run(rounds, study, condition, attack):
    f = rounds[(rounds.study == study) & (rounds.condition == condition) & (rounds.attack == attack) & (rounds["round"] >= 1)]
    out = []
    for seed, run in f.sort_values("round").groupby("seed"):
        out.append({"seed": seed, "acc": run.global_accuracy.tail(3).mean(), "asr": run.backdoor_asr.iloc[-1],
                    "aborted": str(run.run_status.iloc[-1]) == "aborted" if "run_status" in run else False,
                    "rounds": int(run["round"].max())})
    return pd.DataFrame(out)


def main():
    rounds = pd.read_csv(D / "core/all_rounds.csv")
    pow2 = pd.read_csv(D / "sum_only/pow2_all_rounds.csv")

    # ---------------- E1 core comparison (sum-only rows: S = 2^40 rerun)
    attacks = ["none", "label_flip", "sign_flip", "scaled_replacement", "random_noise", "backdoor"]
    rows = []
    for cond in ["baseline", "mtd_only", "smpc_only", "smpc_mtd", "smpc_clip", "smpc_defence_mtd"]:
        source = pow2 if cond in ("smpc_only", "smpc_mtd") else rounds
        cells = []
        for attack in attacks:
            runs = per_run(source, "e1", cond, attack)
            m, h = ci(runs.acc)
            mark = " †" if m < 0.2 else ""
            mark += " ‡" if runs.aborted.any() else ""
            cells.append(fmt(m, h) + mark)
        runs = per_run(source, "e1", cond, "backdoor")
        am, ah = ci(runs.asr)
        bm = runs.acc.mean()
        cells.append(fmt(am, ah) + (" ‖" if bm < 0.5 and am < 0.5 else ""))
        rows.append([LABEL[cond] + (" §" if cond in ("smpc_only", "smpc_mtd") else "")] + cells)
    write("e1_core", table(["Configuration", "No attack", "Label flip", "Sign flip", "Scaled repl.", "Noise", "Backdoor: acc.", "Backdoor: ASR"], rows,
                           "Table 6.4: E1 core comparison. Clean accuracy (mean of the last three rounds) per attack and backdoor attack "
                           "success rate (final round); mean ± half-width of the 95 % Student-t interval over seeds 101–103.",
                           widths=[4, 2, 2, 2, 2, 2, 2, 2]))

    # ---------------- detection by the full framework
    summary = pd.read_csv(D / "core/summary_by_condition.csv")
    det = []
    for attack in ["sign_flip", "scaled_replacement", "backdoor", "random_noise", "label_flip", "none"]:
        get = lambda metric: summary[(summary.study == "e1") & (summary.condition == "smpc_defence_mtd") & (summary.attack == attack) & (summary.metric == metric)]["mean"]
        tpr, fpr = get("rejection_tpr"), get("rejection_fpr")
        det.append([ATTACK[attack], "–" if tpr.empty or pd.isna(tpr.iloc[0]) else f"{tpr.iloc[0]:.2f}",
                    "–" if fpr.empty or pd.isna(fpr.iloc[0]) else f"{fpr.iloc[0]:.3f}"])
    write("e1_detection", table(["Attack", "Rejection rate of malicious participations", "Rejection rate of honest participations"], det,
                                "Table 6.5: Rejections inside SPDZ2k by the full framework (E1; mean over seeds of the per-run rates).",
                                widths=[2, 3, 3]))

    # ---------------- E2 adaptive attacker
    rows = []
    for cond in ["baseline", "smpc_clip", "plaintext_robust", "smpc_defence_mtd"]:
        runs = per_run(rounds, "e2", cond, "adaptive_backdoor")
        m, h = ci(runs.asr)
        rows.append([LABEL[cond], ", ".join(f"{v:.3f}" for v in runs.sort_values("seed").asr), fmt(m, h), f"{runs.acc.mean():.3f}"])
    write("e2_adaptive", table(["Defence", "Final ASR per seed (101, 102, 103)", "Mean ± CI", "Clean accuracy"], rows,
                               "Table 6.6: E2, adaptive backdoor that scales its update to 0.95 × the published threshold.",
                               widths=[4, 4, 3, 2]))

    # ---------------- E3 schedule predictability
    rows = []
    for sched in ["static", "deterministic", "secret"]:
        for adv in ["predictive", "just_in_time"]:
            runs = per_run(rounds, "e3", "baseline", f"backdoor__{sched}__{adv}")
            f = rounds[(rounds.study == "e3") & (rounds.attack == f"backdoor__{sched}__{adv}") & (rounds["round"] >= 1)]
            mal = f.groupby("seed").malicious_selected.mean()
            mm, mh = ci(mal)
            am, ah = ci(runs.acc)
            sm, sh = ci(runs.asr)
            asr = fmt(sm, sh, 2) if am >= 0.2 else "(model destroyed)"
            rows.append([sched.capitalize(), adv.replace("_", "-"), fmt(mm, mh, 2), fmt(am, ah), asr])
    write("e3_mtd", table(["Schedule", "Adversary", "Malicious participants / round", "Clean accuracy", "Final ASR"], rows,
                          "Table 6.7: E3, schedule-aware adversaries against FedAvg (budget 2, ×4 backdoor, three seeds).",
                          widths=[2, 2, 3, 3, 3]))

    # ---------------- validation scenarios (20)
    val = pd.read_csv(D / "mtd_defence/scenario_summary_v20.csv")
    rows = []
    for _, r in val.iterrows():
        rows.append([r.scenario.replace("_", " "), r["mode"], r.threshold, int(r.clients), int(r.dimension),
                     "yes" if str(r.mpc_matches_reference_exactly).lower() == "true" else "no",
                     str(r.accepted).replace("[", "").replace("]", ""),
                     "pass" if str(r.output_check_passed).lower() == "true" else "fail"])
    write("validation", table(["Scenario", "Mode", "Threshold", "K", "d", "Bit-exact", "Accepted", "Output check"], rows,
                              "Table 6.3: SPDZ2k validation scenarios (three parties): every revealed value compared with the exact "
                              "plaintext reference. The last seven scenarios exercise the direction screen.",
                              align=["---", "---", "---", "---:", "---:", "---", "---", "---"],
                              widths=[5, 2, 2, 1, 2, 2, 3, 2]))

    # ---------------- M2
    m1 = pd.read_csv(D / "mtd_defence/m1_runs.csv")
    m2 = pd.read_csv(D / "mtd_defence/m2_runs.csv")
    m2b = pd.read_csv(D / "mtd_defence/m2b_runs.csv")
    base = pd.concat([m1[m1.condition == "reference_defence"], m2b])
    rows = []
    spec = [("reference_defence", base), ("reference_direction_all_t52", m2), ("reference_direction_public_t52", m2),
            ("reference_direction_secret_t52", m2), ("reference_direction_secret10_t52", m2)]
    for cond, frame in spec:
        f = frame[frame.condition == cond] if cond != "reference_defence" else frame
        cell = lambda a, col: f"{f[f.attack == a][col].mean():.3f}"
        rows.append([LABEL[cond], cell("adaptive_backdoor", "asr"), cell("evasive_backdoor", "asr"),
                     cell("label_flip", "rejection_tpr"), cell("none", "rejection_fpr")])
    write("m2", table(["Condition (τ = 0.52, static cohorts of 4)", "Adaptive backdoor ASR", "Evasive backdoor ASR",
                       "Label flip: rejection rate", "No attack: honest rejection rate"], rows,
                      "Table 6.8: M2, direction-screen subset types (means over seeds 101–103; plaintext execution of the in-MPC algorithm).",
                      widths=[4, 2, 2, 2, 2]))

    # ---------------- P3 paired
    p3 = pd.read_csv(D / "mtd_defence/p3_runs.csv")
    conds = ["reference_defence", "reference_direction_secret_t52", "reference_defence_mtd", "reference_direction_secret_mtd_t52"]
    rows = []
    for attack in ["adaptive_backdoor", "evasive_backdoor", "adaptive_backdoor__jit4", "none"]:
        f = p3[p3.attack == attack]
        rows.append([ATTACK[attack]] + [f"{f[f.condition == c].asr.mean():.3f}" for c in conds])
    write("p3", table(["Attack (cohorts of 7, 5 seeds)", "Static, norm only", "Static + screen", "Secret MTD, norm only", "Secret MTD + screen"], rows,
                      "Table 6.9: P3, mean final-round backdoor ASR with paired secrets (identical secret cohorts and subsets within a seed).",
                      widths=[3, 2, 2, 2, 2]))
    diff = pd.read_csv(D / "mtd_defence/p3_paired_differences.csv")
    rows = []
    for attack in ["adaptive_backdoor", "evasive_backdoor", "adaptive_backdoor__jit4"]:
        cells = []
        for other in ["reference_defence", "reference_direction_secret_t52", "reference_defence_mtd"]:
            r = diff[(diff.attack == attack) & (diff.versus == other)].iloc[0]
            cells.append(f"{r.mean_difference:+.3f} ({int(r.seeds_full_lower)}/{int(r.seeds_full_higher)})")
        rows.append([ATTACK[attack]] + cells)
    write("p3_diff", table(["Attack", "vs static, norm only", "vs static + screen", "vs secret MTD, norm only"], rows,
                           "Table 6.10: P3, paired differences of the full combination (secret MTD + secret screen) to each other condition: "
                           "mean ASR difference over five seeds, and in brackets the number of seeds with lower / higher ASR (the rest tied).",
                           widths=[3, 2, 2, 2]))

    # ---------------- F1
    f1 = pd.read_csv(D / "mtd_defence/f1_runs.csv")
    rows = []
    for attack in ["none", "label_flip", "adaptive_backdoor", "evasive_backdoor", "adaptive_backdoor__jit4"]:
        f = f1[f1.attack == attack]
        rows.append([ATTACK[attack], f"{f.asr.mean():.3f} ({f.asr.min():.2f}–{f.asr.max():.2f})", f"{f.accuracy.mean():.3f}",
                     "–" if attack == "none" else f"{f.rejection_tpr.mean():.2f}", f"{f.rejection_fpr.mean():.3f}"])
    write("f1", table(["Attack", "Backdoor ASR (min–max)", "Clean accuracy", "Attackers rejected", "Honest rejected"], rows,
                      "Table 6.11: F1, the final framework executed in SPDZ2k (cohorts of seven, three seeds).",
                      widths=[3, 3, 2, 2, 2]))

    # ---------------- overhead
    e1 = rounds[(rounds.study == "e1") & (rounds.attack == "none") & (rounds["round"] >= 1)]
    rows = []
    for cond in ["baseline", "smpc_only", "smpc_clip", "smpc_defence_mtd"]:
        f = e1[e1.condition == cond]
        t = f.round_seconds.mean()
        p = f.mpc_protocol_seconds_max.mean() if f.mpc_protocol_seconds_max.notna().any() else float("nan")
        mb = f.mpc_global_data_sent_mb.mean() if f.mpc_global_data_sent_mb.notna().any() else float("nan")
        rows.append([LABEL[cond], f"{t:.1f}", f"{t / e1[e1.condition == 'baseline'].round_seconds.mean():.1f}×",
                     "–" if math.isnan(p) else f"{p:.1f}", "–" if math.isnan(mb) else f"{mb / 1000:.2f}"])
    write("overhead", table(["Configuration", "Round time (s)", "vs FedAvg", "Protocol time (s)", "Traffic (GB)"], rows,
                            "Table 6.12: Mean cost per training round without attack (E1; 2,202 parameters, K = 4, three parties on one host).",
                            widths=[5, 2, 2, 2, 2]))
    bench = json.loads((D / "mtd_defence/direction_benchmark.json").read_text())
    groups = {}
    for r in bench:
        key = r["scenario"].split("_")[1]
        st = r["party_statistics"][0]
        groups.setdefault(key, []).append((st["protocol_seconds"], st["global_data_sent_mb"] / 1000, r["end_to_end_seconds"]))
    rows = []
    for key, label in (("none", "Norm defence only"), ("10pct", "+ direction screen, 10 % (220 coordinates)"),
                       ("25pct", "+ direction screen, 25 % (550 coordinates)")):
        a = np.array(groups[key])
        rows.append([label, f"{a[:, 0].mean():.1f}", f"{a[:, 1].mean():.1f}", f"{a[:, 2].mean():.1f}"])
    write("direction_cost", table(["Robust program, d = 2,202, K = 4", "Protocol time (s)", "Traffic (GB)", "End to end (s)"], rows,
                                  "Table 6.13: Cost of the direction screen in SPDZ2k (two repetitions each, all bit-exact).",
                                  widths=[5, 2, 2, 2]))

    # ---------------- E6
    leak = pd.read_csv(D / "leakage/leakage_raw.csv")
    fc = leak[leak.attack == "fc_input"]
    rows = []
    for b in [1, 2, 4, 8]:
        cells = []
        for state in ["initial", "trained"]:
            for view in ["individual", "secure_aggregate"]:
                f = fc[(fc.batch_size == b) & (fc.model_state == state) & (fc.view == view)]
                cells.append(f"{(f.ssim >= 0.9).mean():.2f} ({f.ssim.mean():.3f})")
        rows.append([str(b)] + cells)
    write("e6", table(["B", "FedAvg view, untrained", "SPDZ2k view, untrained", "FedAvg view, trained", "SPDZ2k view, trained"], rows,
                      "Table 6.14: E6, share of the target client's images recovered with SSIM ≥ 0.9 (mean SSIM in brackets) by "
                      "the analytic read-out through the first fully connected layer of the probe MLP.",
                      widths=[1, 3, 3, 3, 3]))

    # ---------------- Appendix A: per-seed tables
    rows = []
    for attack in ["none", "label_flip", "adaptive_backdoor", "evasive_backdoor", "adaptive_backdoor__jit4"]:
        f = f1[f1.attack == attack].sort_values("seed")
        rows.append([ATTACK[attack], ", ".join(f"{v:.3f}" for v in f.asr), ", ".join(f"{v:.3f}" for v in f.accuracy),
                     ", ".join(f"{v:.2f}" for v in f.rejection_tpr) if attack != "none" else "–"])
    write("appendix_f1", table(["Attack", "Final ASR per seed (101–103)", "Accuracy per seed", "Attackers rejected per seed"], rows,
                               "Table A.1: F1 per-seed results (SPDZ2k).", align=["---", "---", "---", "---"], widths=[2, 3, 3, 3]))
    print("tables:", sorted(p.name for p in OUT.glob("*.md")))


if __name__ == "__main__":
    main()
