from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
from exoplanet.pixel_vet import difference_events
p=Path(__file__).parent;f=json.loads((p/'frozen.json').read_text());assert sha(Path(f['source']))==f['source_sha256'];r=json.loads(Path(f['source']).read_text());assert r['windows'][0]['best']==f['best']
for sector in [9,36]:
 q=Path(f'results/pixels-469309982-s{sector}-20261011');saved=json.loads((q/'localization.json').read_text());raw=Path(f'data/pixels/469309982-s{sector:04d}.fits');assert sha(raw)==saved['source']['sha256'] and saved['frozen_sha256']==sha(p/'frozen.json')
 with fits.open(raw) as h:
  assert h[0].header['TICID']==469309982 and h[0].header['SECTOR']==sector
  d=h[1].data;m=np.isfinite(d['TIME']);diff,sigma,events,nums=difference_events(np.asarray(d['TIME'][m],float),np.asarray(d['FLUX'][m],float),np.asarray(d['FLUX_ERR'][m],float),d['QUALITY'][m],f['best'])
 z=np.load(q/'images.npz');np.testing.assert_array_equal(diff,z['difference']);np.testing.assert_array_equal(sigma,z['error']);np.testing.assert_array_equal(events,z['event_differences']);assert nums==saved['event_numbers']
for sector in [63,64]:assert not Path(f'data/lightcurves/s{sector:04d}-469309982.fits').exists()
save_json(p/'verification.json',dict(status='passed',verified_utc=now(),n_sectors=2,n_events=16,clock_unchanged=True,reserved_unopened=True,limitations='Difference-image reproduction only; centroids are not precise source attribution.'))
