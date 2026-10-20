from pathlib import Path
import json,hashlib,datetime,os
import numpy as np,pandas as pd
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from triceratops.triceratops import target
from triceratops.funcs import query_gaia_background
R=Path('results/triceratops-20261013').resolve();D=Path('data/triceratops-20261013').resolve();plan=json.loads((R/'control-plan.json').read_text())
for p,h in plan['inputs'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
clock=json.loads(Path('results/strongest-host-identifiability-20261012/plan.json').read_text())['cases'][0]['clock'];P=clock['period'];DUR=clock['duration'];T=clock['transit_time'];tic=137151335;s=40
with fits.open(f'data/lightcurves/s{s:04d}-{tic}.fits') as h:
 z=h[1].data;good=(z['QUALITY']==0)&np.isfinite(z['TIME'])&np.isfinite(z['SAP_FLUX'])&np.isfinite(z['SAP_FLUX_ERR'])&(z['SAP_FLUX']>0)&(z['SAP_FLUX_ERR']>0);t=z['TIME'][good];y=z['SAP_FLUX'][good].astype(float);err=z['SAP_FLUX_ERR'][good].astype(float);norm=np.median(y);y/=norm;err/=norm;exp=float(np.median(np.diff(t)));event=np.rint((t-T)/P).astype(int);dt=t-(T+event*P)
 cases=[int(e) for e in np.unique(event) if np.sum((event==e)&(abs(dt)<DUR/2))>=2 and np.sum((event==e)&(dt<-DUR/2)&(dt>-3*DUR))>=5 and np.sum((event==e)&(dt>DUR/2)&(dt<3*DUR))>=5];m=np.isin(event,cases)&(abs(dt)<3*DUR);t,y,err,dt,event=[v[m] for v in [t,y,err,dt,event]];box=np.maximum(0,np.minimum(dt+exp/2,DUR/2)-np.maximum(dt-exp/2,-DUR/2))/exp;X=np.zeros((len(t),1+2*len(cases)));X[:,0]=-box
 for j,e in enumerate(cases):X[:,1+2*j]=event==e;X[:,2+2*j]=(event==e)*dt/DUR
 beta=np.linalg.lstsq(X/err[:,None],y/err,rcond=None)[0];base=X[:,1:]@beta[1:];ref=np.mean(beta[1::2]);flux=1+(y-base)/ref;depth=beta[0]/ref;sigma=float(np.std((y-base)[abs(dt)>DUR/2]/ref,ddof=1));w=WCS(h[2].header);ap=np.argwhere((h[2].data&2)>0)[:,::-1];crowd=h[1].header['CROWDSAP']
rows=json.loads(Path('results/neighbors-137151335-20261011/neighbors.json').read_text());star=next(x for x in rows if int(x['ID'])==tic);c0=SkyCoord(star['ra'],star['dec'],unit='deg');df=pd.DataFrame(rows).replace({None:np.nan});coords=SkyCoord(df.ra.values,df.dec.values,unit='deg');df['sep (arcsec)']=c0.separation(coords).arcsec;df['PA (E of N)']=c0.position_angle(coords).deg;df=df[df['sep (arcsec)']<=150].copy();df['first']=df.ID.astype(int)!=tic;df=df.sort_values(['first','sep (arcsec)']).drop(columns='first').reset_index(drop=True);df.ID=df.ID.astype(str)
a=target.__new__(target);a.ID=tic;a.mission='TESS';a.stars=df;a.stars.to_csv(R/f'{tic}-stars-original.csv',index=False);a.estimate_stellar_params();a.pix_coords=[w.all_world2pix(df[['ra','dec']].values,0)];a.calc_depths(depth,[ap],dilution_corrected=False);a.stars.to_csv(R/f'{tic}-stars.csv',index=False);np.savez_compressed(R/f'{tic}-input.npz',time=dt,flux=flux,aperture=ap,pix_coords=a.pix_coords[0],error=sigma);(R/f'{tic}-input.json').write_text(json.dumps(dict(tic=tic,sector=s,clock=clock,depth=depth,sigma=sigma,exptime=exp,header_crowdsap=crowd,modeled_target_fraction=float(a.stars.fluxratio.iloc[0]),n=len(dt),events=cases),indent=2));print('prepared',tic,len(df),sum(a.stars.tdepth>0),sigma,flush=True)
old=os.getcwd();os.chdir(D)
try:fn=query_gaia_background(star['ra'],star['dec'],tic,verbose=1)
finally:os.chdir(old)
if fn:
 path=D/fn;meta=dict(path=str(path.relative_to(R.parents[1])),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),url='https://gea.esac.esa.int/tap-server/tap',query=f'Gaia DR3 at RA={star["ra"]},Dec={star["dec"]},area0.1deg2,G<21;v1.1.0query_gaia_background');(R/f'{tic}-background.json').write_text(json.dumps(meta,indent=2))
