from pathlib import Path
import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent;r=json.loads((O/'results.json').read_text())['rows'];p=json.loads((O/'plan.json').read_text());fig,axs=plt.subplots(2,2,figsize=(12,8),constrained_layout=True)
for a,tic in zip(axs,[80387959,241928959]):
 rows=[x for x in r if x['tic']==tic];ax=a[0]
 for i,x in enumerate(rows):
  c=x['coefficients_ppm'];e=x['bootstrap'][1]['coefficient_sd_ppm'];ax.errorbar(i,c[2],yerr=e[2],fmt='o',color='tab:blue' if x['column']=='SAP_FLUX' else 'tab:orange')
 ax.axhline(0,color='k',lw=.7);ax.set_xticks(range(len(rows)),[f"{x['sector']} {x['column'].replace('_FLUX','')} d{x['degree']}" for x in rows],rotation=70,fontsize=7);ax.set(ylabel='cos(4π phase), ppm; 1-day block SD',title=f'{tic}: baseline / reduction sensitivity')
 ax=a[1];seed=next(x['seed'] for x in p['targets'] if x['tic']==tic)
 for x in rows:
  if x['degree']!=2 or x['column']=='SAP_FLUX':continue
  z=np.load(O/(x['name']+'.npz'));ph=((z['t']-seed['transit_time'])/seed['period'])%1;y=(z['y']-z['X'][:,:-4]@z['beta'][:-4])*1e6;bins=np.floor(ph*24).astype(int);xs=[];ys=[];es=[]
  for key in np.unique(bins):
   v=y[bins==key];xs.append((key+.5)/24);ys.append(np.mean(v));es.append(np.std(v)/np.sqrt(len(v)))
  ax.errorbar(xs,ys,yerr=es,fmt='.',label=f'S{x["sector"]}',alpha=.7)
 ax.axhline(0,color='k',lw=.7);ax.legend();ax.set(xlabel='Frozen orbital phase',ylabel='Baseline-subtracted corrected flux, ppm',title='Display bin errors ignore correlations')
fig.savefig(O/'diagnostic.png',dpi=150)
