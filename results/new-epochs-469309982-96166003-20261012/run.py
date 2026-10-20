"""Evaluate new QLP epochs at archived clocks, without fitting or searching."""
from pathlib import Path
import argparse,json,numpy as np
from exoplanet.pipeline import sha,save_json,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure,prediction_spread
O=Path(__file__).parent;D=Path('data/new-epochs-469309982-96166003-20261012')
def main():
 p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');p.add_argument('--history-reviewed-unopened',action='store_true');p.add_argument('--plan-sha',required=True);a=p.parse_args();assert a.execute and a.history_reviewed_unopened;assert not (O/'execution.json').exists();assert sha(O/'plan.json')==a.plan_sha;plan=json.loads((O/'plan.json').read_text());assert sha(Path(__file__))==plan['script_sha256']
 for path,h in plan['input_sha256'].items():assert sha(Path(path))==h,path
 for path,h in plan['source_sha256'].items():assert sha(Path(path))==h,path
 for case in plan['cases']:
  tic,s=case['tic'],case['sector']
  for root in [Path('data'),D]:
   for f in [root/'qlp'/f'{tic}-s{s:04d}.fits',root/'lightcurves'/f's{s:04d}-{tic}.fits',root/'pixels'/f'{tic}-s{s:04d}.fits']:
    assert not f.exists() and not f.with_suffix('.fits.json').exists(),f
 state=dict(started_utc=now(),plan_sha256=a.plan_sha,history_reviewed_unopened=True,status='running');save_json(O/'execution.json',state);rows=[]
 try:
  for case in plan['cases']:
   for w in [1.5,2.5]:
    t,y,e,provenance=load_qlp(dict(tic=case['tic'],training_sectors=[case['sector']],qlp_products={str(case['sector']):case['product']}),D,window=w,bin_minutes=0)
    np.savez_compressed(O/f"{case['tic']}-w{w}.npz",time=t,flux=y,error=e)
    for clock in [v for v in case['clocks'] if v['window']==w]:
     b=clock['best'];m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);total=m['total'];ranges=clock['ranges'];spread=prediction_spread(t,b,ranges) if ranges else None;precise=bool(ranges and spread<b['duration']/2 and not ranges['search_boundary_hit'] and clock['training_supported_events']>=3);expected=b['depth']/total['error'] if total else None
     conclusion='insufficient_coverage' if total is None else 'timing_prediction_inconclusive' if not precise else 'recovered_at_frozen_ephemeris_requires_further_vetting' if total['snr']>=5 and m['supported_events']>=2 else 'not_recovered_despite_expected_sensitivity' if expected>=5 and total['snr']<2 else 'insufficient_evidence'
     rows.append(dict(tic=case['tic'],sector=case['sector'],window=w,clock_name=clock['name'],role=clock['role'],clock=b,ranges=ranges,measurement=m,timing_spread_days=spread,timing_precise=precise,expected_formal_snr=expected,conclusion=conclusion,data=provenance,scored_utc=now()));save_json(O/'results.json',dict(plan_sha256=a.plan_sha,rows=rows))
  state.update(status='complete',finished_utc=now(),results_sha256=sha(O/'results.json'))
 except Exception as ex:state.update(status='error',failed_utc=now(),error=f'{type(ex).__name__}: {ex}');save_json(O/'execution.json',state);raise
 save_json(O/'execution.json',state)
if __name__=='__main__':main()
