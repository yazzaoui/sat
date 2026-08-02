# Experiment C (harvest) results

Run exactly as pre-registered (phase3-experiment-c-preregistration.md).
C0 determinism gate: PASS — frozen conflict counts reproduced exactly on
all three chessboard sizes, certifying both determinism and zero behavior
change at `--harvest=0`. All 28 UNSAT proofs dpr-trim VERIFIED — the
patch never touched soundness-relevant state.

## Primary family (chessboard), conflicts ×C0

| size | C0 | C1 fail-harvest | C2 succ-harvest | C3 both |
|---|---|---|---|---|
| 12 | 39,848 | **2.48×** | 2.44× | 2.45× |
| 14 | 279,631 | **1.61×** | 1.15× | 1.88× |
| 16 | 1,008,742 | **3.15×** | 1.45× | 2.57× |

C1 ≥ 1.15× on 3/3 sizes → **pre-registered HARM branch.**

## Second family (Tseitin) — informative asymmetry

| size | C0 | C1 | C2 | C3 |
|---|---|---|---|---|
| 30 | 7,316 | 1.00× | **43.5×** | 24.0× |
| 40 | 162,220 | 0.99× | 5.57× | 0.74× |
| 50 | 25,868 | 1.000× (identical) | 1.77× | 1.77× |

C1 is exactly neutral on Tseitin (identical trajectory at n=50 despite
809 transfers) while C2 is severely harmful — the mirror image of
chessboard's ordering. Transfers only bite where the outer solver is in
a queue-consulting mode at that point in search; the direction of the
effect when they do bite is consistently harmful or neutral, never
helpful.

## Controls

- PHP(12) canary: C1 ≡ C0 exactly (487 conflicts; failed reduct solves
  are propagation-only, so nothing to harvest — the built-in no-op check
  passed). C2/C3 performed 372 transfers with zero trajectory change:
  in PHP-heuristic decision mode the outer queue is not consulted.
- uf100 random: C1 neutral (1.01×). C2/C3 swing wildly (0.22×–0.51×) —
  single-run SAT-instance variance, reported as noise, not effect.
  (Correction recorded: the M2 sweep's uf SaDiCaL timings were parse
  failures, not solves — SATLIB header quirk; corrected rows in
  benchmarks/results/uf_correction.log. SaDiCaL genuinely struggles on
  uf250 (>120 s) where CaDiCaL takes 0.01 s.)

## Secondary metrics (logged regardless, per registration)

- Transfer volume: plentiful (7,314 fail-transfers at n=14; 38,350 at
  n=16) — the "underpowered mechanism" reading is excluded.
- Post-harvest windows (mchess14): C0 windows after failed solves
  average 30.6 conflicts (vs 10.8 elsewhere — failures cluster in hard
  regions, as expected). C1's same windows: 37.6 (+23%), other windows
  14.3 (+32%). Harm is uniform, local and global. The Experiment D
  trigger (C1-null with local improvement) does NOT fire.

## Boundary statement (committed framing, harm branch)

**Inner relevance is locally scoped; exporting it misleads the outer
ordering.** Combined with Experiment A: steering information neither
seeds inward nor harvests outward. The reduct solve's two products —
witness and relevance measurement — are inseparable, non-exportable,
and non-importable: the witness search's value is entirely consumed at
the stuck point where it is computed. The boundary map is now closed on
all four tested edges (static cores in, trail-aware guidance in,
activity out on failure, activity out on success).
