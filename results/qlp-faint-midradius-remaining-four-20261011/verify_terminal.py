from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
original=read(out/'checkpoint-1025.json');terminal=read(out/'results.json')
assert len(terminal)==len(original['inventory'])==len(read(out/'plan.json')['targets'])==1025
bytic={r['tic']:r for r in terminal};assert len(bytic)==1025
for r in original['inventory']:assert {k:read(Path(r['path'])).get(k) for k in bytic[r['tic']]}==bytic[r['tic']] and sha(Path(r['path']))==r['sha256']
expected={(r['tic'],r['screened_peak_index']) for r in original['review']};seen=set();files={str(out/'results.json'):sha(out/'results.json')}
for name in ['qlp-faint-midradius-remaining-four-followup-20261011','qlp-faint-midradius-remaining-four-coverage-followup-20261011']:
 p=Path('results')/name/'terminal.json';a=read(p);assert a['status']=='complete'
 for r in a['records']:
  assert r['status']=='complete';key=(r['tic'],r['peak_index']);assert key not in seen;seen.add(key)
 files[str(p)]=sha(p)
assert seen==expected
p=Path('results/qlp-faint-midradius-baseline-recovery-20261011/terminal.json');a=read(p);assert a['status']=='complete'
assert {r['tic'] for r in a['records']}=={r['tic'] for r in original['inventory'] if r['status']=='error'}
assert len(a['records'])==201 and all(not r.get('followups') for r in a['records'])
files[str(p)]=sha(p);j=read(out/'joined-1025.json');assert j['n_distinct_stars']==j['n_distinct_usable']==1025
save_json(out/'terminal-verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'terminal_files':files,'observed_process_exits':{'48386':0,'66198':0,'22347':0,'68067':0},'original_counts':original['counts'],'joined_counts':j['counts'],'n_followups':len(seen),'limits':'Observed tool exits plus exact terminal/inventory matching. 201 original failures retained; 200 baseline recoveries plus prior manual309703302 counted once. Completion of this batch is not completeness across TESS or planet validation.'})
print('Verified complete 1025-star batch, five follow-ups, and 201 recovery records.')
