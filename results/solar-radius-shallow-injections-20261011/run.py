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
from exoplanet.campaign import process_target
from exoplanet.pipeline import read_curve, save_json, sha, now
from exoplanet.search import flatten


from exoplanet.transit_model import integrated_box


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
            for depth in [.0001,.0003]:
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


p=Path(__file__).parent
parent=Path('results/solar-radius-next512-20261011')
rows=[json.loads(f.read_text()) for f in (parent/'targets').glob('*.json')]
pool=sorted([r for r in rows if r.get('disposition')=='below_screen_threshold'],key=lambda r:(r['median_scatter_floor_ppm'],r['tic']))
indices=[len(pool)//4,len(pool)//2,3*len(pool)//4];selected=[pool[i] for i in indices]
run=dict(status='running',started_utc=now(),parent=str(parent),parent_sha256=sha(parent/'run.json'),pool_size=len(pool),indices=indices,tics=[r['tic'] for r in selected],depths=[.0001,.0003],selection='Noise-floor quartiles among below-threshold discovery targets, fixed before injection outcomes',script_sha256=sha(Path(__file__)),source_sha256={f.name:sha(f) for f in Path('src/exoplanet').glob('*.py')},limits='Three deliberately low-variability targets; one phase each; box models. Not population completeness or astrophysical validation.')
save_json(p/'run.json',run);save_json(p/'selected.json',selected)
with ThreadPoolExecutor(3) as pool:
 results=list(pool.map(lambda r:audit(r,Path('data'),p),selected))
save_json(p/'results.json',results)
probes=[q for r in results for q in r['probes']]
run.update(status='complete',finished_utc=now(),n_probes=len(probes),n_errors=sum(q['status']=='error' for q in probes),creditable_recoveries=sum(q['creditable_recovery'] for q in probes))
save_json(p/'run.json',run);print(run,flush=True)
