from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import save_json,sha,now
from exoplanet.campaign import load_training
from exoplanet.followup import refine_training
from exoplanet.search import diagnostics,triage
from exoplanet.vetting import extended_vetting
p=Path(__file__).parent;rows=[]
for tic in []:
 source=Path(f'results/weak-seed-ranks384-512-20261011/targets/{tic}.json');r=json.loads(source.read_text());selection=r['selection'];windows=[];fig,axes=plt.subplots(2,2,figsize=(12,7),constrained_layout=True)
 for i,w in enumerate(r['windows']):
  t,y,e,_=load_training(selection['target'],Path('data'),window=w['window_days']);b=w['best']
  def inverse(t,y,e):return None,None,refine_training(t,y,e,selection['seed'],seed_baseline=selection['original_baseline_days'])[0]
  d=diagnostics(t,y,e,b,searcher=inverse);v=extended_vetting(t,y,e,b,d);flags=triage(b,d)+v['flags'];windows.append(dict(window_days=w['window_days'],diagnostics=d,extended=v,flags=flags))
  phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2
  for ax,lim in zip(axes[i],[b['period']/2,min(b['period']/2,3*b['duration'])]):
   ax.plot(phase*24,(y-1)*1e6,'.',ms=1,alpha=.1);edges=np.linspace(-lim,lim,61);xx=[];yy=[];ee=[]
   for left,right in zip(edges[:-1],edges[1:]):
    m=(phase>=left)&(phase<right)
    if m.any():xx.append((left+right)*12);yy.append(np.average(y[m]-1,weights=1/e[m]**2)*1e6);ee.append(1e6/np.sqrt(np.sum(1/e[m]**2)))
   ax.errorbar(xx,yy,yerr=ee,fmt='.-',color='black');ax.set(xlim=(-lim*24,lim*24),ylim=(-max(800,b['depth']*3e6),max(800,b['depth']*3e6)),xlabel='Hours from fitted dip',ylabel='Flux (ppm)',title=f'{w["window_days"]} d detrending')
 fig.suptitle(f'TIC{tic}: local seeded fit; reserved sectors unopened');fig.savefig(p/f'{tic}.png',dpi=120);plt.close(fig)
 for sector in selection['target']['heldout_sectors']:assert not Path(f'data/lightcurves/s{sector:04d}-{tic}.fits').exists()
 record=dict(tic=tic,source_path=str(source),source_sha256=sha(source),windows=windows);rows.append(record);print(tic,[(x['flags'],x['extended']['noise']['adjusted_snr']) for x in windows],flush=True)
save_json(p/'diagnostics.json',dict(created_utc=now(),rows=rows,limitations='Inverted search is restricted to the same seeded local interval, not global. Sinusoid scan uses existing diagnostic frequency range; formal ratios and noise corrections are heuristic. No full-domain rediscovery or independent validation.'))
