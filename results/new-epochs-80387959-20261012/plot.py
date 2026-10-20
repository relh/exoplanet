from pathlib import Path
import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent;r=json.loads((O/'results.json').read_text());fig,axs=plt.subplots(2,2,figsize=(12,8),constrained_layout=True)
for a,row in zip(axs,r['rows']):
 z=np.load(O/f'image-s{row["sector"]}.npz');im=z['median'];v=np.nanpercentile(im,[5,95]);a[0].imshow(im,origin='lower',vmin=v[0],vmax=v[1]);x,y=z['target_xy'];a[0].plot(x,y,'rx');
 for rad in [1.5,2.5,4,6]:a[0].add_patch(plt.Circle((x,y),rad,fill=False,color='red' if rad<3 else 'orange'))
 a[0].set_title(f'Sector{row["sector"]}: median image; catalog center')
 for ap in row['apertures']:
  f=O/f'curve-s{row["sector"]}-r{ap["radius"]}.npz'
  if not f.exists():continue
  z=np.load(f);a[1].plot(z['t'],z['y'],'.',ms=1,label=f'r={ap["radius"]}')
 a[1].set(xlabel='BTJD',ylabel='Normalized background-subtracted aperture flux',title=row['outcome']);a[1].legend()
fig.savefig(O/'diagnostic.png',dpi=130)
