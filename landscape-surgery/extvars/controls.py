#!/usr/bin/env python3
"""Control-arm definition generators for L1.

Arm C — BVA core heuristic (Manthey–Heule–Biere, simplified to its
scoring core): for literal pairs (l1, l2), count matching remainders
R with both (l1 | R) and (l2 | R) present; gain = matches - 2. Select
top-k positive-gain pairs, definitions z <-> l1 | l2. Degeneracy per
the registration: if fewer than k candidates have positive gain, no
padding — return what exists plus the full candidate report
("BVA found nothing to do on PHP(4)" is a data point).

Arm D — random definitions matched to Cook's shape z <-> a | (b & c),
same count and same LAYERING as arm B: layer-t definitions draw their
literals from the same variable pool Cook's layer-t draws from (base
variables for layer 1, base + earlier z for layer t>1). Seeded.
"""
import random


def bva_definitions(n, clauses, k):
    """Returns (defs, new_var_count, report). defs = list of clause
    lists; each definition allocates one new variable."""
    from collections import defaultdict
    by_rem = defaultdict(set)          # frozenset(remainder) -> literals
    for c in clauses:
        cs = frozenset(c)
        for l in c:
            by_rem[cs - {l}].add(l)
    pair_matches = defaultdict(int)
    for rem, lits in by_rem.items():
        lits = sorted(lits)
        for i in range(len(lits)):
            for j in range(i + 1, len(lits)):
                pair_matches[(lits[i], lits[j])] += 1
    scored = sorted(((m - 2, pair) for pair, m in pair_matches.items()
                     if m - 2 > 0), reverse=True)
    report = {"candidates_positive_gain": len(scored),
              "best_gain": scored[0][0] if scored else None,
              "requested": k}
    defs = []
    nv = n
    for gain, (l1, l2) in scored[:k]:
        nv += 1
        z = nv
        defs += [[-z, l1, l2], [z, -l1], [z, -l2]]
    report["selected"] = min(k, len(scored))
    return defs, nv, report


def random_definitions(n, layer_sizes, seed):
    """Arm D: for each layer t with layer_sizes[t] definitions, draw
    z <-> a | (b & c) with a, b, c distinct random literals over the
    pool (base vars + z-vars of earlier layers). Returns (defs, nv)."""
    rng = random.Random(seed)
    defs = []
    nv = n
    pool_top = n
    for count in layer_sizes:
        this_layer_start = nv
        for _ in range(count):
            nv += 1
            z = nv
            vs = rng.sample(range(1, pool_top + 1), 3)
            a, b, c = (v * rng.choice((1, -1)) for v in vs)
            defs += [[z, -a], [z, -b, -c], [-z, a, b], [-z, a, c]]
        pool_top = nv
        del this_layer_start
    return defs, nv
