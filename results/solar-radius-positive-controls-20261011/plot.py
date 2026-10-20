from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.campaign import load_training
from exoplanet.pipeline import save_json,sha
p=Path(__file__).parent;out=Path('results/solar-radius-positive-controls-run-20261011');evaluation=json.loads((p/'evaluation.json').read_text());fig,axes=plt.subplots(5,1,figsize=(12,14),constrained_layout=True);inputs={}
for ax,row in zip(axes,evaluation['rows']):
 path=out/'targets'/f"{row['tic']}.json";r=json.loads(path.read_text());inputs[str(path)]=sha(path);t,y,dy,_=load_training(r['target'],Path('data'));b=r['best'];phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;edges=np.linspace(-b['period']/2,b['period']/2,101);bx=[];by=[]
 for a,c in zip(edges[:-1],edges[1:]):
  ok=(phase>=a)&(phase<c)
  if ok.sum():bx.append((a+c)/2*24);by.append(np.median(y[ok]-1)*1e6)
 ax.scatter(phase*24,(y-1)*1e6,s=1,alpha=.12);ax.plot(bx,by,'k.-',lw=1);ax.set_xlabel('Hours from strongest fitted box center');ax.set_ylabel('Flux residual (ppm)');ax.set_title(f"{row['name']} control | strongest P={b['period']:.6f}d | selected planet full pass: {row['selected_planet_pass']}")
fig.suptitle('Known-planet controls: strongest search peaks; TOI-5788 strongest peak is planet c, not selected b');fig.savefig(p/'control-folds.png',dpi=120);save_json(p/'plot-inputs.json',dict(script_sha256=sha(Path(__file__)),inputs=inputs,policy='Visualizes strongest search peak even when below threshold; no screened row fabricated and no known clock fitted.'))
