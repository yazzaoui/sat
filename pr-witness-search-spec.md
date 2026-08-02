# Project: Instrumented Witness Search for Satisfaction-Driven Clause Learning (SDCL)

## One-line summary

Build measurement, structure-recovery, and (eventually) learned-guidance infrastructure for discovering **propagation-redundant (PR) clauses** in SAT solving — the strongest practical proof system whose bottleneck is proof *search*, not proof *size*.

---

## 1. Background and motivation

### 1.1 The setting

- SAT solvers based on CDCL (conflict-driven clause learning) are polynomially equivalent to the **resolution** proof system. Resolution has proven exponential lower bounds on natural formula families: pigeonhole (PHP), mutilated chessboard, Tseitin formulas on expanders. On these, every CDCL solver takes exponential time, no matter how well engineered.
- The **PR (propagation redundancy)** proof system (Heule, Kiesl, Biere) admits **polynomial-size** proofs of these same families — without introducing new variables. PR clauses are "satisfiability-preserving" deletions of search space: a PR clause bans a region R of the assignment space, justified by a **witness** ω (a partial assignment) such that any hypothetical solution inside R can be transformed via ω into a solution outside R. Informally: machine-checkable "without loss of generality" arguments.
- Checking that a clause is PR with respect to a given witness is **polynomial time** (unit-propagation based). Verified proof checkers exist (`dpr-trim`).
- The solver paradigm that learns PR clauses during search is **SDCL** (satisfaction-driven clause learning), reference implementation **SaDiCaL** (Heule). It finds witnesses by constructing a "positive reduct" formula at stuck points and solving it with a sub-solver.

### 1.2 The gap this project attacks

PR certificates for the hard families are short, and the checker is fast. What is missing is any principled method to **find** witnesses:

- SaDiCaL's witness search is nearly structureless (heuristic candidate selection + sub-solver call). It rediscovers PHP proofs but generally loses to plain CDCL on industrial instances because witness-hunt overhead is not repaid.
- No published empirical characterization exists of what successful witnesses look like (size, locality, structure).
- Known theory (Atserias–Müller 2019 and successors): resolution is not automatable unless P=NP; general poly-time proof search is off the table. This bounds ambition but says nothing about structured/semantic instance families, where all industrial value lies.

### 1.3 Project thesis

Witnesses are semantic objects (solution-rearrangement maps: swaps, shifts, local reconfigurations) currently hunted at the syntactic clause level. If we (a) measure what real witnesses look like, (b) recover problem structure from clause soup, and (c) guide the search with templates and later a learned ranker, SDCL can consistently beat CDCL on structured instance classes. Every proposed witness is validated by the poly-time checker before use, so guidance may be unreliable without ever compromising soundness.

---

## 2. Prior art to build on (do not rebuild)

| Component | Artifact | Notes |
|---|---|---|
| CDCL baseline | CaDiCaL / Kissat (Biere) | Modern, clean C/C++ codebases |
| SDCL reference | SaDiCaL (Heule) | Finds PR clauses via positive reduct; the codebase to instrument |
| PR proof checker | dpr-trim; formally verified checkers exist | Poly-time validation of PR proofs |
| Pretrained PR clauses | PReLearn (Reeves et al.) | Learns useful PR clauses before search |
| Neural SAT baseline | NeuroSAT lineage; PyTorch Geometric | GNN message passing over formula graphs; known weakness: learns encodings, shatters under re-encoding |

Required reading (~60 pp total, all readable):
1. Heule, Kiesl, Biere — "Short Proofs Without New Variables" (PR system)
2. Heule, Kiesl, Seidl, Biere — "Encoding Redundancy for Satisfaction-Driven Clause Learning" (SDCL / positive reduct)
3. Atserias, Müller — "Automating Resolution is NP-Hard" (the ceiling; skim)

---

## 3. Benchmark families (scoreboard)

Scalable families with known exponential-for-resolution / polynomial-for-PR behavior:

- **PHP(p, h)**: p pigeons, h = p−1 holes. Variables x_{i,j} = pigeon i in hole j. Clauses: each pigeon somewhere (wide clause per pigeon); no two pigeons share a hole (pairwise binary clauses per hole).
- **Mutilated chessboard(n)**: domino tiling of an n×n board with two opposite corners removed.
- **Tseitin formulas** on expander graphs (parity constraints on edges).
- Structured SAT Competition instances (verification, planning, combinatorial) for generalization tests.
- Random 3-SAT at clause/variable ratio 4.25 as a *negative control* — no structure; the method is expected to yield nothing here, and that expectation should be verified and reported.

Success metric per phase: wall-clock and conflict-count comparison of {CaDiCaL, stock SaDiCaL, this project's guided SDCL} across families and sizes, plus verified PR proofs via dpr-trim for every solved UNSAT instance.

---

## 4. Work plan

### Phase 0 — Toolchain bring-up (days)

1. Build CaDiCaL, SaDiCaL, dpr-trim from source (Linux, make).
2. Write DIMACS generators for PHP(n) and chessboard(n) (~50 lines each, any language).
3. Reproduce the headline separation: CaDiCaL times out on PHP(10)–PHP(12); SaDiCaL solves them and emits PR proofs; dpr-trim verifies the proofs.
4. Deliverable: a repeatable benchmark harness (scripts + results table) demonstrating the separation.

### Phase 1 — Witness instrumentation and atlas (2–3 weeks)

1. Patch SaDiCaL to emit a structured event log (JSONL) of every witness attempt: candidate clause, witness ω, accept/reject, positive-reduct solve time, decision level, assignment trail snapshot / conflict context at the stuck point. Treat the run as an event-sourced, replayable log.
2. Build an analysis layer:
   - Construct the **variable-interaction graph** (variables = nodes; co-occurrence in a clause = edge).
   - For each accepted witness: footprint size (#variables), graph radius from the conflict/stuck region, overlap with the banned clause, pattern classification (swap of two variable blocks, cyclic shift, local rearrangement, other).
3. Run over PHP(6..12), chessboard(6..14), Tseitin instances, and ≥20 structured competition instances.
4. Deliverables:
   - **Witness atlas**: empirical distributions of witness size, locality, and pattern class per family.
   - A locality report: is witness footprint concentrated within small graph radius of the stuck region? (This is the key empirical question; a positive answer motivates everything downstream and defines the feature set for Phase 3.)

### Phase 2 — Structure recovery and witness templates (1–2 months)

1. Standalone preprocessing binary: given DIMACS, detect and tag higher-level structure:
   - **Cardinality blocks**: pattern-match clause signatures of standard at-most-k encodings (pairwise, sequential, commander, totalizer).
   - **XOR chains** (for Tseitin/parity structure).
   - **Grid/lattice adjacency** patterns (for tiling-style instances).
   - Symmetry residues (via saucy/breakid-style graph automorphism detection, as a tagging aid — not as the main mechanism).
   Output: a typed overlay mapping clause groups → semantic constructs.
2. Validation: the pass must tag PHP as "counting" and chessboard as "grid + counting" without being told.
3. Hand-written **witness templates** per structure type (e.g., counting structures → block-swap witnesses; grids → local rearrangement witnesses). Integrate template proposal into SaDiCaL's candidate loop ahead of the generic positive-reduct search.
4. Deliverable: guided SDCL vs stock SaDiCaL vs CaDiCaL benchmark. Target: consistent wins on the structured families; honest reporting on competition instances and the random-3SAT negative control.

### Phase 3 — Learned guidance (months, optional/stretch)

1. GNN over the variable-interaction graph (NeuroSAT-style message passing) trained to **rank** candidate (banned-clause, witness) pairs.
2. Training data: Phase 1 event logs (supervised) + self-play on generated families (PHP(n), chessboard(n) give an infinite curriculum; the PR checker provides free ground-truth labels — no human annotation ever).
3. Mitigate the known encoding-overfit failure mode by training on Phase 2's canonicalized/typed representation, not raw clauses; test transfer across re-encodings of the same problems.
4. Deliverable: learned ranker vs template baseline; and a **failure map** — the instance classes where learned witness search stalls (expected: random threshold, crypto). The failure map is itself a research contribution (empirical probe of the automatability boundary).

---

## 5. Architecture notes

- Solver core stays C/C++ (patched SaDiCaL); analysis/training in Python; if a Rust component is desired for generators/analysis, PyO3 bindings are a known-good pattern.
- Every learned or template-proposed witness passes through the PR check (unit propagation) before being learned; soundness never depends on the proposer. All emitted proofs must verify under dpr-trim.
- Event logs are the ground truth for everything: replayable, diffable, and the training corpus. Design the log schema first.

## 6. Explicit non-goals and known ceilings

- **No general poly-time witness finder is possible** unless P=NP (non-automatability results). The target regime is structured/semantic instances only.
- Random 3-SAT near the threshold is expected to be untouched (no structure, and likely no short PR proofs). It is a control, not a target.
- Beating CDCL on broad industrial portfolios is not the Phase-2 bar; beating it on recognized structured families with verified proofs is.

## 7. Risks

| Risk | Mitigation |
|---|---|
| Witness locality hypothesis false | Phase 1 answers this cheaply before larger investment |
| Structure detection brittle across encodings | Restrict to published encoding signatures first; measure coverage honestly |
| GNN learns encodings, not problems | Train on canonicalized overlay; re-encoding transfer tests as a first-class metric |
| Positive-reduct overhead dominates | Template-first proposal order; budget caps per stuck point; fall back to plain CDCL behavior |

## 8. Milestone summary

| Milestone | Evidence |
|---|---|
| M0: separation reproduced | CaDiCaL vs SaDiCaL table on PHP + verified proofs |
| M1: witness atlas | Distributions + locality report over ≥3 families |
| M2: guided SDCL wins | Benchmark table: guided > stock SaDiCaL > CaDiCaL on structured families |
| M3: learned ranker + failure map | Transfer results + documented stall classes |
