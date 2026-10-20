"""Offline independent XML/provenance verification, no network or flux access."""
from pathlib import Path
import json,hashlib,datetime,xml.etree.ElementTree as ET
O=Path(__file__).parent
N={'v':'http://www.ivoa.net/xml/VOTable/v1.3'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(x,label):
 assert x,label
 checks.append(label)
p=json.loads((O/'plan.json').read_text());tp=json.loads((O/'target-plan.json').read_text());req=json.loads((O/'requests.json').read_text());out=json.loads((O/'targets.json').read_text())
check(sha(Path(p['identity_source']))==p['identity_sha256'],'identity input hash')
check(sha(O/'query.py')==p['script_sha256'],'schema script hash')
check(sha(O/'targets.py')==tp['script_sha256'],'target script hash')
check(sha(O/'plan.json')==tp['parent_plan_sha256'],'parent plan hash')
check(set(x['tic'] for x in out)=={80387959,402358350},'two requested identities')
source=json.loads(Path(p['identity_source']).read_text())
for target in p['targets']:
 row=next(x for x in source['rows'] if x['tic']==target['tic'])
 check(target['dr3']==row['dr3'] and target['ra']==float(row['values']['ra']) and target['dec']==float(row['values']['dec']),f"{target['tic']} exact coordinates")
control=json.loads((O/'control.json').read_text()); cp=json.loads((O/'control-plan.json').read_text())
check(sha(O/'control.py')==cp['script_sha256'],'control script hash')
check(sha(Path(cp['source_path']))==cp['source_sha256'],'control official coordinate source hash')
check(cp['created_utc']<control['started_utc'],'control plan before request')
check(control['query']==cp['query'],'frozen control query')
check(len(control['rows'])==3,'positive control returns 3 rows')
for r in req+out+[control]:
 check(sha(Path(r['path']))==r['sha256'],r.get('name',str(r.get('tic')))+' raw hash')
 check(r['status']=='success' and r['http_status']==200,'successful HTTP')
 check(p['created_utc']<r['started_utc'],'plan before request')
 if r['path'].endswith('.xml'):
  root=ET.parse(r['path']).getroot(); ns={'v':root.tag.split('}')[0][1:]}; statuses=[x.attrib.get('value') for x in root.findall('.//v:INFO',ns) if x.attrib.get('name')=='QUERY_STATUS']
  check('OK' in statuses and not set(statuses)&{'ERROR','OVERFLOW'},'XML status')
  fields=[x.attrib['name'] for x in root.findall('.//v:TABLE/v:FIELD',ns)]
  check(fields==r['columns'],'XML field schema')
  check(len(root.findall('.//v:TR',ns))==len(r['rows']),'XML row count')
for r in out:
 target=next(x for x in p['targets'] if x['tic']==r['tic'])
 expected=f"SELECT {','.join(tp['expected_columns'])} FROM dbo.raw WHERE CONTAINS(s_region,CIRCLE('',{target['ra']},{target['dec']},120./3600.))=1"
 check(r['query']==expected,'independent query reconstruction')
 check(r['query']==next(x['query'] for x in tp['queries'] if x['tic']==r['tic']),'frozen exact query')
 check(tp['created_utc']<r['started_utc'],'exact query frozen before access')
 check(len(r['rows'])==0,'empty raw table not error')
schema=req[-1]
check(tp['schema_sha256']==schema['sha256'],'schema plan hash')
check('footprints of the observations are currently not available' in next(x['description'] for x in schema['rows'] if x['column_name']=='s_region'),'raw positions are not footprints')
summary=dict(verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='passed',checks=len(checks),details=checks,limitations='Verifies metadata provenance, exact queries, schema and valid empty results, not archive completeness or astrophysical classification.')
(O/'verification.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary['status'],summary['checks'])
