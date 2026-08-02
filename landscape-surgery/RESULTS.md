# Landscape-surgery results index

Status: **no results yet** — this index is the scaffold every phase
fills in. A phase row gets its verdict only from a pre-registered run;
registrations are linked the moment they are committed, before any run.

| Phase | Question | Registration | Verdict |
|---|---|---|---|
| L0 | Do the probes see the XOR-SAT smoothing? (calibration gate) | [L0-registration](docs/L0-registration.md) | **PASS 100/100 cells; basin validation ρ=0.98 pooled; barrier estimator FAILED its gate — L1 restricted to exact barriers** ([L0-results](docs/L0-results.md)) |
| L1 | H1: do good extension variables merge basins / connect solution clusters (vs BVA / random / baseline; UNSAT originals + SAT siblings)? | — | — |
| L2 | Is basin-merging a general signature or PHP-specific? | — | — |
| L3a | Do good coordinates alone help search (the ER-transfer puzzle)? | — | — |
| L3b | Does probe-guided selection beat BVA under matched budgets? | — | — |

Standing bars inherited from SPEC §3.1/§6: sampled-probe validation
gate (rank correlation vs exact, bar registered in L0 before use);
size-honesty (exact capped at n ≤ 26, trends over size required);
scoring-cost accounting defined in the L3b registration.
