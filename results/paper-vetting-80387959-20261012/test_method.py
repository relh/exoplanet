import numpy as np,json
from pathlib import Path
import importlib.util
from pathlib import Path
_spec = importlib.util.spec_from_file_location("paper_noise_80387959", Path(__file__).with_name("run.py"))
_method = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_method)
fit = _method.fit
maps = _method.maps
split = _method.split
O=Path(__file__).parent

def test_zero_and_signed_injection():
 errors=[]
 for inp in json.loads((O/'plan.json').read_text())['inputs']:
  z=np.load(inp['path']);X,e=z['X'],z['e'];base=np.arange(X.shape[1])*.00001;base[-1]=0
  for dep in [0,.001,-.001]:
   b=base.copy();b[-1]=dep;rec=fit(X,X@b,e)[0];err=float(abs(rec[-1]-dep));errors.append(err);assert err<1e-12
 (O/'injection-tests.json').write_text(json.dumps(dict(passed=True,count=len(errors),max_depth_error= max(errors)),indent=2))

def test_white_and_correlated_nulls():
 z=np.load('results/strongest-80387959-shape-20261012/s90-primary.npz');t,c,X,e=[z[k] for k in ['t','cycles','X','e']];rng=np.random.default_rng(270803);seg,_=split(t,c);L=np.linalg.pinv(X/e[:,None])/e[None,:];methods=maps(t,c);white_theory=[]
 for _,bins in methods:
  vari=[]
  for ix in bins:
   a=np.zeros(len(t));a[ix]=1/len(ix);q=a-(a@X)@L;vari.append(np.sum((q*e)**2))
  white_theory.append(np.sqrt(np.mean(vari)))
 stats=[]
 for phi in [0,.85]:
  noise=rng.normal(size=(len(t),200))
  for s in seg:
   for j in s[1:]:noise[j]=phi*noise[j-1]+np.sqrt(1-phi**2)*noise[j]
  noise*=e[:,None];b=L@noise;res=noise-X@b;betas=[]
  for (_,bins),ref in zip(methods,white_theory):betas.append(np.sqrt(np.mean(np.array([res[ix].mean(axis=0) for ix in bins])**2,axis=0))/ref)
  beta=np.maximum(1,np.max(betas,axis=0));stats.append(dict(phi=phi,replicates=200,median_beta=float(np.median(beta)),depth_scatter_ppm=float(np.std(b[-1],ddof=1)*1e6),mean_depth_ppm=float(np.mean(b[-1])*1e6)))
 assert .9<stats[0]['median_beta']<1.5
 assert stats[1]['median_beta']>1.5*stats[0]['median_beta']
 assert stats[1]['depth_scatter_ppm']>2*stats[0]['depth_scatter_ppm']
 (O/'synthetic-tests.json').write_text(json.dumps(dict(passed=True,scenarios=stats,scope='diagnostic response, not interval-coverage calibration'),indent=2))
