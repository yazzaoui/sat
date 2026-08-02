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


def emit_involutions(clauses, overlay, path):
    """Write witness-template involutions derived from detected structure.

    Format: whitespace integers; each involution = variable pairs
    terminated by 0. Pair (u,u) = flip u; (u,v) = swap values of u and v.
      counting -> row-pair block swaps
      grid     -> 2x2 face rotations (both pairings per face)
      parity   -> XOR-cycle flips (3- and 4-cycles of constraints)
    """
    invs = []
    blocks = [c["vars"] for c in overlay["constructs"]
              if c["type"] in ("exactly-one", "at-most-one")]

    # Counting: rows = positive covering clauses over the column blocks.
    col_of = {}
    for j, col in enumerate(blocks):
        for v in col:
            col_of[v] = j
    rows = []
    for c in clauses:
        if all(l > 0 for l in c) and all(v in col_of for v in c):
            rows.append({col_of[v]: v for v in c})
    for a in range(len(rows)):
        for b in range(a + 1, len(rows)):
            shared = sorted(set(rows[a]) & set(rows[b]))
            if len(shared) >= 2:
                invs.append([(rows[a][j], rows[b][j]) for j in shared])

    # Grid: faces = 4-cycles in the block intersection graph.
    shared_var = {}
    nbr = defaultdict(set)
    for i in range(len(blocks)):
        for j in range(i + 1, len(blocks)):
            s = set(blocks[i]) & set(blocks[j])
            if len(s) == 1:
                shared_var[(i, j)] = shared_var[(j, i)] = s.pop()
                nbr[i].add(j)
                nbr[j].add(i)
    # Re-tiling moves = alternating rotations along simple cycles of blocks
    # (cells). Length 4 = 2x2 face, 6 = 2x3, 8 = 2x4 / 3x3 / L; the atlas
    # flip-size distribution (median ~10 at n=14) says the tail matters.
    seen = set()

    def cycles_from(start, max_len):
        stack = [(start, [start])]
        while stack:
            u, path = stack.pop()
            for w in nbr[u]:
                if w == start and len(path) >= 4:
                    key = frozenset(path)
                    if len(key) == len(path) and key not in seen:
                        seen.add(key)
                        yield list(path)
                elif (w > start and w not in path and len(path) < max_len):
                    stack.append((w, path + [w]))

    for start in sorted(nbr):
        for cyc in cycles_from(start, 8):
            edges = [shared_var[(cyc[t], cyc[(t + 1) % len(cyc)])]
                     for t in range(len(cyc))]
            k = len(edges)
            invs.append([(edges[t], edges[(t + 1) % k])
                         for t in range(0, k, 2)])
            invs.append([(edges[t], edges[(t + 1) % k])
                         for t in range(1, k, 2)])

    # Parity: cycles of XOR constraints; flip every shared variable.
    xors = [c["vars"] for c in overlay["constructs"] if c["type"] == "xor"]
    xshare = {}
    xnbr = defaultdict(set)
    for i in range(len(xors)):
        for j in range(i + 1, len(xors)):
            s = set(xors[i]) & set(xors[j])
            if len(s) == 1:
                xshare[(i, j)] = xshare[(j, i)] = s.pop()
                xnbr[i].add(j)
                xnbr[j].add(i)
    xseen = set()
    for i in xnbr:
        for j in xnbr[i]:
            for k in xnbr[j]:
                if k == i:
                    continue
                if i in xnbr[k]:                       # triangle
                    key = frozenset((i, j, k))
                    if len(key) == 3 and key not in xseen:
                        xseen.add(key)
                        vs = [xshare[(i, j)], xshare[(j, k)], xshare[(k, i)]]
                        invs.append([(v, v) for v in vs])
                for l in xnbr[k] & xnbr[i]:            # square
                    if l in (i, j, k):
                        continue
                    key = frozenset((i, j, k, l))
                    if len(key) == 4 and key not in xseen:
                        xseen.add(key)
                        vs = [xshare[(i, j)], xshare[(j, k)],
                              xshare[(k, l)], xshare[(l, i)]]
                        invs.append([(v, v) for v in vs])

    with open(path, "w") as f:
        for inv in invs:
            f.write(" ".join(f"{u} {v}" for u, v in inv) + " 0\n")
    return len(invs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cnf")
    ap.add_argument("--json", help="write full overlay JSON here")
    ap.add_argument("--involutions", help="write witness-template involutions here")
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
    if args.involutions:
        n = emit_involutions(clauses, overlay, args.involutions)
        print(f"wrote {n} involutions to {args.involutions}")


if __name__ == "__main__":
    main()
