#!/usr/bin/env python3
"""Sampled landscape probes (L0 registration §2.2). All sampling seeded;
every result dict carries (seed, sample counts). Python-first per the
registration; port only if profiling demands.

Probes:
  basin_sample     — R random starts -> plateau-patient descent ->
                     endpoint clustering by plateau identity
  barrier_sample   — noisy-descent first-passage between attractor pairs
                     (the registered corridor ensemble, §3.3)
  autocorrelation  — V autocorrelation length on uniform random walks
  solution_cluster — solution connectivity on satisfiable instances
"""
import random
from collections import deque


def load_cnf(path):
    clauses = []
    n = 0
    for line in open(path):
        t = line.split()
        if not t or t[0] in ("c", "%"):
            continue
        if t[0] == "p":
            n = int(t[2])
            continue
        lits = [int(x) for x in t[:-1]] if t[-1] == "0" else [int(x) for x in t]
        if lits:
            clauses.append(lits)
    return n, clauses


class Landscape:
    """Incremental V evaluation over full assignments."""

    def __init__(self, n, clauses, defs=None):
        self.n = n
        self.clauses = clauses
        self.occ = [[] for _ in range(n + 1)]
        for ci, c in enumerate(clauses):
            for l in c:
                self.occ[abs(l)].append(ci)
        # defs: list of (z_var, fn(assign)->bool) for corridor checks
        self.defs = defs or []

    def init_state(self, assign):
        self.a = assign[:]                     # 1-indexed bools
        self.sat_count = [0] * len(self.clauses)
        self.V = 0
        for ci, c in enumerate(self.clauses):
            s = sum(1 for l in c if self.a[abs(l)] == (l > 0))
            self.sat_count[ci] = s
            if s == 0:
                self.V += 1

    def flip(self, v):
        self.a[v] = not self.a[v]
        for ci in self.occ[v]:
            c = self.clauses[ci]
            s = sum(1 for l in c if self.a[abs(l)] == (l > 0))
            old = self.sat_count[ci]
            self.sat_count[ci] = s
            if old == 0 and s > 0:
                self.V -= 1
            elif old > 0 and s == 0:
                self.V += 1

    def delta(self, v):
        """V change if v were flipped (evaluated, not applied)."""
        d = 0
        self.a[v] = not self.a[v]
        for ci in self.occ[v]:
            c = self.clauses[ci]
            s = sum(1 for l in c if self.a[abs(l)] == (l > 0))
            if self.sat_count[ci] == 0 and s > 0:
                d -= 1
            elif self.sat_count[ci] > 0 and s == 0:
                d += 1
        self.a[v] = not self.a[v]
        return d

    def violates_defs(self):
        return any(self.a[z] != fn(self.a) for z, fn in self.defs)


def _random_assign(n, rng):
    return [False] + [rng.random() < 0.5 for _ in range(n)]


def descend(ls, rng, patience_mult=2):
    """Plateau-patient steepest descent. Returns endpoint assignment."""
    n = ls.n
    patience = patience_mult * n
    stuck = 0
    while True:
        deltas = [(ls.delta(v), v) for v in range(1, n + 1)]
        best = min(deltas)
        if best[0] < 0:
            ls.flip(best[1])
            stuck = 0
        else:
            zeros = [v for d, v in deltas if d == 0]
            if not zeros or stuck >= patience:
                return ls.a[:]
            ls.flip(rng.choice(zeros))
            stuck += 1


def plateau_key(ls, endpoint, cap=10000):
    """Canonical plateau-component identity: BFS over equal-V zero-delta
    moves from the endpoint, capped; key = min assignment reached
    (as a tuple). Cap overflow falls back to (V, frozenset(violated))."""
    ls.init_state(endpoint)
    v0 = ls.V
    start = tuple(endpoint[1:])
    seen = {start}
    best = start
    q = deque([start])
    while q and len(seen) < cap:
        cur = q.popleft()
        ls.init_state([False] + list(cur))
        for var in range(1, ls.n + 1):
            if ls.delta(var) == 0:
                ls.flip(var)
                t = tuple(ls.a[1:])
                if ls.V == v0 and t not in seen:
                    seen.add(t)
                    if t < best:
                        best = t
                    q.append(t)
                ls.flip(var)
    if q:  # cap hit
        viol = frozenset(ci for ci, s in enumerate(ls.sat_count) if s == 0)
        return ("capped", v0, viol)
    return ("plateau", v0, best)


def same_plateau(n, clauses, a, b, rng, tries=20):
    """Connectivity test between two equal-V endpoints: repeatedly walk
    from a toward b using only zero-delta flips, preferring flips that
    reduce Hamming distance; random tie order per try."""
    ls = Landscape(n, clauses)
    for _ in range(tries):
        ls.init_state(a[:])
        for _ in range(4 * n):
            diff = [v for v in range(1, n + 1) if ls.a[v] != b[v]]
            if not diff:
                return True
            rng.shuffle(diff)
            moved = False
            for v in diff:
                if ls.delta(v) == 0:
                    ls.flip(v)
                    moved = True
                    break
            if not moved:
                others = [v for v in range(1, n + 1)
                          if v not in diff and ls.delta(v) == 0]
                if not others:
                    break
                ls.flip(rng.choice(others))
        if not any(ls.a[v] != b[v] for v in range(1, n + 1)):
            return True
    return False


def basin_sample(n, clauses, R=500, seed=1, plateau_cap=20000):
    rng = random.Random(seed)
    ls = Landscape(n, clauses)
    exact_keys = {}          # completed-BFS plateau keys -> count
    capped = []              # endpoints whose plateau BFS hit the cap
    for _ in range(R):
        ls.init_state(_random_assign(n, rng))
        end = descend(ls, rng)
        ls.init_state(end)
        k = plateau_key(ls, end, cap=plateau_cap)
        if k[0] == "capped":
            capped.append((k, end))
        else:
            exact_keys.setdefault(k, 0)
            exact_keys[k] += 1
    # Capped endpoints: group by (V, violated-set), then split groups by
    # pairwise connectivity tests (union-find) — a capped BFS must not
    # silently merge disconnected plateau components (XOR solution
    # spaces are disconnected affine subspaces; this is load-bearing).
    clusters = 0
    groups = {}
    for k, end in capped:
        groups.setdefault(k, []).append(end)
    for k, ends in groups.items():
        reps = []
        for e in ends:
            for r in reps:
                if same_plateau(n, clauses, e, r, rng):
                    break
            else:
                reps.append(e)
        clusters += len(reps)
    all_v = [k[1] for k in exact_keys] + [k[1] for k, _ in capped]
    return {"seed": seed, "R": R,
            "basins_est": len(exact_keys) + clusters,
            "capped_endpoints": len(capped),
            "coverage": sorted(exact_keys.values(), reverse=True)[:10],
            "min_V_seen": min(all_v) if all_v else None,
            "_reps": reps_of(exact_keys, capped, groups)}


def reps_of(exact_keys, capped, groups):
    """One representative endpoint per sampled cluster (internal use:
    attractor list for the barrier ensemble)."""
    reps = {}
    for k, end in capped:
        reps.setdefault(k, end)
    out = list(reps.values())
    # exact-keyed clusters: reconstruct an endpoint from the canonical
    # plateau key (min assignment stored in the key)
    for k in exact_keys:
        if k[0] == "plateau":
            out.append([False] + list(k[2]))
    return out


def barrier_sample(n, clauses, attractors, rng, N=200, eps=0.1,
                   cap_mult=50, defs=None):
    """Registered corridor ensemble: eps-greedy noisy descent from each
    attractor, first passage to any other attractor's plateau. Returns
    per-walk (reached, max_V, violated_defs)."""
    ls = Landscape(n, clauses, defs)
    results = []
    akeys = [plateau_key(Landscape(n, clauses), a) for a in attractors]
    for ai, a in enumerate(attractors):
        for _ in range(N):
            ls.init_state(a[:])
            maxV = ls.V
            corridor = False
            reached = None
            for _ in range(cap_mult * n):
                if rng.random() < eps:
                    ls.flip(rng.randrange(1, n + 1))
                else:
                    deltas = [(ls.delta(v), v) for v in range(1, n + 1)]
                    best = min(deltas)
                    ls.flip(best[1] if best[0] < 0 else
                            rng.choice([v for d, v in deltas if d == 0])
                            if any(d == 0 for d, _ in deltas)
                            else rng.randrange(1, n + 1))
                maxV = max(maxV, ls.V)
                if defs and ls.violates_defs():
                    corridor = True
                if ls.V == min(k[1] for k in akeys):
                    k = plateau_key(Landscape(n, clauses), ls.a)
                    if k in akeys and akeys.index(k) != ai:
                        reached = akeys.index(k)
                        break
            results.append({"from": ai, "reached": reached,
                            "max_V": maxV, "corridor": corridor})
    return results


def autocorrelation(n, clauses, L=10000, seed=1):
    rng = random.Random(seed)
    ls = Landscape(n, clauses)
    ls.init_state(_random_assign(n, rng))
    series = []
    for _ in range(L):
        ls.flip(rng.randrange(1, n + 1))
        series.append(ls.V)
    mean = sum(series) / L
    var = sum((x - mean) ** 2 for x in series) / L
    if var == 0:
        return {"seed": seed, "L": L, "autocorr_len": 0.0}
    # first lag where normalized autocorrelation < 1/e
    import math
    for lag in range(1, L // 2):
        c = sum((series[i] - mean) * (series[i + lag] - mean)
                for i in range(L - lag)) / ((L - lag) * var)
        if c < 1 / math.e:
            return {"seed": seed, "L": L, "autocorr_len": float(lag)}
    return {"seed": seed, "L": L, "autocorr_len": float(L // 2)}


def solution_cluster(n, clauses, R=500, seed=1):
    """On satisfiable instances: sample solutions by restarts, cluster
    by plateau identity at V=0."""
    rng = random.Random(seed)
    ls = Landscape(n, clauses)
    sols = {}
    found = 0
    for _ in range(R):
        ls.init_state(_random_assign(n, rng))
        end = descend(ls, rng)
        ls.init_state(end)
        if ls.V == 0:
            found += 1
            k = plateau_key(ls, end)
            sols.setdefault(k, 0)
            sols[k] += 1
    return {"seed": seed, "R": R, "solutions_found": found,
            "solution_clusters": len(sols)}
