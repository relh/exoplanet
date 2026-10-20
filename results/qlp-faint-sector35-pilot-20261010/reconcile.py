"""Pilot integrity and complete follow-up/recovery inventory, not validation."""
from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
plan=read(out/'plan.json');terminal=read(out/'results.json');cp=read(out/'checkpoint-0100.json')
assert len(plan['targets'])==len(terminal)==100
assert len({r['tic'] for r in terminal})==100
assert {r['tic'] for r in terminal}=={t['tic'] for t in plan['targets']}
for r in cp['inventory']:assert sha(Path(r['path']))==r['sha256']
for name,digest in plan['source_hashes'].items():assert sha(Path('src/exoplanet')/name)==digest
for t in plan['targets']:
 row=read(out/'targets'/f"{t['tic']}.json");assert row['target']==t and row['finished_utc']
 if row['tic']==178826943:assert row['status']=='error'
 else:assert row['status']=='screened'
 for ev in row.get('data',[]):assert sha(Path(f"data/qlp/{t['tic']}-s{ev['sector']:04d}.fits"))==ev['source']['sha256']
rp=Path('results/qlp-faint-sector35-recovery-20261010/178826943');r=read(rp/'plan.json');rr=read(rp/'targets/178826943.json')
assert r['original_sha256']==sha(out/'targets/178826943.json') and sha(Path(r['failed_raw']))==r['failed_raw_sha256']
assert r['counts']['usable_flux']==0 and rr['status']=='error' and '404' in rr['error']
assert (rp/'ASSESSMENT.md').is_file()
for sector in r['target']['heldout_sectors']:assert not Path(f'data/qlp/178826943-s{sector:04d}.fits').exists()
a=read(Path('results/qlp-faint-sector35-pilot-followup-20261010/terminal.json'));b=read(Path('results/qlp-faint-sector35-pilot-coverage-followup-20261010/terminal.json'))
assert a['status']==b['status']=='complete' and a['records']==[]
assert [(r['tic'],r['peak_index'],r['status']) for r in b['records']]==[(141301608,0,'complete')]
assert [(r['tic'],r['screened_peak_index']) for r in cp['review']]==[(141301608,0)]
p=Path('results/qlp-faint-sector35-pilot-coverage-followup-20261010/141301608-peak0');f=read(p/'frozen.json');h=read(p/'heldout.json')
assert f['discovery_sha256']==sha(out/'targets/141301608.json')
assert {r['sector'] for r in h}==set(f['heldout_sectors']) and all(r['started_utc']>=f['utc'] for r in h)
artifacts={str(p/name):sha(p/name) for name in ['frozen.json','heldout.json','secondary.json','discovery.png','ASSESSMENT.md']}
artifacts.update({str(rp/name):sha(rp/name) for name in ['plan.json','result.json','ASSESSMENT.md']})
save_json(out/'reconciliation.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'n_completed':100,'n_usable':99,'n_incomplete':1,'n_reviewed_peaks':1,'artifacts':artifacts,'limits':'Integrity/review inventory, not scientific validation or planet promotion.'})
print('Pilot reconciled:99usable,1incomplete,1reviewed peak')
