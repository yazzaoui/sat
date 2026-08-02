# Phase 2 chessboard results vs pre-registered bars

Judged against `phase2-preregistration.md` (committed before experiments).
All runs dpr-trim VERIFIED; the one soundness bug hit during development
(template acceptance ignored the reduct's incremental UP inconsistency)
was caught immediately by the dpr-trim gate and fixed — the gate works.

## In-solver engine

Patched SaDiCaL: `--template=<file>` loads structure-derived involutions
(swap/flip variable pairs); `prune()` tries them deepest-decision-first
against the positive reduct before the inner SAT solve; partial
application (unassigned partners inert) with the reduct check as sole
gate; `--templatetries` budget. Accept events carry `via: template|reduct`.

## Results

| Metric (pre-registered) | Bar | Outcome |
|---|---|---|
| PHP(10) template hit share | — | **100%** of accepts via template, trajectory unchanged, verified |
| mchess(14) hit share, budget 1024 | ≥60% | **58%** — just under bar; plateaus |
| mchess(16) hit share | ≥60% | 47% — declines with size |
| mchess(16) wall clock | beat stock 7.5 s | **91 s — loses 12×**; conflicts 3.3M vs 1.0M |
| Kill criterion | templates beat stock acceptance | **not met on chessboard** |

## Reading (the informative-number branch)

1. **The taxonomy is fully predictive on PHP** (100% in-solver hit share)
   and majority-predictive on chessboard (58%), so it is not merely
   descriptive — but predictivity declines with size exactly where the
   atlas said the parallel-exchange / long-cycle tail grows.
2. **Static geometric enumeration is the wrong proposal mechanism for
   tilings.** Witnesses live on the *dynamic* assigned-domino structure:
   alternating cycles of the current partial tiling, which are not
   rectangles enumerable offline. The matching-theoretic proposal —
   walk alternating assigned/unassigned edges from the conflict cell at
   the stuck point — is the identified next mechanism (per-stuck-point,
   in C, radius-bounded by the atlas locality result).
3. **Template-steered trajectories degrade CDCL search** (conflicts 3×
   even at equal acceptance): SaDiCaL's flip-bump ordering ("highly
   important for performance" per the source comment) receives a 4–8-flip
   template witness instead of the inner solver's ~10-flip solution and
   the balance/restart heuristics interact badly. Witness *choice* — not
   just witness *existence* — is a search-control input. This is a
   finding the Phase 3 ranker framing should absorb: rank witnesses by
   downstream trajectory quality, not just validity.

## Competition coverage sweep (22 instances, SATLIB)

| Class | Coverage | Note |
|---|---|---|
| flat100 graph coloring (5) | **100%** | pure counting; labels fire |
| logistics planning (4) | 38–55% | counting-heavy; labels fire on 2/4 |
| BMC hardware verification (13) | 4–22% (median ~13%) | XOR + AMO islands in untyped circuit soup |

Templates have a real market in coloring/planning-style instances; BMC
needs circuit-level detectors (gate/ITE patterns) before this approach
reaches it.
