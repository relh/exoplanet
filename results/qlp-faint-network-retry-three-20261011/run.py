"""One separate retry of terminal DNS failures with unchanged discovery inputs."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
from exoplanet.pipeline import sha,save_json,now
from exoplanet.campaign import process_target
from exoplanet.qlp_campaign import load_qlp
out=Path(__file__).parent
campaign=Path('results/qlp-faint-midradius-remaining-three-20261011')
read=lambda p:json.loads(p.read_text())
plan=read(campaign/'plan.json')
for name,h in plan['source_hashes'].items():assert sha(Path('src/exoplanet')/name)==h
records=[]
for tic in [369990670,67326261,279375922,385555011]:
 p=campaign/'targets'/f'{tic}.json';r=read(p)
 assert r['status']=='error' and 'NameResolutionError' in r['error'] and r['finished_utc']
 assert all(not Path(f'data/qlp/{tic}-s{s:04d}.fits').exists() for s in r['target']['heldout_sectors'])
 records.append({'tic':tic,'original_path':str(p),'original_sha256':sha(p),'target':r['target']})
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'campaign_plan_sha256':sha(campaign/'plan.json'),'records':records,'policy':'One retry after terminal DNS errors, identical targets/training/heldout/settings/core; separate files retain originals. Recovery adds attempts, not stars. No holdout opening.'})
(out/'targets').mkdir()
def work(r):
 result=process_target(r['target'],Path('data'),out,load_qlp,120)
 return {k:result.get(k) for k in ['tic','status','disposition','error']}
with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(work,records))
save_json(out/'results.json',rows);print(rows)
