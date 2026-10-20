from pathlib import Path
import json,numpy as np
R=Path(__file__).parent;a=json.loads((R/'analysis.json').read_text());out=[]
for pol in ['strict','relaxed']:
 for r in a['rows']:
  if not(r[pol] and r['robust_in']):continue
  base=[x for x in a['rows'] if x[pol] and x['band']==r['band'] and x['night']!=r['night'] and not x['possible_in']];w=np.array([1/x['error']**2 for x in base]);m=np.array([x['mag'] for x in base]);mean=float(np.sum(w*m)/sum(w));e=float(np.sqrt(r['error']**2+1/sum(w)));d=r['mag']-mean
  out.append({'quality':pol,'band':r['band'],'event':r['event'],'baseline_n':len(base),'baseline_nights':len(set(x['night'] for x in base)),'in_mag':r['mag'],'baseline_weighted_mag':mean,'delta_mag':d,'formal_error':e,'formal_3sigma_upper_mag':d+3*e,'baseline_scatter_mag':float(np.std(m,ddof=1)),'fractional_dimming':1-10**(-0.4*d),'repeat_gate_pass':False})
(R/'comparisons.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
