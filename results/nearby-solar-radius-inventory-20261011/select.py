from pathlib import Path
import csv,json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;p=Path('data/targeting/nearby-solar-radius-20261011.json');meta=json.loads((out/'source.json').read_text());assert sha(p)==meta['sha256'];a=json.loads(p.read_text());stars=a['data'];assert a['status']=='COMPLETE' and len(stars)==a['paging']['rowsFiltered']
coverage_path=Path('data/targeting/coverage.csv');coverage={int(r['tic']):sorted(map(int,r['sectors'].split())) for r in csv.DictReader(coverage_path.open())}
# Exclude any target with a prior target result filename, independent of campaign.
prior={int(p.stem) for p in Path('results').glob('*/targets/*.json') if p.stem.isdigit()}
# Cache filenames supply an additional local reuse check; these do not establish global novelty.
import re
for folder in ['data/qlp','data/lightcurves']:
 for q in Path(folder).glob('*.fits'):
  m=re.match(r'(\d+)-s\d+',q.name) if folder.endswith('qlp') else re.match(r's\d+-(\d+)',q.name)
  if m:prior.add(int(m[1]))
selected=[];counts=dict(catalog=len(stars),no_coverage=0,prior=0,not_multiepoch=0,excluded_catalog_flags=0)
for s in stars:
 tic=int(s['ID']);sectors=coverage.get(tic,[])
 if tic in prior:counts['prior']+=1;continue
 if s.get('duplicate_id') or s.get('disposition') not in [None,'NULL','--','']:counts['excluded_catalog_flags']+=1;continue
 if not sectors:counts['no_coverage']+=1;continue
 old=[v for v in sectors if v<=55];new=[v for v in sectors if 56<=v<=107]
 if not old or not new:counts['not_multiepoch']+=1;continue
 selected.append(dict(tic=tic,star=s,sectors=sectors,discovery_sector=old[0],reserved_sector=new[-1]))
selected.sort(key=lambda r:(r['star']['Tmag'],r['tic']))
save_json(out/'opportunities.json',selected)
save_json(out/'selection.json',dict(counts=counts,n_opportunities=len(selected),inputs={str(q):sha(q) for q in [p,coverage_path,Path(__file__)]},prior_ids=sorted(prior),limits='Cached TESS-SPOC sector inventory, not a new product availability query. Sector numbering is only a coarse epoch proxy. No light curves opened, no known-planet catalog screening yet. Metadata opportunities, not candidates. Local result/cache exclusion is not an exhaustive audit of every historical artifact or global searches.'))
print(counts,'opportunities',len(selected));print(selected[:3])
