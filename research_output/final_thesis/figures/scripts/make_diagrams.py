"""Architecture and process diagrams for the thesis (matplotlib, no data inputs).

    python research_output/final_thesis/figures/scripts/make_diagrams.py

The diagrams depict the implemented components (named after the source files
and functions they show) except where a caption marks a diagram as conceptual.
Registered in figures/provenance_diagrams.json.
"""
from __future__ import annotations

import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

import style as S
from style import BLUE, ORANGE, AQUA, VIOLET, INK, INK2, MUTED

S.apply_style()
SCRIPT = "figures/scripts/make_diagrams.py"
CHARS_PER_UNIT_AT_7PT = 0.95      # calibrated on the rendered previews (DejaVu Sans)


def tint(hex_colour: str, amount: float = 0.86) -> str:
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    mix = lambda c: int(c + (255 - c) * amount)
    return f"#{mix(r):02x}{mix(g):02x}{mix(b):02x}"


class Canvas:
    def __init__(self, w_in, h_in, xmax=100, ymax=60):
        self.fig, self.ax = plt.subplots(figsize=(w_in, h_in))
        self.ax.set_xlim(0, xmax)
        self.ax.set_ylim(0, ymax)
        self.ax.axis("off")
        self.units_per_in_y = ymax / h_in
        self.units_per_in_x = xmax / w_in

    def wrap(self, text, width_units, size):
        capacity = max(8, int(width_units * CHARS_PER_UNIT_AT_7PT * 7.0 / size * (self.units_per_in_y / self.units_per_in_x) ** 0))
        lines = []
        for line in text.split("\n"):
            if "$" in line or len(line) <= capacity:
                lines.append(line)
            else:   # never split identifiers such as receive_robust_result()
                lines.extend(textwrap.wrap(line, capacity, break_long_words=False, break_on_hyphens=False))
        return lines

    def box(self, x, y, w, h, text, colour=MUTED, fill=None, size=7.0, bold=False, ha="center", lw=1.0, name=""):
        self.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=0.9",
                                         facecolor=fill if fill is not None else tint(colour), edgecolor=colour, linewidth=lw))
        lines = self.wrap(text, w - 1.6, size)
        need = len(lines) * size * 1.32 / 72 * self.units_per_in_y
        if need > h + 0.5:
            print(f"  WARNING box '{name or lines[0][:30]}' needs {need:.1f} units, has {h}")
        tx = x + w / 2 if ha == "center" else x + 1.0
        self.ax.text(tx, y + h / 2, "\n".join(lines), ha=ha, va="center", fontsize=size, color=INK,
                     fontweight="bold" if bold else "normal", linespacing=1.3)

    def frame(self, x, y, w, h, label, colour=MUTED, where="top-left"):
        """Dashed group frame; the title goes where no arrow crosses it."""
        self.ax.add_patch(Rectangle((x, y), w, h, facecolor="none", edgecolor=colour, linewidth=0.9, linestyle=(0, (4, 3))))
        vertical, horizontal = where.split("-")
        ty, va = (y + h - 0.5, "top") if vertical == "top" else (y + 0.6, "bottom")
        tx, ha = (x + 0.8, "left") if horizontal == "left" else (x + w - 0.8, "right")
        self.ax.text(tx, ty, label, ha=ha, va=va, fontsize=7, color=INK2, fontweight="bold")

    def arrow(self, p, q, colour=INK2, both=False, rad=0.0, lw=1.0):
        self.ax.add_patch(FancyArrowPatch(p, q, arrowstyle="<|-|>" if both else "-|>", mutation_scale=9, color=colour,
                                          linewidth=lw, connectionstyle=f"arc3,rad={rad}", shrinkA=1.5, shrinkB=1.5))

    def label(self, x, y, text, size=6.5, ha="center", colour=INK2, italic=False):
        self.ax.text(x, y, text, ha=ha, va="center", fontsize=size, color=colour, style="italic" if italic else "normal",
                     bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.92))

    def save(self, name, **kw):
        S.save(self.fig, name, kind="diagram", script=SCRIPT, **kw)


# ------------------------------------------------------------------ D1 conceptual FL
def fl_overview():
    c = Canvas(S.TEXT_WIDTH_IN, 2.9, 100, 46)
    c.box(34, 32, 32, 11, "Server: global model $w_t$\naggregates with FedAvg", BLUE, size=7.5)
    for i, x in enumerate((3, 28, 53, 78)):
        name = f"Client {i + 1}" if i < 3 else "Client K"
        c.box(x, 3, 19, 10, f"{name}\nlocal data $D_k$\nlocal training", AQUA, size=7)
        c.arrow((47, 31.6), (x + 8, 13.4), colour=BLUE, lw=0.9)
        c.arrow((x + 11, 13.4), (53, 31.6), colour=ORANGE, lw=0.9)
    c.label(19, 24, "global model $w_t$", size=7)
    c.label(81, 24, "updated model $w^{(k)}_{t+1}$", size=7)
    c.label(50, 0.6, "Conceptual. Raw data never leaves the clients; the server cannot verify how an update was produced.",
            size=6.5, italic=True)
    c.save("fl_overview", title="Federated learning with a coordinating server (conceptual)",
           caption="Federated averaging (conceptual): in every round the server sends the global model to a cohort of clients, "
                   "each client trains on its own data and returns its model, and the server averages the returned models "
                   "weighted by sample counts.",
           sources=["conceptual; FedAvg as defined by McMahan et al. (2017)"], transform="none")


# ------------------------------------------------------------------ D2 implemented architecture
def system_architecture():
    c = Canvas(S.TEXT_WIDTH_IN, 6.0, 100, 96)
    c.frame(1, 64, 98, 31, "Flower coordinator: ResearchStrategy (federated/flower_simulation.py)", BLUE)
    c.box(3, 67, 22, 20, "MTDController\n(mtd/controller.py)\nselects cohort $C_r$", BLUE, size=6.8)
    c.box(27, 67, 22, 20, "Round set-up\nround_spec()\n(smpc/robust.py)\nweights, bounds", BLUE, size=6.8)
    c.box(51, 67, 22, 20, "Output client\nreceive_robust_result()\ndecode, check norm,\napply or keep model", BLUE, size=6.8)
    c.box(75, 67, 22, 20, "Evaluation\naccuracy, loss, ASR;\nper-round CSV;\nMPC time, traffic", BLUE, size=6.8)
    c.frame(1, 31, 98, 28, "Aggregation parties P0, P1, P2 (smpc/mp_spdz_party_service.py, MP-SPDZ 0.4.3)", VIOLET, where="bottom-left")
    for i, x in enumerate((5, 38, 71)):
        c.box(x, 36.5, 24, 14, f"Party service P{i}\nvalidate, compile, hash;\nrun spdz2k-party.x", VIOLET, size=6.8)
    c.arrow((29.5, 43.5), (37.5, 43.5), colour=VIOLET, both=True)
    c.arrow((62.5, 43.5), (70.5, 43.5), colour=VIOLET, both=True)
    c.label(50, 55.5, "SPDZ2k over $\\mathbb{Z}_{2^{64}}$: MAC-checked, dishonest majority, security with abort", size=6.5)
    c.frame(1, 1, 98, 25, "Flower clients (Ray actors): ResearchNumPyClient + attacks/byzantine.py", AQUA, where="bottom-left")
    for i, x in enumerate((4, 28, 52, 76)):
        name = f"Client {i + 1}" if i < 3 else "Client K"
        c.box(x, 6.5, 20, 15, f"{name} in $C_r$\nlocal SGD,\nplus attack\nsubmit_client_\ndelta()", AQUA, size=6.6)
    c.arrow((38, 66.6), (25, 50.9))
    c.label(22, 61, "HMAC-signed control:\nstart, status, stop, cleanup", size=6.3)
    c.arrow((62, 50.9), (62, 66.6))
    c.label(77, 61, "revealed outputs only:\nT, accept bits, flags, A", size=6.3)
    c.arrow((14, 21.9), (17, 36.1), colour=AQUA)
    c.arrow((86, 21.9), (83, 36.1), colour=AQUA)
    c.label(50, 28.5, "secret inputs $[n_k, x_k]$ sent directly to every party (TLS client certificates); no tensors go to the coordinator",
            size=6.3)
    c.save("system_architecture", title="Implemented system architecture",
           caption="Implemented architecture of the hybrid framework (all components ran on one host in the evaluation). "
                   "The coordinator selects the cohort with the MTD controller and sends the global model to the clients "
                   "(Flower FitIns, not drawn); the clients send their encoded updates directly to the three SPDZ2k parties, "
                   "and only the declared outputs reach the coordinator's output client.",
           sources=["src/fl_security/federated/flower_simulation.py", "src/fl_security/mtd/controller.py",
                    "src/fl_security/smpc/{robust.py, mp_spdz.py, mp_spdz_party_service.py}", "research_output/completion/FINAL_ARCHITECTURE.md"],
           transform="none")


# ------------------------------------------------------------------ D3 round sequence
def round_sequence():
    c = Canvas(S.TEXT_WIDTH_IN, 5.4, 100, 88)
    lanes = {"C": (14, "Coordinator\n+ output client", BLUE), "P": (52, "Party services\nP0, P1, P2", VIOLET),
             "K": (86, "Client k in $C_r$", AQUA)}
    for x, label, colour in lanes.values():
        c.box(x - 11, 79, 22, 7, label, colour, size=7, bold=True)
        c.ax.plot([x, x], [8, 78.5], color=colour, linewidth=1.0, linestyle=(0, (3, 2)))
    steps = [
        (73, "C", "C", "1  cohort $C_r$ from MTDController"),
        (67, "C", "P", "2  start(round, cohort, counts, weights, spec)"),
        (61, "P", "P", "3  validate, compile; hashes must agree"),
        (55, "C", "K", "4  FitIns: global model + robust configuration"),
        (49, "K", "K", "5  local SGD (+ attack); $x_k=\\mathrm{round}(\\Delta_k 2^f)$"),
        (43, "K", "P", "6  secret input $[n_k, x_k]$"),
        (37, "P", "P", "7  in SPDZ2k: norms, T, screens, clip, $A$"),
        (30, "P", "C", "8  reveal T, #clipped, accept bits, flags, $A$"),
        (23, "C", "C", "9  decode; output-norm check; apply or keep"),
        (16, "C", "P", "10  finish_round: exit codes, time, traffic, cleanup"),
    ]
    for y, a, b, text in steps:
        xa, xb = lanes[a][0], lanes[b][0]
        if a == b:
            c.ax.add_patch(Rectangle((xa - 0.6, y - 2.0), 1.2, 4.0, facecolor=MUTED, edgecolor="none"))
            if a == "K":
                c.ax.text(xa - 2, y, text, ha="right", va="center", fontsize=6.5, color=INK)
            else:
                c.ax.text(xa + 2, y, text, ha="left", va="center", fontsize=6.5, color=INK)
        else:
            c.arrow((xa, y), (xb, y))
            c.label((xa + xb) / 2, y + 2.1, text, size=6.5, colour=INK)
    c.label(50, 3.5, "Any failure (missing client, malformed input, hash mismatch, MAC failure, timeout) aborts the round; "
                     "there is no plaintext fallback.", size=6.3, italic=True)
    c.save("round_sequence", title="Sequence of one robust secure round",
           caption="Message sequence of one secure round with the in-MPC defence, as implemented in flower_simulation.py, "
                   "mp_spdz.py and mp_spdz_party_service.py.",
           sources=["src/fl_security/federated/flower_simulation.py", "src/fl_security/smpc/mp_spdz.py",
                    "research_output/completion/FINAL_ARCHITECTURE.md §2"], transform="none")


# ------------------------------------------------------------------ D4 party service
def party_service():
    c = Canvas(S.TEXT_WIDTH_IN, 2.8, 100, 42)
    steps = ["Authenticate\nHMAC-SHA256,\n±300 s window,\nreplay journal",
             "Validate\nprogram, cohort,\ncounts, weights,\nround spec",
             "Compile\nsource with round\narguments; -R 64;\nhash bytecode",
             "Agree\nidentical bytecode\nat every party,\nelse abort",
             "Run\nspdz2k-party.x;\nclient inputs via\nTLS",
             "Finish\nexit code, time,\ntraffic; delete\nround artefacts"]
    for i, text in enumerate(steps):
        x = 1 + i * 16.6
        c.box(x, 15, 15, 22, text, VIOLET, size=6.6)
        if i:
            c.arrow((x - 1.5, 26), (x - 0.1, 26))
    c.box(14, 2.5, 72, 7, "Any failure at any party: all parties stopped, round aborted, previous model kept", ORANGE, size=6.8)
    c.save("party_service", title="Party service pipeline",
           caption="Processing of one round inside each aggregation-party service (mp_spdz_party_service.py).",
           sources=["src/fl_security/smpc/mp_spdz_party_service.py", "docs/threat-model.md (failure behaviour)"], transform="none")


# ------------------------------------------------------------------ D5 in-MPC defence
def inmpc_defence():
    c = Canvas(S.TEXT_WIDTH_IN, 6.0, 100, 100)
    c.frame(1, 25, 98, 74, "Inside SPDZ2k (secret-shared): spdz2k_robust_aggregate.mpc", VIOLET)
    rows = [
        "Inputs: $x_k \\in \\mathbb{Z}_{2^{64}}^d$ (update at scale $2^f$) and public weights $w_k$, $k = 1 \\ldots K$",
        "1  squared norm $R_k=\\Sigma_j\\, x_{kj}^2$; visible contribution $S_k=w_k^2 R_k$",
        "2  validity $v_k=[0\\leq S_k\\leq w_k^2 r_{max}]$: wrapped or malformed inputs excluded",
        "3  threshold $T=\\mathrm{clamp}(\\lambda^2\\cdot \\mathrm{lowermedian}(R'), t_{min}, t_{max})$",
        "4  screen $a_k=v_k\\cdot[S_k\\leq \\rho^2 w_k^2 T]$ (revealed accept bit)",
        "5  optional direction screen on a secret subset $S_r$ (Figure: direction screen)",
        "6  clip $C_k=\\lfloor 2^g\\,\\mathrm{min}(1,\\sqrt{T/R_k})\\rfloor$ by binary search (secret)",
        "7  aggregate $A_j=\\Sigma_k\\, a_k C_k w_k x_{kj}$; reveal $A$, $T$, #clipped, $a_k$",
    ]
    for i, text in enumerate(rows):
        y = 88 - i * 8.2
        c.box(4, y, 92, 5.6, text, VIOLET, size=7, ha="left", name=f"row{i}")
        if i:
            c.arrow((50, y + 8.2 - 0.1), (50, y + 5.9))
    c.frame(1, 1, 98, 20, "Coordinator / output client (plaintext)", BLUE, where="top-right")
    c.box(4, 6, 42, 9, "decode\n$\\bar\\Delta = A / (2^{g+f}\\, \\Sigma_k a_k w_k)$", BLUE, size=7)
    c.box(52, 6, 44, 9, "output-norm check $\\Vert A\\Vert^2\\leq(2^g \\Sigma_k a_k w_k)^2 B$:\npass: apply $\\bar\\Delta$; fail: keep model", BLUE, size=6.8)
    c.arrow((50, 30.5), (25, 15.4))
    c.arrow((46.3, 10.5), (51.7, 10.5))
    c.label(50, 3, "Never revealed: norms, clip coefficients, individual updates", size=6.4, italic=True)
    c.save("inmpc_defence", title="In-MPC robust aggregation",
           caption="The robust aggregation computed inside SPDZ2k and the coordinator's plaintext output check "
                   "(spdz2k_robust_aggregate.mpc, robust.py). Every decision uses the visible contribution $w_k x_k$, "
                   "which closes the wrap-around and weight-inverse attacks on the 64-bit ring.",
           sources=["src/fl_security/smpc/programs/spdz2k_robust_aggregate.mpc", "src/fl_security/smpc/robust.py",
                    "docs/secure_robust_aggregation.md §3-5"], transform="none")


# ------------------------------------------------------------------ D6 direction screen
def direction_screen():
    c = Canvas(S.TEXT_WIDTH_IN, 4.4, 100, 70)
    c.frame(1, 41, 48, 28, "Coordinator (per round r)", BLUE)
    c.box(3, 54, 44, 9, "key = SHA-256(\"direction-screen\" | secret)\n(paired evaluation: per-seed suite key)", BLUE, size=6.4)
    c.box(3, 43.5, 44, 8, "$S_r$ = HMAC PRF sample of round(fraction·d) indices\nfrom HMAC(key, \"direction-subset\" | r)", BLUE, size=6.4)
    c.arrow((25, 53.6), (25, 51.9))
    c.frame(51, 41, 48, 28, "Clients (do not know $S_r$)", AQUA)
    c.box(53, 54, 44, 8, "honest client: submits $x_k$ as trained", AQUA, size=6.6)
    c.box(53, 43.5, 44, 8, "evasive attacker: copies clean values\ninto a guessed 25 % of the coordinates", ORANGE, size=6.4)
    c.frame(1, 1, 98, 35, "Inside SPDZ2k: the indices of $S_r$ and min_agree are public round arguments", VIOLET, where="bottom-left")
    stages = [(3, "sign bits\n$b_{kj}=[x_{kj}\\geq 0]$\n32-bit test, $j\\in S_r$"),
              (27.5, "majority of\nthe others\n$m_{kj}=[2(\\Sigma_i b_{ij}-b_{kj})$\n$\\geq K-1]$, ties: +"),
              (52, "agreement\n$g_k=\\Sigma_{j\\in S_r}[b_{kj}=m_{kj}]$"),
              (76.5, "pass if $g_k\\geq\\lceil\\tau |S_r|\\rceil$\n$a_k \\leftarrow a_k\\cdot \\mathrm{pass}_k$")]
    for x, text in stages:
        c.box(x, 9, 21.5, 17, text, VIOLET, size=6.4)
    for x in (24.8, 49.3, 73.8):
        c.arrow((x, 17.5), (x + 2.6, 17.5))
    c.arrow((20, 43.1), (13, 26.6), colour=BLUE)
    c.arrow((75, 43.1), (15, 26.6), colour=AQUA, rad=0.12)
    c.label(10, 37.8, "indices of $S_r$", size=6.3)
    c.label(60, 37.8, "inputs $x_k$", size=6.3)
    c.save("direction_screen", title="Moving-target direction screen",
           caption="The moving-target direction screen. A secret, round-specific coordinate subset is drawn by the coordinator; "
                   "inside SPDZ2k each client's sign pattern on that subset is compared with the majority of the other cohort "
                   "members, and clients below the agreement threshold leave the aggregate like screen-rejected ones.",
           sources=["src/fl_security/smpc/robust.py (direction_key, direction_indices, direction_screen)",
                    "src/fl_security/smpc/programs/spdz2k_robust_aggregate.mpc", "src/fl_security/federated/flower_simulation.py"],
           transform="none")


# ------------------------------------------------------------------ D7 MTD workflow
def mtd_workflow():
    c = Canvas(S.TEXT_WIDTH_IN, 3.9, 100, 62)
    c.frame(1, 1, 50, 60, "Coordinator (holds FL_MTD_SECRET)", BLUE)
    chain = ["secret, at least 32 bytes;\nnever sent or logged", "key = HMAC-SHA256(secret, seed material)",
             "round key = HMAC(key, round r)\ncounter-mode PRF (HMACCounterRNG)", "rejection sampling and\npartial Fisher-Yates shuffle",
             "cohort $C_r$: K of N clients"]
    for i, text in enumerate(chain):
        y = 49 - i * 11
        c.box(4, y, 44, 7.5, text, BLUE, size=6.6)
        if i:
            c.arrow((26, y + 10.9), (26, y + 7.8))
    c.frame(53, 1, 46, 60, "Adversary (knows code, config, seed)", ORANGE)
    adv = ["runs the scheduler without the secret\n(the deterministic schedule)", "predicted cohort $\\hat C_r$",
           "predictive: clients predicted most often\njust-in-time: members of $\\hat C_r$",
           "secret schedule: hit rate K/N (chance)\nstatic, deterministic: 1.0"]
    for i, text in enumerate(adv):
        y = 47 - i * 13
        c.box(56, y, 40, 9.5, text, ORANGE, size=6.5)
        if i:
            c.arrow((76, y + 12.9), (76, y + 9.8))
    c.save("mtd_workflow", title="Secret-derived MTD scheduling",
           caption="Secret-derived cohort selection (mtd/controller.py, mtd/randomness.py) and the schedule-aware adversary models "
                   "used in E3 (mtd/exposure.py). Without the secret, prediction is no better than chance.",
           sources=["src/fl_security/mtd/controller.py", "src/fl_security/mtd/randomness.py", "src/fl_security/mtd/exposure.py",
                    "docs/mtd_scheduling.md"], transform="none")


# ------------------------------------------------------------------ D8 experiment pipeline
def experiment_pipeline():
    c = Canvas(S.TEXT_WIDTH_IN, 3.4, 100, 54)
    main = [(1, "grid.py\nall studies;\none RunSpec\nper run"), (21, "run_suite.py\nprocess per run,\ntimeout, MTD\nsecret, metadata"),
            (41, "run_experiment.py\nFlower simulation\n+ local SPDZ2k\nparties"), (61, "per-run files\nconfig, CSV,\nanalysis, npz,\nmetadata"),
            (81, "analyze_suite.py\nsummaries,\npaired differences,\nmatrix, figures")]
    for x, text in main:
        c.box(x, 28, 18, 20, text, BLUE, size=6.5)
    for x in (19.2, 39.2, 59.2, 79.2):
        c.arrow((x, 38), (x + 1.6, 38))
    side = [(1, "run_mpc_validation.py\nSPDZ2k vs reference"), (26, "run_mpc_benchmark.py\ncost vs model size"),
            (51, "run_mtd_exposure.py\nMonte-Carlo exposure"), (76, "run_leakage_study.py\ngradient inversion (E6)")]
    for x, text in side:
        c.box(x, 13, 23, 9, text, VIOLET, size=6.4)
    c.box(1, 1.5, 98, 6.5, "Verification: verify_run_configs.py, e2e_reference_summary.py, pow2_vs_fedavg.py, verify_metrics.py",
          AQUA, size=6.5)
    c.save("experiment_pipeline", title="Experiment and evidence pipeline",
           caption="Experiment orchestration and evidence pipeline. Every run is defined in grid.py, executed in its own process "
                   "and recorded with its configuration, commit, configuration hash and secret commitment.",
           sources=["src/fl_security/experiments/{grid.py, suite.py, analysis.py, report.py}", "run_*.py", "analyze_suite.py"],
           transform="none")


# ------------------------------------------------------------------ D9 attack/defence interaction
def attack_defence_layers():
    layers = ["SPDZ2k secure\naggregation", "In-MPC norm\nclip + screen", "Direction screen\n(secret subset)", "Secret MTD\nschedule"]
    rows = [
        ("Curious coordinator\n(inversion)", ["reduces, does\nnot remove (E6)", "-", "-", "-"]),
        ("Sign flip, scaled\nreplacement, noise", ["no effect (E1)", "mitigated (E1)", "separates\n(pilot AUC 0.82-0.98)", "no effect (E1)"]),
        ("Boosted backdoor", ["no effect (E1)", "mitigated (E1)", "weak\n(pilot AUC 0.66)", "no effect alone (E1)"]),
        ("Label flipping", ["no effect (E1)", "partial (E1)", "rejection\n0.77 to 0.93 (M2)", "-"]),
        ("Adaptive backdoor\n(at the bound)", ["no effect (E1)", "partial (E2)", "lowers ASR\n(M2, P3)", "lowers exposure\n(P3)"]),
        ("Evasive backdoor", ["no effect", "partial (M2, P3)", "weak (M2)", "small (P3)"]),
        ("Schedule-targeting\nadversary", ["no effect (E3)", "fails under an\nattacker majority (M3)", "fails under an\nattacker majority (P3)", "main protection\n(E3, P3)"]),
    ]
    level = {"mitigated (E1)": 3, "main protection\n(E3, P3)": 3, "separates\n(pilot AUC 0.82-0.98)": 3,
             "partial (E1)": 2, "partial (E2)": 2, "reduces, does\nnot remove (E6)": 2, "lowers ASR\n(M2, P3)": 2,
             "rejection\n0.77 to 0.93 (M2)": 2, "lowers exposure\n(P3)": 2,
             "partial (M2, P3)": 1, "weak (M2)": 1, "small (P3)": 1, "weak\n(pilot AUC 0.66)": 1}
    c = Canvas(S.TEXT_WIDTH_IN, 4.8, 100, 84)
    x0, cw, rh = 20, 20, 9.6
    for j, layer in enumerate(layers):
        c.box(x0 + j * cw + 0.5, 73.5, cw - 1, 8.5, layer, BLUE, size=6.6, bold=True)
    for i, (attack, cells) in enumerate(rows):
        y = 64 - i * rh
        c.box(0.5, y, 18.5, rh - 1.2, attack, ORANGE, size=6.3)
        for j, cell in enumerate(cells):
            fill = {3: tint(BLUE, 0.55), 2: tint(BLUE, 0.78), 1: tint(BLUE, 0.92), 0: "white"}[level.get(cell, 0)]
            c.box(x0 + j * cw + 0.5, y, cw - 1, rh - 1.2, cell, MUTED, fill=fill, size=6.2)
    c.label(50, 0.8, "Darker cells: stronger measured effect. Brackets name the experiments; '-' means not applicable.", size=6.3, italic=True)
    c.save("attack_defence_layers", title="Which layer addresses which attack",
           caption="Interaction between attack classes and the framework's layers, as measured in this thesis (experiment "
                   "identifiers in brackets).",
           sources=["research_output/completion/FINAL_VALIDATION_REPORT.md", "research_output/mtd_defence/MTD_DEFENCE_REPORT.md",
                    "matrices/VERIFIED_METRICS.csv"], transform="qualitative summary of measured verdicts")


def main():
    for fn in (fl_overview, system_architecture, round_sequence, party_service, inmpc_defence, direction_screen,
               mtd_workflow, experiment_pipeline, attack_defence_layers):
        print("diagram", fn.__name__)
        fn()
    S.write_registry(S.ROOT / "figures" / "provenance_diagrams.json")


if __name__ == "__main__":
    main()
