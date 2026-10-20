from pathlib import Path
import json
import numpy as np
from astropy.timeseries import BoxLeastSquares
from exoplanet.pipeline import sha,save_json,now,read_curve
from exoplanet.search import flatten
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());f=json.loads((O/'frozen.json').read_text());protocol=json.loads((O/'prospective-protocol.json').read_text());assert f['plan_sha256']==sha(O/'plan.json');assert protocol['frozen_sha256']==sha(O/'frozen.json');assert p['created_utc']<=f['frozen_utc']<=protocol['frozen_utc'];assert sha(Path(p['discovery_path']))==p['discovery_sha256']
for path,h in p['source_hashes'].items():assert sha(Path(path))==h
checks=[]
for row in f['rows']:
 arrays=[]
 for record in row['data']:
  path=Path(f"data/lightcurves/s{record['sector']:04d}-96166003.fits");assert sha(path)==record['source']['sha256'];t,y,e,meta=read_curve(path);assert meta['ticid']==96166003 and meta['sector']==record['sector'];arrays.append(flatten(t,y,e,window=row['window']))
 t,y,e=[np.concatenate([a[j] for a in arrays]) for j in range(3)];i=np.argsort(t);t,y,e=t[i],y[i],e[i];z=np.load(O/f"w{row['window']}.npz")
 for k,a in dict(t=t,y=y,e=e).items():np.testing.assert_array_equal(a,z[k])
 # Rebuild complete BLS grid without refine_training helper.
 seed=p['seed'];width=3*seed['duration']*seed['period']/p['original_baseline'];step=seed['duration']*seed['period']/(20*np.ptp(t));n=max(2049,int(np.ceil(2*width/step))+1);assert n==row['grid']['n_grid'];period=np.linspace(max(.25,seed['period']-width),seed['period']+width,n);dur=np.array([.8,1,1.2])*seed['duration'];b=BoxLeastSquares(t,y,e).power(period,dur,objective='likelihood',oversample=50);idx=int(np.argmax(b.power));best={k:float(b[k][idx]) for k in row['best']};assert best==row['best'];good=b.power>=b.power[idx]-4.5;ranges=row['ranges'];np.testing.assert_array_equal(np.c_[b.period[good],b.transit_time[good]],ranges['profile_timing_pairs']);assert bool(good[0] or good[-1])==ranges['search_boundary_hit'];assert float(b.period[good].min())==ranges['period_min'] and float(b.period[good].max())==ranges['period_max'];np.testing.assert_allclose(ranges['period_grid_spacing'],period[1]-period[0]);assert ranges['conditional_epoch_floor_days']==max(best['duration']/50,best['duration']/max(best['depth_snr'],1))
 for clock,m in [(best,row['measurement']),(seed,row['original_clock_measurement'])]:
  ph=(t-clock['transit_time']+clock['period']/2)%clock['period']-clock['period']/2;a=abs(ph)<clock['duration']/2;c=(abs(ph)>clock['duration'])&(abs(ph)<min(3*clock['duration'],clock['period']/2));ev=np.rint((t-clock['transit_time'])/clock['period']).astype(int)
  def check(a,c,s):
   wa=1/e[a]**2;wc=1/e[c]**2;d=y[c]@wc/wc.sum()-y[a]@wa/wa.sum();err=np.sqrt(1/wa.sum()+1/wc.sum());np.testing.assert_allclose([d,err,d/err],[s['depth'],s['error'],s['snr']],atol=1e-10,rtol=1e-8)
  check(a,c,m['total'])
  for event in m['events']:j=ev==event['event'];check(a&j,c&j,event)
  assert m['supported_events']==sum(event['snr']>=2 for event in m['events'])
 for forecast in row['illustrative_forecasts']:
  times=np.array([forecast['assumed_window_start'],forecast['assumed_window_end']]);epochs=np.rint((times-best['transit_time'])/best['period']);offset=[]
  for pp,ep in ranges['profile_timing_pairs']:
   ep+=round((best['transit_time']-ep)/pp)*pp;offset.extend(abs(ep-best['transit_time']+epochs*(pp-best['period'])))
  spread=max(offset,default=0)+3*ranges['conditional_epoch_floor_days'];np.testing.assert_allclose(spread,forecast['spread_days'])
 np.savez_compressed(O/f"w{row['window']}-profile.npz",period=b.period,power=b.power,epoch=b.transit_time,duration=b.duration)
 checks.append(dict(window=row['window'],grid_points=n,profile_pairs=int(good.sum()),raw_products=2))
for sector in [19,59]:assert not Path(f'data/lightcurves/s{sector:04d}-96166003.fits').exists()
save_json(O/'verification.json',dict(status='passed',created_utc=now(),script_sha256=sha(Path(__file__)),checks=checks,additional_cache_absent=[19,59],scope='Raw identities/hash/preprocessing, independently rebuilt grids and profile masks via same Astropy BLS, independent fixed-depth precision sums and timing propagation, frozen provenance/protocol chronology. No new observations, red-noise calibration, physical validation or planet probability.'))
print(checks)
