"""Coordinator-gated nominal sector81 test; no period optimization."""
import argparse,json
from pathlib import Path
from exoplanet.pipeline import sha,save_json,now
from exoplanet.campaign import load_training
from exoplanet.followup import fixed_measure,prediction_spread
O=Path(__file__).parent
CACHE=Path('data/lightcurves/s0081-402358350.fits')
def evaluate(t,y,e,row):
 b=row['best'];ranges=row['ranges'];m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);total=m['total'];spread=prediction_spread(t,b,ranges);precise=spread<b['duration']/2 and not ranges['search_boundary_hit'] and row['measurement']['supported_events']>=3;expected=None if total is None else b['depth']/total['error']
 result='insufficient_coverage' if total is None else 'timing_prediction_inconclusive' if not precise else 'recovered_at_frozen_ephemeris_requires_further_vetting' if total['snr']>=5 and m['supported_events']>=2 else 'not_recovered_despite_expected_sensitivity' if expected>=5 and total['snr']<2 else 'insufficient_evidence'
 return dict(clock=b,measurement=m,timing_spread_days=spread,timing_precise=precise,expected_formal_snr=expected,conclusion=result)
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--execute',action='store_true');parser.add_argument('--history-reviewed-unopened',action='store_true');parser.add_argument('--expected-plan-sha',required=True);a=parser.parse_args();assert a.execute and a.history_reviewed_unopened,'Coordinator must review history and explicitly authorize';assert not (O/'execution.json').exists(),'No automatic overwrite or partial-run resumption';assert not CACHE.exists() and not CACHE.with_suffix('.fits.json').exists(),'Sector81 cache or metadata exists: investigate before any access';assert sha(O/'plan.json')==a.expected_plan_sha
 plan=json.loads((O/'plan.json').read_text());assert plan['run_script_sha256']==sha(Path(__file__))
 for path,h in plan['input_sha256'].items():assert sha(Path(path))==h,f'Input changed: {path}'
 for path,h in plan['source_sha256'].items():assert sha(Path(path))==h,f'Implementation changed: {path}'
 expanded=json.loads(Path(plan['expanded_path']).read_text());original=json.loads(Path(plan['original_path']).read_text());audit=json.loads(Path(plan['audit_path']).read_text());assert audit['status']=='passed' and audit['reserved_cache_absent'];assert json.loads(Path(plan['expanded_verification_path']).read_text())['status']=='passed';assert expanded['training_sectors']==[40,41,54] and expanded['reserved_sectors']==[81];assert [r['window'] for r in expanded['rows']]==[1.5,2.5];assert [r['window'] for r in original['rows']]==[1.5,2.5]
 state=dict(started_utc=now(),status='running',plan_sha256=sha(O/'plan.json'),coordinator_history_reviewed_unopened=True,input_sha256=plan['input_sha256'],source_sha256=plan['source_sha256']);save_json(O/'execution.json',state);rows=[]
 try:
  for window in [1.5,2.5]:
   t,y,e,data=load_training({'tic':402358350,'training_sectors':[81]},Path('data'),window=window)
   for family,source in [('expanded40_41_54',expanded),('original40_41',original)]:
    prior=next(r for r in source['rows'] if r['window']==window);r=evaluate(t,y,e,prior);r.update(family=family,window=window,role='primary' if family=='expanded40_41_54' and window==1.5 else 'prespecified_comparison',data=data,scored_utc=now());rows.append(r);save_json(O/'results.json',dict(plan_sha256=sha(O/'plan.json'),rows=rows))
  assert len(rows)==4;state.update(status='complete',finished_utc=now(),results_sha256=sha(O/'results.json'))
 except Exception as exc:
  state.update(status='error',failed_utc=now(),error=f'{type(exc).__name__}: {exc}');save_json(O/'execution.json',state);raise
 save_json(O/'execution.json',state)
if __name__=='__main__':main()
