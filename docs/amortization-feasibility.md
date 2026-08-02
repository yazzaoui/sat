# Amortization feasibility: consecutive reducts are nearly identical

Directive: quantify consecutive-reduct overlap from existing logs before
building anything. Method: unfiltered positive reducts reconstructed
from logged trails (`scripts/reduct_overlap.py`); the filtered reduct is
a subset, so shared-structure fractions are a faithful proxy (caveat
recorded). No solver runs; data = Experiment C's C0 eventlogs.

| Instance | attempts | lag-1 shared clauses (med/mean/p10) | var overlap | trail Δ (med) |
|---|---|---|---|---|
| mchess14 | 15,653 | **0.96** / 0.86 / 0.53 | 0.90 | 8 lits |
| mchess12 | 5,138 | 0.95 / 0.86 / 0.52 | 0.90 | 8 lits |
| tseitin40 | 17,500 | 0.93 / 0.89 / **0.80** | 0.93 | 3 lits |

Decay is slow: mchess14 still shares 60% (median) at lag 50.

## Decision

Overlap is high across both families — **the persistent-inner-solver
experiment is warranted and gets registered next.** Consecutive hunts
currently pay full price for inner problems that are ≥90% identical;
the boundary map explicitly permits amortization (reuse moves no
information between inner and outer — it stops re-buying the shared
part).

## Technical notes for the registration

- The clean formulation is an incremental inner solver: reduct clauses
  under activation literals, trail literals as assumptions. This keeps
  inner learned clauses valid across calls by construction (they carry
  their activation dependencies) — naive clause retention across
  changing reducts is unsound and must remain structurally impossible,
  same rule as Experiment C's clause-transfer exclusion.
- Prediction to register against: reduct build + solve cost per attempt
  should drop toward the delta size (~4–10% of clauses); the witness
  itself remains inner-authored, so steering is untouched by design —
  the amortization claim is about cost, and downstream conflicts must
  stay within noise of stock (that is the safety bar, not the win bar).
