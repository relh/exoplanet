from pathlib import Path
import csv,json,hashlib,numpy as np
from astropy.time import Time
from scipy.linalg import solve_triangular
p=Path(__file__).parent
checks=[]
def ck(v,label):
 assert v,label
 checks.append(label)
for f in p.glob('*.json'):
 d=json.loads(f.read_text())
 if isinstance(d,dict) and 'path' in d and 'sha256' in d:ck(hashlib.sha256(Path(d['path']).read_bytes()).hexdigest()==d['sha256'],f.name+' raw hash')
plan=json.loads((p/'epoch-plan.json').read_text());result=json.loads((p/'epoch-results.json').read_text());src=json.loads((p/'epoch-source.json').read_text());rows=list(csv.DictReader(Path(src['path']).open()));good=[]
for r in rows:
 ck(r['source_id']==plan['source_id'],'source identity')
 if r['variability_flag_g_reject']!='false' or r['rejected_by_photometry']!='false':continue
 vals=[float(r[k]) for k in ['g_transit_time','g_transit_flux','g_transit_flux_error']]
 if all(np.isfinite(vals)) and vals[1]>0 and vals[2]>0:good.append(vals)
a=np.array(good);t=Time(2455197.5,a[:,0],format='jd',scale='tcb').tdb.jd-2457000.;y=a[:,1]/np.median(a[:,1]);e=a[:,2]/np.median(a[:,1]);saved=np.load(p/'gaia-processed.npz');ck(np.max(abs(t-saved['t']))<1e-8,'two-part JD time conversion');ck(len(t)==result['quality_count']==43,'quality count');ck(np.allclose(y,saved['y']) and np.allclose(e,saved['e']),'normalization')
for c,r in zip(plan['clocks'],result['fixed_tests']):
 b=c['best'];n=np.floor((t-b['transit_time'])/b['period']+.5);dist=abs(t-b['transit_time']-n*b['period']);i=dist<b['duration']/2;o=dist>1.5*b['duration'];m=r['measurement'];ck(i.sum()==m['n_inside'] and o.sum()==m['n_outside'],'independent phase counts');cy=np.unique(n[i]).astype(int).tolist();ck(cy==m['event_cycles'],'event cycles')
 bounds=[round((x-b['transit_time'])/b['period']) for x in [min(t),max(t)]];offset=[]
 for per,ep in c['ranges']['profile_timing_pairs']:
  ep+=round((b['transit_time']-ep)/per)*per
  for k in bounds:offset.append(abs(ep-b['transit_time']+k*(per-b['period'])))
 spread=max(offset,default=0)+3*c['ranges']['conditional_epoch_floor_days'];ck(abs(spread-m['timing_spread_days'])<1e-8,'independent timing profile propagation')
 if i.any() and o.any():
  use=i|o;X=np.column_stack([np.ones(use.sum()),-i[use].astype(float)]);Q,R=np.linalg.qr(X/e[use,None]);coef=solve_triangular(R,Q.T@(y[use]/e[use]));cov=np.linalg.inv(R)@np.linalg.inv(R).T;ck(abs(coef[1]-m['depth'])<1e-10 and abs(np.sqrt(cov[1,1])-m['formal_error'])<1e-10,'independent QR depth and error')
 ck(m['outcome']=='inconclusive' and (spread>=b['duration']/2 or len(cy)<2),'no fixed-clock exclusion')
for peak in result['exploratory']['peaks']:
 angle=2*np.pi*t/peak['period'];X=np.column_stack([np.ones(len(t)),np.sin(angle),np.cos(angle)]);coef=np.linalg.lstsq(X/e[:,None],y/e,rcond=None)[0];chi=np.sum(((y-X@coef)/e)**2);base=np.sum(((y-np.average(y,weights=1/e**2))/e)**2);ck(abs(1-chi/base-peak['power'])<1e-6,'independent sinusoid power')
(p/'verification.json').write_text(json.dumps({'status':'passed','checks':checks,'scope':'Gaia measurements, metadata raw hashes; ZTF separately verified if downloaded.'},indent=2)+'\n');print('PASS',len(checks))
