"""Review completed discovery records with exposure-model event diagnostics.

Immutable companion evidence. Does not replace the original period search or
claim a planet detection. Can snapshot completed targets from a running batch.
"""
import argparse,json,shutil
from pathlib import Path
from .campaign import load_training
from .transit_model import fit_events
from .model_audit import revised_flags
from .vetting import extended_vetting
from .pipeline import save_json,sha,now


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--campaign',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False);(a.output/'source').mkdir()
    for f in Path(__file__).parent.glob('*.py'):shutil.copyfile(f,a.output/'source'/f.name)
    paths=sorted((a.campaign/'targets').glob('*.json'))
    candidates=[];replaceable={'odd_even_mismatch','odd_even_unmeasurable','inconsistent_event_depths','event_consistency_unmeasurable','correlated_noise_unmeasurable'}
    for path in paths:
        r=json.loads(path.read_text())
        if r.get('status')!='screened':continue
        for i,q in enumerate(r.get('screened_peaks',[])):
            if set(q['flags'])<=replaceable:candidates.append((path,r,i))
    meta={'status':'running','started_utc':now(),'campaign':str(a.campaign),'n_completed_snapshot':len(paths),
        'n_selected_peaks':len(candidates),'selection':'All original flags replaceable by exposure or corrected short-bin diagnostics, including original passes',
        'discovery_sha256':{str(p):sha(p) for p,_,_ in candidates},
        'source_sha256':{f.name:sha(f) for f in (a.output/'source').iterdir()},
        'note':'Original source/status immutable. No additional periods or held-out data used. Review priorities are not planet candidates.'}
    save_json(a.output/'run.json',meta);results=[]
    for path,r,i in candidates:
        q=r['screened_peaks'][i];record={'tic':r['tic'],'peak_index':i,'source':str(path),'original_flags':q['flags'],'status':'error'}
        try:
            t,y,dy,_=load_training(r['target'],Path('data'))
            new=extended_vetting(t,y,dy,q['best'],q['diagnostics'])
            old=q.get('extended_vetting',{}).get('flags',[])
            flags=[f for f in q['flags'] if f not in old]+new['flags']
            fit=fit_events(t,y,dy,q['best'],beta=new['noise']['beta'] or 1)
            flags=revised_flags(flags,fit)
            record.update(status='measured',fit=fit,flags=flags,review_priority=not flags)
        except Exception as exc:record['error']=f'{type(exc).__name__}: {exc}'
        results.append(record);save_json(a.output/'results.json',results)
    meta.update(status='complete',finished_utc=now(),review_tics=sorted(set(r['tic'] for r in results if r.get('review_priority'))),n_errors=sum(r['status']=='error' for r in results))
    save_json(a.output/'run.json',meta);print(meta['review_tics'],flush=True)

if __name__=='__main__':main()
