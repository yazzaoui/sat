# Finding Short Proofs: Experiments at the Edge of SAT Solving

## The problem, from the top

Modern SAT solvers (the CDCL family — CaDiCaL, Kissat, …) are the
workhorses of hardware verification, planning, and combinatorics. But
they have a mathematical ceiling: CDCL search is equivalent in power to
the **resolution** proof system, and resolution provably requires
exponential-size proofs for natural problem families — the pigeonhole
principle, mutilated-chessboard tilings, parity (Tseitin) formulas.
On these, every CDCL solver takes exponential time *no matter how well
engineered*.

Stronger proof systems exist. **PR (propagation redundancy)** admits
polynomial-size proofs of those same families, and each proof step is
machine-checkable in polynomial time. **Extended Resolution (ER)** is
stronger still — no exponential lower bound is known for it at all.
The catch, and the subject of this whole repository:

> Short proofs *exist* in these systems, but nobody knows how to
> **search** for them. The bottleneck moved from proof *size* to proof
> *discovery*.

This program attacks that bottleneck experimentally: instrument the
solvers that hunt for strong-proof steps, measure what the hunt
actually computes, map what can and cannot make it cheaper, and test
selection principles for the ingredients (witnesses, extension
variables) that make strong proofs work. Every claim is either backed
by a machine-verified proof or by a pre-registered experiment whose
pass/fail bars were committed to git *before* the experiment ran.

## Workstream 1: witness-search — **complete**

SDCL (satisfaction-driven clause learning) is the solver paradigm that
learns PR clauses during search. Each PR step needs a **witness** — a
small assignment transformation that certifies "this region of the
search space can be skipped without loss of generality." SDCL finds
witnesses by calling a sub-solver at stuck points, which is expensive,
and on most real instances the overhead isn't repaid.

What this workstream established (details: [RESULTS.md](witness-search/RESULTS.md)):

- **Measurement (witness atlas):** across three problem families,
  successful witnesses are extremely *local* — they rearrange a handful
  of variables right next to the conflict (validated against a random
  null model) — and their shape is family-specific and size-invariant
  (e.g. pigeonhole witnesses are always a 4-literal swap).
- **A deployable:** an online gate that measures, during solving,
  whether the witness hunt is paying for itself, and switches the
  solver between full SDCL, plain CDCL, and a lossless fast path
  accordingly. This makes SDCL portfolio-safe for the first time:
  it recovers 100×-to-∞ losses on instance classes where the hunt is
  pure overhead, at a measured cost of ~0.1–1 s.
- **A boundary map (five pre-registered negative results):** every
  attempt to make the witness hunt cheaper by moving information across
  the sub-solver boundary — proposing witnesses from templates, seeding
  the sub-solver with the main solver's conflict analysis, exporting
  the sub-solver's variable activities, caching the sub-problems across
  calls, incrementalizing the dominant filtering step — fails, harms,
  or dies to a measurement, each in a characteristic way. Composite
  finding: *the stuck-point computation is irreducibly local — its
  inputs, cost, and products are all specific to the moment it runs.
  The sub-solver call is the unit of the method, not an inefficiency.*

Everything re-earns itself from a clean clone in ~3 minutes:
[REPRODUCING.md](witness-search/REPRODUCING.md) (12 deterministic
checks — conflict counts, gate verdicts, proof verifications).

## Workstream 2: landscape-surgery — **active**

The successor question, one level up the proof-system hierarchy.
A local search or CDCL run lives on a landscape: assignments are
points, flipping a bit is a move, unsatisfied clauses are altitude.
Fifty years of escape techniques modified the *heights* while keeping
the *geometry* — which points count as neighbors — fixed. But basins
and traps are properties of the geometry, and coordinate changes
provably dissolve them in special cases (XOR formulas are maximally
rugged in bit-flip coordinates and trivially smooth after Gaussian
elimination).

ER's "extension variables" (new variables defined over old ones) are
exactly a coordinate-change mechanism, and they're what makes ER
strong — yet there is no theory of *which* variables to introduce.
The hypothesis under test:

> **Good extension variables — the ones appearing in known short ER
> proofs — measurably merge basins of the search landscape, and
> basin-merging is usable as a selection score.**

Phases (each with pre-registered kill criteria,
[SPEC.md](landscape-surgery/SPEC.md)): build and calibrate landscape
probes on the XOR case where the answer is known (L0); measure whether
Cook's classic pigeonhole extension variables merge basins where
compression-selected and random variables don't (L1); generalize (L2);
then, only if the criterion survives, use it to select variables and
race it against the syntactic state of the art (L3). Either direction
of outcome is a first-time measurement of *why* the strongest proof
system resists automation — or a selection principle for it.

## Repository layout

| Where | What |
|---|---|
| [witness-search/](witness-search/) | Complete workstream: [SPEC](witness-search/SPEC.md) · [RESULTS](witness-search/RESULTS.md) · [REPRODUCING](witness-search/REPRODUCING.md) · docs (pre-registrations + results) · scripts · benchmarks |
| [landscape-surgery/](landscape-surgery/) | Active workstream: [SPEC](landscape-surgery/SPEC.md) · [RESULTS](landscape-surgery/RESULTS.md) (scaffold) · probes/ · extvars/ |
| [common/](common/) | Shared: seeded instance generators; solvers & proof checker (patched SaDiCaL tracked in-repo; CaDiCaL + dpr-trim pinned externals); [DISCIPLINE.md](common/DISCIPLINE.md) — the protocol both workstreams run under |

## The discipline (why you can trust the claims)

Every experiment is pre-registered (hypothesis, arms, pass/fail bars,
kill criteria) in a commit that *precedes* its results. Solvers are
deterministic and every experiment runs behind a gate that must
reproduce frozen baseline conflict counts exactly. Every UNSAT claim
ships a proof verified by an independent checker (dpr-trim). Negative
results are published with the same care as wins — most of the value
here *is* the carefully-measured negatives. See
[common/DISCIPLINE.md](common/DISCIPLINE.md).

## Tags

- `m1-baseline` — frozen witness-search measurement dataset.
- `boundary-map-v1` — witness-search complete (pre-reorganization
  layout; the reproduction suite has been re-verified on the current
  layout since).
