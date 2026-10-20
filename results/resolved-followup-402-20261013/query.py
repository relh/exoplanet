from pathlib import Path
import requests,json,csv,hashlib,datetime,concurrent.futures
p=Path(__file__).parent; root=Path('data/resolved-followup-402-20261013')
queries=[('gaia','https://gea.esac.esa.int/tap-server/tap/sync',"SELECT source_id,ra,dec,ref_epoch,pmra,pmdec,parallax,parallax_error,ruwe,phot_g_mean_mag,phot_variable_flag,has_epoch_photometry,radial_velocity,radial_velocity_error FROM gaiadr3.gaia_source WHERE source_id IN (4318715445843282432,4318716236117290496,4318715445843296256)"),('gaia_scene','https://gea.esac.esa.int/tap-server/tap/sync',"SELECT source_id,ra,dec,phot_g_mean_mag FROM gaiadr3.gaia_source WHERE 1=CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',295.156702012357,15.636309028594,0.001388888889))"),('simbad','https://simbad.cds.unistra.fr/simbad/sim-tap/sync',"SELECT b.oid,b.main_id,b.ra,b.dec,b.otype,i.id FROM basic b JOIN ident i ON i.oidref=b.oid WHERE b.oid IN (SELECT oidref FROM ident WHERE id IN ('TIC 74037550','Gaia DR3 4318715445843282432','2MASS J19403761+1538106'))"),('ztf','https://irsa.ipac.caltech.edu/TAP/sync',"SELECT TOP 1000 * FROM ztf_objects_dr24 WHERE 1=CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',295.156702012357,15.636309028594,0.001388888889))")]
def get(item):
 name,url,q=item; rec=dict(name=name,query=q,requested_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  r=requests.get(url,params=dict(REQUEST='doQuery',LANG='ADQL',FORMAT='csv',QUERY=q,MAXREC=1000),timeout=45);raw=root/f'{name}.csv';raw.write_bytes(r.content);rec.update(url=r.url,path=str(raw),sha256=hashlib.sha256(r.content).hexdigest(),http_status=r.status_code);r.raise_for_status();reader=csv.DictReader(r.text.splitlines());assert reader.fieldnames and len(reader.fieldnames)>1;rec.update(status='success',rows=list(reader),columns=reader.fieldnames)
 except Exception as e:rec.update(status='error',error=repr(e))
 (p/f'{name}.json').write_text(json.dumps(rec,indent=2)+'\n');print(name,rec['status'],len(rec.get('rows',[])),flush=True)
if __name__=='__main__':
 plan=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Metadata-only exact-source availability for TIC74037550, plus exact target/pulsator astrometry. No new flux. Freeze separate plan if justified.',queries=queries,source_catalog='results/triceratops-20261013/402358350-stars.csv')
 plan['source_sha256']=hashlib.sha256(Path(plan['source_catalog']).read_bytes()).hexdigest()
 assert not (p/'plan.json').exists();(p/'plan.json').write_text(json.dumps(plan,indent=2)+'\n')
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(get,queries))
