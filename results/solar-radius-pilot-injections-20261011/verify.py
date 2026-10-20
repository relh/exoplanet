from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;run=json.loads((p/'run.json').read_text());assert run['status']=='complete';assert sha(Path('results/solar-radius-pilot-20261011/run.json'))==run['campaign_sha256']
rows=json.loads((p/'results.json').read_text());probes=[q for r in rows for q in r['probes']];assert len(probes)==run['n_probes']==12
for q in probes:
 r=json.loads(Path(q['evidence_path']).read_text());assert r['status']==q['status']
 matching=[peak for peak in r.get('screened_peaks',[]) if abs(peak['best']['period']/q['period']-1)<.005]
 assert bool(matching)==q['recovered_top3'];assert any(not peak['flags'] for peak in matching)==q['recovered_full_screen']
 assert q['creditable_recovery']==(q['recovered_full_screen'] and not q['baseline_period_match'])
for key,field in [('recovered_top3','recovered_top3'),('recovered_full_screen','recovered_full_screen'),('creditable_recoveries','creditable_recovery')]:assert run[key]==sum(q[field] for q in probes)
save_json(p/'verification.json',dict(status='passed',probes_reconciled=len(probes),source_parent_hash_checked=True,limits='Outcome/provenance audit, not independent rerun or survey completeness.'))
