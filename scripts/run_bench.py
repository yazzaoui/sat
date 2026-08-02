#!/usr/bin/env python3
"""Phase 0 benchmark harness: CaDiCaL vs SaDiCaL (+ dpr-trim verification).

Usage:
  python3 scripts/run_bench.py --family php --sizes 6 7 8 9 10 --timeout 300
  python3 scripts/run_bench.py --family mchess --sizes 6 8 10 12 --timeout 300

Writes benchmarks/results/<family>.csv and prints a markdown table.
Instances are generated into benchmarks/cnf/, proofs into benchmarks/proofs/.
"""
import argparse
import csv
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CADICAL = ROOT / "tools/cadical/build/cadical"
SADICAL = ROOT / "tools/sadical/sadical"
DPRTRIM = ROOT / "tools/dpr-trim/dpr-trim"
CNF = ROOT / "benchmarks/cnf"
PROOFS = ROOT / "benchmarks/proofs"
RESULTS = ROOT / "benchmarks/results"

GENERATORS = {
    "php": ROOT / "generators/php.py",
    "mchess": ROOT / "generators/chessboard.py",
    "tseitin": ROOT / "generators/tseitin.py",
}


def run(cmd, timeout):
    t0 = time.monotonic()
    try:
        p = subprocess.run(
            [str(c) for c in cmd], capture_output=True, text=True, timeout=timeout
        )
        return time.monotonic() - t0, p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return timeout, None, ""


def conflicts_of(output):
    m = re.search(r"conflicts:?\s+(\d+)", output)
    return int(m.group(1)) if m else None


def status_of(code):
    return {10: "SAT", 20: "UNSAT"}.get(code, "timeout" if code is None else f"exit{code}")


def bench(family, size, timeout, sadical_opts=()):
    cnf = CNF / f"{family}{size}.cnf"
    if not cnf.exists():
        cnf.write_text(
            subprocess.run(
                [sys.executable, str(GENERATORS[family]), str(size)],
                capture_output=True, text=True, check=True,
            ).stdout
        )

    row = {"family": family, "size": size}

    t, code, out = run([CADICAL, cnf], timeout)
    row |= {"cadical_status": status_of(code), "cadical_time": round(t, 2),
            "cadical_conflicts": conflicts_of(out)}

    proof = PROOFS / f"{family}{size}.pr"
    t, code, out = run(
        [SADICAL, "--binary=false", "-f", *sadical_opts, cnf, proof], timeout)
    row |= {"sadical_status": status_of(code), "sadical_time": round(t, 2),
            "sadical_conflicts": conflicts_of(out)}

    if row["sadical_status"] == "UNSAT":
        t, code, out = run([DPRTRIM, cnf, proof], max(timeout, 600))
        row["proof_verified"] = "yes" if "s VERIFIED" in out else "NO"
        row["verify_time"] = round(t, 2)
    else:
        row["proof_verified"] = "-"
        row["verify_time"] = "-"
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True, choices=GENERATORS)
    ap.add_argument("--sizes", type=int, nargs="+", required=True)
    ap.add_argument("--timeout", type=float, default=300)
    ap.add_argument("--sadical-opt", action="append", default=[],
                    help="extra option passed to sadical (repeatable)")
    args = ap.parse_args()

    for d in (CNF, PROOFS, RESULTS):
        d.mkdir(parents=True, exist_ok=True)

    rows = []
    for size in args.sizes:
        row = bench(args.family, size, args.timeout, args.sadical_opt)
        rows.append(row)
        print(f"done {args.family}({size}): "
              f"cadical={row['cadical_status']}/{row['cadical_time']}s "
              f"sadical={row['sadical_status']}/{row['sadical_time']}s "
              f"verified={row['proof_verified']}", flush=True)

    sizes = "-".join(str(s) for s in args.sizes)
    out = RESULTS / f"{args.family}_{sizes}.csv"
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    cols = list(rows[0].keys())
    print("\n| " + " | ".join(cols) + " |")
    print("|" + "|".join("---" for _ in cols) + "|")
    for r in rows:
        print("| " + " | ".join(str(r[c]) for c in cols) + " |")


if __name__ == "__main__":
    main()
