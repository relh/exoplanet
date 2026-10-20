from pathlib import Path
import argparse,json,time,warnings,traceback,hashlib
import numpy as np,pandas as pd
from triceratops.triceratops import target
p=argparse.ArgumentParser();p.add_argument('--tic',type=int,required=True);p.add_argument('--draws',type=int,default=10000);p.add_argument('--seed',type=int,default=13);p.add_argument('--noise',type=float,default=1.);p.add_argument('--control',choices=['none','flat','inverted'],default='none');arg=p.parse_args()
R=Path('results/triceratops-20261013');m=json.loads((R/f'{arg.tic}-input.json').read_text());a=target.__new__(target);a.ID=arg.tic;a.mission='TESS';a.stars=pd.read_csv(R/f'{arg.tic}-stars.csv',dtype={'ID':str});assert a.stars.ID.iloc[0]==str(arg.tic);bg=json.loads((R/f'{arg.tic}-background.json').read_text());a.trilegal_fname=bg['path'];a.trilegal_url=None;a.background_population_source='gaia';assert Path(a.trilegal_fname).exists()
z=np.load(R/f'{arg.tic}-input.npz');flux=z['flux'].copy()
if arg.control=='flat':flux=np.ones_like(flux)
if arg.control=='inverted':flux=2-flux
name=f'{arg.tic}-N{arg.draws}-seed{arg.seed}-noise{arg.noise:g}-{arg.control}';start=time.time();np.random.seed(arg.seed);status={**vars(arg),'started':start,'input_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/f'{arg.tic}-stars.csv',R/f'{arg.tic}-input.npz',R/f'{arg.tic}-input.json',R/('control-plan.json' if arg.tic==137151335 else 'plan.json'),R/('control-catalog-correction-plan.json' if arg.tic==137151335 else 'catalog-correction-plan.json')]}}
try:
 with warnings.catch_warnings(record=True) as ws:
  warnings.simplefilter('always');a.calc_probs(z['time'],flux,float(z['error'])*arg.noise,m['clock']['period'],N=arg.draws,parallel=True,verbose=1,exptime=m['exptime'],nsamples=20,dilution_corrected=False)
 status['warnings']=[str(w.message) for w in ws];a.probs['lnZ']=a.lnZ;a.probs.to_csv(R/f'{name}-scenarios.csv',index=False)
 status.update(FPP=float(a.FPP),NFPP=float(a.NFPP),target_planet=1-float(a.FPP),any_host_planet=float(a.probs.loc[a.probs.scenario.isin(['TP','PTP','STP','DTP','BTP','NTP']),'prob'].sum()),degenerate=bool(a.FPP_degenerate),scenario_count=len(a.probs),finite_evidences=int(np.isfinite(a.lnZ).sum()),status='completed')
except Exception as e:status.update(status='failed',error=repr(e),traceback=traceback.format_exc());traceback.print_exc()
status['elapsed_seconds']=time.time()-start;(R/f'{name}.json').write_text(json.dumps(status,indent=2));print(json.dumps(status),flush=True)
