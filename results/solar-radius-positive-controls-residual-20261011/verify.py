from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
from exoplanet.campaign import load_training
from exoplanet.search import keep_outside_signals
p=Path(__file__).parent;run=json.loads((p/'run.json').read_text());assert run['status']=='complete' and run['n_errors']==0;rs=json.loads((p/'results.json').read_text());assert len(rs)==3;checked=0;outcomes=[]
for name,digest in run['source_sha256'].items():assert sha(p/'source'/name)==digest
controls={x['tic']:x for x in json.loads(Path('results/solar-radius-positive-controls-20261011/selected-controls.json').read_text())}
for case in rs:
 src=Path(case['source_path']);assert sha(src)==case['source_sha256'];original=json.loads(src.read_text());t,y,dy,_=load_training(original['target'],Path('data'));period=float(controls[case['tic']]['catalog_planet']['pl_orbper']);cr=[]
 for step in case['rounds']:
  rr=json.loads(Path(step['result_path']).read_text());keep=keep_outside_signals(t,step['masked_signals']);np.testing.assert_allclose(1-keep.mean(),step['removed_fraction']);assert step['removed_fraction']<=.2 and keep.sum()>=200
  for window in [1.5,2.5]:
   tb,yb,eb,_=load_training(original['target'],Path('data'),window=window);tr,yr,er,_=load_training(rr['target'],Path('data'),window=window);m=keep_outside_signals(tb,step['masked_signals']);np.testing.assert_array_equal(tr,tb[m]);np.testing.assert_array_equal(yr,yb[m]);np.testing.assert_array_equal(er,eb[m]);checked+=1
  hits=[dict(period=x['best']['period'],flags=x['flags'],snr=x['best']['depth_snr']) for x in rr['screened_peaks'] if abs(x['best']['period']/period-1)<.01];cr.append(dict(round=step['round'],selected_planet_matches=hits,full_pass=any(not x['flags'] for x in hits),removed_fraction=step['removed_fraction']))
 for s in original['target']['heldout_sectors']:assert not Path(f"data/lightcurves/s{s:04d}-{case['tic']}.fits").exists()
 outcomes.append(dict(tic=case['tic'],name=controls[case['tic']]['catalog_planet']['pl_name'],rounds=cr,stop_reason=case.get('stop_reason','Maximum planned rounds reached')))
save_json(p/'verification.json',dict(status='passed',window_mask_reconstructions=checked,retained_flux_and_error_unchanged=True,source_hashes_checked=True,reserved_cache_absent=True,outcomes=outcomes,limits='Mask accounting and retained data verified; full residual searches not independently rerun. Extra trials are exploratory and do not change original control outcomes.'));print(outcomes)
