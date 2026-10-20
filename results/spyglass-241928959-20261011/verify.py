from pathlib import Path
import json,hashlib,csv,io
p=Path(__file__).parent
rs=json.loads((p/'results.json').read_text()); doc=json.loads((p/'documentation.json').read_text())
for r in rs+[doc]:
 raw=Path(r['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==r['sha256']
 if 'rows' in r:assert list(csv.DictReader(io.StringIO(raw.decode())))==r['rows']
assert len(rs[0]['rows'])==1 and not rs[1]['rows']
r=rs[0]['rows'][0]
t=next(t for t in json.loads(Path('results/gaia-241928959-scene-20261011/plan.json').read_text())['targets'] if t['ID']==241928959)
assert r['Gaia']==t['GAIA'];assert r['TLC']==r['EOM']=='-1'
(p/'verification.json').write_text(json.dumps(dict(status='passed',raw_hashes_checked=3,exact_tic_gaia_dr2_match=r['Gaia'],probability_younger_than_50_myr=float(r['Prob']),catalog_age_myr=float(r['Age']),upper_error_myr=float(r['E_Age']),lower_error_myr=float(r['e_Age']),assigned_cluster=False),indent=2)+'\n')
