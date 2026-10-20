from pathlib import Path
import json,numpy as np
from PRF import TESS_PRF
from exoplanet.prf_fit import fit_templates
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;r=json.loads((p/'fits.json').read_text());models=json.loads((p/'models.json').read_text());rows=[]
for meta,s in zip(models['sectors'],r['sectors']):
 z=np.load(p/f"s{s['sector']}-images.npz");prf=TESS_PRF(meta['camera'],meta['ccd'],s['sector'],meta['col'],meta['row'],localdatadir='data/prf-106583384-20261012/start_s0004');trials=[]
 for dx in [-.1,0,.1]:
  for dy in [-.1,0,.1]:
   fits=[]
   for h in s['hypotheses']:
    pos=np.array(s['positions'][h['tic']])+s['alignment']+np.array([dx,dy]);template=prf.locate(*pos,z['difference'].shape);f=fit_templates(z['difference'],z['error'],[template]);fits.append(dict(tic=h['tic'],chi2=f['chi2'],amplitude=float(f['coefficients'][0])))
   fits.sort(key=lambda h:h['chi2']);trials.append(dict(dx=dx,dy=dy,hypotheses=fits))
 rows.append(dict(sector=s['sector'],trials=trials));print(s['sector'],[x['hypotheses'][0]['tic'] for x in trials])
save_json(p/'registration-sensitivity.json',dict(fits_sha256=sha(p/'fits.json'),script_sha256=sha(Path(__file__)),offset_grid_pixels=[-.1,0,.1],sectors=rows,limits='Chosen perturbation grid, not a measured registration uncertainty or probability. Fixed scene registration plus each common offset; no photometry retuning.'))
