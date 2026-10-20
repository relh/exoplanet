from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import save_json
p=Path(__file__).parent;r=json.loads((p/'results.json').read_text())['rows'];summary=json.loads((p/'summary.json').read_text())['methods'];n=0

def check(values,s):
 global n
 values=[v for v in values if v];e=np.array([v['scatter_scaled_error'] for v in values]);y=np.array([v['depth'] for v in values]);Q,R=np.linalg.qr(np.ones((len(y),1))/e[:,None]);coef=np.linalg.solve(R,Q.T@(y/e));error=abs(1/R[0,0]);assert abs(coef[0]-s['depth'])<1e-12 and abs(error-s['error'])<1e-12;n+=1
for s in summary:
 a=[q for q in r if q['kind']==s['kind'] and q['degree']==s['degree'] and q['outer']==s['outer'] and q['measurement']['status']=='measured']
 for kind in ['depth','left_annulus','right_annulus']:check([q['measurement'][kind] for q in a],s[kind])
 for j,w in enumerate(s['widths']):check([q['measurement']['widths'][j]['measurement'] for q in a],w)
 for v in s['leave_one_event_out']:check([q['measurement']['depth'] for q in a if [q['sector'],q['event']]!=v['omitted']],v)
save_json(p/'summary-verification.json',dict(status='passed',aggregates=n,method='Independent QR constant model across event estimates using reported scatter-scaled errors'));print('PASS',n)
