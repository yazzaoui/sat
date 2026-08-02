# S5 P0 — formalize, theorem-check, choose

Paper-first with measured feasibility, per frame. The no-ending fence
did NOT fire: one candidate survives with a unique canonical
definition. Selection below; P1 registration awaits approval.

## Candidate 1 — clause-database states: DISQUALIFIED (degeneracy + measured explosion)

Definition fixed for the record: states = subsumption-reduced
antichains of derived clauses ⊇ F; moves = add one resolvent
(deletion EXCLUDED by argument: it makes the space non-monotone and
cyclic, and any deletion policy is an arbitrary encoding choice — the
frame's materiality trap in miniature).

**Theorem I (altitude degeneracy).** Under the natural altitude
(#derived clauses), every move ascends by exactly 1: the landscape has
no descent anywhere, no basins, no merge structure. The only intrinsic
geometric quantity is reachability distance — which IS proof length,
definitionally. The space re-states proof complexity; it does not
geometrize it. ∎

**Measured explosion** (BFS under the canonical quotient, PHP(3) —
the smallest instance that exists): states by depth = 1, 12, 102, 682
(×8 per level). Refutations live at depth ≥ the proof length; the
region enumeration P1 needs is infeasible at even the trivial anchor.
Fails the "exactly enumerable at some anchor" criterion by
measurement.

## Candidate 2 — proof-DAG rewrite space: DISQUALIFIED (completeness unproven)

The frame's own criterion: the registered rewrite move set must be
proven to connect refutation space, or the space is disqualified. No
standard local-rewrite set with proven connectivity over resolution
refutation DAGs exists in the literature we hold, and proving one is
an open research problem outside a two-week paper-first box (attempted
sketch for tree-resolution rotations does not extend to DAG sharing).
Additionally, refutation-space enumeration is infeasible a fortiori:
complete refutations are deep points of candidate 1's space, whose
prefix counts already explode (above). Disqualified without a
feasibility run — by the registered criterion, honestly, not by
convenience.

## Candidate 3 — SELECTED: the derivability-wavefront space

**States:** the clause universe over the instance's variables
(optionally width-restricted to ≤ w), quotiented by subsumption.
**Canonical altitude (fixed here, the merge-tree discipline):**
minimal resolution DEPTH of derivation from the axioms —
subsumption-aware, computed exactly by fixpoint DP; unique by
minimality, no tie-breaking anywhere. Alternatives (derivation size,
width-at-derivation) are reported-never-adjudicated checks; size is
explicitly NOT canonical because DAG-size minimality is not a clean
fixpoint (tree/dag ambiguity — an encoding choice, fenced out).
**Geometry:** depth level sets (wavefronts), the backward geodesic DAG
of ⊥, and the width frontier (minimal w making depth(⊥) finite).
**ER embedding:** extension-definition clauses enter as depth-0 axioms
over the enlarged universe; Cook vs shape-matched-random definitions
give the S1-genre control for free.

Non-degeneracy: the space carries structure beyond the single number
depth(⊥) — wavefront populations, geodesic membership, and the
width/depth tradeoff are instance-revealing (measured below).
ER/resolution distinguishable in principle: the known separation is a
statement about exactly this space's distances. Landmarks:
Ben-Sasson–Wigderson width bounds live natively here — the only
candidate with literature to calibrate against, and the pre-registered
tie-break, though no tie arose: candidate 3 is the sole qualifier.

**Measured feasibility (Python, unoptimized):**

| Cell | depth(⊥) | rounds | derived antichain | time |
|---|---|---|---|---|
| PHP(3), w=2 | 4 | 4 | 61 | ms |
| PHP(3), full width | 4 | 4 | 61 | ms |
| PHP(3)+Cook layer (8 vars) | 4 | 4 | 104 | 0.01 s |
| PHP(4), w=3 | 8 | 8 | 801 | 1.8 s |
| PHP(4), w=4 | **7** | 7 | 1431 | 11.7 s |

The width/depth tradeoff is already visible at PHP(4) (wider ⇒
shallower: 8 → 7) — the space showing a real geometric landmark at the
anchor, exactly the calibration behavior the frame wanted from this
candidate. PHP(4)+Cook (20 vars) at bounded width is the expected P1
anchor ceiling; Python costs say a C port of the DP is warranted
there and nowhere else (scope-ruled).

## P0 verdict

| Criterion | C1 | C2 | C3 |
|---|---|---|---|
| Non-degenerate by theorem | ✗ (Thm I) | — | ✓ |
| ER/res distinguishable in principle | ✓ | ✓ | ✓ |
| Exactly enumerable at an anchor | ✗ (measured) | ✗ (a fortiori) | ✓ (measured) |
| Canonical definition unique | ✓ | ✗ (move set unproven) | ✓ |
| Existing landmarks | ✗ | ✗ | ✓ (BW width) |

**Candidate 3 proceeds.** The no-ending fence stands down; P1's
registration (anchor cells, tunnel-form question over the geodesic
DAG, Cook-vs-random control, screen-vs-dynamics two-stage) follows on
approval.
