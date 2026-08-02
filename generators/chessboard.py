#!/usr/bin/env python3
"""Mutilated chessboard(n): n x n board, two opposite corners removed,
tiled by dominoes. UNSAT for even n (removed corners share a color).

One variable per domino placement, i.e. per edge between orthogonally
adjacent surviving cells. Constraints: every surviving cell is covered by
exactly one domino (at-least-one + pairwise at-most-one over its incident
edges).
"""
import sys


def chessboard(n: int) -> str:
    removed = {(0, 0), (n - 1, n - 1)}
    cells = [(r, c) for r in range(n) for c in range(n) if (r, c) not in removed]
    cellset = set(cells)

    edges = {}  # (cell_a, cell_b) sorted -> var index
    incident = {cell: [] for cell in cells}
    for (r, c) in cells:
        for (dr, dc) in ((0, 1), (1, 0)):
            nb = (r + dr, c + dc)
            if nb in cellset:
                v = len(edges) + 1
                edges[((r, c), nb)] = v
                incident[(r, c)].append(v)
                incident[nb].append(v)

    clauses = []
    for cell in cells:
        inc = incident[cell]
        clauses.append(inc[:])  # at least one
        for a in range(len(inc)):
            for b in range(a + 1, len(inc)):
                clauses.append([-inc[a], -inc[b]])  # at most one

    lines = [f"p cnf {len(edges)} {len(clauses)}"]
    lines += [" ".join(map(str, c)) + " 0" for c in clauses]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    n = int(sys.argv[1])
    sys.stdout.write(chessboard(n))
