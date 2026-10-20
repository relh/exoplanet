from pathlib import Path
import csv,json,numpy as np
from exoplanet.pipeline import sha,save_json,now
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());r=json.loads((p/'results.json').read_text());meta=json.loads((p/'ztf-metadata.json').read_text())
assert sha(p/'query.py')==plan['script_sha256'];assert sha(Path(plan['frozen_path']))==plan['frozen_sha256'];f=json.loads(Path(plan['frozen_path']).read_text());v=next(x for x in f['rows'] if x['role']=='primary');assert v['best']==plan['clock'] and v['ranges']==plan['timing_ranges']
for name,d in r['inputs'].items():assert sha(Path(name))==d
assert meta['status']=='success' and sha(Path(meta['path']))==meta['sha256'];rows=list(csv.DictReader(Path(meta['path']).open()));assert rows==meta['rows'] and len(rows)==r['ztf_rows']<1000
gp=Path('results/gaia-402358350-scene-20261011');gaia=json.loads((gp/'gaia_source.json').read_text());source=json.loads((gp/'gaia_source-source.json').read_text());raw=Path('data/catalogs/gaia-402358350-scene-gaia_source-20261011.csv');assert sha(raw)==source['sha256'];assert list(csv.DictReader(raw.open()))==gaia;g=next(x for x in gaia if x['source_id']==r['target_gaia']['source_id']);assert g['has_epoch_photometry']=='false' and r['gaia_query_retrieved_utc']==source['retrieved_utc']
epochs=np.linspace(2018,2027,901);dec0=float(g['dec']);ra=float(g['ra'])+(epochs-float(g['ref_epoch']))*float(g['pmra'])/(3600000*np.cos(np.deg2rad(dec0)));dec=dec0+(epochs-float(g['ref_epoch']))*float(g['pmdec'])/3600000
for row in rows:
 a,b=np.deg2rad(float(row['ra'])),np.deg2rad(float(row['dec']));ar,br=np.deg2rad(ra),np.deg2rad(dec);hv=np.sin((br-b)/2)**2+np.cos(br)*np.cos(b)*np.sin((ar-a)/2)**2;sep=np.rad2deg(2*np.arcsin(np.sqrt(hv)))*3600;x=next(x for x in r['rows'] if x['oid']==row['oid']);np.testing.assert_allclose(sep.min(),x['min_track_separation_arcsec'],atol=2e-7);assert int(row['nobs'])==x['nobs'] and int(row['ngoodobs'])==x['ngoodobs']
assert r['target_associated_oids']==[x['oid'] for x in r['rows'] if x['min_track_separation_arcsec']<=3]==[]
save_json(p/'verification.json',dict(status='passed',utc=now(),ztf_metadata_rows=len(rows),independent_separation_tracks=49,gaia_source_rows=len(gaia),frozen_clock_unchanged=True,lightcurve_measurements=0,reason='No secure target ZTF association and Gaia target epoch availability false',limits='Catalog/association arithmetic audit, not proof of no survey exposures, transit exclusion or absolute blend identification.'))
