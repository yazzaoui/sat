# PR Witness Search for SDCL

Research project: measurement, structure-recovery, and learned-guidance
infrastructure for discovering propagation-redundant (PR) clauses in SAT
solving. Full spec: [pr-witness-search-spec.md](pr-witness-search-spec.md).

## Layout

```
tools/            CaDiCaL, SaDiCaL, dpr-trim (built from source)
generators/       DIMACS generators: php.py <p>, chessboard.py <n>
scripts/          run_bench.py — Phase 0 benchmark harness
benchmarks/
  cnf/            generated instances
  proofs/         SaDiCaL PR proofs (text format, dpr-trim compatible)
  results/        CSV results + run logs
```

## Phase 0 — reproduce the separation (M0)

```sh
# build (macOS/Linux)
cd tools/cadical && ./configure && make
cd tools/sadical && ./configure.sh && make
cd tools/dpr-trim && make

# run
python3 scripts/run_bench.py --family php    --sizes 8 9 10 11 12 13 --timeout 300
python3 scripts/run_bench.py --family mchess --sizes 6 8 10 12 14    --timeout 300
```

The harness generates instances on demand, runs CaDiCaL and SaDiCaL under a
timeout, and verifies every SaDiCaL UNSAT proof with dpr-trim (`s VERIFIED`
required). Expected result: CaDiCaL degrades exponentially and times out on
larger PHP / mutilated-chessboard instances; SaDiCaL solves them quickly with
verified PR proofs.

Notes:
- SaDiCaL is run with `--binary=false` — its binary proof format predates
  dpr-trim's current parser; text proofs verify cleanly.
- SaDiCaL's `--nonroot` decision heuristic defaults to 3 (PHP-style); this
  matters for which families it solves fast (spec §1.2 — the heuristic is
  nearly structureless, which is the gap this project attacks).

## Status

- [x] M0 toolchain built (CaDiCaL 3.0.1, SaDiCaL, dpr-trim)
- [x] Generators validated: PHP, mutilated chessboard, Tseitin (UNSAT + verified proofs)
- [x] M0 separation reproduced — see [docs/m0-separation.md](docs/m0-separation.md)
- [x] Phase 1: SaDiCaL patched with `--eventlog=<path>` JSONL witness logging
      (schema: [docs/event-log-schema.md](docs/event-log-schema.md))
- [x] M1 witness atlas over 3 families — see [docs/witness-atlas.md](docs/witness-atlas.md);
      locality confirmed against a random-set null model (chessboard: true flip
      radius median 2 vs null 13 at n=16, 99–100% of witnesses below null)
- [x] Atlas pattern classification v0 (flip balance × flip-region connectivity):
      PHP ≈ exchange-cycle, Tseitin ≈ parity-cycle, chessboard mixed exchange
- [x] Rejects logged with full attempt features (trail on every attempt) —
      ranker negatives preserved
- [ ] Phase 2: structure recovery + witness templates
