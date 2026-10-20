"""Recover terminal target data errors without changing the active survey."""
from pathlib import Path
import json,time,traceback
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import process_target
from exoplanet.qlp_followup import follow_qlp
out=Path(__file__).parent;campaign=Path('results/qlp-faint-expanded-20261010');prior=Path('results/qlp-faint-recovery-389918717-20261010/result.json')
assert not (out/'plan.json').exists()
prior_result=json.loads(prior.read_text());assert prior_result['status']=='screened'
save_json(out/'plan.json',{'utc':now(),'campaign_plan_sha256':sha(campaign/'plan.json'),'prior_recoveries':[{'tic':389918717,'path':str(prior),'sha256':sha(prior)}],'script_sha256':sha(Path(__file__)),'source_sha256':{p.name:sha(p) for p in Path('src/exoplanet').glob('*.py')},'policy':'Every terminal original target error once, excluding documented prior recovery. Inspect assigned training sectors separately. If >=3 are usable, process all usable assigned sectors with unchanged gates and120daybaseline limit. Preserve original errors and narrower coverage. No raw data/history deletion. Any recovered eligible peaks receive separately frozen native follow-up at first2reservedsectors; detrending-only checks labeled diagnostic. Do not count recovery as another star.'})
seen={389918717};records=[]
def errors():
 items=[]
 for p in (campaign/'targets').glob('*.json'):
  try:r=json.loads(p.read_text())
  except json.JSONDecodeError:continue
  if r['status']=='error' and r.get('finished_utc') and r['tic'] not in seen:items.append((p,r))
 return items
while True:
 for source,r in errors():
  tic=r['tic'];seen.add(tic);dest=out/str(tic);dest.mkdir();target=r['target'];checks=[];usable=[]
  record={'tic':tic,'original_path':str(source),'original_sha256':sha(source),'started_utc':now()}
  save_json(dest/'plan.json',{'utc':now(),'target':target,'original_error':r['error'],'original_sha256':sha(source),'parent_plan_sha256':sha(out/'plan.json')})
  try:
   for sector in target['training_sectors']:
    check={'sector':sector}
    try:
     t,y,e,evidence=load_qlp(dict(target,training_sectors=[sector]),Path('data'));check.update(status='usable',n_clean=len(t),evidence=evidence);usable.append(sector)
    except Exception as exc:check.update(status='error',error=repr(exc))
    raw=Path(f'data/qlp/{tic}-s{sector:04d}.fits');meta=raw.with_suffix('.fits.json')
    if raw.exists():check['raw_sha256']=sha(raw)
    if meta.exists():check['download_provenance']=json.loads(meta.read_text())
    checks.append(check);save_json(dest/'sector-checks.json',checks)
   record['usable_sectors']=usable
   if len(usable)>=3:
    (dest/'targets').mkdir();result=process_target(dict(target,training_sectors=usable),Path('data'),dest,load_qlp,120)
    record.update(status=result['status'],disposition=result.get('disposition'),error=result.get('error'),result_path=str(dest/'targets'/f'{tic}.json'))
    followups=[]
    for i,peak in enumerate(result.get('screened_peaks',[])):
     if set(peak['flags'])<={'crowding_or_missing_crowding','alternative_detrending_prefers_other_period'}:
      check=follow_qlp(dest/'targets'/f'{tic}.json',dest/f'followup-{i}',peak_index=i,max_sectors=2)
      followups.append({'peak_index':i,'original_flags':peak['flags'],'diagnostic_only':'alternative_detrending_prefers_other_period' in peak['flags'],'checks':check})
    record['followups']=followups
   else:record['status']='insufficient_training_coverage'
  except Exception as exc:record.update(status='recovery_error',error=repr(exc),traceback=traceback.format_exc())
  record['finished_utc']=now();save_json(dest/'result.json',record);records.append(record);save_json(out/'progress.json',records);print(tic,record['status'],record.get('disposition'),usable,flush=True)
 if (campaign/'results.json').exists() and not errors():break
 time.sleep(15)
save_json(out/'terminal.json',{'utc':now(),'status':'complete','records':records,'prior_recovery_tics':[389918717]})
