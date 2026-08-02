#!/usr/bin/env python3
"""S3 bar application: six registered signatures from S3-results-data."""
import json
import statistics
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WS.parent / "plateau-structure/scripts"))
from plateau_tools import spearman                      # noqa: E402

ALPHAS = (2.0, 3.0, 3.5, 3.86, 4.0, 4.1, 4.2, 4.267)
SHATTER = (3.86, 4.0, 4.1, 4.2)
NS = (16, 20, 24)


def med(cells, key):
    v = [c[key] for c in cells if c.get(key) is not None]
    return statistics.median(v) if v else None


def main():
    data = json.loads((WS / "docs/S3-results-data.json").read_text())
    cells = data["cells"]
    sat = [c for c in cells if c["min_V"] == 0]
    grid = {}
    for n in NS + (26,):
        for a in ALPHAS:
            cs = [c for c in sat if c["n"] == n and c["alpha"] == a]
            if cs:
                grid[(n, a)] = {
                    "n_sat": len(cs),
                    "f_max": med(cs, "f_max"),
                    "n_clusters": med(cs, "n_clusters"),
                    "min_gap": med(cs, "min_gap"),
                    "frozen": med(cs, "frozen_frac_largest"),
                    "barrier": med(cs, "barrier_median"),
                    "C1": med(cs, "C1"),
                }
    print("per-(n,alpha) medians over SAT seeds:")
    for n in NS + (26,):
        for a in ALPHAS:
            g = grid.get((n, a))
            if g:
                print(f"  n={n} a={a}: sat={g['n_sat']}/10 fmax={g['f_max']} "
                      f"Nc={g['n_clusters']} gap={g['min_gap']} "
                      f"frozen={g['frozen']:.3f} B={g['barrier']} C1={g['C1']}")

    def trend(n, key, lo=None):
        xs, ys = [], []
        for a in ALPHAS:
            if lo and a < lo:
                continue
            g = grid.get((n, a))
            if g and g[key] is not None:
                xs.append(a)
                ys.append(g[key])
        return round(spearman(xs, ys), 3) if len(xs) >= 4 else None

    print("\nSIGNATURES:")
    # 1 f_max
    s1a = all(grid[(n, a)]["f_max"] >= 0.9
              for n in NS for a in (2.0, 3.0) if (n, a) in grid)
    s1b = {n: trend(n, "f_max") for n in NS}
    shat_trend_n = []
    for a in SHATTER:
        col = [grid[(n, a)]["f_max"] for n in NS if (n, a) in grid]
        shat_trend_n.append(all(col[i+1] <= col[i] + 1e-9
                                for i in range(len(col)-1)))
    s1 = s1a and all(v is not None and v <= -0.5 for v in s1b.values())
    print(f"1 f_max: low-alpha>=0.9={s1a} alpha-trends={s1b} "
          f"n-noninc-per-shattered-alpha={shat_trend_n} -> "
          f"{'CLEAR' if s1 else 'FAIL'}")
    # 2 N_c
    s2b = {n: trend(n, "n_clusters", lo=3.0) for n in NS}
    ncol = {a: [grid[(n, a)]["n_clusters"] for n in NS if (n, a) in grid]
            for a in SHATTER}
    s2n = all(c[-1] > c[0] for c in ncol.values() if len(c) == 3)
    s2 = all(v is not None and v >= 0.5 for v in s2b.values()) and s2n
    print(f"2 N_c: alpha-trends={s2b} n-increase={ {a: c for a, c in ncol.items()} } "
          f"-> {'CLEAR' if s2 else 'FAIL'}")
    # 3 separation
    gaps = {(n, a): grid[(n, a)]["min_gap"] for n in NS for a in SHATTER
            if (n, a) in grid}
    s3a_ = all(g is None or g >= 2 for g in gaps.values())
    gn = {a: [grid[(n, a)]["min_gap"] for n in NS
              if (n, a) in grid and grid[(n, a)]["min_gap"] is not None]
          for a in SHATTER}
    print(f"3 separation: gaps={gaps} -> {'CLEAR' if s3a_ else 'FAIL'} "
          f"(g/n trend data: {gn})")
    # 4 freezing
    frz_lo = max(grid[(n, a)]["frozen"] for n in NS
                 for a in ALPHAS if a <= 4.0 and (n, a) in grid)
    frz_hi = {(n, a): grid[(n, a)]["frozen"] for n in NS
              for a in (4.2, 4.267) if (n, a) in grid}
    s4 = frz_lo < 0.05
    print(f"4 freezing: max median frozen alpha<=4.0 = {frz_lo:.3f} "
          f"(bar <0.05) high-alpha={ {k: round(v,3) for k,v in frz_hi.items()} } "
          f"-> {'CLEAR' if s4 else 'FAIL'}")
    # 5 barriers
    s5b = {n: trend(n, "barrier") for n in NS}
    bcol = {a: [grid[(n, a)]["barrier"] for n in NS
                if (n, a) in grid and grid[(n, a)]["barrier"] is not None]
            for a in SHATTER}
    s5 = all(v is not None and v >= 0.5 for v in s5b.values() if v is not None)
    print(f"5 barriers: alpha-trends={s5b} shattered-band-by-n={bcol} "
          f"-> {'CLEAR' if s5 else 'FAIL'}")
    # 6 corridor trigger
    c1max = {}
    for a in SHATTER:
        for n in (26, 24, 20, 16):
            g = grid.get((n, a))
            if g and g["C1"] is not None:
                c1max[a] = (n, g["C1"])
                break
    trigger = any(v[1] >= 0.5 for v in c1max.values())
    print(f"6 corridor: C1 at largest completed n per shattered alpha = "
          f"{c1max} -> TRIGGER {'FIRES' if trigger else 'does not fire'}")

    # threshold curve
    print("\nSAT fraction per (n, alpha):")
    for n in NS + (26,):
        row = []
        for a in ALPHAS:
            cs = [c for c in cells if c["n"] == n and c["alpha"] == a]
            if cs:
                row.append(f"{a}:{sum(1 for c in cs if c['min_V']==0)}/{len(cs)}")
        print(f"  n={n}: " + " ".join(row))


if __name__ == "__main__":
    main()
