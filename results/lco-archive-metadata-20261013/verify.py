import json,pathlib,hashlib
import numpy as np
from astropy.io import fits
R=pathlib.Path('results/lco-archive-metadata-20261013');checks=0
for s in json.load(open(R/'sources.json')):
 if 'path' in s:assert hashlib.sha256(pathlib.Path(s['path']).read_bytes()).hexdigest()==s['sha256'];checks+=1
for tic in [80387959,402358350]:
 a=json.load(open(R/f'{tic}-j2016-paginated.json'));b=json.load(open(R/f'{tic}-j2027-paginated.json'));assert {r['id'] for r in a['records']}=={r['id'] for r in b['records']};checks+=1
 for x in [a,b]:assert x['pages'][-1]['n']==0 and len({r['id'] for r in x['records']})==x['unique_ids'];checks+=1
for r in json.load(open(R/'803-timing.json'))['records']:
 assert not r['overlaps_full_profile'];assert r['btjd_end']<r['full_profile_dip_start_btjd'] or r['btjd_start']>r['full_profile_dip_end_btjd'];checks+=2
for r in json.load(open(R/'registered-feasibility.json'))['results']:
 with fits.open(r['file']) as f:
  for s in r['sources']:
   x,y=s['registered_x0'],s['registered_y0'];vals=[];masks=[]
   for iy in range(round(y)-6,round(y)+7):
    for ix in range(round(x)-6,round(x)+7):
     if (ix-x)**2+(iy-y)**2<36:vals.append(f['SCI'].data[iy,ix]);masks.append(f['BPM'].data[iy,ix])
   assert len(vals)==s['aperture_pixels'];assert sum(v>=f['SCI'].header['SATURATE'] for v in vals)==s['pixels_above_saturate'];assert sum(v!=0 for v in masks)==s['bad_mask_pixels'];checks+=3
(R/'verification.json').write_text(json.dumps({'status':'pass','checks':checks,'scope':'Raw hashes, query-set identity and pagination terminalpages, saved timinginterval arithmetic, scalar saturation/mask recounts. Does not independently validate affine matching, timeconversion, archive completeness, or planetary status.'},indent=2)+'\n');print(checks)
