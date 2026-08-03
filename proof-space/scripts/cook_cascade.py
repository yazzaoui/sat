"""Cook's extension cascade for PHP(p) — the ER definition set used in
the S5 P1 distinguishability gate (docs/P1-registration.md).

Cook's inductive step: with x_{i,j} = "pigeon i in hole j" over an
n-pigeon instance, define z_{i,j} = x_{i,j} OR (x_{i,n-1} AND x_{n,j}),
mapping PHP(n) to PHP(n-1) over the z's. Each definition is four
width-<=3 clauses; layers cascade until 2 pigeons remain. Layer
variables are reassigned two-phase (newcur), so within-layer
definitions all read the previous layer — the bug the one-phase
version had is documented in the session record.

CLI: python3 cook_cascade.py <p> <out.cnf> [--t0]
  writes PHP(p) axioms (+ cascade definitions unless --t0) as DIMACS.
"""

import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p0_feasibility import php_clauses


def cook_cascade_axioms(p):
    h = p - 1
    var = lambda i, j: (i - 1) * h + j
    nv = p * h
    ax = []
    cur = {(i, j): var(i, j) for i in range(1, p + 1) for j in range(1, h + 1)}
    n_now = p
    while n_now >= 3:
        newcur = {}
        for i in range(1, n_now):
            for j in range(1, n_now - 1):
                nv += 1
                z = nv
                a, b, c = cur[(i, j)], cur[(i, n_now - 1)], cur[(n_now, j)]
                ax += [[z, -a], [z, -b, -c], [-z, a, b], [-z, a, c]]
                newcur[(i, j)] = z
        cur = newcur
        n_now -= 1
    return nv, ax


def write_dimacs(path, nv, clauses):
    with open(path, "w") as f:
        f.write("p cnf %d %d\n" % (nv, len(clauses)))
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    p, out = int(args[0]), args[1]
    _, base = php_clauses(p)
    if "--t0" in sys.argv:
        write_dimacs(out, p * (p - 1), base)
    else:
        nv, ax = cook_cascade_axioms(p)
        write_dimacs(out, nv, base + ax)
