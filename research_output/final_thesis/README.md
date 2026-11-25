# Thesis data, figures and verification

The data behind every figure and table of the thesis, the figures with the
scripts that draw them, and the verification records. No experiment was rerun
to produce it; every number comes from the recorded runs in this repository.

| Path | Content |
|---|---|
| `data/` | byte-identical copies of the experiment outputs used by the figures, tables and checks; `data/MANIFEST.csv` gives the source path, SHA-256 and size of each |
| `figures/png/`, `figures/pdf/` | 23 figures (14 charts, 9 diagrams) at 300 dpi and as vector PDF; the thesis uses 18 of them |
| `figures/scripts/` | `make_charts.py` (charts from `data/`), `make_diagrams.py`, shared `style.py` |
| `figures/provenance_*.json` | sources and transformation of every figure, written by the figure scripts |
| `FIGURE_DATA_PROVENANCE.md` | per figure and table: number, file, data sources with SHA-256, transformation, script |
| `tools/make_tables.py` | the generated tables of the thesis, written to `build/tables/` |
| `tools/verify_metrics.py` | recomputes 668 reported values from `data/` and compares them with the original analyses (0 differ); writes `matrices/VERIFIED_METRICS.csv` and `matrices/VERIFICATION_LOG.txt` |
| `matrices/CLAIM_EVIDENCE_MATRIX.md` | main claims of the thesis, traced to their study, evidence and verification |
| `matrices/REFERENCE_VERIFICATION.csv`, `.md` | verification record of the bibliography |

## Regenerating

Run from the repository root with the project's Python environment (NumPy,
pandas and Matplotlib):

```bash
python research_output/final_thesis/figures/scripts/make_charts.py
python research_output/final_thesis/figures/scripts/make_diagrams.py
python research_output/final_thesis/tools/make_tables.py
python research_output/final_thesis/tools/verify_metrics.py
```

The chart and diagram scripts reproduce the committed PNG figures byte for byte,
and `verify_metrics.py` reproduces `VERIFIED_METRICS.csv` unchanged.
`build/` holds generated output only and is not tracked.
