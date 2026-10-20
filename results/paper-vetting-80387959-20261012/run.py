from pathlib import Path
import json,hashlib,numpy as np
O=Path(__file__).parent;plan=json.loads((O/'plan.json').read_text());SEED=plan['seed'];D=plan['duration_days']
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def split(t,c):
 cad=np.median(np.diff(t)[np.diff(c)==0]);cuts=np.flatnonzero((np.diff(c)!=0)|(np.diff(t)>1.5*cad))+1
 return np.split(np.arange(len(t)),cuts),cad

def maps(t,c):
 seg,cad=split(t,c);out=[]
 for width in plan['widths_duration']:
  n=max(2,int(round(width*D/cad)))
  for offset in plan['offset_fractions']:
   bins=[s[j:j+n] for s in seg for j in range(int(offset*n),len(s)-n+1,n)]
   out.append((dict(width_duration=width,offset=offset,n_per_bin=n,n_bins=len(bins),actual_minutes=n*cad*1440),bins))
 return out

def fit(X,y,e):
 A=X/e[:,None];L=np.linalg.pinv(A)/e[None,:];b=L@y;res=y-X@b;scale=max(1,float(np.sqrt(np.sum((res/e)**2)/(len(y)-X.shape[1]))));err=float(np.sqrt(np.sum((L[-1]*e)**2))*scale)
 return b,res,err,L,scale

def audit(t,c,X,y,e,seed):
 b,res,err,L,scale=fit(X,y,e);rng=np.random.default_rng(seed);white=rng.normal(size=(len(y),plan['white_simulations']))*e[:,None]*scale;wr=white-X@(L@white);out=[]
 for info,bins in maps(t,c):
  if len(bins)<plan['min_bins']:out.append(dict(**info,status='insufficient_bins'));continue
  means=np.array([res[i].mean() for i in bins]);wm=np.array([wr[i].mean(axis=0) for i in bins]);obs=np.sqrt(np.mean(means**2));ref=np.sqrt(np.mean(wm**2));out.append(dict(**info,status='ok',rms_ppm=float(obs*1e6),white_reference_ppm=float(ref*1e6),beta=float(obs/ref)))
 beta=max([1]+[v['beta'] for v in out if v['status']=='ok']);return dict(depth_ppm=float(b[-1]*1e6),white_error_ppm=err*1e6,beta=beta,adjusted_error_ppm=err*beta*1e6,conditional_depth_error_ratio=float(b[-1]/(err*beta)),n=len(y),events=np.unique(c).tolist(),scales=out,error_scale=scale)

def main():
 rows=[]
 for inp in plan['inputs']:
  assert sha(inp['path'])==inp['sha256'];z=np.load(inp['path']);sector=int(Path(inp['path']).name.split('-')[0][1:]);t,c,X,y,e=[z[k] for k in ['t','cycles','X','y','e']];row=dict(sector=sector,full=audit(t,c,X,y,e,SEED+sector),omissions=[])
  for ev in np.unique(c):
   m=c!=ev;cols=np.any(X[m]!=0,axis=0);a=audit(t[m],c[m],X[m][:,cols],y[m],e[m],SEED+sector+int(ev)+10000);row['omissions'].append(dict(omitted_event=int(ev),**a))
  rows.append(row);print(sector,row['full']['depth_ppm'],row['full']['beta'],row['full']['adjusted_error_ppm'],flush=True)
 (O/'results.json').write_text(json.dumps(dict(plan_sha256=sha(O/'plan.json'),rows=rows),indent=2))
if __name__=='__main__':main()
