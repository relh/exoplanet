"""Catalog-coordinate diagrams, not observations or host localizations."""
from pathlib import Path
import csv,hashlib,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u
R=Path('results/followup-overview-20261013')
fields=[(80387959,[80387965,80387968,80387961]),(402358350,[1918682563,402358249,74037550])]
fig,axs=plt.subplots(1,2,figsize=(11,5.6),layout='constrained');manifest=[];records=[]
for ax,(tic,ids) in zip(axs,fields):
 p=Path(f'results/triceratops-20261013/{tic}-stars.csv')
 manifest.append(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 rows=list(csv.DictReader(p.open()));target=next(r for r in rows if r['ID']==str(tic));center=SkyCoord(float(target['ra'])*u.deg,float(target['dec'])*u.deg)
 for row in rows:
  sky=SkyCoord(float(row['ra'])*u.deg,float(row['dec'])*u.deg);east,north=center.spherical_offsets_to(sky);x,y=east.arcsec,north.arcsec
  if max(abs(x),abs(y))>65:continue
  ident=int(row['ID']);marked=ident in ids or ident==tic
  ax.scatter(x,y,s=max(8,100*10**(-.17*(float(row['Tmag'])-10))),color='#18785f' if ident==tic else ('#bf5b2b' if marked else '#b9c1c5'),alpha=1 if marked else .6,zorder=3 if marked else 1)
  if marked:
   offset={80387961:(20,-2),80387965:(7,-16),1918682563:(-95,12)}.get(ident,(7,8))
   ax.annotate(str(ident),(x,y),xytext=offset,textcoords='offset points',fontsize=9)
   records.append(dict(field=tic,tic=ident,ra_deg=float(row['ra']),dec_deg=float(row['dec']),east_arcsec=x,north_arcsec=y,separation_arcsec=center.separation(sky).arcsec,Tmag=float(row['Tmag'])))
 ax.axhline(0,color='#dddddd',lw=.6);ax.axvline(0,color='#dddddd',lw=.6)
 ax.set(xlim=(65,-65),ylim=(-65,65),aspect='equal',title=f'TIC {tic}',xlabel='East offset (arcsec; east at left)',ylabel='North offset (arcsec)')
 ax.grid(alpha=.15)
fig.suptitle('Resolved follow-up fields · catalog positions',fontsize=15)
fig.supxlabel('Catalog coordinates, not an image or localization. Brightness sets marker size. Positions require updating for the observing date.',fontsize=9)
fig.savefig(R/'fields.png',dpi=160);plt.close(fig)
(R/'field-coordinates.json').write_text(json.dumps(records,indent=2)+'\n')
(R/'field-provenance.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Wrote',len(records),'highlighted catalog positions')
