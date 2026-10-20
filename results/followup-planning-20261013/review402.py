"""Independent summary and nuisance-projected fit review; no network."""
from pathlib import Path
import json,hashlib,numpy as np
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent;P=ROOT/'results/resolved-followup-402-20261013';checks=0;hashes={}
def read(name):
 q=P/name;hashes[str(q.relative_to(ROOT))]=hashlib.sha256(q.read_bytes()).hexdigest();return json.loads(q.read_text())
def ck(x):
 global checks
 assert x
 checks+=1
plan=read('ztf-plan.json');result=read('ztf-results.json');summary=read('summary.json');manifest=read('ztf-cloud-results.json')
streams={}
for r in result['streams']:
 q=P/f"ztf-{r['oid']}-processed.npz";hashes[str(q.relative_to(ROOT))]=hashlib.sha256(q.read_bytes()).hexdigest();streams[r['oid']]={'filter':r['filterid'],'a':np.load(q)}
ck(sum(r['raw_count'] for r in result['streams'])==836==summary['raw_measurements']);ck(sum(r['quality_count'] for r in result['streams'])==545==summary['quality_measurements']);ck(len(result['measurements'])==72==summary['comparisons']);ck(len({(m['stream'],m['scale'],m['clock_index']) for m in result['measurements']})==72)
maxfiterr=0;maxnoiseerr=0
for m in result['measurements']:
 ids=sorted(k for k,v in streams.items() if v['filter']==int(m['stream'][-1])) if m['stream'].startswith('filter') else [int(m['stream'])]
 keep=np.array(m['kept_indices']);tt=np.concatenate([streams[k]['a'][m['scale']] for k in ids])[keep];yy=np.concatenate([streams[k]['a']['y'] for k in ids])[keep];ee=np.concatenate([streams[k]['a']['e'] for k in ids])[keep];oid=np.concatenate([np.full(len(streams[k]['a']['y']),k) for k in ids])[keep]
 row=plan['clocks'][m['clock_index']];b=row['best'];n=np.floor((tt-b['transit_time'])/b['period']+.5).astype(int);inside=np.abs(tt-b['transit_time']-n*b['period'])<b['duration']/2
 ck(int(inside.sum())==m['n_inside']);ck(sorted(set(n[inside]))==m['inside_cycles']);ck(len(tt)==m['n'])
 # Compare endpoint predictions directly, not the imported propagation routine.
 dist=[]
 for per,ep in row['ranges']['profile_timing_pairs']:
  epoch=ep+round((b['transit_time']-ep)/per)*per
  for k in [min(n),max(n)]:dist.append(abs(epoch+k*per-(b['transit_time']+k*b['period'])))
 spread=max(dist)+3*row['ranges']['conditional_epoch_floor_days']
 ck(abs(spread-m['timing_spread'])<1e-9)
 gate=spread+m['scale_difference_days']+1/86400<b['duration']/2 and len(m['inside_cycles'])>=2
 ck(not gate and m['outcome']=='inconclusive')
 if 'depth' not in m:continue
 # Frisch-Waugh-Lovell: weighted demeaning removes separate stream intercepts.
 w=1/ee**2;xx=-inside.astype(float);xr=xx.copy();yr=yy.copy()
 for k in ids:
  mask=oid==k;xr[mask]-=np.average(xx[mask],weights=w[mask]);yr[mask]-=np.average(yy[mask],weights=w[mask])
 norm=np.dot(w*xr,xr);depth=np.dot(w*xr,yr)/norm;error=norm**-.5;resid=yr-depth*xr;chi=np.dot(w*resid,resid);scaled=error*max(1,(chi/(len(yy)-len(ids)-1))**.5)
 maxfiterr=max(maxfiterr,abs(depth-m['depth']));maxnoiseerr=max(maxnoiseerr,abs(scaled-m['scatter_scaled_error']))
 ck(abs(depth-m['depth'])<1e-10);ck(abs(error-m['formal_error'])<1e-10);ck(abs(scaled-m['scatter_scaled_error'])<1e-10)
ck(max(abs(m.get('snr',0)) for m in result['measurements'])==summary['maximum_absolute_formal_snr']);ck(summary['maximum_absolute_formal_snr']<1.70)
for name in ['ASSESSMENT.md','verify_ztf.py','analyze_ztf.py','ztf-verification.json']:
 q=P/name;hashes[str(q.relative_to(ROOT))]=hashlib.sha256(q.read_bytes()).hexdigest()
report={'status':'pass_no_blocking_findings','checks':checks,'independent_fwl_max_depth_difference':maxfiterr,'independent_scaled_error_max_difference':maxnoiseerr,'conclusion':'All72 comparisons legitimately inconclusive under frozen timing/event gates. No exclusion of TIC74037550 or increased calibrated targetplanet probability follows. The report states these limits.','limits':'Read review and cached-output arithmetic; root runs raw-export/UTC/QR verifier separately. Does not validate aperture model, atmosphere, clock completeness, source isolation or astrophysical interpretation.','source_hashes':hashes}
(OUT/'402-review.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],checks,maxfiterr,maxnoiseerr)
