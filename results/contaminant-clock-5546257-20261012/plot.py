from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent;r=json.loads((p/'results.json').read_text());c=json.loads((p/'clock-comparison.json').read_text());b=json.loads((p/'plan.json').read_text())['clock'];fig,axes=plt.subplots(2,3,figsize=(15,8),constrained_layout=True)
for i,kind in enumerate(['SAP','PDCSAP']):
 row=next(x for x in r['rows'] if x['window']==2.5 and x['kind']==kind);z=np.load(p/f'{kind}-2.5.npz');t,y,e=z['t'],z['y'],z['e']
 for ax,period,epoch,title in [(axes[i,0],b['period'],b['transit_time'],'Candidate fixed clock'),(axes[i,1],c['gaia_period_tdb'],c['reference_btjd_tdb'],'Gaia catalog phase')]:
  phase=(t-epoch)/period%1;edges=np.linspace(0,1,101);means=[];err=[];cent=[]
  for left,right in zip(edges[:-1],edges[1:]):
   sel=(phase>=left)&(phase<right)
   if sel.sum():w=1/e[sel]**2;cent.append((left+right)/2);means.append((np.sum(y[sel]*w)/w.sum()-1)*1e6);err.append(1/np.sqrt(w.sum())*1e6)
  ax.errorbar(cent,means,yerr=err,fmt='.',ms=3);ax.set_title(kind+' '+title);ax.set_xlabel('Phase');ax.set_ylabel('Flux residual ppm')
 for lab,q in c['eclipses'].items():
  lo=q['phase']-q['duration']/q['period']/2;hi=q['phase']+q['duration']/q['period']/2;axes[i,1].axvspan(lo,hi,alpha=.12);axes[i,2].axhspan(lo,hi,alpha=.12)
 events=row['candidate_event_gaia_comparison'];cent=np.array([x['center'] for x in events]);phase=(cent-c['reference_btjd_tdb'])/c['gaia_period_tdb']%1;snr=np.array([x['snr'] for x in events]);axes[i,2].scatter(cent,phase,c=snr,cmap='coolwarm',vmin=-4,vmax=4,s=np.where(snr>=2,45,10));axes[i,2].set_title('Candidate predicted centers; large=SNR≥2');axes[i,2].set_xlabel('BTJD');axes[i,2].set_ylabel('Gaia orbital phase')
fig.suptitle('Already-opened photometry; fixed clocks;2.5-day detrending; nominal Gaia eclipse bands');fig.savefig(p/'clock-comparison.png',dpi=130)
