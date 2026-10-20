"""Independent Decimal/calendar arithmetic, not importing the calculation."""
from pathlib import Path
from decimal import Decimal as D, ROUND_HALF_EVEN
from datetime import date
import json,hashlib
OUT=Path(__file__).resolve().parent; ROOT=OUT.parents[1]
plan=json.loads((OUT/'plan.json').read_text()); data=json.loads((ROOT/plan['input']).read_text(),parse_float=D)
saved=json.loads((OUT/'results.json').read_text());checks=0; maximum=0.
def check(ok):
 global checks
 assert ok
 checks+=1
def close(a,b):
 global maximum
 delta=abs(float(a)-float(b));maximum=max(maximum,delta);check(delta<3e-7)
def rnd(x):return int(x.to_integral_value(rounding=ROUND_HALF_EVEN))
check(hashlib.sha256((OUT/'plan.json').read_bytes()).hexdigest()==(OUT/'plan.sha256').read_text().split()[0])
check(hashlib.sha256((ROOT/plan['input']).read_bytes()).hexdigest()==plan['input_sha256'])
for s in saved['rows']:
 t=next(t for t in data['targets'] if t['tic']==s['tic']); r=t[s['family']][s['row']];b=r['best'];rr=r['ranges'];p=b['period'];ep=b['transit_time'];prim=t['clock_profiles'][0]['best']
 day=D((date.fromisoformat(s['epoch_tdb'])-date(2000,1,1)).days)+D('2451544.5')-D(2457000)
 event=rnd((day-prim['transit_time'])/prim['period']); shift=rnd((prim['transit_time']-ep)/p);k=event+shift
 check(event==s['primary_cycle']);check(shift==s['row_reference_cycle_offset']);check(k==s['row_cycle']);check(rnd((day-ep)/p)==s['independently_nearest_row_cycle'])
 nominal=ep+D(k)*p
 mids=[]
 for pp,ee in rr['profile_timing_pairs']:
  shift2=rnd((ep-ee)/pp);check(abs(ee+D(shift2)*pp-ep)<=pp/2)
  mids.append(ee+D(k+shift2)*pp)
 f=3*rr['conditional_epoch_floor_days'];lo=min(mids)-f;hi=max(mids)+f;spread=max(abs(x-nominal) for x in mids)+f
 for key,v in [('nominal_bjd_tdb',nominal+D(2457000)),('earliest_bjd_tdb',lo+D(2457000)),('latest_bjd_tdb',hi+D(2457000)),('midpoint_envelope_hours',(hi-lo)*24),('max_profile_displacement_plus_floor_hours',spread*24),('half_duration_gate_hours',b['duration']*12),('three_epoch_floor_hours',f*24),('nominal_displacement_from_primary_hours',(nominal-(prim['transit_time']+D(event)*prim['period']))*24)]:close(v,s[key])
 check(s['gate_pass']==(spread<b['duration']/2));check(s['profile_envelope_exceeds_period']==(hi-lo>p));check(s['profile_pairs']==len(mids))
for s in saved['summaries']:
 rows=[r for r in saved['rows'] if r['tic']==s['tic'] and r['epoch_tdb']==s['epoch_tdb']]
 for fam in ['clock_profiles','historical_profiles']:
  rr=[r for r in rows if r['family']==fam]
  if rr:close((max(r['latest_bjd_tdb'] for r in rr)-min(r['earliest_bjd_tdb'] for r in rr))*24,s[fam+'_envelope_hours']);check(s[fam+'_all_gates_pass']==all(r['gate_pass'] for r in rr))
  else:check(s[fam+'_envelope_hours'] is None);check(s[fam+'_all_gates_pass'] is None)
for name,digest in json.loads((OUT/'provenance.json').read_text())['output_sha256'].items():check(hashlib.sha256((OUT/name).read_bytes()).hexdigest()==digest)
report={'passed':True,'checks':checks,'maximum_absolute_numeric_difference_mixed_units':maximum,'method':'Independent decimal arithmetic and Gregorian calendar day differences; all profile pairs, all rows, original gates, input/plan/output hashes','limitations':'Arithmetic agreement is not a calibrated timing uncertainty or an observed event; no flux or sensitivity verified.'}
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
