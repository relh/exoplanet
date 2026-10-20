"""Verify provenance and reconstruct saved fixed-source PRF comparisons."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha, save_json
from exoplanet.pixel_vet import difference_events
from exoplanet.prf_fit import fit_templates
p=Path(__file__).parent
read=lambda x:json.loads(x.read_text())
f=read(p/'fits.json'); m=read(p/'models.json')['sectors'][0]; r=f['sectors'][0]
for key,path in [('script_sha256',p/'analyze.py'),('module_sha256',Path('src/exoplanet/prf_fit.py')),('frozen_sha256',Path('results/qlp-faint-midradius-single-review-20261011/241928959-peak0/frozen.json')),('gaia_sha256',Path('results/gaia-241928959-scene-20261011/gaia_source.json')),('neighbors_sha256',Path('results/neighbors-241928959-20261011/neighbors.json'))]:
 assert sha(path)==f[key],(key,path)
assert sha(Path(m['pixel_path']))==m['pixel_sha256']
for model in m['models']:
 assert sha(Path(model['path']))==model['source']['sha256']
z=np.load(p/'s92-images.npz')
b=read(Path('results/qlp-faint-midradius-single-review-20261011/241928959-peak0/frozen.json'))['best']
with fits.open(m['pixel_path']) as h:
 d=h[1].data; v=np.isfinite(d['TIME'])
 diff,err,events,nums=difference_events(np.array(d['TIME'][v],float),np.array(d['FLUX'][v],float),np.array(d['FLUX_ERR'][v],float),d['QUALITY'][v],b)
 assert h[0].header['CAMERA']==m['camera'] and h[0].header['CCD']==m['ccd']
 assert np.isclose(m['col'],h[1].header['1CRV5P']+(6-h[1].header['1CRP5P'])*h[1].header['1CDL5P'])
 assert np.isclose(m['row'],h[1].header['2CRV5P']+(6-h[1].header['2CRP5P'])*h[1].header['2CDL5P'])
np.testing.assert_allclose(diff,z['difference']); np.testing.assert_allclose(err,z['error'])
assert len(events)==r['n_events']==5
for row in r['hypotheses']:
 fit=fit_templates(diff,err,[z['template_'+row['tic']]])
 np.testing.assert_allclose(fit['chi2'],row['chi2']);np.testing.assert_allclose(fit['coefficients'][0],row['amplitude'])
c=read(p/'empirical-controls.json');assert c['fits_sha256']==sha(p/'fits.json')
for row in c['sectors']:
 assert row['n_controls']==len(row['controls'])==41
 for tic,count in row['correct_host'].items():
  assert count==sum(next(i for i in control['injections'] if i['tic']==tic)['winner']==tic for control in row['controls'])
s=read(p/'registration-sensitivity.json')
for name,digest in s['inputs'].items():assert sha(p/name)==digest
assert len(s['rows'])==17 and all(row['winner']=='241928959' for row in s['rows'])
summary={'verified':True,'events_reconstructed':len(events),'fixed_hypotheses_reconstructed':2,'formal_injections_per_host':100,'shifted_controls_per_host':41,'registration_steps':17,'separation_pixels_propagated':float(np.linalg.norm(np.array(r['positions']['241928959'])-r['positions']['241928961'])),'free_offset_pixels':float(np.linalg.norm(r['free_offset_from_target'])),'minimum_conditional_chi2_advantage':min(row['host_chi2']['241928961']-row['host_chi2']['241928959'] for row in s['rows']),'artifacts':{q.name:sha(q) for q in sorted(p.iterdir()) if q.is_file() and q.name not in ['verification.json','ASSESSMENT.md']},'limits':'Reconstruction verifies recorded calculations, not physical attribution or noise calibration.'}
save_json(p/'verification.json',summary); print(summary)
