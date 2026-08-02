#!/usr/bin/env python3
"""S5 P0 feasibility measurements (sizes and costs only — no P1
questions touched).

A: candidate-1 clause-database state counts at PHP(3), BFS by depth
   under the canonical quotient (subsumption-reduced antichains).
B: candidate-3 derivability-depth DP: universe sizes, rounds to
   fixpoint, depth-to-bottom, width frontier — PHP(3) full-width,
   PHP(3)+Cook layer, PHP(4) at w=3,4.
"""
import sys
import time
from itertools import combinations

sys.setrecursionlimit(100000)


def php_clauses(p):
    h = p - 1
    var = lambda i, j: (i - 1) * h + j
    cl = [[var(i, j) for j in range(1, h + 1)] for i in range(1, p + 1)]
    for j in range(1, h + 1):
        for i in range(1, p + 1):
            for k in range(i + 1, p + 1):
                cl.append([-var(i, j), -var(k, j)])
    return p * h, cl


def to_pn(cl):
    p = n = 0
    for l in cl:
        if l > 0:
            p |= 1 << (l - 1)
        else:
            n |= 1 << (-l - 1)
    return (p, n)


def subsumes(a, b):          # a ⊆ b as clauses
    return (a[0] & ~b[0]) == 0 and (a[1] & ~b[1]) == 0


def resolve(a, b):
    """All non-tautological resolvents of clauses a, b."""
    out = []
    piv = a[0] & b[1]
    piv2 = a[1] & b[0]
    for src, (x, y) in ((piv, (a, b)), (piv2, (b, a))):
        m = src
        while m:
            v = m & -m
            m ^= v
            rp = (x[0] & ~v) | y[0]
            rn = x[1] | (y[1] & ~v)
            if rp & rn:
                continue
            out.append((rp, rn))
    return out


def reduce_antichain(clauses):
    out = []
    for c in sorted(clauses, key=lambda c: bin(c[0] | c[1]).count("1")):
        if not any(subsumes(d, c) for d in out):
            out.append(c)
    return frozenset(out)


# ---------- A: candidate-1 state BFS ----------
def candidate1_bfs(p, max_depth=3, cap=200000):
    _, cl = php_clauses(p)
    start = reduce_antichain([to_pn(c) for c in cl])
    layer = {start}
    seen = {start}
    counts = [1]
    for d in range(1, max_depth + 1):
        nxt = set()
        t0 = time.time()
        for st in layer:
            lst = list(st)
            for a, b in combinations(lst, 2):
                for r in resolve(a, b):
                    if any(subsumes(c, r) for c in st):
                        continue
                    ns = reduce_antichain(list(st) + [r])
                    if ns not in seen:
                        seen.add(ns)
                        nxt.add(ns)
                        if len(seen) > cap:
                            return counts + [f">cap at depth {d}"], time.time() - t0
        counts.append(len(nxt))
        layer = nxt
    return counts, None


# ---------- B: candidate-3 derivability-depth DP ----------
def depth_dp(n, input_clauses, w=None, extra_axioms=()):
    """Minimal resolution DEPTH per derived clause, subsumption-aware,
    width-bounded. Returns (depth_of_bottom, rounds, |derived|, secs)."""
    t0 = time.time()
    derived = {}                        # antichain: clause -> depth
    def add(c, d):
        drop = []
        for e, de in derived.items():
            if subsumes(e, c) and de <= d:
                return False
            if subsumes(c, e) and d <= de:
                drop.append(e)
        for e in drop:
            del derived[e]
        derived[c] = d
        return True

    for c in input_clauses:
        add(to_pn(c), 0)
    for c in extra_axioms:
        add(to_pn(c), 0)
    frontier = list(derived)
    rounds = 0
    while frontier:
        rounds += 1
        new = []
        items = list(derived.items())
        fr = set(frontier)
        for a, da in items:
            for b, db in items:
                if a >= b or (a not in fr and b not in fr):
                    continue
                for r in resolve(a, b):
                    if w is not None and bin(r[0] | r[1]).count("1") > w:
                        continue
                    d = 1 + max(da, db)
                    if add(r, d):
                        new.append(r)
        frontier = new
        if (0, 0) in derived:
            break
    bot = derived.get((0, 0))
    return bot, rounds, len(derived), round(time.time() - t0, 2)


def cook_layer_axioms(p):
    """One Cook layer at PHP(p): z_ij = x_ij | (x_i,h & x_p,j)."""
    h = p - 1
    var = lambda i, j: (i - 1) * h + j
    nv = p * h
    ax = []
    for i in range(1, p):
        for j in range(1, h):
            nv += 1
            z = nv
            a, b, c = var(i, j), var(i, h), var(p, j)
            ax += [[z, -a], [z, -b, -c], [-z, a, b], [-z, a, c]]
    return nv, ax


def main():
    print("== A: candidate-1 state BFS (PHP(3), quotient = subsumption antichain)")
    counts, _ = candidate1_bfs(3, max_depth=3)
    print("   states by depth:", counts)

    print("== B: candidate-3 depth DP")
    n, cl = php_clauses(3)
    for w in (2, 3, None):
        bot, rounds, nd, secs = depth_dp(n, cl, w)
        print(f"   PHP(3) w={w}: bottom depth={bot} rounds={rounds} "
              f"derived={nd} ({secs}s)")
    nv, ax = cook_layer_axioms(3)
    bot, rounds, nd, secs = depth_dp(nv, cl, None, ax)
    print(f"   PHP(3)+Cook layer (vars={nv}): bottom depth={bot} "
          f"rounds={rounds} derived={nd} ({secs}s)")
    n4, cl4 = php_clauses(4)
    for w in (3, 4):
        bot, rounds, nd, secs = depth_dp(n4, cl4, w)
        print(f"   PHP(4) w={w}: bottom depth={bot} rounds={rounds} "
              f"derived={nd} ({secs}s)")


if __name__ == "__main__":
    main()
