from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json,now
O=Path(__file__).parent
files=[(80387959,'results/prf-80387959-20261009/scene-mag15/fits.json'),(402358350,'results/prf-402358350-20261011/fits.json'),(402358350,'results/prf-402358350-s54-20261011/fits.json'),(402358350,'results/prf-402358350-s81-20261011/fits.json')]
rows=[]
for tic,name in files:
 for s in json.loads(Path(name).read_text())['sectors']:
  a=np.array(s['positions'][str(tic)]);yy,xx=np.indices((11,11));assert s['hypotheses'][0]['dof']==117 or tic==402358350
  for h in s['hypotheses']:
   if h['tic']==str(tic):continue
   b=np.array(s['positions'][h['tic']]);sep=float(np.linalg.norm(a-b))
   for rad in [1.,1.5]:
    m=np.hypot(xx-a[0],yy-a[1])<=rad;n=np.hypot(xx-b[0],yy-b[1])<=rad;shared=int((m&n).sum());exclusive=[int((m&~n).sum()),int((n&~m).sum())];rows.append(dict(tic=tic,sector=s['sector'],neighbor=h['tic'],separation_pixels=sep,radius=rad,shared_pixels=shared,exclusive_pixels=exclusive,overlap_fraction=shared/int((m|n).sum()),identical_masks=bool(np.array_equal(m,n)),contrast_constructible=bool(all(exclusive))))
save_json(O/'candidate-geometry.json',dict(created_utc=now(),inputs={name:sha(Path(name)) for tic,name in files},scope='Only archivedcatalogcoordinates and11x11stamp geometry,no candidateeventvalues,templateamplitudes orchi2 compared. Geometricoverlap bounds apertureleverage,not sourceprobability. No candidateflux application because controlsfailed.',rows=rows))
print('cases',len(rows),'identical',sum(x['identical_masks'] for x in rows),'unconstructible',sum(not x['contrast_constructible'] for x in rows),'separation',min(x['separation_pixels'] for x in rows),max(x['separation_pixels'] for x in rows))
