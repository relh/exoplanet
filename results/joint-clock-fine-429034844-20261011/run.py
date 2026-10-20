from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import refine_training,fixed_measure
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;fp=Path('results/qlp-faint-midradius-remaining-one-followup-20261011/429034844-peak1/frozen.json');dp=Path('results/qlp-faint-midradius-remaining-one-20261011/targets/429034844.json');read=lambda p:json.loads(p.read_text());seed=dict(read(fp)['best']);coarse=Path('results/joint-clock-429034844-20261011/fit.json');seed['period']=read(coarse)['best']['period'];target=read(dp)['target'];sectors=[42,43,70]
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'script_sha256':sha(Path(__file__)),'inputs':{str(p):sha(p) for p in [fp,dp,coarse]},'source_hashes':{str(p):sha(p) for p in Path('src/exoplanet').glob('*.py')},'raw':{f'data/qlp/429034844-s{s:04d}.fits':sha(Path(f'data/qlp/429034844-s{s:04d}.fits')) for s in sectors},'sectors':sectors,'seed':seed,'policy':'Posthoc local refinement around retained coarse joint period; original duration seed retained so duration grid is unchanged. Width and spacing based on full joint baseline; local only, not a global cycle-count exclusion. Already opened sectors; no blind validation or new planet inference. Original heldout tests preserved.'})
curves=[];data=[]
for s in sectors:
 t,y,e,ev=load_qlp(dict(target,training_sectors=[s]),Path('data'),bin_minutes=0);curves.append((t,y,e));data.extend(ev)
t,y,e=[np.concatenate([c[i] for c in curves]) for i in range(3)]
best,ranges=refine_training(t,y,e,seed,seed_baseline=np.ptp(t));save_json(out/'fit.json',{'best':best,'ranges':ranges,'data':data})
fig,axes=plt.subplots(3,2,figsize=(12,10),constrained_layout=True);rows=[]
for j,(s,(t,y,e)) in enumerate(zip(sectors,curves)):
 p=best['period'];epoch=best['transit_time'];dur=best['duration'];phase=(t-epoch+p/2)%p-p/2;cycles=np.rint((t-epoch)/p).astype(int);longphase=((t-epoch)/(2*p)+.25)%1-.25
 axes[j,0].scatter(longphase,y,s=2,alpha=.3);axes[j,0].set_title(f'S{s}: joint doubled clock {2*p:.9f}d');axes[j,0].set_ylim(.94,1.025);axes[j,0].set_xlabel('Phase');row={'sector':s,'parities':[]}
 for parity,color in [(0,'tab:blue'),(1,'tab:orange')]:
  m=(cycles%2==parity)&(abs(phase)<.075);axes[j,1].scatter(phase[m],y[m],s=3,alpha=.3,color=color)
  bins=np.linspace(-.075,.075,51);x=[];v=[]
  for lo,hi in zip(bins[:-1],bins[1:]):
   k=m&(phase>=lo)&(phase<hi)
   if k.sum()>=3:x.append((lo+hi)/2);v.append(np.median(y[k]))
  axes[j,1].plot(x,v,color=color,label=f'Parity{parity}');row['parities'].append({'parity':parity,'measurement':fixed_measure(t,y,e,2*p,epoch+parity*p,dur)})
 axes[j,1].legend();axes[j,1].set_ylim(.94,1.025);axes[j,1].set_title(f'S{s}: alternating events');axes[j,1].set_xlabel('Days from joint center');rows.append(row)
fig.savefig(out/'folds.png',dpi=140);save_json(out/'results.json',{'rows':rows,'plot_sha256':sha(out/'folds.png'),'limits':'Selected joint fit; errors are formal and conditional, multiple cycle-count aliases may remain. Source and binary/planet nature unresolved.'});print(best,ranges['search_boundary_hit'])
