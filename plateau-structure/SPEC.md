# Stream S2 — What Structures the Plateau? Registration Frame

(Lead-issued frame, recorded verbatim at kickoff. See
docs/S2-registration.md for the executable registration: precise
candidate definitions, measured feasibility, and bars.)

## Question

The plateau discovery (landscape-surgery stream, banked): UNSAT PHP's
landscape under canonical merge-tree analysis is one undifferentiated
plateau system — hardness there is featurelessness, not ruggedness; a
descent walker receives zero gradient information at the bottom. Yet
practical local search is not blind on plateaus: SLS solvers navigate
them daily using secondary signals (break counts, make counts, age
heuristics) that the primary altitude V = #violated-clauses cannot see.
Nobody has measured, under honest basin definitions, whether these
secondary signals impose structure on the plateau.

S2 asks: do standard secondary potentials structure the plateau — and
does that structure point anywhere useful?

- S2a (structure): under lexicographic refined altitude (V, V₂), does
  the plateau's merge tree develop non-trivial basin structure? Which
  candidates structure it, and how much?
- S2b (usefulness): where structure appears, is it navigationally
  meaningful (distance-to-exit correlation on satisfiable instances;
  UNSAT needs a registered proxy or an honest "not measurable")?

## Candidate menu (FIXED — no additions after registration)

1. break-weighted exposure: Σ over satisfied clauses of
   1/(#satisfying literals)
2. critical-clause count: #clauses satisfied by exactly one literal
3. propagation potential (decidedness)
4. flip mobility (in-menu control; expected structure-poor)

No composite or tuned potentials — the menu is the menu.

## Pre-registered reading branches

- Structured + useful → featurelessness is curable by refinement;
  geometry validates a folklore signal. Ledger-positive.
- Structured + useless → decorative geography. Mildly deflationary.
- Unstructured → the flat is flat all the way down through the
  standard menu; SLS plateau escape must work by other mechanisms.
  Strongest deflationary branch.
- Split verdicts reported per-family (random 3-SAT is the
  anti-symmetry-artifact check).

## Discipline

Registration before code; feasibility measured into registration;
bars before runs; one run per cell; menu fixed; in-menu control;
every claim in reproduce.py; scope rule; time-box 2 weeks to verdict
or suspension; ledger sentence on closure regardless of branch.
