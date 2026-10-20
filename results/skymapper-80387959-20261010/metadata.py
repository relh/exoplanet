"""Get exact image timing and object metadata for returned detections."""
from pathlib import Path
import json
from astropy.io.votable import parse
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent;t=parse('data/catalogs/skymapper-80387959-dr4-photometry.xml').get_first_table().to_table()
for table,key in [('images','image_id'),('master','object_id')]:
 ids=sorted({int(v) for v in t[key]});query=f'SELECT * FROM dr4.{table} WHERE {key} IN ('+','.join(map(str,ids))+')'
 params={'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'votable','MAXREC':10000,'QUERY':query};p=Path(f'data/catalogs/skymapper-80387959-dr4-{table}.xml')
 save_json(out/f'{table}-request.json',{'utc':now(),'params':params,'script_sha256':sha(Path(__file__))})
 try:
  m=fetch('https://api.skymapper.nci.org.au/public/tap/sync',p,params);save_json(out/f'{table}-source.json',m)
  v=parse(p);statuses=[{'name':i.name,'value':i.value,'content':i.content} for r in v.resources for i in r.infos];save_json(out/f'{table}-status.json',statuses)
  if any(i['value'] in ['ERROR','OVERFLOW'] for i in statuses):raise ValueError(statuses)
  tab=v.get_first_table().to_table();assert {int(v) for v in tab[key]}==set(ids)
  save_json(out/f'{table}-schema.json',{'n_rows':len(tab),'columns':[{'name':c,'unit':str(tab[c].unit),'description':tab[c].description} for c in tab.colnames]});print(table,len(tab),flush=True)
 except Exception as exc:save_json(out/f'{table}-error.json',{'utc':now(),'error':repr(exc)});print(table,repr(exc),flush=True)
