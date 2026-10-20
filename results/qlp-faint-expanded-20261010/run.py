"""Search remaining frozen faint-star selection after completed pilot review."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import process_target
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;source=Path('results/qlp-faint-pool-coverage-20261010/selected-four.json')
assert not (out/'plan.json').exists()
pilot=Path('results/qlp-faint-pilot-20261010');prior=json.loads((pilot/'plan.json').read_text())['targets'];terminal=json.loads((pilot/'results.json').read_text());assert len(terminal)==len(prior)==100 and all(r['status']=='screened' for r in terminal)
prior_ids={t['tic'] for t in prior}
audit=json.loads((pilot/'audit.json').read_text());assert audit['terminal_results_present'] and audit['n_completed_files']==100
assert json.loads(Path('results/qlp-faint-pilot-followup-20261010/terminal.json').read_text())['status']=='complete'
targets=[dict(t,estimate_missing_errors=True) for t in json.loads(source.read_text()) if t['tic'] not in prior_ids]
assert len(targets)==1845 and len({t['tic'] for t in targets})==1845
save_json(out/'plan.json',{'utc':now(),'targets':targets,'source':str(source),'source_sha256':sha(source),'script_sha256':sha(Path(__file__)),'source_hashes':{p.name:sha(p) for p in Path('src/exoplanet').glob('*.py')},'pilot_audit_sha256':sha(pilot/'audit.json'),'policy':'Remaining1845 frozen targets, disjoint from initial100; radius/magnitude noise-proxy order. Four consecutive sectors ending<=96; actualbaseline<=120days. Reserved epochs unopened. Same original search and quality gates. Retain and inspect all top3peaks, including flagged peaks. Pilot sensitivity not completeness; no novelty claim.'})
(out/'targets').mkdir(exist_ok=True)
def work(t):
 r=process_target(t,Path('data'),out,load_qlp,120)
 return {k:r.get(k) for k in ['tic','status','error','disposition']}
rows=[]
with ThreadPoolExecutor(max_workers=4) as ex:
 for r in ex.map(work,targets):
  rows.append(r);save_json(out/'progress.json',{'utc':now(),'n_done':len(rows),'n_total':len(targets),'rows':rows})
save_json(out/'results.json',rows)
