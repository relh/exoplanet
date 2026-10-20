from pathlib import Path
import json,math,csv
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());r=read(out/'results.json');g=Path('results/gaia-429034844-scene-20261011')
for p,h in r['inputs'].items():assert sha(Path(p))==h
assert r['script_sha256']==sha(out/'run.py')
for table in ['gaia_source','dr2_neighbourhood']:
 raw=Path(f'data/catalogs/gaia-429034844-scene-{table}-20261011.csv');assert sha(raw)==read(g/f'{table}-source.json')['sha256']
 assert list(csv.DictReader(raw.open()))==read(g/f'{table}.json')
a,b=r['gaia_rows'];rad=math.pi/180
v=math.sin((float(b['dec'])-float(a['dec']))*rad/2)**2+math.cos(float(a['dec'])*rad)*math.cos(float(b['dec'])*rad)*math.sin((float(b['ra'])-float(a['ra']))*rad/2)**2
sep=2*math.asin(math.sqrt(v))/rad*3600;assert abs(sep-r['gaia_separation_arcsec'])<1e-8
f=1/(1+10**(.4*r['tic_delta_Tmag']));assert abs(f-r['illustrative_neighbor_flux_fraction'])<1e-14
for row in r['depth_scenarios']:
 d=row['neighbor_only_intrinsic_depth_equal_throughput'];assert 0<d<1 and abs(d*f-row['observed_box_depth'])<1e-14
# Direct two-flux mixing controls: equal stars, and zero/full eclipse.
for q in [1,.01,10]:
 for d in [0,.3,1]:
  observed=1-(1+q*(1-d))/(1+q)
  assert abs(observed-d*q/(1+q))<1e-14
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'artifacts':{str(p):sha(p) for p in [out/'run.py',out/'results.json',out/'ASSESSMENT.md']},'status':'Inputs/raw CSV identity, independent haversine separation and two-flux mixing arithmetic checked. Not empirical aperture, source-host or spectroscopy validation.'});print('Verified catalog geometry and illustrative dilution.')
