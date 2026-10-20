from pathlib import Path
import json,csv,math
from collections import Counter
from exoplanet.pipeline import sha,save_json,now
from exoplanet.targeting import training_sectors
out=Path(__file__).parent;src=Path('results/nearby-solar-radius-inventory-20261011/opportunities.json');rows=json.loads(src.read_text());known=set();inputs={str(src):sha(src)};catalogs=[]
for name,path,key in [('TOI','data/catalogs/toi.csv','tid'),('confirmed','data/catalogs/confirmed.csv','tic_id'),('CTOI','data/targeting/ctoi.csv','TIC ID'),('archived EB','data/targeting/eb.csv','tess_id')]:
 p=Path(path);rs=list(csv.DictReader(p.open()));assert rs and key in rs[0]
 ids={int(r[key].replace('TIC','').strip()) for r in rs};known|=ids;inputs[path]=sha(p);catalogs.append(dict(name=name,path=path,sha256=sha(p),unique_ids=len(ids)))
counts=Counter();eligible=[];excluded=[]
for r in rows:
 s=r['star'];tic=r['tic'];train=training_sectors(r['sectors']);reason=None
 if tic in known:reason='known_exact_tic'
 elif s.get('contratio') is None or not 0<=s['contratio']<=.2:reason='contamination_or_missing'
 elif not train:reason='no_adjacent_training_pair'
 if reason:counts[reason]+=1;excluded.append(dict(tic=tic,reason=reason));continue
 score=s['rad']**2*10**(.2*(s['Tmag']-10))/math.sqrt(len(train))
 eligible.append(dict(tic=tic,star=s,sectors=r['sectors'],training_sectors=train,heldout_sectors=[r['reserved_sector']],priority_noise_proxy=score))
eligible.sort(key=lambda r:(r['priority_noise_proxy'],r['tic']));pilot=eligible[:16]
# Check selected reserved products are absent before any discovery download.
for r in pilot:
 for sector in r['heldout_sectors']:assert not Path(f'data/lightcurves/s{sector:04d}-{r["tic"]}.fits').exists()
save_json(out/'eligible.json',eligible);save_json(out/'selected.json',pilot);save_json(out/'exclusions.json',excluded)
save_json(out/'plan.json',dict(created_utc=now(),inputs=inputs,catalogs=catalogs,n_input=len(rows),counts=dict(counts),n_eligible=len(eligible),n_pilot=len(pilot),selection_script_sha256=sha(Path(__file__)),policy='Existing adjacent <=55 training selection, max3; latest ordinary sector56..107 reserved. Contamination<=0.2. Rank radius^2 *10^(.2*(Tmag-10))/sqrt(training sectors). Exact TIC catalog exclusions only. Cached catalogs are not a complete novelty check; positional/VSX checks required for signals. No stellar-temperature cut in this expanded-radius pool.'))
print(dict(counts),'eligible',len(eligible),'pilot',[(r['tic'],r['training_sectors'],r['heldout_sectors']) for r in pilot])
