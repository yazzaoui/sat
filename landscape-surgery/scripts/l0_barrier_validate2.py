#!/usr/bin/env python3
"""Like-for-like barrier validation (corrects the v1 design error of
comparing sampled attractor-pair barriers against the all-leaf-pair
exact mean — different objects).

For each validation instance: take the sampler's own attractor reps
(deterministic per seed), compute EXACT per-pair merge levels for those
states via a Python persistence sweep, and the sampled per-pair
estimates via the registered first-passage ensemble. Spearman pooled
over pairs within each (n,density) family. Also completes the
interrupted 20/0.9 R=500 basin re-validation.

Instances: n=16 (10 seeds) and n=20 (seeds 1-5), both densities —
Python exact sweep is the cost ceiling.
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent
sys.path.insert(0, str(WS / "probes"))
import probes as P                                     # noqa: E402
import xor_tools as X                                  # noqa: E402
sys.path.insert(0, str(HERE))
from l0_calibrate import spearman, SEEDS               # noqa: E402


def exact_pair_barriers(n, clauses, targets):
    """Persistence sweep over 2^n states; returns {(i,j): merge level}
    for target state indices (targets = list of assignments)."""
    N = 1 << n
    V = [0] * N
    ALL = N - 1
    for c in clauses:
        mask = base = 0
        for l in c:
            v = abs(l) - 1
            mask |= 1 << v
            if l < 0:
                base |= 1 << v
        free = ALL & ~mask
        sub = free
        while True:
            V[base | sub] += 1
            if sub == 0:
                break
            sub = (sub - 1) & free
    order = sorted(range(N), key=lambda s: V[s])
    parent = [-1] * N
    tset = {}
    for i, a in enumerate(targets):
        s = sum(1 << (v - 1) for v in range(1, n + 1) if a[v])
        tset.setdefault(s, []).append(i)
    roots_targets = {}
    out = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for s in order:
        parent[s] = s
        if s in tset:
            roots_targets[s] = set(tset[s])
        v = V[s]
        for b in range(n):
            nb = s ^ (1 << b)
            if parent[nb] == -1:
                continue
            r1, r2 = find(s), find(nb)
            if r1 == r2:
                continue
            t1 = roots_targets.get(r1, set())
            t2 = roots_targets.get(r2, set())
            for i in t1:
                for j in t2:
                    out[tuple(sorted((i, j)))] = v
            parent[r2] = r1
            if t1 or t2:
                roots_targets[r1] = t1 | t2
                roots_targets.pop(r2, None)
    return out


def main():
    data_file = WS / "docs/L0-results-data.json"
    data = json.loads(data_file.read_text())

    fam = {}
    cells = [(16, d, s) for d in (0.7, 0.9) for s in SEEDS] + \
            [(20, d, s) for d in (0.7, 0.9) for s in (1, 2, 3, 4, 5)]
    for n, d, seed in cells:
        rng = random.Random(seed)
        xr = X.gen_xor(n, round(d * n), 3, seed)
        clauses = X.xor_to_cnf(n, xr)
        bs = P.basin_sample(n, clauses, R=200, seed=seed)
        reps = bs["_reps"][:5]
        if len(reps) < 2:
            continue
        exact_pb = exact_pair_barriers(n, clauses, reps)
        walks = P.barrier_sample(n, clauses, reps, rng, N=50)
        best = {}
        for w in walks:
            if w["reached"] is None:
                continue
            key = tuple(sorted((w["from"], w["reached"])))
            best[key] = min(best.get(key, 1 << 30), w["max_V"])
        pairs = [(exact_pb[k], best[k]) for k in best if k in exact_pb]
        fam.setdefault(f"{n}/{d}", []).extend(pairs)
        print(f"{n}/{d} seed {seed}: {len(pairs)} validated pairs", flush=True)

    result = {}
    for k, pairs in fam.items():
        if len(pairs) >= 8:
            result[k] = {"rho": round(spearman(*zip(*pairs)), 3),
                         "pairs": len(pairs)}
        else:
            result[k] = {"rho": None, "pairs": len(pairs)}
    print("per-pair barrier validation:", json.dumps(result))

    reval = []
    for seed in SEEDS:
        xr = X.gen_xor(20, 18, 3, seed)
        clauses = X.xor_to_cnf(20, xr)
        bs = P.basin_sample(20, clauses, R=500, seed=seed)
        r = next(r for r in data["rows"] if r["n"] == 20
                 and r["density"] == 0.9 and r["seed"] == seed)
        reval.append((r["exact_pre"]["basins"], bs["basins_est"]))
        print(f"20/0.9 seed {seed}: exact={reval[-1][0]} R500={reval[-1][1]}",
              flush=True)
    rho500 = round(spearman(*zip(*reval)), 3)
    print(f"20/0.9 basin re-validation at R=500: rho={rho500}")

    data["summary"]["barrier_validation"] = {
        "design": "like-for-like per-pair (v1 all-leaf-mean comparison was "
                  "a category error, disclosed)",
        "family_pair_spearman": result, "bar": 0.8,
        "v1_partial_wrong_object": {"16/0.7": 0.559, "16/0.9": -0.571,
                                    "20/0.7": 0.83}}
    data["summary"]["family_20_09_revalidation"] = {
        "initial_R200_rho": 0.76, "R500_rho": rho500}
    data_file.write_text(json.dumps(data, indent=1))
    print(f"updated {data_file}")


if __name__ == "__main__":
    main()
