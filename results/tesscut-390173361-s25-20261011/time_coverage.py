from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent
fp=Path('results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/390173361-peak0/frozen.json');b=json.loads(fp.read_text())['best']
p=Path(json.loads((out/'files.json').read_text())[0]['path'])
with fits.open(p) as h:t=np.asarray(h[1].data['TIME']);t=np.sort(t[np.isfinite(t)])
rows=[]
for n in range(int(np.floor((t.min()-b['transit_time'])/b['period'])),int(np.ceil((t.max()-b['transit_time'])/b['period']))+1):
 c=b['transit_time']+n*b['period'];before=t[t<c];after=t[t>c]
 rows.append({'event':n,'center':c,'inside_time_span':bool(t.min()<=c<=t.max()),'nearest_exposure_distance_days':float(abs(t-c).min()),'preceding_time':float(before[-1]) if len(before) else None,'following_time':float(after[0]) if len(after) else None})
save_json(out/'time_coverage.json',{'script_sha256':sha(Path(__file__)),'raw_sha256':sha(p),'frozen_sha256':sha(fp),'time_range':[float(t.min()),float(t.max())],'duration':b['duration'],'windows':rows});print(rows)
