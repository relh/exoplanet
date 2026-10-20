from pathlib import Path
import json,csv,io,hashlib
p=Path(__file__).parent;rs=json.loads((p/'results.json').read_text())
assert {r['tic'] for r in rs}=={241928959,422626648}
for r in rs:
 assert r['status']=='success';raw=Path(r['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==r['sha256']
 reader=csv.DictReader(io.StringIO(raw.decode()));assert list(reader)==r['rows']==[];assert reader.fieldnames==r['columns'];assert {'Per','Type','RAJ2000','DEJ2000'}<=set(reader.fieldnames)
(p/'verification.json').write_text(json.dumps(dict(status='passed',successful_empty_cones=2,radius_arcsec=60,raw_hashes_and_csv_headers_verified=True),indent=2)+'\n')
