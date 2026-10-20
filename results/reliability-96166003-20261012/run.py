from pathlib import Path
import json,numpy as np
from exoplanet.campaign import load_training
from exoplanet.followup import refine_training,fixed_measure
from exoplanet.null_controls import block_permutation
from exoplanet.pipeline import sha,save_json,now
from scipy.stats import beta
O=Path(__file__).parent;DISC=Path('results/solar-radius-ranks5456-5968-20261011/targets/96166003.json');FROZEN=Path('results/expanded-96166003-20261012/frozen-for59.json');SECTORS=[19,43,44,59]
def main():
 assert not (O/'plan.json').exists();d=json.loads(DISC.read_text());seed=d['screened_peaks'][0]['best'];paths=[Path(f'data/lightcurves/s{s:04d}-96166003.fits') for s in SECTORS];assert all(p.exists() and p.with_suffix('.fits.json').exists() for p in paths)
 plan=dict(created_utc=now(),seed=seed,seed_baseline=d['clean_baseline_days'],primary_pre59=json.loads(FROZEN.read_text())['rows'][0]['best'],sectors=SECTORS,window=1.5,block_days=[.25,.5,1.0],draws_per_length=40,random_seed=20261012,inputs={str(p):sha(p) for p in paths+[DISC,FROZEN,Path(__file__),Path('src/exoplanet/followup.py'),Path('src/exoplanet/null_controls.py'),Path('src/exoplanet/search.py')]},policy='Allobservationsalreadyviewed; retrospective conditional selectedfamily reliability diagnostic. MaximumBLSloglikelihood over unchangedoriginalseedfamily and3durations forbothobserved/nulls. Sectorwise gapsegmentedblockpermutation of pairedflux/errors; noiidcadences, no datachosenblocklengths/events.40drawseach3lengths=120controls, do notpoolmodels. Seams/longcorrelationdestruction and survivingtransitfragments violate perfectexchangeability; countsnotglobalFAPorplanetprobability. Primarypre59 fixedclock retained separately, not replacedbyallsectorbest.')
 save_json(O/'plan.json',plan);arrays=[];evidence=[]
 for s in SECTORS:
  t,y,e,ev=load_training({'tic':96166003,'training_sectors':[s]},Path('data'),window=1.5);arrays.append((t,y,e));evidence.extend(ev)
 t,y,e=[np.concatenate([a[j] for a in arrays]) for j in range(3)];np.savez_compressed(O/'input.npz',t=t,y=y,e=e,sector=np.concatenate([np.full(len(a[0]),s) for s,a in zip(SECTORS,arrays)]))
 observed,ranges=refine_training(t,y,e,seed,seed_baseline=plan['seed_baseline']);inverted,ir=refine_training(t,2-y,e,seed,seed_baseline=plan['seed_baseline']);b=plan['primary_pre59'];save_json(O/'observed.json',dict(observed=observed,ranges=ranges,inverted=inverted,inverted_ranges=ir,fixed_primary=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']),data=evidence,plan_sha256=sha(O/'plan.json')))
 rows=[];indices=[]
 for length in plan['block_days']:
  for draw in range(40):
   rng=np.random.default_rng(np.random.SeedSequence([20261012,96166003,int(length*100),draw]));offset=0;parts=[]
   for a in arrays:parts.append(block_permutation(a[0],length,rng)+offset);offset+=len(a[0])
   ix=np.concatenate(parts);best,_=refine_training(t,y[ix],e[ix],seed,seed_baseline=plan['seed_baseline']);rows.append(dict(block_days=length,draw=draw,best=best,exceeds=best['power']>=observed['power']));indices.append(ix)
  save_json(O/'results.json',rows);np.savez_compressed(O/'permutations.npz',indices=np.stack(indices));print('completed',length,flush=True)
 summary=[]
 for length in plan['block_days']:
  k=sum(r['exceeds'] for r in rows if r['block_days']==length);n=40;summary.append(dict(block_days=length,k=k,n=n,fraction=k/n,binomial95_interval=[0 if k==0 else float(beta.ppf(.025,k,n-k+1)),1 if k==n else float(beta.ppf(.975,k+1,n-k))]))
 save_json(O/'summary.json',dict(status='complete',created_utc=now(),rows=summary,interval_note='Binomial MonteCarlo interval within specified randomization model only; modelmisspecification/selectionnotcovered.'))
if __name__=='__main__':main()
