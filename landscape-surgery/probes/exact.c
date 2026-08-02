// Exact landscape probe (L0): full enumeration + persistence merge tree.
//
// Canonical definitions per docs/L0-registration.md §1.2:
//   basins  = merge-tree leaves with persistence > 0 (plateau
//             consolidations, persistence 0, are not leaves)
//   barrier = merge level; summary = mean/max over all leaf pairs,
//             accumulated per merge event as lc1*lc2 pairs at that level
// Also computes the lexicographic steepest-descent disagreement check
// (--lex), reported alongside, never adjudicated.
//
// Memory layout (lead note, designed up front): V as uint16 (clause
// counts in scope are < 2^16), order/parent as uint32, per-state birth
// uint16 + component size + leafcount uint32. Peak ~ 17 bytes/state:
// n=24 -> ~285 MB, n=26 -> ~1.1 GB.
//
// Usage: exact [--lex] formula.cnf
// Output: single JSON line on stdout.

#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int n_vars, n_clauses;
static uint16_t *V;
static uint32_t *parent, *order, *csize, *lc;
static uint16_t *birth;
static uint64_t N;

static uint32_t find (uint32_t x) {
  while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
  return x;
}

int main (int argc, char **argv) {
  int do_lex = 0;
  const char *path = 0;
  for (int i = 1; i < argc; i++) {
    if (!strcmp (argv[i], "--lex")) do_lex = 1;
    else path = argv[i];
  }
  if (!path) { fprintf (stderr, "usage: exact [--lex] cnf\n"); return 1; }

  FILE *f = fopen (path, "r");
  if (!f) { perror (path); return 1; }
  // Parse DIMACS; store clauses as (fixed-mask, base-value) subcubes of
  // violating assignments: literal v>0 false => bit 0, v<0 false => bit 1.
  int cap = 1024, m = 0;
  uint32_t *cmask = malloc (cap * sizeof *cmask);
  uint32_t *cbase = malloc (cap * sizeof *cbase);
  char line[1 << 16];
  while (fgets (line, sizeof line, f)) {
    if (line[0] == 'c') continue;
    if (line[0] == 'p') { sscanf (line, "p cnf %d %d", &n_vars, &n_clauses); continue; }
    int lit; uint32_t mask = 0, base = 0; char *p = line; int any = 0;
    while (sscanf (p, "%d", &lit) == 1) {
      while (*p == ' ' || *p == '\t' || *p == '-') p++;
      while (*p >= '0' && *p <= '9') p++;
      while (*p == ' ' || *p == '\t') p++;
      if (!lit) break;
      any = 1;
      int v = abs (lit) - 1;
      mask |= 1u << v;
      if (lit < 0) base |= 1u << v;
    }
    if (!any) continue;
    if (m == cap) { cap *= 2; cmask = realloc (cmask, cap * sizeof *cmask);
                    cbase = realloc (cbase, cap * sizeof *cbase); }
    cmask[m] = mask; cbase[m] = base; m++;
  }
  fclose (f);
  if (n_vars < 1 || n_vars > 26) { fprintf (stderr, "n out of range\n"); return 1; }
  N = 1ull << n_vars;
  const uint32_t ALL = (uint32_t) (N - 1);

  // V via violating-subcube enumeration.
  V = calloc (N, sizeof *V);
  for (int c = 0; c < m; c++) {
    uint32_t free_ = ALL & ~cmask[c], sub = free_;
    for (;;) {
      V[cbase[c] | sub]++;
      if (!sub) break;
      sub = (sub - 1) & free_;
    }
  }

  // Counting sort by V.
  uint32_t maxv = 0;
  for (uint64_t s = 0; s < N; s++) if (V[s] > maxv) maxv = V[s];
  uint64_t *bucket = calloc ((size_t) maxv + 2, sizeof *bucket);
  for (uint64_t s = 0; s < N; s++) bucket[V[s] + 1]++;
  for (uint32_t v = 1; v <= maxv + 1; v++) bucket[v] += bucket[v - 1];
  order = malloc (N * sizeof *order);
  {
    uint64_t *fill = calloc ((size_t) maxv + 1, sizeof *fill);
    for (uint64_t s = 0; s < N; s++)
      order[bucket[V[s]] + fill[V[s]]++] = (uint32_t) s;
    free (fill);
  }

  // Persistence sweep.
  parent = malloc (N * sizeof *parent);
  memset (parent, 0xff, N * sizeof *parent);   // 0xffffffff = unprocessed
  birth = malloc (N * sizeof *birth);
  csize = malloc (N * sizeof *csize);
  lc = malloc (N * sizeof *lc);
  double barrier_sum = 0; uint64_t barrier_pairs = 0; uint32_t barrier_max = 0;
  uint64_t deaths = 0;
  for (uint64_t i = 0; i < N; i++) {
    uint32_t s = order[i];
    uint16_t v = V[s];
    parent[s] = s; birth[s] = v; csize[s] = 1; lc[s] = 1;
    for (int b = 0; b < n_vars; b++) {
      uint32_t nb = s ^ (1u << b);
      if (parent[nb] == 0xffffffffu) continue;
      uint32_t r1 = find (s), r2 = find (nb);
      if (r1 == r2) continue;
      // Younger = larger birth (ties: consolidation either way).
      uint32_t elder = birth[r1] <= birth[r2] ? r1 : r2;
      uint32_t young = elder == r1 ? r2 : r1;
      uint32_t l1 = lc[elder], l2 = lc[young];
      uint32_t merged_lc;
      if (birth[young] == v) merged_lc = l1 + l2 - 1;  // consolidation
      else {                                            // real leaf death
        deaths++;
        merged_lc = l1 + l2;
        barrier_sum += (double) v * (double) l1 * (double) l2;
        barrier_pairs += (uint64_t) l1 * l2;
        if (v > barrier_max) barrier_max = v;
      }
      parent[young] = elder;
      csize[elder] += csize[young];
      lc[elder] = merged_lc;
    }
  }
  uint32_t root = find (order[0]);
  uint64_t basins = lc[root];
  uint16_t minV = V[order[0]];
  uint64_t nmin = 0;
  for (uint64_t s = 0; s < N; s++) if (V[s] == minV) nmin++;

  uint64_t lex_basins = 0;
  if (do_lex) {
    // dest[s] via memoized argmin-neighbor descent, processed in (V, idx)
    // order so successors resolve before their predecessors.
    uint32_t *dest = parent;                    // reuse parent's memory
    memset (dest, 0xff, N * sizeof *dest);
    for (uint64_t i = 0; i < N; i++) {
      uint32_t s = order[i];
      uint32_t best = s;
      for (int b = 0; b < n_vars; b++) {
        uint32_t nb = s ^ (1u << b);
        if (V[nb] < V[best] || (V[nb] == V[best] && nb < best)) best = nb;
      }
      dest[s] = (best == s) ? s : dest[best];
    }
    // Count distinct destinations (mark bits in csize reused as bitmap).
    memset (csize, 0, N * sizeof *csize);
    for (uint64_t s = 0; s < N; s++) {
      uint32_t d = dest[s];
      if (!csize[d]) { csize[d] = 1; lex_basins++; }
    }
  }

  printf ("{\"n\":%d,\"clauses\":%d,\"min_V\":%u,\"n_min_states\":%llu,"
          "\"basins\":%llu,\"leaf_deaths\":%llu,"
          "\"barrier_mean\":%.4f,\"barrier_max\":%u",
          n_vars, m, minV, (unsigned long long) nmin,
          (unsigned long long) basins, (unsigned long long) deaths,
          barrier_pairs ? barrier_sum / (double) barrier_pairs : 0.0,
          barrier_max);
  if (do_lex)
    printf (",\"lex_basins\":%llu", (unsigned long long) lex_basins);
  printf ("}\n");
  return 0;
}
