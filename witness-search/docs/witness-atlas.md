# Witness atlas (M1)

Per-instance witness statistics from SaDiCaL `--eventlog` runs.
`diam` = interaction-graph diameter (double-sweep lower bound);
`med_rad`/`max_rad` = BFS distance of flipped variables from the
banned-clause variables — the locality measure. `med_foot` = median
witness footprint (#vars); `med_flip` = median #flipped literals.
`null_rad` = median radius of random variable sets of the same size
as the flipped set (50 samples/witness, seed 0); `below_null` = share
of witnesses strictly below their own null median. Locality is only
claimed where true radius sits well below null.

| family | size | vars | diam | attempts | accepts | acc_rate | med_foot | med_flip | med_rad | max_rad | null_rad | below_null | patterns |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| mchess | 6 | 56 | 7 | 49 | 22 | 45% | 24.5 | 5.0 | 2.0 | 5 | 5.0 | 86% | {'exchange-cycle': 9, 'parity-cycle': 8, 'other': 4, 'parallel-exchange': 1} |
| mchess | 8 | 108 | 11 | 415 | 98 | 24% | 46.0 | 7.5 | 2.0 | 4 | 6.25 | 98% | {'exchange-cycle': 82, 'other': 7, 'parity-cycle': 6, 'parallel-exchange': 3} |
| mchess | 10 | 176 | 15 | 2119 | 422 | 20% | 85.0 | 8.0 | 2.0 | 8 | 8.0 | 99% | {'exchange-cycle': 306, 'parallel-exchange': 80, 'other': 21, 'parity-cycle': 15} |
| mchess | 12 | 260 | 19 | 5138 | 983 | 19% | 105 | 8 | 2 | 10 | 10.0 | 100% | {'exchange-cycle': 805, 'parallel-exchange': 137, 'other': 25, 'parity-cycle': 16} |
| mchess | 14 | 360 | 23 | 15653 | 2487 | 16% | 118 | 10 | 2 | 15 | 12.0 | 99% | {'exchange-cycle': 1960, 'parallel-exchange': 425, 'parity-cycle': 63, 'other': 39} |
| mchess | 16 | 476 | 27 | 39311 | 5787 | 15% | 157 | 12 | 2 | 15 | 13.0 | 99% | {'exchange-cycle': 4175, 'parallel-exchange': 1356, 'parity-cycle': 136, 'other': 120} |
| php | 6 | 30 | 2 | 56 | 32 | 57% | 15.0 | 4.0 | 1.0 | 2 | 2.0 | 72% | {'exchange-cycle': 28, 'parity-cycle': 4} |
| php | 7 | 42 | 2 | 110 | 62 | 56% | 24.0 | 4.0 | 1.0 | 2 | 2.0 | 76% | {'exchange-cycle': 58, 'parity-cycle': 4} |
| php | 8 | 56 | 2 | 187 | 104 | 56% | 29.0 | 4.0 | 1.0 | 2 | 2.0 | 79% | {'exchange-cycle': 100, 'parity-cycle': 4} |
| php | 9 | 72 | 2 | 291 | 160 | 55% | 35.0 | 4.0 | 1.0 | 2 | 2.0 | 81% | {'exchange-cycle': 156, 'parity-cycle': 4} |
| php | 10 | 90 | 2 | 426 | 232 | 54% | 41.0 | 4.0 | 1.0 | 2 | 2.0 | 83% | {'exchange-cycle': 228, 'parity-cycle': 4} |
| php | 11 | 110 | 2 | 596 | 322 | 54% | 47.0 | 4.0 | 1.0 | 2 | 2.0 | 85% | {'exchange-cycle': 318, 'parity-cycle': 4} |
| php | 12 | 132 | 2 | 805 | 432 | 54% | 63.0 | 4.0 | 1.0 | 2 | 2.0 | 86% | {'exchange-cycle': 428, 'parity-cycle': 4} |
| tseitin | 20 | 40 | 4 | 827 | 286 | 35% | 22.5 | 6.0 | 1.0 | 3 | 3.0 | 81% | {'parity-cycle': 228, 'exchange-cycle': 57, 'other': 1} |
| tseitin | 30 | 60 | 5 | 1467 | 580 | 40% | 24.0 | 8.0 | 1.0 | 4 | 3.0 | 90% | {'parity-cycle': 431, 'exchange-cycle': 140, 'other': 9} |
| tseitin | 40 | 80 | 5 | 17500 | 8381 | 48% | 29 | 12 | 2 | 5 | 3.0 | 95% | {'parity-cycle': 7487, 'exchange-cycle': 850, 'other': 38, 'parallel-exchange': 6} |
