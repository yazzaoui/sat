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

## Warm start (implemented: `--tplwarm`)

Template hit ⇒ undo trial writes, inject only the flip literals as inner
units, let the inner solver author the witness. SAT is guaranteed on hits
(the template ω extends the units), so a template can never veto a stock
witness — the lead's completeness check holds by construction. The
pollution check is moot by construction: `clear_inner_solver` deletes and
recreates the inner solver every prune, so no phase/activity state
persists across calls. (Correction to an earlier gloss: the inner
witness's steering value comes from within-solve CDCL dynamics on the
reduct, not from outer phase warming — the inner solver is born fresh.)

| Run | Conflicts | Time | Accepts via |
|---|---|---|---|
| php(12) warm | 487 (= stock) | 0.04 s | 432 warm / 0 reduct — lossless |
| mchess(14) warm | 787 K | 6.1 s | 2582 warm / 1724 reduct |
| mchess(16) warm | 3.1 M | 29 s | 4191 warm / 4577 reduct |

Better than direct templates (954 K) but still ~3× stock: **even a valid
geometric flip core, with the inner solver authoring everything else,
degrades steering.** The inner solver's *free choice of which region to
flip* is the load-bearing intelligence; any geometric constraint on the
core costs ~3× on tilings. Direct, warm, and filter integrations all
confirm this from different angles.

## Where templates DO pay: complete-coverage counting instances

Filter mode on SATLIB competition instances (100% counting coverage on
flat100 graph coloring; structure recovery is blind):

| Instance | stock SaDiCaL | filter mode | CaDiCaL |
|---|---|---|---|
| flat100-1 | 1.16 s | **0.01 s** | 0.01 s |
| flat100-10 | **timeout 120 s** | **0.01 s** | — |
| flat100-43 | 8.75 s | **0.01 s** | — |
| flat100-57 | 1.14 s | **0.02 s** | — |
| flat100-80 | 2.03 s | **0.01 s** | — |

Structure-aware filtering eliminates SDCL's witness-hunt pathology
(spec §1.2) on a real instance class — SaDiCaL becomes CaDiCaL-competitive
where stock loses by 100×–∞. On partial coverage (logistics 38–55%)
filter mode is harmful, consistent with the chessboard result. Rule:
**gate filter mode on detected-coverage completeness.**

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
