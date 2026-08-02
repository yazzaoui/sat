# Project: Landscape Surgery — Extension Variables as Basin-Merging Coordinates

## One-line summary

Test whether **good extension variables** — the new-definition coordinates that make Extended Resolution (ER) exponentially stronger than resolution — can be **selected by a geometric criterion**: they are the coordinates that merge basins of the SAT landscape. If the criterion holds, use it to guide automated extension-variable introduction, attacking the strongest proof system known via a measurable physical principle.

This is a successor project to the SDCL/witness-search program. It inherits that project's infrastructure, discipline (pre-registration, verified proofs, kill criteria), and boundary map — and attacks a door with **no known lower-bound theorem in front of it**.

---

## 1. First-principles motivation

### 1.1 The invariant behind fifty years of failures

Every failed approach to escaping local structure in SAT search modified the landscape while keeping the space fixed:

| Approach | What it changed | What stayed fixed |
|---|---|---|
| Clause weighting / DLM / metadynamics | height function V | hypercube + bit-flip adjacency |
| CDCL clause learning | removes regions | hypercube + bit-flip adjacency |
| Analog dynamics (CTDS) | equations of motion | hypercube (continuous relaxation of same geometry) |
| SDCL templates / witness guidance | who proposes moves | hypercube + bit-flip adjacency |

A local minimum is a property of **landscape + neighborhood structure**, not landscape alone. Basins are traps only because of which points count as adjacent. The adjacency has never been the experimental variable. This project makes it the experimental variable.

### 1.2 Proof that coordinate change is real power, not fantasy

XOR-SAT under bit-flip adjacency is a maximally rugged landscape for local search (parity constraints). Under the right affine basis (Gaussian elimination over GF(2)) the solution set is a single connected affine subspace — trivially smooth. Gaussian elimination *is* landscape surgery. XOR-SAT's local-search hardness is entirely an artifact of coordinates.

### 1.3 The connection to the top of the proof-complexity tech tree

Introducing a new variable z with defining clauses z ↔ (a ∧ b) embeds the landscape in a higher-dimensional space where the geometry differs. This is exactly the **extension rule**. Extended Resolution / Extended Frege:

- Polynomial-size proofs of pigeonhole (Cook 1976) and essentially every known "hard for resolution" family.
- **No exponential lower bounds known.** The strongest studied systems with that property.
- Practically unusable because there is **no theory of which extension variables to introduce.** The only practical tool (Bounded Variable Addition, BVA) selects variables to compress the formula — a syntactic criterion, blind to search dynamics. (Recent work: Structured/SBVA won awards using BVA-style preprocessing — evidence the direction has practical teeth even under crude criteria.)

### 1.4 The hypothesis

> **H1 (basin-merging criterion):** Extension variables that appear in short ER proofs of hard families (e.g. Cook's PHP construction) measurably merge basins of the search landscape — reduce basin count / barrier heights between solution-relevant attractors — while random or compression-selected extension variables do not, or do so far less.

> **H2 (selection principle):** If H1 holds, basin-merging is usable as an *online selection score* for automated extension-variable introduction, yielding measurable search improvement (CDCL and/or local search) on families where resolution is exponentially weak.

H1 is a measurement. H2 is an intervention. H1 must be settled before H2 is attempted.

---

## 2. What is genuinely novel here (and prior-art boundaries)

Prior art to study and cite, none of which tests H1:

- **Cook 1976**: hand-crafted ER proof of PHP — the source of known-good extension variables. The ground truth for H1.
- **BVA (Manthey–Heule–Biere) and SBVA**: automated extension variables by formula-size compression. The syntactic baseline for comparison.
- **Extended learning attempts** (e.g. Audemard et al.–lineage extended-clause-learning experiments, Huang/Soos-style solver experiments with ER learning): sporadic, heuristic, mostly negative or neutral results, no geometric criterion. Confirms the gap: nobody knows *which* variables help.
- **Fitness-landscape analysis of SAT** (local-optima networks, autocorrelation studies): measures landscapes but never as a function of coordinate change.
- **Symmetry breaking / structure detection**: from the predecessor project; reusable machinery.

The untested object is the **bridge**: landscape geometry as a *selection function* for extension variables.

---

## 3. Core measurement machinery (Phase L1)

### 3.1 Landscape probes (build these first — everything depends on them)

The full basin structure of a 2^n space is not enumerable beyond ~n=30. The program needs estimators that scale and are validated small-vs-large:

1. **Exact small-n ground truth (n ≤ 26–30):** enumerate assignments; define the landscape as V(x) = #unsatisfied clauses under the *current* clause set (original + definition clauses of any added extension variables); basins by steepest-descent partition under 1-flip adjacency; record basin count, sizes, barrier matrix between basin minima (min–max path height, computable exactly at small n via Dijkstra-on-levels or union-find over level sets — the union-find/persistence approach is the scalable one: sort states by V, sweep upward, merge components; barrier(b1,b2) = level at which they merge).
2. **Sampled estimators (all n):**
   - Basin sampling: many random starts → steepest descent → cluster endpoints; estimate basin count/coverage.
   - Barrier sampling between attractor pairs: constrained random walks / nudged paths; report estimated merge levels.
   - Autocorrelation length of V along random walks (standard ruggedness proxy).
   - Solution-cluster connectivity where solutions are known (for SAT instances).
3. **Validation gate:** on every instance where exact and sampled probes are both computable, sampled estimates must rank-correlate with exact (pre-register the correlation bar, e.g. Spearman ≥ 0.8 on basin-count orderings across perturbed instances). **No downstream result may rest on a probe that fails its validation gate.**

### 3.2 The coordinate-change operator

Adding extension variable z with definition z ↔ f(a,b,...) means: append the defining clauses, extend the space by one dimension. Landscape comparisons before/after must handle the dimension change honestly:

- Compare structure of the *projection*: basins restricted to original variables, with z propagated to its defined value (the "faithful embedding" view), AND
- Compare the full extended landscape (the "search-reality" view — a solver walks the extended space and z can be temporarily inconsistent with its definition; those inconsistent regions are precisely the new corridors).
- **Both views are required output.** The interesting physics, if any, is likely in the corridors — regions where z ≠ f(...) act as tunnels between basins that are disconnected in the projection. Measure corridor usage explicitly: fraction of sampled inter-basin paths that pass through definition-violating states.

### 3.3 Affine/GF(2) surgery (secondary operator)

Also implement basis change y = Ax + b over GF(2) as a second, purer coordinate operator (no dimension change). XOR-SAT is the validation family: the probes must show the landscape smoothing to a single basin under the eliminating basis. This is the **calibration experiment** — if the probes can't see the XOR-SAT transformation, they can't see anything, and the program stops at the probe drawing board.

---

## 4. Experimental program

Run in order. Each phase has a kill/branch criterion. Pre-register bars per experiment in-repo before runs, in the established style (one run per registered arm unless the registration says otherwise; determinism gates where applicable; all UNSAT proof claims dpr-trim-verified when solvers are involved).

### L0 — Probe bring-up + calibration (the XOR-SAT gate)

- Implement exact probes (n ≤ 26) and sampled probes.
- Calibration: random XOR-SAT instances, before/after Gaussian-elimination basis change. Required outcome: probes report rugged → single-basin transition. Validation gate for sampled-vs-exact per §3.1.
- **Kill criterion:** probes fail calibration after bounded effort → stop, report probe design as the bottleneck.

### L1 — The core measurement (H1 on pigeonhole)

Instances: PHP(4..7) exact (PHP(7)=42 vars exact-enumerable at 2^42? No — cap exact at total vars ≤ 26: PHP(4)=12, PHP(5)=20, PHP(6)=30 exceeds → PHP(4),PHP(5) exact; PHP(6..9) sampled). This size honesty is mandatory in the report.

Arms, per instance:
- A: baseline landscape (no extension variables).
- B: + Cook's construction variables (the known-good coordinates; implement the standard inductive definitions; add defining clauses only — not the proof).
- C: + BVA-selected variables (same count as B; the syntactic-criterion control).
- D: + random-definition variables (same count, same definition shapes as B — z ↔ (a∧b) over randomly chosen literals; the noise control).

Measurements: basin count, barrier matrix summary (mean/max inter-attractor barrier), corridor usage (§3.2), all in both views.

**Pre-registered readings:**
- H1-supported: B reduces basin count / barriers markedly below A, and below C and D under matched variable counts (register effect-size bars after L0 calibration variance is known — register them *before* L1 runs).
- H1-refuted-cleanly: B ≈ C ≈ D ≈ A on all probes → the geometric criterion does not distinguish known-good coordinates; the hypothesis dies with a measurement. This is a publishable boundary sentence: *ER's power on PHP is not visible as basin geometry.*
- Confounded: B differs but C matches B → compression and basin-merging coincide on PHP; disentangle on a second family before any H1 claim (Tseitin: known ER-helpful definitions exist along the parity structure; the predecessor project's generators supply instances).

### L2 — Family generalization (only if L1 supports or confounds)

Repeat L1 structure on Tseitin expanders (definitions along cycle/parity structure vs BVA vs random) and mutilated chessboard (definitions from the known counting arguments). Question: is basin-merging a *general* signature of proof-shortening definitions, or PHP-specific?

### L3 — The intervention (H2; only if H1 survives L1+L2)

- L3a (search-effect existence): take the *known-good* variables from L1/L2 arms, add their defining clauses to the formula, run stock CDCL (CaDiCaL) and a standard SLS solver; pre-registered question: does search improve at all when good coordinates are added *without* the proof being supplied? (It is a known open puzzle that ER-helpful definitions do not automatically help CDCL — this experiment measures that directly and its null is informative: *coordinates alone don't transfer; the proof-search must exploit them.*)
- L3b (selection loop): greedy/beam search over candidate definitions (bounded shapes: z ↔ l1∧l2 over structure-suggested literal pairs), scored by sampled basin-merging, added incrementally; compare against BVA-scored selection under identical candidate sets and budgets. Primary metric: solver performance (conflicts, wall clock) on families; secondary: probe scores. Kill criterion: if probe-guided selection cannot beat BVA-guided selection under matched budgets on any family after the registered sweep, H2 closes.

### L4 — (exploratory, unregistered until L3 resolves) Formula-space flow

If basin-merging works as a score, it is a candidate potential Φ for satisfiability-preserving flow in formula space (add/remove definitions, PR clauses, basis changes as moves; Φ-descent as dynamics). Do not design this before L3 lands.

---

## 5. Infrastructure inheritance and build notes

- Reuse: instance generators (PHP, chessboard, Tseitin, uf), the eventlog discipline and schema style, dpr-trim verification pipeline where proofs are claimed, the frozen-baseline/tagging protocol, pre-registration document format.
- New builds: the probe library (exact + sampled; standalone, solver-independent; Python/numpy acceptable for exact small-n, Rust or C for sampled probes at scale if profiling demands), the extension-variable toolkit (Cook construction generator for PHP; BVA either via existing SBVA tooling or reimplementation of the core heuristic; random-definition generator with matched shape distribution), GF(2) basis-change tool.
- Determinism: all sampling seeded; sampled-probe results reported with seed and sample-count; variance estimated by seed families (register the seed protocol in L0).
- Scope rule (inherited): if any component outgrows bounded effort on its planned substrate, stop and report with a named alternative rather than heroic surgery.

## 6. Honest framing: what the known tolls are

State these in every writeup; the program is designed so each has a measurement rather than a hope:

1. **Probe cost:** exact basin analysis is exponential (capped at n ≤ 26); sampled probes may be blind to the structure that matters. Mitigation: L0 calibration gate on XOR-SAT where the answer is known.
2. **The known ER-transfer puzzle:** helpful definitions provably shorten *proofs*, but solvers may not find those proofs — L3a measures exactly this gap and its null is a finding.
3. **Selection-cost migration:** if basin-merging scores are expensive to estimate, the exponential may migrate into the scoring (the conservation-law pattern). Report probe cost alongside any H2 gain; a win that spends more on scoring than it saves on solving is a null, and the registration for L3b must define the accounting.
4. **Small-n myopia:** effects at n ≤ 26 may not be the asymptotic story. Mitigation: sampled probes at 3–5× the exact sizes with validated rank-correlation; trends over size are required output, not single-size snapshots.

## 7. What success and failure each look like

- **Strong success:** H1 confirmed across families + L3b selection beats BVA under honest accounting → a geometric selection principle for the strongest practical proof system; genuinely new.
- **Valuable negative:** H1 cleanly refuted → "proof-shortening definitions are not basin-mergers" — a real boundary sentence about ER's power, measured for the first time.
- **Expected middle:** H1 partially holds, L3a shows the transfer gap, selection is confounded with compression → a mechanism map of *why* extended reasoning resists automation, in the style of the predecessor project's boundary map, one level up the tech tree.

All three outcomes produce the next paper section. The program cannot fail to produce a boundary sentence; it can only fail to be run honestly.
