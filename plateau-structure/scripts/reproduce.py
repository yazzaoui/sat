#!/usr/bin/env python3
"""S2 reproduction suite: pinned representative cells."""
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WS / "scripts"))
sys.path.insert(0, str(WS.parent / "landscape-surgery/extvars"))
import cook                                             # noqa: E402
import plateau_tools as T                               # noqa: E402
from run_s2 import php_nn, r3, alts_for                 # noqa: E402

results = []


def check(name, ok, detail):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def main():
    n, cl = cook.php_clauses(4)
    states, V = T.level_states(n, cl, 1)
    alts = alts_for(states, n, cl, V)
    got = {c: T.merge_tree_leaves(states, alts[c], n)[0]
           for c in ("exposure", "critical", "decidedness", "mobility")}
    check("S2a php4 leaves (24,24,1,36)",
          (got["exposure"], got["critical"], got["decidedness"],
           got["mobility"]) == (24, 24, 1, 36), str(got))
    check("S2a control inversion on php4",
          got["mobility"] > max(got["exposure"], got["critical"],
                                got["decidedness"]), "mobility dominates")

    n, cl = php_nn(4)
    states, V = T.level_states(n, cl, 1)
    exits = T.exit_states(states, n, V)
    dist = T.bfs_exit_distance(states, exits, n)
    covered = [s for s in states if s in dist]
    alts = alts_for(states, n, cl, V)
    rho = T.spearman([float(alts["decidedness"][s]) for s in covered],
                     [dist[s] for s in covered])
    check("S2b php44 decidedness rho ~ -0.8247", abs(rho + 0.8247) < 1e-3,
          f"rho={rho:.4f}")
    blind, _, _ = T.hitting_time(states, exits, n, T.make_step(states, n))
    ht, _, trap = T.hitting_time(states, exits, n,
                                 T.make_step(states, n,
                                             alts["decidedness"], -1))
    ratio = blind / ht
    check("S2b php44 decidedness ratio ~1.346 (< 2x bar)",
          abs(ratio - 1.346) < 5e-3 and trap == 0, f"ratio={ratio:.3f}")

    n, cl = r3(8)
    states, V = T.level_states(n, cl, 1)
    exits = T.exit_states(states, n, V)
    alts = alts_for(states, n, cl, V)
    ht, _, trap = T.hitting_time(states, exits, n,
                                 T.make_step(states, n, alts["exposure"], 1))
    check("S2b r3_8 exposure traps ~49% despite rho=+0.54",
          ht == float("inf") and abs(trap - 0.4894) < 1e-3,
          f"trapped={trap:.4f}")

    n_ok = sum(results)
    print(f"\n{n_ok}/{len(results)} checks passed")
    sys.exit(0 if n_ok == len(results) else 1)


if __name__ == "__main__":
    main()
