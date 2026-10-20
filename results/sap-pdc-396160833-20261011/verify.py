from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());rs=json.loads((p/'results.json').read_text())['rows'];b=plan['clock']
for path,digest in plan['inputs'].items():assert sha(Path(path))==digest
for r in rs:
 arrays=[]
 for meta in r['counts']:
  with fits.open(meta['path']) as h:
   d=h[1].data;mask=(d['QUALITY']==0)&np.isfinite(d['TIME'])
   for key in ['SAP_FLUX','SAP_FLUX_ERR','PDCSAP_FLUX','PDCSAP_FLUX_ERR']:mask &= np.isfinite(d[key])&(d[key]>0)
   a=flatten(np.asarray(d['TIME'][mask],float),np.asarray(d[r['kind']+'_FLUX'][mask],float),np.asarray(d[r['kind']+'_FLUX_ERR'][mask],float),window=r['window']);assert int(mask.sum())==meta['common_input_points'] and len(a[0])==meta['clean_points'];arrays.append(a)
 t,y,e=[np.concatenate([a[k] for a in arrays]) for k in range(3)];assert fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration'])==r['measurement']
 z=np.load(p/f"{r['kind']}-{r['window']}.npz")
 for key,a in [('t',t),('y',y),('e',e)]:np.testing.assert_allclose(z[key],a)
save_json(p/'verification.json',dict(status='passed',raw_reconstructions=4,hashes_checked=True,limits='Shared photons, no independent confirmation; formal noise does not model all instrumental errors.'))
