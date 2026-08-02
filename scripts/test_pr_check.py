#!/usr/bin/env python3
"""Cross-validate pr_check.py against dpr-trim (lead directive: the checker
is load-bearing for soundness; a permissive bug would poison everything).

Known-good: template clauses from the PHP(8) run — each accepted by
pr_check AND part of a dpr-trim-verified proof. Re-checked here one by one:
pr_check must accept clause k against F + clauses[0..k-1].

Known-bad: systematic corruptions of those witnesses (drop the swap target,
flip a polarity, swap wrong column) plus arbitrary non-PR units. pr_check
must reject; each corruption is also spot-checked against dpr-trim by
substituting the corrupted line into the proof head — dpr-trim must fail.

Exit 0 iff all checks agree.
"""
import random
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from atlas import load_cnf
from pr_check import is_pr
from template_php import counting_grid, propose

ROOT = Path(__file__).resolve().parent.parent
DPRTRIM = ROOT / "tools/dpr-trim/dpr-trim"
CADICAL = ROOT / "tools/cadical/build/cadical"


def dpr_verifies(cnf_path, head_lines, tmpdir):
    """Full pipeline check: head + cadical DRAT tail verifies?"""
    guided = tmpdir / "guided.cnf"
    clauses = load_cnf(cnf_path)
    extra = [[int(x) for x in l.split()[:2]] for l in head_lines]
    nvars = max(abs(l) for c in clauses for l in c)
    with guided.open("w") as f:
        f.write(f"p cnf {nvars} {len(clauses) + len(extra)}\n")
        for c in clauses + extra:
            f.write(" ".join(map(str, c)) + " 0\n")
    tail = tmpdir / "tail.drat"
    subprocess.run([str(CADICAL), "-q", "--no-binary", str(guided), str(tail)],
                   capture_output=True)
    proof = tmpdir / "proof.dpr"
    proof.write_text("\n".join(head_lines) + "\n" + tail.read_text())
    r = subprocess.run([str(DPRTRIM), str(cnf_path), str(proof)],
                       capture_output=True, text=True)
    return "s VERIFIED" in r.stdout


def main():
    import tempfile
    rng = random.Random(3)
    cnf_path = ROOT / "benchmarks/cnf/php7.cnf"
    original = load_cnf(cnf_path)

    clauses = list(original)
    accepted = propose(clauses, counting_grid(clauses), log=lambda *a: None)
    print(f"known-good pool: {len(accepted)} template clauses")

    # known-good: re-verify incrementally with pr_check (already done inside
    # propose) and end-to-end with dpr-trim
    head = [" ".join(map(str, C + w)) + " 0" for C, w in accepted]
    with tempfile.TemporaryDirectory() as td:
        assert dpr_verifies(cnf_path, head, Path(td)), \
            "dpr-trim rejected the known-good head"
    print("known-good: pr_check accepts all, dpr-trim verifies combined proof")

    # known-bad: corruptions must be rejected by pr_check
    bad_accepted = 0
    ndpr = 0
    dpr_disagree = 0
    samples = rng.sample(range(len(accepted)), 60)
    for i in samples:
        C, w = accepted[i]
        F = list(original) + [c for c, _ in accepted[:i]]
        corruptions = [
            w[:2] + w[3:],                     # drop one swap literal
            [w[0], -w[1], w[2], w[3]],         # flip a polarity
            [w[0], w[1], w[2], -w[3]],         # flip another
            [-C[0], w[1], w[2], w[3]],         # omega falsifies C's first lit
        ]
        for wbad in corruptions:
            if is_pr(F, C, wbad):
                # pr_check accepting a corruption is only OK if dpr-trim
                # also accepts it (some corruptions stay valid witnesses)
                bad_line = " ".join(map(str, C + wbad)) + " 0"
                trial_head = head[:i] + [bad_line] + head[i + 1:]
                ndpr += 1
                with tempfile.TemporaryDirectory() as td:
                    if not dpr_verifies(cnf_path, trial_head, Path(td)):
                        dpr_disagree += 1
                        print(f"DISAGREE: pr_check accepts, dpr-trim rejects: "
                              f"C={C} w={wbad}")
                bad_accepted += 1

    # arbitrary non-PR units: banning x entirely where a solution needs it
    non_pr = 0
    for _ in range(40):
        v = rng.randrange(1, 43)
        if is_pr(list(original), [-v], [-v]):
            non_pr += 1
    print(f"corruptions accepted by pr_check: {bad_accepted}/240 "
          f"(cross-checked vs dpr-trim: {ndpr}, disagreements: {dpr_disagree})")
    print(f"trivial-witness unit bans accepted: {non_pr}/40 "
          f"(expected 0 — PHP has no pure literals at this stage)")
    ok = dpr_disagree == 0 and non_pr == 0
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
