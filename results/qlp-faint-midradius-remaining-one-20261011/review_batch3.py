"""Preserve six manually inspected follow-up plots ."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha, save_json, now
from exoplanet.archive import qlp_flux_columns
out=Path(__file__).parent
notes={'101404423-peak0': ('followup', 'Shallow rounded central depression with small positive shoulders and a gap in the time series. Eight supported training events; prioritize source images, but no independent recurrence or host attribution.'), '160463097-peak0': ('followup', 'Broad asymmetric central depression in noisy photometry, plus another depression near the edge of the full phase fold. The selected off-phase scan is diagnostic only. Source and physical interpretation unresolved.'), '354475391-peak0': ('coverage-followup', 'Broad irregular gap-adjacent depression with large positive and negative excursions in the time series. Two supported events; not an isolated stable transit. The other seed refines to essentially the same period and depth, not an independent candidate.'), '354475391-peak1': ('coverage-followup', 'Broad irregular gap-adjacent depression with large time-series excursions. This alternate seed converges to essentially the same native fit as peak0; previously opened held data are not new blind evidence. Two fits are not two planets.'), '373414832-peak1': ('coverage-followup', 'Shallow central depression with nearly half the phase coverage absent and broad irregular structure in the zoom. Four supported native events do not repair missing secondary coverage or alternate-detrending ambiguity.'), '66775591-peak0': ('followup', 'Broad rounded depression with prominent positive shoulders on both sides. Repeated folded structure is apparent, but this is not an isolated flat-baseline transit profile; variability or processing effects remain plausible. Independent timing tests remain inconclusive.')}
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
save_json(out/'batch3-reviews.json',{'script_sha256':sha(Path(__file__)),'reports':reports,'status':'Six plots inspected and raw/source/artifact hashes checked; physical/source vetting pending.'})
print('Verified six new review sets.')
