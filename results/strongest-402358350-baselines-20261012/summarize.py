from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import save_json
p=Path(__file__).parent;d=json.loads((p/'results.json').read_text());out=[]
def aggregate(values):
 a=[v for v in values if v is not None];w=1/np.array([v['scatter_scaled_error'] for v in a])**2;y=np.array([v['depth'] for v in a]);mu=np.average(y,weights=w);return dict(n=len(a),depth=float(mu),error=float(np.sqrt(1/w.sum())),heterogeneity_chi2=float(np.sum(w*(y-mu)**2)))
for kind in ['SAP','PDCSAP']:
 for degree in [0,1,2]:
  for outer in [3,5]:
   rows=[r for r in d['rows'] if r['kind']==kind and r['degree']==degree and r['outer']==outer and r['measurement']['status']=='measured'];controls=[(r,c) for r in rows for c in r['controls'] if c['matched']];out.append(dict(kind=kind,degree=degree,outer=outer,events=[[r['sector'],r['event']] for r in rows],depth=aggregate([r['measurement']['depth'] for r in rows]),left_annulus=aggregate([r['measurement']['left_annulus'] for r in rows]),right_annulus=aggregate([r['measurement']['right_annulus'] for r in rows]),widths=[dict(width_multiple=v,**aggregate([r['measurement']['widths'][j]['measurement'] for r in rows])) for j,v in enumerate([.5,.75,1,1.25,1.5,2])],leave_one_event_out=[dict(omitted=[r['sector'],r['event']],**aggregate([q['measurement']['depth'] for q in rows if q['key']!=r['key']])) for r in rows],matched_controls=len(controls),controls_at_least_event_depth=sum(c['measurement']['depth']['depth']>=r['measurement']['depth']['depth'] for r,c in controls)))
save_json(p/'summary.json',dict(methods=out,limits='Inverse scatter-scaled-variance averages; event baselines independent byassumption. Methods/streamscontrols correlated; noFAP or probability.'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axs=plt.subplots(2,4,figsize=(14,7),constrained_layout=True)
for ax,(s,n) in zip(axs.flat,out[0]['events']):
 for kind,color in [('SAP','tab:orange'),('PDCSAP','tab:blue')]:
  # Degree1 radius3 is a presentation example; every matrix result saved.
  row=next(r for r in d['rows'] if r['sector']==s and r['event']==n and r['kind']==kind and r['degree']==1 and r['outer']==3);a=np.load(p/f"{row['key']}.npz");res=(a['y']-a['X']@row['measurement']['coefficients'])*1e6;edges=np.linspace(-2,2,25);xx=[];yy=[];ee=[]
  for lo,hi in zip(edges[:-1],edges[1:]):
   m=(a['x']>=lo)&(a['x']<hi)
   if m.any():w=1/a['e'][m]**2;xx.append((lo+hi)/2);yy.append(np.average(res[m],weights=w));ee.append(np.sqrt(1/w.sum())*1e6)
  ax.errorbar(xx,yy,yerr=ee,fmt='.',color=color,label=kind)
 ax.axvspan(-.5,.5,color='gray',alpha=.15);ax.axhline(0,color='gray',lw=.5);ax.set(title=f'S{s} event{n}',xlabel='Time offset / fixed duration',ylabel='Residual flux, ppm')
axs[0,0].legend();fig.savefig(p/'event-shapes.png',dpi=120)
fig,axs=plt.subplots(1,2,figsize=(12,4),constrained_layout=True)
for i,kind in enumerate(['SAP','PDCSAP']):
 for q in out:
  if q['kind']!=kind:continue
  axs[i].errorbar([r['width_multiple'] for r in q['widths']],[r['depth']*1e6 for r in q['widths']],yerr=[r['error']*1e6 for r in q['widths']],fmt='.-',label=f'degree{q["degree"]}, radius{q["outer"]}D')
 axs[i].set(title=kind,xlabel='Averaging width / fixed duration',ylabel='Combined dimming, ppm');axs[i].legend(fontsize=8)
fig.savefig(p/'width-matrix.png',dpi=130)
print([(q['kind'],q['degree'],q['outer'],q['matched_controls'],q['controls_at_least_event_depth']) for q in out])
