# Research discipline

The protocol both workstreams run under. Everything here was folklore
distributed across the witness-search docs; this file makes it the
contract. New experiments follow it by default; deviations are stated
in the registration, never discovered in the report.

## 1. Pre-registration

- Every experiment gets a registration document in the workstream's
  `docs/`, committed **before** implementation or runs. It states:
  hypothesis (falsifiable), arms, instances, bars (win / null /
  informative-failure), kill criterion, and the interpretation of each
  branch — so no outcome arrives without a committed reading.
- One run per registered arm. No tuning sweeps, no post-null variant
  fishing. If a null suggests a follow-up, it becomes a new
  registration, not an iteration inside the old one.
- Retirement is a decision with a rationale: a registered experiment
  whose outcomes have no consumer must not run; the registration is
  preserved unedited beneath the retirement note.

## 2. Measurement gates

- **Determinism gate:** before any experimental arm, the stock
  configuration must reproduce the frozen baseline conflict counts
  exactly. Drift = stop; nothing is valid until it reproduces.
- **Instrumentation gate:** logging/instrumentation flags must be
  behavior-neutral — determinism gate re-run with the flag on.
- **Validation gate for estimators:** any sampled/approximate probe
  must rank-correlate with exact ground truth where both are
  computable, at a bar registered before use (landscape-surgery §3.1).
  No downstream result may rest on a probe that failed its gate.

## 3. Verification

- Every UNSAT claim ships with a dpr-trim-verified proof
  (`s VERIFIED`). A verification failure after a heuristics-only patch
  means the patch leaked into soundness-relevant state: stop-the-line.
- Soundness exclusions are made **structural** where possible (e.g.
  cross-boundary clause transfer made impossible by construction, not
  avoided by convention).

## 4. Cost honesty

- Decompose every win: a speedup must be attributed to its mechanism
  (the prune-off arm exists so "filtering helped" can't masquerade for
  "the work was skipped").
- Report the tax of any adaptive mechanism alongside its savings
  (probation tax column pattern).
- If scoring/estimation cost can absorb the gain, the registration
  defines the accounting before runs (conservation-law pattern).

## 5. Scope rule

If a component outgrows bounded effort on its planned substrate, stop
and report with a named alternative — never heroic surgery on legacy
code. Termination by pre-build measurement is the cheapest success of
this rule, not a failure.

## 6. Data and provenance

- Baselines are frozen by git tag + sha256-manifested snapshots before
  any dependent phase modifies the system.
- All sampling is seeded; sampled results report seed and sample count;
  variance via seed families, protocol registered at phase start.
- Event logs are ground truth: replayable, diffable, and the analysis
  corpus. Design the schema first.
- Milestones are tagged; reproduction is a runnable script
  (`reproduce.py` pattern) plus a stranger-runnable REPRODUCING doc
  with pinned external commits — re-verified after any repo
  restructuring.

## 7. Reporting

- Outcomes are stated as boundary sentences: every branch of a
  well-registered experiment produces one.
- Corrections are made in-place and in commit history the moment a
  claim decomposes (the flat100 filter correction pattern) — before,
  not after, anyone builds on it.
