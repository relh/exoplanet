"""Compare reference positions and audit potential repeated observations."""
from pathlib import Path
import json,numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
from exoplanet.pipeline import save_json,sha
p=Path(__file__).parent;source=Path('results/ztf-cloud-20261011/results.json');r=json.loads(source.read_text());catalog=Path('results/ztf-catalog-route-20261011/catalog-results.json');lookup={int(x['oid']):y['tic'] for y in json.loads(catalog.read_text()) for x in y['rows']}
gids={422626648:'6254811248843788416',241928959:'6865254022910168320',196681132:'3611756510240137088'}
rows=[];measurements={};inputs={str(source):sha(source),str(catalog):sha(catalog),str(Path(__file__)):sha(Path(__file__))}
for item in r['objects']:
 file=Path(item['path']);assert sha(file)==item['sha256'];inputs[str(file)]=sha(file);o=json.loads(file.read_text());tic=lookup[o['objectid']]
 gp=Path(f'results/gaia-{tic}-scene-20261011/gaia_source.json');inputs[str(gp)]=sha(gp);gaia=json.loads(gp.read_text());point=SkyCoord(o['objra']*u.deg,o['objdec']*u.deg)
 scene=[]
 for g in gaia:
  c=SkyCoord(float(g['ra'])*u.deg,float(g['dec'])*u.deg);sep=float(point.separation(c).arcsec)
  scene.append({'source_id':g['source_id'],'separation_at_gaia_reference_arcsec':sep,'ref_epoch':float(g['ref_epoch'])})
 scene.sort(key=lambda x:x['separation_at_gaia_reference_arcsec']);target=next(g for g in gaia if g['source_id']==gids[tic])
 # ZTF objra/objdec describe a coadded reference; its effective epoch is not provided.
 # Propagation is only a range diagnostic and not a per-exposure astrometric test.
 years=np.arange(2016,2027);dt=years-float(target['ref_epoch']);dec=float(target['dec']);ra=float(target['ra'])
 coords=SkyCoord((ra+dt*float(target['pmra'])/(3600000*np.cos(np.deg2rad(dec))))*u.deg,(dec+dt*float(target['pmdec'])/3600000)*u.deg)
 separations=point.separation(coords).arcsec
 good=[x for x in o['lightcurve'] if x['catflags']==0 and all(x[k] is not None and np.isfinite(x[k]) for k in ['hmjd','mag','magerr']) and x['magerr']>0]
 measurements.setdefault(tic,[]).extend({'oid':o['objectid'],'band':o['filterid'],'hmjd':x['hmjd']} for x in good)
 rows.append({'tic':tic,'oid':o['objectid'],'target_gaia':gids[tic],'nearest_gaia':scene[:3],'target_is_nearest_at_reference_epoch':scene[0]['source_id']==gids[tic],'target_propagation_years':years.tolist(),'target_separation_arcsec':separations.tolist(),'n_good':len(good)})
duplicates=[]
for tic,data in measurements.items():
 pairs=[]
 for band in sorted({x['band'] for x in data}):
  group=sorted([x for x in data if x['band']==band],key=lambda x:x['hmjd'])
  for i,a in enumerate(group):
   for b in group[i+1:]:
    delta=(b['hmjd']-a['hmjd'])*86400
    if delta>2:break
    pairs.append({'first':a,'second':b,'seconds_apart':delta})
 duplicates.append({'tic':tic,'n_good':len(data),'same_band_pairs_within_2_seconds':pairs})
save_json(p/'results.json',{'inputs':inputs,'objects':rows,'duplicate_checks':duplicates,'limits':'Compared only returned Gaia scene entries. ZTF positions are reference-image coordinates with unknown effective epoch, not per-exposure positions. Linear proper motion without parallax; no blend exclusion. Same-band close-time pairs are potential duplicates, not proof of shared exposure; no observations removed.'})
print('target nearest',sum(x['target_is_nearest_at_reference_epoch'] for x in rows),'/',len(rows));print([(x['tic'],len(x['same_band_pairs_within_2_seconds'])) for x in duplicates])
