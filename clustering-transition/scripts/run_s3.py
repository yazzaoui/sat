#!/usr/bin/env python3
"""S3 sweep driver. One run per cell; incremental JSON; chunkable.

Usage: run_s3.py --n 24 --alphas 3.86 4.0 [--seeds 1..10]
Appends cells to docs/S3-results-data.json (keyed n/alpha/seed).
"""
import argparse
import json
import random
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

WS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WS.parent / "plateau-structure/scripts"))
import plateau_tools as T                                # noqa: E402

EXACT = WS.parent / "landscape-surgery/probes/exact"
ALPHAS = (2.0, 3.0, 3.5, 3.86, 4.0, 4.1, 4.2, 4.267)
GAP_CAP_S = 600


def gen(n, alpha, seed):
    rng = random.Random(seed * 1000 + n)
    m = round(alpha * n)
    cl = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), 3)
        cl.append([v * rng.choice((1, -1)) for v in vs])
    return cl


def components(sols, n):
    solset = set(sols)
    comp = {}
    cid = 0
    from collections import deque
    for s in sols:
        if s in comp:
            continue
        comp[s] = cid
        q = deque([s])
        while q:
            u = q.popleft()
            for b in range(n):
                t2 = u ^ (1 << b)
                if t2 in solset and t2 not in comp:
                    comp[t2] = cid
                    q.append(t2)
        cid += 1
    clusters = [[] for _ in range(cid)]
    for s, c in comp.items():
        clusters[c].append(s)
    return clusters


def min_gap(a, b):
    A = np.array(a, dtype=np.uint32)
    B = np.array(b, dtype=np.uint32)
    best = 64
    step = max(1, (1 << 22) // max(len(B), 1))
    for i in range(0, len(A), step):
        x = A[i:i + step, None] ^ B[None, :]
        g = int(np.bitwise_count(x).min())
        if g < best:
            best = g
        if best == 1:
            break
    return best


def cell(n, alpha, seed, work):
    cl = gen(n, alpha, seed)
    Va = T.v_array(n, cl)
    minv = int(Va.min())
    rec = {"n": n, "alpha": alpha, "seed": seed, "min_V": minv}
    if minv > 0:                                   # UNSAT: descriptive
        lvl = [int(s) for s in np.nonzero(Va == minv)[0]]
        rec["unsat_level_size"] = len(lvl)
        rec["unsat_level_components"] = len(components(lvl, n))
        return rec
    sols = [int(s) for s in np.nonzero(Va == 0)[0]]
    clusters = components(sols, n)
    sizes = sorted((len(c) for c in clusters), reverse=True)
    rec["n_solutions"] = len(sols)
    rec["n_clusters"] = len(clusters)
    rec["f_max"] = sizes[0] / len(sols)
    rec["sizes_top"] = sizes[:8]
    big = max(clusters, key=len)
    andm = orm = None
    for s in big:
        andm = s if andm is None else andm & s
        orm = s if orm is None else orm | s
    frozen = bin(andm | (((1 << n) - 1) ^ orm)).count("1")
    rec["frozen_frac_largest"] = frozen / n
    if len(clusters) > 1:
        t0 = time.time()
        gaps = []
        trimmed = False
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                if time.time() - t0 > GAP_CAP_S:
                    trimmed = True
                    break
                gaps.append(min_gap(clusters[i], clusters[j]))
            if trimmed:
                break
        rec["min_gap"] = min(gaps) if gaps else None
        rec["median_gap"] = sorted(gaps)[len(gaps) // 2] if gaps else None
        rec["gap_trimmed"] = trimmed
        # barriers via exact --pairs (reps = min state per cluster)
        cnf = work / f"c{n}_{alpha}_{seed}.cnf"
        with open(cnf, "w") as f:
            f.write(f"p cnf {n} {len(cl)}\n")
            for c in cl:
                f.write(" ".join(map(str, c)) + " 0\n")
        tgt = work / f"c{n}_{alpha}_{seed}.tgt"
        reps = [min(c) for c in clusters]
        tgt.write_text("\n".join(map(str, reps)) + "\n")
        if len(reps) <= 500:
            r = subprocess.run([str(EXACT), "--pairs", str(tgt), str(cnf)],
                               capture_output=True, text=True, check=True)
            lv = {}
            for ln in open(f"{tgt}.out"):
                a, b, v = map(int, ln.split())
                k = (min(a, b), max(a, b))
                lv[k] = min(lv.get(k, 99), v)
            levels = sorted(lv.values())
            rec["barrier_median"] = levels[len(levels) // 2]
            rec["barrier_max"] = max(levels)
            rec["C1"] = sum(1 for v in levels if v <= 1) / len(levels)
            rec["C2"] = sum(1 for v in levels if v <= 2) / len(levels)
        else:
            rec["pairs_trimmed"] = True
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--alphas", type=float, nargs="+", default=list(ALPHAS))
    ap.add_argument("--seeds", type=int, nargs="+",
                    default=list(range(1, 11)))
    args = ap.parse_args()
    out = WS / "docs/S3-results-data.json"
    data = json.loads(out.read_text()) if out.exists() else {"cells": []}
    have = {(c["n"], c["alpha"], c["seed"]) for c in data["cells"]}
    work = Path(tempfile.mkdtemp(prefix="s3-"))
    for alpha in args.alphas:
        for seed in args.seeds:
            if (args.n, alpha, seed) in have:
                continue
            rec = cell(args.n, alpha, seed, work)
            data["cells"].append(rec)
            out.write_text(json.dumps(data, indent=1))
            tag = (f"SAT nc={rec.get('n_clusters')} fmax="
                   f"{rec.get('f_max', 0):.2f} B={rec.get('barrier_median')}"
                   if rec["min_V"] == 0 else
                   f"UNSAT lvl={rec['unsat_level_size']}")
            print(f"n={args.n} a={alpha} s={seed}: {tag}", flush=True)


if __name__ == "__main__":
    main()
