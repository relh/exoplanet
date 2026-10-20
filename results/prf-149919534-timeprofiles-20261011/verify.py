from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());p=read(out/'plan.json');r=read(out/'results.json');s=read(out/'synthetic.json');pm=read(out/'plot-manifest.json');bp=read(out/'baseline-plan.json');br=read(out/'baseline-results.json')
assert p['script_sha256']==sha(out/'run.py') and p['module_sha256']==sha(Path('src/exoplanet/prf_fit.py'))
for path,h in p['inputs'].items():assert sha(Path(path))==h
assert pm['script_sha256']==sha(out/'plot.py') and pm['results_sha256']==sha(out/'results.json') and pm['plot_sha256']==sha(out/'profiles.png')
assert bp['script_sha256']==sha(out/'baseline_sensitivity.py') and bp['profile_plan_sha256']==sha(out/'plan.json') and bp['profile_results_sha256']==sha(out/'results.json')
assert len(s['checks'])==96 and all(x['max_source_error']<1e-8 for x in s['checks'])
assert len(br['synthetic_checks'])==24 and all(x['max_error']<1e-8 for x in br['synthetic_checks'])
fp=Path('results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/149919534-peak0/frozen.json');b=read(fp)['best']
with fits.open('data/pixels/149919534-s0075.fits') as h:
 d=h[1].data;t=np.asarray(d['TIME'],float);ok=np.isfinite(t);t=t[ok];q=d['QUALITY'][ok];err=np.asarray(d['FLUX_ERR'][ok],float)
phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;checks=[]
for window,row,bs in zip(p['windows'],r['rows'],br['rows']):
 assert window['label']==row['label']==bs['label'];assert len(row['bins'])==24
 dt=(t-window['center'])/b['duration'];valid=q==0
 if window['kind']=='control':valid &= abs(phase)>b['duration']
 baseline=valid&(abs(dt)>1)&(abs(dt)<3);no=baseline.sum();assert no==row['baseline_exposures']
 for entry,left,right in zip(row['bins'],p['bin_edges_durations'][:-1],p['bin_edges_durations'][1:]):
  mask=valid&(dt>=left)&(dt<right);ni=mask.sum();overlap=mask&baseline
  assert entry['left']==left and entry['right']==right and entry['n']==ni and entry['overlap_baseline']==int(overlap.sum())
  assert entry['status']=='measured' and ni>=2 and entry['dof']==110
  w=baseline.astype(float)/no-mask.astype(float)/ni
  direct=np.nansum(w[:,None,None]**2*err**2,axis=0)
  expanded=np.nansum(err[baseline]**2,axis=0)/no**2+np.nansum(err[mask]**2,axis=0)/ni**2-2*np.nansum(err[overlap]**2,axis=0)/(ni*no)
  delta=float(abs(direct-expanded).max());assert delta<1e-10;checks.append(delta)
 assert [f['side'] for f in bs['fits']]==['before','after','both']
 for f in bs['fits']:assert f['status']=='measured' and f['baseline_exposures']>=5
base=Path('results/prf-149919534-astrometry-20261011');old=read(base/'fits.json');cs=read(base/'control-summary.json')['windows']
for row in br['rows']:
 both=row['fits'][2]
 if row['kind']=='event':reference=next(x for x in old['rows'] if 'event'+str(x['event'])==row['label'])['fits'][1]
 else:reference=next(c for c in cs if c['event']==row['prior_event'] and c['fraction']==row['prior_fraction'])
 assert max(abs(v-reference['amplitudes'][k]) for k,v in both['amplitudes'].items())<1e-8
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'results_sha256':sha(out/'results.json'),'baseline_results_sha256':sha(out/'baseline-results.json'),'max_covariance_identity_error':max(checks),'status':'96 profiles,120 synthetic contrast checks, overlap variance identity,12 baseline fits and4 prior-fit reproductions verified. Not host or transit validation.'})
print('Verified profiles, overlapping-exposure variance and baseline sensitivity.')
