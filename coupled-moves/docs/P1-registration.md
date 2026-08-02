# P1 registration — net conductance under lazy-propagation dynamics

Committed before any probe code, per cadence; lead approval gates
implementation. Object of study: the P0 survivor (lazy propagation,
full-V altitude, stale-inclusive state space; canonical move rule and
terminal-SCC attractors as fixed in P0-formalization.md).

## 1. Primary quantity: net conductance (lead directive, formalized)

For a base solution s (siblings) let σ(s) = (s, f(s)) be its consistent
lift. Over the canonical start ensemble U = uniform on ALL extended
states (x, z) — the generic, stale-typical initial condition of real
local search:

- **corridor_gain(s)** = Pr_U[ σ(s) reachable in the descent digraph
  G↓ from (x,z), AND s NOT reachable from x in the baseline descent
  digraph ] — mass that reaches s only through stale routes.
- **mine_loss(s)** = Pr_U[ s reachable from x in baseline, AND σ(s)
  NOT reachable from (x,z) in G↓ ] — mass the staleness altitude
  pushes off routes that existed in baseline.
- **NET(s) = corridor_gain(s) − mine_loss(s).**

Identity (exact, no double counting): NET(s) equals the coupled basin
fraction of σ(s) minus the baseline basin fraction of s. The two
mechanisms are the exact decomposition of the basin-mass delta —
"corridors minus mines" is not a metaphor but an equation.

Arm scalar: mean NET over solutions (per-solution table also
reported). Reachability is set-valued (tie-break-free). Structural
sanity check: **arm A has NET ≡ 0 identically** (no z; coupled ≡
baseline) — computed, not assumed, as the pipeline's self-test.

Secondary diagnostics (reported, not bar-bearing): fiber-escape rate
per solution (fraction of stale dressings (s, z′) from which σ(s) is
unreachable — mines sitting directly on the solution); per-arm
measured definition sensitivity (mean #definitions affected per
x-flip) as the covariate Theorem B's fragmentation lesson predicts
both mechanisms scale with — arm D matches B's sensitivity by
construction (count, shape, layering), making the controls
load-bearing exactly where the lead placed them.

## 2. Instances and arms

- **Sibling anchor (primary):** PHP(4,4) + one definition layer.
  Arms: A (baseline), B (Cook-schema layer over the square grid,
  soundness-gated per the parked L1 gate: every solution's definition
  propagation machine-checked before geometry), C (BVA, degeneracy
  handling as registered), D (shape/count/layer-matched random,
  seeds 1–3, reported per-seed).
- **UNSAT anchor (descriptive ONLY — explicitly non-evidential):**
  PHP(4) + full cascade, attractor-level NET. The baseline there is a
  SINGLE attractor (the plateau discovery), so basin-mass deltas have
  almost no structure to redistribute: corridor/mine accounting
  against a one-basin baseline mostly measures fragmentation
  bookkeeping, which Theorem B already explained. This cell
  illustrates mechanisms (stale-repulsion exhibits); it bears no bar,
  and its numbers are not evidence for or against any arm — the
  sibling is the SOLE bar-bearing cell.
- Nothing sampled. No claims beyond the anchors (P1 frame: exact only).

## 3. Feasibility (measured into this registration, lead requirement)

The stale configurations ARE the z-coordinates; no extra factor:

| Object | States | Out-deg | Est. cost | Memory (Tarjan + masks) |
|---|---|---|---|---|
| PHP(4)+cascade (12x + 8z) | 2²⁰ ≈ 1.0 M | 12 | ~2.5·10⁸ clause-ops | ~25 MB |
| PHP(4,4)+layer1 (16x + 9z) | 2²⁵ ≈ 33.5 M | 16 | ~1.6·10¹⁰ clause-ops | ~550 MB |

Algorithm: iterative Tarjan with on-the-fly successor generation
(successors are deterministic flip+cascade; no edge storage), then
attractor-mask propagation in reverse condensation order (one 32-bit
mask per state; 24 solutions ≤ 32 bits). Both anchors fit a laptop.
**Gate:** a successor-function microbenchmark must confirm ≥ 10⁷
successor evaluations/sec in C before runs; if the estimate misses by
>10×, stop-and-report (scope rule) with reachability *sampling* as the
registered fallback — which then requires an L0-style validation pass
against the small anchor before any bar is evaluated. No unvalidated
estimator touches the primary claim.

## 4. Bars (pre-committed; exact computation ⇒ materiality, not noise)

- δ = 0.05 (five percentage points of state-space mass), pre-hoc.
- **Supported (H1-successor):** mean-NET(B) > 0, and
  mean-NET(B) − mean-NET(C) ≥ δ, and mean-NET(B) − mean-NET(D) ≥ δ
  (D: against the per-seed *maximum* — the strict comparator by
  design, not accident: it guards against declaring Cook special when
  the random-definition distribution has a tail that occasionally
  matches it; B must beat D's best draw, not its average).
- **The awkward branch, decided now (lead requirement):** if all
  definitional arms show both mechanisms with the same NET sign and
  separations below δ — magnitude-only differences — the verdict is
  **definition-generic, not Cook-specific: H1-successor NOT
  supported**, regardless of sign, and regardless of how suggestive
  the magnitudes look. Pre-committed against the exact post-hoc
  temptation magnitude gradients invite.
- **Mines-dominate branch:** mean-NET(B) < 0 with corridor_gain > 0 —
  "even proof-relevant coordinates lose more mass to their mines than
  their corridors recover" — informative failure, ledger-ready.
- **Kill:** NET(B) < 0 on the sibling anchor AND no arm separation
  ≥ δ ⇒ stream closes: coupled dynamics carry both mechanisms
  definition-generically; no geometric specialness of proof-relevant
  coordinates in assignment space; successor substrate is proof space
  (S5), per the frame.

## 5. Deliverables and checks

Every number lands in coupled-moves reproduce.py (arm-A NET ≡ 0
structural check, pinned NET values per arm, the soundness gate, the
microbenchmark gate). Disagreement check (lex-descent attractors)
reported alongside SCC attractors, never adjudicated. One run per
cell; deviations by written amendment before affected runs.
