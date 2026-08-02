#!/usr/bin/env python3
"""Close the two L0 validation gaps against the registration:

1. Barrier-ordering validation (registration §3.2, second clause):
   sampled barrier estimates must rank-correlate >= 0.8 with exact
   barrier_mean per (n, density) seed family, on the exact sizes.
   Sampled estimate: attractor reps from basin sampling, first-passage
   ensemble (registered §3.3 parameters, N reduced to 50/pair for the
   validation run — recorded), instance summary = mean over observed
   pair minima of max-V.
2. Family 20/0.9 basin re-validation at R=500 (estimator engineering
   during bring-up; both the R=200 rho=0.76 and the re-validated number
   are reported).

Updates docs/L0-results-data.json in place (adds 'barrier_validation'
and 'family_20_09_revalidation' to summary).
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
from l0_calibrate import spearman, EXACT_N, DENSITIES, SEEDS  # noqa: E402


def sampled_barrier(n, clauses, seed):
    rng = random.Random(seed)
    bs = P.basin_sample(n, clauses, R=200, seed=seed)
    reps = bs["_reps"][:5]                     # cap attractors at 5
    if len(reps) < 2:
        return None
    walks = P.barrier_sample(n, clauses, reps, rng, N=50)
    best = {}
    for w in walks:
        if w["reached"] is None:
            continue
        key = tuple(sorted((w["from"], w["reached"])))
        best[key] = min(best.get(key, 1 << 30), w["max_V"])
    if not best:
        return None
    return sum(best.values()) / len(best)


def main():
    data_file = WS / "docs/L0-results-data.json"
    data = json.loads(data_file.read_text())
    rows = data["rows"]

    fam_rho = {}
    for n in EXACT_N:
        for d in DENSITIES:
            ex, sm = [], []
            for seed in SEEDS:
                r = next(r for r in rows if r["n"] == n
                         and r["density"] == d and r["seed"] == seed)
                xr = X.gen_xor(n, round(d * n), 3, seed)
                clauses = X.xor_to_cnf(n, xr)
                est = sampled_barrier(n, clauses, seed)
                if est is None:
                    continue
                ex.append(r["exact_pre"]["barrier_mean"])
                sm.append(est)
            rho = round(spearman(ex, sm), 3) if len(ex) >= 5 else None
            fam_rho[f"{n}/{d}"] = {"rho": rho, "pairs": len(ex)}
            print(f"barrier validation {n}/{d}: rho={rho} ({len(ex)} seeds)",
                  flush=True)

    reval = []
    for seed in SEEDS:
        xr = X.gen_xor(20, round(0.9 * 20), 3, seed)
        clauses = X.xor_to_cnf(20, xr)
        bs = P.basin_sample(20, clauses, R=500, seed=seed)
        r = next(r for r in rows if r["n"] == 20 and r["density"] == 0.9
                 and r["seed"] == seed)
        reval.append((r["exact_pre"]["basins"], bs["basins_est"]))
        print(f"20/0.9 seed {seed}: exact={reval[-1][0]} "
              f"R500={reval[-1][1]}", flush=True)
    rho500 = round(spearman(*zip(*reval)), 3)
    print(f"20/0.9 re-validation at R=500: rho={rho500}")

    data["summary"]["barrier_validation"] = {
        "family_spearman": fam_rho, "bar": 0.8,
        "protocol_note": "N=50/pair for validation run; attractors capped at 5"}
    data["summary"]["family_20_09_revalidation"] = {
        "initial_R200_rho": 0.76, "R500_rho": rho500}
    data_file.write_text(json.dumps(data, indent=1))
    print(f"updated {data_file}")


if __name__ == "__main__":
    main()
