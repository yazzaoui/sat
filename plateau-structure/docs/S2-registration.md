# S2 registration — precise definitions, measured feasibility, bars

Committed before any structure computation. Feasibility below measured
sizes and costs ONLY — no merge trees, no correlations were computed
before this document (no structure peeking before bars).

## 1. Canonical objects

- **Plateau (S2a):** the V-minimal level of an UNSAT instance,
  analyzed as the induced subgraph under 1-flip adjacency (all
  components if plural — random instances may have several).
- **Exit level (S2b):** the V=1 level of a satisfiable instance;
  **exit state** := a V=1 state adjacent to some V=0 state.
- **Refined structure:** the canonical merge tree (persistence, leaves
  with persistence > 0, merge levels) of V₂ restricted to the plateau
  subgraph. Identical machinery to L0; only the altitude changes.
  Ties inside V₂ handled by the same plateau-component semantics as
  the primary probe (no tie-breaking, per canon).

## 2. Candidate V₂ — precise, frozen

For full assignment x; SAT(c,x) = satisfying literals of clause c:

1. **exposure(x)** = Σ_{c: |SAT(c,x)|≥1} 1/|SAT(c,x)| — computed in
   exact rational arithmetic (fractions), no float ties.
2. **critical(x)** = #{c : |SAT(c,x)| = 1}.
3. **decidedness(x)** = |UP-closure on F of A(x)| where
   A(x) = {l : l is the unique satisfying literal of its clause} —
   one propagation call per state; higher = region more logically
   committed. (This freezes the frame's "propagation potential" to a
   single computable form; no alternatives will be substituted.)
4. **mobility(x)** = #neighbors of x with equal V (in-menu control).

## 3. Instances (all exact; no sampling anywhere in S2)

| Substrate | Role | Level size (measured) |
|---|---|---|
| PHP(4) min level (V=1) | S2a | 60 |
| PHP(5) min level (V=1) | S2a | 360 |
| r3(n=24, m=96) seeds 3,4,7,9 (UNSAT) min levels | S2a generalization | 43 / 553 / 479 / 89 |
| PHP(4,4) V=1 level | S2b | 816 (24 solutions) |
| PHP(5,5) V=1 level | S2b | 7,200 (120 solutions) |
| r3 seeds 1,2,5,6,8,10 (SAT) V=1 levels | S2b generalization | 104–503 |

V₂ evaluation cost (measured, Python, per state): exposure 9 µs,
critical 8 µs, decidedness 42 µs, mobility ≈ n·V-eval. Worst object
(7,200 states × decidedness) ≈ 0.3 s. **Feasibility verdict: trivial
everywhere; pure-Python probes; no C changes; no sampling.** The
frame's stated toll (candidate-3 cost) is measured and immaterial at
these sizes.

## 4. Bars (in writing, before any run)

- **S2a structured (per candidate, per instance):** the V₂ merge tree
  on the plateau has **≥ 3 leaves** with persistence > 0, AND leaf
  count ≥ **2× the mobility control's** leaf count on the same
  plateau. A candidate is *structuring* if it clears on ≥ half its
  S2a substrates **including at least one random UNSAT instance**
  (PHP-only structure = presumed symmetry artifact, reported as
  split verdict).
- **S2b useful (evaluated for structuring candidates; others
  reported descriptively):** primary = |Spearman(V₂, plateau-graph
  distance to nearest exit)| ≥ **0.5** on each S2b substrate class
  (siblings; random SAT), sign REPORTED as part of the finding
  (direction is not assumed a priori). Distances are exact BFS within
  the level subgraph; states in components containing no exit are
  reported separately (unreachable-exit mass).
- **UNSAT S2b: registered as NOT MEASURABLE** — no exits exist below
  a minimal level; no proxy is registered (the honest option the
  frame allows). Any future proxy is an amendment.
- **Noise floor:** the mobility control's own S2b correlation is
  reported; a structuring candidate whose |ρ| does not exceed the
  control's |ρ| fails S2b regardless of the 0.5 bar.
- One run per cell; menu frozen; amendments in writing before
  affected runs.

## 5. Deliverables

Per-instance: leaf counts, persistence distributions, merge summaries
for all four candidates; S2b correlation table with signs; per-family
split verdicts; every number in plateau-structure reproduce.py;
ledger sentence per branch at closure. Time-box: two weeks (expected
well under).
