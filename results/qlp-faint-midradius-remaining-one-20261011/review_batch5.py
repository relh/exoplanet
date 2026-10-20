"""Preserve six manually inspected follow-up plots ."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha, save_json, now
from exoplanet.archive import qlp_flux_columns
out=Path(__file__).parent
notes={'429034844-peak1':('followup','Deep regular dips with three similarly spaced minima in the selected period fold. A shorter alias and eclipsing interpretation need evaluation. Original alternate-detrending flag remains; source and novelty checks pending, no new planet claim.')}
reports=[]
for name,(kind,note) in notes.items():
 p=Path(f'results/qlp-faint-midradius-remaining-one-{kind}-20261011')/name
 f=json.loads((p/'frozen.json').read_text());h=json.loads((p/'heldout.json').read_text());s=json.loads((p/'secondary.json').read_text());b=f['best'];tic=f['tic']
 dp=out/'targets'/f'{tic}.json';assert sha(dp)==f['discovery_sha256']
 for source,digest in f['source_sha256'].items():assert sha(Path('src/exoplanet')/source)==digest
 for data in [f['training_data'],s['data']]+[r.get('data',[]) for r in h]:
  for row in data:assert sha(Path(f"data/qlp/{tic}-s{row['sector']:04d}.fits"))==row['source']['sha256']
 assert all(x['conclusion']=='timing_prediction_inconclusive' for x in h)
 text=f"# TIC {tic}: unresolved screening signal\n\nNative refinement: P={b['period']:.9f} days, duration={b['duration']:.6f} days, box depth={b['depth']:.8f} ± {b['depth_err']:.8f} (formal). Training sectors {f['training_sectors']}; {f['training_measurement']['supported_events']} supported events. These are fitted diagnostic quantities, not physical size estimates or calibrated discovery probabilities.\n\nThe original-seed native discovery plot was inspected: {note}\n\n"
 text+='Reserved-sector timing tests: '+ '; '.join(f"sector {x['sector']}: {x['conclusion']}, timing spread {x['timing_spread_days']:.6f} days" for x in h)+'. Timing uncertainty prevents interpreting a fixed-window absence as exclusion or confirmation.\n\n'
 text+=f"Exploratory off-phase maximum formal SNR: {s['diagnostic'].get('best_dip',{}).get('snr')}. It is selected over phase/duration and is not a calibrated secondary-eclipse significance.\n\nOriginal screening flags, cache-presence records, failed checks and timing profiles remain in the underlying files. Source attribution, catalog checks and physical vetting remain pending. No likely new planet claimed.\n"
 (p/'ASSESSMENT.md').write_text(text)
 save_json(p/'review.json',{'utc':now(),'discovery_sha256':sha(dp),'artifacts':{n:sha(p/n) for n in ['frozen.json','heldout.json','secondary.json','discovery.png','ASSESSMENT.md']},'plot_review':note,'source_checks_pending':True,'host_attribution':'Unresolved; no likely planet.'})
 reports.append({'path':str(p),'review_sha256':sha(p/'review.json')})
save_json(out/'batch5-reviews.json',{'script_sha256':sha(Path(__file__)),'reports':reports,'status':'One plot inspected and raw/source/artifact hashes checked; physical/source vetting pending.'})
print('Verified one new review sets.')
