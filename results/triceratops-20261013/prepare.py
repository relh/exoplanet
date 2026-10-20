from pathlib import Path
import os,json,hashlib,datetime
import numpy as np,pandas as pd
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from triceratops.triceratops import target
from triceratops.funcs import query_gaia_background
R=Path('results/triceratops-20261013').resolve(); D=Path('data/triceratops-20261013').resolve()
plan=json.loads((R/'plan.json').read_text())
for p,h in plan['inputs'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
for tic,s,cat in [(80387959,36,'results/neighbors-80387959-20261009/tic-neighbors.json'),(402358350,54,'results/neighbors-402358350-20261011/neighbors.json')]:
 a=target.__new__(target);a.ID=tic;a.mission='TESS';a.sectors=np.array([s]);a.search_radius=150/20.25;a.background_population_source='gaia';a.trilegal_url=None
 rows=json.loads(Path(cat).read_text()); star=next(x for x in rows if int(x['ID'])==tic);c0=SkyCoord(star['ra'],star['dec'],unit='deg');df=pd.DataFrame(rows).replace({None:np.nan}); coords=SkyCoord(df.ra.values,df.dec.values,unit='deg');df['sep (arcsec)']=c0.separation(coords).arcsec;df['PA (E of N)']=c0.position_angle(coords).deg;df=df[df['sep (arcsec)']<=150].copy();df['first']=df.ID.astype(int)!=tic;df=df.sort_values(['first','sep (arcsec)']).drop(columns='first').reset_index(drop=True);df.ID=df.ID.astype(str)
 a.stars=df;a.stars.to_csv(R/f'{tic}-stars-original.csv',index=False);a.estimate_stellar_params();
 with fits.open(f'data/lightcurves/s{s:04d}-{tic}.fits') as hd:
  w=WCS(hd[2].header);a.pix_coords=[w.all_world2pix(df[['ra','dec']].values,0)];ap=np.argwhere((hd[2].data&2)>0)[:,::-1];headercrowd=hd[1].header['CROWDSAP']
 arr=np.load(f'results/paper-host-vetting-20261012/{tic}-s{s}-sap.npz');base=arr['design'][:,1:]@arr['beta'][1:];ref=np.mean(arr['beta'][1::2]);flux=1+(arr['flux']-base)/ref;dt=arr['dt'];m=next(x for x in json.loads(Path('results/paper-host-vetting-20261012/results.json').read_text())['measurements'] if x['tic']==tic and x['sector']==s)
 cp=json.loads(Path('results/strongest-80387959-shape-20261012/plan.json' if tic==80387959 else 'results/strongest-402358350-baselines-20261012/plan.json').read_text());clock=cp.get('best',cp.get('clock'));sigma=float(np.std((arr['flux']-base)[abs(dt)>clock['duration']/2]/ref,ddof=1))
 a.calc_depths(m['depth'],[ap],dilution_corrected=False);a.stars.to_csv(R/f'{tic}-stars.csv',index=False)
 np.savez_compressed(R/f'{tic}-input.npz',time=dt,flux=flux,aperture=ap,pix_coords=a.pix_coords[0],error=sigma)
 (R/f'{tic}-input.json').write_text(json.dumps(dict(tic=tic,sector=s,clock=clock,depth=m['depth'],sigma=sigma,exptime=m['exposure_days'],header_crowdsap=headercrowd,modeled_target_fraction=float(a.stars.fluxratio.iloc[0]),n=len(dt)),indent=2))
 print('prepared',tic,len(df),'eligible',sum(a.stars.tdepth>0),sigma,flush=True)
 old=os.getcwd();os.chdir(D)
 try:fn=query_gaia_background(star['ra'],star['dec'],tic,verbose=1)
 finally:os.chdir(old)
 print('background',tic,fn,flush=True)
 if fn:
  path=D/fn;meta=dict(path=str(path.relative_to(R.parents[1])),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),url='https://gea.esac.esa.int/tap-server/tap',query=f'Gaia DR3 field at RA={star["ra"]},Dec={star["dec"]},area=0.1deg2,G<21; v1.1.0 query_gaia_background')
  (R/f'{tic}-background.json').write_text(json.dumps(meta,indent=2))
