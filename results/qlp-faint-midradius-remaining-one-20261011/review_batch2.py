"""Preserve six manually inspected follow-up plots and audit a cached failure."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha, save_json, now
from exoplanet.archive import qlp_flux_columns
out=Path(__file__).parent
notes={
'169623350-peak0':('followup','Shallow central depression in the folded native data, with substantial individual-point scatter; no obvious deep secondary in the exploratory scan. The time series alone does not establish individual clean transits. Prioritize source-image checks; no host or planet attribution.'),
'439403383-peak1':('followup','Shallow irregular central depression with large gaps and excursions near segment boundaries. Alternate detrending selects another period. No reliable independent recurrence established.'),
'372994314-peak0':('followup','Broad asymmetric folded depression extends well beyond the fitted box. Scatter grows within later segments and coverage is strongly gapped; narrow isolated transit morphology is not established.'),
'399119821-peak0':('coverage-followup','Large gap and markedly changing scatter, especially just after the gap. Folded depression is irregular and only two events support the fitted clock. No stable isolated transit established.'),
'248352802-peak0':('coverage-followup','Broad asymmetric central depression at the edge of a large phase gap, with multiple minima and increasing baseline after the selected center. Two supported events and alternate-detrending ambiguity remain.'),
'302382075-peak0':('coverage-followup','Enormous variable scatter reaches order-unity flux changes, including negative normalized residuals near minus one and positive excursions above one. The narrow selected box is not a credible isolated shallow transit. Secondary scan also selects a large nearby dip and brightening; physical interpretation is unreliable without data/source diagnostics.')}
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
rp=out/'targets/353061535.json';r=json.loads(rp.read_text());raw=Path('data/qlp/353061535-s0083.fits');assert r['status']=='error'
with fits.open(raw) as h:
 d=h[1].data;flux_col,error_col,_=qlp_flux_columns(d.names);counts={'rows':len(d),'q0':int(np.sum(d['QUALITY']==0)),'finite_flux':int(np.isfinite(d[flux_col]).sum()),'finite_error':int(np.isfinite(d[error_col]).sum())}
assert counts['finite_flux']==0 and counts['finite_error']==0
save_json(out/'data-error-353061535.json',{'script_sha256':sha(Path(__file__)),'result_sha256':sha(rp),'raw_path':str(raw),'raw_sha256':sha(raw),'product':r['target']['qlp_products']['83'],'original_error':r['error'],'flux_column':flux_col,'error_column':error_col,'counts':counts,'audit_note':'Initial audit assumed old KSPSAP names and raised KeyError; corrected to the same column selector used by the loader. Raw data and original search failure unchanged.','interpretation':'No finite selected flux/errors in cached training product; data failure, not a nondetection or network retry. Reserved data not substituted.'})
save_json(out/'batch2-reviews.json',{'script_sha256':sha(Path(__file__)),'reports':reports,'error_audit_sha256':sha(out/'data-error-353061535.json'),'status':'Six manually inspected plots; source/raw/artifact hashes checked. No scientific algorithm changes or new full-suite test claim.'})
print('Verified six review sets and cached data failure',counts)
