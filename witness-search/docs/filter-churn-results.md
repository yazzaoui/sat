# Filter-churn results — gate fired, mechanism dead on arrival

Run per registration (`filter-churn-preregistration.md`): determinism
gate PASS with logging off AND on (frozen counts exact); analysis
offline from logs; instances mchess(12,14) primary, tseitin(40) second.

## The number (per consecutive-hunt delta, lag 1)

| Instance | Verdict churn (shared domain) | Domain churn | **Recompute fraction** |
|---|---|---|---|
| mchess12 | med 0.0% (mean 4.0%) | med 59.4% | **med 61.5%** |
| mchess14 | med 0.0% (mean 4.3%) | med 55.6% | **med 57.6%** |
| tseitin40 | med 5.0% (mean 8.9%) | med 17.0% | med 22.9% |

At lag 5, chessboard recompute reaches ~90%.

## Reading

The pre-registered gate (churn > 10–15% ⇒ dead on arrival, domain
membership counting as change) fires at ~4× its threshold on the
primary family — but the structure is more informative than a flat
rate: **verdicts almost never flip on clauses that stay in the checked
domain (median 0%); the checked domain itself is reconstituted
majority-fresh at every stuck point** (55–59% membership change per
3–8 literal delta). The trail delta doesn't change the answers — it
changes the questions.

## The map's final edge (pre-committed framing)

**Filter verdicts are trail-sensitive at ~58–62% recompute per delta on
the primary family; approximate filtering is structurally unsafe.**
Per the pre-commitment: no incremental-UP data-structure hunt, no
watched-literal surgery on a 2018 codebase. The amortization arc closes
here, completing the boundary map:

1. Static witness cores — fail (four integrations).
2. Trail-aware cheap guidance inward — fails (A).
3. Activity export outward — harms (C).
4. Clause-identity persistence — cost isn't stored there (E, pre-build).
5. Delta-stable filtering — the reduct is a per-trail object at every
   layer measured: clauses copied, verdicts, and now domain membership
   (this result).

Composite statement for the paper: the stuck-point computation is
irreducibly local in time as well as in information — its inputs, its
cost, and its products are all specific to the trail at which it runs.
SDCL's sub-solver call is not an inefficiency to be amortized or
approximated; it is the unit of the method.
