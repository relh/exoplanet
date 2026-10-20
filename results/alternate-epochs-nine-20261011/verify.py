from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(out/'plan.json');sel=read(out/'selection.json');targets=read(out/'selected.json')
assert plan['targets']==targets and len(targets)==9
assert sha(out/'selected.json')==sel['selected_sha256']==plan['selected_sha256']
assert sha(out/'run.py')==plan['script_sha256']
for p,h in sel['input_hashes'].items():assert sha(Path(p))==h
for n,h in plan['source_hashes'].items():assert sha(Path('src/exoplanet')/n)==h
results=read(out/'results.json');assert len(results)==9 and {r['tic'] for r in results}=={t['tic'] for t in targets};rows=[]
for target in targets:
 tic=target['tic'];p=out/'targets'/f'{tic}.json';r=read(p);assert r['target']==target
 assert r['status']=='screened' and r['disposition']=='below_screen_threshold' and r['screened_peaks']==[]
 summary=next(x for x in results if x['tic']==tic);assert all(r.get(k)==v for k,v in summary.items())
 assert [d['sector'] for d in r['data']]==target['training_sectors']
 for d in r['data']:
  root='qlp' if target['discovery_collection']=='QLP' else 'alternate-epochs';raw=Path(f'data/{root}/{tic}-s{d["sector"]:04d}.fits');assert sha(raw)==d['source']['sha256']
  with fits.open(raw) as h:assert h[0].header['TICID']==tic and h[0].header['SECTOR']==d['sector']
 for sector in target['heldout_sectors']:
  for raw in [Path(f'data/qlp/{tic}-s{sector:04d}.fits'),Path(f'data/alternate-epochs/{tic}-s{sector:04d}.fits'),Path(f'data/lightcurves/s{sector:04d}-{tic}.fits')]:assert not raw.exists()
 rows.append({'tic':tic,'result_sha256':sha(p),'snr':r['best']['depth_snr'],'baseline_days':r['clean_baseline_days'],'n_clean':sum(d['n_clean_points'] for d in r['data'])})
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'plan_sha256':sha(out/'plan.json'),'rows':rows,'status':'Nine identities/raw hashes and below-threshold results verified; reserved files absent in standard cache paths. No completeness or planet-exclusion claim.'})
print(rows)
