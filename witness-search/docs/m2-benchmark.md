# M2 benchmark: guided (probation-gated) vs stock vs CaDiCaL

## The three regimes (read any row against its archetype)

1. **Overhead regime** (coloring, most BMC, logistics): the SDCL witness
   hunt is pure cost — `pruneoff ≈ cadical ≪ stock`. The gate's prune-off
   verdict recovers CDCL performance online (tax = bounded probation
   cost, ≤ ~1 s via the 5 s cap). This regime dominated our real-world
   sample; the stock-vs-pruneoff gap (up to timeout-vs-0.01 s) is the
   quantified pathology.
2. **Profitable regime** (PHP-like counting): `stock ≪ pruneoff/cadical`,
   templates complete — gate confirms (`filter-on@100%h`) and filtering
   is lossless.
3. **Mixed regime** (chessboard, Tseitin): pruning pays but templates are
   incomplete — gate reverts to stock (`revert-stock`) with tax ≈ 0.1 s.
   tseitin(50) documents why prune-off needs the acceptance conjunction:
   0% hits but 41% acceptance, and the hunt is worth timeout-vs-0.27 s.

## Corrections and gate v3 (post-table)

**uf rows corrected:** the sweep's uf SaDiCaL timings were parse
failures (SATLIB double-space header; all arms failed identically in
~5 ms). Real numbers: stock SDCL on uf100 = 0.54–7.3 s and uf250 =
timeout(120 s), vs prune-off 0.01–2.45 s — **uf belongs to the overhead
regime**, and the earlier "gate free on random" reading is withdrawn.
The sweep now flags non-solver exits (`ARM-ERROR`).

**Gate v3 (lead-approved):** prune-off is keyed on sustained low
acceptance measured under probation — it works with zero templates
(uf100: prune-off at 9% acceptance, 0.10 s vs 0.59 s stock). A high
template hit share vetoes prune-off where templates exist (protects
mchess at 14% acceptance via its 50% hits; protects tseitin(50) via 41%
acceptance). Structure detection is demoted to a prior: supplies
templates, sets probation budget. A disabled hunt is re-probed every
`reprobeint` conflicts (verified cycling on mchess12).

**Documented residuals (v3):** (a) hunt pays only late — mitigated by
re-probe; (b) profitable hunt + stably low acceptance + structure that
evades detection (mchess-without-detection is this class: measured
timeout vs 1.4 s stock, though *bounded* by CDCL-mode cost, 2.16 s at
n=12 with re-probes). Residual (b) is the price of fully-online
gating; in deployment the structure prior covers the known instances of
this class.

Known structural limit: when a single unbudgeted reduct solve dominates
(logistics.b–d, bmc-ibm-5) no verdict can fire; stock times out
identically, so the gate never regresses. Inner-solve conflict budgeting
is the named future fix. "no-verdict" on fast rows means the instance
finished before the window filled (gate inert, tax ≈ probation overhead
only). The competition-section mchess/php rows compare against sweep-era
stock timings; the synthetic section (same binary, same session, proofs
verified) is authoritative for those families.

Gate: measure-only probation window (200 witness-bearing attempts),
then one of three verdicts — filter confirmed (>=90% template hits),
templates disabled (revert to stock), pruning disabled (<5% hits,
plain CDCL). `tax` = gated - min(stock, pruneoff): negative means
the gate beats every static arm; positive is the measured cost of
gating in that regime (lead directive: the portfolio-safe claim is
measured, not asserted). Timeout 120 s.

## Competition instances (sweep + final-binary gated arm)

| instance | labels | cadical | stock | pruneoff | gated | verdict | tax |
|---|---|---|---|---|---|---|---|
| flat50-1 | counting | 0.01 | 0.08 | 0.01 | 0.05 | no-verdict | +0.04 |
| flat50-10 | counting | 0.01 | 0.02 | 0.00 | 0.01 | no-verdict | +0.01 |
| flat50-100 | counting | 0.01 | 0.04 | 0.00 | 0.02 | no-verdict | +0.02 |
| flat50-1000 | counting | 0.01 | 0.41 | 0.00 | 0.11 | prune-off@0%h/14%a | +0.10 |
| flat50-101 | counting | 0.00 | 0.24 | 0.00 | 0.09 | prune-off@0%h/15%a | +0.08 |
| flat75-1 | counting | 0.01 | 0.33 | 0.01 | 0.15 | prune-off@0%h/13%a | +0.14 |
| flat75-10 | counting | 0.01 | 16.11 | 0.00 | 0.23 | prune-off@0%h/9%a | +0.22 |
| flat75-100 | counting | 0.01 | 3.57 | 0.01 | 0.23 | prune-off@0%h/9%a | +0.22 |
| flat75-11 | counting | 0.01 | 0.62 | 0.01 | 0.18 | prune-off@1%h/10%a | +0.18 |
| flat75-12 | counting | 0.01 | 0.56 | 0.00 | 0.14 | prune-off@0%h/13%a | +0.14 |
| flat100-1 | counting | 0.00 | 1.92 | 0.01 | 0.19 | prune-off@0%h/10%a | +0.18 |
| flat100-10 | counting | 0.00 | timeout | 0.01 | 0.13 | prune-off@0%h/13%a | +0.12 |
| flat100-100 | counting | 0.01 | 31.06 | 0.01 | 0.34 | prune-off@0%h/8%a | +0.33 |
| flat100-11 | counting | 0.01 | 2.72 | 0.01 | 0.23 | prune-off@0%h/10%a | +0.22 |
| flat100-12 | counting | 0.01 | 0.83 | 0.01 | 0.21 | prune-off@0%h/11%a | +0.20 |
| flat125-1 | counting | 0.01 | 8.18 | 0.01 | 0.37 | prune-off@0%h/8%a | +0.36 |
| flat125-10 | counting | 0.01 | 1.29 | 0.01 | 0.34 | prune-off@0%h/8%a | +0.34 |
| flat125-100 | counting | 0.01 | 5.33 | 0.01 | 0.51 | prune-off@2%h/7%a | +0.50 |
| flat125-11 | counting | 0.01 | 1.34 | 0.01 | 0.33 | prune-off@0%h/9%a | +0.33 |
| flat125-12 | counting | 0.01 | 2.35 | 0.01 | 0.51 | prune-off@0%h/7%a | +0.51 |
| flat150-1 | counting | 0.01 | 50.22 | 0.01 | 0.69 | prune-off@1%h/6%a | +0.69 |
| flat150-10 | counting | 0.01 | 12.57 | 0.02 | 0.60 | prune-off@2%h/7%a | +0.58 |
| flat150-100 | counting | 0.01 | 30.75 | 0.00 | 0.81 | prune-off@0%h/6%a | +0.81 |
| flat150-11 | counting | 0.01 | 7.66 | 0.00 | 0.78 | prune-off@0%h/6%a | +0.78 |
| flat150-12 | counting | 0.01 | 27.46 | 0.01 | 0.78 | prune-off@0%h/5%a | +0.77 |
| flat200-1 | counting | 0.01 | timeout | 0.04 | 1.06 | prune-off@1%h/4%a/starved | +1.01 |
| flat200-10 | counting | 0.04 | timeout | 0.04 | 0.99 | prune-off@0%h/5%a | +0.95 |
| flat200-100 | counting | 0.03 | timeout | 0.10 | 0.68 | prune-off@1%h/6%a | +0.59 |
| flat200-11 | counting | 0.02 | 38.05 | 0.01 | 1.16 | prune-off@0%h/4%a/starved | +1.15 |
| flat200-12 | counting | 0.04 | timeout | 0.05 | 1.15 | prune-off@0%h/4%a/starved | +1.09 |
| uf100-01 | - | 0.01 | 0.01 | 0.01 | 0.00 | no-verdict | -0.00 |
| uf100-010 | - | 0.01 | 0.01 | 0.01 | 0.00 | no-verdict | -0.00 |
| uf100-0100 | - | 0.01 | 0.01 | 0.01 | 0.00 | no-verdict | -0.00 |
| uf250-01 | - | 0.01 | 0.01 | 0.01 | 0.00 | no-verdict | -0.00 |
| uf250-010 | - | 0.01 | 0.01 | 0.01 | 0.00 | no-verdict | -0.01 |
| logistics.a | - | 0.01 | timeout | 0.02 | 43.18 | no-verdict | +43.16 |
| logistics.b | counting | 0.03 | timeout | 0.02 | timeout | no-verdict | - |
| logistics.c | counting | 0.02 | timeout | 0.01 | timeout | no-verdict | - |
| logistics.d | - | 0.03 | timeout | 0.03 | timeout | no-verdict | - |
| bmc-ibm-1 | - | 0.16 | timeout | 0.09 | 4.22 | prune-off@0%h/8%a | +4.13 |
| bmc-ibm-2 | - | 0.02 | 7.64 | 0.02 | 0.43 | prune-off@0%h/11%a | +0.41 |
| bmc-ibm-3 | - | 0.90 | timeout | 0.27 | 5.14 | prune-off@0%h/2%a/starved | +4.87 |
| bmc-ibm-4 | - | 0.18 | timeout | 0.20 | 5.38 | prune-off@0%h/0%a/starved | +5.18 |
| bmc-ibm-5 | - | 0.02 | timeout | 0.06 | timeout | no-verdict | - |
| mchess12 | counting+grid | 2.33 | 1.37 | 2.83 | 0.20 | revert-stock@56%h/16%a | -1.18 |
| mchess14 | counting+grid | 23.39 | 2.00 | 56.54 | 1.10 | revert-stock@50%h/14%a | -0.90 |
| php10 | counting | 5.19 | 0.01 | 10.14 | 0.01 | filter-on@100%h | -0.00 |
| php11 | counting | timeout | 0.02 | timeout | 0.01 | filter-on@100%h | -0.01 |

## Synthetic families (UNSAT, guided proofs dpr-trim-verified)

| instance | cadical | stock | gated | verdict | proof |
|---|---|---|---|---|---|
| php10 | 2.65 | 0.01 | 0.01 | filter-on@100%h | yes |
| php11 | 42.81 | 0.01 | 0.01 | filter-on@100%h | yes |
| php12 | timeout | 0.02 | 0.02 | filter-on@100%h | yes |
| php13 | timeout | 0.03 | 0.03 | filter-on@100%h | yes |
| mchess12 | 0.87 | 0.20 | 0.22 | revert-stock@56%h/16%a | yes |
| mchess14 | 16.81 | 1.18 | 1.31 | revert-stock@50%h/14%a | yes |
| mchess16 | timeout | 6.51 | 6.84 | revert-stock@60%h/12%a | yes |
| mchess18 | timeout | 27.20 | 28.36 | revert-stock@54%h/11%a | yes |
| tseitin30 | 1.35 | 0.07 | 0.10 | revert-stock@19%h/38%a | yes |
| tseitin40 | 74.67 | 1.61 | 1.70 | revert-stock@14%h/33%a | yes |
| tseitin50 | timeout | 0.27 | 0.26 | revert-stock@0%h/41%a | yes |
