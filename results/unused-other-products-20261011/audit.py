from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(out/'plan.json');assert sha(Path(plan['source']))==plan['source_sha256'] and sha(out/'run.py')==plan['script_sha256']
results=read(out/'results.json');expected={r['tic']:r for r in plan['targets']};ids=[i for r in results for i in r['ids']];assert len(ids)==len(set(ids))==1885 and set(ids)==set(expected)
obs={};errors=[];counts=Counter()
for r in results:
 if r['status']=='error':errors+=r['ids'];continue
 p=Path(r['path']);assert sha(p)==r['sha256'];data=read(p);meta=read(p.with_suffix('.provenance.json'));assert meta['sha256']==sha(p)
 assert data['status']=='COMPLETE' and len(data['data'])==data['paging']['rowsFiltered']==r['n_rows']
 filters=meta['request']['params']['filters'];assert {int(x) for x in filters[0]['values']}==set(r['ids'])
 assert set(filters[1]['values'])=={'SPOC','TESS-SPOC'}
 for row in data['data']:
  tic=int(row['target_name']);assert tic in r['ids'] and row['provenance_name'] in ['SPOC','TESS-SPOC'];obs.setdefault(tic,[]).append(row)
rows=[]
for tic,t in expected.items():
 found=obs.get(tic,[]);sectors=sorted({int(x['sequence_number']) for x in found if x['sequence_number'] is not None});new=sorted(set(sectors)-set(t['sectors']))
 category='query_error' if tic in errors else 'additional_sector_metadata' if new else 'same_sector_only' if found else 'no_exact_name_match'
 counts[category]+=1;rows.append({**t,'category_original':t['category'],'category':category,'other_product_sectors':sectors,'additional_sectors':new,'observations':found})
save_json(out/'audit.json',{'script_sha256':sha(Path(__file__)),'plan_sha256':sha(out/'plan.json'),'results_sha256':sha(out/'results.json'),'n_targets':len(rows),'counts':dict(counts),'rows':rows,'limits':'Exact-name metadata query only. Different pipeline in same sector shares photons. Additional-sector metadata requires product/FITS validation before selection; no photometry, novelty or completeness claim.'})
print(dict(counts));print('additional examples',[(r['tic'],r['sectors'],r['additional_sectors']) for r in rows if r['additional_sectors']][:20])
