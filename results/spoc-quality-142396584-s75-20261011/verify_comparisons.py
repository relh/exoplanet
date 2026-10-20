from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
read=lambda p:json.loads(p.read_text())
root=Path('results');follow=root/'qlp-faint-midradius-remaining-two-followup-20261011/142396584-peak0';source=root/'qlp-faint-midradius-remaining-two-20261011/targets/142396584.json';out=Path(__file__).parent
artifacts={}
for s in (75,76):
 p=root/f'qlp-faint-142396584-cadence-s{s}-20261011';plan=read(p/'plan.json');r=read(p/'results.json')
 for key,path in [('frozen_sha256',follow/'frozen.json'),('discovery_sha256',source),('script_sha256',p/'run.py'),('spoc_sha256',Path(f'data/lightcurves/s{s:04d}-142396584.fits')),('qlp_sha256',Path(f'data/qlp/142396584-s{s:04d}.fits'))]:assert plan[key]==sha(path)
 for col in ('pdcsap','sap'):
  c=r[col+'_comparison'];assert c['n_matched']==(6338 if s==75 else 5600)
  assert (c['other_common']['total'] is None)==(s==75)
  if s==76:assert c['other_common']['total']['n']==94 and c['qlp_common']['total']['n']==94
 for path in (p/'run.py',p/'plan.json',p/'results.json'):artifacts[str(path)]=sha(path)
a=read(out/'preprocessing-audit.json');assert a['script_sha256']==sha(out/'audit_preprocessing.py') and a['frozen_sha256']==sha(follow/'frozen.json')
for r in a['rows']:
 assert r['raw_sha256']==sha(Path(f"data/lightcurves/s{r['sector']:04d}-142396584.fits"))
 assert r['flattened_inside']==(94 if r['event']==3 else 0)
 assert sum(x['event_points_after_edge_trim'] for x in r['segments'])==r['flattened_inside']
for path in (out/'audit_preprocessing.py',out/'preprocessing-audit.json'):artifacts[str(path)]=sha(path)
save_json(out/'comparison-verification.json',{'artifacts':artifacts,'script_sha256':sha(Path(__file__)),'status':'passed','limits':'Provenance and coverage checks; no independent astrophysical validation.'})
print('Comparison provenance and edge-trim availability verified.')
