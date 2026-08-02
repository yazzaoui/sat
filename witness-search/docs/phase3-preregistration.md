# Phase 3 pre-registered experiments

Committed before either experiment runs. Ordering per lead review:
Experiment A (conflict-analysis-reuse seeding) precedes B (cost
predictor) — A is the sharpest test of the weakened thesis and either
outcome is decisive; B risks a mushy middle without A's result in hand.

Context: four failed template integrations (direct, warm, filter,
largest-first) shared *static* cores. The triangulated conclusion is
"witness search resists amnesia," not "resists cheapening." The untested
quadrant is trail-aware-but-cheap proposal. The outer solver's own
conflict analysis is the cheapest trail-aware signal in existence
(already computed by the learned-clause machinery).

## Experiment A: conflict-analysis-reuse witness seeding

Mechanism: at each prune, seed the inner reduct solve with guidance —
never constraints — from the outer solver's most recent conflict
analysis: the variables of the last learned clause / analyzed set,
mapped into the reduct. Three variants, each tried once (no tuning
fishing):
  A1: inner decision-order seeding (analyzed vars decided first)
  A2: inner phase seeding (analyzed vars phase-initialized to flip of α)
  A3: both

Bars (mchess(14), all runs verified):
- Primary: downstream outer conflicts vs stock 280 K.
  Win ≤ 0.9×; no-harm band 0.9–1.1×; harm > 1.1×.
- Secondary (only at no-harm-or-better): inner-solve cost per accept
  (conflicts, time) vs stock — the "cheaper witness search" claim.
- Kill: all three variants > 1.5× stock ⇒ stop; no variant iteration.

Pre-committed interpretation:
- If even the solver's own entanglement analysis cannot seed useful
  witnesses, the strong claim stands *measured*: witness quality is
  computed by the reduct search itself and is not seedable — publish as
  the boundary result.
- If a variant wins, Phase 3's mechanism is learned seeding (learn what
  to seed, from event logs), not witness ranking.

## Experiment B: cost-prediction pilot (after A) — RETIRED, NOT RUN

Retired by lead decision (2026-08-02) after Experiment C closed the
boundary map: witness choice must remain untouched and nothing usefully
crosses the inner/outer boundary, so a core-feature quality predictor
has no remaining consumer for any outcome — and a registered experiment
with no consumer for any outcome must not run (the discipline applied
to ourselves). A spiritual successor may be re-registered as
failure-time prediction with early-abort as the named consumer and its
own bars. The registration below is preserved unedited for the record.

Frame: cheap prediction of downstream cost from static core features —
a weak predictor is still a proposal-ordering prior; a null is mechanism
confirmation, not failure.

Data: frozen M1 event logs + current logs. Per accept: flip-core
features (size, radius from stuck region, pattern class, overlap,
clause size) → outcome label: outer conflicts accumulated until the
next accept (cost proxy), binarized at the per-instance median.

Bars:
- Usable prior: AUC ≥ 0.7 (held-out instances within family).
- Pre-committed null: AUC < 0.6 ⇒ "witness quality is not predictable
  from static core features" — confirms the mechanism story, publish.
- Middle (0.6–0.7): report as weak signal; only usable if A won (as a
  tie-breaker for seeded proposals), otherwise shelve.

Alternative kept on the table regardless of B: learn to *bias the
reduct solve* (initialization, activity seeding) — steering the process
that computes quality rather than second-guessing its output. A's
variants are the hand-crafted version; a learned version is the Phase 3
main line if A shows any signal.
