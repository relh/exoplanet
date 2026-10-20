from pathlib import Path
import requests,json,hashlib,datetime
O=Path(__file__).parent;D=Path('data')/O.name
urls={'client':'https://raw.githubusercontent.com/asas-sn/skypatrol/master/pyasassn/client.py','web':'https://asas-sn.osu.edu/','v2':'https://asas-sn.ifa.hawaii.edu/skypatrol/'}
rows=[]
for name,url in urls.items():
 row={'name':name,'url':url,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  r=requests.get(url,timeout=(10,30));p=D/(name+'.txt');p.write_bytes(r.content);row.update(url=r.url,status=r.status_code,path=str(p),sha256=hashlib.sha256(r.content).hexdigest());print(name,r.status_code,len(r.content))
 except Exception as e:row['error']=repr(e);print(name,type(e).__name__)
 rows.append(row);(O/'documentation.json').write_text(json.dumps(rows,indent=2)+'\n')
