from pathlib import Path
import json,csv,re,math
from exoplanet.pipeline import sha,save_json,now
p=Path(__file__).parent;qs=json.loads((p/'queries.json').read_text());res=json.loads((p/'results.json').read_text());assert sha(p/'analyze.py')==res['script_sha256'];records=qs+[json.loads((p/'references.json').read_text()),json.loads((p/'eb-probe.json').read_text())]+json.loads((p/'literature-sources.json').read_text())
for rec in records:
 if 'path' in rec:assert sha(Path(rec['path']))==rec['sha256']
ct=next(x for x in qs if x['name']=='current-ctoi');assert ct['status']=='success';rows=list(csv.DictReader(Path(ct['path']).open()));assert len(rows)==ct['row_count']==res['ctoi_rows'];assert [x for x in rows if x['TIC ID'].strip()=='402358350']==res['ctoi_exact_tic_matches']==ct['rows'];near=[]
for r in rows:
 ra,de=map(math.radians,[float(r['RA']),float(r['Dec'])]);ra0,de0=map(math.radians,[295.15063723769,15.64029808626]);v=math.sin((de-de0)/2)**2+math.cos(de)*math.cos(de0)*math.sin((ra-ra0)/2)**2;sep=math.degrees(2*math.asin(math.sqrt(max(0,min(1,v)))))*3600
 if sep<=120:near.append(r)
assert near==[x['row'] for x in res['ctoi_within120arcsec']];assert res['coordinate_parse_errors']==[]
page=Path(next(x for x in qs if x['name']=='target-page')['path']).read_text();assert '<title>ExoFOP TIC 402358350</title>' in page
for name,var in [('TOI','rowData'),('CTOI','rowData2'),('planet_parameters','rowData3')]:assert len(json.loads(re.search(r'var '+var+r' = (\[.*?\]);',page)[1]))==res['target_page_counts'][name]
for x in res['prior_snapshots']:
 assert sha(Path(x['path']))==x['sha256'];rr=list(csv.DictReader(Path(x['path']).open()));assert len(rr)==x['rows'];assert [z for z in rr if z['TIC ID'].strip()=='402358350']==x['exact_tic_matches']
ref=json.loads((p/'references.json').read_text());assert ref['status']=='success';assert list(csv.DictReader(Path(ref['path']).open()))==ref['rows'];eb=json.loads((p/'eb-probe.json').read_text());text=Path(eb['path']).read_text();assert 'TIC 402358350' in text and 'This TESS ID is not in the catalog.' in text
save_json(p/'verification.json',dict(status='passed',utc=now(),ctoi_rows_checked=len(rows),coordinate_check='independent spherical separation calculation',target_page_tables_checked=3,simbad_reference_rows=len(ref['rows']),eb_page_explicit_nonmembership=True,raw_hashes_checked=sum('path' in x for x in records),limits='Snapshot parsing/identity/provenance checks; not complete catalog freshness or exhaustive literature/novelty proof.'))
