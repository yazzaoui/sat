# Experiment A results: conflict-analysis-reuse witness seeding

Run exactly as pre-registered (docs/phase3-preregistration.md): mchess(14),
one run per variant, no variant iteration. Stock reference reproduces the
frozen M1 conflict count exactly (279,631 — determinism confirmed). All
four proofs dpr-trim VERIFIED.

| Run | Outer conflicts | ×stock | Wall | Accepts | Inner conflicts |
|---|---|---|---|---|---|
| stock | 279,631 | 1.00 | 1.76 s | 2487 | 2214 |
| A1 order-seeding | 466,476 | **1.67 — harm** | 2.98 s | 3382 | 3748 |
| A2 phase-seeding | 427,512 | **1.53 — harm** | 3.05 s | 3210 | 4434 |
| A3 both | 303,266 | 1.08 — no-harm band | 2.27 s | 2816 | 2317 |

## Verdict against pre-registered bars

- No variant reached the win bar (≤ 0.9×). A1 and A2 individually harm
  (≥ 1.5×); A3 lands in the no-harm band but its secondary metric also
  fails — inner-solve cost is not reduced (2317 vs 2214 inner conflicts),
  so there is no "cheaper witness search" claim either.
- The formal kill line (all three > 1.5×) did not trigger, but the
  pre-committed interpretation for a no-win outcome applies:

**The strong claim stands, measured: witness quality is computed by the
reduct search itself and is not seedable — even from the outer solver's
own conflict-analysis, the cheapest trail-aware signal in existence.**
The amnesia boundary now has an empirical floor: static cores fail
(four template integrations), and trail-aware-but-cheap guidance fails
(this experiment). What remains above the boundary is the full reduct
solve — SDCL's sub-solver call buys a witness and a relevance
measurement, and neither product can be substituted at lower cost by any
mechanism tested.

Curious non-registered observation (recorded, not pursued): A1 and A2
harm individually yet nearly cancel when combined — consistent with
order- and phase-guidance each dragging the inner search off its natural
path in ways that partially undo each other. Not evidence of a win; no
follow-up variants per the pre-commitment.

## Consequence for Experiment B

B proceeds as pre-registered (cost prediction from static core
features). A's null means B's middle outcome (AUC 0.6–0.7) has no
consumer and only the clean outcomes matter: AUC ≥ 0.7 (usable prior)
or < 0.6 (final confirmation that witness quality is opaque to static
features — closing the Phase 3 question with two pre-registered nulls).
