"""Positional match against a dated, previously downloaded RVBank index only."""
from pathlib import Path
import json,hashlib
from bs4 import BeautifulSoup
from astropy.coordinates import SkyCoord
import astropy.units as u
O=Path(__file__).parent;raw=Path('data/rv/rvbank-index.html');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
plan=json.loads((O/'plan.json').read_text());rows=[];errors=[]
for a in BeautifulSoup(raw.read_text(),'html.parser').find_all('a'):
 href=str(a.get('href',''))
 if not(href.startswith('./Ver_02/') and href.endswith('_HARPS_RVBank_ver02.csv')):continue
 cells=a.find_parent('tr').find_all(['th','td'],recursive=False);f=[c.get_text(' ',strip=True) for c in cells]
 try:
  assert len(f)==12
  c=SkyCoord(f[1],f[2],unit=(u.hourangle,u.deg));rows.append(dict(name=f[0],ra=c.ra.deg,dec=c.dec.deg,href=href))
 except Exception as e:errors.append(dict(cells=f,error=str(e)))
c=SkyCoord([r['ra'] for r in rows]*u.deg,[r['dec'] for r in rows]*u.deg);out=[]
for t in plan['targets']:
 sep=SkyCoord(t['ra']*u.deg,t['dec']*u.deg).separation(c).arcsec;i=int(sep.argmin());out.append(dict(tic=t['tic'],matches=[{**r,'separation_arcsec':float(d)} for r,d in zip(rows,sep) if d<=120],nearest={**rows[i],'separation_arcsec':float(sep[i])}))
obj=dict(raw_path=str(raw),raw_sha256=sha(raw),original_provenance=json.loads(Path(str(raw)+'.json').read_text()),script_sha256=sha(Path(__file__)),n_index_rows=len(rows),parse_errors=errors,radius_arcsec=120,targets=out,limits='Dated index only, not a live all-archive inventory or physical exclusion. No RV series values read. Web viewer rejected live HTML as too large; cached original source used explicitly.')
(O/'rvbank.json').write_text(json.dumps(obj,indent=2)+'\n');print(obj['n_index_rows'],[(r['tic'],len(r['matches']),r['nearest']['separation_arcsec']) for r in out],errors)
