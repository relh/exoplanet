"""Require full campaign coverage and follow-up of every unflagged peak."""
from pathlib import Path
import json
from collections import Counter
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
sel=Path('results/selection-late-sectors-20261010/eligible.json');targets=json.loads(sel.read_text());expected={r['tic'] for r in targets}
rows={};records=[];run_sources=[]
for n in [1,2]:
 root=Path(f'results/campaign-late-sectors-batch{n}-20261010');run=json.loads((root/'run.json').read_text())
 assert run['status']=='complete';assert run['selection_sha256']==sha(sel)
 run_sources.append({'path':str(root/'run.json'),'sha256':sha(root/'run.json')})
 for p in (root/'targets').glob('*.json'):
  r=json.loads(p.read_text());assert r['tic'] not in rows
  rows[r['tic']]=r;records.append({'tic':r['tic'],'path':str(p),'sha256':sha(p)})
assert set(rows)==expected and len(rows)==1322
follow={}
for root in [Path('results/followup-late-420359321-20261010'),Path('results/followup-late-395477762-20261010'),*Path('results/late-sector-followup-20261010').glob('[0-9]*')]:
 if not root.is_dir():continue
 f=json.loads((root/'frozen.json').read_text());held=json.loads((root/'heldout.json').read_text());assert len(held)==len(f['heldout_sectors'])
 follow[(f['tic'],f['seed']['period'])]={'frozen_path':str(root/'frozen.json'),'frozen_sha256':sha(root/'frozen.json'),'heldout_path':str(root/'heldout.json'),'heldout_sha256':sha(root/'heldout.json'),'assessment':str(root/'ASSESSMENT.md'),'assessment_exists':(root/'ASSESSMENT.md').exists(),'results':[{'sector':x['sector'],'status':x['status'],'conclusion':x.get('conclusion',x.get('error'))} for x in held]}
priorities=[];counts=Counter()
for tic,r in rows.items():
 counts[r.get('disposition',r['status'])]+=1
 for i,p in enumerate(r.get('screened_peaks',[])):
  if not p['flags']:
   key=(tic,p['best']['period']);assert key in follow,('Missing follow-up',tic,i)
   assert follow[key]['assessment_exists'],('Missing assessment',tic,i)
   priorities.append({'tic':tic,'peak_index':i,'best':p['best'],'followup':follow[key]})
old={r['tic'] for r in json.loads(Path('results/selection-small-stars-20261009/eligible.json').read_text())}
qlp={r['tic'] for r in json.loads(Path('results/selection-qlp-only-20261010/selected.json').read_text())}
assert not(expected&old or expected&qlp or old&qlp)
q=json.loads(Path('results/audit-qlp-expanded-20261010/final-audit.json').read_text())
save_json(out/'audit.json',{'utc':now(),'run_sources':run_sources,'selection_sha256':sha(sel),'n_expected':len(expected),'n_completed':len(rows),'dispositions':dict(counts),'review_priorities':priorities,'records':records,'disjointness_verified':True,'combined_scope':{'original_selected':len(old),'late_selected':len(expected),'qlp_selected':len(qlp),'total_unique_selected':len(old|expected|qlp),'usable_if_original_11851_audit_holds':len(old)+sum(r['status']=='screened' for r in rows.values())+q['n_usable']},'limitations':'Short-period, brightness/radius/crowding-selected sample; not all TESS targets or a calibrated completeness survey. QLP fallback scopes differ. See original audit for original usable counts.'})
print(dict(counts),'reviewed',[(x['tic'],x['peak_index']) for x in priorities])
