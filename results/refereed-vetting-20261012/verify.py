from pathlib import Path
import json,hashlib,re
from bs4 import BeautifulSoup
P=Path(__file__).parent
n=0
for filename in ['sources.json','followup-metadata.json']:
 for row in json.loads((P/filename).read_text()):
  if 'path' not in row:continue
  p=Path(row['path']);assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'];n+=1
  if filename=='followup-metadata.json':
   text=BeautifulSoup(p.read_text(),'html.parser').get_text(' ',strip=True)
   for section in ['Imaging Observations','Spectroscopy Observations','Time Series Observations','Files']:
    assert re.search(re.escape(section)+r' 0 Add new',text);n+=1
   for variable in ['rowData','rowData2','rowData3']:
    assert row['embedded_tables'][variable]==[];n+=1
print(f'PASS: {n} document-hash and public-inventory checks')
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':n,'scope':'Saved document hashes and public inventory parsing, not completeness of astronomy archives.'},indent=2))
