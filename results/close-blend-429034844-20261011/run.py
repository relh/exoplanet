"""Catalog geometry and illustrative two-star dilution, not a PRF/orbit fit."""
from pathlib import Path
import json,math,csv
from astropy.coordinates import SkyCoord
import astropy.units as u
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());nb=Path('results/neighbors-429034844-20261011/neighbors.json');gp=Path('results/gaia-429034844-scene-20261011/gaia_source.json');mp=gp.with_name('dr2_neighbourhood.json');dp=Path('results/joint-clock-fine-429034844-20261011/results.json')
stars=[next(r for r in read(nb) if int(r['ID'])==tic) for tic in [429034844,611135702]];gaia=[]
for s in stars:
 m=[r for r in read(mp) if r['dr2_source_id']==str(s['GAIA'])];assert len(m)==1
 gaia.append(next(r for r in read(gp) if r['source_id']==m[0]['dr3_source_id']))
a,b=gaia;coord=lambda r:SkyCoord(float(r['ra'])*u.deg,float(r['dec'])*u.deg)
sep=coord(a).separation(coord(b)).arcsec;dt=float(stars[1]['Tmag'])-float(stars[0]['Tmag']);ratio=10**(-.4*dt);fraction=ratio/(1+ratio)
depths=[{'sector':r['sector'],'parity':p['parity'],'observed_box_depth':p['measurement']['total']['depth'],'neighbor_only_intrinsic_depth_equal_throughput':p['measurement']['total']['depth']/fraction} for r in read(dp)['rows'] for p in r['parities']]
fields=['source_id','ra','dec','parallax','parallax_error','pmra','pmra_error','pmdec','pmdec_error','phot_g_mean_mag','ruwe','astrometric_params_solved','radial_velocity','grvs_mag']
r={'inputs':{str(p):sha(p) for p in [nb,gp,mp,dp]},'script_sha256':sha(Path(__file__)),'tic_ids':[429034844,611135702],'gaia_rows':[{k:r[k] for k in fields} for r in gaia],'gaia_separation_arcsec':sep,'tic_separation_arcsec':coord(stars[0]).separation(coord(stars[1])).arcsec,'gaia_separation_nominal_21arcsec_pixels':sep/21,'parallax_difference_mas':float(b['parallax'])-float(a['parallax']),'parallax_difference_formal_error_mas':math.hypot(float(a['parallax_error']),float(b['parallax_error'])),'proper_motion_difference_mas_per_year':{k:float(b[k])-float(a[k]) for k in ['pmra','pmdec']},'tic_delta_Tmag':dt,'illustrative_neighbor_to_target_flux_ratio':ratio,'illustrative_neighbor_flux_fraction':fraction,'depth_scenarios':depths,'limits':'Equal-throughput two-star mixing using catalog T magnitudes. Not aperture calibration; excludes additional flux, variability/color uncertainty and pipeline dilution corrections. Gaia separation at catalog epoch; no proper-motion propagation or bound-pair/orbital claim. No RVS scan geometry or per-epoch contamination model.'}
save_json(out/'results.json',r);print({k:v for k,v in r.items() if k not in ['gaia_rows','inputs']})
