"""Indexed object cone before exact-object measurement query; public NSC DR2."""
from pathlib import Path
from astropy.io.votable import parse
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent
query="SELECT * FROM nsc_dr2.object WHERE 1=CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',165.31041473672,-48.6136321332977,0.006944444444))"
for name in ['objects','measurements']:
 params={'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'votable','MAXREC':100000,'QUERY':query};p=Path(f'data/catalogs/nsc-80387959-{name}.xml')
 save_json(out/f'{name}-request.json',{'utc':now(),'params':params,'script_sha256':sha(Path(__file__)),'documentation':'https://datalab.noirlab.edu/data/nsc','policy':'Public25arcsec object cone, then explicit returned object IDs for epoch measurements. No phase optimization or interpretation before quality/time metadata review.'})
 try:
  m=fetch('https://datalab.noirlab.edu/tap/sync',p,params);save_json(out/f'{name}-source.json',m)
  v=parse(p);status=[{'name':i.name,'value':i.value,'content':i.content} for r in v.resources for i in r.infos];save_json(out/f'{name}-status.json',status)
  if any(i['value'] in ['ERROR','OVERFLOW'] for i in status):raise ValueError(status)
  t=v.get_first_table().to_table();save_json(out/f'{name}-schema.json',{'n_rows':len(t),'columns':[{'name':c,'unit':str(t[c].unit),'description':t[c].description} for c in t.colnames]});print(name,len(t),flush=True)
  if name=='objects':
   ids=[str(r['id']) for r in t];assert 0<len(ids)<=100,'Empty/oversized object result; no measurement inference'
   query='SELECT * FROM nsc_dr2.meas WHERE objectid IN ('+','.join("'"+x.replace("'","''")+"'" for x in ids)+')'
 except Exception as exc:save_json(out/f'{name}-error.json',{'utc':now(),'error':repr(exc)});print(name,repr(exc),flush=True);break
