# P1 results — the awkward branch, in its strongest possible form

Run per registration + canon engine (see Conformance below). All
numbers exact (exhaustive computation, no estimators). Raw:
[P1-results-data.json](P1-results-data.json).

## Numbers (sibling anchor, PHP(4,4)+layer-1, 2²⁵ states)

| Arm | mean NET | mean gain | mean loss | terminal SCCs |
|---|---|---|---|---|
| A (self-test) | **0.0 exactly** | 0 | 0 | 24 |
| B (Cook-schema) | +3.5027·10⁻⁴ | = gain | **0** | 24 |
| C (BVA) | **degenerate: 0 candidates** with positive gain on PHP(4,4) — the registered "BVA found nothing to do" data point, in full | — | — | — |
| D seeds 1–3 (matched random) | +3.5027·10⁻⁴ | = gain | **0** | 24 |

B and D agree to machine precision because the number is a
**combinatorial identity**, verified exhaustively from the mask files:

- Baseline: every non-solution state reaches ALL 24 solutions
  (65,512 = 2¹⁶−24 states with full masks); each solution reaches only
  itself. (The plateau discovery, in reachability form.)
- Coupled (B and D identically): every state except the 24 consistent
  lifts reaches ALL 24 lifts (33,554,408 = 2²⁵−24); zero states reach
  none.
- Therefore per solution: gain = the stale dressings of the OTHER 23
  solutions = 23 × (2⁹−1) = **11,753 states exactly**; loss = 0
  (mines never sever set-valued reachability here).

**NET(s) = 23·511/2²⁵ for every solution and every definitional arm:
the entire coupled-move effect at the anchor is "staleness unlocks the
other solutions' dressings" — a counting identity, blind to which
definitions produce it.**

## Verdict against pre-registered bars

- NET(B) > 0 ✓, but NET(B) − max-seed NET(D) = **0 < δ**: the
  pre-committed awkward branch fires — **definition-generic, not
  Cook-specific; H1-successor NOT supported.** Not by magnitude
  proximity but by bit-for-bit identity with a formula in hand.
- The formal kill bar (NET < 0 ∧ no separation) does not fire; the
  frame's "modest or null structure" branch is realized with an exact
  mechanism instead of a null.
- Stale repulsion (P0's mine mechanism) is real for deterministic
  walkers but never disconnects set-valued reachability at this size:
  loss ≡ 0. The mines bend paths; they sever nothing.

## Theorem F (anchor-exact; conjectured general)

Verified exhaustively at the anchor: if (i) the baseline V ≤ 1 level
set is connected with all solutions on its boundary (the plateau
structure) and (ii) every non-lift extended state has a non-increasing
escape (checked: zero reach-nothing states), then coupled basin of
every lift = everything except the other consistent lifts, hence
NET ≡ (k−1)(2^m −1)/2^(n+m) for k solutions and m definitions —
independent of definition content. Stated as proven-at-anchor
(exhaustive verification IS the proof there), conjectured for
plateau-connected instances generally; no general proof attempted
(scope rule).

## Conformance note (process, disclosed)

The first engine implementation deviated from P0 canon (it repaired
input-touched definitions that were violated, rather than only those
that BECAME violated — near-eager dynamics). Caught by the suspicious
cross-arm identity before any reporting; fixed; the three P0
micro-example behaviors (staleness persistence, accidental repair,
irreversibility) are now permanent engine-level checks in
reproduce.py. The post-fix numbers are identical — the identity is
structural, not an artifact of the deviation — but the canon engine is
the one on record.

## UNSAT anchor

Explicitly non-evidential per registration; deferred — the sibling
verdict fires the branch on its own, and the descriptive cell adds
mechanism illustration only if the lead still wants it.
