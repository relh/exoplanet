from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
p=Path(__file__).parent;src=Path('results/solar-radius-pilot-selection-20261011/eligible.json');eligible=json.loads(src.read_text());rows=eligible[1872:];assert len(rows)==5132;assert len({r['tic'] for r in rows})==len(rows)
for r in rows:
 for s in r['training_sectors']+r['heldout_sectors']:assert not Path(f"data/lightcurves/s{s:04d}-{r['tic']}.fits").exists()
batches=[]
for start in range(1872,len(eligible),512):
 end=min(start+512,len(eligible));selection=p/f'selected-{start}-{end}.json';save_json(selection,eligible[start:end]);batches.append(dict(start=start,end=end,n=end-start,selection=str(selection),selection_sha256=sha(selection),output=f'results/solar-radius-ranks{start}-{end}-20261011'))
save_json(p/'plan.json',dict(created_utc=now(),source=str(src),source_sha256=sha(src),total=5132,workers=2,batches=batches,policy='All remaining targets in original frozen order. No new ranking or relaxed gates. Discovery and reserved caches absent before queue launch. Runs independent of ranks1360–1871; never reads reserved sectors during discovery. Stop on process errors or insufficient disk.'))
print(len(batches),'batches prepared')
