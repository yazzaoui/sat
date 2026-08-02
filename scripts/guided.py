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
        # Gate v3: every regime decision is made online (acceptance-keyed
        # probation with template-hit veto, periodic re-probe). Structure
        # detection is demoted to a prior: it supplies templates when
        # found and sets the probation budget, nothing more.
        cmd = [str(SADICAL), "-q", "-n", "--tplfilter=true"]
        if inv.stat().st_size > 0:
            cmd += [f"--template={inv}"]
            mode = (f"gated with templates (coverage "
                    f"{overlay['coverage']:.0%}, labels {overlay['labels']})")
        else:
            cmd += ["--tplprobation=100"]     # less to measure, smaller tax
            mode = "gated, no templates (acceptance-only probation)"
        print(f"c guided: {mode}", file=sys.stderr)
        cmd += extra + [cnf] + proof
        r = subprocess.run(cmd)
        sys.exit(r.returncode)


if __name__ == "__main__":
    main()
