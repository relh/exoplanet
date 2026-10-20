"""Compare one-component daily/yearly aliases in omitted-year predictions."""
from pathlib import Path
import json
import numpy as np
from exoplanet.pipeline import save_json,sha,now
from exoplanet.rv_activity import fit_activity,predict_activity
out=Path(__file__).parent;parent=Path('results/rv-hd32564-activity-wide-20261010')
periods=np.array([2.55663,11.06327,23.61185,49.10219]);sampling={'solar_day':1.,'sidereal_day':1+1/365.25,'year':1/365.25}
variants=[]
for i,p in enumerate(periods):
 for label,f in sampling.items():
  for sign in [-1,1]:
   seeds=periods.copy();seeds[i]=1/abs(1/p+sign*f)
   variants.append({'component':i,'original_period':float(p),'sampling':label,'sign':sign,'seeds':seeds.tolist()})
assert not (out/'plan.json').exists()
sources={r:{'path':str(parent/f'{r}-nightly.json'),'sha256':sha(parent/f'{r}-nightly.json')} for r in ['RV_mlc_nzp','RV_drs_nzp']}
save_json(out/'plan.json',{'utc':now(),'variants':variants,'sources':sources,'script_sha256':sha(Path(__file__)),'module_sha256':sha(Path('src/exoplanet/rv_activity.py')),'policy':'One replaced component at a time: abs(f +/-1day^-1, +/-1.0027379day^-1, +/-1/365.25day^-1). Parent and alias models use identical nightly complete sample, held years>=20nights, fixed2m/sjitter, no activity or all6linear indicators. Per-period fractional neighborhood=min(.02,.45*period/trainingbaseline), fit on training only. Parent seeds from externally reported already-opened modes. Retrospective conditional prediction, not blind confirmation. Local optimization and one-component aliases only; no exhaustive combinations, eccentric harmonics or GP. Smaller heldchi2 wins; no calibrated probability.','references':['https://arxiv.org/abs/1005.4050']})
records=[];windows=[]
def serial(d):return {k:v.tolist() if isinstance(v,np.ndarray) else v for k,v in d.items()}
for reduction,source in sources.items():
 data=json.loads(Path(source['path']).read_text());t,y,e,a,years=[np.array(data[k]) for k in ['time','rv','error','activity','years']]
 for features,act in [('none',a[:,:0]),('all_six',a)]:
  for year in np.unique(years):
   held=years==year;train=~held
   if held.sum()<20:continue
   base=np.ptp(t[train]);weights=1/e[train]**2
   windows.append({'reduction':reduction,'features':features,'year':int(year),'window_amplitudes':{k:float(abs(np.sum(weights*np.exp(2j*np.pi*f*(t[train]-t[train].mean()))))/weights.sum()) for k,f in sampling.items()}})
   frac=np.minimum(.02,.45*periods/base);main=fit_activity(t[train],y[train],e[train],act[train],periods,fraction=frac)
   resid=(y[held]-predict_activity(main,t[held],act[held]))/e[held];chi2=float(resid@resid)
   for variant in variants:
    seeds=np.array(variant['seeds']);fraction=np.minimum(.02,.45*seeds/base)
    row={'reduction':reduction,'features':features,'year':int(year),'n_held':int(held.sum()),'variant':variant,'parent_model':serial(main),'parent_held_chi2':chi2,'period_fraction':fraction.tolist()}
    try:
     model=fit_activity(t[train],y[train],e[train],act[train],seeds,fraction=fraction)
     rr=(y[held]-predict_activity(model,t[held],act[held]))/e[held]
     row.update(status='complete',alias_model=serial(model),held_chi2_alias_minus_parent=float(rr@rr-chi2),alias_bound_hit=bool(np.any(abs(model['periods']/seeds-1)>=fraction*.99)),parent_bound_hit=bool(np.any(abs(main['periods']/periods-1)>=frac*.99)))
    except Exception as exc:row.update(status='error',error=repr(exc))
    records.append(row)
   save_json(out/'progress.json',records);print(reduction,features,year,'finished',len(records),flush=True)
save_json(out/'windows.json',windows);save_json(out/'results.json',records)
