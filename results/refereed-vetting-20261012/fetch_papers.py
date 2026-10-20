from pathlib import Path
from datetime import datetime,timezone
import requests,hashlib,json
from bs4 import BeautifulSoup
out=Path('results/refereed-vetting-20261012');raw=Path('data/refereed-vetting-20261012')
items=[]
for label,ident in [('giacalone2022','2201.12661'),('eisner2021','2011.13944'),('cacciapuoti2022','2203.15826')]:
 for kind in ['abs','html']:
  url=f'https://arxiv.org/{kind}/{ident}';record=dict(label=label,kind=kind,url=url,retrieved_utc=datetime.now(timezone.utc).isoformat())
  try:
   r=requests.get(url,timeout=35);p=raw/f'{label}-{kind}.html';p.write_bytes(r.content);record.update(status=r.status_code,path=str(p),sha256=hashlib.sha256(r.content).hexdigest())
   if r.ok:
    soup=BeautifulSoup(r.text,'html.parser');(raw/f'{label}-{kind}.txt').write_text(soup.get_text(' ',strip=True))
  except Exception as e:record['error']=str(e)
  items.append(record);(out/'sources.json').write_text(json.dumps(items,indent=2))
print([(r['label'],r['kind'],r.get('status',r.get('error'))) for r in items])
