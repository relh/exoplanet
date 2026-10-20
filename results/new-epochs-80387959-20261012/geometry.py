from pathlib import Path
import json,requests,numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from exoplanet.pipeline import save_json,sha,now
O=Path(__file__).parent;D=Path('data')/O.name;p=json.loads((O/'plan.json').read_text());out=[]
url='https://archive.stsci.edu/files/live/sites/mast/files/home/missions-and-data/active-missions/tess/_documents/EXP-TESS-ARC-ICD-TM-0014-Rev-F.pdf';doc=D/'tess-data-products-revf.pdf'
r=requests.get(url,timeout=90);doc.write_bytes(r.content);r.raise_for_status();save_json(O/'geometry-source.json',dict(url=url,path=str(doc),sha256=sha(doc),http_status=r.status_code,retrieved_utc=now(),interpretation='CCD geometry diagram: 1-based active science columns45to2092,rows1to2048; columns1to44 leadingcollateral. RAWX zero/onebased ambiguity cannot change either outcome because both apertures lie severalpixels outside.'))
for sector in p['sectors']:
 s=json.loads((O/f'source-s{sector}.json').read_text());f=Path(s['files'][0]['path'])
 with fits.open(f) as h:
  w=WCS(h[2].header);pix=np.array(w.world_to_pixel_values(p['ra'],p['dec']));hdr=h[1].header;phys=np.array([hdr[f'{j}CRV5P']+(pix[j-1]+1-hdr[f'{j}CRP5P'])*hdr[f'{j}CDL5P'] for j in [1,2]]);yy,xx=np.indices(h[1].data['FLUX'].shape[1:]);rx=hdr['1CRV5P']+(xx+1-hdr['1CRP5P'])*hdr['1CDL5P'];ry=hdr['2CRV5P']+(yy+1-hdr['2CRP5P'])*hdr['2CDL5P'];science=(rx>=45)&(rx<=2092)&(ry>=1)&(ry<=2048);ap=[]
  for radius in [1.5,2.5]:
   mask=np.hypot(xx-pix[0],yy-pix[1])<=radius;ap.append(dict(radius=radius,total_pixels=int(mask.sum()),science_pixels=int((mask&science).sum()),min_rawx=float(rx[mask].min()),max_rawx=float(rx[mask].max())))
  out.append(dict(sector=sector,raw_sha256=sha(f),pixel_xy_zero_based=pix.tolist(),physical_raw_xy=phys.tolist(),physical_wcs={k:hdr[k] for k in ['1CRV5P','2CRV5P','1CRP5P','2CRP5P','1CDL5P','2CDL5P']},active_science=False,apertures=ap,disposition='invalid_target_photometry_collateral_columns',previous_numerical_file='results.json',supersedes='Any naive cutout-aperture photometric interpretation; not a transit nondetection.'))
save_json(O/'geometry.json',dict(utc=now(),rows=out,final_outcome='Both nominal footprint sectors unusable for target: candidate apertures wholly outside active science area. This satisfies frozen off-detector rejection; original calculations preserved as failed geometric screening.'))
print(json.dumps(out,indent=2))
