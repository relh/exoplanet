"""Audit completed records without treating a live run manifest as proof of life."""
from pathlib import Path
import json,collections
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
selected=json.loads((out/'eligible.json').read_text());ids={t['tic'] for t in selected};seen=set();records=[];errors=[];passes=[];counts=collections.Counter()
for batch in [Path(f'results/campaign-late-sectors-batch{i}-20261010') for i in [1,2]]:
 run=json.loads((batch/'run.json').read_text())
 assert run['selection_sha256']==sha(out/'eligible.json')
 for p in (batch/'targets').glob('*.json'):
  try:d=json.loads(p.read_text())
  except json.JSONDecodeError:continue
  assert d['tic'] in ids and d['tic'] not in seen
  seen.add(d['tic']);counts[d.get('disposition',d['status'])]+=1
  records.append({'path':str(p),'sha256':sha(p)})
  if d['status']=='error':errors.append({'tic':d['tic'],'error':d['error']})
  if d.get('disposition')=='followup_priority':passes.append(d['tic'])
save_json(out/'checkpoint.json',{'utc':now(),'n_selected':len(ids),'n_completed':len(seen),'n_pending':len(ids-seen),'dispositions':dict(counts),'errors':errors,'screen_pass_tics':sorted(passes),'completed_records':records,'note':'Point-in-time audit while batch1 may still run. Screen pass is not a validated candidate. Terminal status separately verified through process handles.'})
print(len(seen),len(ids-seen),dict(counts),'passes',passes)
