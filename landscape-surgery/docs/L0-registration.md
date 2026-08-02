# L0 registration — landscape probes and the XOR-SAT calibration gate

Committed before any probe code (cadence: lead approves this document
first). This registration also fixes the program-wide definitions that
L1+ will reference; changing any of them later requires a written
amendment committed before the affected runs.

## 1. Canonical definitions (program-wide)

### 1.1 Landscape

State space: full assignments over the current variable set (original
variables plus any extension variables in the arm). Height
V(x) = number of unsatisfied clauses under the current clause set
(original + definition clauses). Adjacency: 1-bit flips.

**Scope sentence (pinned, and carried into every result table's
caption):** all L-series basin/barrier claims are about the *SLS
landscape* — V under 1-flip adjacency. The CDCL bridge is L3a's to
earn; no earlier result may be read as a CDCL statement.

### 1.2 Basins and barriers — merge-tree canonical

The canonical structure is the **persistence merge tree** of V:
process states in increasing V-order (level sweep), union-find over
1-flip edges within the swept region.

- **Basin** = leaf of the merge tree = connected component of a
  local-minimum plateau (a maximal connected set of equal-V states
  with no lower neighbor) together with its attraction as leaves merge.
  Basin *count* = number of leaves.
- **Barrier(b₁,b₂)** = merge level of the two leaves (min-max path
  height), from the same sweep.

One deterministic object yields both quantities; no tie-breaking
exists to influence results.

**Disagreement check:** steepest-descent partition with lexicographic
tie-breaking is computed alongside on exact instances. If basin
counts/orderings diverge materially from the merge tree (>10% count
disagreement or any rank flip between arms), the divergence is
*reported*, never silently adjudicated.

### 1.3 Views under extension (dimension change)

- **Projection view:** landscape over original variables with each
  extension variable propagated to its defined value.
- **Search-reality view:** landscape over the full extended space;
  definition-violating states are legal states.
- Both views are required output wherever computable. **Corridor
  usage** = fraction of sampled inter-basin paths passing through at
  least one definition-violating state (protocol §3.3).

### 1.4 Exactness accounting (per-view, corrected from SPEC §L1)

The measured object includes extension variables, so exactness is
counted on the *extended* space per view:

| Instance | Projection view | Search-reality view |
|---|---|---|
| PHP(4) + full Cook cascade (12+8=20 vars) | exact | **exact — the anchor** |
| PHP(5) + one Cook layer (20+12=32 vars) | exact (20 vars) | sampled |
| PHP(6+), Tseitin, chessboard arms | sampled | sampled |

PHP(4) is the anchor where sampled probes must prove themselves
against full ground truth in both views. **Held-in-reserve option
(named, not exercised):** a C exact probe stretched to 2²⁸–2³⁰,
triggered only if L1 returns confounded *and* the confound plausibly
lives in PHP(5) corridor sampling.

## 2. L0 deliverables

1. **Exact probe** (C core, Python driver): full enumeration V
   evaluation (bit-tricks), persistence sweep → basin count, basin
   sizes, barrier matrix; plus the lexicographic-descent disagreement
   check. Capacity target: 2²⁶ states.
2. **Sampled probes** (Python first; ported only if profiling demands):
   a. Basin sampling: R random starts → noisy-free steepest descent
      (plateau walks with bounded patience) → endpoint clustering by
      plateau-component identity; estimates basin count and coverage.
   b. Barrier sampling: noisy-descent first-passage walks between
      attractor pairs (§3.3 ensemble); report estimated merge levels.
   c. Autocorrelation length of V along uniform random walks.
   d. Solution-cluster connectivity on satisfiable instances
      (sampled solutions via SLS restarts; cluster by connectivity
      under 1-flips within the solution set; report cluster count).
3. **GF(2) affine basis-change tool** (y = Ax + b; produces the
   transformed clause set for XOR instances).
4. **`reproduce.py` from day one**: every L0 claim lands as a check
   the day it exists (seeded, deterministic).

## 3. Protocols

### 3.1 Seed protocol

All sampling seeded. Seed families {1..10} per (instance, probe);
report median and IQR across seeds; every sampled number carries
(seed, sample count) in the log. Event logs are JSONL in the
witness-search schema style; schema file committed with the probe
code.

### 3.2 Sampled-vs-exact validation gate

On every instance where both are computable: Spearman rank correlation
of sampled vs exact basin counts across a registered perturbation
family (instance + K clause-order/seed perturbations) must be
**≥ 0.8**, and barrier-ordering correlation likewise ≥ 0.8. Any
adjustment to these bars happens before L1, in writing, justified by
L0 pilot variance. No downstream result may rest on a probe that
failed its gate.

### 3.3 Corridor ensemble (registered here for L1's use)

Between each ordered attractor pair (b₁,b₂): N=200 noisy-descent
walks (ε-greedy: with probability ε=0.1 take a uniform random
neighbor, else steepest descent with plateau patience P=2n flips),
started at b₁'s minimum plateau, terminated at first entry into any
other basin's plateau or at cap L=50n flips; record reached basin,
path max-V, and whether any visited state violates a definition.
**Null corridor rate:** the same ensemble run under arm-D
(random-definition) landscapes provides the matched baseline; arm-B
corridor usage is always reported against arm-D's, never against
zero.

## 4. Calibration experiment (the L0 gate)

Instances: random 3-XOR at densities m/n ∈ {0.7, 0.9} (rugged
regime), n ∈ {16, 20, 24} exact + {40, 60} sampled, 10 seeds each.
Arms: identity basis vs Gaussian-elimination basis (§2.3 tool).

**Required outcome (kill criterion of the whole program):** under the
canonical merge-tree definition, probes must report the rugged →
single-basin transition — exact probes: basin count > some
instance-dependent plural value before, exactly 1 after (all
satisfiable instances; for UNSAT XOR instances the after-basis
landscape must show a single minimum plateau at the violated-equation
count); sampled probes: the same transition through the validation
gate. **If the probes cannot see the XOR transformation after bounded
effort, the program stops at the probe drawing board and reports
probe design as the bottleneck.**

## 5. What L0 does NOT do

No PHP arms, no Cook construction, no BVA, no basin claims about any
non-XOR family. The extension-variable toolkit and the L1 effect-size
bars are registered separately after L0's calibration variance is
known — before L1 runs, per SPEC.

## 6. Decisions incorporated (lead-approved)

1. Per-view exactness table (§1.4); exact-frontier stretch held in
   reserve with named trigger.
2. Merge-tree canonical (§1.2); lexicographic-descent divergence
   reported, not adjudicated; XOR gate passed under the canonical
   definition.
3. SAT siblings (PHP(n,n), even-charge Tseitin) are **in scope for
   L1**, dual reading registered: SAT = "do good coordinates connect
   solution clusters"; UNSAT = "do they merge the trap structure of
   the refutation landscape."
4. BVA degeneracy at exact sizes: no padding, no relaxed criterion;
   report BVA candidate count and best compression gain even when the
   arm is empty ("BVA found nothing to do on PHP(4)" is a data point).
5. Scope sentence pinned (§1.1), in prose and in table captions.
