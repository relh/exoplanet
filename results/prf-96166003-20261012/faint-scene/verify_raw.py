from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pixel_vet import difference_events,individual_difference_events
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;f=Path('results/source-check-96166003-20261011/frozen.json');frozen=json.loads(f.read_text());assert sha(Path(frozen['source']))==frozen['source_sha256'];b=frozen['best'];count=0
for meta in json.loads((p/'models.json').read_text())['sectors']:
 path=Path(meta['pixel_path']);assert sha(path)==meta['pixel_sha256']
 with fits.open(path) as h:
  assert h[0].header['TICID']==96166003 and h[0].header['SECTOR']==meta['sector'];a=h[1].data;ok=np.isfinite(a['TIME']);t=np.asarray(a['TIME'][ok],float);flux=np.asarray(a['FLUX'][ok],float);err=np.asarray(a['FLUX_ERR'][ok],float);quality=a['QUALITY'][ok]
 diff,sigma,events,numbers=difference_events(t,flux,err,quality,b);es,vs,ns=individual_difference_events(t,flux,err,quality,b);assert ns==numbers
 z=np.load(p/f"s{meta['sector']}-images.npz")
 for key,arr in [('difference',diff),('error',sigma),('event_differences',es),('event_variances',vs)]:np.testing.assert_allclose(z[key],arr)
 count+=len(ns)
save_json(p/'raw-verification.json',dict(status='passed',individual_differences_reconstructed=count,clock_provenance_checked=True))
