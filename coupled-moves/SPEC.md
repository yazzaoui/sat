# Stream S1 — Coupled-Move Landscapes: Registration Frame

(Lead-issued frame, recorded verbatim at kickoff.)

## Question

Theorems A/B killed H1 by showing extension variables are
landscape-inert under 1-flip adjacency: z-moves are either free padding
(original-V) or ridge-raising (definition-V). The escape identified at
closure: a walker that flips x and **propagates** definition
consequences in the same move changes the neighborhood structure, which
is where ER's power must enter if it has any geometric form. S1 asks:
**does the landscape under propagation-coupled dynamics show structure
that 1-flip geometry provably cannot?**

## Phase P0 — Formalize before building (mandatory, paper-only, time-boxed)

The lead's closure remark ("Theorem B dies the moment moves propagate")
is **suspect and must be checked first**, because the most natural
coupled move is trivially inert:

**Theorem C candidate (the isomorphism trap):** If the move is "flip
x_i, then eagerly recompute z = f(x) in full," the walk lives on the
section {(x, f(x))}, where all definition clauses are satisfied and
V = V_orig(x). The coupled landscape is then **isomorphic to the
baseline** — leaf-for-leaf, merge-for-merge. Eager full propagation
doesn't open tunnels; it collapses the extension entirely. Prove or
refute this before any code. If it holds (expected), S1's subject is
*not* eager coupling — it is the non-trivial variants below, and the
registration must say which.

Candidate move structures to formalize, with the triviality question
settled by proof for each:

1. **Eager functional propagation** — suspected isomorphic (Theorem C).
   If proven, becomes the stream's null model.
2. **Lazy unit propagation** — flip x_i; propagate only definition
   clauses that become unit; z may go stale. States now include
   inconsistent (x, z); dynamics are **path-dependent**. This is a
   directed transition system, not an undirected graph — the genuinely
   new object. Formalize: state space, move relation, altitude
   (original-V vs full-V both retained as views), and what "basin"
   means for directed dynamics (attractors / SCC condensation /
   quasi-potential — pick one canonical definition, per the merge-tree
   lesson).
3. **Propagation-bundled altitude** — moves are 1-flip on x only, but
   altitude is V after propagation closure. Undirected, cheap; settle
   by proof whether it differs from V_orig at all.

**P0 deliverable:** a short document proving, for each variant, either
(i) isomorphic/inert → discarded with the proof, or (ii) provably
distinct from baseline geometry → eligible for probing, with its
canonical basin definition fixed. **P0 kill criterion:** if all
formalizable variants collapse to baseline by proof, S1 closes by
theorem — ledger sentence: *ER's power is invisible to
assignment-space geometry even under coupled dynamics; the remaining
substrate is proof space (S5).*

## Phase P1 — Probes for the surviving variant(s)

Only registered after P0 output exists. Expected shape if variant 2
survives: exact analysis at anchor sizes only (PHP(4)+cascade both
views; PHP(4,4) siblings); attractors under the canonical directed
definition; arms A/B/C/D. The H1-successor question, sharpened: do
Cook's definitions, under lazy-propagation dynamics, connect regions
(or solutions, on siblings) that are provably separated under 1-flip?
No sampled claims in P1.

## Inherited discipline

Registration before code at each phase; bars and kill criteria before
runs; one canonical definition per measured quantity; C/D controls
mandatory; every claim in reproduce.py; scope rule applies to the
directed-graph tooling. **Time-box:** P0 = 1 week of effort; whole
stream to verdict or suspension within the box. **Ledger:** LEDGER.md
at repo root, backfilled at kickoff; S1 adds its sentence at closure
regardless of branch.

## Honest stakes

Most likely: variants 1 and 3 proven inert, variant 2 survives, P1
finds modest or null structure — closing the physical story of
extension variables completely, proof-space substrate (S5) recorded as
successor. Least likely, most valuable: stale-z corridors genuinely
connect solution clusters on the siblings — the first geometric
signature of ER's power ever measured. Both branches end in a ledger
sentence. The stream cannot fail to produce one; it can only fail to
be run honestly.
