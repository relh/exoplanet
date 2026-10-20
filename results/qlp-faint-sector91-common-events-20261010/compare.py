"""Post-selection timing comparison; descriptive, not calibrated false-alarm test."""
from pathlib import Path
import json,itertools
import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;rows=[];stars={};inputs={}
for tic in [386739254,347752079,25964510,98718764,110976002]:
 kind='pilot' if tic==386739254 else 'expanded'
 p=Path(f'results/qlp-faint-sector91-{kind}-20261010/targets/{tic}.json');d=json.loads(p.read_text());stars[tic]=d['target']['star'];inputs[str(p)]=sha(p)
 for i in [0,1]:
  kind='pilot-coverage' if tic==386739254 else 'coverage'
  p=Path(f'results/qlp-faint-sector91-{kind}-followup-20261010/{tic}-peak{i}/frozen.json');f=json.loads(p.read_text());inputs[str(p)]=sha(p)
  events=f['training_measurement']['events'];assert len(events)==2
  centers=sorted(e['center_btjd'] for e in events);b=f['best']
  rows.append({'tic':tic,'peak':i,'period':b['period'],'duration':b['duration'],'centers':centers,'training_measurement':f['training_measurement']})
separations=[]
for a,b in itertools.combinations(stars,2):
 x,y=stars[a],stars[b];sep=SkyCoord(x['ra']*u.deg,x['dec']*u.deg).separation(SkyCoord(y['ra']*u.deg,y['dec']*u.deg)).deg
 separations.append({'tic_a':a,'tic_b':b,'separation_degrees':float(sep)})
late=np.array([r['centers'][1] for r in rows]);left=max(r['centers'][1]-r['duration']/2 for r in rows);right=min(r['centers'][1]+r['duration']/2 for r in rows)
assert right>left
result={'utc':now(),'script_sha256':sha(Path(__file__)),'inputs':inputs,'rows':rows,'separations':separations,'late_center_span_days':float(np.ptp(late)),'late_center_span_minutes':float(np.ptp(late)*1440),'common_in_transit_interval_btjd':[left,right],'limits':'Post-selection comparison of all 10 eligible peaks (5 distinct stars); aliases on the same star are not independent. Every fit uses the same late event within 43 minutes, despite degree-scale separation. This suggests shared instrumental contamination; no calibrated false-alarm probability, exact physical cause, completeness or planet exclusion.'}
save_json(out/'comparison.json',result)
fig,axes=plt.subplots(1,2,figsize=(12,5),sharey=True,constrained_layout=True)
for j,r in enumerate(rows):
 for k,ax in enumerate(axes):
  x=r['centers'][k];ax.plot([x-r['duration']/2,x+r['duration']/2],[j,j],lw=3);ax.plot(x,j,'ko',ms=3)
axes[0].set_yticks(range(len(rows)),[f"{r['tic']} peak{r['peak']}" for r in rows]);axes[0].set_title('First supported event');axes[1].set_title('Second supported event: shared timing');axes[1].axvspan(left,right,alpha=.15,color='gray')
for ax in axes:ax.set_xlabel('BTJD (days)');ax.ticklabel_format(axis='x',useOffset=False)
fig.suptitle('Sector91: post-selection timing comparison (durations, not confidence intervals)');fig.savefig(out/'timing.png',dpi=140)
print('Late center span minutes:',result['late_center_span_minutes'],'separations:',min(s['separation_degrees'] for s in separations),max(s['separation_degrees'] for s in separations))
