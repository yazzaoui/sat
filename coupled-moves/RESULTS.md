# S1 coupled-moves results index

| Phase | Question | Document | Verdict |
|---|---|---|---|
| P0 | Which coupled-move variants are provably distinct from baseline geometry? | [P0-formalization](docs/P0-formalization.md) | **Complete, paper-only.** Variants 1 (eager) and 3 (bundled altitude) inert by proof; variant 2 collapses under orig-V and from consistent starts; **survivor: lazy propagation, full-V, stale-inclusive state space** — directed, irreversible, carrying both corridor-opening (accidental repair) and solution-repelling (stale altitude) mechanisms. Canonical attractor definition fixed (terminal SCCs, tie-break-free). Kill criterion did not fire. |
| P1 | Net conductance: do Cook's corridors outweigh their mines, beyond controls? | [P1-registration](docs/P1-registration.md) | **Awkward branch, strongest form ([P1-results](docs/P1-results.md)):** NET identical to machine precision across Cook and all random seeds — an exact counting identity NET = 23·511/2²⁵ (staleness unlocks other solutions' dressings; loss ≡ 0, mines bend paths but sever nothing; BVA fully degenerate). **Definition-generic; H1-successor NOT supported.** Theorem F proven-at-anchor by exhaustive masks. Engine canon deviation caught pre-report and fixed; P0 micro-examples now permanent engine checks. reproduce 7/7. |

**Stream closed by lead.** Ledger sentence recorded in
[../LEDGER.md](../LEDGER.md) (entry 6). Parked successor, weak prior,
own registration required: dynamical refinement — hitting-time
conductance (NET at the reachability level is identical across arms;
whether EXPECTED HITTING TIMES differ per arm is unmeasured).
