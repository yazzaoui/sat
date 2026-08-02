#!/usr/bin/env python3
"""Guided SDCL front-end: blind structure recovery, then auto-gated solver
invocation. This is the 'guided' entry in the M2 benchmark table.

Gate (measured, see docs/coverage-threshold.md): filter mode only when
detected structure coverage >= FILTER_THRESHOLD — below it, filter mode is
harmful (missed prunes compound); the solver runs stock.

Usage: guided.py <cnf> [proof] [-- <extra sadical args>]
Exit code = solver exit code (10 SAT / 20 UNSAT).
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SADICAL = ROOT / "tools/sadical/sadical"

def main():
    args = sys.argv[1:]
    extra = []
    if "--" in args:
        i = args.index("--")
        args, extra = args[:i], args[i + 1:]
    cnf = args[0]
    proof = args[1:2]

    with tempfile.TemporaryDirectory() as td:
        ovl = Path(td) / "overlay.json"
        inv = Path(td) / "templates.inv"
        subprocess.run(
            [sys.executable, str(ROOT / "scripts/structure.py"), cnf,
             "--json", str(ovl), "--involutions", str(inv)],
            capture_output=True, check=True, timeout=300)
        overlay = json.loads(ovl.read_text())
        cmd = [str(SADICAL), "-q", "-n"]
        # Offline coverage does NOT predict filter safety (chessboard:
        # 100% coverage, 54% hits). The gate is online: filter mode runs
        # under probation (tplprobation/tplminhit defaults) and disables
        # itself when measured template hit share is insufficient.
        if inv.stat().st_size > 0:
            mode = (f"filter under probation "
                    f"(coverage {overlay['coverage']:.0%}, "
                    f"labels {overlay['labels']})")
            cmd += ["--tplfilter=true", f"--template={inv}"]
        else:
            mode = "stock (no structure detected)"
        print(f"c guided: {mode}", file=sys.stderr)
        cmd += extra + [cnf] + proof
        r = subprocess.run(cmd)
        sys.exit(r.returncode)


if __name__ == "__main__":
    main()
