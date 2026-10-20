from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
out=Path(__file__).parent
for sector,n in [(63,345),(90,519),(90,522)]:
 z=np.load(out/f's{sector}-event{n}.npz')
 hosts=['80387959','80387965','80387961','937808821']
 fig,axes=plt.subplots(1,5,figsize=(16,3.5),constrained_layout=True)
 ims=[z['difference']/z['error']]+[(z['difference']-z['model_'+h])/z['error'] for h in hosts]
 for ax,im,title in zip(axes,ims,['Difference / error']+[h+' residual / error' for h in hosts]):
  a=ax.imshow(im,origin='lower',cmap='coolwarm',vmin=-5,vmax=5);fig.colorbar(a,ax=ax,shrink=.7);ax.set_title(title,fontsize=9)
 fig.suptitle(f'Sector{sector} event{n}: fixed models, formal errors, not calibrated confidence')
 fig.savefig(out/f's{sector}-event{n}.png',dpi=140);plt.close(fig)
