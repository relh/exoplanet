"""Retrospective reaggregation of saved event depths; no new flux or clock fitting."""
from pathlib import Path
import json,hashlib,datetime
import numpy as np
O=Path(__file__).parent
SOURCES={80387959:['results/followup-80387959-qlp90-100-20261009/heldout.json'],402358350:['results/heldout-402358350-s81-20261011/results.json'],241928959:['results/qlp-faint-midradius-single-review-20261011/241928959-peak0/frozen.json'],469309982:['results/followup-469309982-20261011/heldout.json','results/near-epoch-469309982-20261011/results.json'],96166003:['results/heldout-96166003-s59-20261012/results.json'],5546257:['results/followup-5546257-20261011/heldout.json']}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def rows(d):
 if isinstance(d,list):return d
 if 'rows' in d:return d['rows']
 if 'training_measurement' in d:return [{'measurement':d['training_measurement'],'name':'discovery-refined training (selected data)'}]
 return [d]
def combine(d,e):
 w=1/e**2;v=float(np.dot(w,d)/w.sum());error=float(1/np.sqrt(w.sum()));return {'depth':v,'error':error,'formal_snr':v/error}
assert not (O/'plan.json').exists()
save(O/'plan.json',{'created_utc':now(),'sources':SOURCES,'hashes':{p:sha(p) for ps in SOURCES.values() for p in ps},'script_sha256':sha(__file__),'policy':'All saved nominal measurements in listed files, including alternative clocks, retained. No profile_best scans. Inverse-variance mean of per-event depths is equivalent to common-depth fit with separate event intercepts, on events with >=2 inside and >=5 outside samples. Compare archived pooled total, retain incomplete-event distinction. Report every delete-one-event estimate when N>=2; no thresholds selected from result, no planet/false-alarm probabilities, no fresh holdout. Formal errors assume independent samples/events and do not propagate baseline trend or correlated noise. Discovery241 is selected training data; others later sectors have differing timing gates.'})
out=[]
for tic,paths in SOURCES.items():
 for path in paths:
  d=json.loads(Path(path).read_text())
  for index,r in enumerate(rows(d)):
   m=r['measurement'];events=m['events'];depths=np.array([x['depth'] for x in events]);errors=np.array([x['error'] for x in events]);assert np.all(np.isfinite(depths)) and np.all(errors>0)
   v={'tic':tic,'source':path,'row_index':index,'label':{k:r[k] for k in ['sector','name','role','family','window','conclusion'] if k in r},'pooled':m['total'],'n_events':len(events),'events':events}
   if len(events):
    v['matched']=combine(depths,errors);v['positive_events']=int((depths>0).sum());v['max_precision_fraction']=float(np.max(1/errors**2)/np.sum(1/errors**2));v['common_depth_chi2']=float(np.sum(((depths-v['matched']['depth'])/errors)**2));v['dof']=len(events)-1
    v['delete_one']=[{'omitted_event':events[j]['event'],**combine(np.delete(depths,j),np.delete(errors,j))} for j in range(len(events))] if len(events)>1 else []
    v['matched_minus_pooled_ppm']=None if m['total'] is None else 1e6*(v['matched']['depth']-m['total']['depth'])
   out.append(v)
save(O/'results.json',{'created_utc':now(),'plan_sha256':sha(O/'plan.json'),'rows':out})
for r in out:
 m=r.get('matched',{});loo=r.get('delete_one',[])
 print(r['tic'],r['label'],'N',r['n_events'],'matched',round(m.get('depth',0)*1e6,1),'+-',round(m.get('error',0)*1e6,1),'shift',round(r.get('matched_minus_pooled_ppm',0),1),'LOO',[(round(min(x['depth'] for x in loo)*1e6,1),round(max(x['depth'] for x in loo)*1e6,1))] if loo else [])
