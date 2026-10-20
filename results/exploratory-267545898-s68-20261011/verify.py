from pathlib import Path
import json,tempfile
from exoplanet.pipeline import sha,save_json
from exoplanet.campaign import process_target
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());original=json.loads((p/'targets/267545898.json').read_text())
for name,digest in plan['code_hashes'].items():assert sha(Path('src/exoplanet')/name)==digest
assert original['target']['training_sectors']==[68]
for r in original['data']:assert sha(Path('data/lightcurves/s0068-267545898.fits'))==r['source']['sha256']
with tempfile.TemporaryDirectory(prefix='exoplanet-267545898-verification-') as temp:
 q=Path(temp);(q/'targets').mkdir();rep=process_target(plan['target'],Path('data'),q)
 for key in ['best','peaks','screened_peaks','disposition','n_trial_periods','clean_baseline_days']:assert rep[key]==original[key],key
save_json(p/'verification.json',dict(status='passed',code_and_raw_hashes_checked=True,full_search_and_screening_reproduced=True,limits='Reproduction with the same algorithm, not independent statistical validation. Sector68 was already opened before this exploratory search was chosen.'))
