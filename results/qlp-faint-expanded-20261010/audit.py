"""Inventory frozen expanded search without changing discovery gates or opening holdouts."""
from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;plan=json.loads((out/'plan.json').read_text())
expected={t['tic']:t for t in plan['targets']};rows=[];counts=Counter();review=[]
for path in sorted((out/'targets').glob('*.json')):
 r=json.loads(path.read_text());tic=r['tic'];assert tic in expected
 assert r['target']==expected[tic]
 row={'tic':tic,'path':str(path),'sha256':sha(path),'status':r['status'],'disposition':r.get('disposition'),'error':r.get('error'),'peaks':[]}
 counts[r.get('disposition',r['status'])]+=1
 for i,p in enumerate(r.get('peaks',[])):
  screened=next((q for q in r.get('screened_peaks',[]) if q['best']==p),None)
  item={'rank':i,'peak':p,'flags':screened['flags'] if screened else ['below_diagnostic_screen_threshold']}
  if screened:
   item['supported_events']=screened['diagnostics']['supported_events']
   item['radius_earth_if_on_target']=screened['radius_earth_if_on_target']
   item['noise']=screened['extended_vetting']['noise']
   flags=set(screened['flags'])
   item['review_category']='original_review' if flags<={'crowding_or_missing_crowding'} else 'detrending_diagnostic_only' if flags<={'crowding_or_missing_crowding','alternative_detrending_prefers_other_period'} else 'other_flagged'
   if item['review_category']!='other_flagged':review.append({'tic':tic,**item})
  row['peaks'].append(item)
 rows.append(row)
assert len({r['tic'] for r in rows})==len(rows)
terminal=out/'results.json'
if terminal.exists():assert len(rows)==len(expected)==len(json.loads(terminal.read_text()))
save_json(out/'audit.json',{'utc':now(),'terminal_results_present':terminal.exists(),'n_completed_files':len(rows),'n_expected':len(expected),'counts':dict(counts),'plan_sha256':sha(out/'plan.json'),'inventory':rows,'review':review,'interpretation':'Snapshot, not proof of process status. All top3peaks retained. Diagnostic-only alternate-detrending peaks retain original flags and are not promoted. No reserved photometry opened by this audit; no new candidate or completeness claim.'})
print(len(rows),dict(counts),'review',[(r['tic'],r['rank'],r['review_category']) for r in review])
