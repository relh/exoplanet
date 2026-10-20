from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());run=json.loads((p/'run.json').read_text());rs=json.loads((p/'results.json').read_text());assert run['status']=='complete'
for path,digest in plan['inputs'].items():assert sha(Path(path))==digest
assert {r['tic'] for r in rs}==set(plan['tics'])
for row in rs:
 assert len(row['probes'])==12
 for q in row['probes']:
  r=json.loads(Path(q['evidence_path']).read_text());assert r['status']==q['status'];matches=[x for x in r.get('screened_peaks',[]) if abs(x['best']['period']/q['period']-1)<.005]
  assert bool(matches)==q['recovered_top3'];assert any(not x['flags'] for x in matches)==q['recovered_full_screen'];assert q['creditable_recovery']==(q['recovered_full_screen'] and not q['baseline_period_match'])
  for sector in r['target']['heldout_sectors']:assert not Path(f"data/lightcurves/s{sector:04d}-{row['tic']}.fits").exists()
 counts=next(c for c in run['counts'] if c['tic']==row['tic']);assert counts['creditable']==sum(q['creditable_recovery'] for q in row['probes'])
save_json(p/'verification.json',dict(status='passed',trial_records_reconciled=36,source_hashes_checked=True,reserved_cache_absent=True,limits='Checks provenance and outcome accounting; not an independent search rerun or completeness.'))
print('36 trials verified')
