from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
from exoplanet.archive import qlp_flux_columns
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());p=read(out/'plan.json');r=read(out/'result.json')
assert sha(Path(p['parent_path']))==p['parent_sha256'] and sha(out/'run.py')==p['script_sha256']
for n,h in p['source_hashes'].items():assert sha(Path('src/exoplanet')/n)==h
assert r==read(out/'targets/139343242.json') and r['target']==p['target']
assert r['status']=='screened' and r['disposition']=='below_screen_threshold' and r['screened_peaks']==[]
assert r['target']['training_sectors']==[45,47] and r['target']['heldout_sectors']==[44]
assert not Path('data/qlp/139343242-s0044.fits').exists()
assert [d['sector'] for d in r['data']]==[45,47]
for d in r['data']:assert sha(Path(f"data/qlp/139343242-s{d['sector']:04d}.fits"))==d['source']['sha256']
bad=Path('data/qlp/139343242-s0046.fits')
with fits.open(bad) as h:
 assert h[0].header['TICID']==139343242 and h[0].header['SECTOR']==46
 d=h[1].data;fc,ec,_=qlp_flux_columns(d.names)
 assert np.isfinite(d[fc]).sum()==np.isfinite(d[ec]).sum()==0
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'plan_sha256':sha(out/'plan.json'),'result_sha256':sha(out/'result.json'),'excluded_sector46_sha256':sha(bad),'status':'Parent preserved; unusable46 independently checked;45/47 identity and raw hashes checked; reserve44 unopened; below threshold result verified. Not a planet exclusion.'})
print(r['disposition'],r['best']['depth_snr'],r['clean_baseline_days'])
