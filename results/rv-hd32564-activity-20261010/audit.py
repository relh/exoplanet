"""Retain all model choices, including failed wider-neighborhood predictions."""
from pathlib import Path
import json
import numpy as np
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;summary=[]
for root,fraction in [(out,.001),(Path('results/rv-hd32564-activity-wide-20261010'),.01)]:
 plan=json.loads((root/'plan.json').read_text());rows=json.loads((root/'results.json').read_text());assert len(rows)==32
 keys={(r['reduction'],r['features'],r['year']) for r in rows};assert len(keys)==32
 for row in rows:
  for label,model,seeds in [('full',row['full_training_model'],plan['periods'])]+[(str(c['omitted_period']),c['reduced_training_model'],[p for p in plan['periods'] if p!=c['omitted_period']]) for c in row['components']]:
   if abs(np.array(model['periods'])/np.array(seeds)-1).max()>fraction*1.0001:raise AssertionError('Out of bound fit')
 failures=[{'reduction':r['reduction'],'features':r['features'],'year':r['year'],**{k:c[k] for k in ['omitted_period','held_delta_chi2']}} for r in rows for c in r['components'] if c['held_delta_chi2']<=0]
 summary.append({'path':str(root/'results.json'),'sha256':sha(root/'results.json'),'fraction':fraction,'n_fits':len(rows),'n_component_checks':sum(len(r['components']) for r in rows),'nonpositive_checks':failures,'n_full_boundary_fits':sum(bool(np.any(abs(np.array(r['full_training_model']['periods'])/np.array(plan['periods'])-1)>=fraction*.99)) for r in rows)})
save_json(out/'audit.json',{'utc':now(),'experiments':summary,'interpretation':'Retrospective same-spectra linear activity sensitivity; no GP, activity error or lag model, no new discovery or validation.'})
print(summary)
