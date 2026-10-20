from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import os,time,json,subprocess,shutil,datetime
R=Path('results/triceratops-20261013');exe='data/triceratops-20261013/venv/bin/python'
def wait_existing(name,pid):
 while not (R/f'{name}.json').exists():
  if not Path(f'/proc/{pid}').exists():raise RuntimeError(f'Existing process{pid} ended without{name} output')
  time.sleep(3)
 print('EXISTING FINISHED',name,flush=True)
def run(t,n,s=13,noise=1.,control='none'):
 name=f'{t}-N{n}-seed{s}-noise{noise:g}-{control}';p=R/f'{name}.json'
 if p.exists():print('REUSE',name,flush=True);return
 if n==100000:
  while int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))<6*1024**2:time.sleep(5)
 print('START',name,flush=True)
 with (R/f'{name}.log').open('w') as f:subprocess.check_call([exe,'-u',str(R/'run.py'),'--tic',str(t),'--draws',str(n),'--seed',str(s),'--noise',str(noise),'--control',control],stdout=f,stderr=subprocess.STDOUT)
 assert p.exists();print('END',name,flush=True)
def large():
 wait_existing('80387959-N1000000-seed13-noise1-none',1724476);run(402358350,1000000)
def small():
 wait_existing('137151335-N100000-seed13-noise1-none',1756089)
 for t in [80387959,402358350]:
  for noise,c in [(1.5,'none'),(2.,'none'),(1.,'flat'),(1.,'inverted')]:run(t,100000,noise=noise,control=c)
 replay=[];dest=R/'provenance-replay';dest.mkdir(exist_ok=True)
 for p in sorted(R.glob('*-N*-seed*-noise*-none.json')):
  d=json.loads(p.read_text())
  if 'input_hashes' in d:continue
  name=p.stem
  for f in list(R.glob(name+'.*'))+list(R.glob(name+'-scenarios.csv')):shutil.move(str(f),str(dest/f.name))
  run(d['tic'],d['draws'],d['seed'],d['noise']);new=json.loads(p.read_text());diff={k:new[k]-d[k] for k in ['FPP','NFPP','target_planet','any_host_planet']};replay.append(dict(run=name,difference=diff));print('REPLAY',name,diff,flush=True)
 (R/'replay-verification.json').write_text(json.dumps(replay,indent=2))
with ThreadPoolExecutor(max_workers=2) as pool:
 fs=[pool.submit(large),pool.submit(small)]
 for f in fs:f.result()
files=list(R.glob('*-N*-seed*-noise*-*.json'));assert len(files)==17,len(files)
for p in files:
 d=json.loads(p.read_text());assert d['status']=='completed' and 'input_hashes' in d,p
(R/'execution-complete.json').write_text(json.dumps(dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),runs=len(files),status='complete'),indent=2))
subprocess.check_call([exe,str(R/'summarize.py')]);subprocess.check_call([exe,str(R/'write_report.py')]);print('COMPLETE',flush=True)
