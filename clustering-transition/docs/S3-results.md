# S3 results — the split table: inverted signatures at n ≤ 24, first concordant hints at n = 26

255 cells, one run each, both trim valves unfired (0 gap-trimmed, 0
pairs-trimmed). All numbers exact. Raw:
[S3-results-data.json](S3-results-data.json). Bars applied by
[analyze_s3.py](../scripts/analyze_s3.py).

**Both registered caveats govern every sentence below**: measured
object = 1-flip components (not pure states); the k=3 quantitative
picture is a replica prediction (proofs are large-k). This verdict
reads *"the flip-connectivity geometry at accessible n does not match
the narrative's finite-size shadow"* — never "the replica prediction
is wrong."

## The per-signature table (registered split-verdict form)

| # | Signature | Bar outcome | What the data does instead |
|---|---|---|---|
| 1 | Giant-cluster decline | **FAIL** | No monotone decline; at n=16 f_max *rises* with α (ρ=+0.71): near threshold, surviving instances have few solutions in ONE small component. Only n=24 shows the predicted direction (ρ=−0.91). |
| 2 | Cluster-count growth in α | **FAIL — inverted** (verdict stands as registered) | N_c *decreases* with α at every n (ρ = −0.69…−0.93). **Confound, lead-annotated post-hoc (same genre as row 4):** the registered bar measured raw counts at fixed n while the solution set itself collapses with α — fewer solutions mechanically means fewer clusters, and the asymptotic claim is about growth in n relative to solution-space entropy, exactly the piece that came out concordant (N_c grows with n at fixed shattered-band α). Post-hoc descriptive columns (below) show the properly normalized quantity RISES with α — the inversion is partly the bar mis-projecting the theory into finite size. |
| 3 | Separation g ≥ 2 | CLEAR — minimally | Median gaps 2–2.5, flat in n at n ≤ 24: clusters are separated by the *minimum possible* amount, nothing extensive. (n=26: gaps 3, 3, 12 — first movement.) |
| 4 | k=3 late freezing | **FAIL — early and huge** | Median frozen fraction of the largest cluster: 0.19 at α=3.0, 0.60+ from α=3.86 — freezing "onset" ~a full unit of α before the predicted ≈4.254. Honest confound, flagged: frozen fraction anti-correlates with cluster size (n=24 medians: size 604 → frozen 0.19; size 38 → 0.62; size 16 → 0.79); tiny clusters freeze trivially. The registered metric is faithful; its thermodynamic reading needs large clusters that n ≤ 26 does not supply. |
| 5 | Rising barriers | **FAIL — perfectly flat** | Median inter-cluster merge level = 1 at every (n ≤ 24, α), Spearman exactly 0. No ridges exist at accessible sizes. (n=26: 1.5–2 — first movement.) |
| 6 | Corridor trigger C₁ ≥ 0.5 | **FIRES** | C₁ = 1.0 at every n ≤ 24 cell: **every** "separated" cluster pair is connected at V=1. The inter-cluster voids are flats — S2's lesson, now on the physics narrative's home instance class. n=26: C₁ drops to 0.67 (α ≤ 4.0) and 0.0 (α=4.2, one seed pair at barrier 2, gap 12). |

## Post-hoc descriptive columns (lead-directed; NOT verdict-bearing)

Computed from the existing data, clearly labeled post-hoc; the
registered bars stand as registered. Medians:

| n | Nc/\|S\| at α = 2.0 → 4.2 | log Nc / log \|S\| at α = 3.0 → 4.2 |
|---|---|---|
| 16 | 0.003 → 0.33 | 0.25 → 0.00 (tiny-\|S\| degeneracy) |
| 20 | 0.0002 → 0.24 | 0.24 → 0.32 |
| 24 | 0.0001 → 0.13 | 0.23 → 0.42 |

**Clusters-per-solution rises monotonically with α at every n** —
normalized by the collapsing solution set, fragmentation increases
with density, concordant with the narrative's direction. Full table:
[S3-posthoc-complexity.json](S3-posthoc-complexity.json).

Registered verdict category: not concordant (1, 2, 4, 5 fail), not
discordant-in-structure as defined (S3a itself fails), not absent
(trends are strong — some in the wrong direction). **Split table
stands as the verdict**, per registration.

## The finite-size story (S3c, the actual finding)

At n ≤ 24, the clustering narrative's shadow is not merely weak — the
solution-space geometry runs *backwards* in α (clusters are most
numerous at low density, coalescing toward threshold as solution sets
shrink), the barriers the picture predicts do not exist (uniformly 1),
and all inter-cluster connectivity is plateau corridors at V=1. At
n=26 — one size up — the first concordant movements appear
simultaneously: C₁ falls, barriers lift off 1, one gap jumps to 12.
**The asymptotic picture, whatever its truth, begins to bite somewhere
above n≈26 — and everything below is a different geometry entirely:
few, barely-separated, corridor-connected clusters in a landscape that
is flat between them.** Anyone extrapolating clustering intuition to
instances of tens of variables is reasoning about a regime where the
measured geometry is inverted.

The empirical threshold curve (reported per frame): at α = 4.267,
50–70% of instances remain SAT at n ≤ 24 — the threshold's finite-size
smearing is itself a full α-unit wide at these sizes, consistent with
known threshold scaling and part of why the phase labels do not attach.

## Candidate ledger sentence (for lead edit)

*Measured exactly at n ≤ 26 under artifact-controlled definitions, the
random 3-SAT solution space shows the clustering narrative's signatures
inverted or absent — cluster counts fall with density, barriers are
uniformly 1, and every inter-cluster void is a V=1 plateau corridor —
with the first concordant movements appearing only at n=26; the
physics picture's finite-size shadow, at solver-folklore sizes, is a
different geometry than the one the narrative describes.*
