from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha,save_json
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import refine_training,fixed_measure
out=Path(__file__).parent;fp=Path('results/timing-425293543-20261011/fits.json');b=json.loads(fp.read_text())['joint']['best'];dp=Path('results/qlp-faint-midradius-remaining-two-20261011/targets/425293543.json');target=json.loads(dp.read_text())['target']
save_json(out/'plan.json',{'script_sha256':sha(Path(__file__)),'joint_fits_sha256':sha(fp),'discovery_sha256':sha(dp),'policy':'Exploratory parity-separated fits using existing refine_training. Assign nearest joint eclipse number, retain every quality/preprocessed point in each alternating cycle. Search around2P using full baseline, duration grid unchanged. Already-opened sectors53/54/80/81; no independent validation.'})
t,y,e,data=load_qlp(dict(target,training_sectors=[53,54,80,81]),Path('data'),bin_minutes=0)
cycle=np.rint((t-b['transit_time'])/b['period']).astype(int);rows=[]
for parity in (0,1):
 mask=cycle%2==parity;seed=dict(b,period=2*b['period'],transit_time=b['transit_time']+parity*b['period'])
 best,ranges=refine_training(t[mask],y[mask],e[mask],seed)
 rows.append({'parity':parity,'n_points':int(mask.sum()),'best':best,'ranges':ranges,'measurement':fixed_measure(t[mask],y[mask],e[mask],best['period'],best['transit_time'],best['duration'])});print(parity,best,flush=True)
fig,axes=plt.subplots(4,2,figsize=(12,12),constrained_layout=True);per_sector=[]
for i,s in enumerate((53,54,80,81)):
 tt,yy,ee,dd=load_qlp(dict(target,training_sectors=[s]),Path('data'),bin_minutes=0);cy=np.rint((tt-b['transit_time'])/b['period']).astype(int)
 for k,row in enumerate(rows):
  fit=row['best'];m=cy%2==k;ph=(tt[m]-fit['transit_time']+fit['period']/2)%fit['period']-fit['period']/2
  ax=axes[i,k];ax.scatter(ph,yy[m],s=3,alpha=.5);ax.set_xlim(-.15,.15);ax.set_ylim(.75,1.08);ax.set_title(f'S{s}, parity{k}');ax.set_xlabel('Days from separate fit center')
  per_sector.append({'sector':s,'parity':k,'measurement':fixed_measure(tt[m],yy[m],ee[m],fit['period'],fit['transit_time'],fit['duration'])})
fig.savefig(out/'comparison.png',dpi=140)
p0,p1=[v['best']['period'] for v in rows];e0,e1=[v['best']['transit_time'] for v in rows]
sep=(e1-e0)%p0
save_json(out/'results.json',{'data':data,'fits':rows,'per_sector':per_sector,'period_difference_seconds':(p1-p0)*86400,'reference_separation_days':sep,'reference_separation_fraction':sep/p0,'limits':'Separate box fits, not common physical binary model. Model/cadence/systematic errors omitted; parity and period hypothesis selected after opening data. No eccentricity, mass, planet or unique-host inference.'})
save_json(out/'manifest.json',{'script_sha256':sha(Path(__file__)),'results_sha256':sha(out/'results.json'),'plot_sha256':sha(out/'comparison.png')})
