"""Limited injection/recovery audit on real training photometry.

A few deterministic probes are not an occurrence-rate completeness calculation.
Injection is applied before detrending; later sectors are never accessed.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import numpy as np
from .campaign import joint_scan, distinct_peaks
from .pipeline import read_curve, save_json, now, sha
from .search import flatten


def test_target(row,root):
    tic=row['tic'];target=row['target']
    result={'tic':tic,'probes':[]}
    curves=[]
    for s in target['training_sectors']:
        t,f,e,_=read_curve(root/'lightcurves'/f's{s:04d}-{tic}.fits')
        curves.append((t,f,e))
    epoch=min(c[0].min() for c in curves)+1.234
    for depth in [.0005,.001]:
        period,duration=4.37,.08
        out=[]
        for t,f,e in curves:
            # Average a box over exposure time using midpoint quadrature.
            cadence=np.median(np.diff(t))
            offsets=(np.arange(15)+.5)/15-.5
            phase=(t[:,None]+offsets*cadence-epoch+period/2)%period-period/2
            attenuation=1-depth*np.mean(abs(phase)<duration/2,axis=1)
            out.append(flatten(t,f*attenuation,e*attenuation))
        t,y,dy=(np.concatenate([c[k] for c in out]) for k in range(3))
        _,power,best=joint_scan(t,y,dy)
        peaks=distinct_peaks(power)
        recovered=[p for p in peaks if abs(p['period']/period-1)<.005 and p['depth_snr']>=7]
        result['probes'].append({'period':period,'epoch':float(epoch),'duration':duration,
            'depth':depth,'recovered_top3':bool(recovered),'matching_peaks':recovered,'best':best})
    print(f'Injection TIC {tic}: {[p["recovered_top3"] for p in result["probes"]]}',flush=True)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--campaign',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--limit',type=int,default=20)
    p.add_argument('--workers',type=int,default=4)
    a=p.parse_args()
    rows=[json.loads(f.read_text()) for f in (a.campaign/'targets').glob('*.json')]
    rows=sorted([r for r in rows if r['status']=='screened'],key=lambda r:(r['median_scatter_floor_ppm'],r['tic']))[:a.limit]
    a.output.mkdir(parents=True,exist_ok=False)
    save_json(a.output/'run.json',{'started_utc':now(),'selection':'Lowest median scatter floor in currently completed discovery targets',
        'tics':[r['tic'] for r in rows],'source_sha256':{p.name:sha(p) for p in Path(__file__).parent.glob('*.py')},
        'limitations':'Only 4.37-day, 1.92-hour, 500/1000ppm probes on a quiet subset; not survey completeness. Existing astrophysical signals retained.'})
    results=[]
    with ThreadPoolExecutor(a.workers) as pool:
        for r in pool.map(lambda row:test_target(row,Path('data')),rows):
            results.append(r);save_json(a.output/'results.json',results)
    print(f'{sum(p["recovered_top3"] for r in results for p in r["probes"])}/{2*len(results)} probes recovered',flush=True)

if __name__=='__main__':
    main()
