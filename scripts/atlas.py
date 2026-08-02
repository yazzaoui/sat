#!/usr/bin/env python3
"""Witness atlas (Phase 1): analyze SaDiCaL witness event logs.

Usage:
  python3 scripts/atlas.py <events.jsonl> <instance.cnf> [--json]

Per accepted witness:
  - footprint: #variables in the witness
  - flipped:   #literals whose polarity omega inverts (the rearrangement core)
  - radius:    max BFS distance in the variable-interaction graph from the
               stuck region (variables of the banned clause) to any flipped
               variable — the locality measure motivating Phases 2/3
  - overlap:   |vars(witness) ∩ vars(banned clause)|

Aggregates distributions and prints the locality report.
"""
import argparse
import json
import random
import statistics
import sys
from collections import deque


def load_cnf(path):
    clauses = []
    for line in open(path):
        line = line.strip()
        if not line or line[0] in "pc%":
            continue
        lits = [int(x) for x in line.split()][:-1]
        if lits:
            clauses.append(lits)
    return clauses


def interaction_graph(clauses):
    adj = {}
    for c in clauses:
        vs = sorted({abs(l) for l in c})
        for i, u in enumerate(vs):
            for v in vs[i + 1:]:
                adj.setdefault(u, set()).add(v)
                adj.setdefault(v, set()).add(u)
    return adj


def dist_from(adj, sources):
    """BFS distance from a source set to every reachable variable."""
    dist = {s: 0 for s in sources}
    q = deque(sources)
    while q:
        u = q.popleft()
        for v in adj.get(u, ()):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def set_radius(dist, targets):
    """Max distance over targets (None if any target unreachable)."""
    try:
        return max(dist[t] for t in targets) if targets else 0
    except KeyError:
        return None


def flip_components(adj, flip_vars):
    """Connected components of the interaction subgraph induced on flipped vars."""
    left = set(flip_vars)
    comps = []
    while left:
        seed = left.pop()
        comp = {seed}
        q = deque([seed])
        while q:
            u = q.popleft()
            for v in adj.get(u, ()):
                if v in left:
                    left.discard(v)
                    comp.add(v)
                    q.append(v)
        comps.append(comp)
    return comps


def classify(flipped_lits, adj):
    """v0 taxonomy of the rearrangement core (spec Phase 1 item 2).

    balanced   = equally many true->false and false->true flips
                 (permutation-like: preserves counts, as in block swaps)
    exchange-cycle     one connected flipped region, balanced
    parallel-exchange  several connected flipped regions, balanced
    parity-cycle       one region, unbalanced (XOR-style: flips along a walk)
    other              several regions, unbalanced
    """
    pos = sum(1 for l in flipped_lits if l > 0)  # was true, omega makes false
    neg = len(flipped_lits) - pos
    comps = flip_components(adj, {abs(l) for l in flipped_lits})
    balanced = pos == neg
    single = len(comps) == 1
    if balanced and single:
        return "exchange-cycle"
    if balanced:
        return "parallel-exchange"
    if single:
        return "parity-cycle"
    return "other"


NULL_SAMPLES = 50


def analyze(events_path, cnf_path, seed=0):
    events = [json.loads(l) for l in open(events_path)]
    adj = interaction_graph(load_cnf(cnf_path))
    all_vars = list(adj)
    rng = random.Random(seed)
    accepts = [e for e in events if e["ev"] == "accept"]
    rows = []
    for e in accepts:
        clause_vars = {abs(l) for l in e["clause"]}
        wit_vars = {abs(l) for l in e["witness"]}
        flip_vars = {abs(l) for l in e["flipped"]}
        dist = dist_from(adj, clause_vars)
        # Null model: radius of random same-size variable sets from the same
        # stuck region — locality only counts if the truth sits well below.
        null_radii = [
            set_radius(dist, rng.sample(all_vars, len(flip_vars)))
            for _ in range(NULL_SAMPLES)
        ]
        null_radii = [r for r in null_radii if r is not None]
        rows.append({
            "id": e["id"],
            "footprint": len(wit_vars),
            "flipped": len(flip_vars),
            "radius": set_radius(dist, flip_vars),
            "null_radius": statistics.median(null_radii) if null_radii else None,
            "overlap": len(wit_vars & clause_vars),
            "clause_size": len(clause_vars),
            "inner_ms": e["inner"]["time_ms"],
            "pattern": classify(e["flipped"], adj),
        })
    n_attempts = sum(1 for e in events if e["ev"] == "attempt")
    return events, rows, n_attempts


def dist_summary(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return "n/a"
    return (f"min={min(vals)} med={statistics.median(vals)} "
            f"mean={statistics.mean(vals):.2f} max={max(vals)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("events")
    ap.add_argument("cnf")
    ap.add_argument("--json", action="store_true",
                    help="emit per-witness rows as JSON instead of the report")
    args = ap.parse_args()

    events, rows, n_attempts = analyze(args.events, args.cnf)
    if args.json:
        json.dump(rows, sys.stdout, indent=1)
        return
    if not rows:
        print("no accepted witnesses in log")
        return
    nvars = events[0].get("vars", "?") if events else "?"
    print(f"instance: {args.cnf} ({nvars} vars)")
    print(f"attempts: {n_attempts}  accepts: {len(rows)} "
          f"({100 * len(rows) / max(n_attempts, 1):.0f}%)")
    print(f"witness footprint (#vars):  {dist_summary([r['footprint'] for r in rows])}")
    print(f"flipped literals:           {dist_summary([r['flipped'] for r in rows])}")
    print(f"radius from stuck region:   {dist_summary([r['radius'] for r in rows])}")
    print(f"null radius (random sets):  {dist_summary([r['null_radius'] for r in rows])}")
    print(f"overlap with banned clause: {dist_summary([r['overlap'] for r in rows])}")
    unreachable = sum(1 for r in rows if r["radius"] is None)
    if unreachable:
        print(f"warning: {unreachable} witnesses with unreachable flipped vars")


if __name__ == "__main__":
    main()
