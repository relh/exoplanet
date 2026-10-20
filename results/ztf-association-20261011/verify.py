from pathlib import Path
import json,math,itertools
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;r=json.loads((p/'results.json').read_text())
for name,digest in r['inputs'].items():assert sha(Path(name))==digest
count=0
for row in r['objects']:
 obj=json.loads(Path(f"data/ztf/cloud-dr24-{row['oid']}.json").read_text());gaia=json.loads(Path(f"results/gaia-{row['tic']}-scene-20261011/gaia_source.json").read_text())
 def separation(g):
  ra1,d1,ra2,d2=map(math.radians,[obj['objra'],obj['objdec'],float(g['ra']),float(g['dec'])]);h=math.sin((d2-d1)/2)**2+math.cos(d1)*math.cos(d2)*math.sin((ra2-ra1)/2)**2
  return math.degrees(2*math.asin(math.sqrt(h)))*3600
 ranked=sorted(gaia,key=separation)
 for actual,g in zip(row['nearest_gaia'],ranked):
  assert actual['source_id']==g['source_id'];assert math.isclose(actual['separation_at_gaia_reference_arcsec'],separation(g),abs_tol=1e-7);count+=1
for check in r['duplicate_checks']:
 allrows=[]
 for row in r['objects']:
  if row['tic']!=check['tic']:continue
  o=json.loads(Path(f"data/ztf/cloud-dr24-{row['oid']}.json").read_text())
  for x in o['lightcurve']:
   if x['catflags']==0 and all(x[k] is not None and math.isfinite(x[k]) for k in ['hmjd','mag','magerr']) and x['magerr']>0:allrows.append((o['filterid'],x['hmjd']))
 assert len(allrows)==check['n_good']
 pairs=[(a,b) for a,b in itertools.combinations(allrows,2) if a[0]==b[0] and abs(a[1]-b[1])*86400<=2]
 assert len(pairs)==len(check['same_band_pairs_within_2_seconds'])==0
save_json(p/'verification.json',{'nearest_comparisons_recomputed':count,'all_pair_timestamp_audits':3,'artifacts':{q.name:sha(q) for q in p.iterdir() if q.is_file() and q.name!='verification.json'},'status':'Identity geometry and duplicate-time audit passed; not physical source validation.'})
print('verified',count,'separations and3 full timestamp-pair comparisons')
