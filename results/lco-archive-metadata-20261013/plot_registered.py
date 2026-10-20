import json,pathlib,numpy as np
from astropy.io import fits
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=pathlib.Path('results/lco-archive-metadata-20261013');out=json.load(open(R/'registered-feasibility.json'));fig,axes=plt.subplots(1,2,figsize=(12,6),layout='constrained')
for ax,r in zip(axes,out['results']):
 with fits.open(r['file']) as f:
  im=f['SCI'].data;ylo,yhi=1800,1980;xlo,xhi=1020,1240;crop=im[ylo:yhi,xlo:xhi];ax.imshow(np.arcsinh((crop-np.nanmedian(crop))/500),origin='lower',extent=(xlo,xhi,ylo,yhi),cmap='gray',vmin=0,vmax=5)
 for s in r['sources']:
  x,y=s['registered_x0'],s['registered_y0'];ax.scatter(x,y,s=100,facecolors='none',edgecolors='tab:orange');offset={80387959:(18,-32),80387961:(-68,-20),937808821:(18,-8),80387965:(15,12),80387968:(-32,20)}[s['tic']];ax.annotate(str(s['tic']), (x,y), xytext=offset,textcoords='offset points',color='tab:orange',fontsize=8,arrowprops={'arrowstyle':'-','color':'tab:orange','lw':0.7})
 ax.set_title(pathlib.Path(r['file']).name+'\nRegistered baseline image; no predicted transit',fontsize=10);ax.set_xlabel('Science pixel x');ax.set_ylabel('Science pixel y')
fig.savefig(R/'registered-baseline-images.png',dpi=140)
