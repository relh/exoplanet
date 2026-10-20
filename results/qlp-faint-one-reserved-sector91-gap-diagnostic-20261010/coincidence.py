"""Post-selection event timing comparison; no probabilistic false-alarm claim."""
from pathlib import Path
import json,itertools
import astropy.units as u
from astropy.coordinates import SkyCoord
from exoplanet.pipeline import now,sha,save_json
out=Path(__file__).parent;p=out/'results.json';rows=[r for r in json.loads(p.read_text()) if r['tic']!=101436430]
centers=[r['full']['events'][-1]['center_btjd'] for r in rows]
pairs=[]
for a,b in itertools.combinations(rows,2):
 if a['tic']==b['tic']:continue
 sep=SkyCoord(a['ra']*u.deg,a['dec']*u.deg).separation(SkyCoord(b['ra']*u.deg,b['dec']*u.deg)).deg
 pairs.append({'a':[a['tic'],a['peak_index']],'b':[b['tic'],b['peak_index']],'separation_deg':float(sep)})
save_json(out/'coincidence.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'input_sha256':sha(p),'n_peaks':len(rows),'n_stars':len(set(r['tic'] for r in rows)),'last_centers_btjd':centers,'span_hours':24*(max(centers)-min(centers)),'pairs':pairs,'maximum_separation_deg':max(x['separation_deg'] for x in pairs),'interpretation':'Post-selection diagnostic: each two-event peak combines the noisy return interval with a last event near BTJD 3796.35. Broad sky separation and coincident last-event times favor shared systematics, but shared observing windows and selection affect this comparison. Not a calibrated false-alarm probability or proof that each individual dip is instrumental.'})
print('span hours',24*(max(centers)-min(centers)),'max separation deg',max(x['separation_deg'] for x in pairs))
