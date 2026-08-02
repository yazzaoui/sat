#!/usr/bin/env python3
"""S3 reproduction suite: pinned representative cells."""
import sys
import tempfile
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WS / "scripts"))
from run_s3 import cell                                  # noqa: E402

results = []


def check(name, ok, detail):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def main():
    work = Path(tempfile.mkdtemp(prefix="s3-repro-"))
    # inverted N_c + flat barrier + C1=1 exemplar
    r = cell(24, 3.0, 8, work)
    check("n=24 a=3.0 s=8: Nc=7, B=1, C1=1.0",
          r["n_clusters"] == 7 and r["barrier_median"] == 1
          and r["C1"] == 1.0,
          f"Nc={r['n_clusters']} B={r['barrier_median']} C1={r['C1']}")
    # n=26 first-movement exemplar
    r = cell(26, 4.2, 5, work)
    check("n=26 a=4.2 s=5: B=2 (lift-off), Nc=2",
          r["n_clusters"] == 2 and r["barrier_median"] == 2,
          f"Nc={r['n_clusters']} B={r['barrier_median']} gap={r['min_gap']}")
    # freezing-confound exemplar: big cluster, low frozen
    r = cell(24, 2.0, 1, work)
    check("n=24 a=2.0 s=1: fmax=1, frozen=0",
          r["f_max"] == 1.0 and r["frozen_frac_largest"] == 0.0,
          f"fmax={r['f_max']} frozen={r['frozen_frac_largest']}")
    # high-alpha near-threshold SAT survivor with early freezing
    r = cell(24, 4.267, 10, work)
    check("n=24 a=4.267 s=10: SAT, Nc=8, C1=1.0",
          r["min_V"] == 0 and r["n_clusters"] == 8 and r["C1"] == 1.0,
          f"minV={r['min_V']} Nc={r['n_clusters']} C1={r['C1']}")

    n_ok = sum(results)
    print(f"\n{n_ok}/{len(results)} checks passed")
    sys.exit(0 if n_ok == len(results) else 1)


if __name__ == "__main__":
    main()
