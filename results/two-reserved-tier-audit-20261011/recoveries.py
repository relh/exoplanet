from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
p=out/'audit.json';d=json.loads(p.read_text())
errors={int(t) for t,rs in d['records'].items() if rs[0]['status']=='error'}
found={}
for q in sorted(Path('results').glob('qlp-faint*recovery*/**/targets/*.json')):
 r=json.loads(q.read_text());tic=r.get('tic')
 if tic not in errors:continue
 original=json.loads(Path(d['records'][str(tic)][0]['path']).read_text())
 if not set(r['target']['training_sectors']) <= set(original['target']['training_sectors']): print('SECTOR REVIEW',tic,r['target']['training_sectors'],original['target']['training_sectors'])
 found.setdefault(tic,[]).append({'path':str(q),'sha256':sha(q),'training_sectors':r['target']['training_sectors'],'original_training_sectors':original['target']['training_sectors'],'status':r['status'],'disposition':r.get('disposition'),'error':r.get('error')})
missing=sorted(errors-set(found))
assert missing==[423088347]
special=Path('results/qlp-faint-expanded-recovery-20261010/423088347')
evidence={str(q):sha(q) for q in special.iterdir() if q.is_file()}
success=[t for t,rs in found.items() if any(r['status']=='screened' for r in rs)]
save_json(out/'recoveries.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'audit_sha256':sha(p),'n_initial_failures':len(errors),'n_recovered':len(success),'recovered_tics':success,'n_remaining_unusable':len(errors)-len(success),'n_usable_after_recovery':d['n_selected']-len(errors)+len(success),'records':found,'special_no_target_file':{'tic':423088347,'evidence':evidence},'limits':'Initial errors retained. Recovery sector identities recorded; differences require review before using aggregate; no failure is counted as a nondetection. Special case reviewed from explicit result and assessment. Does not validate planet classifications.'})
print('Recovered',len(success),'remaining unusable',len(errors)-len(success),'usable',d['n_selected']-len(errors)+len(success))
