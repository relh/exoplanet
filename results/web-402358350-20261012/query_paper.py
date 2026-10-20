from pathlib import Path
import requests,json,csv,hashlib,datetime,concurrent.futures
p=Path(__file__).parent;root=Path('data/web-402358350-20261012');root.mkdir(exist_ok=True)
requests_list=[('pulsator_paper_schema', 'https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync', "SELECT table_name,column_name,unit,description FROM TAP_SCHEMA.columns WHERE table_name LIKE '%J/A+A/672/A183%'")]
def get(item):
 name,url,q=item;row=dict(name=name,query=q,requested_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());save=p/f'{name}.json'
 try:
  res=requests.get(url,params=dict(REQUEST='doQuery',LANG='ADQL',FORMAT='csv',QUERY=q,MAXREC=10000),timeout=35);raw=root/f'{name}.csv';raw.write_bytes(res.content);row.update(url=res.url,http_status=res.status_code,path=str(raw),sha256=hashlib.sha256(res.content).hexdigest(),bytes=len(res.content));res.raise_for_status();reader=csv.DictReader(res.text.splitlines());assert reader.fieldnames and len(reader.fieldnames)>1,'Unexpected CSV';rows=list(reader);row.update(status='success',columns=reader.fieldnames,rows=rows)
 except Exception as exc:row.update(status='error',error=repr(exc))
 save.write_text(json.dumps(row,indent=2)+'\n');print(name,row['status'],len(row.get('rows',[])),flush=True)
for item in requests_list:get(item)
