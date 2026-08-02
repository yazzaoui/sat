#!/usr/bin/env python3
"""Vertical slice (Phase 2 step 2): counting-structure block-swap templates.

Pipeline, fully blind to the generator:
  1. structure.py overlay on the DIMACS: exactly/at-most-one column blocks
     (holes) + covering positive rows (pigeons) => the counting grid.
  2. Template: inversion-ban clauses (¬x[a][l] ∨ ¬x[b][k]) for row pairs
     a<b and column pairs k<l, witness = the 4-literal block swap
     {¬x[a][l], x[a][k], ¬x[b][k], x[b][l]} — the exchange-cycle pattern
     the M1 atlas found at every PHP size.
  3. Every proposal passes the poly-time PR check (pr_check.py) against the
     formula accumulated so far; rejected proposals are dropped.
  4. Accepted clauses are emitted as a PR proof head (dpr format: clause,
     then witness beginning with the clause's first literal) and appended
     to the CNF handed to CaDiCaL; CaDiCaL's DRAT refutation is
     concatenated after the PR head and the combined proof is verified by
     dpr-trim against the ORIGINAL formula.

Usage: template_php.py <cnf> --out-cnf <path> --out-proof-head <path>
"""
import argparse
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from atlas import load_cnf
from pr_check import is_pr
from structure import find_amo_cliques


def counting_grid(clauses):
    """Recover (rows x cols) grid from structure: cols = AMO cliques,
    rows = positive covering clauses. Returns x[r][c] -> var, or None."""
    cols = [sorted(cl) for cl, _ in find_amo_cliques(clauses)]
    rows = [sorted(c) for c in clauses if all(l > 0 for l in c)]
    if not cols or not rows:
        return None
    col_of = {}
    for j, col in enumerate(cols):
        for v in col:
            col_of[v] = j
    x = []
    for row in rows:
        entry = {}
        for v in row:
            if v not in col_of:
                return None
            entry[col_of[v]] = v
        x.append(entry)
    return x


def propose(clauses, x, log=print):
    """Yield PR-checked inversion bans; mutates clauses by appending."""
    accepted = []
    rows = len(x)
    tried = 0
    for b in range(1, rows):
        for a in range(b):
            cols_a = sorted(x[a])
            cols_b = sorted(x[b])
            for ki, k in enumerate(cols_a):
                for l in cols_b:
                    if l <= k or l not in x[a] or k not in x[b]:
                        continue
                    C = [-x[a][l], -x[b][k]]
                    omega = [-x[a][l], x[a][k], -x[b][k], x[b][l]]
                    tried += 1
                    if is_pr(clauses, C, omega):
                        accepted.append((C, omega))
                        clauses.append(C)
        log(f"row pair block ending at {b}: {len(accepted)} accepted "
            f"of {tried} tried")
    return accepted


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cnf")
    ap.add_argument("--out-cnf", required=True)
    ap.add_argument("--out-proof-head", required=True)
    args = ap.parse_args()

    original = load_cnf(args.cnf)
    clauses = list(original)
    x = counting_grid(clauses)
    if x is None:
        raise SystemExit("no counting grid recovered; template not applicable")
    print(f"grid: {len(x)} rows x {max(len(r) for r in x)} cols")

    accepted = propose(clauses, x)
    print(f"accepted {len(accepted)} PR template clauses")

    nvars = max(abs(l) for c in clauses for l in c)
    with open(args.out_cnf, "w") as f:
        f.write(f"p cnf {nvars} {len(clauses)}\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")
    with open(args.out_proof_head, "w") as f:
        for C, omega in accepted:
            assert omega[0] == C[0]
            f.write(" ".join(map(str, C + omega)) + " 0\n")


if __name__ == "__main__":
    main()
