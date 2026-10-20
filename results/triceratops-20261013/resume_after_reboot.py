"""Resume only the unfinished bounded experiment, serially, after reboot."""
from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess
R=Path('results/triceratops-20261013'); exe='data/triceratops-20261013/venv/bin/python'
archive=R/'reboot-interrupted'; archive.mkdir(exist_ok=True)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
planned=[]
for t in [80387959,402358350]:
 for seed in [13,29,47]:planned.append((t,100000,seed,1.,'none'))
 planned.append((t,1000000,13,1.,'none'))
 for noise,control in [(1.5,'none'),(2.,'none'),(1.,'flat'),(1.,'inverted')]:planned.append((t,100000,13,noise,control))
planned.append((137151335,100000,13,1.,'none'))
def name(row):
 t,n,s,noise,c=row;return f'{t}-N{n}-seed{s}-noise{noise:g}-{c}'
assert len(planned)==17
manifest=R/'reboot-resumption.json'
assert not manifest.exists(), 'Review existing resumption before restarting'
state={str(p.relative_to(R)):digest(p) for p in sorted(R.rglob('*')) if p.is_file() and '__pycache__' not in str(p)}
record=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),boot_id=Path('/proc/sys/kernel/random/boot_id').read_text().strip(),scope='Complete existing bounded 17-run plan and three previously required hash replays only. No new inputs or observations.',inspection='No live local TRICERATOPS process. Retained execution scripts use local subprocesses only; no remote dispatch reference.',scheduling='Serial probability calculations; 2 Numba threads, 1 BLAS thread; minimum 6 GiB available memory before each run.',retained_artifact_sha256=state,planned_runs=[name(row) for row in planned])
manifest.write_text(json.dumps(record,indent=2))
env={**os.environ,'NUMBA_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1'}
replays=[]
for row in planned:
 stem=name(row);p=R/f'{stem}.json';old=None
 if p.exists():
  old=json.loads(p.read_text());assert old['status']=='completed',p
  if 'input_hashes' in old:
   for path,h in old['input_hashes'].items():assert digest(Path(path))==h,path
   print('REUSE',stem,flush=True);continue
  dest=R/'provenance-replay';dest.mkdir(exist_ok=True)
  for f in [p,R/f'{stem}.log',R/f'{stem}-scenarios.csv']:
   if f.exists():assert not (dest/f.name).exists();shutil.copy2(f,dest/f.name)
 else:
  for f in [R/f'{stem}.log',R/f'{stem}-scenarios.csv']:
   if f.exists():assert not (archive/f.name).exists();shutil.copy2(f,archive/f.name)
 available=int(next(line.split()[1] for line in Path('/proc/meminfo').read_text().splitlines() if line.startswith('MemAvailable:')))
 assert available>=6*1024**2, 'Insufficient available memory; stop safely'
 t,n,s,noise,c=row; print('START',stem,flush=True)
 with (R/f'{stem}.log').open('w') as f:subprocess.check_call([exe,'-u',str(R/'run.py'),'--tic',str(t),'--draws',str(n),'--seed',str(s),'--noise',str(noise),'--control',c],env=env,stdout=f,stderr=subprocess.STDOUT)
 new=json.loads(p.read_text());assert new['status']=='completed' and 'input_hashes' in new,p
 if old is not None:replays.append(dict(run=stem,difference={k:new[k]-old[k] for k in ['FPP','NFPP','target_planet','any_host_planet']}))
 print('END',stem,flush=True)
 (R/'replay-verification.json').write_text(json.dumps(replays,indent=2))
for row in planned:
 p=R/f'{name(row)}.json';d=json.loads(p.read_text());assert d['status']=='completed' and 'input_hashes' in d
assert len(list(R.glob('*-N*-seed*-noise*-*.json')))==17
(R/'execution-complete.json').write_text(json.dumps(dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),runs=17,status='complete',resumption_manifest=str(manifest)),indent=2))
subprocess.check_call([exe,str(R/'summarize.py')],env=env)
subprocess.check_call([exe,str(R/'write_report.py')],env=env)
print('COMPLETE',flush=True)
