from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
from exoplanet.pixel_vet import difference_events
p=Path(__file__).parent;f=json.loads((p/'frozen.json').read_text());assert sha(Path(f['source']))==f['source_sha256'];r=json.loads(Path(f['source']).read_text());assert r['screened_peaks'][0]['best']==f['best'];events_checked=0
for sector in [40,41]:
 raw=Path(f'data/pixels/137151335-s{sector:04d}.fits')
 with fits.open(raw) as h:
  assert h[0].header['TICID']==137151335 and h[0].header['SECTOR']==sector
  d=h[1].data;m=np.isfinite(d['TIME']);diff,sigma,events,nums=difference_events(np.asarray(d['TIME'][m],float),np.asarray(d['FLUX'][m],float),np.asarray(d['FLUX_ERR'][m],float),d['QUALITY'][m],f['best'])
 q=Path('results/prf-137151335-20261011');z=np.load(q/f's{sector}-images.npz');np.testing.assert_array_equal(diff,z['difference']);np.testing.assert_array_equal(sigma,z['error']);np.testing.assert_array_equal(events,z['event_differences']);saved=next(x for x in json.loads((q/'fits.json').read_text())['sectors'] if x['sector']==sector);assert nums==[x['event'] for x in saved['events']];events_checked+=len(nums)
assert not Path('data/lightcurves/s0075-137151335.fits').exists()
save_json(p/'verification.json',dict(status='passed',verified_utc=now(),n_events_reproduced=events_checked,n_sectors=2,clock_unchanged=True,reserved_unopened=True,limitations='Known-planet source-control reproduction only. Failed individual moment calculation retained separately; no event excluded.'))
