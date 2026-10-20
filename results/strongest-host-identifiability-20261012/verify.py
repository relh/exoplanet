from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());r=json.loads((O/'results.json').read_text());assert sha(O/'run.py')==p['script_sha256'];assert r['plan_sha256']==sha(O/'plan.json')
for name,h in p['inputs'].items():assert sha(Path(name))==h
checks=[];fig,axes=plt.subplots(4,2,figsize=(10,10),constrained_layout=True)
for i,c in enumerate(p['cases']):
 with fits.open(c['pixel']) as hd:
  d=hd[1].data;k=np.isfinite(d['TIME']);t=np.array(d['TIME'][k],float);f=np.array(d['FLUX'][k],float);e=np.array(d['FLUX_ERR'][k],float);q=d['QUALITY'][k]
 b=c['clock'];ev=np.rint((t-b['transit_time'])/b['period']).astype(int);phase=t-(b['transit_time']+ev*b['period']);good=q==0;ims=[];vs=[];numbers=[]
 for n in np.unique(ev[good&(abs(phase)<b['duration']/2)]):
  a=good&(ev==n)&(abs(phase)<b['duration']/2);o=good&(ev==n)&(abs(phase)>b['duration'])&(abs(phase)<3*b['duration'])
  if a.sum()<2 or o.sum()<5:continue
  ims.append(np.nanmean(f[o],0)-np.nanmean(f[a],0));vs.append(np.nansum(e[o]**2,0)/o.sum()**2+np.nansum(e[a]**2,0)/a.sum()**2);numbers.append(int(n))
 ims=np.array(ims);vs=np.array(vs);yy,xx=np.indices(f.shape[1:])
 for j,rad in enumerate(p['radii']):
  row=next(x for x in r['rows'] if x['tic']==c['tic'] and x['sector']==c['sector'] and x['radius']==rad);z=np.load(O/f"{c['tic']}-s{c['sector']}-r{rad}.npz");np.testing.assert_allclose(ims,z['difference']);np.testing.assert_allclose(vs,z['variance']);assert numbers==row['event_numbers'];masks=[(xx-a)**2+(yy-b)**2<=rad**2 for a,b in c['positions'].values()];a=masks[0]&~masks[1];o=masks[1]&~masks[0];w=a/a.sum()-o/o.sum();np.testing.assert_array_equal(w,z['weights']);assert abs(w.sum())<1e-14
  contrasts=np.array([im[a].mean()-im[o].mean() for im in ims]);variance=np.array([v[a].sum()/a.sum()**2+v[o].sum()/o.sum()**2 for v in vs]);np.testing.assert_allclose(contrasts,row['event_contrasts']);np.testing.assert_allclose(variance,row['event_variances']);precision=1/variance;mean=np.average(contrasts,weights=precision);err=precision.sum()**-.5;np.testing.assert_allclose([mean,err,mean/err],[row['contrast'],row['error'],row['snr']]);loo=[np.average(np.delete(contrasts,n),weights=np.delete(precision,n)) for n in range(len(contrasts))];np.testing.assert_allclose(loo,row['leave_one_out']);np.testing.assert_allclose(contrasts.std(ddof=1)/len(contrasts)**.5,row['empirical_event_scatter_error']);assert row['passed']==bool(mean>0 and mean/err>=3 and min(loo)>0)
  ax=axes[i,j];ax.errorbar(numbers,contrasts,yerr=np.sqrt(variance),fmt='.');ax.axhline(0,color='gray');ax.axhline(mean,color='red',label='weighted mean');ax.set_title(f"{c['tic']} s{c['sector']} r{rad}: SNR {mean/err:.2f}");ax.set_ylabel('Contrast flux per pixel');ax.set_xlabel('All event numbers');checks.append(dict(tic=c['tic'],sector=c['sector'],radius=rad,events=len(numbers),passed=row['passed']))
assert r['all_passed']==all(x['passed'] for x in checks);fig.savefig(O/'controls.png',dpi=120);save_json(O/'verification.json',dict(status='passed',created_utc=now(),checks=checks,scope='Rawhash and independent eventimages,exclusive masks,equal-area contrastvariances/precision sums,allLOO andpredeclared gates. NoPRF/pointingcorrection andnocandidateeventflux.'))
print(checks)
