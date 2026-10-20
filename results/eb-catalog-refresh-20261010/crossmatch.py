"""Compare two complete vetted Kostov2025 tables with our selected stars."""
from pathlib import Path
import csv,json
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
rows=[]
for n,count in [(3,7936),(4,2065)]:
 p=Path(f'data/catalogs/kostov2025-table{n}.csv')
 table=list(csv.DictReader(p.open()));assert len(table)==count
 rows.extend(dict(catalog_table=n,**r) for r in table)
assert len({r['TIC'] for r in rows})==10001
coords=SkyCoord([float(r['RAJ2000']) for r in rows]*u.deg,[float(r['DEJ2000']) for r in rows]*u.deg)
sel=Path('results/selection-late-sectors-20261010/eligible.json')
targets=json.loads(sel.read_text())
matches=[]
for t in targets:
 s=t['star'];sep=SkyCoord(s['ra']*u.deg,s['dec']*u.deg).separation(coords).arcsec
 for i in np.flatnonzero(sep<126):
  matches.append({'search_tic':t['tic'],'separation_arcsec':float(sep[i]),'exact_tic_match':int(rows[i]['TIC'])==t['tic'],'binary':rows[i]})
npth=Path('results/neighbors-80387959-20261009/tic-neighbors.json')
neighbors=json.loads(npth.read_text());ids={str(r['ID']) for r in neighbors}
nmatch=[r for r in rows if r['TIC'] in ids]
sep=SkyCoord(165.31041473672*u.deg,-48.6136321332977*u.deg).separation(coords).arcsec
near=[dict(separation_arcsec=float(sep[i]),**rows[i]) for i in np.flatnonzero(sep<360)]
save_json(out/'kostov-crossmatch.json',{'utc':now(),'catalog_rows':len(rows),'selection_sha256':sha(sel),'n_targets':len(targets),'search_radius_arcsec':126,'matches':matches,'tic80387959':{'neighbors_sha256':sha(npth),'n_neighbors':len(neighbors),'exact_neighbor_matches':nmatch,'positional_matches_within360arcsec':near},'limitations':'Catalog absence does not exclude binaries or establish planetary nature/novelty. Coordinates compared at published J2000; no proper-motion propagation.'})
print('matches',len(matches),'exact',sum(m['exact_tic_match'] for m in matches),'803neighbors',nmatch,'803near',near)
for m in matches:
 if m['exact_tic_match'] or m['separation_arcsec']<21:print(m)

# Extend the refresh to the already-completed original search, with both catalogs.
from astropy.coordinates import search_around_sky
combined=[dict(catalog=f"Kostov2025-table{r['catalog_table']}",tic=int(r['TIC']),ra=float(r['RAJ2000']),dec=float(r['DEJ2000']),period=float(r.get('Per',r.get('Per-TESS')))) for r in rows]
combined.extend(dict(catalog='Villanova',**r) for r in json.loads((out/'villanova-parsed.json').read_text()))
original=Path('results/selection-small-stars-20261009/eligible.json')
oldtargets=json.loads(original.read_text())
c1=SkyCoord([t['star']['ra'] for t in oldtargets]*u.deg,[t['star']['dec'] for t in oldtargets]*u.deg)
c2=SkyCoord([r['ra'] for r in combined]*u.deg,[r['dec'] for r in combined]*u.deg)
a,b,sep,_=search_around_sky(c1,c2,126*u.arcsec)
oldmatches=[dict(search_tic=oldtargets[i]['tic'],separation_arcsec=float(s.arcsec),binary=combined[j]) for i,j,s in zip(a,b,sep)]
save_json(out/'original-search-crossmatch.json',{'utc':now(),'selection_sha256':sha(original),'n_targets':len(oldtargets),'radius_arcsec':126,'matches':oldmatches})
