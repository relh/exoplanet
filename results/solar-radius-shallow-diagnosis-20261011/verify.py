from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());rows=json.loads((p/'results.json').read_text());assert sha(p/'run.py')==plan['script_sha256']
for path,digest in plan['inputs'].items():assert sha(Path(path))==digest
assert len(rows)==36
for row in rows:
 probe=row['probe'];original=json.loads(Path('results/solar-radius-next512-20261011/targets',f"{row['tic']}.json").read_text())
 assert row['raw_hashes']==[sha(Path(f"data/lightcurves/s{s:04d}-{row['tic']}.fits")) for s in original['target']['training_sectors']]
 b,i=row['baseline'],row['injected'];np.testing.assert_allclose(row['incremental_depth'],i['depth']-b['depth']);np.testing.assert_allclose(row['incremental_depth_fraction'],row['incremental_depth']/probe['depth']);np.testing.assert_allclose(row['ideal_depth_over_measured_error'],probe['depth']/i['error'])
rs=[r for r in rows if r['probe']['depth']==.0001];missed=[r for r in rs if not r['probe']['creditable_recovery']];assert len(missed)==15 and all(r['injected']['snr']<7 for r in missed)
save_json(p/'verification.json',dict(status='passed',records_checked=36,missed_100ppm_probes=15,all_missed_100ppm_true_clock_snr_below7=True,incremental_depth_fraction_range_100ppm=[min(r['incremental_depth_fraction'] for r in rs),max(r['incremental_depth_fraction'] for r in rs)],limits='Hash and arithmetic reconciliation, not independent detrending rerun or population calibration.'))
print((p/'verification.json').read_text())
