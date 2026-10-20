from pathlib import Path
import json,numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from exoplanet.pipeline import sha,save_json
from exoplanet.pixel_vet import difference_events,centroid
for tic,sectors in [(30832104,[9])]:
 fp=Path(f'results/refinement-{tic}-20261011/frozen.json');b=json.loads(fp.read_text())['best']
 npth=Path(f'results/neighbors-{tic}-20261011');meta=json.loads((npth/'source.json').read_text());raw=Path(f'data/catalogs/neighbors-{tic}-20261011.json');assert sha(raw)==meta['sha256'];stars=json.loads((npth/'neighbors.json').read_text())
 assert json.loads(raw.read_text())['data']==stars
 for sector in sectors:
  p=Path(f'results/pixels-{tic}-s{sector}-20261011');r=json.loads((p/'localization.json').read_text());raw=Path(f'data/pixels/{tic}-s{sector:04d}.fits');assert sha(raw)==r['source']['sha256'];assert sha(fp)==r['frozen_sha256']
  with fits.open(raw) as h:
   assert h[0].header['TICID']==tic and h[0].header['SECTOR']==sector
   a=h[1].data;t=np.asarray(a['TIME'],float);ok=np.isfinite(t);wcs=WCS(h[2].header);f=np.asarray(a['FLUX'][ok],float);e=np.asarray(a['FLUX_ERR'][ok],float)
   diff,sigma,events,ns=difference_events(t[ok],f,e,a['QUALITY'][ok],b)
   z=np.load(p/'images.npz');np.testing.assert_allclose(z['difference'],diff);np.testing.assert_allclose(z['error'],sigma);np.testing.assert_allclose(z['event_differences'],events)
   assert ns==r['event_numbers'];peak=np.unravel_index(np.argmax(diff/sigma),diff.shape);assert list(peak[::-1])==r['difference_peak_xy'];moment=centroid(diff,peak[::-1]);np.testing.assert_allclose(moment,r['difference_moment_xy'])
   for n in r['neighbors_by_distance']:
    star=next(s for s in stars if s['ID']==n['tic']);x,y=wcs.world_to_pixel_values(star['ra'],star['dec']);np.testing.assert_allclose([x,y],[n['x'],n['y']])
  save_json(p/'verification.json',dict(status='passed',raw_hash_and_fits_identity_checked=True,neighbor_catalog_hash_checked=True,images_reconstructed=True,neighbor_positions_reconstructed=True,limits='Same image routine reapplied to raw data; moments uncalibrated and catalog positions unpropagated.'))
  print(tic,sector,'verified')
