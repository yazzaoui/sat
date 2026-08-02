#!/usr/bin/env python3
"""L0 calibration run (registration §4): random 3-XOR, identity vs
eliminated basis, exact n ∈ {16,20,24} + sampled n ∈ {40,60},
densities {0.7, 0.9}, seeds 1..10.

Gate: exact probes must show plural basins before / single basin after
(SAT: basins==1 at min_V==0; UNSAT: single minimum plateau with the
inconsistency offset). Sampled probes validated against exact by
Spearman >= 0.8 (basin-count orderings per (n,density) seed family and
pooled), and must show the same transition at n ∈ {40,60}.

Output: benchmarks-style JSON lines + summary; writes
../docs/L0-results-data.json
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent
sys.path.insert(0, str(WS / "probes"))
import probes as P                                    # noqa: E402
import xor_tools as X                                 # noqa: E402

EXACT = WS / "probes/exact"
SEEDS = range(1, 11)
DENSITIES = (0.7, 0.9)
EXACT_N = (16, 20, 24)
SAMPLED_N = (40, 60)


def spearman(xs, ys):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(xs), rank(ys)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    return num / (dx * dy) if dx and dy else 0.0


def exact_probe(cnf):
    r = subprocess.run([str(EXACT), "--lex", str(cnf)],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def main():
    work = Path(tempfile.mkdtemp(prefix="l0-"))
    rows = []
    print(f"work: {work}", flush=True)

    for n in EXACT_N + SAMPLED_N:
        for dens in DENSITIES:
            m = round(dens * n)
            for seed in SEEDS:
                rec = {"n": n, "density": dens, "seed": seed}
                xor_rows = X.gen_xor(n, m, 3, seed)
                pre = work / f"x{n}_{dens}_{seed}.cnf"
                X.write_dimacs(pre, n, X.xor_to_cnf(n, xor_rows))
                n_new, elim_clauses, inconsistent = X.eliminated_cnf(n, xor_rows)
                post = work / f"x{n}_{dens}_{seed}.elim.cnf"
                X.write_dimacs(post, max(n_new, 1), elim_clauses)
                rec["satisfiable"] = inconsistent == 0
                rec["inconsistent_rows"] = inconsistent

                if n in EXACT_N:
                    e_pre = exact_probe(pre)
                    e_post = exact_probe(post)
                    rec["exact_pre"] = e_pre
                    rec["exact_post"] = e_post
                # sampled on every size (validation overlap on exact sizes)
                nc, cls = P.load_cnf(pre)
                rec["sampled_pre"] = P.basin_sample(nc, cls, R=200, seed=seed)
                nc2, cls2 = P.load_cnf(post)
                rec["sampled_post"] = P.basin_sample(nc2, cls2, R=100, seed=seed)
                rows.append(rec)
                pre_b = rec.get("exact_pre", {}).get("basins",
                        rec["sampled_pre"]["basins_est"])
                post_b = rec.get("exact_post", {}).get("basins",
                         rec["sampled_post"]["basins_est"])
                print(f"n={n} d={dens} seed={seed} sat={rec['satisfiable']} "
                      f"basins pre={pre_b} post={post_b}", flush=True)

    # --- Gate evaluation ---
    summary = {"gate": {}, "validation": {}, "lex_divergence": []}
    exact_rows = [r for r in rows if "exact_pre" in r]
    plural_pre = sum(1 for r in exact_rows if r["exact_pre"]["basins"] > 1)
    single_post = sum(1 for r in exact_rows if r["exact_post"]["basins"] == 1)
    summary["gate"]["exact_rows"] = len(exact_rows)
    summary["gate"]["plural_before"] = plural_pre
    summary["gate"]["single_after"] = single_post
    big = [r for r in rows if r["n"] in SAMPLED_N]
    summary["gate"]["sampled_rows"] = len(big)
    summary["gate"]["sampled_single_after"] = sum(
        1 for r in big if r["sampled_post"]["basins_est"] == 1)
    summary["gate"]["sampled_plural_before"] = sum(
        1 for r in big if r["sampled_pre"]["basins_est"] > 1)

    # Validation: Spearman per (n, density) family + pooled, exact sizes.
    pooled_x, pooled_y = [], []
    fams = {}
    for r in exact_rows:
        fams.setdefault((r["n"], r["density"]), []).append(
            (r["exact_pre"]["basins"], r["sampled_pre"]["basins_est"]))
        pooled_x.append(r["exact_pre"]["basins"])
        pooled_y.append(r["sampled_pre"]["basins_est"])
    fam_rho = {f"{n}/{d}": round(spearman(*zip(*v)), 3)
               for (n, d), v in fams.items()}
    summary["validation"]["family_spearman"] = fam_rho
    summary["validation"]["pooled_spearman"] = round(
        spearman(pooled_x, pooled_y), 3)
    summary["validation"]["bar"] = 0.8

    for r in exact_rows:
        for phase in ("exact_pre", "exact_post"):
            e = r[phase]
            if e["basins"] and abs(e["lex_basins"] - e["basins"]) > 0.1 * e["basins"]:
                summary["lex_divergence"].append(
                    {"n": r["n"], "density": r["density"], "seed": r["seed"],
                     "phase": phase, "merge_tree": e["basins"],
                     "lex": e["lex_basins"]})

    out = WS / "docs/L0-results-data.json"
    out.write_text(json.dumps({"rows": rows, "summary": summary}, indent=1))
    print("\nSUMMARY:", json.dumps(summary["gate"]))
    print("VALIDATION:", json.dumps(summary["validation"]))
    print(f"lex divergences: {len(summary['lex_divergence'])}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
