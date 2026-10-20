"""Bounded time-averaging sensitivity on archived masked-baseline fits."""
from pathlib import Path
import json, hashlib
import numpy as np
P=Path(__file__).parent
BASE=Path('results/strongest-402358350-baselines-20261012')
def beta_details(x,resid,outside):
    cadence=float(np.median(np.diff(x)))
    ids=np.flatnonzero(outside)
    splits=np.flatnonzero((np.diff(ids)>1)|(np.diff(x[ids])>1.5*cadence))+1
    segments=np.split(ids,splits)
    sigma=float(np.std(resid[outside]))
    trials=[]
    for duration in [.25,.5,1.]:
        n=max(2,int(round(duration/cadence)))
        for offset in sorted(set([0,n//2])):
            chunks=[s[j:j+n] for s in segments for j in range(offset,len(s)-n+1,n)]
            means=np.array([np.mean(resid[c]) for c in chunks]);m=len(means)
            row=dict(duration=duration,n=n,offset=offset,m=m,status='insufficient_bins',means=means.tolist(),chunks=[c.tolist() for c in chunks])
            if m>=4 and sigma>0:
                expected=sigma/np.sqrt(n)*np.sqrt(m/(m-1))
                row.update(status='measured',expected=float(expected),std_binned=float(np.std(means)),beta=float(np.std(means)/expected))
            trials.append(row)
    return dict(beta=max([1.]+[r['beta'] for r in trials if r['status']=='measured']),sigma=sigma,cadence=cadence,segments=[s.tolist() for s in segments],trials=trials)
def main():
    plan=json.loads((P/'plan.json').read_text())
    for file,h in plan['inputs'].items():assert hashlib.sha256(Path(file).read_bytes()).hexdigest()==h
    rows=[]
    for old in json.loads((BASE/'results.json').read_text())['rows']:
        r={k:old[k] for k in ['key','sector','kind','event','degree','outer']};r['status']=old['measurement']['status']
        if r['status']=='measured':
            a=np.load(BASE/(r['key']+'.npz'));x,y,e,X,o,inside=[a[k] for k in ['x','y','e','X','outside','inside']]
            coef=np.linalg.lstsq(X[o]/e[o,None],y[o]/e[o],rcond=None)[0];resid=y-X@coef
            depth=-np.average(resid[inside],weights=1/e[inside]**2)
            assert abs(depth-old['measurement']['depth']['depth'])<1e-12
            diag=beta_details(x,resid,o)
            error=old['measurement']['depth']['scatter_scaled_error']
            r.update(depth=float(depth),original_error=error,inflated_error=error*diag['beta'],diagnostic=diag)
        rows.append(r)
    summary=[]
    for kind in ['SAP','PDCSAP']:
      for deg in [0,1,2]:
       for outer in [3,5]:
        rr=[r for r in rows if r['kind']==kind and r['degree']==deg and r['outer']==outer and r['status']=='measured']
        d,e,ei=np.array([[r['depth'],r['original_error'],r['inflated_error']] for r in rr]).T;w=1/e**2;wi=1/ei**2
        summary.append(dict(kind=kind,degree=deg,outer=outer,n=len(rr),depth=float(np.average(d,weights=w)),original_error=float(1/np.sqrt(w.sum())),inflated_error_fixed_weights=float(np.sqrt(np.sum(w*w*ei*ei))/w.sum()),reweighted_depth=float(np.average(d,weights=wi)),reweighted_error=float(1/np.sqrt(wi.sum())),beta_min=min(r['diagnostic']['beta'] for r in rr),beta_max=max(r['diagnostic']['beta'] for r in rr)))
    result=dict(plan_sha256=hashlib.sha256((P/'plan.json').read_bytes()).hexdigest(),rows=rows,summary=summary)
    (P/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    for r in summary:print(r['kind'],r['degree'],r['outer'],round(r['depth']*1e6),round(r['inflated_error_fixed_weights']*1e6),round(r['beta_max'],2))
if __name__=='__main__':main()
