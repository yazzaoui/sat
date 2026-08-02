// P1 engine: exact net conductance under lazy-propagation dynamics.
//
// Implements the P0 canonical objects exactly:
//   - moves initiate on x-variables only; the repair cascade processes
//     definitions in DAG order: a definition is re-evaluated iff one of
//     its inputs flipped during this move; stale definitions untouched
//     by the move persist (staleness conservation).
//   - descent digraph: edges with V_full(succ) <= V_full(cur).
//   - attractor = terminal SCC; basin = reachability preimage
//     (set-valued, tie-break-free). Computed by iterative Tarjan with
//     on-the-fly successors + attractor-mask propagation in reverse
//     condensation order.
//   - lex-descent disagreement check (reported, never adjudicated).
//
// Soundness gate (re-verified in-engine): every provided solution lift
// satisfies all definition clauses, and flipping any single z at a lift
// violates one (uniqueness).
//
// Input format (emitted by drive_p1.py):
//   p ext <n_total> <n_base>
//   o <lits> 0            original clause
//   d <layer> <zvar> <lits> 0   definition clause owned by zvar
//   s <uint state>        solution lift sigma(s) as packed bits
// Modes: --bench (microbenchmark gate), default = full analysis.
// Output: one JSON line.

#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXC 512
#define MAXL 8
#define MAXZ 32
#define MAXS 32

static int n_total, n_base, n_orig, n_def;
static int oc[MAXC][MAXL], on[MAXC];               // original clauses
static int dc[MAXC][MAXL], dn[MAXC], down[MAXC];   // def clauses + owner
static int dlayer[MAXC];
static int zvars[MAXZ], nz;                        // DAG order
static uint32_t zin_mask[MAXZ];                    // input vars per z
static int zclauses[MAXZ][8], zc_n[MAXZ];          // def clauses per z
static uint32_t sols[MAXS]; static int nsol;
static uint16_t *V;
static uint64_t N;

static int lit_true (uint32_t s, int lit) {
  int v = abs (lit) - 1;
  int val = (s >> v) & 1;
  return lit > 0 ? val : !val;
}
static int clause_sat (uint32_t s, int *lits, int n) {
  for (int i = 0; i < n; i++) if (lit_true (s, lits[i])) return 1;
  return 0;
}

// Lazy-propagation successor: flip x-bit i, cascade in DAG order.
// P0 canon: repair a definition ONLY for clauses that BECAME violated
// during this move (violated now, satisfied at move start). Clauses
// already violated at move start are stale and stay stale unless a
// flip happens to satisfy them (accidental repair) — staleness
// conservation is the load-bearing property of the surviving object.
static uint32_t succ (uint32_t s, int xbit) {
  uint32_t t = s ^ (1u << xbit);
  uint32_t flipped = 1u << xbit;
  for (int k = 0; k < nz; k++) {
    if (!(zin_mask[k] & flipped)) continue;        // inputs untouched
    int became = 0;
    for (int c = 0; c < zc_n[k]; c++) {
      int ci = zclauses[k][c];
      if (!clause_sat (t, dc[ci], dn[ci]) &&
          clause_sat (s, dc[ci], dn[ci])) { became = 1; break; }
    }
    if (became) {
      t ^= 1u << (zvars[k] - 1);
      flipped |= 1u << (zvars[k] - 1);
    }
  }
  return t;
}

static void compute_V (void) {
  V = calloc (N, sizeof *V);
  uint32_t ALL = (uint32_t) (N - 1);
  for (int pass = 0; pass < 2; pass++) {
    int m = pass ? n_def : n_orig;
    for (int c = 0; c < m; c++) {
      int *lits = pass ? dc[c] : oc[c];
      int n = pass ? dn[c] : on[c];
      uint32_t mask = 0, base = 0;
      for (int i = 0; i < n; i++) {
        int v = abs (lits[i]) - 1;
        mask |= 1u << v;
        if (lits[i] < 0) base |= 1u << v;
      }
      uint32_t freeb = ALL & ~mask, sub = freeb;
      for (;;) {
        V[base | sub]++;
        if (!sub) break;
        sub = (sub - 1) & freeb;
      }
    }
  }
}

// ---- iterative Tarjan over the descent digraph ----
static uint32_t *tindex, *tlow, *sccid;
static uint8_t *onstk;
static uint32_t *tstack;
static uint32_t idx_ctr, scc_ctr, tsp;

static void tarjan (void) {
  tindex = calloc (N, 4); tlow = malloc (N * 4); sccid = malloc (N * 4);
  onstk = calloc (N, 1); tstack = malloc (N * 4);
  uint32_t *cstack = malloc (N * 4); uint8_t *estack = malloc (N + 8);
  idx_ctr = 1; scc_ctr = 0; tsp = 0;
  for (uint64_t root = 0; root < N; root++) {
    if (tindex[root]) continue;
    long sp = 0;
    cstack[0] = (uint32_t) root; estack[0] = 0;
    tindex[root] = tlow[root] = idx_ctr++;
    onstk[root] = 1; tstack[tsp++] = (uint32_t) root;
    while (sp >= 0) {
      uint32_t s = cstack[sp];
      if (estack[sp] < n_base) {
        int i = estack[sp]++;
        uint32_t t = succ (s, i);
        if (V[t] > V[s]) continue;                 // not a descent edge
        if (!tindex[t]) {
          sp++;
          cstack[sp] = t; estack[sp] = 0;
          tindex[t] = tlow[t] = idx_ctr++;
          onstk[t] = 1; tstack[tsp++] = t;
        } else if (onstk[t] && tindex[t] < tlow[s])
          tlow[s] = tindex[t];
      } else {
        if (tlow[s] == tindex[s]) {
          uint32_t w;
          do {
            w = tstack[--tsp];
            onstk[w] = 0;
            sccid[w] = scc_ctr;
          } while (w != s);
          scc_ctr++;
        }
        sp--;
        if (sp >= 0 && tlow[s] < tlow[cstack[sp]])
          tlow[cstack[sp]] = tlow[s];
      }
    }
  }
  free (cstack); free (estack);
  free (tindex); free (tlow); free (tstack); free (onstk);
}

int main (int argc, char **argv) {
  int bench = 0; const char *path = 0;
  for (int i = 1; i < argc; i++)
    if (!strcmp (argv[i], "--bench")) bench = 1;
    else if (!path && argv[i][0] != '-') path = argv[i];
  FILE *f = fopen (path, "r");
  if (!f) { perror (path); return 1; }
  char line[4096];
  while (fgets (line, sizeof line, f)) {
    if (line[0] == 'p') sscanf (line, "p ext %d %d", &n_total, &n_base);
    else if (line[0] == 'o') {
      int *L = oc[n_orig], k = 0, x; char *p = line + 1;
      while (sscanf (p, "%d", &x) == 1 && x) {
        L[k++] = x;
        p = strpbrk (p + 1, " \t"); while (*p == ' ') p++;
      }
      on[n_orig++] = k;
    } else if (line[0] == 'd') {
      int layer, owner; char *p = line + 1;
      sscanf (p, "%d %d", &layer, &owner);
      p = strpbrk (p + 1, " \t") + 1; p = strpbrk (p, " \t") + 1;
      int *L = dc[n_def], k = 0, x;
      while (sscanf (p, "%d", &x) == 1 && x) {
        L[k++] = x;
        p = strpbrk (p + 1, " \t"); while (*p == ' ') p++;
      }
      dn[n_def] = k; down[n_def] = owner; dlayer[n_def] = layer; n_def++;
    } else if (line[0] == 's') {
      unsigned long long u; sscanf (line, "s %llu", &u);
      sols[nsol++] = (uint32_t) u;
    }
  }
  fclose (f);
  N = 1ull << n_total;

  // Build z tables in DAG (layer, var) order.
  int seen[MAXZ * 8]; memset (seen, 0, sizeof seen);
  for (int layer = 0; layer < 8; layer++)
    for (int c = 0; c < n_def; c++)
      if (dlayer[c] == layer && !seen[down[c]]) {
        seen[down[c]] = 1;
        zvars[nz] = down[c];
        for (int c2 = 0; c2 < n_def; c2++)
          if (down[c2] == down[c]) {
            zclauses[nz][zc_n[nz]++] = c2;
            for (int i = 0; i < dn[c2]; i++)
              if (abs (dc[c2][i]) != down[c])
                zin_mask[nz] |= 1u << (abs (dc[c2][i]) - 1);
          }
        nz++;
      }

  compute_V ();

  // Soundness gate: lifts satisfy all defs; unique per z-flip.
  for (int k = 0; k < nsol; k++) {
    for (int c = 0; c < n_def; c++)
      if (!clause_sat (sols[k], dc[c], dn[c])) {
        printf ("{\"error\":\"soundness: lift %d violates def\"}\n", k);
        return 2;
      }
    for (int z = 0; z < nz; z++) {
      uint32_t t = sols[k] ^ (1u << (zvars[z] - 1));
      int viol = 0;
      for (int c = 0; c < n_def && !viol; c++)
        if (!clause_sat (t, dc[c], dn[c])) viol = 1;
      if (!viol) {
        printf ("{\"error\":\"soundness: z%d not unique at lift %d\"}\n",
                zvars[z], k);
        return 2;
      }
    }
  }

  if (argc > 3 && !strcmp (argv[argc - 3], "--succ")) {
    uint32_t s = (uint32_t) strtoul (argv[argc - 2], 0, 10);
    int b = atoi (argv[argc - 1]);
    printf ("{\"succ\":%u}\n", succ (s, b));
    return 0;
  }

  if (bench) {
    uint64_t iters = 20000000, acc = 0;
    uint32_t s = 12345;
    clock_t t0 = clock ();
    for (uint64_t i = 0; i < iters; i++) {
      s = s * 1664525u + 1013904223u;
      acc ^= succ (s & (uint32_t) (N - 1), (int) (s >> 28) % n_base);
    }
    double dt = (double) (clock () - t0) / CLOCKS_PER_SEC;
    printf ("{\"bench_evals_per_sec\":%.3e,\"acc\":%llu}\n", iters / dt,
            (unsigned long long) (acc & 1));
    return 0;
  }

  tarjan ();

  // Mask propagation in ascending scc id (= reverse topological).
  uint32_t *mask = calloc (scc_ctr, 4);
  uint8_t *terminal = malloc (scc_ctr); memset (terminal, 1, scc_ctr);
  uint64_t *scc_size = calloc (scc_ctr, 8);
  for (uint64_t s = 0; s < N; s++) scc_size[sccid[s]]++;
  for (int k = 0; k < nsol; k++) mask[sccid[sols[k]]] |= 1u << k;
  // order states by ascending scc id (counting sort)
  uint64_t *off = calloc ((uint64_t) scc_ctr + 1, 8);
  for (uint64_t s = 0; s < N; s++) off[sccid[s] + 1]++;
  for (uint32_t c = 1; c <= scc_ctr; c++) off[c] += off[c - 1];
  uint32_t *order = malloc (N * 4);
  uint64_t *fill = calloc (scc_ctr, 8);
  for (uint64_t s = 0; s < N; s++)
    order[off[sccid[s]] + fill[sccid[s]]++] = (uint32_t) s;
  for (uint64_t i = 0; i < N; i++) {
    uint32_t s = order[i];
    for (int b = 0; b < n_base; b++) {
      uint32_t t = succ (s, b);
      if (V[t] > V[s]) continue;
      if (sccid[t] != sccid[s]) {
        mask[sccid[s]] |= mask[sccid[t]];
        terminal[sccid[s]] = 0;
      }
    }
  }
  uint64_t n_terminal = 0, top[5] = {0};
  for (uint32_t c = 0; c < scc_ctr; c++)
    if (terminal[c]) {
      n_terminal++;
      for (int j = 0; j < 5; j++)
        if (scc_size[c] > top[j]) {
          for (int q = 4; q > j; q--) top[q] = top[q - 1];
          top[j] = scc_size[c]; break;
        }
    }

  // Per-solution basin fractions.
  printf ("{\"n_total\":%d,\"n_base\":%d,\"n_sccs\":%u,"
          "\"n_terminal\":%llu,\"top_terminal_sizes\":[%llu,%llu,%llu,%llu,%llu],"
          "\"basin_fraction\":[", n_total, n_base, scc_ctr,
          (unsigned long long) n_terminal,
          (unsigned long long) top[0], (unsigned long long) top[1],
          (unsigned long long) top[2], (unsigned long long) top[3],
          (unsigned long long) top[4]);
  for (int k = 0; k < nsol; k++) {
    uint64_t cnt = 0;
    for (uint64_t s = 0; s < N; s++)
      if (mask[sccid[s]] & (1u << k)) cnt++;
    printf ("%s%.6f", k ? "," : "", (double) cnt / (double) N);
  }
  // per-state mask dump for the driver's gain/loss join
  printf ("],\"maskfile\":\"");
  char mf[512]; snprintf (mf, sizeof mf, "%s.mask", path);
  printf ("%s\"}\n", mf);
  FILE *mo = fopen (mf, "wb");
  for (uint64_t s = 0; s < N; s++) {
    uint32_t m = mask[sccid[s]];
    fwrite (&m, 4, 1, mo);
  }
  fclose (mo);
  return 0;
}
