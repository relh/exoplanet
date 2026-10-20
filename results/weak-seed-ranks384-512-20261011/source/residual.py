"""Exploratory secondary-signal searches by masking dominant discovery features.

Masking is not a classification of the removed signal. Original searches stay
intact. Extra rounds introduce additional trials and can remove real transits.
https://lightkurve.github.io/lightkurve/tutorials/3-science-examples/exoplanets-identifying-transiting-planet-signals.html
"""
import argparse,json,shutil
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from .campaign import load_training,process_target
from .qlp_campaign import load_qlp
from .model_audit import reconstruct
from .search import keep_outside_signals
from .pipeline import save_json,sha,now


def search_one(index,path,output,rounds):
    original=json.loads(path.read_text());target=original['target']
    summary={'index':index,'tic':original['tic'],'source_path':str(path),'source_sha256':sha(path),'rounds':[]}
    if target.get('masked_signals'):raise ValueError('Start from an unmasked discovery')
    injection=target.get('injection')
    def loader(selected,root,window=1.5):
        if not injection:
            reader=load_qlp if target.get('qlp_products') else load_training
            return reader(selected,root,window=window)
        t,y,dy=reconstruct(original,window=window)
        keep=keep_outside_signals(t,selected.get('masked_signals',[]))
        # Original per-sector counts no longer apply after masking or a changed
        # detrending window; keep provenance and stellar metadata, not stale counts.
        evidence=[{k:v for k,v in d.items() if k in ['sector','source','star','injection']} for d in original['data']]
        for d in evidence:d['masked_signals']=selected.get('masked_signals',[])
        return t[keep],y[keep],dy[keep],evidence
    t,_,_,_=loader(target,Path('data'));signals=[];current=original
    for step in range(1,rounds+1):
        best=current['best']
        if best['depth_snr']<8:summary['stop_reason']='No dominant peak above S/N 8';break
        signal={k:best[k] for k in ['period','transit_time','duration']};signal['halfwidth_days']=best['duration']
        proposed=signals+[signal];keep=keep_outside_signals(t,proposed)
        removed_fraction=1-keep.mean()
        if removed_fraction>.2 or keep.sum()<200:
            summary['stop_reason']='Mask would remove >20% of original data or leave <200 points';break
        if keep_outside_signals(t,signals).sum()-keep.sum()<2:
            summary['stop_reason']='Mask adds fewer than two removed points';break
        signals=proposed;destination=output/f'case-{index:04d}'/f'round-{step}'
        (destination/'targets').mkdir(parents=True,exist_ok=False)
        selected={**target,'masked_signals':signals,'residual_source_sha256':sha(path)}
        result=process_target(selected,Path('data'),destination,loader=loader,
                              max_baseline=120 if target.get('qlp_products') else 100)
        entry={'round':step,'masked_signals':signals,'removed_fraction':float(removed_fraction),
               'status':result['status'],'result_path':str(destination/'targets'/f'{original["tic"]}.json')}
        if result['status']=='error':entry['error']=result['error']
        elif injection:
            matches=[q for q in result['screened_peaks'] if abs(q['best']['period']/injection['period']-1)<.005]
            entry.update(matching_period=bool(matches),matching_pass=any(not q['flags'] for q in matches),
                         matching_flags=[q['flags'] for q in matches])
        else:entry['review_priority']=result['disposition']=='followup_priority'
        summary['rounds'].append(entry);save_json(output/f'case-{index:04d}'/'summary.json',summary)
        if result['status']=='error':break
        current=result
    return summary


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--selection',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--rounds',type=int,default=2);p.add_argument('--workers',type=int,default=2)
    a=p.parse_args()
    if not 1<=a.rounds<=3 or not 1<=a.workers<=4:p.error('rounds 1..3, workers 1..4')
    paths=[Path(s) for s in json.loads(a.selection.read_text())]
    if not 1<=len(paths)<=300:p.error('Select 1..300 saved discoveries')
    a.output.mkdir(parents=True,exist_ok=False);(a.output/'source').mkdir()
    for f in Path(__file__).parent.glob('*.py'):shutil.copyfile(f,a.output/'source'/f.name)
    for name in ['uv.lock','pyproject.toml']:shutil.copyfile(name,a.output/'source'/name)
    run={'status':'running','started_utc':now(),'selection_path':str(a.selection),'selection_sha256':sha(a.selection),
         'source_sha256':{f.name:sha(f) for f in (a.output/'source').iterdir()},'n_cases':len(paths),'rounds':a.rounds,
         'mask_halfwidth':'One fitted duration (total masked width twice duration)','max_cumulative_mask_fraction':.2,
         'limitations':__doc__,'holdout_policy':'Only original training data used'}
    save_json(a.output/'run.json',run);results=[]
    with ThreadPoolExecutor(a.workers) as pool:
        futures=[pool.submit(search_one,i,path,a.output,a.rounds) for i,path in enumerate(paths)]
        for future in as_completed(futures):
            results.append(future.result());save_json(a.output/'results.json',results)
    run.update(status='complete',finished_utc=now(),n_errors=sum(any(z['status']=='error' for z in r['rounds']) for r in results))
    save_json(a.output/'run.json',run)

if __name__=='__main__':main()
