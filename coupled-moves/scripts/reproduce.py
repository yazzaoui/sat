#!/usr/bin/env python3
"""S1 coupled-moves reproduction suite."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
ENGINE = WS / "probes/conductance"
results = []


def check(name, ok, detail):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def main():
    work = Path(tempfile.mkdtemp(prefix="s1-repro-"))
    canon = work / "canon.ext"
    canon.write_text("p ext 3 2\no -1 -2 0\nd 0 3 3 -1 -2 0\n"
                     "d 0 3 -3 1 0\nd 0 3 -3 2 0\ns 1\ns 2\n")

    def succ(s, b):
        r = subprocess.run([str(ENGINE), str(canon), "--succ", str(s), str(b)],
                           capture_output=True, text=True, check=True)
        return json.loads(r.stdout)["succ"]

    # P0 canon conformance (engine-level, parsing included)
    check("canon: staleness persists", succ(4, 0) == 5, f"succ(4,0)={succ(4,0)}")
    check("canon: accidental repair", succ(3, 0) == 2, f"succ(3,0)={succ(3,0)}")
    check("canon: irreversibility", succ(succ(3, 0), 0) == 7,
          f"round-trip={succ(succ(3,0),0)} != 3")

    # Microbenchmark gate (registered >= 1e7 succ/s)
    sys.path.insert(0, str(WS / "scripts"))
    from drive_p1 import emit, arm_b, net, run as erun     # noqa: E402
    import numpy as np                                     # noqa: E402
    db, fb, ntb = arm_b()
    bench = work / "bench.ext"
    emit(bench, db, fb, ntb)
    r = subprocess.run([str(ENGINE), "--bench", str(bench)],
                       capture_output=True, text=True, check=True)
    rate = json.loads(r.stdout)["bench_evals_per_sec"]
    check("microbenchmark gate >= 1e7 succ/s", rate >= 1e7, f"{rate:.2e}")

    # Arm A structural zero + pinned Theorem F identity on arm B
    a = work / "armA.ext"
    emit(a, [], [], 16)
    ja = erun(a)
    base_mask = np.fromfile(f"{a}.mask", dtype=np.uint32)
    ra = net(a, ja, base_mask, 16)
    check("arm A NET == 0 exactly", max(abs(x["net"]) for x in ra) == 0.0,
          "structural self-test")
    b = work / "armB.ext"
    emit(b, db, fb, ntb)
    jb = erun(b)
    rb = net(b, jb, base_mask, ntb)
    gains = {round(x["gain"] * (1 << 25)) for x in rb}
    losses = {x["loss"] for x in rb}
    check("Theorem F identity: gain = 23*511 per solution, loss = 0",
          gains == {11753} and losses == {0.0},
          f"gains={sorted(gains)} losses={sorted(losses)}")
    check("soundness gate active", jb.get("error") is None
          and ja.get("error") is None, "lifts verified in-engine")

    n_ok = sum(results)
    print(f"\n{n_ok}/{len(results)} checks passed")
    sys.exit(0 if n_ok == len(results) else 1)


if __name__ == "__main__":
    main()
