from pathlib import Path
import requests,csv,io
from exoplanet.pipeline import save_json,sha,now
p=Path(__file__).parent;raw=Path('data/catalogs/novelty-402358350-20261011/simbad-references.csv');q="SELECT r.bibcode,r.title,r.doi FROM ref AS r JOIN has_ref AS h ON h.oidbibref=r.oidbib WHERE h.oidref IN (SELECT oidref FROM ident WHERE id='TIC 402358350')";rec=dict(query=q,requested_utc=now())
try:
 r=requests.get('https://simbad.cds.unistra.fr/simbad/sim-tap/sync',params=dict(request='doQuery',lang='adql',format='csv',query=q),timeout=(15,60));raw.write_bytes(r.content);rec.update(url=r.url,path=str(raw),sha256=sha(raw),retrieved_utc=now(),http_status=r.status_code);r.raise_for_status();reader=csv.DictReader(io.StringIO(r.text));rows=list(reader);assert {'bibcode','title','doi'}<=set(reader.fieldnames or []);rec.update(status='success',rows=rows)
except Exception as exc:rec.update(status='error',error=repr(exc))
save_json(p/'references.json',rec);print(rec)
