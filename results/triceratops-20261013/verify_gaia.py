from pathlib import Path
import os,json,tempfile
import pandas as pd,numpy as np
from astropy.table import Table
from astroquery.gaia import Gaia
from triceratops.funcs import query_gaia_background
R=Path('results/triceratops-20261013').resolve();D=Path('data/triceratops-20261013').resolve();out=[]
for tic in [80387959,402358350,137151335]:
 raw=pd.read_csv(D/f'{tic}-gaia-raw.csv');table=Table.from_pandas(raw)
 class Job:
  def get_results(self):return table
 Gaia.launch_job=lambda *a,**kw:Job();Gaia.launch_job_async=lambda *a,**kw:Job()
 work=D/f'offline-verification-{tic}';work.mkdir(exist_ok=True);old=os.getcwd();os.chdir(work)
 try:fn=query_gaia_background(0,0,tic,verbose=0)
 finally:os.chdir(old)
 reconstructed=pd.read_csv(work/fn).sort_values(list(pd.read_csv(work/fn).columns)).reset_index(drop=True);original=pd.read_csv(D/f'{tic}_gaia_background.csv').sort_values(list(reconstructed.columns)).reset_index(drop=True)
 from scipy.spatial import cKDTree
 distance,index=cKDTree(reconstructed.values).query(original.values)
 same=original.shape==reconstructed.shape and len(set(index))==len(index) and float(max(distance))<1e-4
 out.append(dict(tic=tic,raw_rows=len(raw),population_rows=len(original),reconstructed_rows=len(reconstructed),bijective_nearest_rows=len(set(index))==len(index),maximum_euclidean_parameter_difference=float(max(distance)),consistent_with_csv_float_serialization=same,tolerance=1e-4))
 (R/'gaia-verification.json').write_text(json.dumps(out,indent=2));assert same

(R/'gaia-verification.json').write_text(json.dumps(out,indent=2));print(out)
