from pathlib import Path
import hashlib,json,datetime
R=Path('results/triceratops-20261013');D=Path('data/triceratops-20261013');files=[]
for p in sorted(R.rglob('*')):
 if p.is_file() and p.name!='provenance.json':files.append(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size))
raw=[]
for p in D.glob('*'):
 if p.is_file():raw.append(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size))
source=D/'venv/lib/python3.12/site-packages/triceratops'
software=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(source.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
science=[]
for t,s in [(80387959,36),(402358350,54),(137151335,40)]:
 p=Path(f'data/lightcurves/s{s:04d}-{t}.fits');side=json.loads(Path(str(p)+'.json').read_text());science.append(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),url=side['url'],retrieved_utc=side['retrieved_utc']))
(R/'provenance.json').write_text(json.dumps(dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),files=files,raw=raw,software=software,science=science,software_url='https://pypi.org/project/triceratops/1.1.0/',upstream_source_url='https://raw.githubusercontent.com/stevengiacalone/triceratops/v1.1.0/triceratops/triceratops.py',catalogs='Cached TIC source/source.json URLs identified by plan.json inputhashes and prior neighbor assessments; Gaia rawqueries in*-gaia-raw-provenance.json'),indent=2))
