# S4 P1 results — the compass fails its central cell; the failure has a mechanism

One run per cell; greedy sole selector per registration; all scoring
exact (Theorem G path); per-step accounting logged throughout. Raw:
[P1-results-data.json](P1-results-data.json).

## Rediscovery gate (pure XOR)

- **Anchor: PASSES exactly** — loop path [68, 40, 24, 16, 12]
  reproduces P0's measurement step-for-step; endpoint 12 = the bar.
- Seeds 2–5 (≤ 0.25× identity bar): 0.10 ✓, 0.16 ✓, 0.26 ✗, 0.33 ✗ —
  **2 of 4 fail as registered.** The visible reason (annotated, not
  retrofitted): the in-class endpoint is an ABSOLUTE floor (~10–12
  basins on every XOR instance regardless of starting count 30–124);
  the bar assumed multiplicative scaling. Same genre as S3's row-2
  mis-projection; the bar stands as registered and failed.
- All five beat best-of-10 random compositions — and notably, **random
  elementary compositions NEVER improve on identity anywhere in the
  entire matrix** (rnd_min ≥ identity in all 24 cells): every basin
  reduction observed is selection, none is drift.

## Hidden-XOR — the decision cell: FAILS as registered

Bar: ≤ 0.5× identity on ≥ 4/5 AND beats best random on each.

| seed | path | verdict |
|---|---|---|
| 1 | 128 → 64 | ✓ (0.50×, beats random) |
| 2 | 128 → 64 | ✓ |
| 3 | **256 → 256 (stuck at identity)** | ✗ — no single improving op exists |
| 4 | **64 → 64 (stuck at identity)** | ✗ |
| 5 | 256 → 128 → 64 | ✓ (0.25×) |

3/5 < 4/5: **the constructive claim dies at its central cell, per the
registered language.** The mechanism is identifiable and was
foreshadowed by P0's spike: on chain-encoded parity, merging can be
invisible to any SINGLE elementary op — greedy's one-op horizon finds
no descent direction at all on 2/5 instances (not weak descent:
none). Composite moves would be required to cross, and greedy was the
sole selector by registered discipline — the miss is the verdict.

**Informed ≡ blind on every hidden cell** (identical paths and
endpoints): structure-detection candidates bought nothing — where the
one-op horizon fails, knowing the chains does not help; where it
succeeds, blind search finds the same ops.

## Mixed CNF+XOR (descriptive curve)

Reduction ratios: φ=0.25 → ~0.27×; φ=0.5 → ~0.40×; φ=0.75 → ~0.53×.
Substantial merging everywhere, always beating random — and
reducibility DECREASES as XOR fraction rises (recorded; not
interpreted beyond the curve).

## Pure-CNF control: violated on 3/5, per the registered reading

Bar expected ≥ 0.9× on ≥ 4/5; actual 0.75, 1.00, 0.67, 0.80, 1.00.
Registered reading applies verbatim: a Theorem-H-certified structure
surprise, reported as such, NOT a win — expected basin movement under
basis selection certifies that random 3-CNF is not affine-invariant
(true, and in hindsight unsurprising). Absolute movements are 1–2
basins on counts of 2–10; the certification is real, the effect tiny.

## Accounting (lead-required instrumentation, summarized)

Per-cell: 241–2,401 evaluations, 1.6–85 s exact scoring (hidden cells
costliest: n=20, ~0.16 s/eval). Full per-step curves in the JSON.

## Consequence

P2 was registered to open only on P1 selection success; the decision
cell failed. **P2 does not open.** Stream heads to closure with:
anchor gate passed; seeds bar 2/4 failed (absolute-floor
mis-projection, annotated); decision cell failed 3/5 with the one-op
horizon as identified mechanism; controls behaved (random never
improves; informed never helps); Theorem-H certification on the CNF
control, tiny in absolute terms.

## Candidate ledger sentence (for lead edit)

*Score-guided basis selection rediscovers the in-class Gaussian
optimum on pure XOR exactly and always beats random — but at its
decision cell it fails as registered: on chain-hidden parity, basin
merging is invisible to any single elementary operation on 2 of 5
instances (greedy finds no descent direction at all), informed
candidates buy nothing, and the constructive claim dies at the
one-op horizon that P0's spike foreshadowed; the bijective door is
walkable only where the structure is one step deep.*
