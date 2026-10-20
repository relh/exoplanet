from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(out/'plan.json');sel=read(out/'selection.json');assert sha(Path(sel['parent']))==sel['parent_sha256'];assert read(Path(sel['parent']))[16:1477]==plan['targets']==read(out/'selected.json');assert sha(out/'selected.json')==sel['selected_sha256']==plan['source_sha256'];assert sha(out/'run.py')==plan['script_sha256']
for n,h in plan['source_hashes'].items():assert sha(Path('src/exoplanet')/n)==h
expected={t['tic']:t for t in plan['targets']};counts=Counter();inventory=[];eligible=[]
for p in sorted((out/'targets').glob('*.json')):
 r=read(p);assert r['target']==expected[r['tic']] and r['target']['heldout_sectors']==[];counts[r.get('disposition') or r['status']]+=1
 inventory.append({'tic':r['tic'],'path':str(p),'sha256':sha(p),'status':r['status'],'error':r.get('error')})
 for d in r.get('data',[]):assert sha(Path(f"data/qlp/{r['tic']}-s{d['sector']:04d}.fits"))==d['source']['sha256']
 for i,v in enumerate(r.get('screened_peaks',[])):
  flags=set(v['flags']);base={'crowding_or_missing_crowding','alternative_detrending_prefers_other_period'};extra={'secondary_unmeasurable','fewer_than_3_supported_events'}
  category='original_or_detrending' if flags<=base else 'coverage_diagnostic' if flags<=base|extra and flags&extra and v['diagnostics']['supported_events']>=2 else None
  if category:eligible.append({'tic':r['tic'],'peak_index':i,'category':category,'flags':v['flags'],'best':v['best'],'supported_events':v['diagnostics']['supported_events'],'discovery_path':str(p),'discovery_sha256':sha(p)})
terminal=(out/'results.json').exists()
if terminal:
 rows=read(out/'results.json');assert len(rows)==len(inventory)==1461 and {r['tic'] for r in rows}==set(expected)
 for r in rows:assert all(v==read(out/'targets'/f"{r['tic']}.json").get(k) for k,v in r.items())
n=len(inventory);save_json(out/f'checkpoint-{n}.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'plan_sha256':sha(out/'plan.json'),'n_completed':n,'n_planned':1461,'terminal_results_present':terminal,'counts':dict(counts),'inventory':inventory,'eligible':eligible,'limits':'Snapshot hashes verified; process liveness separately polled. Eligible fits need catalog/plot/source checks and lack independent-sector validation. Errors are not nondetections.'})
print(n,dict(counts),[(x['tic'],x['peak_index'],x['category']) for x in eligible])
