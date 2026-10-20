from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;base=Path('results/qlp-near-epoch-after18-20261011')
d=json.loads((base/'inventory.json').read_text());assert sha(base/'eligible.json')==d['eligible_sha256']
assert not (out/'selected.json').exists()
targets=[]
for t in json.loads((base/'eligible.json').read_text()):
 if 104 not in t['sectors']:continue
 held=sorted((s for s in t['sectors'] if s!=104),key=lambda s:(-abs(s-104),-s))
 targets.append(dict(t,training_sectors=[104],heldout_sectors=held))
assert len(targets)==3 and {t['tic'] for t in targets}==set(d['ranked_sectors'][0]['tics'])
save_json(out/'selected.json',targets)
save_json(out/'audit.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'inventory_sha256':sha(base/'inventory.json'),'selected_sha256':sha(out/'selected.json'),'n_selected':len(targets),'policy':'All3untouched metadata-ranked Sector104 targets; reserve other sectors ordered by greatest separation then latest. At least one distinct but nearby epoch; no long-term replication. Original transit gates unchanged.'})
