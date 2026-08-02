# Trajectory study: why template witnesses lose at equal validity

Question (lead-directed, priority over the dynamic proposer): template-first
ordering doesn't change *which* attempts succeed, yet conflicts tripled on
chessboard. Which mechanism carries the damage?

All runs mchess(14), involutions ≤8-cycles, budget 1024 unless noted;
every run dpr-trim VERIFIED. Stock baseline: 280 K conflicts, 1.41 s.

## Ablation of post-accept side channels

| Run | Conflicts | Time | Hit share |
|---|---|---|---|
| template default | 954 K | 8.0 s | 58% |
| flip-bump off on template accepts | **2.38 M** | 23.0 s | 78% |
| balance-restart off | 924 K | 7.8 s | 82% |
| relevant-mode off | 865 K | 7.4 s | 55% |
| all three off | 2.38 M | 22.3 s | 78% |

**The flip-bump is load-bearing guidance, not a poisoned channel** —
removing it doubles the damage. No ablation approaches stock. The naive
"templates poison the bump" hypothesis is dead.

## Witness content is the active ingredient

- Flip sizes in the same run: template accepts median **6**, inner-solver
  (reduct) accepts median **16**.
- Not raw size: largest-first template ordering *worsened* conflicts
  (1.55 M). 
- Interpretation: the inner solver's witness is **informed** — it starts
  from saved phases and works with activities correlated to the outer
  search, so its flip set encodes "which variables matter here now."
  Geometric-minimal template moves carry no such information, and the
  bump then promotes a small arbitrary set.

## Template-as-filter policy (miss ⇒ skip reduct solve)

| Instance | Result |
|---|---|
| php(12), 100% hit share | 0.04 s, conflicts identical to stock (487), verified — **lossless** |
| mchess(14), ~58% hit | **>600 s timeout**; 3.5 M attempts — missed prunes compound exponentially |

Filtering is exactly as good as hit share is complete: perfect at 100%,
catastrophic below it.

## Design conclusions (input to the dynamic proposer)

1. **Witness quality ≠ validity.** The steering value of a witness
   dominates end-to-end performance. Any proposer must be judged on
   downstream conflicts, not acceptance rate. (Refines the pre-registered
   primary metric.)
2. The dynamic alternating-cycle proposer should produce *informed* flips:
   seed and extend cycles using the outer solver's saved phases and
   activity order, mimicking what the inner CDCL would flip.
3. **Most promising synthesis: template ω as inner-solver warm start** —
   assume the template literals and let the inner solver finish. If the
   assumptions hold, the solve is nearly free *and* the witness inherits
   inner-solver quality; if not, normal solve proceeds. Templates then
   accelerate witness search without ever choosing the witness. This
   preserves the 100%-lossless PHP behavior and cannot degrade chessboard
   steering.
4. On families where templates are complete (PHP-like counting), the
   filter policy is free and exact.
