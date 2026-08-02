# Reproducing the boundary map

Every headline claim in this repository re-earns itself from a clean
checkout with the commands below. Total runtime ≈ 2–4 minutes after the
build (all checks are deterministic conflict counts, gate verdicts, and
dpr-trim proof verifications; two measurement checks use tolerance
bands). Requires: C/C++ compiler, make, git, Python ≥ 3.9. Tested on
macOS arm64 (clang 17); the codebases are plain C/C++ and build on
Linux identically.

## 1. Clone and fetch the pinned external toolchain

The patched SaDiCaL (the instrumented solver every experiment ran on)
is tracked in this repository under common/tools/sadical. CaDiCaL and dpr-trim are external and
pinned by commit:

```sh
git clone https://github.com/yazzaoui/sat.git pnp && cd pnp
git clone https://github.com/arminbiere/cadical.git common/tools/cadical
git -C common/tools/cadical checkout c60730422e758ef1cebe7aeddf2dda31c996bf04
git clone https://github.com/marijnheule/dpr-trim.git common/tools/dpr-trim
git -C common/tools/dpr-trim checkout 2dff40530dbc6ac78e52bfe917f872cb16780418
```

## 2. Build

```sh
( cd common/tools/cadical && ./configure && make )
( cd common/tools/sadical && ./configure.sh && make )
( cd common/tools/dpr-trim && make )
```

## 3. Reproduce

```sh
python3 witness-search/scripts/reproduce.py
```

Expected output: `12/12 checks passed`, covering:

| Check | Claim it re-earns |
|---|---|
| M0 php12 | SDCL solves CDCL-timeout PHP(12) in 487 conflicts, proof dpr-trim-VERIFIED (docs/m0-separation.md) |
| determinism ×3 | Frozen baseline conflict counts reproduce exactly (the gate every experiment ran behind) |
| structure | Blind recovery labels chessboard `counting+grid` (docs/witness-atlas.md, phase 2) |
| edge1 | Static template cores inflate conflicts ≥1.5× — 954,009 vs 279,631 (docs/phase2-trajectory-study.md) |
| edge2 | Experiment A: conflict-analysis seeding = 466,476 conflicts, exact (docs/phase3-experiment-a.md) |
| edge3 | Experiment C: activity harvest = 450,448 conflicts, exact (docs/phase3-experiment-c.md) |
| edge4 | Experiment E termination: filtering ≥45% of process time (docs/phase3-experiment-e-preregistration.md) |
| edge5 | Filter churn: recompute median ≈0.58 vs 0.10–0.15 gate (docs/filter-churn-results.md) |
| gate ×2 | Shipped gate: PHP confirms lossless at 100% hits; chessboard reverts with conflicts *identical* to stock (docs/m2-benchmark.md) |

## What is deliberately not covered

- Full experiment matrices (all sizes/arms): headline rows only; the
  complete tables live in `docs/` with their raw data under
  `witness-search/benchmarks/results/` and the frozen M1 snapshot under
  `witness-search/benchmarks/frozen/` (sha256-manifested).
- SATLIB competition instances (coloring/logistics/BMC/uf rows of the
  M2 table): require downloads; `witness-search/scripts/filter_sweep.py` regenerates
  those rows once the archives referenced in it are fetched. Note the
  SATLIB header quirk: SaDiCaL needs the normalized copies (see
  `docs/filter-churn-results.md` history and `witness-search/benchmarks/cnf/uf*.cnf`).
- Wall-clock claims: machine-dependent by nature; every load-bearing
  comparison in the docs is backed by a deterministic conflict count or
  a verdict string that this script does check.

## Map of the claims to their pre-registrations

Every experiment listed above was pre-registered before it ran
(under witness-search/docs/: `phase2-preregistration.md`, `phase3-preregistration.md`,
`phase3-experiment-c-preregistration.md`,
`phase3-experiment-e-preregistration.md`,
`filter-churn-preregistration.md`) — commit history shows each
registration preceding its results.
