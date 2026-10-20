from pathlib import Path
import json,numpy as np
from astropy.io import fits
from astropy.time import Time
from astropy.wcs import WCS
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(out/'plan.json');maps=read(out/'dr2_neighbourhood.json');sources={r['source_id']:r for r in read(out/'gaia_source.json')};pixel=Path('data/pixels/156001092-s0069.fits')
with fits.open(pixel) as h:
 t=np.asarray(h[1].data['TIME']);year=Time(2457000+np.nanmedian(t),format='jd').jyear;w=WCS(h[2].header)
rows=[]
for star in plan['targets']:
 ms=[m for m in maps if m['dr2_source_id']==str(star.get('GAIA'))];row={'tic':star['ID'],'dr2':star.get('GAIA'),'mappings':[]}
 for m in ms:
  s=sources.get(m['dr3_source_id']);item={'mapping':m,'source_available':s is not None}
  if s:
   fields=['ra','dec','pmra','pmdec','ref_epoch'];usable=all(s.get(k) not in [None,''] for k in fields);item['proper_motion_available']=usable
   if usable:
    ra,dec,pmra,pmdec,epoch=[float(s[k]) for k in fields];dt=year-epoch;position=[ra+dt*pmra/(3600000*np.cos(np.deg2rad(dec))),dec+dt*pmdec/3600000];xy=np.array(w.world_to_pixel_values(*position));old=np.array(w.world_to_pixel_values(star['ra'],star['dec']));item.update(propagated_radec=position,propagated_xy=xy.tolist(),pixel_displacement_from_tic=(xy-old).tolist(),displacement_pixels=float(np.linalg.norm(xy-old)))
  row['mappings'].append(item)
 row['unique_complete_mapping']=len(ms)==1 and bool(row['mappings'][0].get('proper_motion_available'))
 rows.append(row)
for table in ['dr2_neighbourhood','gaia_source','vari_classifier_result','vari_eclipsing_binary']:
 src=read(out/f'{table}-source.json');assert sha(Path(f'data/catalogs/gaia-156001092-scene-{table}-20261011.csv'))==src['sha256']
save_json(out/'astrometry-audit.json',{'script_sha256':sha(Path(__file__)),'query_script_sha256':sha(out/'query.py'),'pixel_sha256':sha(pixel),'epoch_jyear':float(year),'inputs':{str(out/n):sha(out/n) for n in ['plan.json','dr2_neighbourhood.json','gaia_source.json','vari_classifier_result.json','vari_eclipsing_binary.json']},'rows':rows,'limits':'All mappings retained, including distant or ambiguous links. Linear proper-motion propagation ignores parallax/radial perspective. Unique mapping does not itself certify crossmatch; missing Gaia is not missing star or variability exclusion.'});print([(r['tic'],len(r['mappings']),[i.get('displacement_pixels') for i in r['mappings']]) for r in rows])
