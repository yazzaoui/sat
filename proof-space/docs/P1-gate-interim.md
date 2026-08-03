# P1 distinguishability gate — interim report (stop-and-report)

## Gate status

**PHP(4) anchor: CONCLUDED — every quantity fails the gate.**

| Cell | Q1 depth(⊥) | Q2 geodesic size | Q3 waves |
|---|---|---|---|
| w=3: T₀ → T_Cook | 8 → 7 (12.5% < 20%) | 641 → **1207** (wrong sign, 1.9×) | fronts widen at every level |
| w=4: T₀ → T_Cook | 7 → 7 (0%) | 1031 → **3240** (wrong sign, 3.1×) | fronts widen |

At the measurable anchor, Cook's machinery is pure front-volume
overhead in exactly the sense the portfolio has now measured five
times at finite size: the asymptotic advantage's shadow runs
backwards below its crossover.

**PHP(5) escalation: T₀ concluded (w=3 frontier closed — the BW
landmark behaving; w=4: depth 13, antichain 13,011, geodesic 8,296);
T_Cook cell COMPUTATIONALLY INFEASIBLE — measured, not estimated:**
antichain 2.4k → 12k → 56k → 145k → 179k through forward round 6 of
≤ 13, per-round cost O(antichain²), remaining rounds + geodesic pass
projected at many hours to days. Chunked checkpointing (built,
verified chunk≡single) does not rescue a cell whose atomic rounds
exceed the environment; further per-round subdivision would be
engineering-around, which the scope rule forbids.

## The decision point (lead's call)

The registered gate rule assumed the escalation cell was computable.
Measured reality: PHP(4) concluded (all fail), PHP(5) ER-cell out of
exact reach under the canonical space (joint-w rule fixes w=4; a
narrower width would need an amendment and T₀ is w=3-unreachable
anyway). Options as the discipline sees them:

1. **Close P1 at the gate** with the scoped verdict: *no registered
   observable separates ER from resolution at exactly-measurable
   scales — PHP(4) measured on all quantities (failing with the
   overhead sign), PHP(5)'s ER cell beyond exact computation under
   the canonical space.* This is Ending-1-shaped for the stream:
   entry 10 completes the through-line with the substrate-complete
   statement, carrying the PHP(5) infeasibility honestly as part of
   the sentence.
2. Amend the space or anchors — which the frame's no-shopping fence
   exists to resist, and nothing in the data suggests a different
   registered quantity would turn the sign at these scales.

Checkpointed state for the PHP(5) cell is preserved (resumable if
ever wanted on bigger hardware); all numbers above are exact and
cross-validated (C ≡ Python on every shared cell; chunked ≡
single-shot).
