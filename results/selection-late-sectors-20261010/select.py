import csv,json
from pathlib import Path
from collections import Counter
from exoplanet.targeting import fetch_small_stars
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;root=Path('data/targeting');stars,tic_source=fetch_small_stars(root)
known=set();sources={}
for name,key in [('toi','tid'),('confirmed','tic_id'),('ctoi','TIC ID'),('eb','tess_id')]:
 p=Path('results/selection-small-stars-20261009')/f'catalog_{name}.csv';sources[name]={'path':str(p),'sha256':sha(p)}
 for r in csv.DictReader(p.open()):known.add(int(r[key].replace('TIC','').strip()))
coverage={int(r['tic']):list(map(int,r['sectors'].split())) for r in csv.DictReader((root/'coverage.csv').open())}
opened=set()
for p in Path('data/lightcurves').glob('s*-*.fits'):
 try:opened.add(int(p.stem.split('-')[1]))
 except ValueError:pass
for p in Path('data/qlp').glob('*-s*.fits'):
 try:opened.add(int(p.stem.split('-s')[0]))
 except ValueError:pass
old={r['tic'] for r in json.loads(Path('results/selection-small-stars-20261009/eligible.json').read_text())}
counts=Counter();eligible=[]
for star in stars:
 tic=int(star['ID']);sectors=sorted(coverage.get(tic,[]));reason=None
 if tic in opened or tic in old:reason='already_opened_or_original_selection'
 elif tic in known:reason='known_catalog_match'
 elif str(star.get('disposition') or '').upper() in {'ARTIFACT','DUPLICATE','SPLIT'} or star.get('duplicate_id'):reason='tic_disposition'
 elif star.get('contratio') is None or star['contratio']>.2:reason='contamination_or_missing'
 elif star.get('Teff') is None or star['Teff']>5300:reason='temperature_or_missing'
 if reason:counts[reason]+=1;continue
 options=[]
 for sector in sectors:
  if sector<56 or sector+1 not in sectors:continue
  training=[sector,sector+1];held=[s for s in sectors if min(abs(s-x) for x in training)>=8]
  if held:options.append((training,held))
 if not options:counts['no_late_pair_and_separate_epoch']+=1;continue
 training,held=options[0];score=star['rad']**2*10**(.2*(star['Tmag']-10))/2**.5
 eligible.append(dict(tic=tic,star=star,sectors=sectors,training_sectors=training,heldout_sectors=held,priority_noise_proxy=score))
eligible.sort(key=lambda r:(r['priority_noise_proxy'],r['tic']))
save_json(out/'eligible.json',eligible);save_json(out/'selected.json',eligible[:256]);save_json(out/'selection.json',dict(created_utc=now(),tic_source=tic_source,catalogs=sources,coverage_sha256=sha(root/'coverage.csv'),script_sha256=sha(Path(__file__)),n_stars=len(stars),n_eligible=len(eligible),n_selected=min(256,len(eligible)),excluded=dict(counts),previously_opened_ids=sorted(opened),rule='Same small nearby-star cuts as original search; previously opened targets excluded. Earliest adjacent pair >=56; reserve sectors separated by>=8 from both training sectors. Ranked by radius/brightness proxy, not measured quietness. Sector spacing is coarse; actual independence/timing checked during follow-up.',limitations='20261009catalog snapshots, exactTIC exclusion only; candidate positional/alias/current catalog vetting still required. Coverage from existing85TESS-SPOCtarget lists, not allTESSsectors.'))
print('eligible',len(eligible),'selected',min(256,len(eligible)));print(Counter(tuple(r['training_sectors']) for r in eligible))
