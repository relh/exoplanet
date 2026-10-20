"""Apply the established time-only recovery policy to completed baseline failures."""
from pathlib import Path
from functools import partial
import json,time,traceback
import numpy as np
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import process_target
from exoplanet.qlp_followup import follow_qlp
from exoplanet.plots import plot_discovery
from exoplanet.secondary import scan_secondary

out=Path(__file__).parent
campaign=Path('results/qlp-faint-midradius-remaining-four-20261011')
read=lambda p:json.loads(p.read_text())
assert not (out/'plan.json').exists()
expected={t['tic']:t for t in read(campaign/'plan.json')['targets']}
save_json(out/'plan.json',{'utc':now(),'campaign_plan_sha256':sha(campaign/'plan.json'),
    'script_sha256':sha(Path(__file__)),
    'source_sha256':{p.name:sha(p) for p in Path('src/exoplanet').glob('*.py')},
    'policy':'Each terminal original error once. Only the known dense-search baseline-limit error is automatically retried. Choose the longest latest suffix of three then two originally assigned training sectors whose cleaned time baseline is <=120 days, before any recovery period search. No reserved epochs used in selection. Original failures retained; alternate windows are not additional stars. Other errors are explicitly deferred for review. Same screening and two-sector native follow-up policies as parent, including separately labeled coverage/detrending diagnostics. Every generated plot requires human/agent review before scientific classification.'})
seen=set();records=[]
def pending():
    items=[]
    for p in (campaign/'targets').glob('*.json'):
        try:r=read(p)
        except json.JSONDecodeError:continue
        if r['status']=='error' and r.get('finished_utc') and r['tic'] not in seen:items.append((p,r))
    return sorted(items,key=lambda item:item[1]['tic'])

while True:
    for source,original in pending():
        tic=original['tic'];seen.add(tic);target=original['target']
        assert target==expected[tic]
        dest=out/str(tic);dest.mkdir()
        rec={'tic':tic,'original_path':str(source),'original_sha256':sha(source),'started_utc':now(),'original_error':original['error']}
        save_json(dest/'plan.json',{**rec,'parent_plan_sha256':sha(out/'plan.json'),'target':target})
        try:
            if original['error']!='ValueError: Training baseline exceeds configured dense-search limit':
                rec.update(status='deferred_other_error',reason='Requires individual data-error review; not a nondetection')
            else:
                assert original['clean_baseline_days']>120 and not original.get('screened_peaks')
                raw=[]
                for ev in original['data']:
                    p=Path(f"data/qlp/{tic}-s{ev['sector']:04d}.fits")
                    assert sha(p)==ev['source']['sha256']
                    raw.append({'path':str(p),'sha256':sha(p)})
                reserved_cached=[s for s in target['heldout_sectors'] if Path(f'data/qlp/{tic}-s{s:04d}.fits').exists()]
                assert not reserved_cached,'Unexpected reserved photometry already cached'
                options=[];chosen=None
                for n in [3,2]:
                    probe=dict(target,training_sectors=target['training_sectors'][-n:])
                    try:
                        t,y,e,evidence=load_qlp(probe,Path('data'))
                        baseline=float(np.ptp(t))
                        options.append({'training_sectors':probe['training_sectors'],'clean_baseline_days':baseline,'n_clean':len(t)})
                    except Exception as exc:
                        options.append({'training_sectors':probe['training_sectors'],'error':repr(exc)});continue
                    if baseline<=120:chosen=probe;break
                save_json(dest/'selection.json',{'utc':now(),'original_sha256':sha(source),'raw':raw,'options':options,'chosen':chosen,'reserved_cached_before_recovery':reserved_cached})
                if chosen is None:rec['status']='no_viable_reduced_window'
                else:
                    assert not set(chosen['training_sectors'])&set(chosen['heldout_sectors'])
                    (dest/'targets').mkdir()
                    result=process_target(chosen,Path('data'),dest,load_qlp,120)
                    rp=dest/'targets'/f'{tic}.json'
                    rec.update(status=result['status'],disposition=result.get('disposition'),error=result.get('error'),result_path=str(rp),result_sha256=sha(rp),training_sectors=chosen['training_sectors'])
                    followups=[]
                    for i,peak in enumerate(result.get('screened_peaks',[])):
                        flags=set(peak['flags']);base={'crowding_or_missing_crowding','alternative_detrending_prefers_other_period'}
                        coverage={'secondary_unmeasurable','fewer_than_3_supported_events'}
                        category='original' if flags<=base else 'coverage_diagnostic' if flags<=base|coverage and flags&coverage and peak['diagnostics']['supported_events']>=2 else None
                        if category is None:continue
                        fd=dest/f'followup-{i}'
                        checks=follow_qlp(rp,fd,peak_index=i,max_sectors=2)
                        plot_discovery(rp,fd/'discovery.png',peak_index=i,loader=partial(load_qlp,bin_minutes=0))
                        t,y,e,evidence=load_qlp(chosen,Path('data'))
                        save_json(fd/'secondary.json',{'data':evidence,'diagnostic':scan_secondary(t,y,e,peak['best']),'policy':'Training-only exploratory selected statistic, not calibrated confidence'})
                        followups.append({'peak_index':i,'category':category,'diagnostic_only':category=='coverage_diagnostic' or 'alternative_detrending_prefers_other_period' in flags,'original_flags':peak['flags'],'directory':str(fd),'checks':checks,'review_status':'pending'})
                    rec['followups']=followups
        except Exception as exc:rec.update(status='recovery_error',error=repr(exc),traceback=traceback.format_exc())
        rec['finished_utc']=now();save_json(dest/'result.json',rec);records.append(rec)
        save_json(out/'progress.json',records);print(tic,rec['status'],rec.get('disposition'),flush=True)
    if (campaign/'results.json').exists() and not pending():break
    time.sleep(15)
save_json(out/'terminal.json',{'utc':now(),'status':'complete','records':records})
