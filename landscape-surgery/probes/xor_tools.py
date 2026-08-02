#!/usr/bin/env python3
"""XOR-SAT tools (L0): seeded random k-XOR generator, GF(2) Gaussian
elimination, and the affine basis-change operator (§3.3 of the spec,
§2.3 of the L0 registration).

A k-XOR instance is a system over GF(2): for each row, XOR of k
variables = rhs bit. CNF encoding of one row = 2^(k-1) clauses (all
sign patterns with the wrong parity), matching the Tseitin generator's
convention in common/generators.

The basis-change operator returns the instance expressed in the
eliminated coordinates: after full Gauss-Jordan elimination each pivot
row reads y_i = c_i where y_i is an affine form of the original
variables; in y-coordinates the clause set is exactly those unit
constraints (free variables unconstrained). For inconsistent systems
(0 = 1 rows) the transformed set carries an always-violated marker row,
so V in y-coordinates = #violated units + #inconsistent rows — the
registered single-minimum-plateau outcome for UNSAT instances.
"""
import argparse
import itertools
import random
import sys


def gen_xor(n, m, k=3, seed=1):
    rng = random.Random(seed)
    rows = []
    for _ in range(m):
        vs = rng.sample(range(n), k)
        rows.append((sorted(vs), rng.randint(0, 1)))
    return rows


def xor_to_cnf(n, rows):
    clauses = []
    for vs, rhs in rows:
        k = len(vs)
        for signs in itertools.product((1, -1), repeat=k):
            neg = sum(1 for s in signs if s < 0)
            # clause forbids the assignment where all its literals are
            # false; that assignment has ones exactly at negative lits,
            # parity neg — forbidden iff parity != rhs
            if neg % 2 != rhs:
                clauses.append([s * (v + 1) for s, v in zip(signs, vs)])
    return clauses


def eliminate(n, rows):
    """Gauss-Jordan over GF(2). Returns (pivot_rows, inconsistent_count)
    where each pivot row is (mask:int over original vars, rhs) in fully
    reduced form, plus the list of pivot columns."""
    mat = [(sum(1 << v for v in vs), rhs) for vs, rhs in rows]
    pivots = []
    for col in range(n):
        pr = next((i for i, (m, _) in enumerate(mat)
                   if (m >> col) & 1 and i not in [p[0] for p in pivots]), None)
        if pr is None:
            continue
        pm, prhs = mat[pr]
        for i, (m, r) in enumerate(mat):
            if i != pr and (m >> col) & 1:
                mat[i] = (m ^ pm, r ^ prhs)
        pivots.append((pr, col))
    inconsistent = sum(1 for m, r in mat if m == 0 and r == 1)
    pivot_rows = [(mat[pr][0], mat[pr][1], col) for pr, col in pivots]
    return pivot_rows, inconsistent


def eliminated_cnf(n, rows):
    """The instance in eliminated coordinates.

    Convention: new variable y_i is the i-th pivot row's affine form
    XOR its rhs, so every constraint reads y_i = 0 — one unit clause
    (-y_i) per pivot. Free coordinates appear in no clause. Inconsistent
    rows (0 = 1) cannot be expressed as CNF over the new coordinates
    without distorting V, so they are returned as a count: the caller
    treats V_true = V_probe + inconsistent (a known constant offset —
    this is the registered UNSAT-XOR outcome: a single minimum plateau
    at the violated-equation count)."""
    pivot_rows, inconsistent = eliminate(n, rows)
    n_new = len(pivot_rows)
    clauses = [[-(i + 1)] for i in range(n_new)]
    return n_new, clauses, inconsistent


def write_dimacs(path, n, clauses):
    with open(path, "w") as f:
        f.write(f"p cnf {n} {len(clauses)}\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("m", type=int)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--out", required=True, help="original-basis CNF path")
    ap.add_argument("--out-elim", help="eliminated-basis CNF path")
    args = ap.parse_args()
    rows = gen_xor(args.n, args.m, args.k, args.seed)
    write_dimacs(args.out, args.n, xor_to_cnf(args.n, rows))
    info = {"n": args.n, "m": args.m, "seed": args.seed}
    if args.out_elim:
        n_new, clauses, inconsistent = eliminated_cnf(args.n, rows)
        write_dimacs(args.out_elim, max(n_new, 1), clauses)
        info.update({"pivots": n_new, "inconsistent_rows": inconsistent,
                     "satisfiable": inconsistent == 0})
    print(info)


if __name__ == "__main__":
    main()
