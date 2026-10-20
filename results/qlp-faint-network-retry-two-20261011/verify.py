from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(out/'plan.json');rows=[]
assert sha(out/'run.py')==plan['script_sha256']
for r in plan['records']:
 p=Path(r['original_path']);assert sha(p)==r['original_sha256']
 q=out/'targets'/f"{r['tic']}.json";a=read(q);assert a['target']==r['target'] and a['status']=='screened' and a['started_utc']>=plan['utc']
 for ev in a['data']:assert sha(Path(f"data/qlp/{r['tic']}-s{ev['sector']:04d}.fits"))==ev['source']['sha256']
 assert all(not Path(f"data/qlp/{r['tic']}-s{s:04d}.fits").exists() for s in a['target']['heldout_sectors'])
 rows.append({'tic':r['tic'],'path':str(q),'sha256':sha(q),'disposition':a['disposition'],'flags':[x['flags'] for x in a.get('screened_peaks',[])]})
save_json(out/'verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'limits':'Same original targets/settings; one retry after terminal DNS failures. Original records unchanged, reserved sectors unopened, no additional stars.'})
print('Verified two successful network retries and preserved originals.')
