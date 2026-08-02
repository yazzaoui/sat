#!/usr/bin/env python3
"""S4 reproduction suite: pinned representative cells."""
import sys
import tempfile
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WS / "scripts"))
from run_p1 import (pure_xor, hidden_xor, pure_cnf, write_cnf,   # noqa: E402
                    greedy, random_controls)

results = []


def check(name, ok, detail):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def main():
    work = Path(tempfile.mkdtemp(prefix="s4-repro-"))
    n, cl = pure_xor(1)
    cnf = work / "a.cnf"
    write_cnf(cnf, n, cl)
    g = greedy(cnf, n, work)
    check("anchor loop path = P0 greedy [68,40,24,16,12]",
          g["path"] == [68, 40, 24, 16, 12], str(g["path"]))
    rc = random_controls(cnf, n, work, 4)
    check("random compositions never improve on anchor",
          min(rc) >= 68, f"rnd_min={min(rc)}")

    n, cl = hidden_xor(3)
    cnf = work / "h3.cnf"
    write_cnf(cnf, n, cl)
    g = greedy(cnf, n, work, max_steps=2)
    check("hidden_3 stuck at identity (one-op horizon)",
          g["path"] == [256], str(g["path"]))

    n, cl = pure_cnf(2)
    cnf = work / "c2.cnf"
    write_cnf(cnf, n, cl)
    g = greedy(cnf, n, work, max_steps=2)
    check("cnf_2 null respected", g["path"] == [3], str(g["path"]))

    n_ok = sum(results)
    print(f"\n{n_ok}/{len(results)} checks passed")
    sys.exit(0 if n_ok == len(results) else 1)


if __name__ == "__main__":
    main()
