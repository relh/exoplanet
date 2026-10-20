from pathlib import Path
import json,numpy as np
from astropy.coordinates import SkyCoord
from astropy.time import Time
import astropy.units as u
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());p=read(out/'plan.json');r=read(out/'fits.json');gp=Path('results/gaia-156001092-scene-20261011');a=read(gp/'astrometry-audit.json');sources={s['source_id']:s for s in read(gp/'gaia_source.json')}
assert p['script_sha256']==sha(out/'analyze.py') and p['module_sha256']==sha(Path('src/exoplanet/prf_fit.py'))
for n,h in p['inputs'].items():assert sha(Path(n))==h
for n,h in a['inputs'].items():assert sha(Path(n))==h
assert a['script_sha256']==sha(gp/'audit.py') and a['query_script_sha256']==sha(gp/'query.py')
assert r['plot_sha256']==sha(out/'comparison.png') and r['images_sha256']==sha(out/'images.npz')
assert len(r['scene_ids'])==13 and sum(x['unique_complete_mapping'] for x in a['rows'])==11
checks=[]
for row in a['rows']:
 for m in row['mappings']:
  s=sources[m['mapping']['dr3_source_id']];c=SkyCoord(ra=float(s['ra'])*u.deg,dec=float(s['dec'])*u.deg,pm_ra_cosdec=float(s['pmra'])*u.mas/u.yr,pm_dec=float(s['pmdec'])*u.mas/u.yr,obstime=Time(float(s['ref_epoch']),format='jyear'));new=c.apply_space_motion(Time(a['epoch_jyear'],format='jyear'));linear=SkyCoord(*m['propagated_radec'],unit='deg');sep=float(new.separation(linear).arcsec);assert sep<.001;checks.append(sep)
assert len(r['controls'])==6 and all(x['max_amplitude_error']<1e-6 for x in r['controls'])
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'fits_sha256':sha(out/'fits.json'),'astrometry_sha256':sha(gp/'astrometry-audit.json'),'max_linear_vs_astropy_arcsec':max(checks),'status':'provenance, position propagation comparison and exact-template controls passed; not source validation'})
print('Verified astrometry and scene inputs.')
