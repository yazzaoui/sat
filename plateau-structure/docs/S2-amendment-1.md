# S2 amendment 1 — S2b made navigational (pre-run, lead-required)

The registered Spearman bar measured association, not navigation; the
frame promised a dynamics claim. S2b is amended to two stages, both
fixed here before any run:

## Stage 1 — screen (bar exactly as registered)

|Spearman(V₂, exact BFS exit distance)| ≥ 0.5 per substrate class,
sign reported, must exceed the mobility control's |ρ|.

## Stage 2 — verdict-bearing: exact hitting-time ratio

For candidates passing the screen (control always computed alongside):

- **Descent direction** is set by the screen's pooled sign per
  (candidate, substrate class) — if ρ > 0 (V₂ high near exits) the
  walker ascends V₂ (descends −V₂). Fixed before the dynamics test,
  never tuned. If per-instance screen signs disagree within a class,
  the candidate FAILS stage 2 for that class (no direction exists to
  fix) — decided now.
- **Walk (refined):** on the V=1 level subgraph; a state adjacent to
  any V=0 state is an EXIT (absorbing, hit at arrival). From a
  non-exit state: if strict V₂-improving level-neighbors exist (in the
  fixed direction), step uniformly among them; otherwise step
  uniformly among ALL level-neighbors (plateau-walk fallback among
  ties, worsening included). Upward (V+1) moves never taken.
- **Walk (blind):** uniform among all level-neighbors; same absorbing
  rule. Identical component structure ⇒ identical unreachable-exit
  exclusion: components with no exit are excluded from both means and
  reported as unreachable mass.
- **Quantity:** exact expected hitting time (linear solve on the
  absorbing chain; largest system 7,200 states — trivial), mean over
  uniform start on all level states (exits contribute 0).
- **Bar:** blind/refined mean hitting-time ratio **≥ 2** per substrate
  class (the lead's proposed margin, adopted; feasibility gives no
  reason to argue it down — the systems are exact, so the bar is pure
  materiality). The structuring candidate's ratio must also exceed
  the control's ratio.

Verdict language: "useful" now means *steers* — S2b passes only if
refined descent provably halves the expected time to an exit.
