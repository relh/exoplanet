from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;fp=Path('results/qlp-faint-midradius-remaining-one-followup-20261011/377129640-peak2/frozen.json');dp=Path('results/qlp-faint-midradius-remaining-one-20261011/targets/377129640.json');read=lambda p:json.loads(p.read_text());b=read(fp)['best'];target=read(dp)['target'];period=b['period']/3;epoch=b['transit_time'];duration=b['duration'];sectors=[45,46,72]
assert not (out/'plan.json').exists()
assert all(Path(f'data/qlp/377129640-s{s:04d}.fits').exists() for s in sectors)
save_json(out/'plan.json',{'script_sha256':sha(Path(__file__)),'inputs':{str(p):sha(p) for p in [fp,dp]},'source_hashes':{p.name:sha(p) for p in Path('src/exoplanet').glob('*.py')},'short_period':period,'epoch':epoch,'duration':duration,'sectors':sectors,'policy':'Posthoc exact frozenP/3 and2P/3, epoch/duration unchanged. No period or phase optimization. Already-opened S45/46/72, not independent blind confirmation; original inconclusive predictions retained. NativeQLP unchanged preprocessing. Compare alternating event families using fixed2P and epochs separated byP. Formal depth errors and scatter diagnostics are not calibrated source/planet probabilities.'})
fig,axes=plt.subplots(3,2,figsize=(12,10),constrained_layout=True);rows=[]
for j,s in enumerate(sectors):
 t,y,e,data=load_qlp(dict(target,training_sectors=[s]),Path('data'),bin_minutes=0);ph=(t-epoch+period/2)%period-period/2;cycles=np.rint((t-epoch)/period).astype(int);long_phase=((t-epoch)/(2*period)+.25)%1-.25;row={'sector':s,'data':data,'short':fixed_measure(t,y,e,period,epoch,duration),'parities':[]}
 axes[j,0].scatter(long_phase,y,s=2,alpha=.35);axes[j,0].set_title(f'S{s}: fixed doubled clock {2*period:.8f}d');axes[j,0].set_xlabel('Phase (centers0 and0.5)');axes[j,0].set_ylim(.93,1.035)
 for parity,color in [(0,'tab:blue'),(1,'tab:orange')]:
  mask=(cycles%2==parity)&(abs(ph)<.12);axes[j,1].scatter(ph[mask],y[mask],s=3,alpha=.35,color=color,label=f'Parity{parity}')
  bins=np.linspace(-.12,.12,49);centers=[];medians=[]
  for lo,hi in zip(bins[:-1],bins[1:]):
   ix=mask&(ph>=lo)&(ph<hi)
   if ix.sum()>=3:centers.append((lo+hi)/2);medians.append(float(np.median(y[ix])))
  axes[j,1].plot(centers,medians,color=color,lw=1.5)
  row['parities'].append({'parity':parity,'measurement':fixed_measure(t,y,e,2*period,epoch+parity*period,duration)})
 axes[j,1].set_title(f'S{s}: alternating short-clock events');axes[j,1].set_xlabel('Days from fixed center');axes[j,1].set_ylim(.93,1.035);axes[j,1].legend()
 rows.append(row)
fig.savefig(out/'folds.png',dpi=140)
save_json(out/'results.json',{'rows':rows,'plot_sha256':sha(out/'folds.png'),'limits':'Posthoc alias/parity test with unchanged clock. Timing drift can bias fixed-window depth; aperture blending and correlated noise remain. Alternate events are not separate planets.'})
print([(r['sector'],[(x['parity'],x['measurement']['total'],x['measurement']['supported_events']) for x in r['parities']]) for r in rows])
