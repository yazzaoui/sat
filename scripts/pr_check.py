#!/usr/bin/env python3
"""Polynomial-time PR check (Heule–Kiesl–Biere): soundness gate for every
template-proposed witness. A clause C is PR w.r.t. formula F with witness
omega iff for every D in F: D|omega is satisfied, or
F|alpha ∪ ¬(D|omega) has a unit-propagation conflict, where alpha = ¬C.

No proposer is ever trusted; this check (and dpr-trim downstream) is the
soundness boundary (spec §5).
"""


def unit_propagate(clauses, assignment):
    """UP to fixpoint. assignment: dict var -> bool. Returns False on conflict."""
    assign = dict(assignment)
    changed = True
    while changed:
        changed = False
        for c in clauses:
            unassigned = None
            sat = False
            count = 0
            for l in c:
                v = assign.get(abs(l))
                if v is None:
                    unassigned = l
                    count += 1
                elif (l > 0) == v:
                    sat = True
                    break
            if sat:
                continue
            if count == 0:
                return False
            if count == 1:
                assign[abs(unassigned)] = unassigned > 0
                changed = True
    return assign


def reduce_clause(clause, assignment):
    """None if satisfied, else remaining literals."""
    out = []
    for l in clause:
        v = assignment.get(abs(l))
        if v is None:
            out.append(l)
        elif (l > 0) == v:
            return None
    return out


def is_pr(clauses, C, omega):
    """Is C propagation-redundant w.r.t. clauses with witness omega?"""
    alpha = {abs(l): l < 0 for l in C}          # negation of C
    w = {abs(l): l > 0 for l in omega}
    # omega must satisfy C itself (it is the "moved-to" region)
    if not any(w.get(abs(l)) == (l > 0) for l in C):
        return False
    base = unit_propagate(clauses, alpha)
    if base is False:
        return True                              # C is RUP outright
    for D in clauses:
        rest = reduce_clause(D, w)
        if rest is None:
            continue                             # D|omega satisfied
        # need UP conflict from F|alpha with ¬(D|omega)
        trial = dict(base)
        conflict = False
        for l in rest:
            v = trial.get(abs(l))
            if v == (l > 0):
                conflict = True                  # ¬(D|omega) contradicts base
                break
            trial[abs(l)] = l < 0
        if conflict:
            continue
        if unit_propagate(clauses, trial) is not False:
            return False
    return True
