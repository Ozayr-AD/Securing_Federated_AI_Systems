"""Shared figure style, colours and provenance registry for the thesis figures.

Colours follow a validated categorical palette in fixed order (colour-blind
safe for adjacent series); every configuration keeps the same colour in every
figure. Text uses ink colours, never series colours.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]          # research_output/final_thesis
DATA = ROOT / "data"
PNG = ROOT / "figures" / "png"
PDF = ROOT / "figures" / "pdf"

# categorical slots (light mode), fixed order
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = (
    "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948")
DARK_BLUE = "#1c5cab"            # blue ramp step 550: related entity of BLUE
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS = "#e1e0d9", "#c3c2b7"
SURFACE = "#ffffff"

CONFIG = {   # entity -> (label, colour); the same in every figure
    # orange (FedAvg) is never paired with yellow: that pair fails the palette's
    # colour-vision separation check, so the sum-only path is violet.
    "baseline": ("FedAvg, no defence", ORANGE),
    "mtd_only": ("FedAvg + MTD", YELLOW),
    "smpc_only": ("SPDZ2k sum only", VIOLET),
    "smpc_mtd": ("SPDZ2k sum only + MTD", GREEN),
    "smpc_clip": ("SPDZ2k + static clipping", AQUA),
    "smpc_defence": ("SPDZ2k + clip/screen, static cohort", DARK_BLUE),
    "smpc_defence_mtd": ("Full framework: SPDZ2k + clip/screen + MTD", BLUE),
    "plaintext_robust": ("Plaintext detector (no SMPC)", MAGENTA),
    "smpc_screen": ("SPDZ2k + screening only", RED),
}

TEXT_WIDTH_IN = 6.3      # about 16 cm, the text width of an A4 page with 2.5 cm margins
REGISTRY: list[dict] = []


def apply_style() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 8.5, "axes.titlesize": 9, "axes.titleweight": "bold",
        "axes.labelsize": 8.5, "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 8,
        "axes.edgecolor": AXIS, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
        "text.color": INK, "axes.titlecolor": INK, "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "lines.linewidth": 1.6, "lines.markersize": 5, "legend.frameon": False,
        "pdf.fonttype": 42, "svg.fonttype": "none",
    })


def save(fig, name: str, *, title: str, caption: str, sources: list[str], transform: str,
         kind: str = "chart", script: str = "figures/scripts/make_charts.py") -> None:
    PNG.mkdir(parents=True, exist_ok=True)
    PDF.mkdir(parents=True, exist_ok=True)
    fig.savefig(PNG / f"{name}.png", dpi=300, bbox_inches="tight")
    fig.savefig(PDF / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)
    REGISTRY.append({"name": name, "kind": kind, "title": title, "caption": caption, "sources": sources,
                     "transform": transform, "script": script,
                     "png": f"figures/png/{name}.png", "pdf": f"figures/pdf/{name}.pdf"})


def write_registry(path: Path) -> None:
    path.write_text(json.dumps(REGISTRY, indent=2), encoding="utf-8")


def end_label(ax, x, y, text, colour=INK2, dx=4, dy=0, **kw):
    """Direct label at the end of a line, in ink colour."""
    ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points", va="center", ha="left",
                fontsize=7.5, color=colour, **kw)
