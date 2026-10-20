import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PRF import TESS_PRF
from exoplanet.prf_fit import fit_templates
p=Path(__file__).parent
rows=json.loads((p/'fits.json').read_text())['sectors']
fig,axes=plt.subplots(1,3,figsize=(12,4),constrained_layout=True,squeeze=False)
for axesrow,row in zip(axes,rows):
 d=np.load(p/f"s{row['sector']}-images.npz")
 meta=json.loads((p/'models.json').read_text())['sectors'][0]
 prf=TESS_PRF(meta['camera'],meta['ccd'],91,meta['col'],meta['row'],localdatadir='data/prf/start_s0004')
 xy=np.array(row['positions']['422626648'])+row['alignment']+row['free_offset_from_target']
 template=prf.locate(*xy,d['difference'].shape)
 f=fit_templates(d['difference'],d['error'],[template]);plane=f['model']-f['coefficients'][0]*template
 for ax,z,title in zip(axesrow,[(d['difference']-plane)/d['error'],(d['free_model']-plane)/d['error'],(d['difference']-d['free_model'])/d['error']],['Difference minus fitted plane / error','Free PRF component / error','Residual / error']):
  im=ax.imshow(z,origin='lower',cmap='coolwarm',vmin=-6,vmax=6)
  for tic,pos in row['positions'].items():
   xy=np.array(pos)+row['alignment'];ax.plot(*xy,'x',label=tic,ms=5)
  ax.set_title(f"S{row['sector']}: {title}")
 axesrow[0].legend(fontsize=6)
fig.colorbar(im,ax=axes.ravel().tolist(),shrink=.3)
fig.savefig(p/'prf-fits.png',dpi=140)
