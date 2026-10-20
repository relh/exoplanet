"""Audit exposure-model event diagnostics against completed known injections."""
import argparse,json,shutil
from pathlib import Path
import numpy as np
from .pipeline import read_curve,save_json,sha,now
from .search import flatten
from .transit_model import fit_events,integrated_box


def reconstruct(row,window=1.5):
    injection=row['target']['injection'];parts=[]
    for sector in row['target']['training_sectors']:
        path=Path(f'data/lightcurves/s{sector:04d}-{row["tic"]}.fits')
        t,f,e,_=read_curve(path)
        attenuation=1-injection['depth']*integrated_box(t,injection['period'],injection['epoch'],injection['duration'],np.median(np.diff(t)))
        parts.append(flatten(t,f*attenuation,e*attenuation,window=window))
    return tuple(np.concatenate([p[k] for p in parts]) for k in range(3))


def revised_flags(flags,fit):
    result=[f for f in flags if f not in ['odd_even_mismatch','odd_even_unmeasurable','inconsistent_event_depths','event_consistency_unmeasurable']]
    if not fit['optimization_success'] or fit['boundary_hit'] or fit['best']['depth']<=0:
        result.append('exposure_model_fit_unreliable')
    if fit['odd_even_sigma'] is None:result.append('odd_even_unmeasurable')
    elif fit['odd_even_sigma']>3:result.append('odd_even_mismatch')
    ec=fit['event_consistency']
    if ec is None:result.append('event_consistency_unmeasurable')
    elif ec['conditional_chi2_sf']<.001:result.append('inconsistent_event_depths')
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--injections',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run=json.loads((a.injections/'run.json').read_text())
    if run['status']!='complete':p.error('Only audit completed injection runs')
    a.output.mkdir(parents=True,exist_ok=False);(a.output/'source').mkdir()
    for f in Path(__file__).parent.glob('*.py'):shutil.copyfile(f,a.output/'source'/f.name)
    meta={'status':'running','started_utc':now(),'injection_run_sha256':sha(a.injections/'run.json'),
          'source_sha256':{f.name:sha(f) for f in (a.output/'source').iterdir()},
          'note':'Compare two replacement diagnostics only; other flags retained. Fits use discovery seeds, never injection truth. Truth used solely for selecting a matching recovered peak.'}
    save_json(a.output/'run.json',meta);results=[]
    for row in json.loads((a.injections/'results.json').read_text()):
        for probe in row['probes']:
            path=Path(probe['evidence_path']);r=json.loads(path.read_text())
            matches=[q for q in r.get('screened_peaks',[]) if abs(q['best']['period']/probe['period']-1)<.005]
            if not matches:continue
            t,y,dy=reconstruct(r)
            for peak in matches:
                fit=fit_events(t,y,dy,peak['best'],beta=peak['extended_vetting']['noise']['beta'] or 1)
                flags=revised_flags(peak['flags'],fit)
                results.append({'tic':row['tic'],'injection':r['target']['injection'],'source_sha256':sha(path),
                    'old_flags':peak['flags'],'revised_flags':flags,'fit':fit})
                save_json(a.output/'results.json',results)
    meta.update(status='complete',finished_utc=now(),n_matches=len(results),
        original_passes=sum(not r['old_flags'] for r in results),revised_passes=sum(not r['revised_flags'] for r in results))
    save_json(a.output/'run.json',meta);print({k:meta[k] for k in ['n_matches','original_passes','revised_passes']},flush=True)

if __name__=='__main__':main()
