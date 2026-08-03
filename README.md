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

## Workstream 2: landscape-surgery — **complete, closed by proof**

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

How it ended (details: [RESULTS.md](landscape-surgery/RESULTS.md)):
the probes passed their calibration gate at full strength (100/100
cells see the XOR smoothing), and then the program completed one level
deeper than its experiments — **by theorem**. Two short proofs
([the theorems](landscape-surgery/docs/extension-inertness-theorems.md))
show that functional extension variables cannot merge solution
clusters on assignment landscapes under bit-flip adjacency: they are
*inert* when altitude ignores them (product theorem) and
*isolation-preserving-or-fragmenting* when it counts them (verified
against a measured 1 → 115 fragmentation). The founding analogy had
conflated two operators: Gaussian elimination *rewires* adjacency
(bijective — and genuinely merges, as calibration showed), while
extension *adds dimensions* keeping old adjacency. ER's power must
therefore enter through **move structure** — walkers that flip and
propagate in one step — not through terrain. Along the way, a
standalone descriptive discovery: the UNSAT pigeonhole refutation
landscape is one undifferentiated plateau system; its apparent
"ruggedness" at measured sizes is an artifact of tie-breaking in
descent-partition definitions, which much fitness-landscape literature
builds on. Two successor programs are named (bijective-surgery
selection; the coupled-move substrate) but deliberately not started.

## The stream program (successors, all run to closed verdicts)

After the two founding workstreams closed, the program continued as
short registered streams, each ending in a one-sentence ledger entry
([LEDGER.md](LEDGER.md) — the whole program in ten sentences):

| Stream | Question | Verdict (short form) |
|---|---|---|
| [S1 coupled-moves/](coupled-moves/) | Does propagation-coupled dynamics show structure 1-flip geometry cannot? | Closed by Theorem F: net conductance is a counting identity, blind to definition content |
| [S2 plateau-structure/](plateau-structure/) | Do folklore secondary signals structure the plateau? | No — and walking them is at best sub-1.5×, at worst a trap; the flat is flat all the way down |
| [S3 clustering-transition/](clustering-transition/) | Does the statistical-physics clustering picture hold at enumerable sizes? | Signatures inverted or absent at n ≤ 24; the narrative's geometry has a measurable onset (~n=26) |
| [S4 affine-surgery/](affine-surgery/) | Can basin-merging scores discover basis changes blind? | Rediscovers in-class optima on pure XOR; dies at its decision cell — the one-op horizon |
| [S5 proof-space/](proof-space/) | Is ER's power visible as geometry in *proof* space? | Closed at its distinguishability gate: no registered observable separates ER from resolution at exactly measurable scales — the sixth finite-size inversion; the arc is complete |

Each stream folder carries its lead-issued frame (SPEC.md),
registrations committed before runs, results with raw data, and its
own `scripts/reproduce.py`.

## Repository layout

| Where | What |
|---|---|
| [LEDGER.md](LEDGER.md) | One sentence per closed question — ten entries, the program's abstract |
| [witness-search/](witness-search/) | Complete workstream: [SPEC](witness-search/SPEC.md) · [RESULTS](witness-search/RESULTS.md) · [REPRODUCING](witness-search/REPRODUCING.md) · docs (pre-registrations + results) · scripts · benchmarks |
| [landscape-surgery/](landscape-surgery/) | Complete workstream (closed by proof): [SPEC](landscape-surgery/SPEC.md) · [RESULTS](landscape-surgery/RESULTS.md) · [theorems](landscape-surgery/docs/extension-inertness-theorems.md) · probes/ (exact merge-tree core + flag-gated `--pairs`/`--basis` modes) · extvars/ |
| [coupled-moves/](coupled-moves/) · [plateau-structure/](plateau-structure/) · [clustering-transition/](clustering-transition/) · [affine-surgery/](affine-surgery/) · [proof-space/](proof-space/) | The five closed streams (table above) |
| [common/](common/) | Shared: seeded instance generators; solvers & proof checker (patched SaDiCaL tracked in-repo; CaDiCaL + dpr-trim pinned externals); [DISCIPLINE.md](common/DISCIPLINE.md) — the protocol everything runs under |

## The discipline (why you can trust the claims)

Every experiment is pre-registered (hypothesis, arms, pass/fail bars,
kill criteria) in a commit that *precedes* its results. Solvers are
deterministic and every experiment runs behind a gate that must
reproduce frozen baseline conflict counts exactly. Every UNSAT claim
ships a proof verified by an independent checker (dpr-trim). Negative
results are published with the same care as wins — most of the value
here *is* the carefully-measured negatives. See
[common/DISCIPLINE.md](common/DISCIPLINE.md).

## Reproduction

Witness-search: [REPRODUCING.md](witness-search/REPRODUCING.md)
(clean-clone, 12 checks). Every other workstream/stream:
`python3 <dir>/scripts/reproduce.py` after building the probes
(`make -C landscape-surgery/probes`,
`cc -O3 -o proof-space/probes/depthdp proof-space/probes/depthdp.c`,
and the toolchain per
[common/README.md](common/README.md)). All suites are deterministic;
pinned values are the papers' headline numbers.

## Tags

- `m1-baseline` — frozen witness-search measurement dataset.
- `boundary-map-v1` — witness-search complete (pre-reorganization
  layout; the reproduction suite has been re-verified on the current
  layout since).
- `landscape-surgery-v1` — second workstream complete, closed by
  proof.
