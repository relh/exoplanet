from pathlib import Path
import json,csv,io
from astropy.coordinates import SkyCoord
import astropy.units as u
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent
r=json.loads((p/'results.json').read_text())[0]
d=json.loads((p/'discovery.json').read_text())
assert r['status']=='success' and sha(Path(r['path']))==r['sha256']
assert list(csv.DictReader(io.StringIO(Path(r['path']).read_text())))==r['rows']
b=next(x for x in r['rows'] if x['OID']=='4637399')
t=d['target']['star']; peak=d['screened_peaks'][0]['best']
s=SkyCoord(t['ra']*u.deg,t['dec']*u.deg).separation(SkyCoord(float(b['RAJ2000'])*u.deg,float(b['DEJ2000'])*u.deg)).arcsec
save_json(p/'verification.json',dict(status='passed',raw_catalog_hash_checked=True,neighbor_separation_arcsec_from_rounded_catalog_coordinates=s,period_difference_days=peak['period']-float(b['Period']),relative_period_difference=(peak['period']/float(b['Period'])-1),neighbor_identity=b['Name'].strip(),target_identity_not_equated_to_neighbor=True))
print(s, peak['period']-float(b['Period']))
