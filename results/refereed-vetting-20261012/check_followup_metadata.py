from pathlib import Path
from datetime import datetime,timezone
import requests,hashlib,json,re
from bs4 import BeautifulSoup
out=Path('results/refereed-vetting-20261012');raw=Path('data/refereed-vetting-20261012');records=[]
for tic in [80387959,402358350]:
 url=f'https://exofop.ipac.caltech.edu/tess/target.php?id={tic}';rec={'tic':tic,'url':url,'retrieved_utc':datetime.now(timezone.utc).isoformat(),'scope':'Public target-page metadata only; no follow-up flux, images or spectra downloaded.'}
 try:
  r=requests.get(url,timeout=30);p=raw/f'exofop-{tic}.html';p.write_bytes(r.content);rec.update(status=r.status_code,path=str(p),sha256=hashlib.sha256(r.content).hexdigest())
  if r.ok:
   soup=BeautifulSoup(r.text,'html.parser');(raw/f'exofop-{tic}.txt').write_text(soup.get_text(' ',strip=True))
   tables={}
   for var,body in re.findall(r'var (rowData\d*)\s*=\s*(\[.*?\]);',r.text,re.S):
    try:tables[var]=json.loads(body)
    except Exception as e:tables[var]={'parse_error':str(e)}
   rec['embedded_tables']=tables
 except Exception as e:rec['error']=str(e)
 records.append(rec);(out/'followup-metadata.json').write_text(json.dumps(records,indent=2))
print([(r['tic'],r.get('status'),{k:len(v) for k,v in r.get('embedded_tables',{}).items()}) for r in records])
