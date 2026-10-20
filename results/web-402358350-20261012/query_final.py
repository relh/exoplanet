from pathlib import Path
import requests,json,csv,hashlib,datetime,concurrent.futures
p=Path(__file__).parent;root=Path('data/web-402358350-20261012');root.mkdir(exist_ok=True)
requests_list=[('rave', 'https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync', 'SELECT TOP 100 * FROM "III/283/ravedr6" WHERE 1=CONTAINS(POINT(\'ICRS\',RAJ2000,DEJ2000),CIRCLE(\'ICRS\',295.15092862046833,15.640411694115707,0.01666666667))'), ('wds_name', 'https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync', 'SELECT TOP 100 * FROM "B/wds/wds" WHERE WDS LIKE \'1940%+15%\''), ('pulsator_references_recovery', 'https://simbad.cds.unistra.fr/simbad/sim-tap/sync', 'SELECT b.bibcode,b.title FROM ref b JOIN has_ref h ON h.oidbibref=b.oidbib WHERE h.oidref=27530495')]
def get(item):
 name,url,q=item;row=dict(name=name,query=q,requested_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());save=p/f'{name}.json'
 try:
  res=requests.get(url,params=dict(REQUEST='doQuery',LANG='ADQL',FORMAT='csv',QUERY=q,MAXREC=10000),timeout=35);raw=root/f'{name}.csv';raw.write_bytes(res.content);row.update(url=res.url,http_status=res.status_code,path=str(raw),sha256=hashlib.sha256(res.content).hexdigest(),bytes=len(res.content));res.raise_for_status();reader=csv.DictReader(res.text.splitlines());assert reader.fieldnames and len(reader.fieldnames)>1,'Unexpected CSV';rows=list(reader);row.update(status='success',columns=reader.fieldnames,rows=rows)
 except Exception as exc:row.update(status='error',error=repr(exc))
 save.write_text(json.dumps(row,indent=2)+'\n');print(name,row['status'],len(row.get('rows',[])),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(get,requests_list))
