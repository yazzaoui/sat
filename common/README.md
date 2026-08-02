# Common infrastructure

Shared by all workstreams.

## generators/

Seeded DIMACS generators — deterministic, instances are regenerable
and therefore never committed:
- `php.py <p>` — pigeonhole PHP(p), p pigeons / p−1 holes, UNSAT
- `chessboard.py <n>` — mutilated chessboard tiling, UNSAT for even n
- `tseitin.py <n> [seed]` — Tseitin on random 4-regular graph, odd
  charge, UNSAT (seed default 1)

## tools/

- `sadical/` — **tracked in-repo**: SaDiCaL patched by the
  witness-search program. All experimental machinery is flag-gated and
  default-off (`--eventlog`, `--template`, `--tplfilter` + gate v3
  options, `--seed`, `--harvest`, `--logfilter`, `--persist`-era
  options); stock invocations reproduce the frozen baselines exactly
  (enforced by `witness-search/scripts/reproduce.py`).
- `cadical/`, `dpr-trim/` — **external, git-ignored**; fetch at the
  pinned commits (see `witness-search/REPRODUCING.md`):
  cadical `c60730422e758ef1cebe7aeddf2dda31c996bf04`,
  dpr-trim `2dff40530dbc6ac78e52bfe917f872cb16780418`.

Build all three:
```sh
( cd tools/cadical && ./configure && make )
( cd tools/sadical && ./configure.sh && make )
( cd tools/dpr-trim && make )
```

## DISCIPLINE.md

The research protocol: pre-registration, determinism and validation
gates, verification requirements, cost honesty, scope rule, freezing
and reproduction. Both workstreams run under it.

## Change policy

Anything here is load-bearing for reproduction suites. Behavioral
changes to `sadical` must keep stock behavior byte-identical (the
determinism checks in reproduce.py are the tripwire); generator changes
require regenerating any dependent frozen expectations — prefer new
files over edits.
