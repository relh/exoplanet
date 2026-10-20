from pathlib import Path
import json
from astropy.io import fits
from astropy.wcs import WCS
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;npth=Path('results/neighbors-74189224-20261011/neighbors.json');rows=json.loads(npth.read_text());star=next(s for s in rows if int(s['ID'])==74181772);positions=[]
for sector in (103,104):
 f=json.loads(Path(f'results/tesscut-74189224-s{sector}-20261011/files.json').read_text())[0];assert sha(Path(f['path']))==f['sha256']
 with fits.open(f['path']) as h:x,y=WCS(h[2].header).world_to_pixel_values(star['ra'],star['dec'])
 positions.append({'sector':sector,'x':float(x),'y':float(y),'source_sha256':f['sha256']})
save_json(out/'neighbor-projection.json',{'script_sha256':sha(Path(__file__)),'neighbors_sha256':sha(npth),'tic':74181772,'Tmag':star['Tmag'],'positions':positions,'limits':'Post-hoc position comparison only. Unpropagated TIC coordinate; no variability or unique host inference.'});print(positions)
