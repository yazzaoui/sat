#!/usr/bin/env python3
"""Reproduce the boundary map from scratch: one representative row per
edge, plus the M0 foundation, determinism gates, and the shipped gate's
verdicts. Every check is deterministic (conflict counts, verdicts,
dpr-trim) except the two labelled measurements, which use tolerance
bands. Exit 0 iff every check passes.

Run from the repository root after building the toolchain
(see REPRODUCING.md). Instances are regenerated from seeds into a
temporary work directory — nothing outside the repo is consulted.
"""
import json
import re
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CADICAL = ROOT.parent / "common/tools/cadical/build/cadical"
SADICAL = ROOT.parent / "common/tools/sadical/sadical"
DPRTRIM = ROOT.parent / "common/tools/dpr-trim/dpr-trim"

results = []


def check(name, ok, detail):
    results.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def gen(work, family, arg):
    out = work / f"{family}{arg}.cnf"
    script = {"php": "php.py", "mchess": "chessboard.py",
              "tseitin": "tseitin.py"}[family]
    out.write_text(subprocess.run(
        [sys.executable, str(ROOT.parent / "common/generators" / script), str(arg)],
        capture_output=True, text=True, check=True).stdout)
    return out


def sadical(args, timeout=300):
    return subprocess.run([str(SADICAL), *[str(a) for a in args]],
                          capture_output=True, text=True, timeout=timeout)


def conflicts_of(eventlog):
    return [json.loads(l) for l in open(eventlog)][-1]["conflicts"]


def main():
    work = Path(tempfile.mkdtemp(prefix="repro-"))
    print(f"work dir: {work}\n")

    php12 = gen(work, "php", 12)
    mchess12 = gen(work, "mchess", 12)
    mchess14 = gen(work, "mchess", 14)
    tseitin40 = gen(work, "tseitin", 40)

    # --- M0 foundation: PHP(12), CDCL-hard, SDCL-trivial, proof verified.
    proof = work / "php12.pr"
    r = sadical(["-q", "-n", "--binary=false", "-f",
                 f"--eventlog={work}/php12.jsonl", php12, proof])
    v = subprocess.run([str(DPRTRIM), str(php12), str(proof)],
                       capture_output=True, text=True)
    check("M0 php12 UNSAT+verified+487",
          r.returncode == 20 and "s VERIFIED" in v.stdout
          and conflicts_of(f"{work}/php12.jsonl") == 487,
          f"exit={r.returncode} conflicts={conflicts_of(f'{work}/php12.jsonl')} "
          f"verified={'s VERIFIED' in v.stdout}")

    # --- Determinism gate: frozen stock conflict counts.
    for cnf, want in ((mchess12, 39848), (mchess14, 279631),
                      (tseitin40, 162220)):
        ev = work / (cnf.stem + ".stock.jsonl")
        sadical(["-q", "-n", f"--eventlog={ev}", cnf])
        got = conflicts_of(ev)
        check(f"determinism {cnf.stem}", got == want,
              f"conflicts={got} frozen={want}")

    # --- Structure recovery (blind validation, edge-1 prerequisite).
    inv14 = work / "mchess14.inv"
    s = subprocess.run([sys.executable, str(ROOT / "scripts/structure.py"),
                        str(mchess14), "--involutions", str(inv14)],
                       capture_output=True, text=True)
    check("structure mchess14 = counting+grid",
          "'counting', 'grid'" in s.stdout or "counting" in s.stdout
          and "grid" in s.stdout, s.stdout.strip().split("\n")[0][:90])

    # --- Edge 1: static template cores degrade steering (direct mode).
    ev = work / "edge1.jsonl"
    sadical(["-q", "-n", "--templatetries=1024", f"--template={inv14}",
             f"--eventlog={ev}", mchess14])
    got = conflicts_of(ev)
    check("edge1 template-direct conflicts inflate >=1.5x",
          got >= 1.5 * 279631, f"conflicts={got} (stock 279631)")

    # --- Edge 2 (Experiment A): conflict-analysis seeding harms.
    ev = work / "edge2.jsonl"
    sadical(["-q", "-n", "--seed=1", f"--eventlog={ev}", mchess14])
    got = conflicts_of(ev)
    check("edge2 A1 seeding = 466476", got == 466476, f"conflicts={got}")

    # --- Edge 3 (Experiment C): activity harvest harms.
    ev = work / "edge3.jsonl"
    sadical(["-q", "-n", "--harvest=1", f"--eventlog={ev}", mchess14])
    got = conflicts_of(ev)
    check("edge3 C1 harvest = 450448", got == 450448, f"conflicts={got}")

    # --- Edge 4 (E termination measurement): filtering dominates.
    r = sadical(["-n", mchess14])
    m = re.search(r"filtering:\s+[\d.]+ sec\s+(\d+)%", r.stdout)
    pct = int(m.group(1)) if m else -1
    check("edge4 filtering >=45% of process time", pct >= 45, f"{pct}%")

    # --- Edge 5 (churn): domain reconstitution per delta.
    ev = work / "edge5.jsonl"
    sadical(["-q", "-n", "--logfilter=true", f"--eventlog={ev}", mchess14])
    att = [e for e in (json.loads(l) for l in open(ev))
           if e["ev"] == "attempt"]
    rec = []
    doms = [frozenset(e["fchk"]) for e in att]
    flts = [frozenset(e["fflt"]) for e in att]
    for i in range(len(att) - 1):
        union = doms[i] | doms[i + 1]
        if not union:
            continue
        flips = sum(1 for c in doms[i] & doms[i + 1]
                    if (c in flts[i]) != (c in flts[i + 1]))
        rec.append((len(doms[i] ^ doms[i + 1]) + flips) / len(union))
    med = statistics.median(rec)
    check("edge5 recompute median in [0.50, 0.65]", 0.50 <= med <= 0.65,
          f"median={med:.3f} (registered gate threshold 0.10-0.15)")

    # --- Shipped gate: three verdicts, steering-neutral revert.
    inv12 = work / "php12.inv"
    subprocess.run([sys.executable, str(ROOT / "scripts/structure.py"),
                    str(php12), "--involutions", str(inv12)],
                   capture_output=True)
    r = sadical(["-n", "--tplfilter=true", f"--template={inv12}", php12])
    check("gate php12 filter confirmed @100%",
          "confirmed by probation (100% hits)" in r.stdout, "verdict line found"
          if "confirmed" in r.stdout else r.stdout[-200:])
    ev = work / "gate14.jsonl"
    r = sadical(["-n", "--tplfilter=true", f"--template={inv14}",
                 f"--eventlog={ev}", mchess14])
    got = conflicts_of(ev)
    check("gate mchess14 reverts, conflicts == stock",
          "templates disabled after probation" in r.stdout and got == 279631,
          f"conflicts={got} (stock 279631), verdict "
          f"{'found' if 'templates disabled' in r.stdout else 'MISSING'}")

    n_ok = sum(1 for _, ok, _ in results if ok)
    print(f"\n{n_ok}/{len(results)} checks passed")
    sys.exit(0 if n_ok == len(results) else 1)


if __name__ == "__main__":
    main()
