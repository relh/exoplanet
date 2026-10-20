from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
from exoplanet.campaign import load_training,joint_scan
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());r=json.loads((p/'targets/267682293.json').read_text());assert sha(Path('results/solar-radius-ranks2384-2896-20261011/targets/267682293.json'))==plan['original_sha256'];assert r['target']==plan['target'];assert plan['created_utc']<=r['started_utc'];assert r['target']['training_sectors']==[7,8]
for name,digest in plan['source_hashes'].items():assert sha(Path('src/exoplanet')/name)==digest
for d in plan['raw_diagnostics']:
 assert sha(Path(d['path']))==d['source']['sha256']
 with fits.open(d['path']) as h:
  assert h[0].header['TICID']==267682293 and h[0].header['SECTOR']==d['sector'];a=h[1].data;q=(a['QUALITY']==0)&np.isfinite(a['TIME'])
  for name,z in d['channels'].items():
   v=np.asarray(a[name][q],float);v=v[np.isfinite(v)];assert len(v)==z['n_finite'] and int((v>0).sum())==z['n_positive'];np.testing.assert_array_equal(np.percentile(v,[0,50,100]),z['range'])
t,y,e,_=load_training(r['target'],Path('data'));_,_,best=joint_scan(t,y,e);assert best==r['best'];assert r['disposition']=='below_screen_threshold' and r['screened_peaks']==[];assert not Path('data/lightcurves/s0062-267682293.fits').exists()
save_json(p/'verification.json',dict(status='passed',original_error_preserved=True,raw_products_checked=3,source_hashes_checked=True,recovery_search_peak_reproduced=True,reserved_cache_absent=True,limits='A separate two-sector recovery, not a replacement of the original failed three-sector run or a planet exclusion.'))
print(best)
