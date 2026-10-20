import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent
rows=json.loads((p/'fits.json').read_text())['sectors']
fig,axes=plt.subplots(1,3,figsize=(12,4),constrained_layout=True,squeeze=False)
for axesrow,row in zip(axes,rows):
 d=np.load(p/f"s{row['sector']}-images.npz")
 for ax,z,title in zip(axesrow,[d['difference']/d['error'],d['free_model']/d['error'],(d['difference']-d['free_model'])/d['error']],['Difference / error','Free PRF + plane / error','Residual / error']):
  im=ax.imshow(z,origin='lower',cmap='coolwarm',vmin=-6,vmax=6)
  for tic,pos in row['positions'].items():
   xy=np.array(pos)+row['alignment'];ax.plot(*xy,'x',label=tic,ms=5)
  ax.set_title(f"S{row['sector']}: {title}")
 axesrow[0].legend(fontsize=6)
fig.colorbar(im,ax=axes.ravel().tolist(),shrink=.3)
fig.savefig(p/'prf-fits.png',dpi=140)
