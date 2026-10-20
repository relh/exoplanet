"""Backward propagation of saved clock metadata; no observational data access."""
from pathlib import Path
import json, hashlib, csv
from astropy.time import Time
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
plan=json.loads((OUT/'plan.json').read_text())
src=ROOT/plan['input']
assert hashlib.sha256(src.read_bytes()).hexdigest()==plan['input_sha256']
inputs=json.loads(src.read_text())
rows=[]; summaries=[]
for target in inputs['targets']:
 primary=target['clock_profiles'][0]['best']; ref=primary['transit_time']
 for date in plan['epochs_tdb']:
  btjd=float(Time(date,scale='tdb').jd)-2457000
  n=round((btjd-ref)/primary['period'])
  group=[]
  for family in ['clock_profiles','historical_profiles']:
   for i,row in enumerate(target[family]):
    best=row['best']; ranges=row['ranges']; p=best['period']; ep=best['transit_time']
    offset=round((ref-ep)/p); cycle=n+offset
    nominal=ep+cycle*p
    points=[te+(cycle+round((ep-te)/tp))*tp for tp,te in ranges['profile_timing_pairs']]
    floor=3*ranges['conditional_epoch_floor_days']
    lo=min(points)-floor; hi=max(points)+floor
    spread=max(abs(t-nominal) for t in points)+floor
    r={'tic':target['tic'],'epoch_tdb':date,'family':family,'row':i,'role':row.get('role'),'primary_cycle':n,'row_reference_cycle_offset':offset,'row_cycle':cycle,'independently_nearest_row_cycle':round((btjd-ep)/p),'nominal_bjd_tdb':nominal+2457000,'nominal_displacement_from_primary_hours':(nominal-(ref+n*primary['period']))*24,'earliest_bjd_tdb':lo+2457000,'latest_bjd_tdb':hi+2457000,'midpoint_envelope_hours':(hi-lo)*24,'max_profile_displacement_plus_floor_hours':spread*24,'half_duration_gate_hours':best['duration']*12,'gate_pass':spread<best['duration']/2,'profile_pairs':len(points),'three_epoch_floor_hours':floor*24,'profile_envelope_exceeds_period':hi-lo>p}
    rows.append(r);group.append(r)
  s={'tic':target['tic'],'epoch_tdb':date,'primary_nominal_bjd_tdb':ref+n*primary['period']+2457000}
  for family in ['clock_profiles','historical_profiles']:
   rr=[r for r in group if r['family']==family]
   s[family+'_envelope_hours']=(max(r['latest_bjd_tdb'] for r in rr)-min(r['earliest_bjd_tdb'] for r in rr))*24 if rr else None
   s[family+'_all_gates_pass']=all(r['gate_pass'] for r in rr) if rr else None
  summaries.append(s)
(OUT/'results.json').write_text(json.dumps({'rows':rows,'summaries':summaries},indent=2)+'\n')
with (OUT/'rows.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(OUT/'provenance.json').write_text(json.dumps({'input_sha256':{plan['input']:plan['input_sha256'],'plan.json':hashlib.sha256((OUT/'plan.json').read_bytes()).hexdigest(),'calculate.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},'output_sha256':{name:hashlib.sha256((OUT/name).read_bytes()).hexdigest() for name in ['results.json','rows.csv']},'network_access':'none','flux_access':'none'},indent=2)+'\n')
for s in summaries: print(s)
