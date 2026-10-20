"""Verify bounded campaign accounting and current candidate-index evidence."""
from pathlib import Path
import json,re
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
two=Path('results/two-reserved-tier-audit-20261011/audit.json')
one=Path('results/one-reserved-tier-audit-20261011/audit.json')
a=json.loads(two.read_text());b=json.loads(one.read_text())
assert not a['missing_tics'] and not a['multiple_records'] and not a['target_plan_mismatches']
ids_two=set(map(int,a['records']));ids_one=set()
for batch in b['batches']:
 folder=Path(batch['sector_folder']);p=folder/'reconciliation.json'
 assert sha(p)==batch['reconciliation_sha256']
 rec=json.loads(p.read_text())
 for item in rec['inventory']:
  q=Path(item['path']);assert sha(q)==item['sha256']
  tic=json.loads(q.read_text())['tic'];assert tic not in ids_one;ids_one.add(tic)
assert len(ids_one)==6206 and len(ids_two)==28049 and not ids_one&ids_two
recovery=Path('results/two-reserved-tier-audit-20261011/recoveries.json')
r=json.loads(recovery.read_text())
v=Path('results/two-reserved-tier-audit-20261011/recovery-plan-verification.json')
rv=json.loads(v.read_text());assert rv['recoveries_sha256']==sha(recovery)
for row in rv['rows']:
 assert sha(Path(row['plan']))==row['plan_sha256'] and sha(Path(row['result']))==row['result_sha256']
f=json.loads((out/'followups.json').read_text())
assert not f['issues'] and not f['modern_gate_unaccounted']
readme=Path('README.md').read_text();top=readme.split('This index highlights')[0]
links=[]
for match in re.finditer(r'\]\((results/[^)]+)\)',top):
 p=Path(match.group(1));assert p.is_file();links.append({'path':str(p),'sha256':sha(p)})
assert 'No confirmed discovery or securely attributed new planet candidate yet.' in top
assert len(links)>=20
sources=[two,one,recovery,v,Path('results/user-posts-20261010/NOTES.md'),Path('results/rv-hd32564-activity-20261010/ASSESSMENT.md'),Path('results/hd32564-tess-rv23-20261010/ASSESSMENT.md'),Path('results/prf-80387959-20261009/ASSESSMENT.md'),Path('results/tglc-80387959-20261009/ASSESSMENT.md'),Path('results/nsc-80387959-q3c-20261010/ASSESSMENT.md'),Path('results/skymapper-80387959-20261010/ASSESSMENT.md')]
usable=r['n_usable_after_recovery']+b['usable_after_recovery']
save_json(out/'verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'n_distinct_selected':len(ids_one|ids_two),'n_usable_after_recovery':usable,'n_unusable':len(ids_one|ids_two)-usable,'candidate_index_links':links,'source_hashes':{str(p):sha(p) for p in sources},'earlier_followups_sha256':sha(out/'followups.json'),'limits':'Scoped campaign accounting and current evidence provenance, not an all-TESS census, sensitivity calibration, false-alarm probability or planet confirmation.'})
print('distinct',len(ids_one|ids_two),'usable',usable,'unusable',len(ids_one|ids_two)-usable,'index links',len(links))
