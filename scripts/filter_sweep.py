#!/usr/bin/env python3
"""Filter-mode sweep across the coverage spectrum (tasks: coloring
expansion + coverage-threshold curve).

Per instance: blind structure recovery (coverage, labels, involutions),
then wall clock for CaDiCaL, stock SaDiCaL, filter-mode SaDiCaL.
Output: benchmarks/results/filter_sweep.csv
"""
import csv
import glob
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRATCH = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "benchmarks/results"
TIMEOUT = 120

CADICAL = ROOT / "tools/cadical/build/cadical"
SADICAL = ROOT / "tools/sadical/sadical"
COMP = ROOT / "benchmarks/competition"


def pick(pattern, n):
    return sorted(glob.glob(str(COMP / pattern), recursive=True))[:n]


INSTANCES = (
    pick("flat50-115/**/*.cnf", 5) + pick("flat75-180/**/*.cnf", 5)
    + pick("flat100-239/**/*.cnf", 5) + pick("flat125-301/**/*.cnf", 5)
    + pick("flat150-360/**/*.cnf", 5) + pick("flat200-479/**/*.cnf", 5)
    + pick("uf100-430/**/*.cnf", 3) + pick("uf250-1065/**/*.cnf", 2)
    + pick("logistics/*.cnf", 4) + pick("bmc/bmc-ibm-[1-5].cnf", 5)
    + [str(ROOT / "benchmarks/cnf/mchess12.cnf"),
       str(ROOT / "benchmarks/cnf/mchess14.cnf"),
       str(ROOT / "benchmarks/cnf/php10.cnf"),
       str(ROOT / "benchmarks/cnf/php11.cnf")]
)


def timed(cmd, timeout=TIMEOUT):
    t0 = time.time()
    try:
        r = subprocess.run([str(c) for c in cmd], capture_output=True,
                           timeout=timeout)
        return round(time.time() - t0, 3), r.returncode
    except subprocess.TimeoutExpired:
        return timeout, None


def main():
    rows = []
    out = ROOT / "benchmarks/results/filter_sweep.csv"
    for cnf in INSTANCES:
        name = Path(cnf).stem
        inv = SCRATCH / f"{name}.inv"
        ovl = SCRATCH / f"{name}.overlay.json"
        t0 = time.time()
        try:
            subprocess.run([sys.executable, str(ROOT / "scripts/structure.py"),
                            cnf, "--json", str(ovl), "--involutions", str(inv)],
                           capture_output=True, timeout=300, check=True)
            struct_t = round(time.time() - t0, 2)
            overlay = json.loads(ovl.read_text())
        except Exception as e:
            print(f"{name}: structure FAILED ({e})", flush=True)
            continue
        row = {"instance": name, "coverage": overlay["coverage"],
               "labels": "+".join(overlay["labels"]) or "-",
               "struct_time": struct_t}
        row["cadical"], row["cadical_exit"] = timed([CADICAL, "-q", cnf])
        row["stock"], row["stock_exit"] = timed([SADICAL, "-q", "-n", cnf])
        # prune-off arm: SaDiCaL as plain CDCL — decomposes any "filter win"
        # into "filtering" vs "witness hunt was pure overhead here"
        row["pruneoff"], row["pruneoff_exit"] = timed(
            [SADICAL, "-q", "-n", "--prune=false", cnf])
        # probation-gated filter (tplprobation=200, tplminhit=90 defaults)
        row["filter"], row["filter_exit"] = timed(
            [SADICAL, "-q", "-n", "--tplfilter=true", f"--template={inv}", cnf])
        exits = {row[k] for k in ("stock_exit", "filter_exit", "pruneoff_exit")
                 if row[k] is not None}
        if len(exits) > 1:
            row["labels"] += " RESULT-MISMATCH"
        # A non-solver exit (not 10/20/timeout) is a parse or crash error,
        # not a timing — identical failures across arms must not pass
        # silently (SATLIB uf header bug, caught in Experiment C).
        if any(row[k] not in (10, 20, None)
               for k in ("cadical_exit", "stock_exit", "filter_exit",
                         "pruneoff_exit")):
            row["labels"] += " ARM-ERROR"
        rows.append(row)
        print(f"{name}: cov={row['coverage']:.0%} labels={row['labels']} "
              f"cadical={row['cadical']} stock={row['stock']} "
              f"filter={row['filter']}", flush=True)
        with out.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
