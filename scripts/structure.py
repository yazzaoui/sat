#!/usr/bin/env python3
"""Structure recovery (Phase 2 step 1): DIMACS in, typed overlay out.

Detectors, in template-value order:
  1. at-most-one blocks    — cliques in the mutual-exclusion graph built from
                             all-negative binary clauses (pairwise encoding)
  2. exactly-one groups    — an AMO block plus a covering positive clause
                             over exactly the same variables
  3. XOR constraints       — 2^(k-1) clauses over the same k variables, all
                             with the same parity of negated literals
  4. grid adjacency        — the intersection graph of exactly-one blocks is
                             2D-lattice-like (degree <= 4, rich in 4-cycles)

Output: JSON overlay {constructs: [{type, vars, clauses}], coverage,
labels} where `clauses` are 0-based indices into the DIMACS clause list and
`labels` is the blind family classification ("counting", "parity", "grid").

Usage: structure.py <cnf> [--json out.json]
"""
import argparse
import json
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from atlas import load_cnf


def find_amo_cliques(clauses):
    """Maximal cliques (greedy, edge-covering) in the mutual-exclusion graph."""
    excl = defaultdict(set)          # var -> vars mutually excluded with it
    edge_clause = {}                 # (a, b) sorted -> clause index
    for idx, c in enumerate(clauses):
        if len(c) == 2 and c[0] < 0 and c[1] < 0:
            a, b = sorted((-c[0], -c[1]))
            excl[a].add(b)
            excl[b].add(a)
            edge_clause[(a, b)] = idx
    uncovered = set(edge_clause)
    cliques = []
    while uncovered:
        a, b = next(iter(uncovered))
        clique = {a, b}
        # grow among common neighbours, largest exclusion degree first
        cands = excl[a] & excl[b]
        for v in sorted(cands, key=lambda v: -len(excl[v])):
            if all(v in excl[u] for u in clique):
                clique.add(v)
        for e in combinations(sorted(clique), 2):
            uncovered.discard(e)
        idxs = [edge_clause[e] for e in combinations(sorted(clique), 2)]
        cliques.append((clique, idxs))
    return cliques


def find_xors(clauses):
    """Groups of 2^(k-1) same-variable clauses with uniform negation parity."""
    by_vars = defaultdict(list)
    for idx, c in enumerate(clauses):
        vs = frozenset(abs(l) for l in c)
        if len(vs) == len(c) >= 3:
            by_vars[vs].append(idx)
    xors = []
    for vs, idxs in by_vars.items():
        k = len(vs)
        if len(idxs) != 2 ** (k - 1):
            continue
        parities = {sum(1 for l in clauses[i] if l < 0) % 2 for i in idxs}
        if len(parities) == 1:
            xors.append((sorted(vs), idxs, 1 - parities.pop()))
    return xors


def grid_score(xone_blocks):
    """Lattice-likeness of the block intersection graph: (share of blocks
    with degree <= 4, share of edges lying on a 4-cycle)."""
    n = len(xone_blocks)
    if n < 4:
        return 0.0, 0.0
    var_blocks = defaultdict(set)
    for i, (vs, _) in enumerate(xone_blocks):
        for v in vs:
            var_blocks[v].add(i)
    nbr = defaultdict(set)
    for blocks in var_blocks.values():
        for i, j in combinations(sorted(blocks), 2):
            nbr[i].add(j)
            nbr[j].add(i)
    deg_ok = sum(1 for i in range(n) if len(nbr[i]) <= 4) / n
    edges = [(i, j) for i in nbr for j in nbr[i] if i < j]
    if not edges:
        return deg_ok, 0.0
    on_sq = 0
    for i, j in edges:
        # i-j on a 4-cycle: some k in N(j)\{i}, l in N(i)\{j}, k-l adjacent
        if any(k != i and l != j and k in nbr[l]
               for k in nbr[j] for l in nbr[i]):
            on_sq += 1
    return deg_ok, on_sq / len(edges)


def recover(clauses):
    constructs = []
    tagged = set()

    xors = find_xors(clauses)
    for vs, idxs, rhs in xors:
        constructs.append({"type": "xor", "vars": vs, "rhs": rhs,
                           "clauses": idxs})
        tagged.update(idxs)

    pos_clauses = {frozenset(c): i for i, c in enumerate(clauses)
                   if all(l > 0 for l in c)}
    amo_only, xone = [], []
    for clique, idxs in find_amo_cliques(clauses):
        if any(i in tagged for i in idxs):
            continue
        cover = pos_clauses.get(frozenset(clique))
        if cover is not None:
            xone.append((sorted(clique), idxs + [cover]))
        else:
            amo_only.append((sorted(clique), idxs))
    for vs, idxs in xone:
        constructs.append({"type": "exactly-one", "vars": vs, "clauses": idxs})
        tagged.update(idxs)
    for vs, idxs in amo_only:
        constructs.append({"type": "at-most-one", "vars": vs, "clauses": idxs})
        tagged.update(idxs)

    deg_ok, sq = grid_score(xone)

    coverage = len(tagged) / len(clauses) if clauses else 0.0
    counting_cov = sum(len(c["clauses"]) for c in constructs
                      if c["type"] in ("exactly-one", "at-most-one"))
    parity_cov = sum(len(c["clauses"]) for c in constructs
                     if c["type"] == "xor")
    labels = []
    if counting_cov >= 0.5 * len(clauses):
        labels.append("counting")
    if parity_cov >= 0.5 * len(clauses):
        labels.append("parity")
    if xone and deg_ok >= 0.6 and sq >= 0.6:
        labels.append("grid")
    return {
        "constructs": constructs,
        "coverage": round(coverage, 3),
        "grid_score": {"deg_le4": round(deg_ok, 3), "edges_on_square": round(sq, 3)},
        "labels": sorted(labels),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cnf")
    ap.add_argument("--json", help="write full overlay JSON here")
    args = ap.parse_args()
    clauses = load_cnf(args.cnf)
    overlay = recover(clauses)
    if args.json:
        Path(args.json).write_text(json.dumps(overlay, indent=1))
    counts = defaultdict(int)
    for c in overlay["constructs"]:
        counts[c["type"]] += 1
    print(f"{args.cnf}: labels={overlay['labels']} "
          f"coverage={overlay['coverage']:.0%} "
          f"constructs={dict(counts)} grid={overlay['grid_score']}")


if __name__ == "__main__":
    main()
