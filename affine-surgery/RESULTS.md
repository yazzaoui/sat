# S4 affine-surgery results index

| Phase | Question | Document | Verdict |
|---|---|---|---|
| P0 | Operator class, representation toll, anchor walkability | [P0-formalization](docs/P0-formalization.md) | **Complete.** Thm G: measurement needs no re-encoding (score = move-basis selection on unchanged V). Thm H: flat-in-expectation for structureless V — control sharpened. **Operator-split correction:** Gaussian elimination = column ops (in-class, bijection) + row ops (constraint reformulation, out of class); in-class anchor optimum ≈ 12, not 1. Canonical composition non-monotone (68→104 spike); greedy monotone 68→40→24→16→12. Kill criterion does not fire. |
| P1 | Selection loop | [P1-registration](docs/P1-registration.md) → [P1-results](docs/P1-results.md) | **Decision cell FAILS as registered** (hidden-XOR 3/5 < 4/5; two instances stuck at identity — no single improving op exists; the one-op horizon P0's spike foreshadowed). Anchor gate PASSES exactly (loop = P0 path); seeds bar 2/4 fail via absolute-floor mis-projection (annotated); random compositions NEVER improve anywhere (selection is real); informed ≡ blind; CNF control violated 3/5 = Theorem-H certification, tiny absolute. |
| P2 | Solver effect under conservation-law accounting | — | **Does not open** (registered condition: P1 selection success). |

**Stream closed by lead.** Ledger sentence recorded verbatim in [../LEDGER.md](../LEDGER.md) (entry 9). Parked (weak prior, own registration required if ever pursued): the composite-op horizon question — selectors that can cross score-worse intermediate terrain.
