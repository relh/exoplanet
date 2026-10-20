from pathlib import Path
import json,copy
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import process_target,SETTINGS
out=Path(__file__).parent;source=Path('results/qlp-faint-midradius-near-reserved-remaining-20261011/targets/139343242.json');original=json.loads(source.read_text());target=copy.deepcopy(original['target'])
assert original['status']=='error' and target['training_sectors']==[45,46,47] and target['heldout_sectors']==[44]
assert not (out/'plan.json').exists() and not Path('data/qlp/139343242-s0044.fits').exists()
target['training_sectors']=[45,47]
save_json(out/'plan.json',{'utc':now(),'target':target,'parent_path':str(source),'parent_sha256':sha(source),'script_sha256':sha(Path(__file__)),'source_hashes':{p.name:sha(p) for p in Path('src/exoplanet').glob('*.py')},'settings':SETTINGS,'policy':'Exclude only sector46 with audited zero finite selected flux. Search original discovery45/47 with unchanged gates and max_baseline120. Preserve failed parent and reserve44. If47 fails, retain failure rather than silently changing selection.'})
(out/'targets').mkdir(exist_ok=True)
r=process_target(target,Path('data'),out,load_qlp,120)
save_json(out/'result.json',r)
print(r['status'],r.get('disposition'),r.get('error'),flush=True)
