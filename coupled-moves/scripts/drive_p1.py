#!/usr/bin/env python3
"""P1 driver: emit arm instances, run the conductance engine, compute
the exact NET decomposition (corridor_gain / mine_loss) from mask
files. Registered order: bench gate -> arm A self-test -> B, C, D."""
import itertools
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

WS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WS.parent / "landscape-surgery/extvars"))
import controls                                     # noqa: E402

ENGINE = WS / "probes/conductance"
NB = 16                                             # PHP(4,4) base vars


def var(i, j):
    return (i - 1) * 4 + j


def php44_clauses():
    cl = [[var(i, j) for j in range(1, 5)] for i in range(1, 5)]
    for j in range(1, 5):
        for i in range(1, 5):
            for k in range(i + 1, 5):
                cl.append([-var(i, j), -var(k, j)])
    return cl


def solutions_base():
    sols = []
    for perm in itertools.permutations(range(1, 5)):
        s = 0
        for i, j in enumerate(perm, start=1):
            s |= 1 << (var(i, j) - 1)
        sols.append(s)
    return sols


def eval_defs(x_state, defs_fn):
    """defs_fn: list of (zvar, fn(bits)->bool) in DAG order."""
    s = x_state
    for zv, fn in defs_fn:
        if fn(s):
            s |= 1 << (zv - 1)
    return s


def emit(path, defs_clauses, defs_fn, n_total):
    sols = solutions_base()
    with open(path, "w") as f:
        f.write(f"p ext {n_total} {NB}\n")
        for c in php44_clauses():
            f.write("o " + " ".join(map(str, c)) + " 0\n")
        for layer, owner, lits in defs_clauses:
            f.write(f"d {layer} {owner} " + " ".join(map(str, lits)) + " 0\n")
        for s in sols:
            f.write(f"s {eval_defs(s, defs_fn)}\n")


def bit(s, v):
    return (s >> (v - 1)) & 1


def lit_val(s, l):
    return bit(s, abs(l)) if l > 0 else 1 - bit(s, abs(l))


def arm_b():
    """Cook-schema layer over the square grid: z_ij = x_ij | (x_i4 & x_4j)."""
    defs, fns = [], []
    zv = NB
    for i in range(1, 4):
        for j in range(1, 4):
            zv += 1
            a, b, c = var(i, j), var(i, 4), var(4, j)
            defs += [(0, zv, [zv, -a]), (0, zv, [zv, -b, -c]),
                     (0, zv, [-zv, a, b]), (0, zv, [-zv, a, c])]
            fns.append((zv, lambda s, a=a, b=b, c=c:
                        bit(s, a) or (bit(s, b) and bit(s, c))))
    return defs, fns, zv


def arm_c():
    cl = php44_clauses()
    raw, nv, report = controls.bva_definitions(NB, cl, 9)
    defs, fns = [], []
    # raw is triples per definition: (-z,l1,l2),(z,-l1),(z,-l2)
    for t in range(0, len(raw), 3):
        z = -raw[t][0]
        l1, l2 = raw[t][1], raw[t][2]
        defs += [(0, z, raw[t]), (0, z, raw[t + 1]), (0, z, raw[t + 2])]
        fns.append((z, lambda s, l1=l1, l2=l2:
                    bool(lit_val(s, l1) or lit_val(s, l2))))
    return defs, fns, nv, report


def arm_d(seed):
    raw, nv = controls.random_definitions(NB, [9], seed)
    defs, fns = [], []
    for t in range(0, len(raw), 4):
        z = raw[t][0]
        a, bq, cq = -raw[t][1], -raw[t + 1][1], -raw[t + 1][2]
        defs += [(0, z, raw[t]), (0, z, raw[t + 1]),
                 (0, z, raw[t + 2]), (0, z, raw[t + 3])]
        fns.append((z, lambda s, a=a, b=bq, c=cq:
                    bool(lit_val(s, a) or (lit_val(s, b) and lit_val(s, c)))))
    return defs, fns, nv


def run(path):
    r = subprocess.run([str(ENGINE), str(path)], capture_output=True,
                       text=True, check=True)
    return json.loads(r.stdout)


def net(coupled_path, coupled_out, base_mask, n_total):
    cm = np.fromfile(f"{coupled_path}.mask", dtype=np.uint32)
    xs = np.arange(1 << n_total, dtype=np.uint32) & 0xFFFF
    bm = base_mask[xs]
    res = []
    for k in range(24):
        cb = (cm >> k) & 1
        bb = (bm >> k) & 1
        gain = float(np.mean((cb == 1) & (bb == 0)))
        loss = float(np.mean((cb == 0) & (bb == 1)))
        res.append({"sol": k, "gain": gain, "loss": loss,
                    "net": gain - loss})
    return res


def main(out_dir):
    out = Path(out_dir)
    out.mkdir(exist_ok=True)
    # Arm A / baseline: no defs.
    a = out / "armA.ext"
    emit(a, [], [], NB)
    ja = run(a)
    base_mask = np.fromfile(f"{a}.mask", dtype=np.uint32)
    ra = net(a, ja, base_mask, NB)
    print("armA self-test: max|NET| =",
          max(abs(r["net"]) for r in ra), flush=True)
    results = {"A": {"engine": ja, "net": ra}}

    db, fb, ntb = arm_b()
    b = out / "armB.ext"
    emit(b, db, fb, ntb)
    jb = run(b)
    results["B"] = {"engine": jb, "net": net(b, jb, base_mask, ntb)}
    print("armB done", flush=True)

    dc_, fc, ntc, report = arm_c()
    if fc:
        c = out / "armC.ext"
        emit(c, dc_, fc, ntc)
        jc = run(c)
        results["C"] = {"engine": jc, "net": net(c, jc, base_mask, ntc),
                        "bva_report": report}
    else:
        results["C"] = {"degenerate": True, "bva_report": report}
    print("armC done:", report, flush=True)

    for seed in (1, 2, 3):
        dd, fd, ntd = arm_d(seed)
        d = out / f"armD{seed}.ext"
        emit(d, dd, fd, ntd)
        jd = run(d)
        results[f"D{seed}"] = {"engine": jd,
                               "net": net(d, jd, base_mask, ntd)}
        print(f"armD seed {seed} done", flush=True)

    summary = {}
    for arm, r in results.items():
        if "net" in r:
            summary[arm] = {
                "mean_net": sum(x["net"] for x in r["net"]) / 24,
                "mean_gain": sum(x["gain"] for x in r["net"]) / 24,
                "mean_loss": sum(x["loss"] for x in r["net"]) / 24,
                "n_terminal": r["engine"]["n_terminal"]}
    print(json.dumps(summary, indent=1))
    (WS / "docs/P1-results-data.json").write_text(
        json.dumps({"results": results, "summary": summary}, indent=1))
    print("wrote docs/P1-results-data.json")


if __name__ == "__main__":
    main(sys.argv[1])
