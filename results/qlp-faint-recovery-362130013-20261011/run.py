"""Inspect a terminal target error; retain original error and reserved epochs."""
from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import process_target
out=Path(__file__).parent;source=Path('results/qlp-faint-midradius-remaining-two-20261011/targets/362130013.json');original=json.loads(source.read_text());assert original['status']=='error';target=original['target']
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'original_path':str(source),'original_sha256':sha(source),'target':target,'script_sha256':sha(Path(__file__)),'policy':'Original per-target task terminal error; survey worker has terminated. Inspect each of two assigned training sectors only. Retain all errors; if >=2 sectors usable, search those with unchanged pipeline and actualbaseline<=120days. Narrower training coverage explicitly labeled; reserved epochs untouched. Do not overwrite original result or count missing data as no transit.'})
assert all(not Path(f"data/qlp/{target['tic']}-s{s:04d}.fits").exists() for s in target['heldout_sectors'])
checks=[];usable=[]
for sector in target['training_sectors']:
 row={'sector':sector}
 try:
  t,y,e,data=load_qlp(dict(target,training_sectors=[sector]),Path('data'))
  row.update(status='usable',n_clean=len(t),evidence=data);usable.append(sector)
 except Exception as exc:row.update(status='error',error=repr(exc))
 raw=Path(f"data/qlp/{target['tic']}-s{sector:04d}.fits")
 if raw.exists():row['raw_sha256']=sha(raw)
 meta=raw.with_suffix('.fits.json')
 if meta.exists():row['download_provenance']=json.loads(meta.read_text())
 checks.append(row);save_json(out/'sector-checks.json',checks);print(row['sector'],row['status'],row.get('n_clean',row.get('error')),flush=True)
save_json(out/'selection.json',{'utc':now(),'usable_sectors':usable,'sector_checks_sha256':sha(out/'sector-checks.json'),'target':dict(target,training_sectors=usable) if len(usable)>=2 else None,'policy':'All usable original assigned sectors if at least two; no selection by period or measured quietness.'})
if len(usable)>=2:
 (out/'targets').mkdir();r=process_target(dict(target,training_sectors=usable),Path('data'),out,load_qlp,120)
 save_json(out/'result.json',{'utc':now(),'status':r['status'],'disposition':r.get('disposition'),'error':r.get('error'),'usable_sectors':usable,'original_error_retained':True,'path':str(out/'targets'/f'{target["tic"]}.json')})
else:save_json(out/'result.json',{'utc':now(),'status':'insufficient_training_coverage','usable_sectors':usable,'original_error_retained':True})
