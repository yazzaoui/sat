#!/usr/bin/env python3
"""S5 proof-space: reproduce every number behind the stream's claims.

Fast suite (default, ~2 min): P0 disqualification/selection numbers,
the generator identity, all six fast gate cells via the C probe,
C-vs-Python cross-validation, and the mechanical application of the
registered gate rule (docs/P1-registration.md).

  python3 scripts/reproduce.py            # fast suite
  python3 scripts/reproduce.py --slow     # + PHP(5) T0 w=4 baseline
                                          #   (~10 min) and the
                                          #   decision-cell growth
                                          #   measurement (~6 min)

Build the probe first:  cc -O3 -o probes/depthdp probes/depthdp.c
Run from proof-space/.
"""

import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PROBE = os.path.join(ROOT, "probes", "depthdp")
sys.path.insert(0, HERE)

from p0_feasibility import php_clauses, candidate1_bfs, depth_dp
from cook_cascade import cook_cascade_axioms, write_dimacs

checks = []


def check(name, ok, detail=""):
    checks.append(ok)
    print("%-4s %s%s" % ("PASS" if ok else "FAIL", name,
                         (" — " + detail) if detail else ""))


def probe(width, cnf, *extra):
    out = subprocess.run([PROBE, "--width", str(width), cnf, *extra],
                         capture_output=True, text=True).stdout
    return json.loads(out.splitlines()[-1])


def gen(p, t0=False):
    f = tempfile.NamedTemporaryFile(suffix=".cnf", delete=False)
    f.close()
    _, base = php_clauses(p)
    if t0:
        write_dimacs(f.name, p * (p - 1), base)
    else:
        nv, ax = cook_cascade_axioms(p)
        write_dimacs(f.name, nv, base + ax)
    return f.name


slow = "--slow" in sys.argv

# ---- P0: candidate disqualification / selection numbers ----------------
counts, _ = candidate1_bfs(3, max_depth=3)
check("P0 candidate-1 state explosion at PHP(3): 1/12/102/682",
      counts == [1, 12, 102, 682], str(counts))

bot, _, na, _ = depth_dp(6, php_clauses(3)[1])
check("P0 PHP(3) T0 unbounded: depth(bottom)=4, antichain 61",
      bot == 4 and na == 61, "depth=%s antichain=%s" % (bot, na))

# ---- generator identity: the committed decision-cell CNF ---------------
tf5 = gen(5)
committed = os.path.join(ROOT, "data", "php5_cook.cnf")
check("cook_cascade.py reproduces data/php5_cook.cnf byte-for-byte",
      open(tf5).read() == open(committed).read())

# ---- the six fast gate cells (C probe, exact JSON) ---------------------
EXPECT = {
    ("t0", 4, 3): {"depth": 8, "antichain": 801, "geodesic_size": 641},
    ("t0", 4, 4): {"depth": 7, "antichain": 1431, "geodesic_size": 1031},
    ("tf", 4, 3): {"depth": 7, "antichain": 2443, "geodesic_size": 1207},
    ("tf", 4, 4): {"depth": 7, "antichain": 6622, "geodesic_size": 3240},
    ("t0", 5, 3): {"depth": -1, "antichain": 45, "geodesic_size": 0},
    ("tf", 5, 3): {"depth": -1, "antichain": 1181, "geodesic_size": 0},
}
got = {}
for (arm, p, w), exp in EXPECT.items():
    cnf = gen(p, t0=(arm == "t0"))
    j = probe(w, cnf)
    got[(arm, p, w)] = j
    ok = all(j[k] == v for k, v in exp.items())
    check("gate cell %s PHP(%d) w=%d" % (arm.upper(), p, w), ok, json.dumps(
        {k: j[k] for k in ("depth", "antichain", "geodesic_size")}))
    os.unlink(cnf)

# ---- C == Python cross-validation (shared cheap cell) ------------------
bot_py, _, _, _ = depth_dp(12, php_clauses(4)[1], w=3)
check("C == Python on T0 PHP(4) w=3 (depth)",
      bot_py == got[("t0", 4, 3)]["depth"], "python depth=%s" % bot_py)

# ---- the registered gate rule, applied mechanically --------------------
# Q1 (depth of bottom): pass = predicted-sign separation >= 20%
q1_w3 = (got[("t0", 4, 3)]["depth"] - got[("tf", 4, 3)]["depth"]) \
    / got[("t0", 4, 3)]["depth"]
q1_w4 = (got[("t0", 4, 4)]["depth"] - got[("tf", 4, 4)]["depth"]) \
    / got[("t0", 4, 4)]["depth"]
check("gate Q1 fails at PHP(4): max separation 12.5%% < 20%%",
      abs(q1_w3 - 0.125) < 1e-9 and q1_w4 == 0,
      "w3=%.3f w4=%.3f" % (q1_w3, q1_w4))

# Q2 (geodesic size): predicted sign = Cook SMALLER; measured LARGER
r3 = got[("tf", 4, 3)]["geodesic_size"] / got[("t0", 4, 3)]["geodesic_size"]
r4 = got[("tf", 4, 4)]["geodesic_size"] / got[("t0", 4, 4)]["geodesic_size"]
check("gate Q2 wrong-sign at PHP(4): geodesic 1.9x / 3.1x LARGER",
      abs(r3 - 1207 / 641) < 1e-9 and abs(r4 - 3240 / 1031) < 1e-9,
      "w3=%.2fx w4=%.2fx" % (r3, r4))

# width-relief annotation (ledger entry 10): at PHP(5) w=3 BOTH close
check("width-relief claim fails: PHP(5) w=3 closes for T0 AND T_Cook "
      "(45 vs 1181, no bottom either side)",
      got[("t0", 5, 3)]["depth"] == -1 and got[("tf", 5, 3)]["depth"] == -1
      and got[("tf", 5, 3)]["antichain"] == 1181)

# ---- slow cells --------------------------------------------------------
if slow:
    t05 = gen(5, t0=True)
    j = probe(4, t05)
    check("PHP(5) T0 w=4 baseline: depth 13, antichain 13011, "
          "geodesic 8296",
          j["depth"] == 13 and j["antichain"] == 13011
          and j["geodesic_size"] == 8296, json.dumps(j))
    os.unlink(t05)

    # decision-cell infeasibility: front growth through 5 forward rounds
    st = tempfile.NamedTemporaryFile(suffix=".bin", delete=False)
    st.close()
    os.unlink(st.name)
    out = subprocess.run(
        [PROBE, "--width", "4", committed, "--state", st.name,
         "--rounds", "5", "--geo-levels", "0"],
        capture_output=True, text=True).stdout
    j = json.loads(out.splitlines()[-1])
    check("decision cell T_Cook PHP(5) w=4: nd=144749 after round 5, "
          "no bottom (growth measured, cell out of exact reach)",
          j.get("nd") == 144749 and j.get("bottom") == -1, out.strip())
    os.unlink(st.name)
else:
    print("skip PHP(5) w=4 cells (rerun with --slow, ~16 min)")

os.unlink(tf5)
print("\n%d/%d checks passed" % (sum(checks), len(checks)))
sys.exit(0 if all(checks) else 1)
