# Experiment E (amortization: persistent inner solver) — pre-registration

Committed before implementation. Feasibility basis:
`amortization-feasibility.md` — consecutive reducts share 93–96% of
clauses (median), trail deltas 3–8 literals, 60% overlap at lag 50.

## Where the danger lives (lead, verbatim intent)

The subtle risk is not soundness — activation literals handle that — it
is a **confound with the mechanism theorem**. A persistent inner solver
accumulates state (activities, phases, learned clauses) across hunts:
later reduct solves are no longer memset-fresh, and the boundary map
says witness intelligence is computed fresh at each stuck point. E
changes the conditions of that computation. Therefore:

1. **The safety bar is the PRIMARY bar**: downstream conflicts within
   [0.95×, 1.05×] of stock on all three chessboard sizes (steering
   unchanged). If persistence shifts witness choice enough to move
   steering, that is a mechanism finding (interesting) AND a failure of
   the cost-only claim — the two must not be blurred in the report.
2. **Attribution metric required**: per-hunt inner-solve cost split
   warm/cold over hunt sequence position. The cost claim must show the
   shape of amortization (early hunts full price, later hunts cheap) —
   a flat aggregate with redistributed cost must not masquerade as a
   win.

## Bars (one run per arm, C0-style determinism gate, proofs verified)

- Primary (safety): downstream conflicts ∈ [0.95×, 1.05×] stock,
  mchess(12,14,16).
- Win: total inner-solve time ≤ 0.5× stock with primary held. (The
  overlap numbers say 2× is conservative; the bar is not inflated to
  match the hope.)
- Informative-failure branches, pre-named:
  a. steering shifted (outside primary band) → mechanism finding;
     E fails as engineering. Report both halves separately.
  b. assumption-management overhead eats the savings (the classic
     incremental-SAT tax) → measured and reported honestly.
- Second family: tseitin(30,40,50) same bars, reported separately.

## Mechanism (fixed before implementation)

- Persistent inner solver across hunts; identity variable mapping
  (inner var = outer var index).
- Per-clause activation: reduced clause r gets activation literal a_r
  on first appearance, stored persistently (`r ∨ ¬a_r`); a hunt's reduct
  = assumptions {a_r : r in current reduct} (+ banned-decisions clause,
  per-hunt activated). ~96% of a hunt's activations are cache hits.
- Assumptions implemented as forced first decisions in the inner solve;
  conflict at-or-below assumption level = reduct-UNSAT. Learned clauses
  carry negated activation literals by normal resolution, so validity
  across hunts holds **by construction** — naive clause retention
  remains structurally impossible (Experiment C's exclusion rule, kept
  structural).
- Deactivated/stale cached clauses garbage-collected under a cache cap
  (LRU); cap fixed before runs, not tuned.

## Cost-structure fact shaping implementation

Measured: inner solves are propagation-dominated (2,214 total inner
conflicts across 6,574 hunts at mchess14) — the hunt's price is reduct
CONSTRUCTION + CLAUSE LOADING, not search. Amortizing solver state
alone cannot reach the win bar; the per-clause cache (skipping re-load
of the ~96% shared clauses) is the load-bearing mechanism. The O(|F|)
satisfied-clause scan per hunt must also become delta-driven (occurrence
lists over the 3–8 changed trail literals) or it becomes the new floor.

## Scope rule

Same as Experiment C: if the patch outgrows a bounded implementation
effort, stop and report the blocker rather than engineering around it —
an oversized diff on a 2018 codebase is itself information (the honest
alternative is porting the experiment to an incremental-SAT-native
inner engine, which is a different registration).
