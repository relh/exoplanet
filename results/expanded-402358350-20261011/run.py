"""Explicitly gated sector54 evaluation and training expansion; never open81."""
import argparse,json
from pathlib import Path
from collections import Counter
from exoplanet.pipeline import sha,save_json,now
from exoplanet.campaign import load_training
from exoplanet.followup import fixed_measure,prediction_spread,refine_training
O=Path(__file__).parent
BATCH=Path('results/solar-radius-ranks4944-5456-20261011')
PRIOR=Path('results/timing-402358350-discovery-20261011/frozen.json')
DISC=BATCH/'targets/402358350.json'
def absent(sector):
 assert not Path(f'data/lightcurves/s{sector:04d}-402358350.fits').exists(),f'Sector{sector} already cached; inspect history and write explicit recovery plan'
def gate(expected):
 verification=BATCH/'verification.json';assert sha(verification)==expected,'Coordinator-supplied terminal audit hash mismatch'
 v=json.loads(verification.read_text());r=json.loads((BATCH/'run.json').read_text());assert v['status']=='passed' and v['reserved_cache_absent'] is True and r['status']=='complete'
 selection=Path(r['selection_path']);selected=json.loads(selection.read_text());assert sha(selection)==r['selection_sha256'];rows=[json.loads(p.read_text()) for p in (BATCH/'targets').glob('*.json')];assert len(rows)==len(selected)==512;assert {x['tic'] for x in rows}=={x['tic'] for x in selected};assert dict(Counter(x.get('disposition',x['status']) for x in rows))==v['counts'];assert any(x['tic']==402358350 for x in v['eligible_peaks'])
 assert v['queue_plan_sha256']==sha(Path('results/solar-radius-remaining-resume4432-20261011/plan.json'));assert v['verifier_sha256']==sha(Path('results/solar-radius-remaining-resume4432-20261011/run.py'))
 for name,h in r['source_sha256'].items():assert sha(BATCH/'source'/name)==h
 assert r['n_errors']==sum(x['status']=='error' for x in rows)
 return v,r
def evaluate(t,y,e,clock,ranges,train):
 m=fixed_measure(t,y,e,clock['period'],clock['transit_time'],clock['duration']);spread=prediction_spread(t,clock,ranges);total=m['total'];precise=spread<clock['duration']/2 and not ranges['search_boundary_hit'] and train['supported_events']>=3;expected=None if total is None else clock['depth']/total['error']
 result='insufficient_coverage' if total is None else 'timing_prediction_inconclusive' if not precise else 'recovered_at_frozen_ephemeris_requires_further_vetting' if total['snr']>=5 and m['supported_events']>=2 else 'not_recovered_despite_expected_sensitivity' if expected>=5 and total['snr']<2 else 'insufficient_evidence'
 return dict(measurement=m,timing_spread_days=spread,timing_precise=precise,expected_formal_snr=expected,conclusion=result)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--execute',action='store_true');ap.add_argument('--expected-terminal-audit-sha',required=True);a=ap.parse_args();assert a.execute,'Explicit coordinator execution required';assert not (O/'execution.json').exists(),'Do not overwrite experiment; inspect recorded state'
 plan=json.loads((O/'plan.json').read_text());assert sha(Path(__file__))==plan['run_script_sha256'];assert sha(PRIOR)==plan['prior_frozen_sha256'] and sha(DISC)==plan['discovery_sha256'];v,run=gate(a.expected_terminal_audit_sha);absent(54);absent(81)
 for s in [40,41]:assert Path(f'data/lightcurves/s{s:04d}-402358350.fits.json').exists()
 state=dict(started_utc=now(),status='running',plan_sha256=sha(O/'plan.json'),terminal_audit_sha256=a.expected_terminal_audit_sha,terminal_verified_utc=v['verified_utc'],run_manifest_sha256=sha(BATCH/'run.json'));save_json(O/'execution.json',state)
 prior=json.loads(PRIOR.read_text());disc=json.loads(DISC.read_text());checks=[]
 try:
  # Every original-clock measurement completes and is saved before adding54 to training.
  for row in prior['rows']:
   absent(81);w=row['window'];t,y,e,evidence=load_training({'tic':402358350,'training_sectors':[54]},Path('data'),window=w);result=evaluate(t,y,e,row['best'],row['ranges'],row['measurement']);seed=disc['screened_peaks'][0]['best'];result.update(window=w,role=row['role'],data=evidence,clock=row['best'],original_discovery_clock_measurement=fixed_measure(t,y,e,seed['period'],seed['transit_time'],seed['duration']),scored_utc=now());checks.append(result);save_json(O/'sector54-original-predictions.json',dict(prior_frozen_sha256=sha(PRIOR),rows=checks))
  expanded=[]
  for row in prior['rows']:
   absent(81);w=row['window'];t,y,e,evidence=load_training({'tic':402358350,'training_sectors':[40,41,54]},Path('data'),window=w);seed=disc['screened_peaks'][0]['best'];best,ranges=refine_training(t,y,e,seed,seed_baseline=disc['clean_baseline_days']);expanded.append(dict(window=w,role=row['role'],best=best,ranges=ranges,measurement=fixed_measure(t,y,e,best['period'],best['transit_time'],best['duration']),data=evidence))
  absent(81);save_json(O/'frozen-for81.json',dict(frozen_utc=now(),plan_sha256=sha(O/'plan.json'),original54_predictions_sha256=sha(O/'sector54-original-predictions.json'),training_sectors=[40,41,54],reserved_sectors=[81],rows=expanded,policy='54 explicitly becomes training regardless of nominal recovery result; no81 data opened. Primary1.5day window unchanged. Local selected-family profile, conditional uncertainties and source ambiguity retained. Sector81 retrieval requires separate coordinator execution and preserved original40/41 prediction.'));state.update(status='complete',finished_utc=now(),frozen_for81_sha256=sha(O/'frozen-for81.json'))
 except Exception as exc:
  state.update(status='error',failed_utc=now(),error=f'{type(exc).__name__}: {exc}');save_json(O/'execution.json',state);raise
 save_json(O/'execution.json',state)
if __name__=='__main__':main()
