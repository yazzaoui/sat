#!/usr/bin/env python3
"""Cook's 1976 extension-variable construction for PHP, with DRAT proof
emission (the L1 logic gate: dpr-trim must VERIFY the emitted refutation
against the original PHP formula before arm B is measured as geometry).

Construction, layer n -> n-1 (current matrix cur[i][j], i in [n] pigeons,
j in [n-1] holes):
    z[i][j] := cur[i][j] OR (cur[i][n-1] AND cur[n][j])
for i in [n-1], j in [n-2]. Definition clauses per z (z-first ordering so
each is RAT on its first literal for DRAT):
    (z | -a)  (z | -b | -c)  (-z | a | b)  (-z | a | c)
Derived clauses per layer, each RUP in emission order:
    lemmas   (-z[i][j] | -cur[k][j])   for ordered i != k in [n-1]
    holes    (-z[i][j] | -z[k][j])     for i < k
    pigeons  (z[i][1] | ... | z[i][n-2])
Recurse to n=2, then the empty clause is RUP.

Arm-B landscape formulas take ONLY the definition clauses (spec L1:
"defining clauses only — not the proof"): full cascade at PHP(4),
first layer at PHP(5), per the registered exactness accounting.
"""
import sys
from pathlib import Path


def php_clauses(p):
    h = p - 1
    var = lambda i, j: (i - 1) * h + j
    cl = [[var(i, j) for j in range(1, h + 1)] for i in range(1, p + 1)]
    for j in range(1, h + 1):
        for i in range(1, p + 1):
            for k in range(i + 1, p + 1):
                cl.append([-var(i, j), -var(k, j)])
    return p * h, cl


def cascade(p, layers=None):
    """Returns (n_total_vars, def_clauses, proof_lines, per_layer_vars).

    def_clauses: definition clauses of the first `layers` layers
    (default: full cascade). proof_lines: the FULL refutation (defs of
    all layers + derived lemmas + empty clause), independent of
    `layers` — the logic gate always verifies the complete construction.
    """
    nv, _ = php_clauses(p)
    cur = [[(i - 1) * (p - 1) + j for j in range(1, p)] for i in range(1, p + 1)]
    cur = [[0] * p] + [[0] + row for row in cur]        # 1-index
    next_var = nv
    proof = []
    defs_out = []
    layer_vars = []
    n = p
    layer_idx = 0
    while n >= 3:
        layer_idx += 1
        z = [[0] * (n - 1) for _ in range(n)]           # z[i][j], 1-indexed
        layer_defs = []
        for i in range(1, n):
            for j in range(1, n - 1):
                next_var += 1
                z[i][j] = next_var
                a, b, c = cur[i][j], cur[i][n - 1], cur[n][j]
                layer_defs += [[z[i][j], -a],
                               [z[i][j], -b, -c],
                               [-z[i][j], a, b],
                               [-z[i][j], a, c]]
        proof += layer_defs
        if layers is None or layer_idx <= layers:
            defs_out += layer_defs
            layer_vars.append(next_var)
        for j in range(1, n - 1):                       # lemmas (RUP)
            for i in range(1, n):
                for k in range(1, n):
                    if i != k:
                        proof.append([-z[i][j], -cur[k][j]])
        for j in range(1, n - 1):                       # hole-z (RUP)
            for i in range(1, n):
                for k in range(i + 1, n):
                    proof.append([-z[i][j], -z[k][j]])
        for i in range(1, n):                           # pigeon-z (RUP)
            proof.append([z[i][j] for j in range(1, n - 1)])
        cur = z
        n -= 1
    proof.append([])                                    # empty clause
    return next_var, defs_out, proof, layer_vars


def write_dimacs(path, n, clauses):
    with open(path, "w") as f:
        f.write(f"p cnf {n} {len(clauses)}\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")


def write_proof(path, proof):
    with open(path, "w") as f:
        for c in proof:
            f.write(" ".join(map(str, c)) + " 0\n")


def arm_b_formula(p, layers=None):
    """Original PHP(p) + definition clauses (first `layers`, default all)."""
    nv, cl = php_clauses(p)
    n_total, defs, _, _ = cascade(p, layers)
    if layers is None:
        return n_total, cl + defs
    # n_total counts all cascade vars; restrict to emitted layers
    max_var = max((abs(l) for c in defs for l in c), default=nv)
    return max_var, cl + defs


if __name__ == "__main__":
    p = int(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".")
    nv, cl = php_clauses(p)
    write_dimacs(out / f"php{p}.cnf", nv, cl)
    _, _, proof, _ = cascade(p)
    write_proof(out / f"php{p}.cook.drat", proof)
    print(f"php{p}: {nv} base vars, proof {len(proof)} lines")
