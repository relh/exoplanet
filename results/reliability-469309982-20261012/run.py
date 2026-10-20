from pathlib import Path
import json,numpy as np
from scipy.stats import beta
from exoplanet.pipeline import sha,save_json,now,read_curve
from exoplanet.search import flatten
from exoplanet.followup import refine_training
from exoplanet.null_controls import block_permutation
O=Path(__file__).parent;SOURCE=Path('results/weak-seed-ranks8-32-20261011/targets/469309982.json');SECTORS=[9,10,36,37]
def evaluate(raw,seed,baseline):
 windows=[]
 for window in [1.5,2.5]:
  arrays=[flatten(*a,window=window) for a in raw];t,y,e=[np.concatenate([a[j] for a in arrays]) for j in range(3)];best,ranges=refine_training(t,y,e,seed,seed_baseline=baseline);windows.append(dict(window=window,best=best,ranges=ranges))
 a,b=windows;eligible=bool(a['best']['depth_snr']>=8 and b['best']['depth_snr']>=8 and abs(a['best']['period']/b['best']['period']-1)<.005 and not a['ranges']['search_boundary_hit'] and not b['ranges']['search_boundary_hit']);return dict(windows=windows,eligible=eligible,statistic=float(min(a['best']['depth_snr'],b['best']['depth_snr'])))
def main():
 assert not (O/'plan.json').exists();source=json.loads(SOURCE.read_text());selection=source['selection'];seed=selection['seed'];baseline=selection['original_baseline_days'];snap=SOURCE.parent.parent/'source';assert selection['target']['training_sectors']==SECTORS
 for name in ['followup.py','search.py','campaign.py']:assert sha(snap/name)==sha(Path('src/exoplanet')/name)
 raw=[];paths=[]
 for s in SECTORS:
  p=Path(f'data/lightcurves/s{s:04d}-469309982.fits');t,y,e,meta=read_curve(p);assert meta['ticid']==469309982 and meta['sector']==s;raw.append((t,y,e));paths.append(p)
 plan=dict(created_utc=now(),source_path=str(SOURCE),seed=seed,baseline=baseline,sectors=SECTORS,windows=[1.5,2.5],block_days=[.25,.5,1.],draws_per_length=40,random_seed=20261012,inputs={str(p):sha(p) for p in paths+[SOURCE,Path(__file__),*[(snap/name) for name in ['followup.py','search.py','campaign.py']]]},selection='Actualweak-seedlocalflag: bothformalSNR>=8,periodagreement<.5percent,neitherperiodprofileboundary. Statistic=min(twoformalSNRs),compareonlyeligiblecontrols toobservedstatistic;also reportallflagcounts. Notoriginalfullsearchgates.',policy='Conditiononoriginalselectedseedand4expandedtrainingsectors, notnew59/64data. Rawqualityscreenedflux/errorpairs blockpermuted sectorwisegapsegments, then identicaltwo-windowflatten/localrefine. All120controls retain fullresults;40each3blockmodels notpooled. Breakslongcorrelations/createsseams;notglobalFAPorplanetodds.')
 save_json(O/'plan.json',plan);observed=evaluate(raw,seed,baseline)
 for a,b in zip(observed['windows'],source['windows']):assert a['best']==b['best'] and a['ranges']==b['timing_ranges']
 assert observed['eligible']==source['local_review_flag'];save_json(O/'observed.json',dict(result=observed,source_reproduced=True,inverted=evaluate([(t,2*np.median(y)-y,e) for t,y,e in raw],seed,baseline)))
 rows=[];perms=[]
 for length in plan['block_days']:
  for draw in range(40):
   rng=np.random.default_rng(np.random.SeedSequence([20261012,469309982,int(length*100),draw]));shuffled=[];ixs=[];offset=0
   for t,y,e in raw:
    ix=block_permutation(t,length,rng);shuffled.append((t,y[ix],e[ix]));ixs.append(ix+offset);offset+=len(t)
   result=evaluate(shuffled,seed,baseline);rows.append(dict(block_days=length,draw=draw,**result,exceeds=bool(result['eligible'] and result['statistic']>=observed['statistic'])));perms.append(np.concatenate(ixs))
  save_json(O/'results.json',rows);np.savez_compressed(O/'permutations.npz',indices=np.stack(perms));print('completed',length,flush=True)
 summary=[]
 for length in plan['block_days']:
  rr=[r for r in rows if r['block_days']==length];k=sum(r['exceeds'] for r in rr);summary.append(dict(block_days=length,k=k,n=40,local_flags=sum(r['eligible'] for r in rr),interval95=[0 if k==0 else float(beta.ppf(.025,k,41-k)),1 if k==40 else float(beta.ppf(.975,k+1,40-k))]))
 save_json(O/'summary.json',dict(status='complete',created_utc=now(),rows=summary,limitations='IntervalsMonteCarlowithinrandomizationmodelonly; noselection/modeluncertaintyincluded.'))
if __name__=='__main__':main()
