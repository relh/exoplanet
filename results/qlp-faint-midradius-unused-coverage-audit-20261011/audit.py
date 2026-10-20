"""Audit the remaining metadata pool without opening photometry."""
from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());prior=Path('results/qlp-faint-midradius-one-reserved-pilot-20261011');sel=read(prior/'selection.json');pool=Path(sel['pool_path']);assert sha(pool)==sel['pool_sha256'];eligible=read(prior/'eligible.json');assert sha(prior/'eligible.json')==sel['eligible_sha256'];excluded=set(sel['excluded_ids'])|{r['tic'] for r in eligible};obs={}
for src in sel['coverage_sources']:
 p=Path(src['path']);assert sha(p)==src['sha256']
 for r in read(p)['data']:obs.setdefault(int(r['target_name']),set()).add(int(r['sequence_number']))
rows=[];counts=Counter();lengths=Counter()
for t in read(pool):
 if t['tic'] in excluded:continue
 sectors=sorted(obs.get(t['tic'],[]));cached=[str(p) for p in Path('data/qlp').glob(f"{t['tic']}-s*.fits")];assert not cached
 longest=max((sum(1 for k in range(len(sectors)) if all(s+j in sectors for j in range(k+1))) for s in sectors),default=0)
 if not sectors:category='no_qlp_product'
 elif len(sectors)==1:category='single_sector_only'
 elif sectors[-1]-sectors[0]<8:category='multiple_sectors_without_distant_reserve'
 else:category='unexpected_distant_reserve'
 counts[category]+=1;lengths[len(sectors)]+=1;rows.append({'tic':t['tic'],'sectors':sectors,'longest_consecutive_block':longest,'category':category,'cached_qlp':cached})
assert len(rows)==2024 and counts['unexpected_distant_reserve']==0
save_json(out/'inventory.json',rows)
save_json(out/'audit.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'inputs':{str(prior/'selection.json'):sha(prior/'selection.json'),str(prior/'eligible.json'):sha(prior/'eligible.json'),str(pool):sha(pool)},'coverage_sources':sel['coverage_sources'],'inventory_sha256':sha(out/'inventory.json'),'n_remaining':len(rows),'counts':dict(counts),'sector_counts':dict(lengths),'limits':'Metadata only; no photometry opened. Local unused sample is not globally unexplored. Fewer or adjacent epochs cannot supply the prior distant-sector validation design.'})
print(dict(counts),dict(lengths));print('multisector examples',[r for r in rows if len(r['sectors'])>1][:10])
