#!/usr/bin/env python3
"""Experiment C matrix: arms C0-C3 x instances, per pre-registration."""
import glob, json, subprocess, sys, time
R = '/Users/youmew/research/pnp'
S = sys.argv[1]
def find(name):
    for pat in (f'{R}/benchmarks/cnf/{name}.cnf', f'{R}/benchmarks/competition/**/{name}.cnf'):
        g = glob.glob(pat, recursive=True)
        if g: return g[0]
INSTANCES = ['mchess12','mchess14','mchess16','tseitin30','tseitin40','tseitin50',
             'php12','uf100-01','uf250-01']
for name in INSTANCES:
    cnf = find(name)
    for arm in (0,1,2,3):
        ev = f'{S}/expC_{name}_c{arm}.events.jsonl'
        pr = f'{S}/expC_{name}_c{arm}.pr'
        t0 = time.time()
        r = subprocess.run([f'{R}/tools/sadical/sadical','-q','-n','--binary=false','-f',
                            f'--harvest={arm}', f'--eventlog={ev}', cnf, pr],
                           capture_output=True, timeout=600)
        wall = time.time() - t0
        events = [json.loads(l) for l in open(ev)]
        end = [e for e in events if e['ev']=='run_end'][0]
        harv = [e for e in events if e['ev']=='harvest']
        verified = '-'
        if r.returncode == 20:
            v = subprocess.run([f'{R}/tools/dpr-trim/dpr-trim', cnf, pr],
                               capture_output=True, text=True)
            verified = 'yes' if 's VERIFIED' in v.stdout else 'NO'
        print(f"{name} C{arm}: conflicts={end['conflicts']} wall={wall:.2f}s "
              f"transfers={end['harvests']} harvest_events={len(harv)} "
              f"exit={r.returncode} verified={verified}", flush=True)
