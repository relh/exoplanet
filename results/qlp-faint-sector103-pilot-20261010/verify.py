from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
plan=read(out/'plan.json');terminal=read(out/'results.json');assert len(terminal)==100
assert {r['tic'] for r in terminal}=={t['tic'] for t in plan['targets']}
for name,digest in plan['source_hashes'].items():assert sha(Path('src/exoplanet')/name)==digest
inventory=[]
for t in plan['targets']:
 p=out/'targets'/f"{t['tic']}.json";r=read(p);assert r['target']==t and r['finished_utc']
 for ev in r.get('data',[]):assert sha(Path(f"data/qlp/{r['tic']}-s{ev['sector']:04d}.fits"))==ev['source']['sha256']
 if r['status']=='error':assert r['tic']==120523140
 else:assert r['status']=='screened'
 inventory.append({'path':str(p),'sha256':sha(p)})
folder=Path('results/qlp-faint-sector103-recovery-20261010/120523140');rp=read(folder/'plan.json');rr=read(folder/'result.json');r=read(Path(rr['path']))
assert sha(Path(rp['original_path']))==rp['original_sha256']==rr['original_sha256']
assert sha(Path(rp['failed_raw']))==rp['failed_raw_sha256']
assert r['target']==rp['target'] and r['status']=='screened' and r['finished_utc']
for ev in r['data']:assert sha(Path(f"data/qlp/{r['tic']}-s{ev['sector']:04d}.fits"))==ev['source']['sha256']
base={'crowding_or_missing_crowding','alternative_detrending_prefers_other_period'}
coverage={'fewer_than_3_supported_events','secondary_unmeasurable'}
for p in r['screened_peaks']:
 flags=set(p['flags']);assert not flags<=base
 assert not(flags<=base|coverage and flags&coverage and p['diagnostics']['supported_events']>=2)
assert (folder/'ASSESSMENT.md').exists()
save_json(out/'verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'plan_sha256':sha(out/'plan.json'),'n_original':100,'n_original_usable':99,'n_distinct_usable_after_recovery':100,'inventory':inventory,'recovery_sha256':sha(Path(rr['path'])),'recovery_assessment_sha256':sha(folder/'ASSESSMENT.md'),'limits':'Integrity and eligibility check; not planet validation. Original failure retained.'})
print('Verified 100 original records and separate recovery')
