"""Block-permutation controls for the maximum BLS statistic on training data.

Preserves flux/error pairs and short contiguous runs, destroys coherence across
blocks. Conditional diagnostic only: finite blocks disrupt long correlations,
introduce seams, and can retain parts of real signals. Not a survey-wide FAP.
"""
import argparse,json,shutil
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
import numpy as np
from .campaign import load_training,joint_scan
from .pipeline import save_json,sha,now


def block_permutation(t, block_days, rng):
    """Permute blocks within each gap-separated segment without replacing points."""
    permutation=np.arange(len(t))
    for segment in np.split(np.arange(len(t)),np.flatnonzero(np.diff(t)>.3)+1):
        if len(segment)<2:continue
        cadence=np.median(np.diff(t[segment]))
        n=max(2,int(round(block_days/cadence)))
        blocks=[segment[start:start+n] for start in range(0,len(segment),n)]
        permutation[segment]=np.concatenate([blocks[i] for i in rng.permutation(len(blocks))])
    return permutation


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--discovery',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--draws-per-length',type=int,default=16);p.add_argument('--workers',type=int,default=2)
    a=p.parse_args()
    if not 1<=a.draws_per_length<=1000 or not 1<=a.workers<=4:p.error('draws 1..1000, workers 1..4')
    r=json.loads(a.discovery.read_text());t,y,dy,evidence=load_training(r['target'],Path('data'))
    a.output.mkdir(parents=True,exist_ok=False);(a.output/'source').mkdir()
    for f in Path(__file__).parent.glob('*.py'):shutil.copyfile(f,a.output/'source'/f.name)
    observed=joint_scan(t,y,dy)[2]
    run={'status':'running','started_utc':now(),'tic':r['tic'],'discovery_sha256':sha(a.discovery),
        'observed':observed,'data':evidence,'block_lengths_days':[.5,1,2],
        'draws_per_length':a.draws_per_length,'seed':20261009,'source_sha256':{f.name:sha(f) for f in (a.output/'source').iterdir()},
        'limitations':__doc__,'holdout_policy':'Only original discovery training sectors opened'}
    save_json(a.output/'run.json',run)
    def probe(spec):
        length,draw=spec
        rng=np.random.default_rng(np.random.SeedSequence([20261009,r['tic'],int(length*10),draw]))
        ix=block_permutation(t,length,rng)
        best=joint_scan(t,y[ix],dy[ix])[2]
        return {'block_days':length,'draw':draw,'best':best,'exceeds_observed_power':best['power']>=observed['power']}
    results=[]
    with ThreadPoolExecutor(a.workers) as pool:
        futures=[pool.submit(probe,(length,draw)) for length in [.5,1,2] for draw in range(a.draws_per_length)]
        for future in as_completed(futures):
            results.append(future.result());save_json(a.output/'results.json',results)
    run.update(status='complete',finished_utc=now(),summary=[{'block_days':length,'n':a.draws_per_length,
        'exceedances':sum(z['exceeds_observed_power'] for z in results if z['block_days']==length)} for length in [.5,1,2]])
    save_json(a.output/'run.json',run);print(run['summary'],flush=True)

if __name__=='__main__':main()
