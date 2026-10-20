from pathlib import Path
import requests,json,hashlib,datetime
O=Path('results/web-241928959-20261012');D=Path('data/web-241928959-20261012')
jobs=[('spyglass-readme','https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/ApJ/954/134',{'format':'html','tex':'true'}),('spyglass-exact','https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync',{'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':'SELECT TOP 10 * FROM "J/ApJ/954/134/table1" WHERE Gaia=6865254022910168320'}),('simbad-ident','https://simbad.cds.unistra.fr/simbad/sim-tap/sync',{'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':'SELECT id FROM ident WHERE oidref=30823552'}),('simbad-refs','https://simbad.cds.unistra.fr/simbad/sim-tap/sync',{'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':'SELECT bibcode FROM has_ref WHERE oidref=30823552'})]
rows=[]
for name,url,params in jobs:
 try:
  r=requests.get(url,params=params,timeout=90);p=D/(name+'.response');p.write_bytes(r.content);rows.append(dict(name=name,url=r.url,status=r.status_code,path=str(p),sha256=hashlib.sha256(r.content).hexdigest(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()));print(name,r.status_code,r.text[:1200],flush=True)
 except Exception as e:rows.append(dict(name=name,error=str(e),url=url,params=params))
 (O/'queries.json').write_text(json.dumps(rows,indent=2))
