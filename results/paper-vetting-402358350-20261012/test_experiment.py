"""Deterministic synthetic behavior, independent of astronomical interpretation."""
import numpy as np
import importlib.util
from pathlib import Path
_spec = importlib.util.spec_from_file_location("paper_noise_402358350", Path(__file__).with_name("run.py"))
_method = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_method)
beta_details = _method.beta_details

def test_white_vs_correlated_noise():
 rng=np.random.default_rng(402358350);x=np.arange(20000)*.01;o=np.ones(len(x),bool);white=rng.normal(size=len(x));red=np.empty(len(x));red[0]=white[0]
 for j in range(1,len(x)):red[j]=.9*red[j-1]+np.sqrt(1-.9**2)*white[j]
 bw=beta_details(x,white,o)['beta'];br=beta_details(x,red,o)['beta']
 assert .9<=bw<=1.2
 assert br>3 and br>3*bw

def test_gaps_and_mask_split():
 x=np.r_[np.arange(100)*.01,2+np.arange(100)*.01];o=np.ones(200,bool);o[40:60]=False;r=np.sin(x*30);d=beta_details(x,r,o)
 assert len(d['segments'])==3
 for t in d['trials']:
  for c in t['chunks']:assert np.all(o[c]) and np.max(np.diff(x[c]))<.015

def test_signed_injection_and_refit():
 rng=np.random.default_rng(1402);x=np.arange(-5,5,.01);X=np.c_[np.ones(len(x)),x];e=np.ones(len(x))*.0005;o=abs(x)>1;i=abs(x)<.5;y=1+.0001*x+rng.normal(0,.0005,len(x))
 def measure(flux):
  coeff=np.linalg.lstsq(X[o]/e[o,None],flux[o]/e[o],rcond=None)[0];res=flux-X@coeff
  return -np.mean(res[i]),beta_details(x,res,o)['beta']
 d,b=measure(y)
 for amplitude in [-.0006,.0006]:
  yi=y-amplitude*i;di,bi=measure(yi);assert abs(di-d-amplitude)<1e-12;assert abs(bi-b)<1e-12
