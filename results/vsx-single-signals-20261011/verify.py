from pathlib import Path
import json, hashlib
from astropy.coordinates import SkyCoord
import astropy.units as u
out=Path(__file__).parent
load=lambda p:json.loads(Path(p).read_text())
records=load(out/'results.json')+[load(out/'paper-source.json'),load(out/'epic-source-corrected.json')]
for r in records:
 assert hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()==r['sha256']
epic=records[-1]['rows'][0]
tic=next(r for r in load('results/neighbors-196681132-20261011/neighbors.json') if r['ID']==196681132)
assert epic['2MASS'].strip()==tic['TWOMASS']
assert epic['UCAC4']==tic['UCAC']
text=Path('data/literature/crossfield-2018-c17-arxiv.txt').read_text()
assert 'Eclipsing Binaries' in text
line=next(l for l in text.splitlines() if l.startswith('212601505'))
assert line.split()[3]=='0.724453'
sep=SkyCoord(float(epic['RAJ2000'])*u.deg,float(epic['DEJ2000'])*u.deg).separation(SkyCoord(tic['ra']*u.deg,tic['dec']*u.deg)).arcsec
result=dict(status='passed',raw_hashes_verified=len(records),same_2mass=tic['TWOMASS'],same_ucac=tic['UCAC'],unpropagated_epic_tic_separation_arcsec=sep,paper_row=line,tess_minus_paper_period_seconds=(.7244717004955156-.724453)*86400,tess_minus_vsx_period_seconds=(.7244717004955156-.72436144)*86400)
(out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
