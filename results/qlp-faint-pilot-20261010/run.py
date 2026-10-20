"""Frozen 100-star pilot; four training sectors, unopened reserved epochs."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import process_target
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;source=Path('results/qlp-faint-pool-coverage-20261010/selected-four.json')
assert not (out/'plan.json').exists()
targets=[dict(t,estimate_missing_errors=True) for t in json.loads(source.read_text())[:100]]
save_json(out/'plan.json',{'utc':now(),'targets':targets,'source':str(source),'source_sha256':sha(source),'script_sha256':sha(Path(__file__)),'source_hashes':{p.name:sha(p) for p in Path('src/exoplanet').glob('*.py')},'policy':'First100 in frozen radius/magnitude noise-proxy order. Four consecutive sectors ending<=96; actualbaseline<=120days. Reserved epochs unopened. Same original search and quality gates. Retain and inspect all top3peaks, including flagged peaks. Pilot sensitivity not completeness; no novelty claim.'})
(out/'targets').mkdir(exist_ok=True)
def work(t):
 r=process_target(t,Path('data'),out,load_qlp,120)
 return {k:r.get(k) for k in ['tic','status','error','disposition']}
rows=[]
with ThreadPoolExecutor(max_workers=2) as ex:
 for r in ex.map(work,targets):
  rows.append(r);save_json(out/'progress.json',{'utc':now(),'n_done':len(rows),'n_total':len(targets),'rows':rows})
save_json(out/'results.json',rows)
