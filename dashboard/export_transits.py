"""Presentation-only export of saved baseline-subtracted observations; no refit."""
from pathlib import Path
import hashlib, json
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'dashboard/dist'
manifest = []
def read(path, binary=False):
    p = ROOT/path
    manifest.append({'source':path,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    return np.load(p) if binary else json.loads(p.read_text())
output = {}
base = 'results/strongest-80387959-shape-20261012'
plan = read(base+'/plan.json'); results = read(base+'/results.json')
series=[]
for row in results['rows']:
    sector=row['sector']; a=read(f'{base}/s{sector}-primary.npz',True)
    # Remove only the saved event-intercept/slope columns, retaining the dip.
    residual = a['y'] - a['X'][:,:-1] @ a['beta'][:-1]
    hours=a['dt']*24
    c=next(c for c in row['cases'] if c['name']=='primary')
    mask=np.abs(a['dt'])<2*plan['best']['duration']
    series.append(dict(label=f"Sector {sector} · {'QLP' if sector>=90 else 'SPOC'}",sector=sector,depth=c['depths_ppm'][0],points=np.column_stack([hours[mask],residual[mask]*1e6]).round(6).tolist(),events=len(c['events'])))
output['80387959']=dict(period=plan['best']['period'],duration_hours=plan['best']['duration']*24,reference_depth_ppm=plan['best']['depth']*1e6,series=series,method='Corrected flux; saved joint event baseline removed, transit term retained. Sectors have different cadences, products and depths. Combining them is descriptive.',reference='Animation uses the original saved clock depth, not a new fit to combined sectors.')
base='results/strongest-402358350-baselines-20261012'
plan=read(base+'/plan.json');results=read(base+'/results.json');summary=read(base+'/summary.json')
series=[]
for sector in [40,41,54,81]:
    points=[];count=0
    for row in results['rows']:
        if not(row['sector']==sector and row['kind']=='PDCSAP' and row['degree']==1 and row['outer']==3 and row['measurement']['status']=='measured'):continue
        a=read(f"{base}/{row['key']}.npz",True)
        residual=a['y']-a['X']@np.array(row['measurement']['coefficients'])
        mask=np.abs(a['x'])<2
        points.extend(np.column_stack([a['x'][mask]*plan['clock']['duration']*24,residual[mask]*1e6]).round(6).tolist());count+=1
    series.append(dict(label=f'Sector {sector} · PDCSAP',sector=sector,points=points,events=count))
ref=next(m for m in summary['methods'] if m['kind']=='PDCSAP' and m['degree']==1 and m['outer']==3)
output['402358350']=dict(period=plan['clock']['period'],duration_hours=plan['clock']['duration']*24,reference_depth_ppm=ref['depth']['depth']*1e6,series=series,method='PDCSAP flux; saved linear baseline fitted outside the dip, within ±3 durations. Same presentation choice as the archived event-shapes figure. One gap event is excluded by the original coverage gate. Timing remains unresolved.',reference='Animation uses the saved eight-event PDCSAP linear-baseline depth, not a physical transit fit.')
(OUT/'transits.json').write_text(json.dumps(output,separators=(',',':'),allow_nan=False))
(OUT/'transit-provenance.json').write_text(json.dumps({'inputs':manifest,'display':'All saved samples within ±2 fixed durations. Flux is additive baseline residual in ppm. Browser bins are equal-width arithmetic means, no smoothing or refitting. No new statistical evidence or observation.','animation':'Hypothetical central crossing of one uniform, undiluted stellar disk. Radius ratio sqrt(reference depth); geometry, host and surface appearance unmeasured.'},indent=2))
print({tic: {'points':sum(len(s['points']) for s in d['series']),'events':sum(s['events'] for s in d['series'])} for tic,d in output.items()})
