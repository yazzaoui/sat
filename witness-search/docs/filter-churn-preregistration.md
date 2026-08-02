# Filter-verdict churn instrumentation — pre-registration

Committed before the instrumentation runs. Scope: **instrumentation
only; the mechanism is held.** (Lead directive, verbatim intent.)

## Question

What fraction of filter verdicts change per consecutive-hunt trail
delta (3–8 literals)? Filter verdicts are the trail-global 55% of hunt
cost (E termination); delta-stable filtering is only conceivable if
verdicts are empirically near-stable.

## Why this successor is categorically more dangerous than E

Approximate filtering changes the reduct, and per the mechanism
refinement the reduct's structure is where much of the second product
(the relevance measurement) is computed. E risked de-freshening the
computation; delta-stable filtering risks handing it a **different
problem**. Hence, stated now, before the number exists:

## Decision gate (pre-committed)

- **Churn > 10–15% per delta → the mechanism is dead on arrival.** No
  hunting for a clever incremental-UP data structure to force it — that
  path is watched-literal surgery on a 2018 codebase, the exact
  heroic-surgery territory the scope rule exists to prevent. The map
  gains its final edge ("filter verdicts are trail-sensitive at rate X;
  approximate filtering is structurally unsafe") and the arc closes.
- **Churn low → register the mechanism** with fidelity bar PRIMARY:
  reduct identity or provably-equivalent verdicts; steering within the
  E-style noise band ([0.95×, 1.05×] stock conflicts) as the tripwire.

## Instrumentation (light, log-only)

- `--logfilter` option: for each hunt, the attempt event additionally
  records the filter-checked clause ids (`c->added`, the stable unique
  id) and the filtered subset. Volume is small (mid-run: ~50 checked,
  ~18 filtered per hunt).
- Zero behavior change with the flag off; determinism gate re-run with
  flag ON must also reproduce frozen conflict counts (logging must not
  perturb).

## Analysis (offline, from logs)

- Per consecutive attempt pair (lags 1, 2, 5): churn = fraction of
  clauses present in both checked domains whose verdict differs;
  also the domain-membership churn itself (a clause entering/leaving
  the checked domain is a verdict change for delta purposes).
- Instances: mchess(12,14), tseitin(40). Report per-family; the gate
  applies to the primary family (chessboard).
