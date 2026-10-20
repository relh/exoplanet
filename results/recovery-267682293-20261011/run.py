from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
from exoplanet.campaign import process_target
p=Path(__file__).parent;src=Path('results/solar-radius-ranks2384-2896-20261011/targets/267682293.json');r=json.loads(src.read_text());assert r['status']=='error';rows=[]
for s in r['target']['training_sectors']:
 raw=Path(f'data/lightcurves/s{s:04d}-267682293.fits');meta=json.loads(Path(str(raw)+'.json').read_text());assert sha(raw)==meta['sha256']
 with fits.open(raw) as h:
  assert h[0].header['TICID']==267682293 and h[0].header['SECTOR']==s;a=h[1].data;q=(a['QUALITY']==0)&np.isfinite(a['TIME']);channels={}
  for name in ['SAP_FLUX','PDCSAP_FLUX']:
   v=np.asarray(a[name][q],float);v=v[np.isfinite(v)];channels[name]=dict(n_finite=len(v),n_positive=int((v>0).sum()),range=np.percentile(v,[0,50,100]).tolist())
 rows.append(dict(sector=s,path=str(raw),source=meta,channels=channels))
assert all(next(x for x in rows if x['sector']==s)['channels']['PDCSAP_FLUX']['n_positive']>200 for s in [7,8]);assert rows[-1]['sector']==9 and rows[-1]['channels']['PDCSAP_FLUX']['n_positive']==0
selected=dict(r['target']);selected['training_sectors']=[7,8];assert not Path('data/lightcurves/s0062-267682293.fits').exists()
save_json(p/'plan.json',dict(created_utc=now(),original_sha256=sha(src),target=selected,raw_diagnostics=rows,script_sha256=sha(Path(__file__)),source_hashes={q.name:sha(q) for q in Path('src/exoplanet').glob('*.py')},policy='Explicit recovery from original all-negative-flux sector9 error using the two valid adjacent original sectors7/8. Original error retained. No signal-outcome selection, no flux sign inversion, no heldout sector, unchanged gates.'))
(p/'targets').mkdir(exist_ok=False);process_target(selected,Path('data'),p)
