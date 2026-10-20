from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
plan=read(out/'plan.json');assert sha(Path(plan['original_path']))==plan['original_sha256']
checks=read(out/'sector-checks.json');sel=read(out/'selection.json');result=read(out/'result.json')
assert sel['usable_sectors']==[45] and sel['target'] is None
assert result['status']=='insufficient_training_coverage'
assert sha(out/'sector-checks.json')==sel['sector_checks_sha256']
for r in checks:
 raw=Path(f"data/qlp/275133703-s{r['sector']:04d}.fits")
 assert sha(raw)==r['raw_sha256']==r['download_provenance']['sha256']
assert checks[0]['status']=='usable' and checks[0]['n_clean']==2432
assert checks[1]['status']=='error' and 'Insufficient adjacent samples for empirical errors' in checks[1]['error']
assert all(not Path(f'data/qlp/275133703-s{s:04d}.fits').exists() for s in plan['target']['heldout_sectors'])
from astropy.io import fits
from exoplanet.archive import qlp_flux_columns
import numpy as np
with fits.open('data/qlp/275133703-s0046.fits') as h:
 fc,ec,_=qlp_flux_columns(h[1].data.names);assert len(h[1].data)==1880 and np.isfinite(h[1].data[fc]).sum()==0
save_json(out/'verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'original_sha256':plan['original_sha256'],'selection_sha256':sha(out/'selection.json'),'result_sha256':sha(out/'result.json'),'limits':'Only sector45 usable under unchanged preprocessing; no alternate period search run, no holdout opened, no planet exclusion.'})
print('Verified retained failure and insufficient two-sector coverage')
