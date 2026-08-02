# S5 P1 registration — theory-lattice deformation, gated by distinguishability

Committed before code. Two-stage by lead direction: the
distinguishability pre-check is the OPENING GATE; numeric bars are set
by a bars-amendment committed after the gate and before the main
runs, on a quantity the gate certifies. A bar on a non-separating
observable is the L1-floor failure mode in proof-space clothing; the
gate exists to make that impossible.

## 1. Canonical move (lead-required, fixed here)

**The move is atomic definition addition/removal on the theory
lattice.** Points: theories T = F ∪ D where D ⊆ the candidate
definition set (each definition = one extension variable WITH its
defining clauses, moved as a unit — clause-level edits would create
non-functional intermediate theories, an encoding artifact). The
observable at each point is the depth-wavefront landscape of T
(candidate quantities below). The tunnel question becomes: **how does
the landscape deform along paths from F to F ∪ D_Cook — monotonically
(each definition helps; walkable) or cliff-like (invisible until
complete; the S4 one-op-horizon genre)?**

Why this canon and not clause-graph locality: the lattice is finite
and exactly enumerable at the anchor (2^8 theories for the PHP(4)
cascade); its atomic unit is unique; and it is literally the
program's question (definition selection as geometry-guided walking).
Clause-graph locality (geodesic overlap between adjacent theories) is
the reported-never-adjudicated check.

## 2. The distinguishability pre-check gate (lead-required, runs before any bar exists)

Candidate primary quantities, each with the direction theory demands:

| Quantity | Theory-demanded direction under D_Cook |
|---|---|
| Q1: depth(⊥) | ≤ baseline (monotone by axiom-addition; lead's concern: may barely move — PHP resolution depth is only polynomial) |
| Q2: geodesic-DAG size (#clauses participating in some minimal-depth derivation of ⊥) | **< baseline** (ER compression is a SIZE phenomenon; its shadow here is front volume, not path length) |
| Q3: wavefront volumes (antichain sizes per depth level, restricted to the geodesic DAG) | thinner fronts under D_Cook |

**Gate rule (registered decision procedure, no post-hoc choice):**
compute Q1–Q3 for T₀ = F and T_full = F ∪ D_Cook at anchor PHP(4)
(full cascade, 8 definitions). A quantity PASSES if it separates with
the predicted sign by ≥ 20% (materiality, pre-hoc). If none passes at
PHP(4), escalate ONCE to PHP(5) (one layer, 12 definitions) — the
escalation is registered here, not shopped later. If none passes at
either anchor, **P1 closes at the gate**: "no registered observable
separates ER from resolution at exactly enumerable scales" — itself a
verdict, reported with both anchors' numbers.

The primary quantity = the passing Q with the largest separation;
others become reported checks. Space parameters: subsumption-quotient
throughout; width bound w = minimal w with depth(⊥) finite for BOTH
theories at the anchor (measured in the gate; the bound is part of
the space definition at ER cells by necessity — 3^20 is not
enumerable unbounded).

## 3. Main measurement (after the bars-amendment)

- **Full lattice at PHP(4):** all 2^8 theories, primary quantity per
  point — the complete deformation landscape (does the score descend
  monotonically toward D_Cook along the lattice?).
- **Controls (S1 genre):** shape-matched random definition sets
  (same count, shape, layering, variable pool; seeds 1–3): their
  lattice corners and paths, same quantities. Cook must beat the
  best random corner by a margin set in the bars-amendment.
- **Walk form (screen-vs-dynamics two-stage, mandatory):**
  screen = per-definition marginal effect on the primary quantity
  (correlation with membership in D_Cook); dynamics = greedy
  definition-addition guided by the primary score, from F, must
  actually reach a theory matching D_Cook's separation (bars-amendment
  sets the fraction) vs random-order path controls. Association
  without navigation gets no fourth chance to hide.
- **PHP(5) path-sampled** (lattice too large): Cook-order path +
  random-order paths only; descriptive unless the bars-amendment
  says otherwise.

## 4. Costs and scope

C port of the depth DP approved for the PHP(4)+Cook cell class ONLY
(20 vars, width-bounded), per lead accounting; Python elsewhere.
Python is tried first even there; the port happens only on measured
need (scope rule). One run per cell; per-cell provenance; every
headline in reproduce.py; ledger entry 10 owed at stream closure
regardless of branch.
