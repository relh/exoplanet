"""Summarize saved anonymous CHEOPS query metadata; never accesses network/flux."""
from pathlib import Path
import json, hashlib, re, datetime
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[1]
RAW=ROOT/'data/cheops-metadata-20261013'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text())
plan=load(BASE/'plan.json')
queries=[]
for target in plan['targets']:
 tic=target['tic']; req=load(RAW/f'{tic}-request.json')['data']
 fields=dict(re.findall(r'name="([^"]+)"\r\n\r\n([^\r]*)',req['postData']))
 html=(RAW/f'{tic}-result.html').read_text()
 matches=re.findall(r'Showing 0 to 0 of 0 entries|No data available in table',html)
 queries.append(dict(tic=tic,query_fields=fields,query_url=req['url'],request_utc=datetime.datetime.fromtimestamp(req['timestamp']/1000,datetime.timezone.utc).isoformat(),response_date=req['responseHeaders']['Date'],http_status=req['status'],result_url='https://cheops.unige.ch/archive_browser/index.php/results-page/',status='completed_empty_table' if req['status']==200 and len(matches)==2 else 'requires_review',returned_entries=0 if len(matches)==2 else None,result_markers=matches))
provenance=[]
for p in sorted(RAW.iterdir()):
 provenance.append(dict(path=str(p.relative_to(ROOT)),sha256=digest(p),bytes=p.stat().st_size,saved_utc=datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat(),source_url='https://cheops.unige.ch/archive_browser/index.php/wp-json/contact-form-7/v1/contact-forms/42/feedback' if p.name=='control-request.json' else 'https://cheops.unige.ch/archive_browser/index.php/results-page/' if p.name=='control-result.txt' else 'https://cheops.unige.ch/archive_browser/' if p.name=='control-resolved.txt' else 'https://cheops.unige.ch/archive_browser/' if p.name.endswith(('network.json','input.html')) else 'https://cheops.unige.ch/archive_browser/index.php/results-page/' if p.name.endswith('result.html') else next((q['query_url'] for q in queries if p.name==q['tic']+'-request.json'),next((d['url'] for d in load(BASE/'documentation.json') if d.get('path')==str(p.relative_to(ROOT))),None))))
(BASE/'summary.json').write_text(json.dumps({'plan_sha256':digest(BASE/'plan.json'),'queries':queries,'new_flux_opened':False},indent=2)+'\n')
(BASE/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
print([(q['tic'],q['status']) for q in queries])
