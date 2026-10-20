from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
from exoplanet.prf_fit import fit_templates
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());fp=Path('results/joint-clock-fine-429034844-20261011/fit.json');b=read(fp)['best'];dirs=[];coverage=[]
for sector,count,winner in [(42,33,'429034844'),(43,40,'611135702')]:
 sp=Path(f'results/spoc-pixels-429034844-s{sector}-20261011');pr=Path(f'results/prf-429034844-s{sector}-20261011');rr=Path(f'results/prf-ratio-429034844-s{sector}-20261011');dirs.extend([sp,pr,rr]);a=read(sp/'analysis/localization.json');m=read(pr/'models.json')['sectors'][0];f=read(pr/'fits.json');r=f['sectors'][0];raw=Path(m['pixel_path'])
 assert read(sp/'status.json')['exit_code']==0 and sha(raw)==m['pixel_sha256']==a['source']['sha256']
 assert a['frozen_sha256']==f['frozen_sha256']==sha(fp) and a['n_events']==r['n_events']==count
 for model in m['models']:assert sha(Path(model['path']))==model['source']['sha256']
 z=np.load(pr/f's{sector}-images.npz');spz=np.load(sp/'analysis/images.npz')
 for name in ['difference','error']:np.testing.assert_allclose(z[name],spz[name])
 for h in r['hypotheses']:np.testing.assert_allclose(fit_templates(z['difference'],z['error'],[z['template_'+h['tic']]])['chi2'],h['chi2'])
 assert f['script_sha256']==sha(pr/'analyze.py') and f['module_sha256']==sha(Path('src/exoplanet/prf_fit.py'))
 c=read(pr/'empirical-controls.json');assert c['fits_sha256']==sha(pr/'fits.json') and c['sectors'][0]['n_controls']==41
 plan=read(rr/'plan.json');res=read(rr/'results.json');assert plan['script_sha256']==sha(rr/'run.py')
 for path,h in plan['inputs'].items():assert sha(Path(path))==h
 assert [x['ratio'] for x in res['rows']]==plan['ratios'] and all(x['winner']==winner for x in res['rows'])
 for control in res['controls']:np.testing.assert_allclose(control['recovered'],control['truth'],atol=1e-5)
 with fits.open(raw) as hd:
  assert hd[0].header['SECTOR']==sector
  d=hd[1].data;t=np.asarray(d['TIME']);q=np.asarray(d['QUALITY']);valid=np.isfinite(t);phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;en=np.zeros(len(t),int);en[valid]=np.rint((t[valid]-b['transit_time'])/b['period']).astype(int);events=[]
  for n in np.unique(en[valid&(abs(phase)<b['duration']/2)]):
   ni=int((valid&(q==0)&(en==n)&(abs(phase)<b['duration']/2)).sum());no=int((valid&(q==0)&(en==n)&(abs(phase)>b['duration'])&(abs(phase)<3*b['duration'])).sum());events.append({'event':int(n),'inside_quality_zero':ni,'outside_quality_zero':no})
  assert [e['event'] for e in events if e['inside_quality_zero']>=2 and e['outside_quality_zero']>=5]==a['event_numbers']
 coverage.append({'sector':sector,'events':events})
save_json(out/'coverage.json',coverage)
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'artifacts':{str(p):sha(p) for directory in dirs for p in directory.rglob('*') if p.is_file()},'coverage_sha256':sha(out/'coverage.json'),'status':'Pixel/model hashes, exact stack agreement, source fits, frozen timing, independent event gates and ten ratio controls verified; no calibrated host attribution.'});print('Verified both older-sector source fits and coverage.')
