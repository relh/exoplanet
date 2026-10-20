"""Deduplicate the QLP campaign and audit unrecovered native data failures."""
from pathlib import Path
import json,csv
from collections import Counter
import numpy as np
from astropy.io import fits
from exoplanet.archive import qlp_flux_columns
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
initial=Path('results/campaign-qlp-expanded-20261010');recovery=Path('results/campaign-qlp-expanded-recovery-20261010')
run=json.loads((initial/'run.json').read_text());rr=json.loads((recovery/'run.json').read_text())
assert run['status']=='complete' and rr['status']=='complete'
selected=json.loads(Path(run['selection_path']).read_text());ids={r['tic'] for r in selected}
original={int(p.stem):json.loads(p.read_text()) for p in (initial/'targets').glob('*.json')}
recovered={int(p.stem):json.loads(p.read_text()) for p in (recovery/'targets').glob('*.json')}
assert set(original)==ids and set(recovered)<=ids
counts=Counter();fails=[];reviews=[];sources=[]
coverage={int(r['tic']):list(map(int,r['sectors'].split())) for r in csv.DictReader(open('data/targeting/coverage.csv'))}
for tic in sorted(ids):
 row=recovered.get(tic,original[tic]);p=(recovery if tic in recovered else initial)/'targets'/f'{tic}.json'
 sources.append({'tic':tic,'path':str(p),'sha256':sha(p)})
 counts[row.get('disposition',row['status'])]+=1
 if row['status']=='error':
  failure={'tic':tic,'original_error':original[tic]['error'],'final_error':row['error'],'sectors':[],'available_spoc_sectors':coverage.get(tic,[])}
  for s in row['target']['training_sectors']:
   f=Path(f'data/qlp/{tic}-s{s:04d}.fits');entry={'sector':s,'path':str(f)}
   if f.exists():
    entry['sha256']=sha(f)
    with fits.open(f) as h:
     d=h[1].data;flux,error,_=qlp_flux_columns(d.names);q=d['QUALITY']==0
     v=q&np.isfinite(d['TIME'])&np.isfinite(d[flux])&(d[flux]>0)
     entry.update(n_rows=len(d),n_quality_zero=int(q.sum()),n_positive_flux=int(v.sum()),n_valid_pairs=int((v&np.isfinite(d[error])&(d[error]>0)).sum()))
   else:entry['status']='not_downloaded_before_failure'
   failure['sectors'].append(entry)
  fails.append(failure)
 for i,peak in enumerate(row.get('screened_peaks',[])):
  if set(peak['flags'])<={'crowding_or_missing_crowding'}:reviews.append({'tic':tic,'peak_index':i,'best':peak['best'],'flags':peak['flags']})
save_json(out/'audit.json',{'utc':now(),'original_run_sha256':sha(initial/'run.json'),'recovery_run_sha256':sha(recovery/'run.json'),'n_selected':len(ids),'n_usable':len(ids)-len(fails),'n_original_errors':run['n_errors'],'n_recovery_attempted':len(recovered),'n_recovered':sum(r['status']=='screened' for r in recovered.values()),'counts':dict(counts),'remaining_failures':fails,'review_peaks':reviews,'final_records':sources,'note':'Original and recovery target sets deduplicated; empirical errors are labeled in each sector evidence. Remaining failures are not searched nulls.'})
print(dict(counts),'usable',len(ids)-len(fails),'review',reviews)
for f in fails:print(f)
