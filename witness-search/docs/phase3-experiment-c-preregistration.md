# Experiment C (harvest) — pre-registration

Committed before implementation or any run. Protocol as handed over by
the lead; implementation notes adapted to SaDiCaL's actual heuristic
structure are recorded at the bottom BEFORE runs.

## Hypothesis (falsifiable)

Failed reduct solves compute local variable-relevance information that,
transferred to the outer solver's ordering, reduces downstream
conflicts. Null: steering information is solver-local and transfer is
neutral or harmful — extending the A boundary ("not seedable inward")
with "not harvestable outward."

## Arms

- C0 stock — must reproduce frozen baseline conflict counts exactly
  (determinism gate; if C0 drifts, stop — no results valid).
- C1 transfer on FAILED reduct solves only (the money arm — the 84% waste)
- C2 transfer on SUCCESSFUL solves only (control: does the activity
  profile add anything beyond the flip set the bump already gets?)
- C3 both

Transfer: inner solver's top-10 most active reduct variables at solve
end, mapped inner→outer, one standard bump each through the normal bump
path. k=10 and magnitude fixed here, in advance; no tuning sweeps.

Out of scope, structurally: transferring learned clauses (unsound under
the outer formula; the patch must make it impossible, not just avoided).

## Instances

mchess(12,14,16) primary; tseitin(30,40,50) second family; PHP(12)
lossless canary (no-op check, see notes); uf100-01/uf250-01 noise
control. Every UNSAT proof through dpr-trim; any verification failure =
patch leaked into soundness-relevant state = stop-the-line.

## Bars (one run per arm, no fishing)

- Win: C1 ≤ 0.9× stock conflicts on ≥2 of 3 chessboard sizes, wall
  clock ≤ 1.1×.
- Null: 0.9–1.15× across the board.
- Harm (informative): ≥ 1.15× — "activity transfer is anti-steering."
- Secondary (logged regardless): conflicts-per-window after each
  harvest event (local effect that washes out globally?); harvest-event
  count per run (low volume = "underpowered mechanism," distinct from
  null).
- Interpretation clause: C1-null + local-window improvement ⇒ follow-up
  is decay/magnitude as Experiment D with its own registration — not
  tuning inside C.

Report framing, committed now: outcome stated as a boundary sentence.
Win → "steering information transfers outward at zero constraint on
witness choice." Null → "steering is solver-local in both directions;
the two products are inseparable and non-exportable." Harm → "inner
relevance is locally scoped; exporting it misleads the outer ordering."

## Implementation notes (fixed before runs)

1. SaDiCaL has no numeric VSIDS: activity = VMTF queue recency. "Top-10
   most active" := the 10 most recently bumped inner variables (walk
   inner queue from `queue.last` backward), guarded by
   `inner->local.conflicts > 0` — an inner solve with zero conflicts
   bumped nothing, so its queue order is insertion noise, not activity.
   This guard is also the PHP canary mechanism: PHP inner solves are
   propagation-trivial (≈0 conflicts), so C1 must equal C0 exactly.
2. Mapping check (the likeliest silent bug, per protocol): inner
   variables are renamed at reduct construction; the reverse map exists
   — `var(inner, m)->mapped` stores the outer index (verified in
   source, sadical.c map()). The patch must use it, never identity.
3. Outer bump through the normal path only: dequeue + enqueue_last
   (the flip-bump mechanism flagged performance-critical), applied in
   reverse activity order so the most active inner variable ends up
   frontmost in the outer queue. No direct score/state writes.
4. Eventlog `harvest` event emitted whenever eventlog is on (variables,
   outcome, inner conflicts) — log-always, transfer-per-arm.
5. Flag: `--harvest=0|1|2|3` (off/fail/succ/both; numeric because
   SaDiCaL options are numeric). Zero behavior change at 0, verified by
   C0 reproduction.
6. Size expectation: small patch, one session including runs; if it
   grows, stop and report (mapping is probably wrong).
