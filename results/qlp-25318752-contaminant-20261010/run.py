"""Measure neighboring source at target's pre-existing frozen ephemeris."""
from pathlib import Path
import json
import numpy as np
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
out=Path(__file__).parent;assert not (out/'plan.json').exists()
f=Path('results/qlp-25324731-expanded-20261010/followup/frozen.json');b=json.loads(f.read_text())['best']
p=Path('results/qlp-25324731-catalogs-20261010/25324731-neighbors.json');neighbors=json.loads(p.read_text());star=next(r for r in neighbors if int(r['ID'])==25318752)
idstr=f'{25318752:016d}';parts='/'.join(idstr[i:i+4] for i in range(0,16,4));products={str(s):{'dataURL':f'mast:HLSP/qlp/s{s:04d}/{parts}/hlsp_qlp_tess_ffi_s{s:04d}-{idstr}_tess_v01_llc.fits'} for s in [8,9,35]}
target={'tic':25318752,'training_sectors':[8,9,35],'qlp_products':products,'star':star,'estimate_missing_errors':True}
save_json(out/'plan.json',{'utc':now(),'target':target,'frozen_sha256':sha(f),'neighbors_sha256':sha(p),'script_sha256':sha(Path(__file__)),'policy':'Construct standard QLP product URI for bright off-target pixel source; FITS TIC/sector headers validated by loader. Fixed existing ephemeris; no period or phase optimization. Separate extraction of same observations, not independent data.'})
rows=[];curves=[]
for s in target['training_sectors']:
 try:
  t,y,e,data=load_qlp(dict(target,training_sectors=[s]),Path('data'),bin_minutes=0)
  m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);rows.append({'sector':s,'status':'measured','data':data,'measurement':m});curves.append((s,t,y,e))
 except Exception as exc:rows.append({'sector':s,'status':'error','error':repr(exc)})
 save_json(out/'measurements.json',rows)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axes=plt.subplots(len(curves),1,figsize=(10,3*len(curves)),squeeze=False,constrained_layout=True)
for ax,(s,t,y,e) in zip(axes[:,0],curves):
 phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2
 ax.plot(phase,y,'.',ms=2);ax.axvspan(-b['duration']/2,b['duration']/2,color='red',alpha=.15);ax.set(title=f'TIC25318752 sector{s}',xlabel='Days from frozen target event',ylabel='Normalized flux')
fig.savefig(out/'fixed-phase.png',dpi=130)
for r in rows:print(r['sector'],r.get('measurement',{}).get('total',r.get('error')),flush=True)
