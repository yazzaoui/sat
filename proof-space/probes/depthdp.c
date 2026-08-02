// S5 depth-DP probe: subsumption-aware minimal resolution depth,
// width-bounded, with geodesic-DAG extraction (backward marking).
// The one approved C port (P1 registration §4; trigger fired by
// measured Python timeout on the PHP(4)+cascade w=4 cell).
//
// Input: DIMACS (axioms = all clauses, definitions included).
// Args: --width w (required), cnf path.
// Output: one JSON line: depth of bottom (or null), antichain size,
// geodesic size, wavefront volumes.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { uint64_t p, n; int depth; uint8_t alive, mark; } Cl;
static Cl *D;
static long nd, cap;
static int W, NV;

static int width (uint64_t p, uint64_t n) {
  return __builtin_popcountll (p) + __builtin_popcountll (n);
}
static int subsumes (Cl *a, uint64_t p, uint64_t n) {
  return (a->p & ~p) == 0 && (a->n & ~n) == 0;
}

static int add_clause (uint64_t p, uint64_t n, int depth) {
  for (long i = 0; i < nd; i++) {
    if (!D[i].alive) continue;
    if (subsumes (&D[i], p, n) && D[i].depth <= depth) return 0;
  }
  for (long i = 0; i < nd; i++) {
    if (!D[i].alive) continue;
    if ((p & ~D[i].p) == 0 && (n & ~D[i].n) == 0 && depth <= D[i].depth)
      D[i].alive = 0;                    // new subsumes old
  }
  if (nd == cap) { cap *= 2; D = realloc (D, cap * sizeof (Cl)); }
  D[nd++] = (Cl){ p, n, depth, 1, 0 };
  return 1;
}

int main (int argc, char **argv) {
  const char *path = 0;
  for (int i = 1; i < argc; i++) {
    if (!strcmp (argv[i], "--width")) W = atoi (argv[++i]);
    else path = argv[i];
  }
  FILE *f = fopen (path, "r");
  if (!f) { perror (path); return 1; }
  cap = 1 << 16; D = malloc (cap * sizeof (Cl));
  char line[1 << 16];
  while (fgets (line, sizeof line, f)) {
    if (line[0] == 'c') continue;
    if (line[0] == 'p') { sscanf (line, "p cnf %d %*d", &NV); continue; }
    uint64_t p = 0, n = 0; int lit; char *q = line; int any = 0;
    while (sscanf (q, "%d", &lit) == 1 && lit) {
      any = 1;
      if (lit > 0) p |= 1ull << (lit - 1); else n |= 1ull << (-lit - 1);
      while (*q == ' ' || *q == '\t' || *q == '-') q++;
      while (*q >= '0' && *q <= '9') q++;
      while (*q == ' ' || *q == '\t') q++;
    }
    if (any) add_clause (p, n, 0);
  }
  fclose (f);

  // rounds: resolve frontier x alive
  long frontier_start = 0;
  int bottom = -1;
  while (1) {
    long nd0 = nd;
    long fs = frontier_start;
    frontier_start = nd0;
    int progress = 0;
    for (long i = 0; i < nd0; i++) {
      if (!D[i].alive) continue;
      long jstart = i < fs ? fs : i + 1;
      for (long j = jstart; j < nd0; j++) {
        if (!D[j].alive) continue;
        Cl a = D[i], b = D[j];
        for (int pass = 0; pass < 2; pass++) {
          uint64_t piv = pass ? (a.n & b.p) : (a.p & b.n);
          while (piv) {
            uint64_t v = piv & -piv; piv ^= v;
            uint64_t rp, rn;
            if (!pass) { rp = (a.p & ~v) | b.p; rn = a.n | (b.n & ~v); }
            else       { rp = a.p | (b.p & ~v); rn = (a.n & ~v) | b.n; }
            if (rp & rn) continue;
            if (width (rp, rn) > W) continue;
            int d = 1 + (a.depth > b.depth ? a.depth : b.depth);
            if (add_clause (rp, rn, d)) {
              progress = 1;
              if (rp == 0 && rn == 0 && (bottom < 0 || d < bottom))
                bottom = d;
            }
          }
        }
      }
    }
    if (bottom >= 0 || !progress) break;
  }

  long alive = 0;
  for (long i = 0; i < nd; i++) alive += D[i].alive;

  // geodesic backward mark
  long gsize = 0;
  long waves[128]; memset (waves, 0, sizeof waves);
  if (bottom >= 0) {
    for (long i = 0; i < nd; i++)
      if (D[i].alive && D[i].p == 0 && D[i].n == 0) D[i].mark = 1;
    for (int d = bottom; d > 0; d--) {
      for (long c = 0; c < nd; c++) {
        if (!D[c].alive || !D[c].mark || D[c].depth != d) continue;
        for (long i = 0; i < nd; i++) {
          if (!D[i].alive || D[i].depth >= d) continue;
          for (long j = 0; j < nd; j++) {
            if (!D[j].alive || D[j].depth >= d) continue;
            int dm = 1 + (D[i].depth > D[j].depth ? D[i].depth : D[j].depth);
            if (dm != d) continue;
            Cl a = D[i], b = D[j];
            for (int pass = 0; pass < 2; pass++) {
              uint64_t piv = pass ? (a.n & b.p) : (a.p & b.n);
              while (piv) {
                uint64_t v = piv & -piv; piv ^= v;
                uint64_t rp, rn;
                if (!pass) { rp = (a.p & ~v) | b.p; rn = a.n | (b.n & ~v); }
                else       { rp = a.p | (b.p & ~v); rn = (a.n & ~v) | b.n; }
                if (rp & rn) continue;
                if (width (rp, rn) > W) continue;
                if ((rp & ~D[c].p) == 0 && (rn & ~D[c].n) == 0) {
                  D[i].mark = 1; D[j].mark = 1;
                }
              }
            }
          }
        }
      }
    }
    for (long i = 0; i < nd; i++)
      if (D[i].alive && D[i].mark) { gsize++; waves[D[i].depth]++; }
  }

  printf ("{\"width\":%d,\"depth\":%s%d,\"antichain\":%ld,"
          "\"geodesic_size\":%ld,\"waves\":[",
          W, bottom < 0 ? "-" : "", bottom < 0 ? 1 : bottom, alive, gsize);
  if (bottom >= 0)
    for (int d = 0; d <= bottom; d++)
      printf ("%s%ld", d ? "," : "", waves[d]);
  printf ("]}\n");
  return 0;
}
