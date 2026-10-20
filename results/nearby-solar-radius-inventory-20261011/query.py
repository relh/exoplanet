from pathlib import Path
import requests,json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent
req={'service':'Mast.Catalogs.Filtered.Tic.Rows','params':{'columns':'ID,ra,dec,Tmag,rad,Teff,d,contratio,disposition,duplicate_id','filters':[{'paramName':'rad','values':[{'min':.81,'max':1.1}]},{'paramName':'Tmag','values':[{'min':6,'max':12}]},{'paramName':'d','values':[{'min':0,'max':120}]}]},'format':'json','pagesize':100000,'page':1}
save_json(out/'request.json',req)
r=requests.post('https://mast.stsci.edu/api/v0/invoke',data={'request':json.dumps(req)},timeout=(20,60));r.raise_for_status();p=Path('data/targeting/nearby-solar-radius-20261011.json');p.write_bytes(r.content)
save_json(out/'source.json',dict(url=r.url,request=req,path=str(p),sha256=sha(p),retrieved_utc=now()))
a=r.json();assert a['status']=='COMPLETE';rows=a['data'];assert len(rows)==a['paging']['rowsFiltered']==len({s['ID'] for s in rows})
assert all(.81<=s['rad']<=1.1 and 6<=s['Tmag']<=12 and 0<=s['d']<=120 for s in rows)
print('complete',len(rows))
