import csv,json,math
from pathlib import Path
from astropy.coordinates import SkyCoord
import astropy.units as u
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;provenance=Path('results/novelty-402358350-20261011/queries.json');q=next(x for x in json.loads(provenance.read_text()) if x['name']=='current-ctoi');assert q['status']=='success';raw=Path(q['path']);assert sha(raw)==q['sha256'];rows=list(csv.DictReader(raw.open()));assert len(rows)==q['row_count'];disc=Path('results/solar-radius-ranks5456-5968-20261011/targets/96166003.json');star=json.loads(disc.read_text())['target']['star'];pos=SkyCoord(star['ra'],star['dec'],unit='deg');exact=[];near=[]
for row in rows:
 if int(row['TIC ID'])==96166003:exact.append(row)
 ra,dec=float(row['RA']),float(row['Dec']);sep=pos.separation(SkyCoord(ra,dec,unit='deg')).to_value(u.arcsec)
 a,b,c,d=map(math.radians,[star['ra'],star['dec'],ra,dec]);h=math.sin((d-b)/2)**2+math.cos(b)*math.cos(d)*math.sin((c-a)/2)**2;ind=math.degrees(2*math.asin(math.sqrt(min(1,max(0,h)))))*3600;assert abs(sep-ind)<1e-6
 if sep<=120:near.append(dict(separation_arcsec=float(sep),row=row))
save_json(out/'results.json',dict(checked_utc=now(),tic=96166003,source_url=q['url'],snapshot_retrieved_utc=q['retrieved_utc'],raw_path=str(raw),raw_sha256=sha(raw),provenance_sha256=sha(provenance),discovery_sha256=sha(disc),script_sha256=sha(Path(__file__)),n_catalog_rows=len(rows),exact_matches=exact,within120arcsec=near,coordinate_verification='Astropy and independent haversine agree for every catalog row',limits='Reused dated public CTOI snapshot only; no current target-page, TOI, literature or private-submission completeness claim. Nonmatch is not proof of novelty.'))
print(len(rows),len(exact),len(near))
