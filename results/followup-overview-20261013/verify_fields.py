"""Independent spherical geometry and input-provenance check."""
from pathlib import Path
import hashlib,json,math
R=Path('results/followup-overview-20261013');rows=json.loads((R/'field-coordinates.json').read_text());checks=0
for item in json.loads((R/'field-provenance.json').read_text()):
 assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['sha256'];checks+=1
for row in rows:
 center=next(r for r in rows if r['field']==row['field'] and r['tic']==row['field'])
 a,d,a0,d0=map(math.radians,[row['ra_deg'],row['dec_deg'],center['ra_deg'],center['dec_deg']]);da=a-a0
 xx=math.cos(d)*math.sin(da);yy=math.sin(d)*math.cos(d0)-math.cos(d)*math.sin(d0)*math.cos(da);zz=math.sin(d)*math.sin(d0)+math.cos(d)*math.cos(d0)*math.cos(da)
 east=math.degrees(math.atan2(xx,zz))*3600;north=math.degrees(math.asin(yy))*3600;sep=math.degrees(math.atan2(math.hypot(xx,yy),zz))*3600
 for k,v in [('east_arcsec',east),('north_arcsec',north),('separation_arcsec',sep)]:assert abs(row[k]-v)<1e-7;checks+=1
(R/'field-verification.json').write_text(json.dumps(dict(checks=checks,passed=True,limitation='Catalog geometry only; no host attribution or observed eclipse.'),indent=2)+'\n');print(checks,'checks pass')
