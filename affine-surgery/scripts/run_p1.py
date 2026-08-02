#!/usr/bin/env python3
"""S4 P1: greedy basis-selection loop with per-step accounting."""
import functools
import json
import random
import subprocess
import sys
import tempfile
import time
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WS.parent / "landscape-surgery/probes"))
sys.path.insert(0, str(WS.parent / "witness-search/scripts"))
import xor_tools as X                                    # noqa: E402
from structure import find_xors                          # noqa: E402

EXACT = WS.parent / "landscape-surgery/probes/exact"


def matmul(A, B, n):
    return [functools.reduce(lambda x, y: x ^ y,
            (B[j] for j in range(n) if (A[i] >> j) & 1), 0)
            for i in range(n)]


def col_masks(A, n):
    return [sum(((A[r] >> c) & 1) << r for r in range(n)) for c in range(n)]


class Scorer:
    def __init__(self, cnf, n, work):
        self.cnf, self.n, self.work = cnf, n, work
        self.evals = 0
        self.eval_time = 0.0

    def basins(self, cols):
        bf = self.work / f"b{self.evals}.txt"
        bf.write_text("\n".join(map(str, cols)) + "\n")
        t0 = time.time()
        r = subprocess.run([str(EXACT), "--basis", str(bf), str(self.cnf)],
                           capture_output=True, text=True, check=True)
        self.eval_time += time.time() - t0
        self.evals += 1
        return json.loads(r.stdout)["basins"]


def greedy(cnf, n, work, cand_pairs=None, max_steps=25):
    I = [1 << v for v in range(n)]
    pairs = cand_pairs or [(i, j) for i in range(n) for j in range(n) if i != j]
    sc = Scorer(cnf, n, work)
    Ainv = I[:]
    cur = sc.basins(col_masks(Ainv, n))
    path = [cur]
    steps = []
    for step in range(max_steps):
        t0 = time.time()
        e0 = sc.evals
        best = None
        for (i, j) in pairs:
            E = I[:]
            E[i] = (1 << i) | (1 << j)
            cand = matmul(E, Ainv, n)
            b = sc.basins(col_masks(cand, n))
            if best is None or b < best[0]:
                best = (b, cand)
        steps.append({"step": step, "evals": sc.evals - e0,
                      "wall_s": round(time.time() - t0, 2), "best": best[0]})
        if best[0] >= cur:
            break
        Ainv = best[1]
        cur = best[0]
        path.append(cur)
    return {"path": path, "endpoint": cur, "identity": path[0],
            "steps": steps, "total_evals": sc.evals,
            "total_eval_time_s": round(sc.eval_time, 2)}


def random_controls(cnf, n, work, length, n_seq=10, seed=99):
    rng = random.Random(seed)
    I = [1 << v for v in range(n)]
    sc = Scorer(cnf, n, work)
    ends = []
    for _ in range(n_seq):
        Ainv = I[:]
        for _ in range(max(length, 1)):
            i, j = rng.sample(range(n), 2)
            E = I[:]
            E[i] = (1 << i) | (1 << j)
            Ainv = matmul(E, Ainv, n)
        ends.append(sc.basins(col_masks(Ainv, n)))
    return ends


def informed_pairs(clauses, n):
    xors = find_xors(clauses)
    pairs = set()
    for vs, _, _ in xors:
        for a in vs:
            for b in vs:
                if a != b:
                    pairs.add((a - 1, b - 1))
    return sorted(pairs)


# ---------- instance generators ----------
def pure_xor(seed, n=16, m=14):
    rows = X.gen_xor(n, m, 3, seed)
    return n, X.xor_to_cnf(n, rows)


def hidden_xor(seed, n_orig=12, width=6, chains=2):
    """Long parities Tseitin-split into 3-XOR chains with aux vars."""
    rng = random.Random(seed)
    clauses = []
    nv = n_orig
    # NOTE: xor_to_cnf expects 0-BASED variable ids (it shifts +1).
    for _ in range(chains):
        vs = rng.sample(range(n_orig), width)          # 0-based
        rhs = rng.randint(0, 1)
        prev = vs[0]
        for k in range(1, width - 1):
            aux = nv                                    # 0-based id of new var
            nv += 1
            clauses += X.xor_to_cnf(0, [([prev, vs[k], aux], 0)])
            prev = aux
        clauses += X.xor_to_cnf(0, [([prev, vs[width - 1]], rhs)])
    return nv, clauses


def mixed(seed, phi, n=16):
    rng = random.Random(seed)
    m_total = round(2.0 * n)
    m_xor = round(phi * m_total)
    rows = X.gen_xor(n, m_xor, 3, seed)
    clauses = X.xor_to_cnf(n, rows)
    for _ in range(m_total - m_xor):
        vs = rng.sample(range(1, n + 1), 3)
        clauses.append([v * rng.choice((1, -1)) for v in vs])
    return n, clauses


def pure_cnf(seed, n=16, alpha=3.5):
    rng = random.Random(seed * 77)
    clauses = []
    for _ in range(round(alpha * n)):
        vs = rng.sample(range(1, n + 1), 3)
        clauses.append([v * rng.choice((1, -1)) for v in vs])
    return n, clauses


def write_cnf(path, n, clauses):
    with open(path, "w") as f:
        f.write(f"p cnf {n} {len(clauses)}\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")


def run_cell(name, n, clauses, work, informed=False):
    cnf = work / f"{name}.cnf"
    write_cnf(cnf, n, clauses)
    cand = informed_pairs(clauses, n) if informed else None
    if informed and not cand:
        return {"name": name, "informed_degenerate": True}
    g = greedy(cnf, n, work, cand)
    rc = random_controls(cnf, n, work, len(g["path"]) - 1)
    g.update({"name": name, "informed": informed,
              "random_endpoints": rc,
              "beats_best_random": g["endpoint"] < min(rc) if rc else None})
    return g


def main(out_dir):
    work = Path(tempfile.mkdtemp(prefix="s4p1-"))
    res = []
    for seed in range(1, 6):
        n, cl = pure_xor(seed)
        res.append(run_cell(f"xor_{seed}", n, cl, work))
        print(res[-1]["name"], res[-1]["path"], flush=True)
    for seed in range(1, 6):
        n, cl = hidden_xor(seed)
        res.append(run_cell(f"hidden_{seed}", n, cl, work))
        print(res[-1]["name"], res[-1]["path"], flush=True)
        res.append(run_cell(f"hidden_{seed}_informed", n, cl, work, True))
        r = res[-1]
        print(r["name"], r.get("path", "DEGENERATE"), flush=True)
    for phi in (0.25, 0.5, 0.75):
        for seed in (1, 2, 3):
            n, cl = mixed(seed, phi)
            res.append(run_cell(f"mixed{phi}_{seed}", n, cl, work))
            print(res[-1]["name"], res[-1]["path"], flush=True)
    for seed in range(1, 6):
        n, cl = pure_cnf(seed)
        res.append(run_cell(f"cnf_{seed}", n, cl, work))
        print(res[-1]["name"], res[-1]["path"], flush=True)
    Path(out_dir).write_text(json.dumps(res, indent=1))
    print("wrote", out_dir)


if __name__ == "__main__":
    main(sys.argv[1])
