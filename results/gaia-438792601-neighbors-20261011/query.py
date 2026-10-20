"""Check Gaia variability for the localized neighbor hypothesis."""
from pathlib import Path
import csv,json
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent
npth=Path('results/neighbors-438792601-20261011/neighbors.json')
analyses=[Path(f'results/tesscut-438792601-s{s}-20261011/analysis.json') for s in [99,100]]
selected={438792601}
for p in analyses:
 selected.update(r['tic'] for r in json.loads(p.read_text())['neighbors'] if r['distance_from_moment_pixels']<=1.)
neighbors=[r for r in json.loads(npth.read_text()) if int(r['ID']) in selected]
assert len(neighbors)==len(selected)
missing=[int(r['ID']) for r in neighbors if r.get('GAIA') is None]
ids=','.join(str(int(r['GAIA'])) for r in neighbors if r.get('GAIA') is not None)
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'neighbors_sha256':sha(npth),'script_sha256':sha(Path(__file__)),
    'image_analysis_hashes':{str(p):sha(p) for p in analyses},'selection':'Target plus every listed source within one pixel of either raw-image moment; no single-variable attribution.', 'targets':neighbors,'missing_gaia_tics':missing,'policy':'TIC Gaia identifiers treated as DR2; obtain DR2-to-DR3 neighborhood mappings before querying DR3. Retain all mappings, errors and nonmatches. Catalog labels do not uniquely identify the TESS source or exclude unlisted variability.'})
def query(table,column,values):
    q=f'select * from gaiadr3.{table} where {column} in ({values})'
    p=Path(f'data/catalogs/gaia-438792601-neighbors-{table}-20261011.csv')
    save_json(out/f'{table}-request.json',{'utc':now(),'query':q})
    source=fetch('https://gea.esac.esa.int/tap-server/tap/sync',p,
        {'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','MAXREC':100000,'QUERY':q})
    save_json(out/f'{table}-source.json',source)
    reader=csv.DictReader(p.open());assert column in reader.fieldnames,'Unexpected response schema'
    rows=list(reader);assert len(rows)<100000
    save_json(out/f'{table}.json',rows)
    return rows
try:
    mappings=query('dr2_neighbourhood','dr2_source_id',ids)
    dr3=','.join(sorted({str(int(r['dr3_source_id'])) for r in mappings}))
    assert dr3,'No mapped DR3 sources; not a variability nonmatch'
    counts={}
    for table in ['gaia_source','vari_classifier_result','vari_eclipsing_binary']:
        rows=query(table,'source_id',dr3);counts[table]=len(rows)
    save_json(out/'results.json',{'utc':now(),'status':'complete','n_mappings':len(mappings),
        'counts':counts,'limits':'Catalog variability lookup, not epoch-photometry confirmation or exclusion. DR2/DR3 mappings may be ambiguous; retain every returned mapping.'})
    print(counts)
except Exception as exc:
    save_json(out/'error.json',{'utc':now(),'error':repr(exc)});raise
