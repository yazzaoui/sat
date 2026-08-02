#!/usr/bin/env python3
"""Amortization feasibility (lead directive): quantify overlap between
consecutive positive reducts, from existing event logs — no solver runs.

Reducts are reconstructed as the UNFILTERED positive reduct (for each
formula clause satisfied by the trail: its assigned literals, plus the
negated-decisions clause). SaDiCaL's filtered reduct drops a subset of
these; shared-structure fractions on the unfiltered version are an upper
bound on cost but a faithful proxy for shared structure. Caveat recorded.

Usage: reduct_overlap.py <events.jsonl> <cnf> [--lags 1 2 5 10]
"""
import argparse
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from atlas import load_cnf


def reduct_signature(clauses, trail_set, decisions):
    """Frozenset of reduced-clause tuples + the banned clause."""
    sig = set()
    for ci, c in enumerate(clauses):
        assigned = []
        satisfied = False
        for l in c:
            if l in trail_set:
                satisfied = True
                assigned.append(l)
            elif -l in trail_set:
                assigned.append(l)
        if satisfied:
            sig.add((ci, tuple(assigned)))
    sig.add(("banned", tuple(sorted(-d for d in decisions))))
    return sig


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("events")
    ap.add_argument("cnf")
    ap.add_argument("--lags", type=int, nargs="+", default=[1, 2, 5, 10])
    args = ap.parse_args()

    clauses = load_cnf(args.cnf)
    attempts = [e for e in (json.loads(l) for l in open(args.events))
                if e["ev"] == "attempt"]
    print(f"{args.events}: {len(attempts)} attempts, {len(clauses)} clauses")

    sigs, vars_, trails = [], [], []
    for a in attempts:
        tset = set(a["trail"])
        sigs.append(reduct_signature(clauses, tset, a["decisions_lits"]))
        vars_.append({abs(l) for l in a["trail"]})
        trails.append(tset)

    for lag in args.lags:
        cl_ov, var_ov, tdelta = [], [], []
        for i in range(len(sigs) - lag):
            a, b = sigs[i], sigs[i + lag]
            cl_ov.append(len(a & b) / max(len(a), 1))
            va, vb = vars_[i], vars_[i + lag]
            var_ov.append(len(va & vb) / max(len(va | vb), 1))
            tdelta.append(len(trails[i] ^ trails[i + lag]))
        print(f"lag {lag:>3}: shared-clause frac med={statistics.median(cl_ov):.2f} "
              f"mean={statistics.mean(cl_ov):.2f} p10={sorted(cl_ov)[len(cl_ov)//10]:.2f} | "
              f"var-overlap med={statistics.median(var_ov):.2f} | "
              f"trail-delta med={statistics.median(tdelta):.0f} lits")


if __name__ == "__main__":
    main()
