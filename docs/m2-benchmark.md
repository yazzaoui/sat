# M2 benchmark: guided (probation-gated) vs stock vs CaDiCaL

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
| flat50-1 | counting | 0.01 | 0.08 | 0.01 | 0.08 | no-verdict | +0.08 |
| flat50-10 | counting | 0.01 | 0.02 | 0.00 | 0.02 | no-verdict | +0.02 |
| flat50-100 | counting | 0.01 | 0.04 | 0.00 | 0.04 | no-verdict | +0.04 |
| flat50-1000 | counting | 0.01 | 0.41 | 0.00 | 0.19 | pruning@0% | +0.19 |
| flat50-101 | counting | 0.00 | 0.24 | 0.00 | 0.16 | pruning@0% | +0.15 |
| flat75-1 | counting | 0.01 | 0.33 | 0.01 | 0.28 | pruning@0% | +0.27 |
| flat75-10 | counting | 0.01 | 16.11 | 0.00 | 0.52 | pruning@0% | +0.52 |
| flat75-100 | counting | 0.01 | 3.57 | 0.01 | 0.49 | pruning@0% | +0.49 |
| flat75-11 | counting | 0.01 | 0.62 | 0.01 | 0.40 | pruning@1% | +0.39 |
| flat75-12 | counting | 0.01 | 0.56 | 0.00 | 0.30 | pruning@0% | +0.29 |
| flat100-1 | counting | 0.00 | 1.92 | 0.01 | 0.38 | pruning@0% | +0.37 |
| flat100-10 | counting | 0.00 | timeout | 0.01 | 0.26 | pruning@0% | +0.26 |
| flat100-100 | counting | 0.01 | 31.06 | 0.01 | 0.68 | pruning@0% | +0.67 |
| flat100-11 | counting | 0.01 | 2.72 | 0.01 | 0.49 | pruning@0% | +0.48 |
| flat100-12 | counting | 0.01 | 0.83 | 0.01 | 0.41 | pruning@0% | +0.41 |
| flat125-1 | counting | 0.01 | 8.18 | 0.01 | 0.70 | pruning@0% | +0.70 |
| flat125-10 | counting | 0.01 | 1.29 | 0.01 | 0.64 | pruning@0% | +0.63 |
| flat125-100 | counting | 0.01 | 5.33 | 0.01 | 0.92 | pruning@2% | +0.91 |
| flat125-11 | counting | 0.01 | 1.34 | 0.01 | 0.84 | pruning@0% | +0.83 |
| flat125-12 | counting | 0.01 | 2.35 | 0.01 | 1.23 | pruning@0% | +1.23 |
| flat150-1 | counting | 0.01 | 50.22 | 0.01 | 1.83 | pruning@1% | +1.82 |
| flat150-10 | counting | 0.01 | 12.57 | 0.02 | 2.53 | pruning@2% | +2.51 |
| flat150-100 | counting | 0.01 | 30.75 | 0.00 | 1.99 | pruning@0% | +1.98 |
| flat150-11 | counting | 0.01 | 7.66 | 0.00 | 1.59 | pruning@0% | +1.59 |
| flat150-12 | counting | 0.01 | 27.46 | 0.01 | 1.99 | pruning@0% | +1.97 |
| flat200-1 | counting | 0.01 | timeout | 0.04 | 2.32 | pruning@1% | +2.28 |
| flat200-10 | counting | 0.04 | timeout | 0.04 | 1.70 | pruning@0% | +1.67 |
| flat200-100 | counting | 0.03 | timeout | 0.10 | 1.27 | pruning@1% | +1.18 |
| flat200-11 | counting | 0.02 | 38.05 | 0.01 | 2.48 | pruning@0% | +2.46 |
| flat200-12 | counting | 0.04 | timeout | 0.05 | 2.15 | pruning@0% | +2.10 |
| uf100-01 | - | 0.01 | 0.01 | 0.01 | 0.00 | no-verdict | -0.00 |
| uf100-010 | - | 0.01 | 0.01 | 0.01 | 0.00 | no-verdict | -0.00 |
| uf100-0100 | - | 0.01 | 0.01 | 0.01 | 0.00 | no-verdict | -0.00 |
| uf250-01 | - | 0.01 | 0.01 | 0.01 | 0.00 | no-verdict | -0.00 |
| uf250-010 | - | 0.01 | 0.01 | 0.01 | 0.00 | no-verdict | -0.00 |
| logistics.a | - | 0.01 | timeout | 0.02 | 68.14 | no-verdict | +68.12 |
| logistics.b | counting | 0.03 | timeout | 0.02 | timeout | no-verdict | - |
| logistics.c | counting | 0.02 | timeout | 0.01 | timeout | no-verdict | - |
| logistics.d | - | 0.03 | timeout | 0.03 | timeout | no-verdict | - |
| bmc-ibm-1 | - | 0.16 | timeout | 0.09 | 5.55 | pruning@0% | +5.46 |
| bmc-ibm-2 | - | 0.02 | 7.64 | 0.02 | 0.48 | pruning@0% | +0.46 |
| bmc-ibm-3 | - | 0.90 | timeout | 0.27 | 70.22 | pruning@0% | +69.95 |
| bmc-ibm-4 | - | 0.18 | timeout | 0.20 | 46.54 | pruning@0% | +46.34 |
| bmc-ibm-5 | - | 0.02 | timeout | 0.06 | timeout | no-verdict | - |
| mchess12 | counting+grid | 2.33 | 1.37 | 2.83 | 0.51 | templates@56% | -0.86 |
| mchess14 | counting+grid | 23.39 | 2.00 | 56.54 | 3.22 | templates@50% | +1.22 |
| php10 | counting | 5.19 | 0.01 | 10.14 | 0.02 | template@100% | +0.00 |
| php11 | counting | timeout | 0.02 | timeout | 0.03 | template@100% | +0.00 |

## Synthetic families (UNSAT, guided proofs dpr-trim-verified)

| instance | cadical | stock | gated | verdict | proof |
|---|---|---|---|---|---|
| php10 | 8.14 | 0.03 | 0.02 | template@100% | yes |
| php11 | 102.21 | 0.02 | 0.02 | template@100% | yes |
| php12 | timeout | 0.03 | 0.03 | template@100% | yes |
| php13 | timeout | 0.03 | 0.03 | template@100% | yes |
| mchess12 | 0.93 | 0.25 | 0.27 | templates@56% | yes |
| mchess14 | 20.91 | 1.41 | 1.47 | templates@50% | yes |
| mchess16 | 99.20 | 4.18 | 4.33 | templates@60% | yes |
| mchess18 | timeout | 31.20 | 30.82 | templates@54% | yes |
| tseitin30 | 0.86 | 0.05 | 0.05 | templates@19% | yes |
| tseitin40 | 45.89 | 0.83 | 0.89 | templates@14% | yes |
| tseitin50 | timeout | 0.12 | 51.46 | pruning@0% | yes |
