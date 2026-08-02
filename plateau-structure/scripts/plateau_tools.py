#!/usr/bin/env python3
"""S2 probe library: level extraction, merge trees over arbitrary
(exact) altitudes on induced subgraphs, exit distances, and exact
absorbing-chain hitting times. Pure Python + numpy; everything exact."""
from fractions import Fraction
from collections import deque

import numpy as np


def v_array(n, clauses):
    V = np.zeros(1 << n, dtype=np.int16)
    for c in clauses:
        mask = base = 0
        for l in c:
            mask |= 1 << (abs(l) - 1)
            if l < 0:
                base |= 1 << (abs(l) - 1)
        free = ((1 << n) - 1) & ~mask
        subs = []
        s = free
        while True:
            subs.append(s)
            if s == 0:
                break
            s = (s - 1) & free
        V[np.array(subs, dtype=np.int64) + base] += 1
    return V


def level_states(n, clauses, level):
    V = v_array(n, clauses)
    return [int(s) for s in np.nonzero(V == level)[0]], V


def sat_lits(s, c):
    return [l for l in c if ((s >> (abs(l) - 1)) & 1) == (l > 0)]


# --- frozen candidate menu (registration §2) ---
def exposure(s, clauses):
    tot = Fraction(0)
    for c in clauses:
        k = len(sat_lits(s, c))
        if k:
            tot += Fraction(1, k)
    return tot


def critical(s, clauses):
    return sum(1 for c in clauses if len(sat_lits(s, c)) == 1)


def decidedness(s, clauses):
    derived = {}
    for c in clauses:
        sl = sat_lits(s, c)
        if len(sl) == 1:
            derived[abs(sl[0])] = sl[0] > 0
    changed = True
    while changed:
        changed = False
        for c in clauses:
            if any(derived.get(abs(l)) == (l > 0) for l in c):
                continue
            un = [l for l in c if abs(l) not in derived]
            if len(un) == 1:
                derived[abs(un[0])] = un[0] > 0
                changed = True
    return len(derived)


def mobility(s, clauses, n, V):
    return sum(1 for b in range(n) if V[s ^ (1 << b)] == V[s])


# --- merge tree over an induced subgraph with exact altitudes ---
def merge_tree_leaves(states, alt, n):
    """states: list of packed ints (one V-level); alt: dict state->
    comparable exact value. Returns (persistent_leaf_count,
    n_components). exact.c's lc-counting scheme, altitudes exact."""
    sset = set(states)
    order = sorted(states, key=lambda s: (alt[s], s))
    parent, birth, lc = {}, {}, {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    n_comp = 0
    for s in order:
        parent[s] = s
        birth[s] = alt[s]
        lc[s] = 1
        for b in range(n):
            t = s ^ (1 << b)
            if t in parent and t in sset:
                r1, r2 = find(s), find(t)
                if r1 == r2:
                    continue
                elder = r1 if birth[r1] <= birth[r2] else r2
                young = r2 if elder is r1 else r1
                merged = (lc[elder] + lc[young] - 1
                          if birth[young] == alt[s]
                          else lc[elder] + lc[young])
                parent[young] = elder
                lc[elder] = merged
    roots = {find(s) for s in states}
    n_comp = len(roots)
    return sum(lc[r] for r in roots), n_comp


# --- S2b machinery ---
def exit_states(states, n, V):
    ex = set()
    for s in states:
        for b in range(n):
            if V[s ^ (1 << b)] < V[s]:
                ex.add(s)
                break
    return ex


def bfs_exit_distance(states, exits, n):
    sset = set(states)
    dist = {s: 0 for s in exits}
    q = deque(exits)
    while q:
        s = q.popleft()
        for b in range(n):
            t = s ^ (1 << b)
            if t in sset and t not in dist:
                dist[t] = dist[s] + 1
                q.append(t)
    return dist          # states absent = unreachable-exit components


def spearman(xs, ys):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    rx, ry = rank(xs), rank(ys)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    return num / (dx * dy) if dx and dy else 0.0


def hitting_time(states, exits, n, step_fn):
    """Exact expected hitting time, uniform start over all level states
    (exits contribute 0). Returns (mean, unreachable_mass, trapped_mass).
    unreachable = no undirected path to an exit (excluded from both
    walks identically). trapped = exit-reachable in the level graph but
    NOT under this walk's directed transitions — hitting time infinite;
    if trapped_mass > 0, mean is float('inf') (the registered bar reads
    uniform-start expectation, which diverges)."""
    reach = bfs_exit_distance(states, exits, n)
    live = [s for s in states if s in reach and s not in exits]
    # directed reverse-reachability from exits under the walk
    preds = {s: [] for s in live}
    for s in live:
        for t in step_fn(s):
            if t in preds:
                preds[t].append(s)
            # edges into exits handled below
    from collections import deque
    walkreach = set()
    q = deque()
    exset = set(exits)
    for s in live:
        if any(t in exset for t in step_fn(s)):
            pass
    # BFS backward: start from states with an edge into an exit
    for s in live:
        if any(t in exset for t in step_fn(s)):
            walkreach.add(s)
            q.append(s)
    while q:
        u = q.popleft()
        for v in preds[u]:
            if v not in walkreach:
                walkreach.add(v)
                q.append(v)
    trapped = [s for s in live if s not in walkreach]
    solve = [s for s in live if s in walkreach]
    idx = {s: i for i, s in enumerate(solve)}
    m = len(solve)
    mean_reaching = 0.0
    if m:
        A = np.zeros((m, m))
        b = np.ones(m)
        for s in solve:
            succs = step_fn(s)
            p = 1.0 / len(succs)
            A[idx[s], idx[s]] = 1.0
            for t in succs:
                if t in idx:
                    A[idx[s], idx[t]] -= p
        E = np.linalg.solve(A, b)
        mean_reaching = float(sum(E))
    covered = len(live) + len(exits)
    unreachable = 1.0 - covered / len(states)
    trapped_mass = len(trapped) / len(states)
    mean = float('inf') if trapped else mean_reaching / covered
    return mean, unreachable, trapped_mass


def make_step(states, n, alt=None, direction=1):
    """Refined lexicographic step (alt None => blind). Returns step_fn."""
    sset = set(states)

    def step(s):
        nbrs = [s ^ (1 << b) for b in range(n) if (s ^ (1 << b)) in sset]
        if alt is not None:
            better = [t for t in nbrs
                      if direction * (alt[t] - alt[s]) < 0]
            if better:
                return better
        return nbrs if nbrs else [s]
    return step
