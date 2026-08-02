#!/usr/bin/env python3
"""S2 execution: S2a structure + S2b screen + amended S2b dynamics.
One run per cell, menu frozen, bars per registration + amendment 1."""
import json
import random
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WS / "scripts"))
sys.path.insert(0, str(WS.parent / "landscape-surgery/extvars"))
import cook                                             # noqa: E402
import plateau_tools as T                               # noqa: E402

CANDS = ("exposure", "critical", "decidedness", "mobility")


def php_nn(nn):
    h = nn
    var = lambda i, j: (i - 1) * h + j                  # noqa: E731
    cl = [[var(i, j) for j in range(1, h + 1)] for i in range(1, nn + 1)]
    for j in range(1, h + 1):
        for i in range(1, nn + 1):
            for k in range(i + 1, nn + 1):
                cl.append([-var(i, j), -var(k, j)])
    return nn * h, cl


def r3(seed, n=24, m=96):
    rng = random.Random(seed)
    cl = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), 3)
        cl.append([v * rng.choice((1, -1)) for v in vs])
    return n, cl


def alts_for(states, n, cl, V):
    return {
        "exposure": {s: T.exposure(s, cl) for s in states},
        "critical": {s: T.critical(s, cl) for s in states},
        "decidedness": {s: T.decidedness(s, cl) for s in states},
        "mobility": {s: T.mobility(s, cl, n, V) for s in states},
    }


def main():
    out = {"S2a": {}, "S2b": {}}

    s2a = [("php4", *cook.php_clauses(4)),
           ("php5", *cook.php_clauses(5))] + \
          [(f"r3_{s}", *r3(s)) for s in (3, 4, 7, 9)]
    for name, n, cl in s2a:
        states, V = T.level_states(n, cl, 1)
        alts = alts_for(states, n, cl, V)
        row = {"level_size": len(states)}
        for cand in CANDS:
            leaves, ncomp = T.merge_tree_leaves(states, alts[cand], n)
            row[cand] = {"leaves": leaves, "components": ncomp}
        ctrl = row["mobility"]["leaves"]
        for cand in CANDS[:3]:
            L = row[cand]["leaves"]
            row[cand]["structured"] = bool(L >= 3 and L >= 2 * ctrl)
        out["S2a"][name] = row
        print(f"S2a {name}: size={len(states)} " +
              " ".join(f"{c}={row[c]['leaves']}" for c in CANDS), flush=True)

    s2b = [("php44", *php_nn(4)), ("php55", *php_nn(5))] + \
          [(f"r3_{s}", *r3(s)) for s in (1, 2, 5, 6, 8, 10)]
    for name, n, cl in s2b:
        states, V = T.level_states(n, cl, 1)
        exits = T.exit_states(states, n, V)
        dist = T.bfs_exit_distance(states, exits, n)
        covered = [s for s in states if s in dist]
        alts = alts_for(states, n, cl, V)
        row = {"level_size": len(states), "exits": len(exits),
               "unreachable_mass": 1 - len(covered) / len(states)}
        ds = [dist[s] for s in covered]
        for cand in CANDS:
            xs = [float(alts[cand][s]) for s in covered]
            row[cand] = {"rho": round(T.spearman(xs, ds), 4)}
        # dynamics (amendment 1): all candidates + control, direction by sign
        blind, um, btrap = T.hitting_time(states, exits, n,
                                          T.make_step(states, n))
        row["blind_hit"] = round(blind, 3)
        for cand in CANDS:
            rho = row[cand]["rho"]
            direction = 1 if rho > 0 else -1
            # descend toward exits: exits have distance 0; if rho>0 (V2
            # high far from exits) walker seeks LOWER V2 -> direction +1
            step = T.make_step(states, n, alts[cand], direction)
            ht, _, trap = T.hitting_time(states, exits, n, step)
            row[cand]["hit"] = None if ht == float("inf") else round(ht, 3)
            row[cand]["trapped_mass"] = round(trap, 4)
            row[cand]["ratio"] = (0.0 if ht == float("inf")
                                  else round(blind / ht, 3) if ht > 0 else None)
        out["S2b"][name] = row
        print(f"S2b {name}: size={len(states)} exits={len(exits)} "
              f"blind={row['blind_hit']} " +
              " ".join(f"{c}:rho={row[c]['rho']},x{row[c]['ratio']}"
                       for c in CANDS), flush=True)

    (WS / "docs/S2-results-data.json").write_text(json.dumps(out, indent=1))
    print("wrote docs/S2-results-data.json")


if __name__ == "__main__":
    main()
