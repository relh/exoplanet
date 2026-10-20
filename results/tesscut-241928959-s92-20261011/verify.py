from pathlib import Path
import json,zipfile,hashlib,numpy as np
from astropy.io import fits
from exoplanet.pixel_vet import difference_events
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());files=read(out/'files.json');assert len(files)==1;f=files[0];p=Path(f['path']);assert sha(p)==f['sha256'];archive=Path('data/pixels/tesscut-241928959-s92.zip');assert sha(archive)==read(out/'source.json')['sha256']
with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read(f['member'])).hexdigest()==sha(p)
case=Path('results/qlp-faint-midradius-single-review-20261011/241928959-peak0');b=read(case/'frozen.json')['best'];a=read(out/'analysis.json');assert a['fit_sha256']==sha(case/'frozen.json');assert a['neighbor_sha256']==sha(Path('results/neighbors-241928959-20261011/neighbors.json'))
with fits.open(p) as h:
 assert h[0].header['SECTOR']==92 and h[1].header['TIMESYS']=='TDB' and h[1].header['BJDREFI']==2457000
 d=h[1].data;good=np.isfinite(d['TIME']);t=np.array(d['TIME'][good],float);flux=np.array(d['FLUX'][good],float);err=np.array(d['FLUX_ERR'][good],float);q=d['QUALITY'][good]
 diff,e,events,numbers=difference_events(t,flux,err,q,b)
 saved=np.load(out/'images.npz');np.testing.assert_array_equal(diff,saved['difference']);np.testing.assert_array_equal(e,saved['error']);np.testing.assert_array_equal(events,saved['event_differences']);assert list(numbers)==a['event_numbers']==[0,1,2,4,6]
c=read(out/'coverage.json');assert c['raw_sha256']==sha(p) and c['frozen_sha256']==sha(case/'frozen.json');bad=next(r for r in c['events'] if r['event']==3);assert bad['inside_quality_zero']==0 and bad['quality_counts']=={'2048':14}
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'analysis_sha256':sha(out/'analysis.json'),'raw_sha256':sha(p),'status':'ZIP member and raw/fit/neighbor hashes checked; all five difference arrays exactly reconstructed; fully flagged event3 excluded. Same photons, no independent validation or calibrated host probability.'})
print('five event arrays verified')
