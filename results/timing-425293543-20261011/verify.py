from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(out/'plan.json');fits=read(out/'fits.json');comp=read(out/'comparison.json')
assert plan['script_sha256']==sha(out/'run.py') and comp['fits_sha256']==sha(out/'fits.json') and comp['plot_sha256']==sha(out/'comparison.png')
fp=Path('results/qlp-faint-midradius-remaining-two-followup-20261011/425293543-peak0/frozen.json');assert plan['frozen_sha256']==sha(fp)
for group,fit in fits.items():
 assert not fit['ranges']['search_boundary_hit']
 assert [v['sector'] for v in fit['data']]==plan['groups'][group]
 for v in fit['data']:assert v['source']['sha256']==sha(Path(f"data/qlp/425293543-s{v['sector']:04d}.fits"))
plots=[]
for s in (53,54):
 p=Path(f'results/tesscut-425293543-shift-s{s}-20261011');i=read(p/'individual-events.json')
 for path,h in i['inputs'].items():assert sha(Path(path))==h
 assert i['script_sha256']==sha(p/'plot_events.py') and i['plot_sha256']==sha(p/'individual-events.png');plots.append({'sector':s,'manifest_sha256':sha(p/'individual-events.json')})
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'fits_sha256':sha(out/'fits.json'),'comparison_sha256':sha(out/'comparison.json'),'individual_plots':plots,'visual_review':'Comparison lightcurve plot inspected: joint fit aligns deep rounded eclipses across all4sectors. Both shifted individual-image grids inspected (7+11events): relative compact target feature recurs, including events with large positive/negative field backgrounds.','limits':'Exploratory refit of opened data. Single group profile widths underestimate between-group differences; no physical timing-variation or unique-host/planet claim. No alias exclusion.'})
print('Timing inputs and plotted evidence verified.')
