from pathlib import Path
import json,csv,io,requests
from exoplanet.pipeline import sha,save_json,now
p=Path(__file__).parent;root=Path('data/catalogs/external-coverage-402358350-20261011');root.mkdir(exist_ok=True);f=Path('results/expanded-402358350-20261011/frozen-for81.json');frozen=json.loads(f.read_text());clock=next(x for x in frozen['rows'] if x['role']=='primary');q="SELECT TOP 1000 * FROM ztf_objects_dr24 WHERE CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',295.15063723769,15.64029808626,0.004166666666666667))=1"
plan=dict(created_utc=now(),frozen_path=str(f),frozen_sha256=sha(f),clock=clock['best'],timing_ranges=clock['ranges'],metadata_query=q,query_radius_arcsec=15,photometry_policy='Freeze before any external flux. Only fixed expanded primary ephemeris and its saved profile; no period search, no maximize over timing profiles. Query source associations first. catflags0 finite positive errors; object baselines and both UTC/TDB HMJD assumptions if flux becomes available; no photometric outlier selection.',script_sha256=sha(Path(__file__)))
assert not (p/'plan.json').exists();save_json(p/'plan.json',plan);rec=dict(query=q,requested_utc=now())
try:
 r=requests.get('https://irsa.ipac.caltech.edu/TAP/sync',params=dict(REQUEST='doQuery',LANG='ADQL',FORMAT='csv',QUERY=q),timeout=(15,45));raw=root/'ztf-dr24.csv';raw.write_bytes(r.content);rec.update(url=r.url,path=str(raw),sha256=sha(raw),http_status=r.status_code,retrieved_utc=now());r.raise_for_status();reader=csv.DictReader(io.StringIO(r.text));rows=list(reader);assert {'oid','ra','dec','nobs'}<=set(reader.fieldnames or []);rec.update(status='success',rows=rows,columns=reader.fieldnames,possibly_truncated=len(rows)==1000)
except Exception as exc:rec.update(status='error',error=repr(exc))
save_json(p/'ztf-metadata.json',rec);print(rec['status'],len(rec.get('rows',[])))
