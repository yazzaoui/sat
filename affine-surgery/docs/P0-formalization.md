# S4 P0 — formalization, walkability, and an operator-split correction

Paper + measurement, per frame. Kill criterion did NOT fire; one
frame-premise correction requires lead sign-off before P1 registration.

## Theorem G (move-basis duality — the representation trap dissolves for measurement)

For invertible M over GF(2)ⁿ, the transformed formula F∘M⁻¹ under
unit flips is landscape-isomorphic to the ORIGINAL V under move set
{s ↦ s ⊕ B_k}, B_k = columns of M⁻¹ (map φ(y)=M⁻¹y carries altitude
and adjacency). *Proof:* V′(y)=V(φ(y)); y⊕e_k ↦ φ(y)⊕M⁻¹e_k. ∎

Consequence: **scoring requires no formula transformation at all** —
V is computed once, only neighbor masks change (`exact --basis`,
flag-gated, stock-identical). The frame's representation toll applies
only to P2's CDCL path; the measurement path's toll is zero.

## Theorem H (flatness for structureless V — the control, sharpened)

If the distribution of V is invariant under affine re-coordinatization
(uniform random V is), every basin/merge statistic has basis-
independent expectation ((V, B-moves) ≅ (V∘M, unit moves), V∘M ~ V).
∎ Any expected score movement under basis selection certifies
non-generic algebraic structure. Random k-CNF is NOT affine-invariant,
so pure-CNF cells stay an empirical control — but the theorem states
exactly what a signal there would mean. (No cheap theorem found for
the CNF distribution itself; registered as an open note, per frame's
conditional.)

## The operator-split correction (frame premise, sharpened by measurement)

Anchor: XOR n=16, m=14, seed 1 (L0 cell: 68 basins pre-elimination,
1 post). Building M from the pivot rows and applying Theorem G:
**columns-of-M⁻¹ moves on V_orig give 26 basins, not 1** — and the
algebra is airtight (decomposition re-multiplies to M exactly).
Resolution: Gaussian elimination = **column operations (coordinate
change, a landscape bijection — the registered operator class) + row
operations (replacing the constraint set by XOR-combinations, which
changes V itself and is NOT a bijection of the landscape).** L0's
calibration validated the composite. The registered class is the
column half only.

The frame's premise is corrected, not broken: pure coordinate change
DOES merge substantially (below), but the full 68→1 collapse is out
of class, and **P1's "must rediscover Gaussian elimination" gate is
unreachable as stated** — it must be restated (lead decision) as:
selected compositions must reach the in-class anchor optimum
(empirically ≤ 12, see below), with the hidden-XOR blind-discovery
question unchanged.

## Anchor walkability (the kill-criterion measurement)

- **Canonical Gauss-order composition (15 ops): NON-monotone** —
  68 → 104 (spike!) → … → 43 → 26. Greedy selection would refuse the
  first op; the known-good ordering passes through worse territory.
- **Greedy over all 240 elementary ops per step: monotone** —
  68 → 40 → 24 → 16 → 12, stuck at 12 with no improving op (4 steps).
  Greedy beats the canonical endpoint (12 < 26) and never spikes.

**Verdict: the score landscape is greedily walkable on the anchor;
the kill criterion does not fire.** Caveats registered for P1: greedy
sticks at a local optimum of unknown distance from the in-class true
optimum; greedy cost is O(n²) score evaluations per step (anchor:
240 exact evaluations/step at ms each; sampled scoring at larger n
is P1's costed subject).

## Tolls (measured)

- Measurement path: zero (Theorem G).
- Parity-literal width along the canonical anchor path: max 3 —
  CNF re-encoding at these depths is trivial (chain encoding, ≤ 2 aux
  vars/literal). Width growth with depth d on larger instances is a
  P1-registered cap, not discovered mid-run.
- Data: [P0-anchor-curve.json](P0-anchor-curve.json),
  [P0-greedy-walk.json](P0-greedy-walk.json).

## P0 verdict

| Item | Outcome |
|---|---|
| Representation trap | Dissolved for measurement (Thm G); P2-only toll |
| Anchor walkability | Walkable (greedy monotone 68→12); canonical order non-monotone — ordering artifact |
| In-class reachable target | ~12 on anchor, NOT 1 — operator split (column vs row ops); frame premise corrected |
| Null direction | Thm H sharpens the control; no CNF theorem, empirical control stands |
| Kill criterion | Does not fire |

P1 registration awaits lead approval AND the restated rediscovery
gate per the operator-split correction.
