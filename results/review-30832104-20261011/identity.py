from pathlib import Path
import csv,json
from exoplanet.pipeline import fetch,save_json,now
p=Path(__file__).parent
q="SELECT b.main_id,b.ra,b.dec,i.id FROM basic b JOIN ident i ON i.oidref=b.oid WHERE b.oid IN (SELECT oidref FROM ident WHERE id='TIC 30832104')"
rec=dict(query=q,created_utc=now())
try:
 raw=Path('data/catalogs/identity-30832104-20261011.csv');source=fetch('https://simbad.cds.unistra.fr/simbad/sim-tap/sync',raw,{'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':q});rows=list(csv.DictReader(raw.open()));assert rows and 'main_id' in rows[0];rec.update(status='success',source=source,rows=rows,path=str(raw))
except Exception as exc:rec.update(status='error',error=repr(exc))
save_json(p/'identity.json',rec);print(rec)
