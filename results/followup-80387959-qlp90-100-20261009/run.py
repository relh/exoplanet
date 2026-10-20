"""Reassign previously inspected S63 to training, then test untouched QLP90/100."""
import json,sys,shutil
from pathlib import Path
import numpy as np
from exoplanet.pipeline import save_json,sha,now
from exoplanet.campaign import load_training
from exoplanet.followup import refine_training,fixed_measure,prediction_spread
from exoplanet.qlp_campaign import load_qlp
out=Path(__file__).parent
if sys.argv[1]=='freeze':
 assert not (out/'frozen.json').exists()
 for sector in [90,100]:assert not Path(f'data/qlp/80387959-s{sector:04d}.fits').exists(),'Already downloaded: audit before proceeding'
 discovery=Path('results/inspection-batch11-20261009/80387959-discovery.json');row=json.loads(discovery.read_text())
 target=dict(row['target']);target['training_sectors']=[10,36,37,63]
 t,y,dy,evidence=load_training(target,Path('data'))
 best,ranges=refine_training(t,y,dy,row['screened_peaks'][0]['best'],seed_baseline=row['clean_baseline_days'])
 source=out/'source';source.mkdir()
 for p in Path('src/exoplanet').glob('*.py'):shutil.copyfile(p,source/p.name)
 save_json(out/'frozen.json',{'frozen_utc':now(),'tic':80387959,'best':best,'timing_ranges':ranges,'training_data':evidence,'training_measurement':fixed_measure(t,y,dy,best['period'],best['transit_time'],best['duration']),'training_sectors':[10,36,37,63],'heldout_sectors':[90,100],'discovery_sha256':sha(discovery),'old_followup_sha256':sha(Path('results/followup-80387959-expanded-20261009/heldout.json')),'script_sha256':sha(Path(__file__)),'source_sha256':{p.name:sha(p) for p in source.iterdir()},'policy':'Sector63 already inspected and explicitly reassigned to training. Previous inconclusive result preserved. S90/100 photometry not previously opened. Refine once before either test; no adaptation between sectors. QLP 10-minute bins, standard flattening, published errors unless none usable then existing explicit adjacent-MAD policy. Recovery: timing spread < D/2, no profile boundary, >=3 training events, fixed SNR>=5 and >=2 supported heldout events. Dependent phase controls not FAP; no discovery/validation claim.'})
 print('FROZEN',best,flush=True)
elif sys.argv[1]=='test':
 frozen=json.loads((out/'frozen.json').read_text());assert sha(Path(__file__))==frozen['script_sha256']
 assert not (out/'heldout.json').exists()
 products=json.loads(Path('results/qlp-coverage-80387959-20261009/metadata.json').read_text())['observations'];products={str(o['sequence_number']):o for o in products}
 best=frozen['best'];results=[]
 for sector in frozen['heldout_sectors']:
  row={'sector':sector,'started_utc':now(),'status':'error','frozen_sha256':sha(out/'frozen.json')}
  try:
   target={'tic':80387959,'training_sectors':[sector],'qlp_products':products,'estimate_missing_errors':True}
   t,y,dy,evidence=load_qlp(target,Path('data'))
   m=fixed_measure(t,y,dy,best['period'],best['transit_time'],best['duration']);spread=prediction_spread(t,best,frozen['timing_ranges'])
   precise=spread<best['duration']/2 and not frozen['timing_ranges']['search_boundary_hit'] and frozen['training_measurement']['supported_events']>=3
   total=m['total'];expected=None if total is None else best['depth']/total['error']
   controls=[]
   for shift in np.arange(1,50)*best['period']/50:
    if min(shift,best['period']-shift)<2*best['duration']:continue
    v=fixed_measure(t,y,dy,best['period'],best['transit_time']+shift,best['duration'])['total']
    if v:controls.append(v['snr'])
   if not precise:conclusion='timing_prediction_inconclusive'
   elif total is None:conclusion='insufficient_coverage'
   elif total['snr']>=5 and m['supported_events']>=2:conclusion='recovered_at_frozen_ephemeris_requires_further_vetting'
   elif expected>=5 and total['snr']<2:conclusion='not_recovered_despite_expected_sensitivity'
   else:conclusion='insufficient_evidence'
   row.update(status='measured',data=evidence,measurement=m,timing_spread_days=spread,timing_precise=precise,expected_formal_snr=expected,phase_control_snrs=controls,conclusion=conclusion)
   np.savez_compressed(out/f's{sector}-processed.npz',t=t,y=y,dy=dy)
  except Exception as exc:row['error']=repr(exc)
  results.append(row);save_json(out/'heldout.json',results);print(sector,row.get('conclusion',row.get('error')),flush=True)
else:raise ValueError('freeze or test required')
