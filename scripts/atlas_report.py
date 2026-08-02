#!/usr/bin/env python3
"""Aggregate witness atlas over all collected event logs (M1 deliverable).

Scans benchmarks/results/*.events.jsonl, pairs each with its CNF, computes
per-instance witness statistics plus interaction-graph diameter (double-sweep
lower bound), and writes docs/witness-atlas.md.
"""
import re
import statistics
from collections import Counter, deque
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from atlas import analyze, interaction_graph, load_cnf

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "benchmarks/results"
CNF = ROOT / "benchmarks/cnf"


def diameter_lb(adj):
    def ecc(src):
        dist = {src: 0}
        q = deque([src])
        far = src
        while q:
            u = q.popleft()
            for v in adj.get(u, ()):
                if v not in dist:
                    dist[v] = dist[u] + 1
                    q.append(v)
                    far = v
        return dist[far], far

    v0 = next(iter(adj))
    _, far = ecc(v0)
    d, _ = ecc(far)
    return d


def med(vals):
    vals = [v for v in vals if v is not None]
    return statistics.median(vals) if vals else None


def mx(vals):
    vals = [v for v in vals if v is not None]
    return max(vals) if vals else None


def main():
    rows = []
    for events_path in sorted(RESULTS.glob("*.events.jsonl")):
        name = events_path.name.replace(".events.jsonl", "")
        cnf_path = CNF / f"{name}.cnf"
        if not cnf_path.exists():
            print(f"skip {name}: no CNF")
            continue
        events, wits, n_attempts = analyze(events_path, cnf_path)
        adj = interaction_graph(load_cnf(cnf_path))
        m = re.match(r"([a-z]+)(\d+)", name)
        rows.append({
            "family": m.group(1), "size": int(m.group(2)),
            "vars": len(adj), "diam": diameter_lb(adj),
            "attempts": n_attempts, "accepts": len(wits),
            "acc_rate": f"{100 * len(wits) / max(n_attempts, 1):.0f}%",
            "med_foot": med([w["footprint"] for w in wits]),
            "med_flip": med([w["flipped"] for w in wits]),
            "med_rad": med([w["radius"] for w in wits]),
            "max_rad": mx([w["radius"] for w in wits]),
            "null_rad": med([w["null_radius"] for w in wits]),
            "below_null": (
                f"{100 * statistics.mean([w['radius'] < w['null_radius'] for w in wits if w['radius'] is not None and w['null_radius'] is not None]):.0f}%"
                if wits else "-"),
            "patterns": dict(sorted(
                Counter(w["pattern"] for w in wits).items(),
                key=lambda kv: -kv[1])),
        })
        print(f"done {name}")

    rows.sort(key=lambda r: (r["family"], r["size"]))
    cols = ["family", "size", "vars", "diam", "attempts", "accepts",
            "acc_rate", "med_foot", "med_flip", "med_rad", "max_rad",
            "null_rad", "below_null", "patterns"]
    lines = [
        "# Witness atlas (M1)",
        "",
        "Per-instance witness statistics from SaDiCaL `--eventlog` runs.",
        "`diam` = interaction-graph diameter (double-sweep lower bound);",
        "`med_rad`/`max_rad` = BFS distance of flipped variables from the",
        "banned-clause variables — the locality measure. `med_foot` = median",
        "witness footprint (#vars); `med_flip` = median #flipped literals.",
        "`null_rad` = median radius of random variable sets of the same size",
        "as the flipped set (50 samples/witness, seed 0); `below_null` = share",
        "of witnesses strictly below their own null median. Locality is only",
        "claimed where true radius sits well below null.",
        "",
        "| " + " | ".join(cols) + " |",
        "|" + "|".join("---" for _ in cols) + "|",
    ]
    for r in rows:
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    out = ROOT / "docs/witness-atlas.md"
    out.write_text("\n".join(lines) + "\n")
    print(f"\nwrote {out}")
    print("\n".join(lines[7:]))


if __name__ == "__main__":
    main()
