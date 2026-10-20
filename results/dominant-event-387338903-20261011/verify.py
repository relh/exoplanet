from pathlib import Path
import json,subprocess,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
p=Path(__file__).parent;before=json.loads((p/'diagnostic.json').read_text());subprocess.run(['uv','run','python',str(p/'analyze.py')],check=True);after=json.loads((p/'diagnostic.json').read_text());before.pop('created_utc');after.pop('created_utc');assert before==after
raw=Path('data/lightcurves/s0007-387338903.fits');assert sha(raw)==after['raw_sha256']
with fits.open(raw) as h:
 d=h[1].data;m=np.isfinite(d['TIME'])&(abs(d['TIME']-1514.345)<1)
 for k,v in after['raw_columns'].items():np.testing.assert_allclose(np.asarray(v,dtype=float),np.asarray(d[k][m],float),equal_nan=True)
save_json(p/'verification.json',dict(status='passed',verified_utc=now(),omission_measurements_reproduced=2,raw_columns_reconstructed=True,script_sha256=sha(p/'analyze.py'),limits='Same-algorithm reproduction and raw-data check; posthoc event omission and telemetry coincidence do not identify physical cause.'))
