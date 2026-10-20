from pathlib import Path
import json,collections
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;run=json.loads((p/'run.json').read_text());assert run['status']=='complete';assert sha(p/'run.py')==run['script_sha256'];parent=Path(run['parent']);assert sha(parent/'run.json')==run['parent_sha256']
for name,digest in run['source_sha256'].items():assert sha(Path('src/exoplanet')/name)==digest
allrows=[json.loads(f.read_text()) for f in (parent/'targets').glob('*.json')];pool=sorted([r for r in allrows if r.get('disposition')=='below_screen_threshold'],key=lambda r:(r['median_scatter_floor_ppm'],r['tic']));selected=[pool[i] for i in run['indices']];assert selected==json.loads((p/'selected.json').read_text());assert [r['tic'] for r in selected]==run['tics'];results=json.loads((p/'results.json').read_text());counts=[]
for row,original in zip(results,selected):
 assert row['tic']==original['tic'] and row['baseline_peaks']==original['peaks'];assert len(row['probes'])==12
 for q in row['probes']:
  record=json.loads(Path(q['evidence_path']).read_text());assert record['status']==q['status'];assert q['depth'] in [.0001,.0003];assert record['target']['injection']=={k:q[k] for k in ['period','duration','depth','epoch']}
  matching=[r for r in record.get('screened_peaks',[]) if abs(r['best']['period']/q['period']-1)<.005];baseline=any(abs(r['period']/q['period']-1)<.005 and r['depth_snr']>=7 for r in original['peaks']);assert q['baseline_period_match']==baseline;assert q['recovered_top3']==bool(matching);assert q['recovered_full_screen']==any(not r['flags'] for r in matching);assert q['creditable_recovery']==(q['recovered_full_screen'] and not baseline)
  for data in record['data']:assert sha(Path(f"data/lightcurves/s{data['sector']:04d}-{row['tic']}.fits"))==data['source']['sha256']
  for s in original['target']['heldout_sectors']:assert not Path(f"data/lightcurves/s{s:04d}-{row['tic']}.fits").exists()
 counts.append(dict(tic=row['tic'],by_depth=[dict(depth=d,total=6,top3=sum(q['recovered_top3'] for q in row['probes'] if q['depth']==d),creditable=sum(q['creditable_recovery'] for q in row['probes'] if q['depth']==d)) for d in [.0001,.0003]]))
probes=[q for row in results for q in row['probes']];assert len(probes)==run['n_probes']==36;assert sum(q['creditable_recovery'] for q in probes)==run['creditable_recoveries'];assert sum(q['status']=='error' for q in probes)==run['n_errors']
save_json(p/'verification.json',dict(status='passed',trial_records_reconciled=36,counts=counts,reserved_cache_absent=True,limits='Checks selection, provenance and accounting; not independent recovery reruns or population completeness.'));print(json.dumps(counts))
