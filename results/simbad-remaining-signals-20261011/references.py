from pathlib import Path
import requests,json,hashlib,csv,io
out=Path(__file__).parent
queries={'identifiers':'SELECT oidref,id FROM ident WHERE oidref IN (30823552,24982167)','references':'SELECT h.oidref,r.bibcode,r.doi,r.title,r.abstract FROM has_ref AS h JOIN ref AS r ON h.oidbibref=r.oidbib WHERE h.oidref IN (30823552,24982167)'}
results=[]
for label,q in queries.items():
 rec=dict(label=label,query=q)
 try:
  r=requests.get('https://simbad.cds.unistra.fr/simbad/sim-tap/sync',params=dict(request='doQuery',lang='adql',format='csv',query=q),timeout=45);r.raise_for_status();p=Path(f'data/targeting/simbad-two-{label}-20261011.csv');p.write_bytes(r.content)
  rec.update(status='success',url=r.url,path=str(p),sha256=hashlib.sha256(r.content).hexdigest(),rows=list(csv.DictReader(io.StringIO(r.text))))
 except Exception as e:rec.update(status='error',error=repr(e))
 results.append(rec)
(out/'references.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
