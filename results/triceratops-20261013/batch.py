import subprocess,json,time
from pathlib import Path
R=Path('results/triceratops-20261013');exe='data/triceratops-20261013/venv/bin/python'
jobs=[(t,n,s,noise,c) for n,seeds in [(100000,[13,29,47]),(1000000,[13,29,47])] for t in [80387959,402358350] for s in seeds for noise,c in [(1.,'none')]]
jobs += [(t,100000,13,noise,c) for t in [80387959,402358350] for noise,c in [(1.5,'none'),(2.,'none'),(1.,'flat'),(1.,'inverted')]]
for t,n,s,noise,c in jobs:
 name=f'{t}-N{n}-seed{s}-noise{noise:g}-{c}';print('START',name,flush=True)
 with (R/f'{name}.log').open('w') as f:code=subprocess.call([exe,'-u',str(R/'run.py'),'--tic',str(t),'--draws',str(n),'--seed',str(s),'--noise',str(noise),'--control',c],stdout=f,stderr=subprocess.STDOUT)
 print('END',name,code,flush=True)
