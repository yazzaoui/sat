# L1 registration — H1 on pigeonhole (+ SAT siblings)

Committed before toolkit code, per cadence; lead approval gates
implementation.

## Question

H1: do known-good extension variables (Cook's construction) measurably
merge basins / connect solution clusters, where compression-selected
(BVA) and random matched-shape definitions do not?

*(Scope, in every table caption: claims are about the SLS landscape —
V under 1-flip adjacency. The CDCL bridge is L3a's.)*

## Instances

- UNSAT originals: PHP(4) [anchor], PHP(5), PHP(6), PHP(7).
- SAT siblings (lead decision #3, dual reading): PHP(n,n) for n=4,5,6;
  even-charge Tseitin (n=20, 30; seeds 1–3).
  - UNSAT reading: do good coordinates merge the trap structure of the
    refutation landscape?
  - SAT reading: do good coordinates connect solution clusters?

## Arms (per instance)

- A: baseline (no extensions)
- B: Cook-construction variables (UNSAT PHP; for SAT siblings and
  Tseitin: the known proof-relevant definitions — Tseitin: parity-chain
  definitions along the graph structure)
- C: BVA-selected, count-matched to B; degeneracy handling per lead
  decision #4 (no padding; report candidate count + best compression
  gain when empty)
- D: random definitions, matched to B in count AND shape distribution
  (Cook's shape is z ↔ a ∨ (b ∧ c) — D must match it, not z ↔ a∧b)

## Exactness (per-view, from the approved L0 accounting)

| Instance+B | Projection | Search-reality |
|---|---|---|
| PHP(4)+full cascade (20 vars) | exact | exact — anchor |
| PHP(5)+one layer (32 vars) | exact | sampled |
| all larger | sampled | sampled |

Barrier claims are **exact-only** (L0 consequence). Sampled sizes
report basin counts and corridor events only.

## Gates that must pass before any H1 reading

1. **Cook-cascade logic gate (lead check #3):** the toolkit must emit,
   for PHP(4) and PHP(5), the extension definitions plus the short
   refutation as a DRAT/PR proof, and dpr-trim must say VERIFIED
   against the original PHP formula. Arm B is not measured until its
   coordinates are proven to be Cook's coordinates *as logic*. This
   check also lands in reproduce.py permanently.
2. **Corridor-protocol calibration at the anchor (lead check #2):**
   exact ground truth for corridors exists at PHP(4)+cascade:
   corridor-gap(b₁,b₂) := merge level in the definition-consistent
   subspace (≅ projection view) − merge level in the full extended
   space. A strictly positive gap is an exact certificate that
   corridors connect the pair below the consistent barrier.
   Pass/fail: over anchor attractor pairs, (i) sampled corridor-usage
   must be positive on ≥90% of pairs with positive exact gap and zero
   on ≥90% of zero-gap pairs (classification agreement), and (ii)
   Spearman(exact gap, sampled usage rate) ≥ 0.8. Fail ⇒ corridor
   metrics get the barrier treatment (exact-only at the anchor);
   basin-count H1 readings are unaffected.
3. **Determinism/regeneration:** all instances from seeded generators;
   sampled runs at the final estimator parameters below; PHP(4)-anchor
   sampled-vs-exact validation in BOTH views added to reproduce.py
   (lead build note, registered placeholder now discharged).

## Final estimator parameters (fixed here)

Basin sampling: R=200 (density-0.7-like instances) / R=500 (0.9-like
and all PHP arms — conservative default), plateau cap 20000,
connectivity-test fallback as in L0. Corridor ensemble: registered §3.3
parameters (N=200 per pair, ε=0.1, patience 2n, cap 50n).

## Effect-size bars (numeric values from the L0 noise addendum)

Estimator noise measured at final parameters, fixed instances × probe
seeds 1–8 (`estimator_noise` in L0-results-data.json; 6/8 cells — the
interrupted pair is subsumed by the saturation finding):

| Family | mean basins_est | sd | CV | note |
|---|---|---|---|---|
| 40/0.7 | 182.8 / 197.5 | 3.7 / 2.1 | 0.020 / 0.010 | clean |
| 40/0.9 | 472.6 / 478.9 | 5.2 / 6.4 | 0.011 / 0.013 | near R=500 ceiling |
| 60/0.7 | 199.9 / 200.0 | 0.35 / 0.00 | ≤0.002 | **saturated at R** |

Reading: unsaturated estimator noise is CV ≤ 0.02; estimates at or
near R are saturated lower bounds whose variance is artificially small.

**Saturation guard (pre-registered adaptive rule, not tuning):** before
any inter-arm comparison at a sampled size, if any arm's basins_est
exceeds 0.5·R, double R and re-estimate (all arms of that instance,
same probe seeds), repeating until all arms are below 0.5·R or R hits
8000; if the ceiling is hit, that cell reports saturated lower bounds
and is excluded from bar evaluation (reported, not silently dropped).

Bars:
- **Sampled basin counts:** arm B's estimate must lie below EACH of
  A, C, D by more than max(3·(0.02·Â), 0.10·Â) — with unsaturated
  CV=0.02 the 10%-of-A floor dominates, so effectively **B must be
  ≥10% below every other arm** — at every sampled size, with the
  deficit non-shrinking as size grows (trends-over-size required,
  spec toll #4). Â = arm A's estimate at that size.
- **Exact basin counts (PHP(4), PHP(5)-projection):** strict counts;
  B < min(A, C, D) with reduction ≥ 20% vs A (pre-hoc materiality
  threshold; no noise term exists).
- **Exact barriers (anchor sizes only):** B's barrier_mean ≤ 0.8 × A's,
  and ≤ each of C, D (20% pre-hoc materiality).
- **SAT siblings:** B's solution-cluster count < min(A, C, D) with the
  same noise-guarded margin at sampled sizes.

## Pre-registered readings (from SPEC, sharpened)

- **H1-supported:** B clears the bars; C and D do not (C may show
  partial effect — see confounded).
- **H1-refuted-cleanly:** B ≈ C ≈ D ≈ A within noise on all probes and
  all instances ⇒ "ER's power on PHP is not visible as basin geometry
  of the SLS landscape." Publishable boundary sentence; program
  branches to L2 only if the lead elects the second family anyway.
- **Confounded:** B differs but C matches B ⇒ compression and
  basin-merging coincide on PHP; disentangle on Tseitin before any H1
  claim (already in-scope via the siblings).
- **Split (new, enabled by decision #3):** H1 holds on SAT siblings
  but not UNSAT originals (or vice versa) ⇒ a finding about *where*
  ER's geometric signature lives; report as such.

## One run per registered cell; no tuning after bars are set; every
## deviation is a written amendment committed before affected runs.
