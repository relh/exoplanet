from pathlib import Path
import json,hashlib
from bs4 import BeautifulSoup
O=Path(__file__).parent;rows=json.loads((O/'documentation.json').read_text())
for row in rows:
 if 'path' in row:assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256']
client=Path(rows[0]['path']).read_text();assert 'asassn-lb01.ifa.hawaii.edu:9006/get_schema' in client
soup=BeautifulSoup(Path(rows[1]['path']).read_text(),'html.parser');form=soup.find('form',action='/sky-patrol/computation/check');assert form and form.find(attrs={'name':'query[ra]'}) and form.find(attrs={'name':'query[dec]'}) and form.find(class_='g-recaptcha')
assert rows[1]['status']==200 and 'error' in rows[2]
(O/'verification.json').write_text(json.dumps({'status':'passed','raw_hashes':2,'form_action':form['action'],'captcha_present':True,'scope':'Raw response hashes and static form/client endpoint inspection. No target catalog query, backend-computation test or flux access.'},indent=2)+'\n');print('PASS: documentation provenance and form fields')
