"""Parse the site's HTML-wrapped CSV, whose header order differs from body."""
from pathlib import Path
from html.parser import HTMLParser
import re,csv,json
from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
p=Path('data/catalogs/villanova-current-20261010.csv')
class TextParser(HTMLParser):
 def __init__(self):
  super().__init__(); self.parts=[]
 def handle_data(self,data): self.parts.append(data)
parser=TextParser();parser.feed(p.read_text());s=' '.join(parser.parts)
chunks=re.split(r'\bTrue,',s)[1:]
rows=[]
for chunk in chunks:
 fields=[v.strip() for v in next(csv.reader([' '.join(chunk.split())]))]
 assert len(fields)==7,fields
 tic,sectors,ra,dec,period,flags,_=fields
 assert tic.isdigit() and all(x.isdigit() for x in sectors.split(';'))
 rows.append(dict(tic=int(tic),sectors=sectors,ra=float(ra),dec=float(dec),period=float(period),flags=flags))
assert len(rows)==4584 and len({r['tic'] for r in rows})==4578
save_json(out/'villanova-parsed.json',rows)
coords=SkyCoord([r['ra'] for r in rows]*u.deg,[r['dec'] for r in rows]*u.deg)
targets=json.loads(Path('results/selection-late-sectors-20261010/eligible.json').read_text())
matches=[]
for t in targets:
 star=t['star'];sep=SkyCoord(star['ra']*u.deg,star['dec']*u.deg).separation(coords).arcsec
 for i in np.flatnonzero(sep<126):matches.append(dict(search_tic=t['tic'],separation_arcsec=float(sep[i]),binary=rows[i]))
sep=SkyCoord(165.31041473672*u.deg,-48.6136321332977*u.deg).separation(coords).arcsec
save_json(out/'villanova-crossmatch.json',{'utc':now(),'raw_sha256':sha(p),'rows':len(rows),'parser_note':'Server returns HTML-wrapped CSV. Body order verified by ID, semicolon-delimited sectors and coordinate values; differs from requested-order header. Catalog count matches live 4584-entry list. No negative result means absence of binaries.','search_radius_arcsec':126,'matches':matches,'tic80387959_within360arcsec':[dict(separation_arcsec=float(sep[i]),binary=rows[i]) for i in np.flatnonzero(sep<360)]})
print('matches',matches)
