from pathlib import Path
import json,csv,io,requests
from exoplanet.pipeline import save_json,sha,now
O=Path(__file__).parent
q={'service':'Mast.Catalogs.Filtered.Tic.Rows','params':{'columns':'ID,ra,dec,GAIA,TYC,HIP','filters':[{'paramName':'ID','values':['459244300']}]},'format':'json','pagesize':100,'page':1};record=dict(created_utc=now(),request=q,status='error')
try:
 r=requests.post('https://mast.stsci.edu/api/v0/invoke',data={'request':json.dumps(q)},timeout=40);r.raise_for_status();raw=Path('data/targeting/tic459244300-exact.json');raw.write_bytes(r.content);x=r.json();record.update(url=r.url,path=str(raw),sha256=sha(raw),response=x);assert x['status']=='COMPLETE' and len(x['data'])==1 and int(x['data'][0]['ID'])==459244300
 dr2=x['data'][0]['GAIA'];query=f'select dr2_source_id,dr3_source_id from gaiadr3.dr2_neighbourhood where dr2_source_id={dr2}';rr=requests.get('https://gea.esac.esa.int/tap-server/tap/sync',params=dict(REQUEST='doQuery',LANG='ADQL',FORMAT='csv',QUERY=query),timeout=40);rr.raise_for_status();pp=Path('data/targeting/tic459244300-dr2-dr3.csv');pp.write_bytes(rr.content);rows=list(csv.DictReader(io.StringIO(rr.text)));record.update(status='complete',mapping=dict(query=query,url=rr.url,path=str(pp),sha256=sha(pp),rows=rows))
except Exception as e:record['error']=repr(e)
save_json(O/'tic-identity.json',record);print(record)
