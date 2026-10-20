from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());a=read(out/'audit.json');rows=read(out/'inventory.json');assert sha(out/'inventory.json')==a['inventory_sha256']
for path,h in a['inputs'].items():assert sha(Path(path))==h
assert len(rows)==len({r['tic'] for r in rows})==2024
assert dict(Counter(r['category'] for r in rows))==a['counts']
assert {str(k):v for k,v in Counter(len(r['sectors']) for r in rows).items()}==a['sector_counts']
cached={int(p.stem.split('-s')[0]) for p in Path('data/qlp').glob('*-s*.fits')}
for r in rows:
 assert r['tic'] not in cached
 run=best=0;previous=None
 for sector in r['sectors']:
  run=run+1 if previous is not None and sector==previous+1 else 1;best=max(best,run);previous=sector
 assert best==r['longest_consecutive_block']
 assert not r['sectors'] or max(r['sectors'])-min(r['sectors'])<8
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'audit_sha256':sha(out/'audit.json'),'inventory_sha256':sha(out/'inventory.json'),'status':'2024 unique unused IDs, metadata inputs, categories, independently computed consecutive blocks and current QLP cache absence verified; no photometry or sensitivity claim.'})
print(a['counts'])
