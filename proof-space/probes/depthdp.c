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

// checkpoint format: header {W, nd, frontier_start, bottom, gcursor}
// then D array. Enables chunked runs (environment kills long jobs).
static long frontier_start_g = 0;
static int bottom_g = -1, gcursor_g = -1;

static void dump_state (const char *f) {
  FILE *o = fopen (f, "wb");
  long hdr[5] = { W, nd, frontier_start_g, bottom_g, gcursor_g };
  fwrite (hdr, sizeof hdr, 1, o);
  fwrite (D, sizeof (Cl), nd, o);
  fclose (o);
}
static int load_state (const char *f) {
  FILE *o = fopen (f, "rb");
  if (!o) return 0;
  long hdr[5];
  if (fread (hdr, sizeof hdr, 1, o) != 1) { fclose (o); return 0; }
  W = hdr[0]; nd = hdr[1]; frontier_start_g = hdr[2];
  bottom_g = hdr[3]; gcursor_g = hdr[4];
  cap = nd + (1 << 16);
  D = malloc (cap * sizeof (Cl));
  if (fread (D, sizeof (Cl), nd, o) != (size_t) nd) { fclose (o); return 0; }
  fclose (o);
  return 1;
}

int main (int argc, char **argv) {
  const char *path = 0, *state = 0;
  int max_rounds = 1 << 30, geo_levels = 1 << 30, report_only = 0;
  for (int i = 1; i < argc; i++) {
    if (!strcmp (argv[i], "--width")) W = atoi (argv[++i]);
    else if (!strcmp (argv[i], "--state")) state = argv[++i];
    else if (!strcmp (argv[i], "--rounds")) max_rounds = atoi (argv[++i]);
    else if (!strcmp (argv[i], "--geo-levels")) geo_levels = atoi (argv[++i]);
    else if (!strcmp (argv[i], "--report")) report_only = 1;
    else path = argv[i];
  }
  int resumed = state && load_state (state);
  if (!resumed && !path) { fprintf (stderr, "need cnf or state\n"); return 1; }
  if (!resumed) {
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
  }                                      // end !resumed

  long frontier_start = frontier_start_g;
  int bottom = bottom_g;
  int rounds_done = 0;
  if (report_only) goto report;
  if (gcursor_g >= 0) goto geodesic;     // forward phase already done

  // rounds: resolve frontier x alive (with per-round compaction of
  // dead clauses — loops then run over ~antichain, not all-ever-added)
  while (1) {
    if (rounds_done++ >= max_rounds) {   // checkpoint and exit
      frontier_start_g = frontier_start; bottom_g = bottom;
      dump_state (state);
      printf ("{\"checkpoint\":\"forward\",\"nd\":%ld,\"bottom\":%d}\n",
              nd, bottom);
      return 0;
    }
    // compact: drop dead entries below the frontier boundary, keeping
    // relative order; adjust frontier_start accordingly
    {
      long w2 = 0, fs_new = frontier_start;
      for (long i = 0; i < nd; i++) {
        if (!D[i].alive) { if (i < frontier_start) fs_new--; continue; }
        D[w2++] = D[i];
      }
      nd = w2;
      frontier_start = fs_new < 0 ? 0 : fs_new;
    }
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
  gcursor_g = bottom;                    // forward phase complete

geodesic: ;
  long alive = 0;
  for (long i = 0; i < nd; i++) alive += D[i].alive;

  // geodesic backward mark
  long gsize = 0;
  long waves[128]; memset (waves, 0, sizeof waves);
  if (bottom >= 0) {
    if (gcursor_g == bottom)
      for (long i = 0; i < nd; i++)
        if (D[i].alive && D[i].p == 0 && D[i].n == 0) D[i].mark = 1;
    int glv = 0;
    for (int d = gcursor_g; d > 0; d--) {
      if (glv++ >= geo_levels) {         // checkpoint and exit
        frontier_start_g = frontier_start; bottom_g = bottom;
        gcursor_g = d;
        dump_state (state);
        printf ("{\"checkpoint\":\"geodesic\",\"cursor\":%d}\n", d);
        return 0;
      }
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
    gcursor_g = 0;
    if (state) { frontier_start_g = frontier_start; bottom_g = bottom;
                 dump_state (state); }
  }

report: ;
  if (report_only) {
    bottom = bottom_g;
    for (long i = 0; i < nd; i++)
      if (D[i].alive && D[i].mark) { gsize++; waves[D[i].depth]++; }
    for (long i = 0; i < nd; i++) alive += D[i].alive;
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
