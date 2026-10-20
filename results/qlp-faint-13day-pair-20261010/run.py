"""Post-hoc comparison of two selected signals; no causal attribution."""
from pathlib import Path
import json
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits
import astropy.units as u
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
out=Path(__file__).parent;tics=[198186473,233194992];targets={};frozen={};sources={}
for tic in tics:
 p=Path(f'results/qlp-faint-expanded-20261010/targets/{tic}.json');q=Path(f'results/qlp-faint-expanded-followup-20261010/{tic}-peak0/frozen.json')
 targets[tic]=json.loads(p.read_text())['target'];frozen[tic]=json.loads(q.read_text());sources[str(tic)]={'discovery_sha256':sha(p),'frozen_sha256':sha(q)}
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'sources':sources,'script_sha256':sha(Path(__file__)),'policy':'Post-hoc selected-pair comparison using existing training only. Compare coordinates, detector headers, predicted centers and measurements at each frozen ephemeris. No new epochs, fitting, causal attribution or calibrated significance.'})
a,b=[targets[t]['star'] for t in tics];sep=SkyCoord(a['ra']*u.deg,a['dec']*u.deg).separation(SkyCoord(b['ra']*u.deg,b['dec']*u.deg)).deg
rows=[]
for tic in tics:
 target=targets[tic];t,y,e,data=load_qlp(target,Path('data'),bin_minutes=0);headers=[]
 for s in target['training_sectors']:
  path=Path(f'data/qlp/{tic}-s{s:04d}.fits')
  with fits.open(path) as h:headers.append({'sector':s,'sha256':sha(path),'camera':h[0].header.get('CAMERA'),'ccd':h[0].header.get('CCD')})
 measurements={str(other):fixed_measure(t,y,e,**dict(zip(['period','epoch','duration'],[frozen[other]['best'][k] for k in ['period','transit_time','duration']]))) for other in tics}
 rows.append({'tic':tic,'data':data,'detectors':headers,'measurements_by_ephemeris':measurements})
b1,b2=[frozen[t]['best'] for t in tics];offsets=[]
for n in range(8):
 c1=b1['transit_time']+n*b1['period'];m=round((c1-b2['transit_time'])/b2['period']);c2=b2['transit_time']+m*b2['period'];offsets.append({'first_center':c1,'second_center':c2,'offset_days':c2-c1,'boxes_overlap':abs(c2-c1)<(b1['duration']+b2['duration'])/2})
save_json(out/'results.json',{'finished_utc':now(),'separation_degrees':sep,'center_offsets':offsets,'rows':rows})
print('separation',sep,'offsets',offsets)
for r in rows:print(r['tic'],r['detectors'],{k:v['total'] for k,v in r['measurements_by_ephemeris'].items()})
