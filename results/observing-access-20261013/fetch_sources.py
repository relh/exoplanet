"""Snapshot public access/instrument documentation; no credentials or observations."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import hashlib,json,urllib.request
root=Path('data/observing-access-20261013');root.mkdir(parents=True,exist_ok=True)
urls={
'lco-sites':'https://lco.global/observatory/sites/',
'lco-process':'https://lco.global/observatory/process/',
'lco-2027a':'https://lco.global/news/callforproposals2027a/',
'lco-sinistro':'https://lco.global/observatory/instruments/sinistro/',
'lco-1m':'https://lco.global/observatory/telescopes/1m0/1m-spec/',
'lco-partners':'https://lco.global/education/partners/',
'lco-education-access':'https://lco.global/education/activities/preparing-an-observation-request-on-lco/',
'itelescope-t17':'https://support.itelescope.net/support/solutions/articles/231915-telescope-17',
'itelescope-terms':'https://www.itelescope.net/terms-of-use',
'itelescope-reservations':'https://support.itelescope.net/support/solutions/articles/143104-i-am-unable-to-create-a-reservation-what-can-i-do-',
'itelescope-plan-quotas':'https://go.itelescope.net/info.aspx',
'aavsonet':'https://archive.aavso.org/index.php/aavsonet',
'aavsonet-proposal':'https://archive.aavso.org/index.php/how-write-aavsonet-proposal',
'aavso-membership':'https://aavso.org/become-a-member/',
}
def get(item):
 name,url=item;row={'id':name,'url':url,'retrieved_utc':datetime.now(timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'exoplanet-observing-access-documentation/1.0'}),timeout=45) as r:
   body=r.read(); row.update(status=r.status,final_url=r.url,content_type=r.headers.get('content-type'))
  p=root/(name+'.html');p.write_bytes(body);row.update(path=str(p),bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
 except Exception as e:row['error']=str(e)
 return row
with ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(get,urls.items()))
Path('results/observing-access-20261013/sources.json').write_text(json.dumps({'scope':'public documentation only; no observation data or private account access','sources':rows},indent=2)+'\n')
for row in rows:print(row['id'],row.get('status'),row.get('error',''),row.get('bytes'))
