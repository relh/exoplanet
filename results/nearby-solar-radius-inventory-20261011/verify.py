from pathlib import Path
import json,csv
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;sel=json.loads((p/'selection.json').read_text());rows=json.loads((p/'opportunities.json').read_text());source=json.loads((p/'source.json').read_text());assert sha(Path(source['path']))==source['sha256']
for path,digest in sel['inputs'].items():assert sha(Path(path))==digest
catalog=json.loads(Path(source['path']).read_text());assert len(catalog['data'])==catalog['paging']['rowsFiltered']==27033;assert len({x['ID'] for x in catalog['data']})==27033
byid={x['ID']:x for x in catalog['data']};cov={int(r['tic']):list(map(int,r['sectors'].split())) for r in csv.DictReader(open('data/targeting/coverage.csv'))};prior=set(sel['prior_ids'])
assert len(rows)==len({r['tic'] for r in rows})==sel['n_opportunities'];assert sum(v for k,v in sel['counts'].items() if k!='catalog')+len(rows)==len(byid)
for r in rows:
 assert r['star']==byid[r['tic']] and r['tic'] not in prior
 assert r['discovery_sector'] in cov[r['tic']] and r['reserved_sector'] in cov[r['tic']]
 assert r['discovery_sector']<=55<r['reserved_sector']<=107
save_json(p/'verification.json',dict(status='passed',unique_catalog_rows=len(byid),opportunities_checked=len(rows),partition_counts_reconciled=True,limits='Verifies cached metadata, not light-curve usability or novelty.'))
print(len(rows),'opportunities checked')
