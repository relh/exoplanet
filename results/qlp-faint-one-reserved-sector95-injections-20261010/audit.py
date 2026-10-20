"""Check period, phase and depth of synthetic recoveries without changing gates."""
from pathlib import Path
import json,hashlib
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;plan=json.loads((out/'plan.json').read_text());p=out/'results.json'
terminal=p.exists()
if not terminal:p=out/'progress.json'
payload=p.read_bytes();rows=json.loads(payload);audit=[]
for r in rows:
 source=Path(r['path']);d=json.loads(source.read_text());matches=[]
 assert d['target']['injection']['period']==r['period']
 for peak in d.get('peaks',[]):
  if abs(peak['period']/r['period']-1)>=.005:continue
  offsets=[]
  for fraction in [0,.5,1]:
   time=r['epoch']-.317*r['period']+fraction*d['clean_baseline_days']
   event=r['epoch']+round((time-r['epoch'])/r['period'])*r['period']
   delta=(event-peak['transit_time']+peak['period']/2)%peak['period']-peak['period']/2
   offsets.append(float(delta))
  matches.append({'fit':peak,'phase_offsets_days_start_mid_end':offsets,'depth_ratio':peak['depth']/r['depth'],'within_half_injected_duration_at_three_times':max(map(abs,offsets))<=r['duration']/2})
 audit.append({**r,'source_sha256':sha(source),'matches':matches})
if terminal:assert len(rows)==len(plan['targets'])*len(plan['periods'])*len(plan['radii_earth'])==12
save_json(out/'audit.json',{'utc':now(),'terminal':terminal,'input_sha256':hashlib.sha256(payload).hexdigest(),'n_completed':len(rows),'n_errors':sum(r['status']=='error' for r in rows),'n_top3_period_recovered':sum(r['recovered_top3'] for r in rows),'n_noncrowding_pass':sum(r['noncrowding_screen_pass'] for r in rows),'rows':audit,'limits':'Period and phase diagnostics of injections only. Existing flags retained. Three timing samples are not a timing posterior. No survey completeness or planet claim.'})
print('terminal',terminal,'completed',len(rows),'period_recovered',sum(r['recovered_top3'] for r in rows),'screen_pass',sum(r['noncrowding_screen_pass'] for r in rows))
