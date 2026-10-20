import requests,json,hashlib,datetime,pathlib,sys
R=pathlib.Path(__file__).parent; D=pathlib.Path('data')/R.name; M=R/'manifest.json'
def get(name,url,params=None):
 p=D/(name+'.txt'); assert not p.exists(),p
 rec={'name':name,'requested_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'request_url':url,'params':params}
 try:
  a=requests.get(url,params=params,timeout=60);p.write_bytes(a.content);rec.update(url=a.url,status=a.status_code,bytes=len(a.content),sha256=hashlib.sha256(a.content).hexdigest(),path=str(p)); print(name,a.status_code,len(a.content),a.text[:200])
 except Exception as e: rec['error']=repr(e);print(rec)
 rec['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();m=json.loads(M.read_text()) if M.exists() else [];m.append(rec);M.write_text(json.dumps(m,indent=2)+'\n')
 return rec
if __name__=='__main__':
 for n in ['SuperWASPUsage','program_interfaces','TAP']:
  get(n,'https://exoplanetarchive.ipac.caltech.edu/docs/'+n+'.html')
 get('tap-tables','https://exoplanetarchive.ipac.caltech.edu/TAP/sync',{'query':"select table_name,description from TAP_SCHEMA.tables where table_name like '%wasp%'",'format':'json'})
