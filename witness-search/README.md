# Witness search (SDCL) — complete

Instrumented witness search for propagation-redundant clause learning:
measurement, structure recovery, guided proposal, and the boundary map
of what can and cannot be moved across the inner/outer solver boundary.

- **Mandate:** [SPEC.md](SPEC.md)
- **Every claim, one line each:** [RESULTS.md](RESULTS.md)
- **Watch it re-earn itself:** [REPRODUCING.md](REPRODUCING.md)
- **Protocol it ran under:** [../common/DISCIPLINE.md](../common/DISCIPLINE.md)

What shipped beyond the science: the probation-gated portfolio-safe
SDCL solver (`../common/tools/sadical`, patched: eventlog, templates,
warm start, gate v3, seeding/harvest instrumentation, filter-churn
logging — every experiment's machinery remains flag-gated and
default-off; stock behavior reproduces frozen baselines exactly).

Key paths:
- `scripts/run_bench.py` — benchmark harness
- `scripts/structure.py` — blind structure recovery (+ involution emit)
- `scripts/guided.py` — gated-solver front-end
- `scripts/reproduce.py` — the 12-check reproduction suite
- `benchmarks/frozen/` — sha256-manifested M1 snapshot
