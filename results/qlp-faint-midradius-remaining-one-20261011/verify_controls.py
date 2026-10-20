from pathlib import Path
import json,numpy as np
from astropy.io import fits
from astropy.timeseries import BoxLeastSquares
from exoplanet.archive import qlp_flux_columns
from exoplanet.campaign import DURATIONS
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());cp=out/'checkpoint-0647.json';snapshot=read(cp);assert len(snapshot['inventory'])==647
for row in snapshot['inventory']:assert sha(Path(row['path']))==row['sha256']
reports=[]
for name in ['remaining-one-injections','remaining-one-larger-injections']:
 root=Path(f'results/qlp-faint-midradius-{name}-20261011');p=read(root/'plan.json');a=read(root/'audit.json');assert a['terminal'] and len(a['rows'])==12;assert p['script_sha256']==sha(root/'run.py');assert a['input_sha256']==sha(root/'results.json');assert p['parent_sha256']==sha(out/'plan.json')
 assert p['targets']==read(out/'plan.json')['targets'][:3]
 for n,h in p['source_hashes'].items():assert sha(Path('src/exoplanet')/n)==h
 for t in p['targets']:
  eq=read(root/f"{t['tic']}-baseline-equivalence.json");assert eq['exact_arrays_equal'] and eq['discovery_sha256']==sha(out/'targets'/f"{t['tic']}.json")
  for ev in eq['sources']:assert sha(Path(f"data/qlp/{t['tic']}-s{ev['sector']:04d}.fits"))==ev['source']['sha256']
 bounds=[]
 for row in a['rows']:
  path=Path(row['path']);assert sha(path)==row['source_sha256'];r=read(path);b=r['clean_baseline_days'];grid=BoxLeastSquares([0,b],[1,1]).autoperiod(DURATIONS,minimum_period=.5,maximum_period=min(20,b/2.5),frequency_factor=2)
  bounds.append({'tic':row['tic'],'period':row['period'],'radius_earth':row['radius_earth'],'grid_min':float(min(grid)),'grid_max':float(max(grid)),'in_grid':bool(min(grid)<=row['period']<=max(grid))})
 save_json(root/'bounds.json',{'audit_sha256':sha(root/'audit.json'),'rows':bounds})
 reports.append({'directory':str(root),'audit_sha256':sha(root/'audit.json'),'n':12,'in_grid':sum(b['in_grid'] for b in bounds),'period_recovered':a['n_top3_period_recovered'],'screen_pass':a['n_noncrowding_pass'],'phase_consistent_matches':sum(any(m['within_half_injected_duration_at_three_times'] for m in r['matches']) for r in a['rows'])})
pixel=Path('data/qlp/59570933-s0046.fits');result=out/'targets/59570933.json';r=read(result);assert r['status']=='error'
with fits.open(pixel) as h:
 d=h[1].data;fc,ec,_=qlp_flux_columns(d.names);counts={'rows':len(d),'q0':int((d['QUALITY']==0).sum()),'finite_flux':int(np.isfinite(d[fc]).sum()),'finite_error':int(np.isfinite(d[ec]).sum())};assert counts['finite_flux']==counts['finite_error']==0
save_json(out/'data-error-59570933.json',{'script_sha256':sha(Path(__file__)),'result_sha256':sha(result),'pixel_path':str(pixel),'pixel_sha256':sha(pixel),'product':r['target']['qlp_products']['46'],'original_error':r['error'],'counts':counts,'interpretation':'Cached training product has no finite selected flux/error values. No usable light curve, not a transit nondetection or network retry. Reserved data not substituted.'})
save_json(out/'controls-verification.json',{'script_sha256':sha(Path(__file__)),'checkpoint_sha256':sha(cp),'controls':reports,'error_audit_sha256':sha(out/'data-error-59570933.json'),'status':'647 immutable outputs,24 injection results/bounds/source hashes/loader equivalence and cached data failure verified. Not survey completeness.'});print(reports)
