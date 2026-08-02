# L1 amendment 1 — the baseline floor (pre-comparison, lead-directed)

**CLOSURE NOTE (post-approval):** the amendment was approved with all
four clauses, and execution of clause 3 ended the phase: while
formalizing the sibling bars ("fraction of solution pairs connected
below the uniform ridge"), that metric was proven unsatisfiable for
any definitional-extension arm — see
[extension-inertness-theorems.md](extension-inertness-theorems.md).
No sibling bars were registered, no arms were run; the L-series
completed by proof. Clauses 2's control and the sibling soundness gate
were parked unexecuted (nothing speculative finished, per direction).

Committed before any inter-arm comparison. Trigger: pre-run
measurements at the anchor found the registered bars degenerate.
Approval gates all L1 arm runs.

## Measurements triggering this amendment (all committed data)

| Object | Result |
|---|---|
| PHP(4) baseline, exact | **1 basin** (60 min states at V=1: 24 pigeon-unplaced + 36 collision, one connected plateau system), barriers 0; lex artifact: 24 |
| PHP(5) baseline, exact | **1 basin** (360 min states), barriers 0; lex artifact: 120 |
| PHP(6)/PHP(7) baseline, sampled | all 40/40 endpoints at V=1; 9/12 and 11/12 connect to a single representative (one-sided test: failures prove nothing) — **floored** |
| PHP(4)+Cook, search-reality, exact | **115 basins**, barrier mean 2.93 max 4 — fragmentation, the inverted sign |
| PHP(4,4) SAT sibling, exact | min_V=0, **24 solutions = 24 basins** (isolated points; lex agrees 24 — no plateau artifact at V=0), all pairs merge at barrier exactly 1 |
| PHP(5,5) SAT sibling, exact | **120 solutions = 120 basins**, uniform barrier 1 |

A-priori lemma (stated, probe-verified): for functional definitions the
projection view is identical to the baseline landscape; all extension
effects live in the search-reality view and its corridors.

## Clause 1 — floor case

If a cell's baseline (arm A) basin count ≤ k = 3, the registered
comparison bars are N/A for that cell; all arms are reported
*descriptively* (basin counts, barriers where exact, corridor stats),
with no pass/fail language. By the measurements above this applies to
every UNSAT PHP cell at every size.

## Clause 2 — original-V control on the fragmentation

Before any reading of arm B's 1 → 115 fragmentation, recompute arm B's
merge tree at both anchor sizes under **V restricted to original
clauses only** (definition clauses shape the space's dimensionality but
contribute no altitude). Pre-committed readings:

- Fragmentation vanishes under original-V ⇒ **artifact**: the extended
  landscape is rugged in the definition clauses' bookkeeping, not in
  the problem. Report as such.
- Fragmentation persists ⇒ **genuine carving**: Cook's coordinates
  partition the undifferentiated plateau into structured pieces.
  Independent support for that reading exists (a single flat plateau
  gives descent zero gradient information; featurelessness is its own
  pathology; "merging is good" was a hypothesis about rugged
  landscapes, silent on flat ones) — but per Clause 4 it triggers a
  follow-up registration, not a victory condition here.

## Clause 3 — H1's testable form migrates to the SAT siblings

The conditional is now measured: PHP(6,7) baselines stay floored AND
PHP(4,4)/PHP(5,5) escape (24/120 isolated solution basins, uniform
barrier 1). Therefore:

- **L1's primary H1 test = solution-cluster connectivity on the SAT
  siblings** (per the original decision #3 dual reading): do Cook-style
  coordinates connect solution clusters — reduce cluster count in the
  search-reality view / create corridors between solution basins —
  where BVA and random matched definitions do not? The registered bars
  apply with "basin count" read as "solution-cluster count"; the
  isolated-solution baseline (N! clusters, uniform barrier 1) makes
  both the count and corridor-gap measurements maximally crisp.
- The UNSAT PHP instances become a **descriptive appendix**: the first
  characterization of an UNSAT refutation landscape under a canonical
  basin definition (single mixed-kind plateau system; hardness not
  stored in basin count at these sizes).
- Note: Cook's construction is defined for UNSAT PHP(n+1,n); for the
  SAT siblings arm B uses the same definitional shapes over the
  sibling's variables (the construction's coordinates, applied to the
  square grid — exact form fixed in the arm-B sibling generator before
  runs, committed with this amendment's approval).

## Clause 4 — no retrofitted bars

No new pass/fail bars are invented for the fragmentation direction in
this phase. If the carving reading survives its Clause-2 control, it
gets its own registration (hypothesis, bars, kill criteria) as a
separate document. This clause exists because an inverted-sign finding
is exactly where a program starts unconsciously fishing.
