from pathlib import Path
import hashlib,json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text())
p=read(out/'plan.json');m=read(Path('results/prf-149919534-20261011/models.json'));r=read(out/'fits.json');bc=read(out/'broader-controls.json');bp=read(out/'broader-controls-plan.json')
assert p['script_sha256']==sha(out/'analyze.py') and p['module_sha256']==sha(Path('src/exoplanet/prf_fit.py'))
assert m['script_sha256']==sha(Path('results/prf-149919534-20261011/download_models.py'))
for name,h in p['inputs'].items():assert sha(Path(name))==h
for s in m['sectors']:
 assert s['sector']==75 and sha(Path(s['pixel_path']))==s['pixel_sha256']
 for f in s['models']:assert sha(Path(f['path']))==f['source']['sha256']
assert r['plot_sha256']==sha(out/'comparison.png') and r['images_sha256']==sha(out/'images.npz')
assert len(r['controls'])==6 and all(i['max_amplitude_error']<1e-6 for i in r['controls'])
assert bp['script_sha256']==sha(out/'broader_controls.py') and bc['plan_sha256']==sha(out/'broader-controls-plan.json')
assert bp['images_sha256']==sha(out/'images.npz') and bp['fits_sha256']==sha(out/'fits.json')
fp=Path('results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/149919534-peak0/frozen.json')
assert bp['frozen_sha256']==sha(fp);b=read(fp)['best']
with fits.open(s['pixel_path']) as h:
 d=h[1].data;t=np.asarray(d['TIME'],float);ok=np.isfinite(t);t=t[ok];q=d['QUALITY'][ok]
phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;valid=(q==0)&(abs(phase)>b['duration'])
assert len(bc['rows'])==36
assert {(x['event'],x['fraction']) for x in bc['rows']}=={(n,f) for n in [1,2] for f in bp['fractions']}
windows={};attempts=[]
for row in bc['rows']:
 center=b['transit_time']+(row['event']+row['fraction'])*b['period'];dt=abs(t-center)
 inside=valid&(dt<b['duration']/2);outside=valid&(dt>b['duration'])&(dt<3*b['duration'])
 assert (int(inside.sum()),int(outside.sum()))==(row['inside'],row['outside'])
 if inside.sum()<2 or outside.sum()<5:
  assert row['status']=='insufficient_coverage';continue
 assert row['status']=='measured' and row['max_injection_difference_error']<1e-6
 key=hashlib.sha256(inside.tobytes()+outside.tobytes()).hexdigest()
 if key in windows:
  assert all(abs(windows[key]['amplitudes'][i]-row['amplitudes'][i])<1e-10 for i in r['scene_ids'])
 else:windows[key]=dict(row,center_btjd=center)
 attempts.append({'event':row['event'],'fraction':row['fraction'],'mask_sha256':key})
summary={'measured_rows':len(attempts),'unique_windows':len(windows),'insufficient_rows':36-len(attempts),'windows':list(windows.values()),'attempts':attempts,'ranges':{}}
for tic in ['149919534','149919536','149919530']:
 vals=[c['amplitudes'][tic] for c in windows.values()];summary['ranges'][tic]=[min(vals),max(vals)]
assert len(attempts)==13 and len(windows)==8
save_json(out/'control-summary.json',summary)
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'fits_sha256':sha(out/'fits.json'),'broader_controls_sha256':sha(out/'broader-controls.json'),'summary_sha256':sha(out/'control-summary.json'),'status':'Raw/model provenance, six exact-template controls, 36 window attempts, exact-mask deduplication and linear injection responses verified. No physical source validation.'})
print('Verified:',summary['measured_rows'],'measured rows;',summary['unique_windows'],'unique;',summary['insufficient_rows'],'missing; ranges',summary['ranges'])

from astropy.coordinates import SkyCoord
from astropy.time import Time
import astropy.units as u
gp=Path('results/gaia-149919534-scene-20261011');a=read(gp/'astrometry-audit.json');sources={s['source_id']:s for s in read(gp/'gaia_source.json')}
assert a['script_sha256']==sha(gp/'audit.py') and a['query_script_sha256']==sha(gp/'query.py')
for name,h in a['inputs'].items():assert sha(Path(name))==h
checks=[]
for row in a['rows']:
 for mapping in row['mappings']:
  if not mapping.get('proper_motion_available'):continue
  src=sources[mapping['mapping']['dr3_source_id']]
  coord=SkyCoord(ra=float(src['ra'])*u.deg,dec=float(src['dec'])*u.deg,pm_ra_cosdec=float(src['pmra'])*u.mas/u.yr,pm_dec=float(src['pmdec'])*u.mas/u.yr,obstime=Time(float(src['ref_epoch']),format='jyear'))
  propagated=coord.apply_space_motion(Time(a['epoch_jyear'],format='jyear'));linear=SkyCoord(*mapping['propagated_radec'],unit='deg');sep=float(propagated.separation(linear).arcsec);assert sep<.001;checks.append(sep)
assert r['scene_ids']==read(Path('results/prf-149919534-20261011/fits.json'))['scene_ids']
save_json(out/'astrometry-verification.json',{'script_sha256':sha(Path(__file__)),'astrometry_sha256':sha(gp/'astrometry-audit.json'),'n_comparisons':len(checks),'max_linear_vs_astropy_arcsec':max(checks),'status':'Propagation arithmetic and fixed scene membership checked; no crossmatch or host validation.'})
print('Astrometry checks passed.')
