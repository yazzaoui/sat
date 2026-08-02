# Phase 2 pre-registered success criteria (chessboard)

Committed BEFORE the guided-chessboard experiments run. Lead-approved bars:

1. **Primary — acceptance rate under template-first ordering.**
   Stock SaDiCaL at mchess(14): 16% of positive-reduct attempts accepted
   (frozen M1 atlas). Success bar: **≥ 60%** template-first acceptance at
   the same size. ≥ 90% = strong result. Stall at ~30% = taxonomy partly
   descriptive; residual goes to reduct fallback and is reported as such.
2. **Secondary — end-to-end.** Guided SDCL beats stock SaDiCaL wall-clock
   at mchess(16–18), against the frozen m1-baseline numbers
   (stock: 7.51 s at n=16, 44.43 s at n=18).
3. **Kill criterion.** If template proposals on chessboard do not beat
   stock acceptance by end of the tuning session, the v0 taxonomy was
   descriptive rather than predictive — reported as a finding, not hidden.

Template set under test (from the atlas distribution — 80% exchange-cycle
with a size-growing parallel-exchange tail):
- 2×2 face-rotation involutions (single exchange-cycle re-tiling),
  enumerated from the block-intersection graph's 4-cycles;
- radius-bounded proposal order: faces touching the deepest decision first
  (justified by the constant-radius-2 atlas result);
- parallel-exchange = reduct fallback in v0 (single faces only); if
  acceptance lands materially below the accept-pattern share (~80%),
  face-pair compositions are the named next lever.

Soundness invariant unchanged: every accepted witness — template or reduct
— flows through the PR machinery and every emitted proof must verify under
dpr-trim. No exceptions.
