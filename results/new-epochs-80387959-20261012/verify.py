from pathlib import Path
import json,hashlib,datetime,numpy as np
from astropy.io import fits
O=Path(__file__).parent;load=lambda n:json.loads((O/n).read_text());sha=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest();p=load('plan.json');geo=load('geometry.json');meta=load('metadata.json');assert sha(meta['path'])==meta['sha256'];assert meta['status']=='success';assert len(meta['rows'])==meta['paging']['rowsFiltered'];assert load('history-audit.json')['matching_raw_paths']==[];doc=load('geometry-source.json');assert sha(doc['path'])==doc['sha256'];assert Path(doc['path']).read_bytes().startswith(b'%PDF');frozen=datetime.datetime.fromisoformat(p['frozen_utc']);checks=[]
for row in geo['rows']:
 sector=row['sector'];s=load(f'source-s{sector}.json');assert datetime.datetime.fromisoformat(s['started_utc'])>frozen;assert s['plan_sha256']==sha(O/'plan.json');assert sha(s['path'])==s['sha256'];f=s['files'][0];assert sha(f['path'])==f['sha256']==row['raw_sha256']
 with fits.open(f['path']) as h:
  assert h[0].header['SECTOR']==sector;assert h[1].header['TIMESYS']=='TDB' and h[1].header['BJDREFI']==2457000
  a=h[2].header;ra,de,ra0,de0=np.deg2rad([p['ra'],p['dec'],a['CRVAL1'],a['CRVAL2']]);den=np.sin(de0)*np.sin(de)+np.cos(de0)*np.cos(de)*np.cos(ra-ra0);tan=np.rad2deg([np.cos(de)*np.sin(ra-ra0)/den,(np.cos(de0)*np.sin(de)-np.sin(de0)*np.cos(de)*np.cos(ra-ra0))/den]);cd=np.array([[a['PC1_1'],a['PC1_2']],[a['PC2_1'],a['PC2_2']]]);pix=np.linalg.solve(cd,tan)+[a['CRPIX1']-1,a['CRPIX2']-1];assert np.allclose(pix,row['pixel_xy_zero_based'],atol=1e-6,rtol=0);hdr=h[1].header;phys=pix+[hdr['1CRV5P'],hdr['2CRV5P']];assert np.allclose(phys,row['physical_raw_xy'],atol=1e-6,rtol=0);assert phys[0]+2.5<44.5
  for ap in row['apertures']:
   assert ap['science_pixels']==0;assert ap['max_rawx']<45
  hdus=[dict(hdu=i,checksum=int(v.verify_checksum()),datasum=int(v.verify_datasum())) for i,v in enumerate(h)];assert all(v['checksum']==1 and v['datasum']==1 for v in hdus);checks.append(dict(sector=sector,manual_tangent_projection_raw_xy=phys.tolist(),all_apertures_outside_science=True,hdus=hdus))
# Retain arithmetic checks of invalid calculations, without treating them as stellar data.
for f in O.glob('fit-s*.npz'):
 z=np.load(f);X=z['X']/z['E'][:,None];y=z['Y']/z['E'];coef=np.linalg.solve(X.T@X,X.T@y);assert np.allclose(coef,z['beta'],atol=1e-9,rtol=0)
(O/'verification.json').write_text(json.dumps(dict(status='passed',checks=checks,scope='Hash/provenance/timestamp/schema checks; independent manual tangent-plane sky-to-pixel projection; physical RAWX check and FITS checksums; normal-equation verification of preserved invalid-aperture fits. Establishes unusable geometry, not astrophysical non-recurrence.'),indent=2)+'\n');print((O/'verification.json').read_text())
