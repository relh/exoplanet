from pathlib import Path
import os,time,json,subprocess,shutil
R=Path('results/triceratops-20261013');D=R/'provenance-replay';D.mkdir(exist_ok=True);exe='data/triceratops-20261013/venv/bin/python'
while Path('/proc/1666149').exists():time.sleep(5)
for p in sorted(R.glob('*-N*-seed*-noise*-none.json')):
 d=json.loads(p.read_text())
 if 'input_hashes' in d:continue
 name=p.stem
 for x in list(R.glob(name+'.*'))+list(R.glob(name+'-scenarios.csv')):shutil.move(str(x),str(D/x.name))
 with (R/f'{name}.log').open('w') as f:subprocess.check_call([exe,'-u',str(R/'run.py'),'--tic',str(d['tic']),'--draws',str(d['draws']),'--seed',str(d['seed']),'--noise',str(d['noise'])],stdout=f,stderr=subprocess.STDOUT)
 new=json.loads(p.read_text());print(name,{k:new[k]-d[k] for k in ['FPP','NFPP','target_planet','any_host_planet']},flush=True)
subprocess.check_call([exe,str(R/'summarize.py')])
