from pathlib import Path
import json
from exoplanet.campaign import process_target
from exoplanet.pipeline import save_json,sha,now
p=Path(__file__).parent;src=Path('results/review-267545898-20261011/discovery.json');target=json.loads(src.read_text())['target'];target['training_sectors']=[68];target['heldout_sectors']=[]
save_json(p/'plan.json',dict(created_utc=now(),target=target,source_discovery_sha256=sha(src),code_hashes={x.name:sha(x) for x in Path('src/exoplanet').glob('*.py')},policy='Exploratory application of the unchanged full discovery search to already-opened sector68. Chosen after nominal/profile check; not a new blind holdout. Same gates and search domain; no threshold relaxation.'))
r=process_target(target,Path('data'),p)
print(r['disposition'],r.get('best'),[(x['best']['period'],x['flags']) for x in r.get('screened_peaks',[])])
from exoplanet.plots import plot_discovery
plot_discovery(p/'targets/267545898.json',p/'discovery.png')
