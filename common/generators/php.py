#!/usr/bin/env python3
"""Pigeonhole principle PHP(p): p pigeons, p-1 holes. Always UNSAT.

Variable x_{i,j} ("pigeon i sits in hole j") has DIMACS index (i-1)*h + j
for i in 1..p, j in 1..h with h = p-1.

Clauses:
  - each pigeon sits somewhere:      (x_{i,1} v ... v x_{i,h})   for each i
  - no two pigeons share a hole:     (-x_{i,j} v -x_{k,j})       for i<k, each j
"""
import sys


def php(p: int) -> str:
    h = p - 1
    var = lambda i, j: (i - 1) * h + j
    clauses = []
    for i in range(1, p + 1):
        clauses.append([var(i, j) for j in range(1, h + 1)])
    for j in range(1, h + 1):
        for i in range(1, p + 1):
            for k in range(i + 1, p + 1):
                clauses.append([-var(i, j), -var(k, j)])
    lines = [f"p cnf {p * h} {len(clauses)}"]
    lines += [" ".join(map(str, c)) + " 0" for c in clauses]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    p = int(sys.argv[1])
    sys.stdout.write(php(p))
