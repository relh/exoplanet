from pathlib import Path
import requests,json,hashlib,datetime
O=Path('results/extension-469309982-96166003-20261012');D=Path('data/extension-469309982-96166003-20261012')
rows=[]
for tic,g in [(469309982,'5259582389096040960'),(96166003,'161856980718462208')]:
 for typ,query in [('identity',f"SELECT b.oid,b.main_id,b.ra,b.dec,b.otype,b.nbref FROM basic b JOIN ident i ON i.oidref=b.oid WHERE i.id='Gaia DR3 {g}'"),('aliases',f"SELECT j.id FROM ident i JOIN ident j ON i.oidref=j.oidref WHERE i.id='Gaia DR3 {g}'"),('bibliography',f"SELECT r.bibcode FROM ident i JOIN has_ref h ON h.oidref=i.oidref JOIN ref r ON r.oidbib=h.oidbibref WHERE i.id='Gaia DR3 {g}'")]:
  name=f'{tic}-{typ}';url='https://simbad.cds.unistra.fr/simbad/sim-tap/sync'
  try:
   r=requests.get(url,params={'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':query},timeout=90);p=D/(name+'.csv');p.write_bytes(r.content);rows.append(dict(name=name,url=r.url,path=str(p),status=r.status_code,sha256=hashlib.sha256(r.content).hexdigest(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()));print(name,r.status_code,r.text[:4500],flush=True)
  except Exception as e:rows.append(dict(name=name,error=str(e),query=query,url=url))
  (O/'queries.json').write_text(json.dumps(rows,indent=2))
