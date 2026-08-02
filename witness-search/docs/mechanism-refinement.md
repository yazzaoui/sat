# Mechanism refinement: where the witness intelligence actually lives

Trigger (lead): 2,214 inner conflicts across 6,574 hunts (~0.3/hunt)
means inner solves barely search on chessboard — the post-memset-fresh
gloss ("deep CDCL dynamics") needed a direct check. Run on existing
Experiment C C0 logs; no new solver runs.

## Inner conflicts by hunt outcome

| Instance | Accepts: conflict-bearing | Rejects: conflict-bearing |
|---|---|---|
| mchess12 | 28% (mean 0.43) | 5% (mean 0.11) |
| mchess14 | 40% (mean 0.89) | 11% (mean 0.33) |
| mchess16 | 50% (mean 1.31) | 13% (mean 0.43) |
| tseitin40 | 61% (mean 0.61) | **0%** (mean 0.00) |
| php12 | 86% (mean 0.88) | **0%** (mean 0.00) |

## Reading

1. **Rejects are propagation-only almost everywhere** (exactly 0% on
   tseitin/php; 5–13% on chessboard): UNSAT reducts are decided by unit
   propagation, not search. The 84% "waste" is loading + one propagation
   pass per stuck point — consistent with, and explaining, the
   cost-structure fact in the E registration.
2. **The rare search effort concentrates in the successful hunts**:
   accepts are 4–8× more likely to be conflict-bearing than rejects,
   and the gap widens with instance size (28→50% on chessboard).
   "Search computes the good ones" survives in sharpened form.
3. **The narrative sentence, tightened** (for the paper): the steering
   information is computed by the reduct solve; on tiling instances
   that computation is largely propagation and reduct structure, with
   conflict-driven search appearing precisely when a witness must be
   *found* rather than *read off* — and it is those found witnesses
   that carry the search's contribution.
4. Retroactive sharpening of Experiment C: harvested activity came
   mostly from propagation-only or near-conflict-free solves — the
   activity signal being exported was largely noise, which is exactly
   why exporting it misled the outer ordering.
5. Note for any B-successor (early-abort prediction): rejects already
   cost ~one propagation pass; there is little left for early-abort to
   save beyond what E's clause cache targets. The successor's value
   case narrows accordingly.

Two-products framing after this refinement: unchanged in substance —
the boundary edges failed empirically regardless of where the
intelligence originates — but the second product is more precisely "a
propagation-structured relevance measurement, occasionally refined by
search exactly where refinement pays."
