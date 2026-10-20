"""Independent checks of saved request fields, empty table markers and file hashes."""
from pathlib import Path
import json,hashlib,re
B=Path(__file__).resolve().parent; R=B.parents[1]
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=read(B/'plan.json'); s=read(B/'summary.json'); checks=[]
def check(name,ok):
 checks.append({'check':name,'pass':bool(ok)})
check('frozen plan hash',sha(B/'plan.json')==(B/'plan.sha256').read_text().split()[0])
check('source identity snapshot',sha(R/p['source_path'])==p['source_sha256'])
check('two target queries',len(s['queries'])==2)
for prov in read(B/'provenance.json'):check('raw hash '+prov['path'],sha(R/prov['path'])==prov['sha256'])
for t,q in zip(p['targets'],s['queries']):
 tic=t['tic']; fields=q['query_fields']; raw=R/'data/cheops-metadata-20261013'
 check(tic+' query after freeze',q['request_utc']>p['frozen_utc'])
 check(tic+' RA',float(fields['ra'])==t['ra_deg'])
 check(tic+' Dec',float(fields['dec'])==t['dec_deg'])
 check(tic+' radius degrees',abs(float(fields['radious'])*3600-120)<1e-10)
 check(tic+' unrestricted dates',fields['visit-start']==fields['visit-stop']=='')
 check(tic+' all proprietary statuses',fields['proprietary-st']=='ALL')
 check(tic+' latest version',fields['revision-nb']=='latest')
 check(tic+' successful HTTP',q['http_status']==200)
 h=(raw/f'{tic}-result.html').read_text()
 check(tic+' empty table marker','No data available in table' in h)
 check(tic+' zero count','Showing 0 to 0 of 0 entries' in h)
 check(tic+' no observation links',not re.search(r'CH_PR\d+',re.search(r'<table id="results".*?</table>',h,re.S).group(0)))
 check(tic+' empty classification',q['status']=='completed_empty_table' and q['returned_entries']==0)
c=read(B/'control-summary.json'); cp=read(B/'control-plan.json')
check('control plan hash',sha(B/'control-plan.json')==(B/'control-plan.sha256').read_text().split()[0])
check('control HTTP',c['http_status']==200)
check('control coordinate only',c['query_fields']['target-name']=='')
check('control same radius',abs(float(c['query_fields']['radious'])*3600-120)<1e-10)
check('control same filters',all(c['query_fields'][k]==s['queries'][0]['query_fields'][k] for k in ['proprietary-st','revision-nb','visit-start','visit-stop']))
check('control eight visits',c['returned_entries']==len(c['rows'])==8)
check('control all target',all(row[3]=='WASP-189' for row in c['rows']))
check('control all public',all(row[9]=='PUBLIC' for row in c['rows']))
check('control displayed eight','Showing 1 to 8 of 8 entries' in (R/'data/cheops-metadata-20261013/control-result.html').read_text())
check('metadata only',not s['new_flux_opened'])
out={'checks':checks,'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'limits':'Checks verify saved query provenance and displayed results, not archive completeness or planetary origin.'}
(B/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(out['passed'],out['failed']);assert out['failed']==0
