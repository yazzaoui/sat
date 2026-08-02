# Witness event log schema (Phase 1)

One JSONL file per solver run, `--eventlog=<path>`. Every line is one event
object with an `ev` discriminator. The log is the ground truth for the witness
atlas and the Phase 3 training corpus: replayable, diffable (spec §5).

Integer literals use DIMACS convention (sign = polarity). Variable indices are
the *original* DIMACS indices of the outer solver — never inner-solver mapped
indices — so events join directly against the input CNF and its
variable-interaction graph.

## Events

### `run_start` (once, first line)
```json
{"ev":"run_start", "schema":1, "cnf":"php10.cnf", "vars":90, "clauses":415,
 "options":{"filter":true,"nonroot":3,"level":2000}, "argv":["..."]}
```

### `attempt` — prune() entered at a look-ahead stuck point
```json
{"ev":"attempt", "id":17, "conflicts":412, "decisions":530, "level":3,
 "trail_size":45, "decisions_lits":[4,-17,23],
 "reduct":{"considered":415,"filtered":210,"copied":205,"assumed":12}}
```
- `id`: attempt counter, links the paired outcome event.
- `conflicts`/`decisions`: global outer-solver counters — the temporal
  coordinate for replay.
- `decisions_lits`: current decision literals, outermost first. The candidate
  (banned) clause is exactly their negations, so it is not stored separately.
- `trail_size`: outer trail length at the stuck point.
- `trail`: full outer trail snapshot. Carried on *every* attempt so rejected
  attempts have the same context features as accepts — rejects are the
  negative examples for the Phase 3 ranker and dominate event count.

### `accept` — positive reduct satisfiable; PR clause learned
```json
{"ev":"accept", "id":17, "clause":[-4,17,-23],
 "witness":[-4,17,-23,31,-42], "flipped":[4,-31],
 "inner":{"time_ms":1.2,"conflicts":3,"decisions":9},
 "trail":[4,9,-17,...]}
```
- `clause`: the learned PR clause (negated decisions, flipped decision first —
  proof line order, matches `trace_pruned_clause`).
- `witness`: ω as traced to the proof — the inner model mapped back to outer
  literals over the stamped trail.
- `flipped`: trail literals whose polarity ω changes (the "rearrangement" —
  primary object of atlas pattern classification).
- `trail`: full outer trail at the stuck point (assignment snapshot, spec
  Phase 1 item 1). Stored on accepts; see Size discipline.

### `reject` — positive reduct unsatisfiable
```json
{"ev":"reject", "id":17, "inner":{"time_ms":0.4,"conflicts":11,"decisions":20}}
```

### `run_end` (once, last line)
```json
{"ev":"run_end", "result":20, "time_s":3.41, "pruned":812, "reduct_unsat":94,
 "conflicts":1200}
```
A missing `run_end` marks a crashed/killed run — analyzers must tolerate it.

## Size discipline

Full trail snapshots are O(vars) per event and are carried on every
`attempt` (and duplicated on `accept` for self-containedness). Logs are a
few hundred bytes–KB per event; if this ever dominates on huge instances,
compress the log rather than dropping the negatives — rejected attempts are
training data, not noise.

## Invariants (checked by the analysis loader)

1. Every `attempt` has exactly one `accept` or `reject` with the same `id`.
2. `clause` literals = negations of `decisions_lits` (reordered).
3. `flipped ⊆ trail` polarities inverted; `witness` consistent with `trail`
   outside `flipped`.
4. Event `id`s strictly increase; `conflicts` non-decreasing.

## Analysis-layer joins (Phase 1 item 2)

- Variable-interaction graph from `cnf` → witness footprint radius from the
  stuck region (`decisions_lits` variables) via BFS.
- Footprint size = `|witness|`; overlap with banned clause = `|witness ∩ vars(clause)|`.
- Pattern classification operates on `flipped` structured by the recovered
  variable layout (Phase 2 overlay).
