# S4 P1 registration — the selection loop

Committed before loop code. Gate restated per P0's operator split
(lead-approved). Greedy is the SOLE selector — no beam, no fallback
selectors; if greedy misses a bar, that is a verdict, not an
invitation to shop for search strategies (lead directive). The
canonical-order spike (68→104 before descending) is kept visible
here as the reason op ORDER is part of the terrain: the loop's
sequencing is greedy-local by design, not textbook-order.

## Loop (fixed)

From identity basis: at each step, evaluate the score for every
candidate elementary op applied to the current move basis
(Ainv ← E(i,j)·Ainv); take the strict best; stop when no op improves.
Score = exact basin count of (V, basis-moves) via `exact --basis`
(Theorem G: V unchanged, masks only). Exact scoring throughout P1 —
the sampled-estimator question is deferred entirely (no sampled
claims in this phase).

**Per-step accounting instrumentation from the start (lead
requirement):** score evaluations per step, wall-clock per evaluation
and per step, cumulative totals — logged in the run JSON alongside
basin numbers. P2's conservation-law verdict consumes this curve.

## Candidates

- **Blind:** all n(n−1) elementary ops per step.
- **Informed:** ops restricted to variable pairs co-occurring in XOR
  constraints detected by the witness-search structure tool
  (`find_xors`, resurrected as candidate generator), plus pairs
  sharing a detected chain. Registered comparison: endpoints AND
  evaluation counts. If only informed works, "the compass reads maps
  but cannot explore."

## Instances (all exact; feasibility from P0 timings)

1. **Pure XOR (rediscovery gate):** n=16, m=14, seeds 1–5 (anchor =
   seed 1). Cost: ~240 evals × ~5 ms ≈ 1.2 s/step, ≤ ~8 steps.
2. **Hidden-XOR CNF (THE decision cell):** long parity constraints
   (width 6) Tseitin-split into 3-XOR chains with auxiliary variables,
   CNF-encoded; n_total ≤ 20 (originals 12 + aux ≤ 8), seeds 1–5.
   The compass must find basis ops mixing original and auxiliary
   variables without being told the chains exist.
3. **Mixed CNF+XOR:** random 3-CNF at α=2.0 (on the non-XOR vars) +
   XOR fraction φ ∈ {0.25, 0.5, 0.75} of constraints, n=16,
   seeds 1–3 per φ.
4. **Pure random CNF (negative control, Theorem-H-sharpened):** n=16,
   α=3.5, SAT seeds, 5 instances. A basin signal here would certify
   algebraic structure in the distribution; the registered expectation
   is null.

## Controls (per instance)

- Identity (initial basin count).
- Random elementary compositions: 10 sequences, length matched to
  greedy's step count for that instance; **greedy's endpoint must
  beat the MINIMUM (best) random endpoint** (S1/P1 strictness
  convention).

## Bars (pre-run)

- **Rediscovery gate:** on the anchor, the loop must reach ≤ 12
  basins (P0's greedy measurement — the gate verifies the loop
  implementation reproduces what the measurement found); on XOR seeds
  2–5, endpoint ≤ 0.25× identity (≥75% reduction) with a monotone
  path.
- **Hidden-XOR (decision):** blind greedy endpoint ≤ 0.5× identity
  (≥50% reduction) on ≥ 4 of 5 seeds AND beats best-random on each.
  Fail ⇒ the compass cannot discover hidden parity structure blind —
  the constructive claim dies at its central cell.
- **Mixed:** reduction expected to grow with φ; reported as a curve
  (descriptive; no bar).
- **Pure CNF:** endpoint ≥ 0.9× identity (≤10% reduction) on ≥ 4 of
  5 — the expected null respected; violation = Theorem-H-certified
  structure surprise, reported as such (not a win).
- **Blind-vs-informed:** informed matching blind's endpoints with
  fewer evaluations = efficiency note; informed succeeding where
  blind fails = "reads maps, cannot explore" verdict on the compass.

One run per cell; deviations by written amendment; every headline in
reproduce.py; ledger sentence at stream closure.
