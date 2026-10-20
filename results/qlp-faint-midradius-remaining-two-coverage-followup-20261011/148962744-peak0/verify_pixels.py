from pathlib import Path
import json
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (74,75):
 raw=Path(f'results/tesscut-148962744-s{s}-20261011');proc=Path(f'results/spoc-pixels-148962744-s{s}-20261011');file=read(raw/'files.json')[0];pp=Path(f'data/pixels/148962744-s{s:04d}.fits')
 assert sha(Path(file['path']))==file['sha256']
 with fits.open(pp) as h:assert h[0].header['TICID']==148962744 and h[0].header['SECTOR']==s
 for p,path in ((raw,Path(file['path'])),(proc,pp)):
  c=read(p/'coverage.json');assert c['raw_sha256']==sha(path) and c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(p/'audit_coverage.py')
 assert [e['quality_counts'] for e in c['events']]==([{'4096':68},{'4096':69}] if s==74 else [{'4096':69},{'4096':68}])
 assert all(e['inside_quality_zero']==e['outside_quality_zero']==0 for e in c['events'])
 assert read(proc/'status.json')['exit_code']==1 and 'Fewer than two image events' in (proc/'stderr.txt').read_text()
 rc=read(raw/'coverage.json')
 if s==74:
  assert [e['inside_quality_zero'] for e in rc['events']]==[68,69] and [e['outside_quality_zero'] for e in rc['events']]==[273,274]
  a=read(raw/'analysis.json');assert a['n_events']==2 and a['fit_sha256']==sha(out/'frozen.json') and a['source']['sha256']==file['sha256']
  assert a['script_sha256']==sha(raw/'analyze.py') and a['neighbor_sha256']==sha(Path('results/neighbors-148962744-20261011/neighbors.json'))
 else:
  assert [e['quality_counts'] for e in rc['events']]==[{'2048':69},{'2048':68}]
  assert [e['outside_quality_zero'] for e in rc['events']]==[5,70]
  assert read(raw/'status.json')['exit_code']==1 and 'Fewer than two image events' in (raw/'stderr.txt').read_text()
 rows.append({'sector':s,'raw_file_sha256':file['sha256'],'processed_file_sha256':sha(pp),'raw_coverage_sha256':sha(raw/'coverage.json'),'processed_coverage_sha256':sha(proc/'coverage.json'),'raw_status_sha256':sha(raw/'status.json'),'processed_status_sha256':sha(proc/'status.json')})
p=Path('results/tesscut-148962744-s75-20261011');i=read(p/'individual-events.json')
for path,h in i['inputs'].items():assert sha(Path(path))==h
assert i['script_sha256']==sha(p/'plot_events.py') and i['plot_sha256']==sha(p/'individual-events.png')
r=Path('results/tesscut-148962744-s74-20261011')
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'pixel_module_sha256':sha(Path('src/exoplanet/pixel_vet.py')),'rows':rows,'analysis_sha256':sha(r/'analysis.json'),'stack_sha256':sha(r/'difference.png'),'individual_manifest_sha256':sha(p/'individual-events.json'),'visual_review':'S74 stack and both individual maps inspected: positive across field with column structure, no consistent isolated source. No S75 source image exists.','limits':'Background and quality concerns. All274processed inside exposures4096; all137rawS75inside2048. Missing usable data not nondetection; no Gaia attribution or gates relaxed.'})
print('Source provenance, exposure counts and failures verified.')
