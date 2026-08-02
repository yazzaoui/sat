#!/usr/bin/env python3
"""Tseitin formula on a random 4-regular graph with n vertices. UNSAT.

One variable per edge. Per vertex v a parity constraint: XOR of incident
edge vars = charge(v), with total charge odd (vertex 0 charged 1, rest 0),
so the formula is unsatisfiable. Each degree-4 vertex contributes the 8
clauses ruling out assignments of wrong parity.

Graph: configuration model, resampled until simple; deterministic via seed
(default 1) so instances are reproducible.

Usage: tseitin.py <n> [seed]
"""
import itertools
import random
import sys


def random_regular(n, d, rng):
    while True:
        stubs = [v for v in range(n) for _ in range(d)]
        rng.shuffle(stubs)
        edges = set()
        ok = True
        for a, b in zip(stubs[::2], stubs[1::2]):
            if a == b or (min(a, b), max(a, b)) in edges:
                ok = False
                break
            edges.add((min(a, b), max(a, b)))
        if ok:
            return sorted(edges)


def tseitin(n, seed=1, d=4):
    if (n * d) % 2:
        raise SystemExit("n*d must be even")
    rng = random.Random(seed)
    edges = random_regular(n, d, rng)
    evar = {e: i + 1 for i, e in enumerate(edges)}
    incident = {v: [] for v in range(n)}
    for e in edges:
        incident[e[0]].append(evar[e])
        incident[e[1]].append(evar[e])

    clauses = []
    for v in range(n):
        charge = 1 if v == 0 else 0
        inc = incident[v]
        # forbid every assignment whose parity != charge
        for signs in itertools.product((1, -1), repeat=len(inc)):
            ones = sum(1 for s in signs if s > 0)
            if ones % 2 != charge:
                clauses.append([-s * x for s, x in zip(signs, inc)])
    lines = [f"p cnf {len(edges)} {len(clauses)}"]
    lines += [" ".join(map(str, c)) + " 0" for c in clauses]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    n = int(sys.argv[1])
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    sys.stdout.write(tseitin(n, seed))
