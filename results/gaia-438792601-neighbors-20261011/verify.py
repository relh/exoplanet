"""Verify catalog provenance and compare the neighboring binary's period."""
from pathlib import Path
import json
from exoplanet.pipeline import sha, save_json, now

out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
plan=read(out/'plan.json')
assert sha(Path('results/neighbors-438792601-20261011/neighbors.json'))==plan['neighbors_sha256']
for p,h in plan['image_analysis_hashes'].items():assert sha(Path(p))==h
inventory=[]
for table in ['dr2_neighbourhood','gaia_source','vari_classifier_result','vari_eclipsing_binary']:
    raw=Path(f'data/catalogs/gaia-438792601-neighbors-{table}-20261011.csv')
    source=read(out/f'{table}-source.json')
    assert sha(raw)==source['sha256'] and raw.stat().st_size==source['bytes']
    inventory.append({'table':table,'raw_sha256':sha(raw),'json_sha256':sha(out/f'{table}.json'),'source_sha256':sha(out/f'{table}-source.json')})
neighbor=next(t for t in plan['targets'] if int(t['ID'])==288891067)
mappings=[r for r in read(out/'dr2_neighbourhood.json') if r['dr2_source_id']==neighbor['GAIA']]
assert len(mappings)==1
sourceid=mappings[0]['dr3_source_id']
entries=[r for r in read(out/'vari_eclipsing_binary.json') if r['source_id']==sourceid]
assert len(entries)==1
eb=entries[0];frequency=float(eb['frequency']);period=1/frequency
fitpath=Path('results/qlp-faint-midradius-four-pilot-followup-20261011/438792601-peak0/frozen.json')
fit=read(fitpath)['best']
save_json(out/'verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),
    'inventory':inventory,'tic':288891067,'gaia_dr3':sourceid,'dr2_dr3_mapping':mappings,
    'gaia_period_days':period,'gaia_formal_period_error_days':float(eb['frequency_error'])/frequency**2,
    'tess_period_days':fit['period'],'fit_sha256':sha(fitpath),
    'tess_minus_gaia_period_seconds':(fit['period']-period)*86400,
    'fractional_period_difference':fit['period']/period-1,
    'frequency_units_documentation':'https://gaia.aip.de/metadata/gaiadr3/vari_eclipsing_binary/',
    'limits':'Close periods and repeated off-target moments favor this cataloged eclipsing-binary candidate as contaminant. Blended pixels do not prove unique source attribution. No joint period-error model, phase alignment, Gaia epoch-photometry inspection, or calibrated chance-match probability.'})
print('TIC288891067 Gaia period:',period,'days; TESS-minus-Gaia seconds:',(fit['period']-period)*86400)
