from pathlib import Path
import json,hashlib,numpy as np
from scipy.linalg import lstsq
from astropy.io import fits
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=json.loads((O/'plan-v2.json').read_text());r=json.loads((O/'results.json').read_text());checks=[]
assert sha(O/'run-v2.py')==p['script_sha256']
for name,h in p['inputs'].items():assert sha(name)==h
fig,axes=plt.subplots(4,3,figsize=(10,12),constrained_layout=True)
for i,(c,row) in enumerate(zip(p['cases'],r['rows'])):
 z=np.load(O/f"{c['tic']}-s{c['sector']}.npz");b=c['clock']
 with fits.open(c['pixel']) as hd:
  d=hd[1].data;t=np.array(d['TIME'],float);f=np.array(d['FLUX'],float);e=np.array(d['FLUX_ERR'],float);q=d['QUALITY'];pt=np.c_[d['POS_CORR1'],d['POS_CORR2']].astype(float)
 finite=np.isfinite(t);event=np.zeros(len(t),int);event[finite]=np.rint((t[finite]-b['transit_time'])/b['period']).astype(int);dt=t-(b['transit_time']+event*b['period']);good=finite&(q==0);out=good&np.isfinite(pt).all(1)&np.isfinite(f).all((1,2))&(abs(dt)>max(.5,3*b['duration']));np.testing.assert_array_equal(out,z['outside'])
 blocks=np.floor((t-np.nanmin(t))/2);tr=out&(blocks%2==0);te=out&(blocks%2==1);flat=f.reshape(len(t),-1);mu=pt[tr].mean(0);sd=pt[tr].std(0);X=np.c_[np.ones(len(t)),(pt-mu)/sd];coef=lstsq(X[tr],flat[tr],lapack_driver='gelsy')[0];ratio=np.linalg.norm(flat[te]-X[te]@coef)/np.linalg.norm(flat[te]-flat[tr].mean(0));np.testing.assert_allclose(ratio,row['heldout_rms_ratio'],rtol=1e-10)
 mu=pt[out].mean(0);sd=pt[out].std(0);X=np.c_[np.ones(len(t)),(pt-mu)/sd];coef=lstsq(X[out],flat[out],lapack_driver='gelsy')[0];np.testing.assert_allclose(coef,z['coeff'],rtol=1e-8,atol=1e-7);corrected=(flat-X[:,1:]@coef[1:]).reshape(f.shape)
 maps=[[],[]];vars=[];events=[]
 for n in np.unique(event[good&(abs(dt)<b['duration']/2)]):
  ins=good&(event==n)&(abs(dt)<b['duration']/2);outs=good&(event==n)&(abs(dt)>b['duration'])&(abs(dt)<3*b['duration'])
  if ins.sum()<2 or outs.sum()<5:continue
  for j,a in enumerate([f,corrected]):maps[j].append(np.nanmean(a[outs],0)-np.nanmean(a[ins],0))
  vars.append(np.nansum(e[outs]**2,0)/outs.sum()**2+np.nansum(e[ins]**2,0)/ins.sum()**2);events.append(int(n))
 assert events==row['events'];w=1/np.asarray(vars);noise=np.sqrt(1/w.sum(0));np.testing.assert_allclose(noise,z['error']);ims=[(w*np.asarray(v)).sum(0)/w.sum(0) for v in maps]
 for a,k in zip(ims,['raw','corrected']):np.testing.assert_allclose(a,z[k],rtol=1e-7,atol=1e-6)
 templates=np.load(c['templates']);yy,xx=np.indices(noise.shape,dtype=float)
 for a,rows in zip(ims,[row['before'],row['after']]):
  for h in rows:
   cols=np.array([templates['template_'+h['tic']],np.ones_like(xx),xx-xx.mean(),yy-yy.mean()]);valid=np.isfinite(a)&np.isfinite(noise)&(noise>0)&np.isfinite(cols).all(0);design=cols[:,valid].T/noise[valid,None];data=a[valid]/noise[valid];coef=lstsq(design,data,lapack_driver='gelsy')[0];chi=np.sum((data-design@coef)**2);np.testing.assert_allclose([coef[0],chi],[h['amplitude'],h['chi2']],rtol=1e-8,atol=1e-6)
 expected=row['expected_host'];before=next(h for h in row['before'] if h['tic']==expected);after=next(h for h in row['after'] if h['tic']==expected);gaps=[min(h['chi2'] for h in hs if h['tic']!=expected)-next(h['chi2'] for h in hs if h['tic']==expected) for hs in [row['before'],row['after']]];np.testing.assert_allclose(gaps,[row['before_gap'],row['after_gap']]);fraction=abs(after['amplitude']/before['amplitude']-1);assert row['passed']==bool(ratio<1 and row['after'][0]['tic']==expected and gaps[1]>gaps[0] and fraction<=.2)
 for ax,a,title in zip(axes[i],[ims[0],ims[1],ims[1]-ims[0]],['Uncorrected','Corrected','Correction change']):
  im=ax.imshow(a,origin='lower',cmap='coolwarm');fig.colorbar(im,ax=ax,shrink=.75);ax.set_title(f"{c['tic']} s{c['sector']}: {title}",fontsize=9)
 checks.append(dict(tic=c['tic'],sector=c['sector'],events=len(events),fits=len(row['before'])*2,passed=row['passed'],integrated_stamp_flux_before=float(ims[0].sum()),integrated_stamp_flux_after=float(ims[1].sum())))
assert r['all_passed']==all(x['passed'] for x in checks)
fig.savefig(O/'controls.png',dpi=125)
(O/'verification.json').write_text(json.dumps(dict(verified=True,input_hashes=len(p['inputs']),method='Independent QR regression and fixed-template fits; nearest-cycle event masks and weighted image arithmetic; identical frozen gates.',cases=checks),indent=2))
print(json.dumps(checks,indent=2))
