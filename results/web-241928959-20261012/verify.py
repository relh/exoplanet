from pathlib import Path
import json,csv,hashlib
from urllib.parse import urlparse,parse_qs
O=Path(__file__).parent
records=[r for p in sorted(O.glob('queries*.json')) for r in json.loads(p.read_text())]
parsed={};errors=[]
for r in records:
 if 'path' not in r:errors.append(r);continue
 p=Path(r['path']);assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
 if r['status']!=200:
  assert 'ERROR' in p.read_text();errors.append(r['name']);continue
 if r['name']=='spyglass-readme':assert 'Candidate members of young associations' in p.read_text();continue
 parsed[r['name']]=list(csv.DictReader(p.open()))
for name in ['spyglass-exact','spyglass-older','binary-exact','wds-cone-fixed']:assert parsed[name]==[]
assert parsed['simbad-ident']==[{'id':'Gaia DR3 6865254022910168320'}]
assert parsed['simbad-ref-join']==[{'bibcode':'2021ApJ...917...23K'}]
source=Path('data/catalogs/neighbors-241928959-20261011.json');tic=next(x for x in json.loads(source.read_text())['data'] if x['ID']==241928959);assert tic['GAIA']=='6865254022910168320';assert tic['TWOMASS']=='19515688-2130112';assert tic['UCAC']=='343-196048';assert tic['ALLWISE']=='J195156.87-213011.2'
for name in ['spyglass-exact','spyglass-older','binary-exact']:
 r=next(x for x in records if x['name']==name);q=parse_qs(urlparse(r['url']).query)['QUERY'][0];assert '6865254022910168320' in q
r=next(x for x in records if x['name']=='binary-exact');assert 'Source1=' in r['url'] or 'Source1%3D' in r['url'];assert 'Source2' in r['url']
wds=next(x for x in records if x['name']=='wds-cone-fixed');q=parse_qs(urlparse(wds['url']).query)['QUERY'][0];assert '297.987022155552,-21.5031691342776,0.0166666667' in q
out=dict(verified=True,raw_records=len(records),errors_preserved=errors,counts={k:len(v) for k,v in parsed.items()},identity_source=str(source),identity_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),aliases={k:tic[k] for k in ['ID','GAIA','TWOMASS','UCAC','ALLWISE']},scope='Response hashes, independent CSV parsing, source identity and exact queries; no completeness claim.')
(O/'verification.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
