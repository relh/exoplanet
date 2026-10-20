"""Refine cached discovery sectors43/44; never access additional observations."""
from pathlib import Path
import json
import numpy as np
from exoplanet.campaign import load_training
from exoplanet.followup import refine_training,fixed_measure,prediction_spread
from exoplanet.pipeline import sha,save_json,now
O=Path(__file__).parent;SOURCE=Path('results/solar-radius-ranks5456-5968-20261011/targets/96166003.json')
def guard():
 for sector in [19,59]:
  assert not Path(f'data/lightcurves/s{sector:04d}-96166003.fits').exists(),'Additional observation already cached; review protocol before proceeding'
def main():
 guard();assert not (O/'plan.json').exists(),'No overwriting frozen plan';r=json.loads(SOURCE.read_text());seed=r['screened_peaks'][0]['best'];assert r['target']['training_sectors']==[43,44]
 for s in [43,44]:assert Path(f'data/lightcurves/s{s:04d}-96166003.fits.json').exists()
 plan=dict(created_utc=now(),discovery_path=str(SOURCE),discovery_sha256=sha(SOURCE),training_sectors=[43,44],windows=[1.5,2.5],primary_window=1.5,seed=seed,original_baseline=r['clean_baseline_days'],source_hashes={str(p):sha(p) for p in [Path(__file__),*Path('src/exoplanet').glob('*.py')]},policy='Training-only local refinement conditional on previously selected.955day family. No additional/lightcurve downloads. Timing profile is a box/white-noise heuristic, not red-noise posterior. Primary1.5day and secondary2.5day detrending predetermined; retain original clock and all profile pairs.')
 save_json(O/'plan.json',plan);rows=[]
 for w in plan['windows']:
  t,y,e,data=load_training(r['target'],Path('data'),window=w);best,ranges=refine_training(t,y,e,seed,seed_baseline=plan['original_baseline']);measurement=fixed_measure(t,y,e,best['period'],best['transit_time'],best['duration']);original=fixed_measure(t,y,e,seed['period'],seed['transit_time'],seed['duration']);baseline=np.ptp(t);width=3*seed['duration']*seed['period']/plan['original_baseline'];step=seed['duration']*seed['period']/(20*baseline);ngrid=max(2049,int(np.ceil(2*width/step))+1)
  grid=dict(period_min=max(.25,seed['period']-width),period_max=seed['period']+width,n_grid=ngrid,durations=(np.array([.8,1,1.2])*seed['duration']).tolist(),oversample=50,objective='likelihood',profile_delta_log_likelihood=4.5)
  forecasts=[dict(days_after_training_end=d,assumed_window_start=float(t.max()+d),assumed_window_end=float(t.max()+d+27),spread_days=prediction_spread(np.array([t.max()+d,t.max()+d+27]),best,ranges)) for d in [30,365,730,1095]]
  rows.append(dict(window=w,role='primary' if w==1.5 else 'sensitivity',best=best,ranges=ranges,grid=grid,measurement=measurement,original_clock_measurement=original,data=data,illustrative_forecasts=forecasts,forecast_note='Hypothetical27day windows, not actual sector19/59 dates or coverage.'))
  np.savez_compressed(O/f'w{w}.npz',t=t,y=y,e=e)
 save_json(O/'frozen.json',dict(frozen_utc=now(),plan_sha256=sha(O/'plan.json'),rows=rows));guard()
 protocol=dict(frozen_utc=now(),frozen_sha256=sha(O/'frozen.json'),intended_sectors=[19,59],opening_gate='Parent campaign terminal audit must succeed and coordinator must explicitly launch future run. This script never opens sectors19/59. Verify cache/history and freeze file hashes immediately before retrieval.',primary='Use1.5day refined best period/epoch/duration unchanged in both sectors, primary flattenwindow1.5. Save fixed original discovery clock comparison. Use2.5day own refinedclock/flatten only as predetermined sensitivity; do not choose larger SNR.',timing='Evaluate existing prediction_spread using actual cleaned timestamps; precise only if spread<duration/2, profile not touching period boundary, and training supports>=3events.',decision_order=['No usable data/total measurement: insufficient_coverage (retain error if retrieval/preprocessing failed)','Imprecise prediction: timing_prediction_inconclusive, regardless of nominal depth','Precise and SNR>=5 and at least2 events withSNR>=2: recovered_at_frozen_ephemeris_requires_further_vetting','Precise and expected formalSNR>=5 and observedSNR<2: not_recovered_despite_expected_sensitivity','Otherwise insufficient_evidence'],expected_snr='Training BLS depth divided by fixed-depth measurement error in new sector',forbidden='No new timing/period/duration optimization or selecting a favorable profile pair as primary. Do not change59clock after seeing19 under this protocol.',profiles='Any saved-profile envelope or maximum reported later is exploratory/conditional and separate from nominal result; no calibrated significance.',scope='Success is repeatability at a conditional clock, not identification of host or planet. Ambiguous pixel source and shared instrumental systematics remain. Failed gates and both detrending outcomes retained. If a different plan trains on19 to predict59, freeze it separately before59 and preserve this original43/44 prediction.')
 save_json(O/'prospective-protocol.json',protocol);print([(x['window'],x['best']['period'],x['best']['duration'],len(x['ranges']['profile_timing_pairs'])) for x in rows])
if __name__=='__main__':main()
