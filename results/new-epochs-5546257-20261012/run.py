from pathlib import Path
import json,numpy as np,traceback
from astropy.io import fits
from exoplanet.pipeline import save_json,sha,now,fetch
from exoplanet.integrity import verify_hdus
from exoplanet.archive import qlp_flux_columns
from exoplanet.qlp_campaign import empirical_errors
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure,prediction_spread
p=Path(__file__).parent;root=Path('data/new-epochs-5546257-20261012');plan=json.loads((p/'plan.json').read_text());rows=[];products=[]
for product in plan['products']:
 s=int(product['sequence_number']);item=dict(sector=s,started_utc=now(),status='error');path=root/f'5546257-s{s:04d}.fits'
 try:
  source=fetch('https://mast.stsci.edu/api/v0.1/Download/file/?uri='+product['dataURL'],path);item['source']=source
  with fits.open(path) as h:
   integrity=verify_hdus(path,h);assert h[0].header['TICID']==5546257 and h[0].header['SECTOR']==s;assert h[1].header.get('BJDREFI',h[0].header.get('BJDREFI'))==2457000;assert h[1].header.get('TIMESYS',h[0].header.get('TIMESYS'))=='TDB';d=h[1].data;save_json(p/f'headers-s{s}.json',dict(hdus=[dict(index=i,cards=[dict(key=c.keyword,value=str(c.value),comment=c.comment) for c in x.header.cards]) for i,x in enumerate(h)],columns=[dict(name=c.name,format=c.format,unit=c.unit) for c in h[1].columns]));fluxcol,errorcol,_=qlp_flux_columns(d.names);t=np.array(d['TIME'],float);y=np.array(d[fluxcol],float);e=np.array(d[errorcol],float);quality=np.array(d['QUALITY']);usable=(quality==0)&np.isfinite(t)&np.isfinite(y)&(y>0);valid=np.isfinite(e)&(e>0);errmodel=dict(kind='published',n_valid_pairs=int(np.sum(usable&valid)))
   if not np.any(usable&valid):
    sigma,errmodel=empirical_errors(t[usable],y[usable]);e[usable]=sigma
   keep=usable&np.isfinite(e)&(e>0);t,y,e=t[keep],y[keep],e[keep];ix=np.argsort(t);t,y,e=t[ix],y[ix],e[ix];assert np.all(np.diff(t)>0);item.update(flux_column=fluxcol,error_column=errorcol,error_model=errmodel,integrity=integrity,n_input=len(t),span=[float(min(t)),float(max(t))])
  for w in plan['windows']:
   tt,yy,ee=flatten(t,y,e,window=w);np.savez_compressed(p/f's{s}-w{w}.npz',t=tt,y=yy,e=ee)
   for c in plan['clocks']:
    b=c['best'];m=fixed_measure(tt,yy,ee,b['period'],b['transit_time'],b['duration']);spread=prediction_spread(tt,b,c['ranges']) if c['ranges'] else None;precise=spread is not None and spread<b['duration']/2 and not c['ranges']['search_boundary_hit'] and plan['training_supported_events']>=3;total=m['total'];expected=b['depth']/total['error'] if total else None;controls=[]
    for shift in np.arange(1,50)*b['period']/50:
     if min(shift,b['period']-shift)<2*b['duration']:continue
     q=fixed_measure(tt,yy,ee,b['period'],b['transit_time']+shift,b['duration'])['total'];controls.append(dict(shift=float(shift),measurement=q))
    conclusion='timing_prediction_inconclusive'
    if precise:
     if total is None:conclusion='insufficient_coverage'
     elif total['snr']>=5 and m['supported_events']>=2:conclusion='recovered_at_frozen_ephemeris_requires_further_vetting'
     elif expected>=5 and total['snr']<2:conclusion='not_recovered_despite_expected_sensitivity'
     else:conclusion='insufficient_evidence'
    rows.append(dict(sector=s,window=w,clock=c['name'],n_clean=len(tt),measurement=m,spread_days=spread,precise=precise,expected_formal_snr=expected,controls=controls,conclusion=conclusion))
  item['status']='measured'
 except Exception as exc:item.update(error=repr(exc),traceback=traceback.format_exc())
 products.append(item);save_json(p/'results.json',dict(created_utc=now(),plan_sha256=sha(p/'plan.json'),products=products,rows=rows));print('sector',s,item['status'],item.get('error'),flush=True)
print([(r['sector'],r['window'],r['clock'],r['measurement']['total'],r['spread_days']) for r in rows])
