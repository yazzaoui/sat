# Related work check (pre-draft, lead-directed)

## Ardelius & Zdeborová 2008 — the anticipated collision, resolved

"Exhaustive enumeration unveils clustering and freezing in the random
3-satisfiability problem," PRE 78, 040101(R) (2008); arXiv:0804.0362.

**What they did (overlaps S3a):** exhaustive enumeration of complete
SOLUTION sets of random 3-SAT at moderate sizes (solution enumeration
scales with |S|, not 2^n, so their reachable n exceeds ours for the
solution set itself); clusters = connected components (same canonical
definition); headline: cluster numbers correspond "surprisingly well"
with asymptotic predictions at moderate sizes; located the freezing
transition empirically.

**Consistency with S3:** their concordance claim is the
scaling/complexity view of cluster counts — the same direction our
POST-HOC normalized columns show (Nc/|S| rising with α at every n).
Our registered raw-count bar's "inversion" is the solution-collapse
confound (row-2 annotation) and must never be presented as
contradicting this paper; properly normalized, we agree with them on
S3a.

**What they did not and could not measure (the safe novelty, exactly
as the lead predicted):** everything requiring the FULL landscape —
- inter-cluster BARRIERS (merge levels: uniformly 1 through n=24,
  first lift-off at n=26);
- CORRIDOR structure (C₁ = 1.0 through n=24: every inter-cluster void
  a V=1 plateau flat);
- the landscape above the solutions generally, under the canonical
  artifact-controlled merge-tree framework;
- the plateau-dominance connection (plateau discovery + S2 lineage);
- UNSAT minimal-level curves across α;
- the registered-bars methodology itself.

**Paper-1 claim, sharpened by this check:** the solution-space
CLUSTER-COUNT story at small n was known (and matches theory in
normalized form — consistent with us); the new content is the
CONNECTING GEOMETRY — no ridges exist at solver-folklore sizes, every
void is a flat, and the ridge geometry has a measurable onset at
n ≈ 26. Nobody has measured barriers or corridors between clusters;
those rows (5, 6) and the onset are collision-free.

Sources: [arXiv:0804.0362](https://arxiv.org/abs/0804.0362),
[PRE 78, 040101](https://link.aps.org/doi/10.1103/PhysRevE.78.040101).
Full-text pass required during drafting for their exact n range and
any barrier-adjacent remarks; this note scopes the claim
conservatively until then.
