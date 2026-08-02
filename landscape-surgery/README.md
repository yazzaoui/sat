# Landscape surgery — complete (closed by proof)

Extension variables as basin-merging coordinates: can the coordinates
that make Extended Resolution exponentially stronger be *selected* by a
measurable geometric criterion?

**Answer: no — by theorem, one level deeper than the experiments.**
Functional extensions are provably inert-or-fragmenting on assignment
landscapes under 1-flip adjacency; the merging power the instruments
validated belongs exclusively to bijective re-coordinatization, and
ER's power must enter through coupled flip-and-propagate moves, not
terrain. See [RESULTS.md](RESULTS.md) and
[the theorems](docs/extension-inertness-theorems.md). Bonus
descriptive discovery: the UNSAT PHP refutation landscape is one
undifferentiated plateau system — prior "ruggedness" at these sizes
was a descent-partition tie-break artifact.

- **Mandate:** [SPEC.md](SPEC.md)
- **Phase status and verdicts:** [RESULTS.md](RESULTS.md)
- **Protocol:** [../common/DISCIPLINE.md](../common/DISCIPLINE.md) —
  pre-registration before runs, validation gates for every sampled
  probe, kill criteria per phase, seeded sampling, scope rule.

## Layout

- `docs/` — registrations land here before any run (L0 first: probe
  bring-up + the XOR-SAT calibration gate)
- `probes/` — landscape probe library (exact small-n + sampled
  estimators; solver-independent)
- `extvars/` — extension-variable toolkit (Cook-construction generator,
  BVA baseline, matched-shape random definitions, GF(2) basis change)

## Inherited from witness-search (do not rebuild)

- Seeded generators: `../common/generators/` (PHP, chessboard, Tseitin)
- Verification: `../common/tools/dpr-trim` for any UNSAT proof claim
- Solvers: CaDiCaL (`../common/tools/cadical`) for L3; the patched
  SaDiCaL is available but not assumed
- Discipline artifacts: freeze/tag protocol, reproduction-suite
  pattern, registration format (see `../witness-search/docs/` for
  worked examples)

## Phase sequence (from SPEC, each with kill/branch criteria)

L0 probes+calibration → L1 core H1 measurement (PHP, 4 arms) →
L2 family generalization → L3 intervention (H2) → L4 exploratory
(unregistered until L3 resolves).
