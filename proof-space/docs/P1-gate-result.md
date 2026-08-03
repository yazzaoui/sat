# P1 distinguishability gate — final result (stream-closing)

The gate registered in [P1-registration.md](P1-registration.md) asked,
before any main run was allowed: does ANY registered observable of the
derivability-wavefront space (Q1 depth of ⊥, Q2 geodesic-DAG size, Q3
wavefront volumes) separate T_Cook = PHP + Cook's cascade from
T₀ = PHP, with the predicted sign, at ≥ 20%, at the PHP(4) anchor or
the one registered escalation PHP(5)? Verdict: **no — P1 closes at the
gate.** Ledger entry 10 records the stream (Ending 1, negative form).

## Measured cells

All numbers exact (fixpoint depth-DP, subsumption-aware, width = the
minimal joint refutation width per the registered rule). C probe
(`probes/depthdp.c`) cross-validated against the Python reference on
every shared cell; chunked checkpoint runs verified identical to
single-shot. Every number: `python3 scripts/reproduce.py [--slow]`.

### PHP(4) anchor — concluded, every quantity fails

| Cell | Q1 depth(⊥) | antichain | Q2 geodesic | Q3 fronts |
|---|---|---|---|---|
| w=3 T₀ | 8 | 801 | 641 | [22,36,72,240,108,84,66,12,1] |
| w=3 T_Cook | 7 (−12.5%, < 20%) | 2,443 | **1,207 (1.9× — wrong sign)** | wider at every level |
| w=4 T₀ | 7 | 1,431 | 1,031 | [22,36,234,456,228,42,12,1] |
| w=4 T_Cook | 7 (0%) | 6,622 | **3,240 (3.1× — wrong sign)** | wider at every level |

Q2's predicted sign was Cook SMALLER (the polynomial upper bound's
shadow); measured: larger, both widths. Q3 fronts widen at every
level. Cook's definitions leave depth essentially unchanged and
enlarge every size quantity.

### PHP(5) escalation — baseline concluded; ER cell out of exact reach

| Cell | result |
|---|---|
| w=3 T₀ | frontier **closes**, no ⊥ (antichain 45) — the Ben-Sasson–Wigderson width landmark behaving natively in the space |
| w=3 T_Cook | frontier **also closes**, no ⊥ (antichain 1,181 — 26× T₀'s closed front, still no refutation) |
| w=4 T₀ | depth 13, antichain 13,011, geodesic 8,296, waves [45,80,360,480,2280,960,1560,1320,240,260,500,190,20,1] |
| w=4 T_Cook | **computationally infeasible — measured, not estimated**: live antichain 2.4k → 12k → 56k → 145k → 179k through forward round 6 of ≤ 13, per-round cost quadratic in that count; remaining rounds + geodesic pass project to days. Checkpoint state preserved: [`data/php5_cook_w4_state.bin`](../data/php5_cook_w4_state.bin) (resume: `probes/depthdp --state <file> --rounds k`) |

The escalation cell's own front growth is the finding: the ER theory's
wavefront volume — the size-shadow the lead flagged at registration as
the quantity that had to carry the separation if depth couldn't — is
what pushes the cell beyond exact computation, in the overhead
direction.

## Width-relief annotation (ledger entry 10)

The closure sentence banked a descriptive finding: "the definitions'
only in-space finite-size value is width-relief (T_Cook refuting where
T₀'s width frontier closes)." **Measurement contradicts it**: at the
only cell it can refer to (PHP(5) w=3, where T₀ closes), T_Cook's
frontier also closes without ⊥ — 1,181 clauses of front against T₀'s
45, and no refutation. At every measured width the cascade relieves
nothing; the overhead sign holds even where nothing refutes. Flagged
to the lead for emendation; recorded as an annotation on entry 10.

## Verdict (registered rule, applied mechanically)

No quantity passes at either anchor. Per the registered rule, P1
closes at the gate: **no registered observable separates ER from
resolution at exactly measurable scales** — PHP(4) measured on all
quantities (failing with the overhead sign), PHP(5)'s ER cell beyond
exact computation under the canonical space. Sixth measured instance
of the program's finite-size inversion: the asymptotic advantage's
machinery is pure overhead below its crossover.

The main-phase apparatus (full 2⁸ theory lattice, shape-matched random
controls, screen-vs-dynamics walk) was never built — the gate existed
to prevent exactly that spend on a non-separating observable, and it
fired.

Historical note: the mid-cell stop-and-report that triggered the
lead's closure decision is preserved verbatim in
[P1-gate-interim.md](P1-gate-interim.md).
