# Securing Federated AI Systems

Code and evidence of the BSc thesis *Securing Federated AI Systems: secure
aggregation with SPDZ2k, an in-MPC poisoning defence and moving target defence
for federated learning* (Uzair Muhammad, Computer Science BSc, Eötvös Loránd
University, Faculty of Informatics, 2026; supervisor: Bencsik Gergely).

## What it is

A federated learning framework built on [Flower](https://flower.ai) that combines
three layers in one training pipeline:

1. **Secure aggregation.** Client updates are summed with the maliciously secure
   SPDZ2k protocol of [MP-SPDZ](https://github.com/data61/MP-SPDZ) v0.4.3, so the
   coordinator never sees an individual update.
2. **A poisoning defence inside the secure computation.** Each update is
   screened and clipped against a threshold derived from the cohort's median
   update norm, with checks that close the wrap-around attacks of the 64-bit ring.
3. **Moving target defence.** The participants of each round are drawn from a
   secret schedule, and a sign-agreement check rejects updates that point against
   the majority on a secret, changing subset of coordinates.

## Main results

Evaluated on Fashion-MNIST with twelve simulated clients in 542 training runs,
157 of them inside SPDZ2k, all on one host with a 2,202-parameter model:

* The secure program matched its exact plaintext specification in all 20
  validation scenarios and in every training round.
* Secure sum-only aggregation is federated averaging bit for bit, so on its own
  it does nothing against poisoning.
* The in-MPC defence cut a boosted backdoor's attack success rate from 0.921 to
  0.017 without rejecting an honest client, at 3.7 times the round time of plain
  averaging. Attackers that stay just under the bound, or flip labels, keep part
  of their influence.
* Secret cohorts plus the secret direction check gave the lowest attack success
  against every attacker in a paired five-seed study (not statistically
  significant with five seeds).
* Secure aggregation reduced, but did not prevent, reconstruction of training
  images by a curious coordinator.

## Quick start

Linux is required for the SPDZ2k parties; on Windows or macOS only the plaintext
paths and the unit tests run.

```bash
python -m pip install -e ".[simulation,dev]"
python -m pytest -q

# plaintext FedAvg under a boosted backdoor
python run_experiment.py --config configs/plaintext.yaml

# full framework: SPDZ2k with three local parties, in-MPC defence, secret MTD schedule
# (needs MP-SPDZ v0.4.3 with spdz2k-party.x built)
export FL_MPSPDZ_HOME=/path/to/MP-SPDZ-v0.4.3
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
export FL_MTD_SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
python run_experiment.py --config configs/example.yaml --local-mp-spdz
```

Results go to `results/<name>/`. [docs/reproduction.md](docs/reproduction.md)
lists the commands for every study, run times and troubleshooting.

## Repository layout

| Path | Content |
|---|---|
| `src/fl_security/` | the framework: `federated/` (Flower simulation, model, data), `smpc/` (SPDZ2k coordinator, party service, MPC programs with the in-MPC defence and direction screen, exact reference), `mtd/` (participation schedules, exposure models), `attacks/`, `experiments/` (study grid, suite, analysis, reports) |
| `run_experiment.py` | one run from a YAML configuration |
| `run_suite.py`, `analyze_suite.py` | run whole studies from `src/fl_security/experiments/grid.py` and summarise them |
| `run_mpc_validation.py`, `run_mpc_benchmark.py`, `run_mtd_exposure.py`, `run_leakage_study.py` | SPDZ2k validation, cost benchmarks, schedule exposure, gradient-inversion study |
| `configs/` | `example.yaml` (full framework) and `plaintext.yaml` (FedAvg baseline) |
| `tests/` | unit and integration tests; `FL_RUN_MPSPDZ_TESTS=1` adds a real SPDZ2k round |
| `docs/` | architecture, threat model, SPDZ2k implementation, in-MPC defence, MTD scheduling, methodology, security limitations, reproduction |
| `research_output/completion/` | main evaluation E1–E5, validation, benchmarks, MTD exposure, update leakage E6 (`experiments/leakage/`) and the corrected sum-only rerun (`experiments_pow2/`) |
| `research_output/mtd_defence/` | direction-screen pilot and studies M1–M3, P3 and F1 |
| `research_output/final_thesis/` | the data behind every figure and table of the thesis, the figures and their scripts, and the verification records |

Every run directory holds its `config.yaml`, per-round results,
`round_analysis.csv` and `run_metadata.json`.

## Notes on the evidence

* The work was developed on the branches `research/spdz2k-secure-robust-aggregation`,
  `research/gradient-inversion-leakage`, `research/sum-only-pow2-scale-fix` and
  `research/mtd-direction-screen`. Their evidence is merged here at the paths
  above; the commit IDs recorded in the runs refer to that development history.
* Not included: the binary instrumentation archives (`*.npz`, about 1 MB per
  run; those of the main evaluation are hashed in
  `research_output/completion/final_validation_manifest.json`), the run logs,
  and the `pairing_key` from which P3 derived its MTD secrets.
* All results come from simulation on one host (aarch64, 3 vCPUs, 17 GiB RAM).
  Cross-host deployment was not validated; see
  [docs/security-limitations.md](docs/security-limitations.md).
