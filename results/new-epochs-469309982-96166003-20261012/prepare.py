from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
O=Path(__file__).parent;assert not (O/'plan.json').exists()
paths=['data/coverage-six-extension-20261012/qlp.json','results/coverage-six-extension-20261012/results.json','results/weak-seed-ranks8-32-20261011/targets/469309982.json','results/followup-469309982-20261011/frozen.json','results/expanded-96166003-20261012/frozen-for59.json','results/timing-96166003-discovery-20261011/frozen.json','results/timing-96166003-discovery-20261011/plan.json']
products=json.loads(Path(paths[0]).read_text())['data'];weak=json.loads(Path(paths[2]).read_text());expanded=json.loads(Path(paths[4]).read_text());original=json.loads(Path(paths[5]).read_text());seed961=json.loads(Path(paths[6]).read_text())['seed'];cases=[]
for tic,s in [(469309982,90),(96166003,86)]:
 clocks=[]
 if tic==469309982:
  for row in weak['windows']:
   w=row['window_days'];clocks.append(dict(name='archived_refined9_10_36_37',window=w,role='primary' if w==1.5 else 'comparison',best=row['best'],ranges=row['timing_ranges'],training_supported_events=row['measurement']['supported_events']))
  seed=weak['selection']['seed']
 else:
  for name,source in [('expanded19_43_44',expanded),('original43_44',original)]:
   for row in source['rows']:
    w=row['window'];clocks.append(dict(name=name,window=w,role='primary' if name.startswith('expanded') and w==1.5 else 'comparison',best=row['best'],ranges=row['ranges'],training_supported_events=row['measurement']['supported_events']))
  seed=seed961
 for w in [1.5,2.5]:clocks.append(dict(name='original_unprofiled_seed_reference',window=w,role='reference_only',best=seed,ranges=None,training_supported_events=0))
 matches=[r for r in products if int(r['target_name'])==tic and r['sequence_number']==s];assert len(matches)==1;cases.append(dict(tic=tic,sector=s,product=matches[0],clocks=clocks))
plan=dict(created_utc=now(),cases=cases,input_sha256={p:sha(Path(p)) for p in paths},source_sha256={str(p):sha(p) for p in Path('src/exoplanet').glob('*.py')},script_sha256=sha(O/'run.py'),policy='No new timing search/refit; retain all clocks and negative results. Primary frozen historical clock at1.5day. Native QLP cadence, existing flux-column selection, published positive errors only, quality0, no missing-error estimation. Detrend1.5/2.5; unchanged fixed_measure and strict timing/coverage/sensitivity gates. Seed reference lacks timing profile so never declares recovery. QLP vs original SPOC reduction is processing difference; new epoch is independent only if history verified unseen. All prior epochs already opened; conditional profile limitations retained.',cache_preflight='No matching90/469 or86/961 FITS or sidecar found in sharedcache by filename scan; runner repeats exact conventional paths and isolatedroot absence. Coordinator must independently review fullsessionhistory before execute; do not infer unseen solely fromabsence.',scope='Retrospective project selection, prospective epoch scoring only; no planet odds/globalFAP; no pixels/new stellar models; no automatic retries ofpartialrun.')
save_json(O/'plan.json',plan);print(sha(O/'plan.json'))
