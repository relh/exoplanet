import re,json
from pathlib import Path
from urllib.parse import urljoin
from astropy.io import fits
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent;models=[]
for sector in [91]:
 p=Path('data/pixels/tess-s0091-1-1_202.641615_-10.555397_11x11_astrocut.fits')
 with fits.open(p) as h:
  cam,ccd=h[0].header['CAMERA'],h[0].header['CCD'];shape=h[1].data['FLUX'].shape[1:]
  x0=h[2].header.get('CRVAL1P',h[1].header.get('1CRV5P'));y0=h[2].header.get('CRVAL2P',h[1].header.get('2CRV5P'));x=x0+(shape[1]-1)/2;y=y0+(shape[0]-1)/2
 url=f'https://archive.stsci.edu/missions/tess/models/prf_fitsfiles/start_s0004/cam{cam}_ccd{ccd}/';index=Path(f'data/prf/cam{cam}_ccd{ccd}.html');directory_source=fetch(url,index)
 names=re.findall(r'href="([^"]+\.fits)"',index.read_text());coords=[]
 for name in names:
  match=re.search(r'row(\d+)-col(\d+)\.fits',name)
  if match and 'phot' not in name:coords.append((int(match[2]),int(match[1]),name))
 selected=[]
 for sx,sy in [(-1,-1),(-1,1),(1,-1),(1,1)]:
  candidates=[c for c in coords if (c[0]-x)*sx>0 and (c[1]-y)*sy>0];assert candidates
  col,row,name=min(candidates,key=lambda c:(c[0]-x)**2+(c[1]-y)**2);dest=Path(f'data/prf/start_s0004/cam{cam}_ccd{ccd}')/Path(name).name
  source=fetch(urljoin(url,name),dest);selected.append({'grid_col':col,'grid_row':row,'path':str(dest),'source':source})
 models.append({'sector':sector,'camera':cam,'ccd':ccd,'col':x,'row':y,'pixel_path':str(p),'pixel_sha256':sha(p),'directory_source':directory_source,'models':selected})
 save_json(out/'models.json',{'created_utc':now(),'script_sha256':sha(Path(__file__)),'sectors':models})
 print(sector,len(selected),flush=True)
