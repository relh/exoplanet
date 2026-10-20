"""Full-screen injection probes in real training data; never opens validation data.

A small, deliberately quiet sample is not survey completeness. Baseline peaks
are retained so coincident pre-existing signals are not credited as recoveries.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import shutil
import numpy as np
from .campaign import process_target
from .pipeline import read_curve, save_json, sha, now
from .search import flatten


def integrated_box(t, period, epoch, duration, exposure):
    # Exact box/exposure overlap, valid for duration + exposure < period.
    if duration<=0 or exposure<=0 or duration+exposure>=period:
        raise ValueError('Invalid transit/exposure geometry')
    phase=(t-epoch+period/2)%period-period/2
    left=np.maximum(phase-exposure/2,-duration/2)
    right=np.minimum(phase+exposure/2,duration/2)
    return np.clip((right-left)/exposure,0,1)


def audit(row, root, output):
    tic=row['tic'];target=row['target'];curves=[]
    for sector in target['training_sectors']:
        path=root/'lightcurves'/f's{sector:04d}-{tic}.fits'
        t,f,e,star=read_curve(path)
        source=json.loads(path.with_suffix('.fits.json').read_text())
        curves.append((sector,t,f,e,star,source))
    result={'tic':tic,'probes':[],'baseline_peaks':row['peaks']}
    for period in [1.37,4.73,13.13]:
        for duration in [.04,.12]:
            for depth in [.00025,.00075]:
                epoch=min(c[1][0] for c in curves)+.317*period
                probe={'period':period,'duration':duration,'depth':depth,'epoch':float(epoch)}
                def loader(_target,_root,window=1.5):
                    clean=[];evidence=[]
                    for sector,t,f,e,star,source in curves:
                        exposure=float(np.median(np.diff(t)))
                        attenuation=1-depth*integrated_box(t,period,epoch,duration,exposure)
                        part=flatten(t,f*attenuation,e*attenuation,window=window)
                        clean.append(part)
                        evidence.append({'sector':sector,'source':source,'star':star,
                            'injection':probe,'exposure_days':exposure,'n_clean_points':len(part[0])})
                    tt,yy,ee=(np.concatenate([p[k] for p in clean]) for k in range(3))
                    order=np.argsort(tt)
                    return tt[order],yy[order],ee[order],evidence
                destination=output/str(tic)/f'p{period}-d{duration}-z{depth}'
                (destination/'targets').mkdir(parents=True,exist_ok=False)
                r=process_target({**target,'injection':probe},root,destination,loader=loader)
                baseline_match=any(abs(p['period']/period-1)<.005 and p['depth_snr']>=7 for p in row['peaks'])
                matching=[p for p in r.get('screened_peaks',[]) if abs(p['best']['period']/period-1)<.005]
                result['probes'].append({**probe,'status':r['status'],'error':r.get('error'),
                    'baseline_period_match':baseline_match,'recovered_top3':bool(matching),
                    'recovered_full_screen':any(not p['flags'] for p in matching),
                    'creditable_recovery':any(not p['flags'] for p in matching) and not baseline_match,
                    'matching_flags':[p['flags'] for p in matching],
                    'evidence_path':str(destination/'targets'/f'{tic}.json')})
                save_json(output/str(tic)/'summary.json',result)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--campaign',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--limit',type=int,default=8);p.add_argument('--workers',type=int,default=2)
    a=p.parse_args()
    if not 1<=a.limit<=40 or not 1<=a.workers<=4:p.error('limit 1..40, workers 1..4')
    parent=json.loads((a.campaign/'run.json').read_text())
    if parent['status']!='complete':p.error('Select only from a completed campaign')
    rows=[json.loads(f.read_text()) for f in (a.campaign/'targets').glob('*.json')]
    rows=sorted([r for r in rows if r['status']=='screened'],key=lambda r:(r['median_scatter_floor_ppm'],r['tic']))[:a.limit]
    a.output.mkdir(parents=True,exist_ok=False);(a.output/'source').mkdir()
    for f in Path(__file__).parent.glob('*.py'):shutil.copyfile(f,a.output/'source'/f.name)
    for f in ['uv.lock','pyproject.toml']:shutil.copyfile(f,a.output/'source'/f)
    run={'status':'running','started_utc':now(),'tics':[r['tic'] for r in rows],
        'campaign_sha256':sha(a.campaign/'run.json'),'source_sha256':{f.name:sha(f) for f in (a.output/'source').iterdir()},
        'selection':'Eight quietest completed batch targets by measured median scatter, or requested limit',
        'limitations':'Selected quiet subset, one phase per period; box injections, exact exposure overlap using median cadence. Not completeness or false-positive calibration. Original astrophysical variability remains.'}
    save_json(a.output/'run.json',run);results=[]
    with ThreadPoolExecutor(a.workers) as pool:
        futures=[pool.submit(audit,r,Path('data'),a.output) for r in rows]
        for future in as_completed(futures):
            results.append(future.result());save_json(a.output/'results.json',results)
    probes=[p for r in results for p in r['probes']]
    run.update(status='complete',finished_utc=now(),n_probes=len(probes),
        n_errors=sum(p['status']=='error' for p in probes),
        recovered_top3=sum(p['recovered_top3'] for p in probes),
        recovered_full_screen=sum(p['recovered_full_screen'] for p in probes),
        creditable_recoveries=sum(p['creditable_recovery'] for p in probes))
    save_json(a.output/'run.json',run);print(json.dumps(run),flush=True)

if __name__=='__main__':main()
