#!/usr/bin/env python3
"""Assemble the M2 benchmark table (docs/m2-benchmark.md).

Inputs:
  - benchmarks/results/filter_sweep.csv  (cadical / stock / pruneoff arms;
    binary-stable columns)
  - a fresh gated-arm pass run HERE with the final binary (the sweep's
    'filter' column mixed gate semantics across mid-sweep rebuilds and is
    discarded)
  - synthetic family rows (php / mchess / tseitin) run here: guided vs
    stock vs cadical, dpr-trim verification on every UNSAT guided run.

Probation-tax accounting (lead directive): tax = gated - min(stock,
pruneoff). Negative = the gate beats every static arm; positive = the
measured cost of gating in that regime.
"""
import csv
import glob
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRATCH = Path(sys.argv[1])
TIMEOUT = 120
CADICAL = ROOT / "tools/cadical/build/cadical"
SADICAL = ROOT / "tools/sadical/sadical"
DPRTRIM = ROOT / "tools/dpr-trim/dpr-trim"


def timed(cmd, timeout=TIMEOUT):
    t0 = time.time()
    try:
        r = subprocess.run([str(c) for c in cmd], capture_output=True,
                           text=True, timeout=timeout)
        return round(time.time() - t0, 3), r.returncode, r.stdout
    except subprocess.TimeoutExpired:
        return float(timeout), None, ""


def verdict_of(out):
    m = re.search(r"c (template filter confirmed|templates disabled|"
                  r"pruning disabled|template filter disabled)"
                  r" (?:by|after) probation "
                  r"\((\d+)% hits(?:, (\d+)% acceptance)?(, starved)?\)", out)
    if not m:
        return "no-verdict"
    kind = {"template filter confirmed": "filter-on",
            "templates disabled": "revert-stock",
            "pruning disabled": "prune-off",
            "template filter disabled": "filter-off"}[m.group(1)]
    acc = f"/{m.group(3)}%a" if m.group(3) else ""
    starved = "/starved" if m.group(4) else ""
    return f"{kind}@{m.group(2)}%h{acc}{starved}"


def gated_run(cnf, inv, proof=None):
    cmd = [SADICAL, "-n", "--tplfilter=true", f"--template={inv}"]
    if proof:
        cmd += ["--binary=false", "-f"]
    t, code, out = timed(cmd + [cnf] + ([proof] if proof else []))
    verified = ""
    if proof and code == 20:
        _, _, vout = timed([DPRTRIM, cnf, proof], 600)
        verified = "yes" if "s VERIFIED" in vout else "NO"
    return t, code, verdict_of(out), verified


def involutions_for(cnf):
    inv = SCRATCH / (Path(cnf).stem + ".m2.inv")
    subprocess.run([sys.executable, str(ROOT / "scripts/structure.py"),
                    str(cnf), "--involutions", str(inv)],
                   capture_output=True, timeout=300, check=True)
    return inv


def fmt(t, code):
    if code is None:
        return "timeout"
    return f"{t:.2f}"


def main():
    lines = []

    # --- competition rows from the sweep + fresh gated pass ---
    rows = list(csv.DictReader(open(ROOT / "benchmarks/results/filter_sweep.csv")))
    comp = []
    for r in rows:
        cnfs = glob.glob(str(ROOT / "benchmarks/competition" / "**" /
                             (r["instance"] + ".cnf")), recursive=True) or \
               glob.glob(str(ROOT / "benchmarks/cnf" / (r["instance"] + ".cnf")))
        if not cnfs:
            continue
        cnf = cnfs[0]
        inv = involutions_for(cnf)
        gt, gcode, verdict, _ = gated_run(cnf, inv)
        stock = float(r["stock"])
        pruneoff = float(r["pruneoff"])
        code = lambda k: None if r[k] in ("", "None") else int(float(r[k]))
        best = min(stock, pruneoff)
        tax = gt - best if gcode is not None else float("nan")
        comp.append({
            "instance": r["instance"], "labels": r["labels"],
            "cadical": fmt(float(r["cadical"]), code("cadical_exit")),
            "stock": fmt(stock, code("stock_exit")),
            "pruneoff": fmt(pruneoff, code("pruneoff_exit")),
            "gated": fmt(gt, gcode), "verdict": verdict,
            "tax": f"{tax:+.2f}" if tax == tax else "-",
        })
        print(f"{r['instance']}: gated={fmt(gt,gcode)} {verdict} tax={comp[-1]['tax']}",
              flush=True)

    hdr = ["instance", "labels", "cadical", "stock", "pruneoff", "gated",
           "verdict", "tax"]
    lines += ["## Competition instances (sweep + final-binary gated arm)", "",
              "| " + " | ".join(hdr) + " |",
              "|" + "|".join("---" for _ in hdr) + "|"]
    lines += ["| " + " | ".join(str(c[h]) for h in hdr) + " |" for c in comp]

    # --- synthetic UNSAT families: guided with verified proofs ---
    lines += ["", "## Synthetic families (UNSAT, guided proofs dpr-trim-verified)",
              "", "| instance | cadical | stock | gated | verdict | proof |",
              "|---|---|---|---|---|---|"]
    synth = [f"php{p}" for p in (10, 11, 12, 13)] + \
            [f"mchess{n}" for n in (12, 14, 16, 18)] + \
            [f"tseitin{n}" for n in (30, 40, 50)]
    for name in synth:
        cnf = ROOT / "benchmarks/cnf" / f"{name}.cnf"
        if not cnf.exists():
            continue
        inv = involutions_for(cnf)
        ct, ccode, _ = timed([CADICAL, "-q", cnf])
        st, scode, _ = timed([SADICAL, "-q", "-n", cnf])
        proof = SCRATCH / f"{name}.m2.pr"
        gt, gcode, verdict, verified = gated_run(cnf, inv, proof)
        lines.append(f"| {name} | {fmt(ct, ccode)} | {fmt(st, scode)} | "
                     f"{fmt(gt, gcode)} | {verdict} | {verified} |")
        print(f"{name}: cadical={fmt(ct,ccode)} stock={fmt(st,scode)} "
              f"gated={fmt(gt,gcode)} {verdict} verified={verified}", flush=True)

    out = ROOT / "docs/m2-benchmark.md"
    header = [
        "# M2 benchmark: guided (probation-gated) vs stock vs CaDiCaL",
        "",
        "Gate: measure-only probation window (200 witness-bearing attempts),",
        "then one of three verdicts — filter confirmed (>=90% template hits),",
        "templates disabled (revert to stock), pruning disabled (<5% hits,",
        "plain CDCL). `tax` = gated - min(stock, pruneoff): negative means",
        "the gate beats every static arm; positive is the measured cost of",
        "gating in that regime (lead directive: the portfolio-safe claim is",
        "measured, not asserted). Timeout 120 s.", ""]
    out.write_text("\n".join(header + lines) + "\n")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
