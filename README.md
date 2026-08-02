# PR / Proof-Search Research Program

Two research workstreams sharing one toolchain and one discipline.

| Workstream | Status | Entry points |
|---|---|---|
| [witness-search](witness-search/) | **Complete** — boundary map closed, clean-clone reproducible (tag `boundary-map-v1`) | [SPEC](witness-search/SPEC.md) · [RESULTS](witness-search/RESULTS.md) · [REPRODUCING](witness-search/REPRODUCING.md) |
| [landscape-surgery](landscape-surgery/) | **Active** — L0 probe bring-up next | [SPEC](landscape-surgery/SPEC.md) · [RESULTS](landscape-surgery/RESULTS.md) |
| [common](common/) | Shared infrastructure | [README](common/README.md) · [DISCIPLINE](common/DISCIPLINE.md) |

## Layout

```
common/            shared infrastructure
  generators/      seeded DIMACS generators (PHP, chessboard, Tseitin)
  tools/           solvers & checker: sadical (patched, tracked),
                   cadical + dpr-trim (external, pinned — see the
                   workstream REPRODUCING docs for commits)
  DISCIPLINE.md    the research protocol both workstreams run under
witness-search/    SDCL witness search (complete)
  SPEC.md          original mandate
  RESULTS.md       verdict index — every claim, one line, one link
  REPRODUCING.md   stranger-runnable reproduction (12 checks)
  docs/            pre-registrations and results
  scripts/         experiment + analysis code
  benchmarks/      results (tracked), frozen M1 snapshot (sha256),
                   instances/proofs (regenerable, ignored)
landscape-surgery/ extension variables as basin-merging coordinates (active)
  SPEC.md          mandate
  RESULTS.md       phase/verdict index (scaffold)
  docs/            registrations land here before any run
  probes/          landscape probe library (L0)
  extvars/         extension-variable toolkit (Cook / BVA / random arms)
```

## Tags

- `m1-baseline` — frozen witness-search M1 dataset.
- `boundary-map-v1` — witness-search complete; pre-reorganization layout.
  (Post-reorganization reproduction re-verified; see RESULTS.md.)
