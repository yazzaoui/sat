# S3 registration — quoted claims, measured feasibility, final bars

Committed before any structure computation. Feasibility measured
solution COUNTS and cell costs only (counts are the frame-requested
threshold curve and the trim decision); no cluster structure, no
merge trees, no barriers were computed before this document.

## 1. The physics claims, quoted precisely (what "concordant" is measured against)

For random 3-SAT (k=3), the replica-method predictions
(Krzakala–Montanari–Ricci-Tersenghi–Semerjian–Zdeborová 2007 lineage;
threshold numerics Mertens–Mézard–Zecchina):

- α_s ≈ 4.2667 — satisfiability threshold.
- α_d ≈ 3.86 — dynamical/clustering transition: below, the solution
  set is dominated by one cluster containing almost all solutions
  (whp); above, it shatters into exponentially many clusters, none
  dominant, mutually separated by Θ(n) Hamming distance.
- α_c ≈ 4.25 — condensation: the measure concentrates on O(1)
  largest clusters.
- Freezing (frozen variables — variables constant across a cluster —
  in dominant clusters): for k=3 predicted only very near α_s
  (≈ 4.254+); at lower α clusters are predicted unfrozen.
- **Rigor caveat, part of the registration:** shattering is PROVEN for
  large k (k ≥ 8 lineage, Achlioptas–Coja-Oghlan); for k=3 the
  quantitative picture is a replica prediction. S3 measures against
  the k=3 predictions as stated above; discordance at small n
  therefore reads against the finite-size reach of a heuristic
  picture, not against theorems (S3c pre-commitment, both directions).

## 2. Canonical objects

- **Cluster (S3a):** connected component of the exact V=0 set under
  1-flip adjacency (literature definition; tie-free at a level set).
- **Frozen fraction of a cluster:** fraction of variables taking one
  value across the entire cluster (exact bitwise AND/OR).
- **Inter-cluster gap:** minimum Hamming distance between clusters
  (exact, pairwise over cluster members; feasible at measured sizes).
- **Inter-cluster barrier (S3b):** the merge level of the two
  clusters' leaves in the canonical merge tree of the full landscape —
  computed by extending exact.c with a targets mode (track cluster
  representatives' roots during the persistence sweep; emit pairwise
  merge levels). Corridor fraction C_v = fraction of cluster pairs
  with merge level ≤ v (v = 1, 2): the plateau-vs-ridge question.
- **UNSAT cells (α near threshold):** S3b-only descriptive curve —
  min-level size and component count vs α (the plateau discovery's
  generalization sweep); no bar.

## 3. Sweep and feasibility (measured)

α ∈ {2.0, 3.0, 3.5, 3.86, 4.0, 4.1, 4.2, 4.267} × n ∈ {16, 20, 24} ×
seeds 1–10 (seed formula: Random(seed·1000+n), m = round(α·n), 3
literals/clause, no repeated variable in a clause). Registered
stretch: n=26 × α ∈ {3.86, 4.0, 4.2} × seeds 1–5, run within
time-box if the main sweep completes.

Measured feasibility (seeds 1–3 probe): solution counts peak ≈ 42K
(n=24, α=2.0) — **no low-α trim needed**; V-array cost ≈ 11 s/cell at
n=24 (main sweep ≈ 20 min total); n=26 stretch ≈ 45 s/cell + C-side
merge sweep seconds/cell (L0-measured). Cluster/pair analysis on
≤ 50K-state solution sets: trivial. Largest pairwise-gap computation
(42K² at α=2.0 n=24) ≈ 10⁹ word-ops — minutes, acceptable; if a cell
exceeds 10 min it is reported as gap-trimmed (cluster count/sizes
still exact) rather than silently skipped.

## 4. Registered signatures and final bars (before runs)

Per (n, α) cell: medians over SAT seeds. Trends = Spearman over the
α-grid at fixed n, and over n at fixed α. "Shattered band" :=
α ∈ {3.86, 4.0, 4.1, 4.2}.

1. **Giant-cluster fraction** f_max = |largest cluster|/#solutions.
   Concordant: median f_max ≥ 0.9 at α ≤ 3.0 for every n, AND
   Spearman(f_max, α) ≤ −0.5 at every n, AND median f_max at fixed
   shattered-band α non-increasing in n.
2. **Cluster count** N_c: Spearman(N_c, α) ≥ +0.5 on α ∈ [3.0, 4.2]
   at every n, AND median N_c in the shattered band increasing in n.
3. **Separation** g/n (min inter-cluster Hamming gap, normalized):
   concordant = median g ≥ 2 in the shattered band (clusters truly
   separated, not adjacent) AND median g/n non-decreasing in n.
4. **Freezing:** median frozen fraction of the largest cluster ≈ 0
   (< 0.05) for α ≤ 4.0, with positive onset (≥ 0.1) if anywhere only
   at α ≥ 4.2 — the k=3 near-threshold prediction.
5. **Barriers (S3b):** median inter-cluster merge level B:
   Spearman(B, α) ≥ +0.5 at every n AND median B in the shattered
   band non-decreasing in n.
6. **Corridor fraction (S3b):** C₁ reported as a curve.
   **Discordant-in-structure trigger:** C₁ ≥ 0.5 in the shattered
   band at the largest completed n — half or more of "separated"
   cluster pairs actually connected by V=1 plateau corridors (voids
   that are flats).

Verdicts: **Concordant** = signatures 1–5 all clear. **Discordant in
structure** = S3a signatures (1–4) clear but trigger 6 fires or
signature 5 fails. **Absent** = |Spearman| < 0.3 for signatures 1, 2,
5 at every n. **Split verdicts** reported per-signature per-sub-
question; any mixed outcome is stated as the per-signature table, not
forced into a single word.

## 5. Discipline

One run per cell; no metric additions; per-cell provenance (seed
formula above); every headline number in reproduce.py; scope rule on
the exact.c targets extension; time-box 3 weeks; ledger sentence on
closure regardless of branch. Instruments await lead approval of this
registration before code.
