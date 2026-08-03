# S5 proof-space results index

**Stream closed** (Ending 1, negative form — [LEDGER.md entry 10](../LEDGER.md)).

| Phase | Question | Document | Verdict |
|---|---|---|---|
| P0 | Which candidate geometry survives with one canonical definition? | [P0-formalization](docs/P0-formalization.md) | **Complete.** C1 disqualified (Theorem I altitude degeneracy + measured ×8/level state explosion at PHP(3)); C2 disqualified (rewrite completeness unproven — the registered criterion); **C3 selected: the derivability-wavefront space** (canonical altitude = subsumption-aware minimal derivation depth; wavefronts, geodesic DAG of ⊥, width frontier; BW landmarks native). No-ending fence did not fire. |
| P1 | Does any registered observable separate T_Cook from T₀? (distinguishability gate, mandatory before main runs) | [P1-registration](docs/P1-registration.md) · [P1-gate-result](docs/P1-gate-result.md) | **Closed at the gate.** PHP(4): Q1 depth separation ≤ 12.5% < 20%; Q2 geodesic wrong-sign (1.9× / 3.1× LARGER with Cook's definitions); Q3 fronts wider at every level. PHP(5): T₀ baseline complete (w=3 frontier closes — the BW landmark; w=4 depth 13, geodesic 8,296); T_Cook w=3 also closes (antichain 1,181 vs 45 — the banked width-relief claim fails measurement, see gate-result annotation); T_Cook w=4 measured infeasible (antichain 179k by round 6 of ≤ 13, quadratic rounds — checkpoint state in `data/`, resumable). **No registered observable separates ER from resolution at exactly measurable scales.** Sixth finite-size inversion. Main phase (2⁸ lattice, controls, walks) correctly never built. |

Every number: `python3 scripts/reproduce.py` (13 fast checks, ~2 min)
and `--slow` (+2 checks, ~16 min: the PHP(5) w=4 baseline and the
decision-cell growth measurement). Probe: `cc -O3 -o probes/depthdp
probes/depthdp.c`.

Ledger sentence: entry 10, recorded verbatim with one post-recording
measurement annotation (width-relief clause contradicted; lead
emendation pending).
