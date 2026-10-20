from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent;fp=Path('results/source-check-469309982-20261011/frozen.json');b=json.loads(fp.read_text())['best'];paths=[Path(f'data/lightcurves/s{s:04d}-469309982.fits') for s in [9,36]];channels=['SAP_BKG','POS_CORR1','POS_CORR2','MOM_CENTR1','MOM_CENTR2']
save_json(p/'plan.json',dict(created_utc=now(),inputs={str(q):sha(q) for q in paths+[fp,Path(__file__)]},channels=channels,policy='Unchanged discovery clock in previously examined sectors9/36; post-selection descriptive event centers; local linear trend fitted outside duration but within3durations, then mean residual inside half-duration. Descriptive diagnostics, not calibrated significance or localization.'))
def measure(dt,y,duration):
 good=np.isfinite(dt)&np.isfinite(y);inside=good&(abs(dt)<duration/2);outside=good&(abs(dt)>duration)&(abs(dt)<3*duration)
 if inside.sum()<2 or outside.sum()<5:return None
 a=np.column_stack([np.ones(len(dt)),dt]);coef=np.linalg.lstsq(a[outside],y[outside],rcond=None)[0];res=y-a@coef;scale=float(np.std(res[outside],ddof=2));offset=float(np.mean(res[inside]));return dict(n_in=int(inside.sum()),n_out=int(outside.sum()),offset=offset,outside_scatter=scale,offset_over_scatter=offset/scale if scale>0 else None,baseline=coef.tolist())
# Deterministic linear-trend/offset arithmetic check, separate from observations.
x=np.linspace(-.48,.48,97);y=3+2*x;y[abs(x)<.08]+=.125;assert abs(measure(x,y,.16)['offset']-.125)<1e-12
rows=[];fig,axes=plt.subplots(20,len(channels),figsize=(16,34),constrained_layout=True);plotrow=0
for sector,path in zip([9,36],paths):
 with fits.open(path) as h:
  data=h[1].data;good=(data['QUALITY']==0)&np.isfinite(data['TIME']);t=np.asarray(data['TIME'][good],float);cycles=np.rint((t-b['transit_time'])/b['period']).astype(int)
  for n in sorted(set(cycles)):
   center=b['transit_time']+n*b['period'];dt=t-center
   if (abs(dt)<b['duration']/2).sum()<2:continue
   row=dict(sector=sector,event=int(n),center_btjd=center,channels={})
   for j,name in enumerate(channels):
    values=np.asarray(data[name][good],float);m=measure(dt,values,b['duration']);row['channels'][name]=m
    if plotrow<20:
     mask=np.isfinite(values)&(abs(dt)<3*b['duration']);display=values-np.nanmedian(values[mask]);ax=axes[plotrow,j];ax.scatter(dt[mask]*24,display[mask],s=6);ax.axvspan(-b['duration']*12,b['duration']*12,alpha=.15);ax.set_title(f'E{n} {name}',fontsize=9);ax.set_xlabel('Hours')
   rows.append(row);plotrow+=1
save_json(p/'results.json',dict(events=rows,synthetic_linear_offset_check='passed'));fig.savefig(p/'telemetry.png',dpi=120);print([(r['event'],{k:None if v is None else round(v['offset_over_scatter'],2) if v['offset_over_scatter'] is not None else None for k,v in r['channels'].items()}) for r in rows])
