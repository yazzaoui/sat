# L0 results — calibration gate PASSED; barrier estimator failed its gate

Run per [L0-registration.md](L0-registration.md). Raw data:
[L0-results-data.json](L0-results-data.json). All numbers seeded and
regenerable; representative cells pinned in `scripts/reproduce.py`.

*(Scope reminder, per registration §1.1: all basin/barrier statements
are about the SLS landscape — V under 1-flip adjacency.)*

## The calibration gate: PASS, 100/100 cells

Random 3-XOR, identity vs Gauss-eliminated basis, densities {0.7, 0.9},
seeds 1–10:

| Probe | Cells | Plural before | Single basin after |
|---|---|---|---|
| Exact (n = 16, 20, 24) | 60 | **60/60** (68–384 basins) | **60/60** |
| Sampled (n = 40, 60) | 40 | **40/40** | **40/40** |

UNSAT instances (no planted solution; ~15% of draws) behave exactly per
the registered offset convention: single minimum plateau after basis
change. The probes see the landscape surgery on the family where the
answer is known — the program proceeds.

## Basin-count validation: PASS (after one estimator adjustment)

Sampled-vs-exact Spearman, per family and pooled (bar ≥ 0.8):

| Family | ρ | | Family | ρ |
|---|---|---|---|---|
| 16/0.7 | 0.963 | | 20/0.7 | 0.912 |
| 16/0.9 | 0.960 | | 20/0.9 | 0.76 @R=200 → **0.893 @R=500** |
| 24/0.7 | 0.945 | | 24/0.9 | 0.976 |

Pooled: **0.98**. The 20/0.9 family needed R=500 (bring-up estimator
engineering, both numbers disclosed); final probe parameters for L1 are
fixed in the L1 registration.

## Barrier estimator: FAILED its validation gate

Two-stage disclosure:

1. **v1 validation was a design error (mine):** it compared sampled
   attractor-pair barriers against the exact *all-leaf-pair* mean —
   different objects (68–384 leaves, mostly tiny; the sampler sees ≤5
   large attractors). Partial v1 numbers (0.56 / −0.57 / 0.83) are
   retained in the data file as `v1_partial_wrong_object`.
2. **Corrected like-for-like validation** (exact per-pair merge levels
   for the sampler's own attractor pairs, pooled per family):

| Family | ρ (pairs) |
|---|---|
| 16/0.7 | 0.356 (73) |
| 16/0.9 | 0.223 (62) |
| 20/0.7 | 0.468 (22) |
| 20/0.9 | 0.337 (26) |

Nowhere near 0.8: the ε-greedy first-passage max-V estimator does not
track exact merge levels even for the right pairs. **Registered
consequence (§3.2): no downstream result may rest on sampled barriers.**
L1 inherits the restriction: sampled sizes report basin counts (and
corridor *usage*, a path-event count, not a barrier magnitude — its own
calibration happens at the PHP(4) anchor); barrier claims are
exact-only (PHP(4) both views; PHP(5) projection view).

Named follow-up if barriers at sampled sizes become load-bearing:
nudged/bisection path sampling instead of first-passage max-V — would
need its own registration and validation pass. Not pursued now.

## Lex-descent disagreement check: divergence on all 60 rugged cells

Lexicographic steepest-descent basin counts exceed merge-tree counts on
every pre-basis instance (typical ~2×, e.g. 142 vs 68) — the plateau
tie-break artifact, measured at scale. Post-basis instances: both
definitions agree (1 = 1). Reported, not adjudicated, per registration;
the canonical definition passed the gate on its own terms.

## Probe cost (honesty toll #1)

Exact: n=24 ≈ seconds/instance at ~285 MB; n=26 ceiling ≈ 1.1 GB
(untested in L0, no instance required it). Sampled: R=200 basin
sampling at n=60 ≈ tens of seconds/instance (Python; port only if L1
profiling demands). Full 100-cell calibration ≈ 40 min wall clock on
one core.

## L0 verdict

Probes validated for basin structure; transition gate passed;
**program proceeds to L1** with the barrier restriction inherited and
the L1 registration (effect-size bars from this run's variance, final
estimator parameters, Cook/BVA/random toolkit) as the next document.
