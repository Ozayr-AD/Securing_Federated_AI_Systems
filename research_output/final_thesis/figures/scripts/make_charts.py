"""Evidence charts for the thesis, generated only from the copies in data/.

    python research_output/final_thesis/figures/scripts/make_charts.py

Each chart is saved as figures/png/<name>.png (300 dpi) and figures/pdf/<name>.pdf
and registered with its sources and transformation in
figures/provenance_charts.json (input to FIGURE_DATA_PROVENANCE.md).
No value is interpolated, smoothed or invented; error bands are the 95 %
Student-t intervals computed by the original analysis or by this script from
the per-seed values it plots.
"""
from __future__ import annotations

import json
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import style as S
from style import BLUE, ORANGE, AQUA, YELLOW, VIOLET, MAGENTA, DARK_BLUE, INK, INK2, MUTED, CONFIG

S.apply_style()
D = S.DATA
ROUNDS = pd.read_csv(D / "core/all_rounds.csv")
ROUNDS = ROUNDS[ROUNDS["round"] >= 1].sort_values(["study", "condition", "attack", "seed", "round"])


def per_run(study, condition, attack):
    frame = ROUNDS[(ROUNDS.study == study) & (ROUNDS.condition == condition) & (ROUNDS.attack == attack)]
    out = []
    for seed, run in frame.groupby("seed"):
        out.append({"seed": seed, "last3": run.global_accuracy.tail(3).mean(),
                    "asr": run.backdoor_asr.iloc[-1], "malicious": run.malicious_selected.mean()})
    return pd.DataFrame(out)


def dot_rows(ax, rows, value, xlabel, ref=None, ref_label=None, xlim=(0, 1)):
    """Horizontal dot plot: per-seed points and a mean tick for each labelled row."""
    for i, (label, colour, frame) in enumerate(rows):
        y = len(rows) - 1 - i
        vals = frame[value].to_numpy()
        ax.scatter(vals, np.full(len(vals), y), s=22, color=colour, alpha=0.9, zorder=3, edgecolor="white", linewidth=0.5)
        mean = float(np.mean(vals))
        ax.plot([mean, mean], [y - 0.28, y + 0.28], color=INK, linewidth=1.4, zorder=4)
        # mean label beside the row's points (right of them, or left if they reach the right edge)
        span = xlim[1] - xlim[0]
        right = max(vals.max(), mean)
        if right < xlim[0] + 0.78 * span:
            ax.annotate(f"mean {mean:.3f}", (right, y), xytext=(6, 0), textcoords="offset points",
                        ha="left", va="center", fontsize=7, color=INK2)
        else:
            ax.annotate(f"mean {mean:.3f}", (min(vals.min(), mean), y), xytext=(-6, 0), textcoords="offset points",
                        ha="right", va="center", fontsize=7, color=INK2)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows][::-1])
    ax.set_xlim(*xlim)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_xlabel(xlabel)
    ax.grid(axis="y", visible=False)
    if ref is not None:
        ax.axvline(ref, color=MUTED, linestyle=":", linewidth=1)
        ax.annotate(ref_label, (ref, len(rows) - 0.4), xytext=(3, -1), textcoords="offset points", fontsize=7,
                    color=INK2, va="top")


# ------------------------------------------------------------------ E1 trajectories
def e1_backdoor_rounds():
    acc = pd.read_csv(D / "core/accuracy_over_rounds.csv")
    sel = acc[(acc.study == "e1") & (acc.attack == "backdoor")]
    fig, axes = plt.subplots(1, 2, figsize=(S.TEXT_WIDTH_IN, 2.6), sharex=True)
    for ax, metric, ylabel in ((axes[0], "global_accuracy", "Clean test accuracy"),
                               (axes[1], "backdoor_asr", "Backdoor attack success rate")):
        for cond in ("baseline", "smpc_clip", "smpc_defence_mtd"):
            label, colour = CONFIG[cond]
            f = sel[(sel.condition == cond) & (sel.metric == metric)].sort_values("round")
            f = f[f["round"] >= 1]
            ax.plot(f["round"], f["mean"], color=colour, label=label)
            ax.fill_between(f["round"], f.ci95_lower.clip(0, 1), f.ci95_upper.clip(0, 1), color=colour, alpha=0.13, linewidth=0)
            if metric == "backdoor_asr":
                S.end_label(ax, f["round"].iloc[-1], f["mean"].iloc[-1], f"{f['mean'].iloc[-1]:.3f}")
        ax.set_ylabel(ylabel)
        ax.set_xlabel("Training round")
        ax.set_ylim(0, 1)
        ax.set_xticks(range(1, 11))
    axes[0].set_title("(a) Clean accuracy", loc="left")
    axes[1].set_title("(b) Backdoor success", loc="left")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.08))
    fig.tight_layout()
    S.save(fig, "e1_backdoor_rounds", title="E1: training under the boosted backdoor",
           caption="Clean accuracy (a) and backdoor attack success rate (b) per round under the ×4 boosted backdoor "
                   "(E1, three seeds). Lines are means; bands are 95 % Student-t intervals over seeds.",
           sources=["data/core/accuracy_over_rounds.csv"],
           transform="rows study=e1, attack=backdoor, metric in {global_accuracy, backdoor_asr}, rounds 1-10; "
                     "mean and ci95 columns plotted as recorded (CI clipped to [0,1])")


# ------------------------------------------------------------------ boosted vs adaptive backdoor
def backdoor_asr_by_defence():
    clean = per_run("e1", "baseline", "none").asr.mean()
    boosted = [(CONFIG[c][0], CONFIG[c][1], per_run(st, c, "backdoor")) for st, c in (
        ("e1", "baseline"), ("e1", "smpc_clip"), ("e1x", "plaintext_robust"), ("e1x", "smpc_defence"), ("e1", "smpc_defence_mtd"))]
    adaptive = [(CONFIG[c][0], CONFIG[c][1], per_run("e2", c, "adaptive_backdoor")) for c in (
        "baseline", "smpc_clip", "plaintext_robust", "smpc_defence_mtd")]
    fig, axes = plt.subplots(2, 1, figsize=(S.TEXT_WIDTH_IN, 4.2))
    dot_rows(axes[0], boosted, "asr", "Final-round backdoor ASR", clean, f"clean model {clean:.3f}")
    axes[0].set_title("(a) Boosted backdoor, ×4 (E1, E1x)", loc="left")
    dot_rows(axes[1], adaptive, "asr", "Final-round backdoor ASR", clean, f"clean model {clean:.3f}")
    axes[1].set_title("(b) Adaptive backdoor, 0.95 × threshold (E2)", loc="left")
    fig.tight_layout()
    S.save(fig, "backdoor_asr_by_defence", title="Backdoor success by defence, boosted vs adaptive attacker",
           caption="Final-round backdoor attack success rate per seed (dots) and mean (tick) for each defence. "
                   "(a) Boosted backdoor, E1/E1x; (b) adaptive backdoor that scales its update to 0.95 × the "
                   "published threshold, E2. The dotted line is the clean model's natural trigger response (E1, no attack).",
           sources=["data/core/all_rounds.csv"],
           transform="per run: backdoor_asr of the last completed round; studies e1/e1x (attack backdoor) and e2 "
                     "(adaptive_backdoor); reference = mean final ASR of e1 baseline without attack")


# ------------------------------------------------------------------ E3 schedule predictability
def e3_predictability():
    schedules = ["static", "deterministic", "secret"]
    adversaries = [("predictive", BLUE, "Predictive (fixed set)"), ("just_in_time", ORANGE, "Just-in-time")]
    fig, axes = plt.subplots(1, 2, figsize=(S.TEXT_WIDTH_IN, 2.6))
    for ax, value, ylabel in ((axes[0], "malicious", "Malicious participants per round"),
                              (axes[1], "last3", "Clean accuracy (last 3 rounds)")):
        for j, (adv, colour, label) in enumerate(adversaries):
            means = []
            for i, sched in enumerate(schedules):
                frame = per_run("e3", "baseline", f"backdoor__{sched}__{adv}")
                x = i + (j - 0.5) * 0.22
                ax.scatter(np.full(len(frame), x), frame[value], s=18, color=colour, alpha=0.85, edgecolor="white", linewidth=0.5, zorder=3)
                means.append((x, frame[value].mean()))
            xs, ys = zip(*means)
            ax.plot(xs, ys, color=colour, linewidth=1.2, marker="D", markersize=4, label=label, zorder=4)
        ax.set_xticks(range(3))
        ax.set_xticklabels(["Static", "Deterministic\n(public seed)", "Secret\n(HMAC key)"])
        ax.set_ylabel(ylabel)
        ax.grid(axis="x", visible=False)
    axes[0].set_ylim(0, 2.2)
    axes[1].set_ylim(0, 1)
    axes[0].set_title("(a) Attacker exposure", loc="left")
    axes[1].set_title("(b) Model utility", loc="left")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.06))
    fig.tight_layout()
    S.save(fig, "e3_schedule_predictability", title="E3: schedule predictability in federated training",
           caption="Schedule-aware adversaries (budget 2, ×4 backdoor, FedAvg without defence, three seeds). "
                   "(a) Mean number of malicious clients per cohort; (b) clean accuracy. Dots are seeds, diamonds means.",
           sources=["data/core/all_rounds.csv"],
           transform="per run (study e3): mean of malicious_selected over rounds 1-10 and mean global_accuracy of the last three rounds")


# ------------------------------------------------------------------ E3-MC exposure
def e3mc_exposure():
    e = pd.read_csv(D / "mtd_exposure/exposure_summary_R10.csv")
    e = e[e.metric == "compromise_hit_rate"]
    advs = [("random", BLUE, "Random"), ("predictive", ORANGE, "Predictive"), ("just_in_time", AQUA, "Just-in-time")]
    schedules = ["static", "deterministic", "secret"]
    fig, axes = plt.subplots(1, 2, figsize=(S.TEXT_WIDTH_IN, 2.4), sharey=True)
    for ax, budget in zip(axes, (2, 3)):
        for j, (adv, colour, label) in enumerate(advs):
            for i, sched in enumerate(schedules):
                row = e[(e.budget == budget) & (e.schedule == sched) & (e.adversary == adv)]
                if row.empty:
                    continue
                x = i + (j - 1) * 0.22
                m, lo, hi = float(row["mean"].iloc[0]), float(row.ci95_lower.iloc[0]), float(row.ci95_upper.iloc[0])
                ax.errorbar(x, m, yerr=[[m - lo], [hi - m]], fmt="o", color=colour, markersize=5, capsize=2,
                            label=label if i == 0 else None, zorder=3)
        ax.axhline(4 / 12, color=MUTED, linestyle=":", linewidth=1)
        ax.annotate("K/N = 0.33", (2.45, 4 / 12), xytext=(0, 3), textcoords="offset points", fontsize=7, color=INK2, ha="right")
        ax.set_xticks(range(3))
        ax.set_xticklabels(["Static", "Deterministic", "Secret"])
        ax.set_title(f"({'ab'[budget - 2]}) Adversary budget b = {budget}", loc="left")
        ax.set_ylim(0, 1.08)
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("Compromise hit rate")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.07))
    fig.tight_layout()
    S.save(fig, "e3mc_exposure", title="E3-MC: compromise hit rate per schedule",
           caption="Share of compromised clients that end up in a cohort (N = 12, K = 4, R = 10 rounds, 200 Monte-Carlo trials). "
                   "Error bars are 95 % Student-t intervals over trials; the dotted line is the random baseline K/N.",
           sources=["data/mtd_exposure/exposure_summary_R10.csv"],
           transform="rows metric=compromise_hit_rate, budgets 2 and 3; mean and ci95 columns as recorded")


# ------------------------------------------------------------------ E4 sweeps
def e4_sweeps():
    fig, axes = plt.subplots(1, 3, figsize=(S.TEXT_WIDTH_IN, 2.5))
    boosts = [1, 2, 8, 16]
    for cond in ("baseline", "reference_defence"):
        label = CONFIG["baseline"][0] if cond == "baseline" else "Norm defence (plaintext execution)"
        colour = ORANGE if cond == "baseline" else DARK_BLUE
        jit = 0.9 if cond == "baseline" else 1.1          # horizontal offset of the points only (log axis)
        acc_means, asr_points = [], []
        for b in boosts:
            frame = per_run("e4", cond, f"backdoor__boost{b}")
            axes[0].scatter(np.full(len(frame), b * jit), frame.last3, s=16, color=colour, alpha=0.85, edgecolor="white", linewidth=0.5, zorder=3)
            acc_means.append(frame.last3.mean())
            for _, r in frame.iterrows():
                destroyed = r.last3 < 0.2
                axes[1].scatter(b * jit, r.asr, s=18, zorder=3, linewidth=1,
                                facecolor="white" if destroyed else colour, edgecolor=colour)
            asr_points.append(frame[frame.last3 >= 0.2].asr.mean() if (frame.last3 >= 0.2).any() else np.nan)
        axes[0].plot(boosts, acc_means, color=colour, label=label)
        valid = [(b, v) for b, v in zip(boosts, asr_points) if not math.isnan(v)]
        axes[1].plot(*zip(*valid), color=colour)
        strengths, means = [1, 2, 8], []
        for s_ in strengths:
            frame = per_run("e4", cond, f"sign_flip__str{s_}")
            axes[2].scatter(np.full(len(frame), s_ * jit), frame.last3, s=16, color=colour, alpha=0.85, edgecolor="white", linewidth=0.5, zorder=3)
            means.append(frame.last3.mean())
        axes[2].plot(strengths, means, color=colour)
    for ax in axes:
        ax.set_xscale("log", base=2)
        ax.set_ylim(0, 1.02)
    axes[0].set_xticks(boosts, [f"×{b}" for b in boosts])
    axes[1].set_xticks(boosts, [f"×{b}" for b in boosts])
    axes[2].set_xticks([1, 2, 8], ["×1", "×2", "×8"])
    axes[0].set_ylabel("Clean accuracy (last 3 rounds)")
    axes[1].set_ylabel("Final-round backdoor ASR")
    axes[2].set_ylabel("Clean accuracy (last 3 rounds)")
    axes[0].set_xlabel("Backdoor boost")
    axes[1].set_xlabel("Backdoor boost")
    axes[2].set_xlabel("Sign-flip strength")
    axes[0].set_title("(a) Backdoor: accuracy", loc="left")
    axes[1].set_title("(b) Backdoor: ASR", loc="left")
    axes[2].set_title("(c) Sign flip: accuracy", loc="left")
    axes[1].annotate("hollow: model destroyed\n(accuracy < 0.2)", (0.98, 0.5), xycoords="axes fraction", ha="right", fontsize=6.5, color=INK2)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.07))
    fig.tight_layout()
    S.save(fig, "e4_sweeps", title="E4: attack-strength sweeps",
           caption="Attack-strength sweeps (two seeds) for FedAvg and the plaintext execution of the adaptive norm defence, "
                   "which is trajectory-identical to the SPDZ2k program. Dots are seeds, lines connect means. In (b) hollow "
                   "markers are runs whose model was destroyed; the line averages only runs with a usable model.",
           sources=["data/core/all_rounds.csv"],
           transform="per run (study e4): last-three-round mean accuracy and final-round ASR; attacks backdoor__boost{1,2,8,16} and sign_flip__str{1,2,8}")


# ------------------------------------------------------------------ overhead in training
def overhead_rounds():
    conds = ["baseline", "smpc_only", "smpc_clip", "smpc_defence_mtd"]
    e1 = ROUNDS[(ROUNDS.study == "e1") & (ROUNDS.attack == "none")]
    stats = {c: e1[e1.condition == c] for c in conds}
    fig, axes = plt.subplots(1, 3, figsize=(S.TEXT_WIDTH_IN, 2.5), sharey=True)
    labels = [CONFIG[c][0].replace("Full framework: ", "Full framework\n").replace("SPDZ2k + ", "SPDZ2k +\n") for c in conds]
    for ax, column, xlabel, fmt in ((axes[0], "round_seconds", "Round wall time (s)", "{:.1f}"),
                                    (axes[1], "mpc_protocol_seconds_max", "MP-SPDZ protocol time (s)", "{:.1f}"),
                                    (axes[2], "mpc_global_data_sent_mb", "Party traffic per round (GB)", "{:.2f}")):
        for i, c in enumerate(conds):
            y = len(conds) - 1 - i
            series = stats[c][column]
            if series.notna().any():
                v = float(series.mean()) / (1000 if column.endswith("_mb") else 1)
                ax.barh(y, v, height=0.62, color=CONFIG[c][1])
                ax.annotate(fmt.format(v), (v, y), xytext=(3, 0), textcoords="offset points", va="center", fontsize=7, color=INK2)
            else:
                ax.annotate("n/a (plaintext)", (0, y), xytext=(3, 0), textcoords="offset points", va="center", fontsize=7, color=MUTED)
        ax.set_xlabel(xlabel)
        ax.grid(axis="y", visible=False)
        ax.margins(x=0.25)
    axes[0].set_yticks(range(len(conds)))
    axes[0].set_yticklabels(labels[::-1])
    fig.tight_layout()
    S.save(fig, "overhead_in_training", title="Per-round cost inside federated training",
           caption="Mean cost per training round without attack (E1, 2,202 parameters, K = 4, three SPDZ2k parties on one host; "
                   "3 runs × 10 rounds per configuration). The sum-only round includes about 8.5 s of per-round compilation.",
           sources=["data/core/all_rounds.csv"],
           transform="study e1, attack none, rounds 1-10: means of round_seconds, mpc_protocol_seconds_max and mpc_global_data_sent_mb (MB/1000)")


# ------------------------------------------------------------------ benchmark scaling
def benchmark_scaling():
    b = pd.read_csv(D / "benchmarks/benchmark_results.csv")
    b = b[(b.parties == 3) & (b["mode"] == "clip_screen") & (b.threshold == "adaptive")]
    fig, axes = plt.subplots(1, 2, figsize=(S.TEXT_WIDTH_IN, 2.6))
    for program, label, colour in (("weighted_sum", "Sum-only program", VIOLET), ("robust_aggregate", "Robust program (clip + screen)", BLUE)):
        f = b[(b.program == program) & (b.status == "completed")]
        g = f.groupby("dimension").agg(t=("protocol_seconds_max", "mean"), mb=("global_data_sent_mb", "mean")).reset_index()
        axes[0].scatter(f.dimension, f.protocol_seconds_max, s=14, color=colour, alpha=0.7, edgecolor="white", linewidth=0.4, zorder=3)
        axes[0].plot(g.dimension, g.t, color=colour, label=label)
        axes[1].plot(g.dimension, g.mb / 1000, color=colour, marker="o", markersize=3.5)
    failed = b[(b.status != "completed")]
    for _, r in failed.iterrows():
        axes[0].scatter(r.dimension, 600, marker="x", color=VIOLET, s=30, zorder=4)
    for ax in axes:
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Model parameters d")
    axes[0].axhline(600, color=MUTED, linestyle=":", linewidth=1)
    axes[0].annotate("600 s round timeout", (1000, 600), xytext=(0, 3), textcoords="offset points", fontsize=6.5, color=INK2)
    axes[0].set_ylabel("Protocol time per round (s)")
    axes[1].set_ylabel("Party traffic per round (GB)")
    axes[0].set_title("(a) Time", loc="left")
    axes[1].set_title("(b) Traffic", loc="left")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.07))
    fig.tight_layout()
    S.save(fig, "benchmark_scaling", title="SPDZ2k cost vs model size",
           caption="Isolated SPDZ2k rounds (three local parties, K = 4) for model sizes from 1,000 to 100,000 parameters. "
                   "Dots are repetitions, lines connect means; both axes are logarithmic. The cross marks the sum-only round "
                   "with 250,000 parameters, which the parties' 600 s round timeout stopped.",
           sources=["data/benchmarks/benchmark_results.csv"],
           transform="rows parties=3, mode=clip_screen, threshold=adaptive (the sum-only rows carry the same label columns); "
                     "completed rows: protocol_seconds_max and global_data_sent_mb/1000; failed row marked at the timeout")


# ------------------------------------------------------------------ direction pilot
def pilot_sign_agreement():
    p = pd.read_csv(D / "mtd_defence/pilot_scores.csv")
    p = p[p.attackers_in_cohort == 1]
    order = [("label_flip", "Label flip"), ("sign_flip", "Sign flip"), ("scaled_replacement", "Scaled replacement"),
             ("random_noise", "Gaussian noise"), ("adaptive_backdoor", "Adaptive backdoor"), ("backdoor", "Boosted backdoor")]
    col = "sign_agree_0.25_single"
    fig, ax = plt.subplots(figsize=(S.TEXT_WIDTH_IN, 3.0))
    for i, (attack, label) in enumerate(order):
        f = p[p.attack == attack]
        hon, mal = f.loc[~f.malicious, col].dropna(), f.loc[f.malicious, col].dropna()
        y = len(order) - 1 - i
        for vals, offset, colour, name in ((hon, 0.17, BLUE, "Honest clients"), (mal, -0.17, ORANGE, "Attacker")):
            ax.boxplot(vals, positions=[y + offset], orientation="horizontal", widths=0.28, patch_artist=True, showfliers=False,
                       boxprops=dict(facecolor=colour, edgecolor=colour, alpha=0.35), medianprops=dict(color=colour, linewidth=1.6),
                       whiskerprops=dict(color=colour), capprops=dict(color=colour))
        auc = float(((hon.to_numpy()[:, None] > mal.to_numpy()[None, :]).mean()
                     + 0.5 * (hon.to_numpy()[:, None] == mal.to_numpy()[None, :]).mean()))
        ax.annotate(f"AUC {auc:.2f}", (1.0, y), xytext=(4, 0), textcoords="offset points", va="center", fontsize=7.5, color=INK2,
                    annotation_clip=False)
    ax.axvline(0.52, color=INK2, linestyle="--", linewidth=1)
    ax.annotate("τ = 0.52", (0.52, len(order) - 0.45), xytext=(3, 0), textcoords="offset points", fontsize=7, color=INK2)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([o[1] for o in order][::-1])
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("Sign agreement with the majority of the other cohort members (random 25 % coordinate subset)")
    ax.grid(axis="y", visible=False)
    from matplotlib.patches import Patch
    ax.legend([Patch(facecolor=BLUE, alpha=0.35, edgecolor=BLUE), Patch(facecolor=ORANGE, alpha=0.35, edgecolor=ORANGE)],
              ["Honest clients", "Attacker"], loc="lower left", ncol=2, bbox_to_anchor=(0, 1.0))
    fig.tight_layout()
    S.save(fig, "pilot_sign_agreement", title="Pilot: sign agreement of honest and malicious updates",
           caption="Offline pilot on the recorded updates of 175 runs: sign agreement of each update with the majority of the "
                   "other cohort members on a random 25 % coordinate subset, for cohorts with exactly one attacker. Boxes span "
                   "the quartiles, whiskers 1.5 × IQR. AUC = probability that an honest update agrees more than the attacker's.",
           sources=["data/mtd_defence/pilot_scores.csv"],
           transform="rows attackers_in_cohort = 1; column sign_agree_0.25_single split by the malicious flag; AUC by pairwise comparison (ties 0.5)")


# ------------------------------------------------------------------ M2 subset types
def m2_subsets():
    m1 = pd.read_csv(D / "mtd_defence/m1_runs.csv")
    m2 = pd.read_csv(D / "mtd_defence/m2_runs.csv")
    m2b = pd.read_csv(D / "mtd_defence/m2b_runs.csv")
    base = pd.concat([m1[m1.condition == "reference_defence"], m2b])
    rows_spec = [("Norm defence only", DARK_BLUE, base, None),
                 ("+ screen, all coordinates", AQUA, m2, "reference_direction_all_t52"),
                 ("+ screen, public 25 % subset", YELLOW, m2, "reference_direction_public_t52"),
                 ("+ screen, secret 25 % subset", BLUE, m2, "reference_direction_secret_t52"),
                 ("+ screen, secret 10 % subset", VIOLET, m2, "reference_direction_secret10_t52")]
    fig, axes = plt.subplots(1, 2, figsize=(S.TEXT_WIDTH_IN, 2.9), sharey=True)
    for ax, attack, title in ((axes[0], "adaptive_backdoor", "(a) Adaptive backdoor"), (axes[1], "evasive_backdoor", "(b) Evasive backdoor")):
        rows = []
        for label, colour, frame, cond in rows_spec:
            f = frame[(frame.attack == attack) & ((frame.condition == cond) if cond else True)]
            rows.append((label, colour, f))
        dot_rows(ax, rows, "asr", "Final-round backdoor ASR", xlim=(0, 0.5))
        ax.set_title(title, loc="left")
    axes[1].set_ylabel("")
    fig.tight_layout()
    S.save(fig, "m2_subset_types", title="M2: which coordinates the direction screen checks",
           caption="Direction screen with τ = 0.52 and static cohorts of four (three seeds; plaintext execution of the in-MPC algorithm). "
                   "Dots are seeds, ticks means. The norm-only baseline combines M1 (seeds 101, 102) and M2b (seed 103).",
           sources=["data/mtd_defence/m1_runs.csv", "data/mtd_defence/m2_runs.csv", "data/mtd_defence/m2b_runs.csv"],
           transform="final-round ASR per run as recorded in the run tables (m1_summary.py)")


# ------------------------------------------------------------------ P3 paired
def p3_paired():
    p3 = pd.read_csv(D / "mtd_defence/p3_runs.csv")
    conds = [("reference_defence", "Static\nnorm", DARK_BLUE), ("reference_direction_secret_t52", "Static\n+screen", AQUA),
             ("reference_defence_mtd", "MTD\nnorm", YELLOW), ("reference_direction_secret_mtd_t52", "MTD\n+screen", BLUE)]
    attacks = [("adaptive_backdoor", "(a) Adaptive backdoor"), ("evasive_backdoor", "(b) Evasive backdoor"),
               ("adaptive_backdoor__jit4", "(c) Just-in-time (4 corrupted)")]
    fig, axes = plt.subplots(1, 3, figsize=(S.TEXT_WIDTH_IN, 2.9), sharey=True)
    for ax, (attack, title) in zip(axes, attacks):
        table = p3[p3.attack == attack].pivot_table(index="seed", columns="condition", values="asr")[[c for c, _, _ in conds]]
        for seed, row in table.iterrows():
            ax.plot(range(4), row.to_numpy(), color=MUTED, linewidth=0.7, alpha=0.7, zorder=2)
        for i, (c, _, colour) in enumerate(conds):
            ax.scatter(np.full(len(table), i), table[c], s=16, color=colour, edgecolor="white", linewidth=0.5, zorder=3)
            m = table[c].mean()
            ax.plot([i - 0.22, i + 0.22], [m, m], color=INK, linewidth=1.5, zorder=4)
            ax.annotate(f"{m:.2f}", (i + 0.22, m), xytext=(2, 0), textcoords="offset points", ha="left", va="center",
                        fontsize=7, color=INK, fontweight="bold")
        ax.set_xticks(range(4))
        ax.set_xticklabels([c[1] for c in conds], fontsize=7)
        ax.set_xlim(-0.4, 3.6)
        ax.set_title(title, loc="left")
        ax.grid(axis="x", visible=False)
        ax.set_ylim(0, 1.05)
    axes[0].set_ylabel("Final-round backdoor ASR")
    fig.tight_layout()
    S.save(fig, "p3_paired", title="P3: paired comparison of static and secret cohorts",
           caption="Paired evaluation (cohorts of seven, five seeds): within a seed all conditions share the same secret cohorts "
                   "and secret subsets. Grey lines connect the four conditions of one seed; black ticks are means.",
           sources=["data/mtd_defence/p3_runs.csv"],
           transform="final-round ASR per run as recorded; pivot by seed and condition")


# ------------------------------------------------------------------ F1 SPDZ2k final framework
def f1_framework():
    f1 = pd.read_csv(D / "mtd_defence/f1_runs.csv")
    attacks = [("none", "No attack"), ("label_flip", "Label flip"), ("adaptive_backdoor", "Adaptive backdoor"),
               ("evasive_backdoor", "Evasive backdoor"), ("adaptive_backdoor__jit4", "Just-in-time (4 corrupted)")]
    fig, axes = plt.subplots(1, 2, figsize=(S.TEXT_WIDTH_IN, 2.5), sharey=True)
    rows = [(label, BLUE, f1[f1.attack == a]) for a, label in attacks]
    dot_rows(axes[0], rows, "asr", "Final-round backdoor ASR")
    dot_rows(axes[1], rows, "accuracy", "Clean accuracy (last 3 rounds)", xlim=(0.7, 0.9))
    axes[0].set_title("(a) Backdoor success", loc="left")
    axes[1].set_title("(b) Clean accuracy", loc="left")
    fig.tight_layout()
    S.save(fig, "f1_spdz2k_framework", title="F1: final framework inside SPDZ2k",
           caption="Final framework executed in SPDZ2k (secure clip/screen, secret 25 % direction screen with τ = 0.52, secret MTD, "
                   "cohorts of seven; three seeds). Dots are seeds, ticks means.",
           sources=["data/mtd_defence/f1_runs.csv"],
           transform="final-round ASR and last-three-round accuracy per run as recorded")


# ------------------------------------------------------------------ direction screen cost
def direction_cost():
    bench = json.loads((D / "mtd_defence/direction_benchmark.json").read_text())
    groups = {}
    for row in bench:
        key = row["scenario"].split("_")[1]
        st = row["party_statistics"][0]
        groups.setdefault(key, []).append((st["protocol_seconds"], st["global_data_sent_mb"] / 1000))
    spec = [("none", "Norm defence only", DARK_BLUE), ("10pct", "+ screen, 10 % subset (220 coord.)", VIOLET),
            ("25pct", "+ screen, 25 % subset (550 coord.)", BLUE)]
    fig, axes = plt.subplots(1, 2, figsize=(S.TEXT_WIDTH_IN, 1.9), sharey=True)
    for ax, idx, xlabel in ((axes[0], 0, "Protocol time per round (s)"), (axes[1], 1, "Party traffic per round (GB)")):
        for i, (key, label, colour) in enumerate(spec):
            vals = np.array([v[idx] for v in groups[key]])
            y = len(spec) - 1 - i
            ax.barh(y, vals.mean(), height=0.6, color=colour)
            ax.scatter(vals, np.full(len(vals), y), s=10, color=INK, zorder=3)
            ax.annotate(f"{vals.mean():.1f}", (vals.mean(), y), xytext=(4, 0), textcoords="offset points", va="center", fontsize=7, color=INK2)
        ax.set_xlabel(xlabel)
        ax.grid(axis="y", visible=False)
        ax.margins(x=0.2)
    axes[0].set_yticks(range(3))
    axes[0].set_yticklabels([s[1] for s in spec][::-1])
    fig.tight_layout()
    S.save(fig, "direction_screen_cost", title="Cost of the direction screen in SPDZ2k",
           caption="One SPDZ2k round of the robust program at d = 2,202 and K = 4 (three local parties), without and with the "
                   "direction screen; two repetitions each (dots), bars are means. All rounds matched the reference bit for bit.",
           sources=["data/mtd_defence/direction_benchmark.json"],
           transform="party 0 protocol_seconds and global_data_sent_mb/1000 per repetition")


# ------------------------------------------------------------------ sum-only correction
def sum_only_correction():
    traj = {k: pd.read_csv(D / f"sum_only/scaled_replacement_{k}_results.csv") for k in
            ("baseline_s102", "smpc_only_1e6_s102", "smpc_only_2p40_s102")}
    fig, axes = plt.subplots(1, 2, figsize=(S.TEXT_WIDTH_IN, 2.5), gridspec_kw={"width_ratios": [1.5, 1]})
    ax = axes[0]
    for key, label, colour, style_ in (("baseline_s102", "FedAvg (plaintext)", ORANGE, dict(linewidth=2.2)),
                                       ("smpc_only_1e6_s102", "SPDZ2k sum only, S = 10⁶", VIOLET, dict()),
                                       ("smpc_only_2p40_s102", "SPDZ2k sum only, S = 2⁴⁰", INK, dict(linestyle="--", marker="o", markersize=3.5, markerfacecolor="white", linewidth=1))):
        f = traj[key]
        f = f[f["round"] >= 1]
        ax.plot(f["round"], f.global_accuracy, color=colour, label=label, **style_)
    ax.set_xlabel("Training round")
    ax.set_ylabel("Clean test accuracy")
    ax.set_ylim(0, 1)
    ax.set_xticks(range(1, 11))
    ax.set_title("(a) Scaled replacement, seed 102", loc="left")
    ax.legend(loc="upper right", fontsize=7)
    pw = pd.read_csv(D / "sum_only/pow2_vs_fedavg.csv")
    ax = axes[1]
    for i, (variant, label, colour) in enumerate((("S=10^6 (original)", "S = 10⁶", VIOLET), ("S=2^40 (rerun)", "S = 2⁴⁰", INK))):
        vals = pw[pw.variant == variant].max_abs_accuracy_difference.astype(float).to_numpy()
        jitter = (np.arange(len(vals)) % 6 - 2.5) * 0.04
        ax.scatter(i + jitter, vals, s=14, color=colour, facecolor="white" if colour == INK else colour, zorder=3)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["S = 10⁶\n(original)", "S = 2⁴⁰\n(rerun)"])
    ax.set_xlim(-0.6, 1.6)
    ax.set_ylabel("Max |Δ accuracy| vs FedAvg")
    ax.set_title("(b) All 18 smpc_only runs", loc="left")
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    S.save(fig, "sum_only_correction", title="Sum-only SPDZ2k against FedAvg before and after the scale correction",
           caption="(a) Accuracy trajectories of one seed-matched triple under scaled replacement: the decimal scale S = 10⁶ "
                   "diverges from FedAvg, the power-of-two scale S = 2⁴⁰ coincides with it in every round. (b) Largest per-round "
                   "accuracy difference to FedAvg for each of the 18 smpc_only runs (zero for every rerun).",
           sources=["data/sum_only/scaled_replacement_baseline_s102_results.csv", "data/sum_only/scaled_replacement_smpc_only_1e6_s102_results.csv",
                    "data/sum_only/scaled_replacement_smpc_only_2p40_s102_results.csv", "data/sum_only/pow2_vs_fedavg.csv"],
           transform="global_accuracy per round as recorded; max_abs_accuracy_difference per run (pow2_vs_fedavg.py)")


# ------------------------------------------------------------------ E6 leakage
def e6_leakage():
    leak = pd.read_csv(D / "leakage/leakage_raw.csv")
    fc = leak[leak.attack == "fc_input"]
    fig, axes = plt.subplots(1, 2, figsize=(S.TEXT_WIDTH_IN, 2.5), sharey=True)
    for ax, state, title in ((axes[0], "initial", "(a) Untrained model"), (axes[1], "trained", "(b) Model after one epoch")):
        for view, label, colour in (("individual", "Plaintext FedAvg view (target's own update)", ORANGE),
                                    ("secure_aggregate", "SPDZ2k view (aggregate of 4 clients)", VIOLET)):
            f = fc[(fc.model_state == state) & (fc.view == view)]
            g = f.groupby("batch_size").apply(lambda x: pd.Series({"share": (x.ssim >= 0.9).mean(), "n": len(x)}), include_groups=False).reset_index()
            ax.plot(g.batch_size, g.share, color=colour, marker="o", markersize=4, label=label)
        ax.set_xscale("log", base=2)
        ax.set_xticks([1, 2, 4, 8], ["1", "2", "4", "8"])
        ax.set_xlabel("Images per client update (B)")
        ax.set_ylim(0, 1.05)
        ax.set_title(title, loc="left")
    axes[0].set_ylabel("Share of target images with SSIM ≥ 0.9")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.07))
    fig.tight_layout()
    S.save(fig, "e6_leakage", title="E6: images recoverable by a curious coordinator",
           caption="Analytic input read-out through the first fully connected layer of a probe MLP (E6, FedSGD, 8 trials per point): "
                   "share of the target client's images recovered near-exactly from its own update (plaintext FedAvg) and from "
                   "the SPDZ2k aggregate of a four-client cohort.",
           sources=["data/leakage/leakage_raw.csv"],
           transform="rows attack=fc_input; share of image records with ssim >= 0.9 per (model_state, view, batch_size)")


def main():
    for fn in (e1_backdoor_rounds, backdoor_asr_by_defence, e3_predictability, e3mc_exposure, e4_sweeps, overhead_rounds,
               benchmark_scaling, pilot_sign_agreement, m2_subsets, p3_paired, f1_framework, direction_cost,
               sum_only_correction, e6_leakage):
        fn()
        print("ok", fn.__name__)
    S.write_registry(S.ROOT / "figures" / "provenance_charts.json")


if __name__ == "__main__":
    main()
