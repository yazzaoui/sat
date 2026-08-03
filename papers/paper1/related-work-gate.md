# Paper 1 — related-work gate: the Ardelius–Zdeborová full-text pass

Registration gate per lead directive (2026-08-02): the outline is not
drafted until we know precisely what the 2008-era exact-enumeration
work did and did not measure, because Paper 1's novelty claim is
scoped by that answer.

Source read in full: J. Ardelius, L. Zdeborová, *Exhaustive
enumeration unveils clustering and freezing in random 3-SAT*, Phys.
Rev. E 78, 040101(R) (2008); arXiv:0804.0362v2 (4 pp.).

## What A–Z measured

1. **Instances.** Random 3-SAT (`makewff`), full solution set
   enumerated with `relsat`. Sizes N = 25–150 for the cluster-count
   study; N ≤ 100 for freezing (memory-capped at < 5·10⁷ solutions).
   Median-by-solution-count instance of A = 999 formulas, B = 1000
   repetitions.
2. **Cluster definition = ours.** Clusters are connected components
   of the graph whose vertices are solutions and whose edges join
   solutions at Hamming distance 1 — exactly S3's flip-connectivity
   definition. Their footnote [37] rejects the "sub-extensive
   distance" alternative because 1-flip components share a whitening
   core; S3's definitional care has direct precedent, and the
   co-citation is natural, not defensive.
3. **Cluster COUNTS vs asymptotics.** The complexity function
   Σ(N) = ⟨log S⟩/N vs α, compared to the survey-propagation
   asymptotic prediction — "remarkably good" agreement near
   α_s = 4.267, already at N = 25–150. Plus the trend in the largest
   cluster's solution share below the clustering transition.
4. **Freezing.** Whitening (peeling) per solution; P_f(α, N) =
   probability an unfrozen solution exists, via random clause
   removal; crossing-point estimate α_f = 4.254 ± 0.009 ≈ α_s;
   comparison against SLS (α ≈ 4.21) and SP-decimation (α ≈ 4.252)
   performance limits.
5. **A finite-size observation of theirs we inherit:** properties
   related to clustering are *less* finite-size-sensitive than
   properties of solutions themselves.

## What A–Z did not measure — and could not, by construction

Their enumeration is of the **solution set only**. Every observable is
intrinsic to that set (component counts, sizes, whitening cores).
Consequently:

- **No inter-cluster terrain.** Nothing between clusters is examined:
  no barriers, no basin structure, no corridors, no V = #violated
  landscape. (Full state-space enumeration at their N is 2^N —
  unreachable; S3's n ≤ 26 full-space sweep is a different
  instrument, not a smaller version of theirs.)
- **No separation geometry.** No inter-cluster distances/gaps, no
  claim about what divides clusters or how high the divide is.
- **No basin/ruggedness analysis.** No canonical basin definition, no
  descent partitions, no tie-break-artifact question — the
  plateau-discovery axis is absent.
- **No size-axis onset.** Their transitions live on the α axis at
  fixed-N ensembles (crossing points). The question S3 answered —
  at what *n* do the narrative's geometric signatures first appear,
  concordantly — is not posed.

## Scoped novelty claim (the narrowed branch — as pre-committed)

Paper 1 does **not** claim first exact enumeration of clusters at
small n; A–Z own that, with our cluster definition, and their
count-concordance result stands unchallenged. Paper 1's contribution
is what their instrument could not see:

- **C1 (terrain).** Measured under a canonical basin definition, the
  landscape between and around clusters at exactly enumerable sizes:
  barriers uniformly 1, every inter-cluster void a V = 1 plateau
  corridor, C₁ = 1.0 through n = 24 (S3).
- **C2 (artifact).** Apparent ruggedness at these sizes is a
  descent-partition tie-break artifact; under the canonical
  definition the refutation landscape is one plateau system
  (landscape-surgery plateau discovery).
- **C3 (signals).** The folklore secondary-signal menu adds no
  structure beyond flatness-degree, steers at sub-1.5× at best, and
  traps up to 49% of walkers at worst (S2).
- **C4 (onset).** The clustering narrative's geometric signatures
  have a measurable size-axis onset: first concordant movements
  (corridors closing, barriers lifting, gaps jumping) at n = 26.
- **C5 (the frame that joins us to A–Z rather than against them).**
  The narrative's *counting* shadow arrives early (A–Z: counts match
  asymptotics from N = 25) while its *geometry* is absent below
  n ≈ 26 (us): "the flats where the field drew mountains" — the map's
  numbers precede its mountains, and solver-folklore sizes live in
  the gap.

All claims scoped to the finite-size shadow; asymptotics untouched;
confound annotations (S3 row 2, Nc/|S|) carried into the paper.

## Related-work spine (beyond A–Z)

- Krzakala–Montanari–Ricci-Tersenghi–Semerjian–Zdeborová PNAS 2007
  (the phase-diagram narrative being tested at finite size).
- Mézard–Mora–Zecchina PRL 2005; Achlioptas–Ricci-Tersenghi STOC
  2006 (rigorous clustering/frozen-variables results — asymptotic,
  explicitly not contradicted).
- Kroc–Sabharwal–Selman AUAI 2007 (frozen-fraction numerics at
  α = 4.20 — again solution-set observables).
- Mann–Hartmann / Zhou et al. cluster enumeration lineage — to be
  swept once at outline time for any *full-state-space* precedent;
  the pass above establishes none exists in the A–Z line, which is
  the line the field cites.
- Fitness-landscape literature building on descent-partition
  ruggedness (targets of C2) — list fixed at outline registration.

## Gate verdict

The narrowing branch fires, and it is the safe one: C1–C4 survive
untouched (none is a cluster count), C5 gains a co-citation ally, and
the novelty sentence is exact: **first full-state-space geometry of
the clustering narrative at exactly enumerable sizes, under a
canonical basin definition — where the narrative's counts were
already known to arrive early, we show its mountains arrive late.**
Outline registration may now be drafted (venue named) for lead
approval; prose remains fenced until that approval.
