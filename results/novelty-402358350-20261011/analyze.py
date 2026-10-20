from pathlib import Path
import csv,json,re,numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
from exoplanet.pipeline import save_json,sha,now
p=Path(__file__).parent;q=json.loads((p/'queries.json').read_text());ct=next(x for x in q if x['name']=='current-ctoi');assert ct['status']=='success';rows=list(csv.DictReader(Path(ct['path']).open()));exact=[x for x in rows if x['TIC ID'].strip()=='402358350'];near=[];parse_errors=[];target=SkyCoord(295.15063723769,15.64029808626,unit='deg')
for i,r in enumerate(rows):
 try:
  pos=SkyCoord(float(r['RA']),float(r['Dec']),unit='deg');sep=float(target.separation(pos).to_value(u.arcsec))
  if sep<=120:near.append(dict(separation_arcsec=sep,row=r))
 except Exception as exc:parse_errors.append(dict(row_index=i,error=repr(exc)))
page=next(x for x in q if x['name']=='target-page');text=Path(page['path']).read_text();assert '<title>ExoFOP TIC 402358350</title>' in text
counts={}
for name,var in [('TOI','rowData'),('CTOI','rowData2'),('planet_parameters','rowData3')]:
 m=re.search(r'var '+var+r' = (\[.*?\]);',text);assert m;parsed=json.loads(m[1]);counts[name]=len(parsed)
prior=[]
for n in ['data/targeting/ctoi.csv','data/catalogs/241928959-ctoi-20261011.csv']:
 f=Path(n);meta=json.loads(Path(n+'.json').read_text());assert sha(f)==meta['sha256'];rs=list(csv.DictReader(f.open()));prior.append(dict(path=n,retrieved_utc=meta['retrieved_utc'],sha256=sha(f),rows=len(rs),exact_tic_matches=[x for x in rs if x['TIC ID'].strip()=='402358350']))
save_json(p/'results.json',dict(created_utc=now(),script_sha256=sha(Path(__file__)),ctoi_rows=len(rows),ctoi_exact_tic_matches=exact,ctoi_within120arcsec=near,coordinate_parse_errors=parse_errors,target_page_counts=counts,target_page_confirmed_planet_na=bool(re.search(r'Confirmed Planet\(s\):\s*N/A',text)),prior_snapshots=prior,source_hashes={x['path']:x['sha256'] for x in q if 'path' in x},limitations='Public catalog/page nonmatches, not a proof of novelty or exhaustive literature review.'))
print('CTOI',len(rows),'exact',len(exact),'near',len(near),'parseerrors',len(parse_errors),'page',counts)
