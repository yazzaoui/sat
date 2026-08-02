# Witness-search results index

Status: **complete**. Every row links its full document; every UNSAT
claim is dpr-trim-verified; every experiment row was pre-registered
before running. Reproduce all headline rows: [REPRODUCING.md](REPRODUCING.md).

## Milestones

| Milestone | Verdict | Document |
|---|---|---|
| M0 separation | Reproduced on 3 families with CDCL timeouts, verified proofs | [m0-separation](docs/m0-separation.md) |
| M1 witness atlas | Locality confirmed vs null model; pattern taxonomy separates families blind | [witness-atlas](docs/witness-atlas.md) |
| M2 benchmark + gate | Three regimes; portfolio-safe online gate shipped (v3), tax measured | [m2-benchmark](docs/m2-benchmark.md) |

## Boundary map (five edges, all pre-registered)

| Edge | Verdict | Document |
|---|---|---|
| Static template cores | Fail: valid geometric cores cost ~3× steering in every integration mode | [phase2-trajectory-study](docs/phase2-trajectory-study.md), [phase2-chessboard-results](docs/phase2-chessboard-results.md) |
| Trail-aware guidance inward (A) | Null/harm: witness quality not seedable, even from own conflict analysis | [phase3-experiment-a](docs/phase3-experiment-a.md) |
| Activity export outward (C) | Harm: inner relevance is locally scoped | [phase3-experiment-c](docs/phase3-experiment-c.md) |
| Clause-identity persistence (E) | Terminated pre-build: cost is trail-global, not clause-local | [phase3-experiment-e-preregistration](docs/phase3-experiment-e-preregistration.md) |
| Delta-stable filtering | Gate fired at 4× threshold: the delta changes the questions, not the answers | [filter-churn-results](docs/filter-churn-results.md) |

Composite: the stuck-point computation is irreducibly local in time and
information; the sub-solver call is the unit of the method
([mechanism-refinement](docs/mechanism-refinement.md)).

## Retired / auxiliary

- Experiment B: retired unrun, no consumer for any outcome
  ([phase3-preregistration](docs/phase3-preregistration.md)).
- Amortization feasibility: overlap 93–96%, which motivated E
  ([amortization-feasibility](docs/amortization-feasibility.md)).
- Vertical slice (external PHP templates): plumbing proof
  ([phase2-vertical-slice](docs/phase2-vertical-slice.md)).

## Reproduction status

- Tag `boundary-map-v1`: 12/12 clean-clone checks (pre-reorganization
  layout).
- Post-reorganization: reproduce.py re-run from the new layout —
  see the reorganization commit message for the re-verified 12/12.
