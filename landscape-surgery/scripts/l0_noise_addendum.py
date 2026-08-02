#!/usr/bin/env python3
"""L0 addendum: estimator measurement noise at final parameters.
Fixed instances (generator seeds 1-2 per family), probe seeds 1-8.
L0 coupled gen/probe seeds, confounding instance variability with
estimator noise; effect-size bars must derive from the latter (lead
directive). Appends 'estimator_noise' to L0-results-data.json."""
import json, statistics, sys
from pathlib import Path
WS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WS / "probes"))
import probes as P, xor_tools as X

FINAL_R = {0.7: 200, 0.9: 500}
out = {}
for n in (40, 60):
    for d in (0.7, 0.9):
        cvs = []
        for gseed in (1, 2):
            rows = X.gen_xor(n, round(d * n), 3, gseed)
            clauses = X.xor_to_cnf(n, rows)
            ests = [P.basin_sample(n, clauses, R=FINAL_R[d], seed=ps)["basins_est"]
                    for ps in range(1, 9)]
            mean = statistics.mean(ests)
            sd = statistics.stdev(ests)
            cvs.append({"gen_seed": gseed, "mean": mean, "sd": round(sd, 2),
                        "cv": round(sd / mean, 4) if mean else None,
                        "estimates": ests})
            print(f"n={n} d={d} gseed={gseed}: mean={mean:.1f} sd={sd:.2f} "
                  f"cv={sd/mean:.3f}", flush=True)
        out[f"{n}/{d}"] = cvs
data_file = WS / "docs/L0-results-data.json"
data = json.loads(data_file.read_text())
data["summary"]["estimator_noise"] = {"final_R": FINAL_R, "families": out}
data_file.write_text(json.dumps(data, indent=1))
print("updated", data_file)
