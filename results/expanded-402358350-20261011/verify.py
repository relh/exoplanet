"""Independent precision-sum measurements and grid reconstruction after execution."""
from pathlib import Path
import json
import numpy as np
from astropy.timeseries import BoxLeastSquares
from exoplanet.pipeline import sha,save_json,now,read_curve
from exoplanet.search import flatten
O=Path(__file__).parent

def rebuild(records,window):
 arrays=[]
 for r in records:
  p=Path(f"data/lightcurves/s{r['sector']:04d}-402358350.fits");assert sha(p)==r['source']['sha256'];t,y,e,m=read_curve(p);assert m['ticid']==402358350 and m['sector']==r['sector'];arrays.append(flatten(t,y,e,window=window))
 t,y,e=[np.concatenate([a[j] for a in arrays]) for j in range(3)];i=np.argsort(t);return t[i],y[i],e[i]
def measured(t,y,e,b,saved):
 ph=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;ev=np.rint((t-b['transit_time'])/b['period']).astype(int);a=abs(ph)<b['duration']/2;c=(abs(ph)>b['duration'])&(abs(ph)<min(3*b['duration'],b['period']/2))
 def depth(a,c):
  if a.sum()<2 or c.sum()<5:return None
  wa=1/e[a]**2;wc=1/e[c]**2;d=y[c]@wc/wc.sum()-y[a]@wa/wa.sum();err=np.sqrt(1/wa.sum()+1/wc.sum());return dict(depth=float(d),error=float(err),snr=float(d/err),n=int(a.sum()))
 def check(x,s):
  assert (x is None)==(s is None)
  if x:
   for k in x:np.testing.assert_allclose(x[k],s[k],atol=1e-10,rtol=1e-8)
 check(depth(a,c),saved['total']);events=[]
 for n in np.unique(ev[a]):
  d=depth(a&(ev==n),c&(ev==n))
  if d:events.append((int(n),d))
 assert len(events)==len(saved['events'])
 for (n,d),s in zip(events,saved['events']):assert n==s['event'];check(d,s)
 assert sum(d['snr']>=2 for n,d in events)==saved['supported_events']
def spread(t,b,r):
 cyc=np.rint((np.array([t.min(),t.max()])-b['transit_time'])/b['period']);offset=[]
 for p,ep in r['profile_timing_pairs']:
  ep+=round((b['transit_time']-ep)/p)*p;offset.extend(abs(ep-b['transit_time']+cyc*(p-b['period'])))
 return float(max(offset,default=0)+3*r['conditional_epoch_floor_days'])
def main():
 plan=json.loads((O/'plan.json').read_text());state=json.loads((O/'execution.json').read_text());assert state['status']=='complete';assert state['plan_sha256']==sha(O/'plan.json');assert plan['run_script_sha256']==sha(O/'run.py');assert sha(Path('results/solar-radius-ranks4944-5456-20261011/verification.json'))==state['terminal_audit_sha256'];priorpath=Path('results/timing-402358350-discovery-20261011/frozen.json');assert sha(priorpath)==plan['prior_frozen_sha256'];prior=json.loads(priorpath.read_text());disc=json.loads(Path('results/solar-radius-ranks4944-5456-20261011/targets/402358350.json').read_text());seed=disc['screened_peaks'][0]['best'];pred=json.loads((O/'sector54-original-predictions.json').read_text());expanded=json.loads((O/'frozen-for81.json').read_text());assert expanded['plan_sha256']==sha(O/'plan.json');assert expanded['original54_predictions_sha256']==sha(O/'sector54-original-predictions.json');assert state['frozen_for81_sha256']==sha(O/'frozen-for81.json');assert expanded['training_sectors']==[40,41,54] and expanded['reserved_sectors']==[81]
 checks=[]
 for row,old in zip(pred['rows'],prior['rows']):
  assert row['clock']==old['best'] and row['window']==old['window'];assert [r['sector'] for r in row['data']]==[54];raw=row['data'][0]['source'];assert state['terminal_verified_utc']<=state['started_utc']<=raw['retrieved_utc']<=row['scored_utc']<=expanded['frozen_utc'];t,y,e=rebuild(row['data'],row['window']);b=old['best'];measured(t,y,e,b,row['measurement']);measured(t,y,e,seed,row['original_discovery_clock_measurement']);s=spread(t,b,old['ranges']);np.testing.assert_allclose(s,row['timing_spread_days']);m=row['measurement'];total=m['total'];precise=s<b['duration']/2 and not old['ranges']['search_boundary_hit'] and old['measurement']['supported_events']>=3;expected=None if total is None else b['depth']/total['error'];result='insufficient_coverage' if total is None else 'timing_prediction_inconclusive' if not precise else 'recovered_at_frozen_ephemeris_requires_further_vetting' if total['snr']>=5 and m['supported_events']>=2 else 'not_recovered_despite_expected_sensitivity' if expected>=5 and total['snr']<2 else 'insufficient_evidence';assert result==row['conclusion'] and precise==row['timing_precise'];np.testing.assert_allclose(expected,row['expected_formal_snr']);np.savez_compressed(O/f"sector54-w{row['window']}.npz",t=t,y=y,e=e)
 for row in expanded['rows']:
  assert [r['sector'] for r in row['data']]==[40,41,54];t,y,e=rebuild(row['data'],row['window']);width=3*seed['duration']*seed['period']/disc['clean_baseline_days'];step=seed['duration']*seed['period']/(20*np.ptp(t));n=max(2049,int(np.ceil(2*width/step))+1);assert n<=50001;periods=np.linspace(max(.25,seed['period']-width),seed['period']+width,n);bls=BoxLeastSquares(t,y,e).power(periods,np.array([.8,1,1.2])*seed['duration'],objective='likelihood',oversample=50);idx=int(np.argmax(bls.power));best={k:float(bls[k][idx]) for k in row['best']};assert best==row['best'];good=bls.power>=bls.power[idx]-4.5;r=row['ranges'];np.testing.assert_array_equal(np.c_[bls.period[good],bls.transit_time[good]],r['profile_timing_pairs']);assert bool(good[0] or good[-1])==r['search_boundary_hit'];assert r['period_min']==float(bls.period[good].min()) and r['period_max']==float(bls.period[good].max());assert r['conditional_epoch_floor_days']==max(best['duration']/50,best['duration']/max(best['depth_snr'],1));measured(t,y,e,best,row['measurement']);np.savez_compressed(O/f"expanded-w{row['window']}.npz",t=t,y=y,e=e,profile_period=bls.period,profile_power=bls.power);checks.append(dict(window=row['window'],grid_points=n,profile_pairs=int(good.sum())))
 assert not Path('data/lightcurves/s0081-402358350.fits').exists();save_json(O/'verification.json',dict(status='passed',created_utc=now(),script_sha256=sha(Path(__file__)),checks=checks,sector81_cache_absent=True,scope='Raw hash/identity/preprocessing, four original54fixed measurements and two expanded measurement sets via independent precision sums, independently constructed Astropy grids/profiles, original54timing/conclusion rules, terminalaudit-before-download and predictions-before-expanded-freeze chronology. Same BLS implementation; no calibrated astrophysical significance.'));print(checks)
if __name__=='__main__':main()
