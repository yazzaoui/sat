# Phase 2 vertical slice: counting templates on PHP

Pipeline (fully blind — grid recovered by `structure.py`, never from
generator knowledge):

```
DIMACS ─→ structure.py ─→ counting grid (rows × AMO columns)
       ─→ template_php.py: inversion-ban clauses (¬x[a][l] ∨ ¬x[b][k]),
          witness = 4-literal block swap  (the M1 exchange-cycle pattern)
       ─→ pr_check.py: poly-time PR check per proposal (soundness gate)
       ─→ CaDiCaL on formula + accepted clauses, DRAT tail
       ─→ dpr-trim( original CNF, PR head ++ DRAT tail ) must say VERIFIED
```

## Results (vs frozen m1-baseline, 300 s timeout)

| p | baseline CaDiCaL | template gen | guided solve | proposals accepted | verified |
|---|---|---|---|---|---|
| 10 | 3.2 s | 14.6 s | 0.02 s | 1620/1620 | yes |
| 11 | 56.7 s | 40.5 s | 0.01 s | 2475/2475 | yes |
| 12 | **timeout** | 81.7 s | 0.02 s | 3630/3630 | yes |
| 13 | **timeout** | 326.6 s | 0.02 s | 5148/5148 | yes |

## Reading

- The plumbing works end-to-end: recovered structure → template proposal →
  machine-checked PR clauses → verified refutation of the original formula.
  PHP(8): 181 PR lemmas in core, `s VERIFIED`.
- **Solve time is size-independent (~0.02 s) once templates are in** — the
  inversion bans make the residual formula unit-propagation-trivial.
- Template acceptance is 100% at every size: on PHP the block-swap template
  is not merely descriptive but exactly predictive, as the M1 atlas's 99%
  exchange-cycle uniformity suggested.
- The bottleneck is template *generation*: naive Python PR checker rechecks
  the whole accumulated formula per candidate (O(p⁴) candidates × O(|F|)
  UP). php13 takes 327 s in the proposer against SaDiCaL's 0.06 s in-search
  discovery. This is expected for the slice and irrelevant to the Step 2
  target, which moves proposal into SaDiCaL's candidate loop where the
  atlas-guided ordering is measured by acceptance rate, not by external
  re-derivation cost. Cheap speedups if the external path stays useful:
  incremental UP with watched literals, restrict the PR check to clauses
  touched by omega, C implementation.

## Next (per lead directive)

1. Chessboard templates — the real test: 80% exchange-cycle with a growing
   parallel-exchange tail; templates must cover a distribution. Bounded
   enumeration within radius 2 of the conflict (justified by the atlas's
   constant-radius result).
2. In-solver template-first proposal in SaDiCaL's `prune()`; primary metric
   acceptance rate vs stock (16% → 60%+?), kill criterion as defined.
3. Competition-instance coverage sweep for `structure.py`.
