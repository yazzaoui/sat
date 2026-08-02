# The extension-inertness theorems — L-series closure by proof

Status: checked and approved by lead review. These two theorems ended
the L-series: H1's last testable form (sibling solution-cluster
connectivity) is unsatisfiable by any definitional-extension arm, so
the arms were never run. The kill cost one formalization attempt —
no soundness gate, no registered bars, no experiments.

Setting: assignment landscapes V over full assignments, 1-flip
adjacency, canonical merge-tree structure (L0 registration §1). An
extension arm adds variables z with functional definitions z ↔ f(x)
as clauses (Cook-style; any functional definitional extension
qualifies).

## Theorem A (original-V view: extensions are inert)

If V counts only original clauses, then V′(x, z) = V(x) and the
extended landscape is the product of the baseline with a free
hypercube on z. Every sub-level set factors as L_c × {0,1}^|z|;
z-flips never change V′, x-connectivity within sub-level sets is
unchanged, so the merge tree is identical to the baseline's
(leaf-for-leaf and merge-level-for-merge-level; component sizes
multiply by 2^|z|).

*Proof.* Immediate from V′(x,z) = V(x): a coordinate that altitude
ignores is padding. ∎

Consequence: the "definition-violating states cost nothing, so
corridors open" picture cannot occur in this view — motion in z is
free and goes nowhere.

## Theorem B (definition-V view: level-0 isolation is preserved; ridges only stay or rise)

Let V″ = (#violated original clauses) + (#violated definition
clauses). Then V″ = 0 iff x satisfies the original formula and
z = f(x); the V″=0 set bijects to the base solution set. If the base
solution set has minimum Hamming distance ≥ 2, the V″=0 states are
pairwise non-adjacent, so every solution-pair merge level is ≥ 1.
In particular, when the baseline solution-pair ridge is uniformly 1
(PHP(n,n): permutation matrices, pairwise distance ≥ 4), no extension
arm can connect any solution pair below the baseline ridge.

*Proof.* A 1-flip between two V″=0 states changes either one z
coordinate (impossible: z is determined by x) or one x coordinate
(impossible: distinct solutions differ in ≥ 2 bits). ∎

*Ridge-rise mechanism (sensitivity).* A V″≤1 path must keep
z = f(x) exactly while x crosses V=1 states; but z updates are
separate flips, so wherever some definition is sensitive to a crossed
bit, the walker occupies a state with V=1 and ≥1 violated definition:
V″ ≥ 2. Ridges rise exactly where definitions are sensitive to the
crossing coordinates. Measured instance: PHP(4)+Cook cascade goes
from 1 basin (baseline) to 115 basins with barriers up to 4 — Cook's
running-tally definitions are maximally sensitive, so the observed
fragmentation is overdetermined by this mechanism.

*Corollary (why clause 4 mattered).* In any fragmentation-direction
comparison, low-sensitivity random definitions (arm D) beat Cook's
(arm B) — a meaningless victory that the no-retrofitted-bars clause
existed to refuse.

## The operator split (correcting the founding conflation)

Spec §1.2 presented Gaussian elimination and the extension rule as one
operator family. They are not (lead review, owning the error):

- **Bijective re-coordinatization** (affine GF(2) maps): rewires
  adjacency on the same space. This is what merged the XOR landscape
  to a single basin — the L0 calibration validated exactly and only
  this operator.
- **Extension** (definitional, dimension-adding): keeps old adjacency.
  By Theorems A and B it is inert in one canonical view and
  isolation-preserving-or-fragmenting in the other.

The landscape-surgery power demonstrated by the instruments belongs
exclusively to the bijective operator.

## Calibration of novelty (stated honestly)

To a proof-complexity theorist, "extension variables don't directly
help local search" is folklore-adjacent, not shocking. What is new
here is the precise form: inertness in the original-V view, level-0
isolation plus the quantified sensitivity/ridge-rise mechanism in the
definition-V view, under 1-flip adjacency, with the fragmentation
mechanism verified against a measured instance (1 → 115). A crisp
formalization of something half-believed.

## Where ER's power must live (the positive content)

Both proofs lean entirely on one assumption: **z moves separately
from x.** If the walker may flip x and propagate z in the same move,
Theorem B's ridge argument collapses — z tracks f(x) for free and
definitions never pay altitude. "Flip and propagate" is not exotic:
it is what CDCL and propagation-based local search do natively.

The theorems therefore locate ER's power: **not in the terrain, but
in the move structure.** Extension variables are inert as geography
and active only through a walker that propagates. This closes the
loop the program opened: a local minimum is a property of landscape
*plus* neighborhood — and definitions change nothing unless they
change the neighborhood, via coupled moves. The assignment-landscape
program measured the terrain; the terrain was never the object. The
object is the pair.

## Successor programs (named, not started)

1. **Bijective/affine surgery selection.** Validated instruments, open
   door — with its toll stated at the gate: general bijections are
   all-powerful and unfindable (sorting states by V smooths any
   landscape; computing that ordering is the original problem);
   affine-over-GF(2) is findable and provably narrow. The
   conservation law is visible before the program starts.
2. **The coupled-move substrate.** Landscape + propagation as the
   joint object — where these theorems point, and where the
   instrumentation questions are entirely unsolved.

Both are new programs requiring their own specs, not amendments to
this one.
