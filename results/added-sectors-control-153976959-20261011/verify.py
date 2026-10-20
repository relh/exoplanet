from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json,read_curve
from exoplanet.campaign import load_training
from exoplanet.followup import refine_training,fixed_measure
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());f=json.loads((p/'frozen.json').read_text());a=json.loads((p/'alternative.json').read_text());original=json.loads(Path(plan['original_path']).read_text());assert sha(Path(plan['original_path']))==plan['original_sha256']==f['discovery_sha256'];assert plan['seed']==original['best']==f['seed'];assert plan['created_utc']<f['frozen_utc']
for name,digest in plan['source_sha256'].items():assert sha(Path('src/exoplanet')/name)==digest
for item in f['training_data']:
 raw=Path(f"data/lightcurves/s{item['sector']:04d}-153976959.fits");assert sha(raw)==item['source']['sha256'];_,_,_,star=read_curve(raw);assert star['ticid']==153976959 and star['sector']==item['sector']
 if item['sector'] in plan['added_sectors']:assert item['source']['retrieved_utc']>plan['created_utc']
for window,saved in [(1.5,f),(2.5,a)]:
 t,y,e,_=load_training(plan['target'],Path('data'),window=window);best,ranges=refine_training(t,y,e,original['best'],seed_baseline=plan['original_baseline_days']);assert best==saved['best'] and ranges==saved['timing_ranges'];m=fixed_measure(t,y,e,best['period'],best['transit_time'],best['duration']);assert m==saved['training_measurement' if window==1.5 else 'measurement']
 if window==1.5:
  z=np.load(p/'photometry.npz');np.testing.assert_array_equal(z['time'],t);np.testing.assert_array_equal(z['flux'],y);np.testing.assert_array_equal(z['error'],e)
# Matched original-only local refinement distinguishes added-data gains from the finer local search.
matched=[]
for window in [1.5,2.5]:
 t,y,e,_=load_training(original['target'],Path('data'),window=window);best,ranges=refine_training(t,y,e,original['best'],seed_baseline=plan['original_baseline_days']);matched.append(dict(window_days=window,best=best,timing_ranges=ranges,measurement=fixed_measure(t,y,e,best['period'],best['transit_time'],best['duration'])))
save_json(p/'matched-original.json',dict(rows=matched,policy='Same local-refinement routine on original two sectors only; computed after the expanded run, not a new independent control.'))
assert not Path('data/lightcurves/s0076-153976959.fits').exists()
save_json(p/'verification.json',dict(status='passed',raw_products_checked=len(f['training_data']),two_expanded_refinements_reproduced=True,added_downloads_after_plan=True,catalog_period_not_passed_to_refinement=True,reserved_cache_absent=True,limits='Same-algorithm reproducibility; one selected positive control; local seeded search, not a full-domain search or full-screen classification.'))
print('matched original',[(x['window_days'],x['best']) for x in matched])
