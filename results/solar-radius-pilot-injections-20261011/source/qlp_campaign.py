"""Search selected newer QLP sectors while preserving earlier unused validation."""
import argparse,json,shutil
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
import numpy as np
from astropy.io import fits
from .pipeline import fetch,save_json,sha,now
from .integrity import verify_hdus
from .search import flatten,keep_outside_signals
from .campaign import process_target,SETTINGS
from .archive import qlp_flux_columns


def empirical_errors(t,y):
    """Robust adjacent-difference scale for exploratory equal-weight searches.

    This estimates short-timescale scatter, not a calibrated red-noise error.
    """
    dt=np.diff(t);cadence=np.median(dt[dt>0])
    diff=np.diff(y)[(dt>0)&(dt<1.5*cadence)]
    if len(diff)<100:raise ValueError('Insufficient adjacent samples for empirical errors')
    sigma=1.4826*np.median(abs(diff-np.median(diff)))/np.sqrt(2)
    if not np.isfinite(sigma) or sigma<=0:raise ValueError('Invalid empirical noise estimate')
    return float(sigma),{'kind':'estimated_adjacent_difference_MAD','n_pairs':len(diff),
        'sigma_flux_units':float(sigma),'sigma_relative_ppm':float(sigma/np.median(y)*1e6),
        'caution':'Equal weights from robust point-to-point scatter; not published uncertainties or calibrated significance'}


def bin_curve(t,y,dy,width=10/1440):
    if len(t)==0:raise ValueError('No finite positive quality-zero QLP flux/error pairs')
    index=np.floor((t-t[0])/width).astype(int);unique,inverse=np.unique(index,return_inverse=True)
    weights=1/dy**2;sumw=np.bincount(inverse,weights=weights)
    return (np.bincount(inverse,weights=t*weights)/sumw,
            np.bincount(inverse,weights=y*weights)/sumw,np.sqrt(1/sumw))


def load_qlp(target,root,window=1.5,bin_minutes=10):
    if not np.isfinite(bin_minutes) or not 0<=bin_minutes<=30:
        raise ValueError('QLP bin width must be between 0 (native) and 30 minutes')
    parts=[];evidence=[]
    for sector in target['training_sectors']:
        obs=target['qlp_products'][str(sector)]
        path=root/'qlp'/f'{target["tic"]}-s{sector:04d}.fits'
        source=fetch('https://mast.stsci.edu/api/v0.1/Download/file/?uri='+obs['dataURL'],path)
        with fits.open(path) as hdus:
            integrity=verify_hdus(path,hdus);h=hdus[0].header;d=hdus[1].data
            if h['TICID']!=target['tic'] or h['SECTOR']!=sector:raise ValueError('QLP FITS identity mismatch')
            if hdus[1].header.get('BJDREFI',h.get('BJDREFI'))!=2457000:raise ValueError('QLP time reference')
            flux_col,error_col,_=qlp_flux_columns(d.names)
            t,y,dy=(np.array(d[k],dtype=float) for k in ['TIME',flux_col,error_col])
            usable=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(y)&(y>0)
            valid_errors=np.isfinite(dy)&(dy>0)
            error_model={'kind':'published','usable_error_pairs':int(np.sum(usable&valid_errors))}
            if not np.any(usable&valid_errors) and target.get('estimate_missing_errors'):
                idx=np.flatnonzero(usable);idx=idx[np.argsort(t[idx])]
                sigma,error_model=empirical_errors(t[idx],y[idx]);dy[usable]=sigma
            keep=usable&np.isfinite(dy)&(dy>0)
            t,y,dy=t[keep],y[keep],dy[keep];order=np.argsort(t);t,y,dy=t[order],y[order],dy[order]
            if np.any(np.diff(t)<=0):raise ValueError('Duplicate QLP time stamps')
            n_native=len(t)
            if bin_minutes>0:t,y,dy=bin_curve(t,y,dy,width=bin_minutes/1440)
            t,y,dy=flatten(t,y,dy,window=window)
            n_pre_mask=len(t)
            if target.get('masked_signals'):
                keep=keep_outside_signals(t,target['masked_signals'])
                t,y,dy=t[keep],y[keep],dy[keep]
            parts.append((t,y,dy))
            evidence.append({'sector':sector,'source':source,'n_native_quality_points':n_native,
                'n_clean_points':len(t),'bin_minutes':bin_minutes,'flux_column':flux_col,
                'n_pre_mask_clean_points':n_pre_mask,'masked_signals':target.get('masked_signals',[]),
                'error_model':error_model,
                'star':{'ticid':target['tic'],'sector':sector,'crowdsap':h.get('CROWDSAP'),
                    'fits_integrity':integrity,'collection':'QLP','radius':h.get('RADIUS'),
                    'crowding_note':'No measured aperture-crowding value if CROWDSAP absent'}})
    t,y,dy=(np.concatenate([c[k] for c in parts]) for k in range(3))
    order=np.argsort(t);t,y,dy=t[order],y[order],dy[order]
    if np.any(np.diff(t)<=0):raise ValueError('Overlapping QLP sectors')
    return t,y,dy,evidence


def select(legacy,observations,limit):
    obs_by_tic={}
    for o in observations:obs_by_tic.setdefault(int(o['target_name']),{})[int(o['sequence_number'])]=o
    rows=[]
    for path in (legacy/'targets').glob('*.json'):
        r=json.loads(path.read_text())
        if r['status']!='screened' or r['median_scatter_floor_ppm']>600:continue
        target=r['target'];products=obs_by_tic.get(r['tic'],{})
        newer=sorted(s for s in products if s>85)
        pairs=[[s,s+1] for s in newer if s+1 in newer]
        reserve=[s for s in products if 56<=s<=85]
        if not pairs or not reserve:continue
        # New observations are discovery data, not subsequently blind validation.
        target=dict(target);target['training_sectors']=pairs[-1];target['heldout_sectors']=sorted(reserve)
        target['qlp_products']={str(s):products[s] for s in target['training_sectors']}
        target['legacy_noise_ppm']=r['median_scatter_floor_ppm'];target['legacy_discovery_sha256']=sha(path)
        rows.append(target)
    rows.sort(key=lambda t:(t['legacy_noise_ppm'],t['tic']))
    return rows[:limit]


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--legacy',type=Path,required=True)
    p.add_argument('--observations',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--limit',type=int,default=60);p.add_argument('--workers',type=int,default=2)
    p.add_argument('--selected',type=Path,help='Reuse an exact saved selection')
    p.add_argument('--max-baseline-days',type=float,default=120,help='Newer sectors can span about 54 days each')
    p.add_argument('--estimate-missing-errors',action='store_true',help='Explicit exploratory fallback only where no published usable uncertainties exist')
    a=p.parse_args();obs=json.loads(a.observations.read_text())
    if not 1<=a.limit<=200 or not 1<=a.workers<=4:p.error('limit 1..200 and workers 1..4 required')
    if not 100<=a.max_baseline_days<=180:p.error('max baseline must be 100..180 days')
    targets=json.loads(a.selected.read_text()) if a.selected else select(a.legacy,obs,a.limit)
    if a.estimate_missing_errors:targets=[{**t,'estimate_missing_errors':True} for t in targets]
    if not targets:p.error('No eligible targets with newer adjacent QLP sectors')
    a.output.mkdir(parents=True,exist_ok=False);(a.output/'targets').mkdir();(a.output/'source').mkdir()
    for source in Path(__file__).parent.glob('*.py'):shutil.copyfile(source,a.output/'source'/source.name)
    for name in ['uv.lock','pyproject.toml']:shutil.copyfile(name,a.output/'source'/name)
    save_json(a.output/'selected.json',targets)
    run={'started_utc':now(),'status':'running','n_selected':len(targets),'settings':{**SETTINGS,'max_training_baseline_days':a.max_baseline_days,'estimate_missing_errors':a.estimate_missing_errors},
        'selection':'Quietest completed legacy targets with <=600ppm floor, latest adjacent pair >85, and unused QLP sector 56..85 available',
        'caution':'Legacy-only selection; snapshots record exact chosen sample. Both legacy discovery and new QLP discovery are no longer held out. QLP aperture crowding remains unassessed.',
        'saved_selection_sha256':sha(a.selected) if a.selected else None,
        'observation_sha256':sha(a.observations),'source_sha256':{p.name:sha(p) for p in (a.output/'source').glob('*.py')}}
    save_json(a.output/'run.json',run);results=[]
    with ThreadPoolExecutor(a.workers) as pool:
        futures=[pool.submit(process_target,t,Path('data'),a.output,load_qlp,a.max_baseline_days) for t in targets]
        for future in as_completed(futures):
            results.append(future.result());save_json(a.output/'progress.json',{'completed':len(results),'total':len(targets),'updated_utc':now()})
    review=[]
    for r in results:
        for i,peak in enumerate(r.get('screened_peaks',[])):
            if set(peak['flags'])<= {'crowding_or_missing_crowding'}:
                review.append({'tic':r['tic'],'peak_index':i,'best':peak['best'],'flags':peak['flags']})
    run.update(status='complete',finished_utc=now(),n_errors=sum(r['status']=='error' for r in results))
    save_json(a.output/'run.json',run);save_json(a.output/'review.json',review)
    print('Needs pixel/crowding vetting:',review,flush=True)

if __name__=='__main__':main()
