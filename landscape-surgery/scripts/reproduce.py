#!/usr/bin/env python3
"""Landscape-surgery reproduction suite. Day-one per the L0 registration:
every claim lands here as a deterministic check when it is produced.

Current checks (grow per phase):
  1. Canonical merge-tree unit instances (known structure by hand).
  2. Calibration representative cell (n=16, density 0.9, seed 1):
     exact rugged->single-basin transition with pinned values.
  3. Committed calibration data internal consistency + gate + validation
     re-evaluation from docs/L0-results-data.json.

Registered future check (placeholder, lands at L1-prep with the Cook
generator): PHP(4)-anchor sampled-vs-exact validation in BOTH views —
the only instance where corridors have ground truth (lead build note).
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WS / "probes"))
import probes as P                                     # noqa: E402
import xor_tools as X                                  # noqa: E402

EXACT = WS / "probes/exact"
results = []


def check(name, ok, detail):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def exact_probe(cnf):
    r = subprocess.run([str(EXACT), "--lex", str(cnf)],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def main():
    work = Path(tempfile.mkdtemp(prefix="ls-repro-"))

    # 1. Unit merge trees.
    t1 = work / "t1.cnf"
    t1.write_text("p cnf 2 1\n1 2 0\n")
    e = exact_probe(t1)
    check("unit single-plateau", e["basins"] == 1 and e["lex_basins"] == 2,
          f"merge-tree {e['basins']} (lex artifact: {e['lex_basins']})")
    cl = []
    for s in (1, 2, 4, 3, 5, 6):
        cl.append([-(b + 1) if (s >> b) & 1 else (b + 1) for b in range(3)])
    t2 = work / "t2.cnf"
    t2.write_text(f"p cnf 3 {len(cl)}\n"
                  + "".join(" ".join(map(str, c)) + " 0\n" for c in cl))
    e = exact_probe(t2)
    check("unit two-minima", e["basins"] == 2 and e["barrier_max"] == 1,
          f"basins={e['basins']} barrier={e['barrier_max']}")

    # 2. Calibration representative cell (pinned).
    rows = X.gen_xor(16, round(0.9 * 16), 3, 1)
    pre = work / "cal.cnf"
    X.write_dimacs(pre, 16, X.xor_to_cnf(16, rows))
    n_new, cls, inc = X.eliminated_cnf(16, rows)
    post = work / "cal.elim.cnf"
    X.write_dimacs(post, max(n_new, 1), cls)
    e1, e2 = exact_probe(pre), exact_probe(post)
    check("calibration cell pre (rugged)",
          e1["basins"] == 68 and abs(e1["barrier_mean"] - 3.5522) < 1e-3,
          f"basins={e1['basins']} barrier_mean={e1['barrier_mean']}")
    check("calibration cell post (single basin)",
          e2["basins"] == 1 and e2["barrier_max"] == 0 and inc == 0,
          f"basins={e2['basins']}")

    # 3. Committed calibration data: gate + validation re-evaluated.
    data_file = WS / "docs/L0-results-data.json"
    if data_file.exists():
        data = json.loads(data_file.read_text())
        g = data["summary"]["gate"]
        check("L0 gate: exact plural-before/single-after",
              g["plural_before"] == g["exact_rows"]
              and g["single_after"] == g["exact_rows"],
              f"{g['plural_before']}/{g['exact_rows']} plural, "
              f"{g['single_after']}/{g['exact_rows']} single-after")
        v = data["summary"]["validation"]
        check("L0 validation: pooled Spearman >= 0.8",
              v["pooled_spearman"] >= 0.8, f"rho={v['pooled_spearman']}")
    else:
        check("L0 calibration data present", False, "docs/L0-results-data.json missing")

    # 4. Empirical anchors of the extension-inertness theorems.
    sys.path.insert(0, str(WS / "extvars"))
    import cook                                        # noqa: E402
    nv, cl = cook.php_clauses(4)
    a4 = work / "armA_php4.cnf"
    cook.write_dimacs(a4, nv, cl)
    e = exact_probe(a4)
    check("UNSAT PHP(4) baseline = single plateau system",
          e["basins"] == 1 and e["min_V"] == 1 and e["n_min_states"] == 60
          and e["lex_basins"] == 24,
          f"basins={e['basins']} lex-artifact={e['lex_basins']}")
    nb, clb = cook.arm_b_formula(4)
    b4 = work / "armB_php4.cnf"
    cook.write_dimacs(b4, nb, clb)
    e = exact_probe(b4)
    check("Cook cascade fragments anchor 1 -> 115",
          e["basins"] == 115 and e["barrier_max"] == 4,
          f"basins={e['basins']} barrier_max={e['barrier_max']}")
    h = 4
    var = lambda i, j: (i - 1) * h + j                 # noqa: E731
    cl44 = [[var(i, j) for j in range(1, h + 1)] for i in range(1, 5)]
    for j in range(1, h + 1):
        for i in range(1, 5):
            for k in range(i + 1, 5):
                cl44.append([-var(i, j), -var(k, j)])
    s44 = work / "php44.cnf"
    cook.write_dimacs(s44, 16, cl44)
    e = exact_probe(s44)
    check("SAT sibling PHP(4,4): 24 isolated solution basins, ridge 1",
          e["basins"] == 24 and e["n_min_states"] == 24
          and e["barrier_max"] == 1 and e["min_V"] == 0,
          f"basins={e['basins']} ridge={e['barrier_max']}")
    # Cook logic gate (permanent, per L1 registration gate 1)
    import subprocess as sp
    for p in (4, 5):
        nvp, clp = cook.php_clauses(p)
        cnf = work / f"gate{p}.cnf"
        cook.write_dimacs(cnf, nvp, clp)
        _, _, proof, _ = cook.cascade(p)
        drat = work / f"gate{p}.drat"
        cook.write_proof(drat, proof)
        DPR = WS.parent / "common/tools/dpr-trim/dpr-trim"
        r = sp.run([str(DPR), str(cnf), str(drat)],
                   capture_output=True, text=True)
        check(f"Cook logic gate PHP({p})", "s VERIFIED" in r.stdout,
              "dpr-trim VERIFIED" if "s VERIFIED" in r.stdout else "FAILED")

    n_ok = sum(results)
    print(f"\n{n_ok}/{len(results)} checks passed")
    sys.exit(0 if n_ok == len(results) else 1)


if __name__ == "__main__":
    main()
