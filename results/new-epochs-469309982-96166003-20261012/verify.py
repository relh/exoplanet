from pathlib import Path
import json,importlib.util,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
from exoplanet.search import flatten
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent;D=Path('data/new-epochs-469309982-96166003-20261012')
h=Path('results/expanded-96166003-20261012/verify.py');sp=importlib.util.spec_from_file_location('independent',h);ind=importlib.util.module_from_spec(sp);sp.loader.exec_module(ind)
p=json.loads((O/'plan.json').read_text());r=json.loads((O/'results.json').read_text());s=json.loads((O/'execution.json').read_text());assert s['status']=='complete' and s['results_sha256']==sha(O/'results.json');assert s['plan_sha256']==r['plan_sha256']==sha(O/'plan.json');assert p['script_sha256']==sha(O/'run.py')
for path,hs in {**p['input_sha256'],**p['source_sha256']}.items():assert sha(Path(path))==hs
assert len(r['rows'])==10
checks=[];fig,axes=plt.subplots(10,2,figsize=(11,24),constrained_layout=True)
for i,row in enumerate(r['rows']):
 case=next(c for c in p['cases'] if c['tic']==row['tic']);prior=next(c for c in case['clocks'] if c['name']==row['clock_name'] and c['window']==row['window']);assert row['clock']==prior['best'] and row['ranges']==prior['ranges'];b=row['clock'];source=row['data'][0]['source'];path=D/'qlp'/f"{row['tic']}-s{row['sector']:04d}.fits";assert sha(path)==source['sha256'];assert p['created_utc']<=s['started_utc']<=source['retrieved_utc']<=row['scored_utc']<=s['finished_utc'];assert case['product']['dataURL'] in source['url']
 with fits.open(path) as hd:
  assert hd[0].header['TICID']==row['tic'] and hd[0].header['SECTOR']==row['sector'];assert hd[1].header.get('BJDREFI',hd[0].header.get('BJDREFI'))==2457000;d=hd[1].data;assert row['data'][0]['flux_column']=='DET_FLUX';t=np.array(d['TIME'],float);y=np.array(d['DET_FLUX'],float);e=np.array(d['DET_FLUX_ERR'],float);keep=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(y)&(y>0)&np.isfinite(e)&(e>0);order=np.argsort(t[keep]);t,y,e=flatten(t[keep][order],y[keep][order],e[keep][order],window=row['window'])
 z=np.load(O/f"{row['tic']}-w{row['window']}.npz")
 for v,k in zip([t,y,e],['time','flux','error']):np.testing.assert_array_equal(v,z[k])
 ind.measured(t,y,e,b,row['measurement']);ranges=row['ranges'];spread=ind.spread(t,b,ranges) if ranges else None;precise=bool(ranges and spread<b['duration']/2 and not ranges['search_boundary_hit'] and prior['training_supported_events']>=3);assert precise==row['timing_precise'];assert (spread is None)==(row['timing_spread_days'] is None)
 if spread is not None:np.testing.assert_allclose(spread,row['timing_spread_days'])
 m=row['measurement'];total=m['total'];expected=b['depth']/total['error'] if total else None
 if expected is not None:np.testing.assert_allclose(expected,row['expected_formal_snr'])
 conclusion='insufficient_coverage' if total is None else 'timing_prediction_inconclusive' if not precise else 'recovered_at_frozen_ephemeris_requires_further_vetting' if total['snr']>=5 and m['supported_events']>=2 else 'not_recovered_despite_expected_sensitivity' if expected>=5 and total['snr']<2 else 'insufficient_evidence';assert conclusion==row['conclusion'];checks.append(dict(tic=row['tic'],clock=row['clock_name'],window=row['window'],n_events=len(m['events']),outcome=conclusion))
 phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;edges=np.linspace(-min(.45*b['period'],3*b['duration']),min(.45*b['period'],3*b['duration']),31);xs=[];ys=[];es=[]
 for a,c in zip(edges[:-1],edges[1:]):
  k=(phase>=a)&(phase<c)
  if k.sum():w=1/e[k]**2;xs.append((a+c)/2);ys.append((np.dot(w,y[k])/w.sum()-1)*1e6);es.append(1e6/np.sqrt(w.sum()))
 ax=axes[i,0];ax.errorbar(xs,ys,yerr=es,fmt='.',ms=3);ax.axvspan(-b['duration']/2,b['duration']/2,alpha=.15,color='gray');ax.axhline(0,color='gray',lw=.5);ax.set_title(f"{row['tic']} {row['clock_name']} w{row['window']}",fontsize=8);ax.set_ylabel('Flux ppm');ax=axes[i,1];ax.errorbar([v['center_btjd'] for v in m['events']],[v['depth']*1e6 for v in m['events']],yerr=[v['error']*1e6 for v in m['events']],fmt='.');ax.axhline(0,color='gray',lw=.5);ax.set_ylabel('Event depth ppm')
fig.savefig(O/'fixed-clocks.png',dpi=110);plt.close(fig)
save_json(O/'verification.json',dict(status='passed',created_utc=now(),helper_sha256=sha(h),checks=checks,scope='Raw identity,hash,quality and column reconstruction; shared flatten reproduced; independent precision-sum total/event and timing arithmetic; unchanged clocks/decision rules and plan-before-retrieval chronology. Does not independently implement detrending or calibrate correlated errors.'));print(checks)
