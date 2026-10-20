"""Nightly RV ingestion for reproducible exploratory campaigns."""
import csv
import numpy as np


def nightly(path,column='RV_mlc_nzp',error_column='e_RV_mlc_nzp',jitter=2.):
    rows=list(csv.DictReader(open(path)))
    values=[]
    for r in rows:
        t,y,e,flag=[float(r[k]) for k in ['BJD',column,error_column,'f_RV']]
        if flag==0 and np.all(np.isfinite([t,y,e])) and 0<e<100 and abs(y)<1e6:
            values.append((t,y,e))
    a=np.array(values)
    if not len(a):raise ValueError('No usable RVs')
    t,y,e=a.T;days=np.floor(t+.5);result=[]
    for day in np.unique(days):
        m=days==day;w=1/e[m]**2
        result.append([np.average(t[m],weights=w),np.average(y[m],weights=w),np.hypot(1/np.sqrt(w.sum()),jitter)])
    t,y,e=np.array(result).T
    return t,y,e,(t>=2457163).astype(int)
