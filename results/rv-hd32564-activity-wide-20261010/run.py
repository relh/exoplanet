"""Retrospective omitted-year checks conditional on contemporaneous activity."""
from pathlib import Path
import csv,json
import numpy as np
from astropy.time import Time
from exoplanet.rv_activity import fit_activity,predict_activity
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;source=Path('data/rv/HD32564.csv');raw=list(csv.DictReader(source.open()))
columns=['Halpha','RHKp','BIS','FWHM_DRS','dLW','CRX'];periods=[2.55663,11.06327,23.61185,49.10219]
assert sha(source)==json.loads(Path('results/user-posts-20261010/hd32564-source.json').read_text())['sha256']
assert not (out/'plan.json').exists()
sets={'none':[],'Halpha':[0],'RHKp':[1],'all_six':list(range(6))}
save_json(out/'plan.json',{'utc':now(),'source':str(source),'source_sha256':sha(source),'script_sha256':sha(Path(__file__)),'module_sha256':sha(Path('src/exoplanet/rv_activity.py')),'periods':periods,'neighborhood_fraction':.01,'reason':'Post-hoc sensitivity: several original +/-0.1% training fits reach a boundary; retain originals and compare +/-1% neighborhoods.','activity_columns':columns,'feature_sets':sets,'policy':'Common complete pre-upgrade rows for all feature sets; original f_RV==0, RVerror0..100, RHKp>0 and all activity finite with abs<1e6. Nightly RV inverse-variance averages also applied to contemporaneous activity; activity error ignored. Fixed2m/s nightly jitter; training-only predictor scaling and simultaneous linear activity+offset+trend+circular RV fit. Omitted years with>=20nights. All period neighborhoods seeded from known full-data modes +/-1%; retrospective conditional prediction, not blind forecast/confirmation. Held activity values are observed covariates. No GP or lagged model; all outcomes retained.','references':['https://arxiv.org/abs/2311.12438']})
records=[]
def serial(d):return {k:v.tolist() if isinstance(v,np.ndarray) else v for k,v in d.items()}
for rv,err in [('RV_mlc_nzp','e_RV_mlc_nzp'),('RV_drs_nzp','e_RV_drs_nzp')]:
 good=[r for r in raw if float(r['f_RV'])==0 and float(r['BJD'])<2457163 and np.isfinite(float(r[rv])) and 0<float(r[err])<100 and float(r['RHKp'])>0 and all(np.isfinite(float(r[k])) and abs(float(r[k]))<1e6 for k in columns)]
 nights=np.array([np.floor(float(r['BJD'])+.5) for r in good]);ts=[];ys=[];es=[];acts=[]
 for n in np.unique(nights):
  rows=[r for r,m in zip(good,nights==n) if m];w=np.array([1/float(r[err])**2 for r in rows]);ts.append(np.average([float(r['BJD']) for r in rows],weights=w));ys.append(np.average([float(r[rv]) for r in rows],weights=w));es.append(np.hypot(1/np.sqrt(w.sum()),2.));acts.append([np.average([float(r[k]) for r in rows],weights=w) for k in columns])
 t,y,e,a=map(np.array,[ts,ys,es,acts]);years=np.floor(Time(t,format='jd').decimalyear).astype(int)
 save_json(out/f'{rv}-nightly.json',{'time':t.tolist(),'rv':y.tolist(),'error':e.tolist(),'activity':a.tolist(),'years':years.tolist(),'n_raw_used':len(good),'n_raw_total':len(raw)})
 for name,indices in sets.items():
  act=a[:,indices]
  for year in np.unique(years):
   held=years==year;train=~held
   if held.sum()<20:continue
   full=fit_activity(t[train],y[train],e[train],act[train],periods,fraction=.01)
   pred=predict_activity(full,t[held],act[held]);resid=(y[held]-pred)/e[held]
   base=fit_activity(t[train],y[train],e[train],act[train],[],fraction=.01);basepred=predict_activity(base,t[held],act[held])
   drops=[]
   for i,p in enumerate(periods):
    reduced=fit_activity(t[train],y[train],e[train],act[train],periods[:i]+periods[i+1:],fraction=.01);rr=(y[held]-predict_activity(reduced,t[held],act[held]))/e[held]
    drops.append({'omitted_period':p,'held_delta_chi2':float(rr@rr-resid@resid),'reduced_training_model':serial(reduced)})
   row={'reduction':rv,'features':name,'year':int(year),'n_held':int(held.sum()),'n_train':int(train.sum()),'full_training_model':serial(full),'held_predictions':pred.tolist(),'held_rms':float(np.sqrt(np.mean((y[held]-pred)**2))),'base_held_rms':float(np.sqrt(np.mean((y[held]-basepred)**2))),'components':drops}
   records.append(row);save_json(out/'progress.json',records);print(rv,name,year,round(row['held_rms'],3),[(x['omitted_period'],round(x['held_delta_chi2'],2)) for x in drops],flush=True)
save_json(out/'results.json',records)
