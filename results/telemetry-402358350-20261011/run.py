from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
O=Path(__file__).parent;FP=Path('results/expanded-402358350-20261011/frozen-for81.json');CHANNELS=['SAP_BKG','POS_CORR1','POS_CORR2','MOM_CENTR1','MOM_CENTR2'];SECTORS=[40,41,54,81]
def measure(dt,y,d):
 good=np.isfinite(dt)&np.isfinite(y);a=good&(abs(dt)<d/2);c=good&(abs(dt)>d)&(abs(dt)<3*d)
 if a.sum()<2 or c.sum()<5:return None
 design=np.c_[np.ones(len(dt)),dt];coef=np.linalg.lstsq(design[c],y[c],rcond=None)[0];res=y-design@coef;scatter=float(np.std(res[c],ddof=2));offset=float(np.mean(res[a]));return dict(n_in=int(a.sum()),n_out=int(c.sum()),offset=offset,scatter=scatter,ratio=offset/scatter if scatter>0 else None)
def main():
 assert not (O/'plan.json').exists();b=json.loads(FP.read_text())['rows'][0]['best'];paths=[Path(f'data/lightcurves/s{s:04d}-402358350.fits') for s in SECTORS];shifts=[-.5,-.4,-.3,-.2,.2,.3,.4,.5]
 save_json(O/'plan.json',dict(created_utc=now(),clock=b,channels=CHANNELS,sectors=SECTORS,control_shifts_periods=shifts,inputs={str(p):sha(p) for p in paths+[FP,Path(__file__)]},policy='Cached alreadyopened lightcurve telemetry only. Fixed expandedprimaryclock; no exclusions/refit. Local linear baseline D<|dt|<3D, mean inside|dt|<D/2. Quality0. Control centers shifted by specifiedperiodfractions, alltrueevent±D masks excluded. Match eachchannel in/outcounts within20percent of event counts; retain rejected controls. Ratios descriptive not significance; controls overlap and share instrumental variation. Constant channels are uninformative.'))
 events=[]
 for s,path in zip(SECTORS,paths):
  with fits.open(path,checksum=False) as h:
   d=h[1].data;all_t=np.asarray(d['TIME'],float);quality=np.asarray(d['QUALITY']);good=(quality==0)&np.isfinite(all_t);t=all_t[good];cycles=np.rint((t-b['transit_time'])/b['period']).astype(int);phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2
   for n in sorted(set(cycles)):
    center=b['transit_time']+n*b['period'];dt=t-center
    if (abs(dt)<b['duration']/2).sum()<2:continue
    qa=quality[np.isfinite(all_t)&(abs(all_t-center)<b['duration']/2)];values,counts=np.unique(qa,return_counts=True);row=dict(sector=s,event=int(n),center_btjd=center,raw_inside_quality_counts={str(int(v)):int(c) for v,c in zip(values,counts)},channels={})
    for key in CHANNELS:
     y=np.asarray(d[key][good],float);m=measure(dt,y,b['duration']);constant=bool(np.nanmax(y)==np.nanmin(y));controls=[]
     for shift in shifts:
      allowed=abs(phase)>=b['duration'];control=measure((t-center-shift*b['period'])[allowed],y[allowed],b['duration']);matched=bool(m is not None and control is not None and .8<=control['n_in']/m['n_in']<=1.2 and .8<=control['n_out']/m['n_out']<=1.2)
      controls.append(dict(shift=shift,measurement=control,matched_counts=matched))
     eligible=[c['measurement']['ratio'] for c in controls if c['matched_counts'] and c['measurement']['ratio'] is not None];rank=None if constant or m is None or m['ratio'] is None or not eligible else sum(abs(v)>=abs(m['ratio']) for v in eligible)
     row['channels'][key]=dict(measurement=m,constant_channel=constant,controls=controls,n_matched=len(eligible),n_control_abs_ratio_ge_event=rank)
    events.append(row)
 save_json(O/'results.json',dict(created_utc=now(),plan_sha256=sha(O/'plan.json'),events=events));print('events',len(events))
if __name__=='__main__':main()
