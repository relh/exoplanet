"""Audit terminal original searches and follow-up records; do not erase errors."""
from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import sha, save_json, now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
checkpoint=read(out/'checkpoint-4144.json');summaries=read(out/'results.json')
assert len(summaries)==len({r['tic'] for r in summaries})==4144
summaries={r['tic']:r for r in summaries}
assert checkpoint['n_completed']==checkpoint['n_planned']==4144
for r in checkpoint['inventory']:
 p=Path(r['path']);d=read(p);assert sha(p)==r['sha256']
 assert {k:d.get(k) for k in summaries[r['tic']]}==summaries[r['tic']]
expected={(r['tic'],r['screened_peak_index']) for r in checkpoint['review']}
seen=set();followups=[];terminals={}
for kind in ['two-followup','two-coverage-followup']:
 p=Path(f'results/qlp-faint-midradius-remaining-{kind}-20261011');terminal=read(p/'terminal.json');assert terminal['status']=='complete'
 terminals[str(p/'terminal.json')]=sha(p/'terminal.json')
 for r in terminal['records']:
  key=(r['tic'],r['peak_index']);assert key not in seen;seen.add(key)
  assert r['status']=='complete' and sha(Path(r['discovery_path']))==r['discovery_sha256']
  folder=p/f"{r['tic']}-peak{r['peak_index']}";f=read(folder/'frozen.json');h=read(folder/'heldout.json')
  assert f['discovery_sha256']==r['discovery_sha256']
  assert [{'sector':x['sector'],'status':x['status'],'conclusion':x.get('conclusion')} for x in h]==[{'sector':x['sector'],'status':x['status'],'conclusion':x.get('conclusion')} for x in r['heldout']]
  followups.append({'tic':r['tic'],'peak_index':r['peak_index'],'path':str(folder),'artifacts':{n:sha(folder/n) for n in ['frozen.json','heldout.json','secondary.json','discovery.png']}})
assert seen==expected and len(seen)==71
counts=dict(Counter(r.get('disposition') or r['status'] for r in summaries.values()))
assert counts==checkpoint['counts']
save_json(out/'terminal-verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'checkpoint_sha256':sha(out/'checkpoint-4144.json'),'results_sha256':sha(out/'results.json'),'n_distinct':4144,'original_counts':counts,'followups':followups,'terminal_hashes':terminals,'observed_exit_codes':{'13778':0,'65928':0,'50025':0},'limits':'Original-run accounting only. Forty-two original errors remain recorded; separate retries and coverage reviews must be joined once per star later. All71 eligible follow-up computations finished, but scientific source/candidate review is incomplete. Does not prove survey completeness or planet validation.'})
print('Verified 4144 original target results and 71 terminal followups:',counts)
