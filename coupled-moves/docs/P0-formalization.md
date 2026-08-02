# P0 — coupled-move formalization (paper-only, pre-code)

Setting: base variables x, extension variables z with functional
definitions z ↔ f(x) as clauses (layered DAG, Cook-style; each
definition clause contains exactly one literal of the variable it
defines — its *owned* variable — plus input literals). V_orig counts
original clauses (x-only); D counts violated definition clauses;
V_full = V_orig + D.

## Theorem C (eager coupling collapses) — CONFIRMED

Move: flip x_i, recompute z = f(x) in full. From any state the first
move lands on the section {(x, f(x))}; on the section D = 0, so
V_full = V_orig(x), and moves project to 1-flips on x. The map
x ↦ (x, f(x)) is an isomorphism of landscapes (leaf-for-leaf,
merge-for-merge); off-section states are one-step transient. Eager
coupling does not open tunnels — it deletes the extension. ∎
*Variant 1 is the stream's null model, as suspected.*

## Theorem D (bundled altitude is baseline) — variant 3 inert

For functional definitions, unit propagation from any full x fixes
every z to f(x) layer by layer (checked for the 4-clause z↔a∨(b∧c)
encoding: every input case propagates the owned literal). Propagation
assigns only z; original clauses are x-only; hence the propagation-
closure altitude is Ṽ(x) = V_orig(x) + 0 identically. Variant 3 is
the baseline landscape with extra evaluation cost. ∎

## Variant 2 (lazy propagation) — the precise object

Canonical move relation (fixed here; the "walker moves in problem
space, definitions respond" picture):

- States: ALL full assignments (x, z), consistent or not.
- Initiating moves: flip one x-variable (z never initiates).
- Response: repair to fixpoint every definition clause that **became
  violated during this move**, by flipping its owned variable;
  repairs cascade DAG-forward and terminate (≤ |z| flips).
- **Staleness conservation:** clauses violated *before* the move are
  not repaired (they did not "become" violated). Staleness persists
  until an input flip touches it.

### Theorem E (three collapses inside variant 2)

(i) **From consistent states, lazy ≡ eager ≡ baseline.** If D = 0,
every input flip breaks exactly the clauses forcing the affected
definitions' new values; the cascade restores z = f(x). The reachable
component of the section is the section; Theorem C applies. ∎

(ii) **Under original-V altitude, variant 2 is baseline regardless of
staleness.** V_orig ignores z; initiating moves are x-flips; the
x-trajectory of any V_orig-descent equals the baseline trajectory
(Theorem A redux, dynamical form). ∎

(iii) **Irreversibility is real.** Example below: flip x_i and flip it
back need not return to the start (the return flip triggers a repair
the outbound flip did not). The system is genuinely directed. ∎

### The surviving object — and the surprise

What survives P0 is *narrower than the frame expected and sharper*:

> **S1's non-trivial object is variant 2 under FULL-V altitude on the
> inconsistent-inclusive state space** — reachable only from stale
> starts (random initial assignments are typically stale), never from
> the section.

Worked micro-example (F = (¬x1 ∨ ¬x2), one definition z ↔ x1∧x2,
clauses (z∨¬x1∨¬x2), (¬z∨x1), (¬z∨x2)):

- *Accidental repair (corridors open):* state x=(1,1), z=0 has
  V_full = 2 (one original + one definition violation). Flip x1:
  nothing becomes violated, but (z∨¬x1∨¬x2) becomes satisfied — the
  stale clause is cured by accident. V_full: 2 → 0 in one move — a
  descending route the baseline landscape does not have.
- *Stale repulsion (the surprise):* state x=(0,0), z=1 sits ON a base
  solution (V_orig = 0) yet has V_full = 2 from two stale definition
  clauses, and its neighbors have V_full = 1: **staleness pushes the
  walker off a true solution.** Persistent stale clauses act as
  altitude the baseline never sees, in both directions.
- *Irreversibility:* (1,1,z=0) → flip x1 → (0,1,z=0) → flip x1 back →
  cascade fires → (1,1,z=1) ≠ start.

Both mechanisms — corridor-opening accidental repairs AND
solution-repelling stale altitude — coexist in the surviving object.
P1's question is which dominates under Cook's definitions vs controls.

## Canonical basin definition for directed dynamics (fixed here)

The move digraph restricted to non-increasing V_full (plateau moves
included). **Attractor := terminal strongly connected component;
basin := reachability preimage.** This is a set-valued, tie-break-free
canonical object (the merge-tree lesson carried over: SCC condensation
requires no ordering choices). Disagreement check: deterministic
steepest-descent-with-lexicographic-tie-break attractors, reported
alongside, never adjudicated.

## P0 verdict

| Variant | Status |
|---|---|
| 1 eager | **Inert by Theorem C** — null model |
| 3 bundled altitude | **Inert by Theorem D** |
| 2 lazy, orig-V view | **Inert by Theorem E(ii)** |
| 2 lazy, consistent starts | **Collapses by Theorem E(i)** |
| **2 lazy, full-V, stale-inclusive** | **SURVIVES — provably distinct** (worked example: irreversibility, accidental repair, stale repulsion) |

The stream's kill criterion did not fire: one variant survives with
its canonical definitions fixed. P1 registration may proceed (after
approval, per cadence), scoped exactly to the surviving object at the
anchors (PHP(4)+cascade, PHP(4,4)+layer-1), arms A/B/C/D, with the
sharpened question: **under lazy-propagation dynamics from stale
starts, do Cook's definitions produce attractor/basin structure — in
particular reachability between solution regions — that the baseline
provably lacks, beyond what shape-matched random definitions
produce?** The stale-repulsion mechanism must be measured alongside
the corridor mechanism — the surviving object carries both signs, and
only the controls can say whether either is *Cook-specific*.
