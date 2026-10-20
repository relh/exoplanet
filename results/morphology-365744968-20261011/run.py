from pathlib import Path
import json,numpy as np
from astropy.io import fits
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.qlp_campaign import load_qlp
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent
fp=Path('results/qlp-faint-midradius-remaining-one-followup-20261011/365744968-peak0/frozen.json')
dp=Path('results/qlp-faint-midradius-remaining-one-20261011/targets/365744968.json')
b=json.loads(fp.read_text())['best'];target=json.loads(dp.read_text())['target'];period=b['period'];epoch=b['transit_time'];sectors=[6,32,98]
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'script_sha256':sha(Path(__file__)),'inputs':{str(p):sha(p) for p in [fp,dp]},'sources':{str(p):sha(p) for p in Path('src/exoplanet').glob('*.py')},'raw':{f'data/qlp/365744968-s{s:04d}.fits':sha(Path(f'data/qlp/365744968-s{s:04d}.fits')) for s in sectors},'sectors':sectors,'period':period,'epoch':epoch,'policy':'Posthoc visualization of already opened sectors. Fixed original clock, no phase or period fit. Compare quality-zero positive SAP and pipeline-selected flux normalized by sector median with unchanged native QLP loader at1.5/3day flatten windows. Fold medians require at least3points/bin. No formal detection, rotation inference or blind validation.'})
rows=[]
for s in sectors:
 curves=[]
 with fits.open(f'data/qlp/365744968-s{s:04d}.fits') as hd:
  d=hd[1].data
  for col in ['SAP_FLUX','DET_FLUX' if 'DET_FLUX' in d.names else 'KSPSAP_FLUX']:
   t=np.array(d['TIME'],float);y=np.array(d[col],float);k=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(y)&(y>0);t=t[k];y=y[k];y=y/np.median(y);curves.append((col,t,y))
 for w in [1.5,3.0]:
  t,y,e,evidence=load_qlp(dict(target,training_sectors=[s]),Path('data'),window=w,bin_minutes=0);curves.append((f'flatten{w}d',t,y))
 fig,axs=plt.subplots(4,2,figsize=(13,12),constrained_layout=True);stats=[]
 for i,(label,t,y) in enumerate(curves):
  ph=((t-epoch)/period+.5)%1-.5
  axs[i,0].scatter(t,y,s=2,alpha=.35);axs[i,0].set_xlabel('BTJD');axs[i,0].set_title(f'S{s} {label}')
  axs[i,1].scatter(ph,y,s=2,alpha=.25)
  bins=np.linspace(-.5,.5,81);xx=[];yy=[]
  for lo,hi in zip(bins[:-1],bins[1:]):
   k=(ph>=lo)&(ph<hi)
   if k.sum()>=3:xx.append((lo+hi)/2);yy.append(float(np.median(y[k])))
  axs[i,1].plot(xx,yy,c='red');axs[i,1].axvspan(-b['duration']/period/2,b['duration']/period/2,alpha=.15,color='orange');axs[i,1].set_xlabel('Fixed phase');axs[i,1].set_title(f'P={period:.8f}d; original epoch')
  stats.append({'label':label,'n':len(t),'percentiles_1_50_99':np.percentile(y,[1,50,99]).tolist(),'phase_centers':xx,'phase_medians':yy})
 p=out/f'sector-{s}.png';fig.savefig(p,dpi=130);plt.close(fig);rows.append({'sector':s,'curves':stats,'plot':str(p),'plot_sha256':sha(p)})
save_json(out/'results.json',{'rows':rows,'limits':'Timing uncertainty smears older folds; differences between detrendings are not independent observations. Activity and blending remain possible.'})
print('Saved three morphology panels.')
