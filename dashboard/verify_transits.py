"""Check presentation exports against every saved input; no observations opened."""
from pathlib import Path
import hashlib,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'dashboard/dist/transits.json').read_text())
manifest=json.loads((ROOT/'dashboard/dist/transit-provenance.json').read_text())
for record in manifest['inputs']:
    assert hashlib.sha256((ROOT/record['source']).read_bytes()).hexdigest()==record['sha256']
checked=0
for tic,run in [('80387959','strongest-80387959-shape-20261012'),('402358350','strongest-402358350-baselines-20261012')]:
    base=ROOT/'results'/run;plan=json.loads((base/'plan.json').read_text());results=json.loads((base/'results.json').read_text())
    clock=plan['best'] if tic=='80387959' else plan['clock']
    assert d[tic]['period']==clock['period'] and d[tic]['duration_hours']==24*clock['duration']
    for series in d[tic]['series']:
        expected=[];sector=series['sector'];events=0
        if tic=='80387959':
            a=np.load(base/f's{sector}-primary.npz')
            # Full-model residual + fitted signal, independent algebraic form.
            flux=a['y']-a['X']@a['beta']+a['X'][:,-1]*a['beta'][-1]
            selected=np.abs(a['dt'])<2*clock['duration']
            expected=np.column_stack([a['dt'][selected]*24,flux[selected]*1e6])
            events=len(np.unique(a['cycles']))
        else:
            for row in results['rows']:
                if row['sector']!=sector or row['kind']!='PDCSAP' or row['degree']!=1 or row['outer']!=3 or row['measurement']['status']!='measured':continue
                a=np.load(base/(row['key']+'.npz'));intercept,slope=row['measurement']['coefficients']
                flux=a['y']-intercept-slope*a['x'];selected=np.abs(a['x'])<2
                expected.extend(zip(a['x'][selected]*24*clock['duration'],flux[selected]*1e6));events+=1
        expected=np.asarray(expected);actual=np.asarray(series['points'])
        assert actual.shape==expected.shape
        assert np.allclose(actual,expected,atol=0.0000006,rtol=0)
        assert np.isfinite(actual).all() and series['events']==events
        checked+=len(actual)
assert checked==4045
print(f'PASS: {checked} exported observations, all sector/event counts, clocks and {len(manifest["inputs"])} source hashes.')
