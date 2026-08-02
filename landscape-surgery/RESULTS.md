# Landscape-surgery results index

Status: **complete — closed by proof.** The program's founding
question was answered one level deeper than its experiments: the
extension rule is provably inert-or-fragmenting on assignment
landscapes under 1-flip adjacency; its power must enter through move
structure, not terrain. Successor programs named, not started.

| Phase | Question | Registration | Verdict |
|---|---|---|---|
| L0 | Do the probes see the XOR-SAT smoothing? | [L0-registration](docs/L0-registration.md) | **PASS 100/100 cells**; basin validation ρ=0.98 pooled; barrier estimator failed its gate (restriction inherited) ([L0-results](docs/L0-results.md)) |
| L1 pre-run | (a) What does the UNSAT refutation landscape look like? (b) Baseline floor | [L1-registration](docs/L1-registration.md) + [amendment 1](docs/L1-amendment-1.md) | **Descriptive discovery:** UNSAT PHP = one mixed-kind plateau system at every size measured; prior "ruggedness" at these sizes = descent-partition tie-break artifact (lex 24/120 vs canonical 1/1). Cook cascade fragments 1→115 (mechanism identified). SAT siblings: N! isolated solution basins, uniform ridge 1. |
| L1 arms | H1: do good coordinates connect solution clusters? | held at amendment gate | **Closed by theorem — never run.** Sibling metric proven unsatisfiable for definitional extensions ([extension-inertness-theorems](docs/extension-inertness-theorems.md)): inert in original-V (product theorem), level-0-isolating + ridge-raising in definition-V (sensitivity mechanism, verified against the measured 1→115). |
| L2, L3 | — | — | Not run: predicated on H1 having a testable landscape form; closed with L1. |

Operator split (correcting spec §1.2): the L0-validated merging power
belongs exclusively to bijective re-coordinatization; extensions act
only through coupled flip-and-propagate moves. Successors (new
programs, not amendments): bijective surgery selection (toll stated:
general bijections unfindable, affine findable-but-narrow); the
coupled-move substrate (landscape + propagation as the joint object).
