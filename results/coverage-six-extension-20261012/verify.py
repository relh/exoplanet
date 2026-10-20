from pathlib import Path
import json,hashlib
O=Path(__file__).parent
plan=json.loads((O/'plan.json').read_text());records=json.loads((O/'manifest.json').read_text());rows=json.loads((O/'results.json').read_text())['rows']
checks=[]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(plan['input'])==plan['sha256'];checks.append('coordinate input hash')
for r in records:
 assert r.get('http_status')==200 and sha(r['path'])==r['sha256'];checks.append(r['name']+' raw hash/status')
q=next(r for r in records if r['name']=='qlp');data=json.loads(Path(q['path']).read_text());assert data['status']=='COMPLETE' and len(data['data'])==data['paging']['rowsFiltered'];checks.append('QLP pagination complete')
for row in rows:
 tic=str(row['tic']);meta=next(r for r in records if r['name']==tic);d=json.loads(Path(meta['path']).read_text());sectors=sorted({int(x['sector']) for x in d['results']});assert row['footprint_sectors']==sectors;assert row['not_documented_opened']==sorted(set(sectors)-set(plan['opened_sectors'][tic]));assert meta['params']==plan['coordinates'][tic]
 qs=sorted({int(x['sequence_number']) for x in data['data'] if str(x['target_name'])==tic});assert qs==row['qlp_sectors'];assert row['qlp_not_documented_opened']==sorted(set(qs)-set(plan['opened_sectors'][tic]));checks.append(tic+' footprint/QLP independent reconciliation')
(O/'verification.json').write_text(json.dumps({'status':'passed','checks':checks,'scope':'Raw hashes, exact query positions/target IDs, response pagination and sector-set arithmetic; not detector-edge usability or unopened-history proof.'},indent=2)+'\n');print('PASS',len(checks))
