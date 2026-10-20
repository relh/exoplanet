"""Publish completed resolved-source checks and a site-independent planning packet."""
from pathlib import Path
import hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dashboard/dist'
DIRS=['followup-overview-20261013','resolved-followup-803-20261013','resolved-followup-402-20261013','followup-planning-20261013','observing-access-20261013','site-visibility-20261013','lco-archive-metadata-20261013','decisive-observation-protocol-20261013','eso-raw-metadata-20261013','cheops-metadata-20261013','remaining-evidence-audit-20261013','superwasp-metadata-20261013','old-epoch-timing-20261013','t17-feasibility-20261013','t17-access-inquiry-20261013','t17-review-20261013']
def export():
 manifest=[]
 for directory in DIRS:
  source=ROOT/'results'/directory/'ASSESSMENT.md'
  assert source.exists(),f'Wait for {source}'
  name=directory+'.txt';shutil.copyfile(source,OUT/name)
  manifest.append(dict(source=str(source.relative_to(ROOT)),export=name,sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
 for source,name in [('results/followup-overview-20261013/fields.png','followup-fields.png'),('results/followup-planning-20261013/events.csv','followup-events.csv'),('results/followup-planning-20261013/targets.json','followup-targets.json'),('results/followup-planning-20261013/neighbors.csv','followup-neighbors.csv')]:
  p=ROOT/source;shutil.copyfile(p,OUT/name);manifest.append(dict(source=source,export=name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 with zipfile.ZipFile(OUT/'followup-evidence.zip','w',zipfile.ZIP_DEFLATED) as z:
  for directory in DIRS:
   for p in sorted((ROOT/'results'/directory).rglob('*')):
    if p.is_file() and '__pycache__' not in p.parts:
     member=str(p.relative_to(ROOT/'results'));z.write(p,member);manifest.append(dict(source=str(p.relative_to(ROOT)),archive_member=member,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 (OUT/'followup-provenance.json').write_text(json.dumps(manifest,indent=2)+'\n')
 page=OUT/'index.html';s=page.read_text();start=s.index('<h2 id="follow-up">');end=s.index('<h2>Assessment status</h2>',start)
 section='''<h2 id="follow-up">Resolved-source follow-up</h2>
<p>New archival tests examine two additional neighboring stars. Neither candidate has been validated. The observation packet below preserves the existing clocks and their timing limitations.</p>
<div class="table-scroll"><table><thead><tr><th>Signal</th><th>New check</th><th>Observation planning</th></tr></thead><tbody>
<tr><th>TIC 80387959</th><td>Two SkyMapper measurements show no dimming of neighbor TIC 80387968 during one predicted event. This weakens a same-depth, flat-bottom eclipse explanation; one event cannot exclude the source. <a href="resolved-followup-803-20261013.txt">Results and limits ↗</a></td><td>About 5.6 hours for the retained timing envelope, dip duration and one hour of baseline on each side.</td></tr>
<tr><th>TIC 402358350</th><td>ZTF supplied 836 measurements of neighbor TIC 74037550; 545 pass quality cuts. All 72 fixed-clock comparisons remain inconclusive because timing or coverage is inadequate. <a href="resolved-followup-402-20261013.txt">Results and limits ↗</a></td><td>Expanded-clock sensitivity requires 17.5–18.5 hours; older clocks disagree more. Recover the ephemeris before attempting a short targeted observation.</td></tr>
</tbody></table></div>
<p><strong>TIC 80387959 is the priority for a resolved observing attempt.</strong> Measure the target and competing stars separately across the allowed event window. A neighbor can only be cleared if timing coverage and measured precision could detect the required eclipse. Resolving one alternative does not establish a planet.</p>
<p>The packet lists nominal events through April 2027. These are <strong>site-independent planning windows, not a telescope schedule or calibrated confidence intervals</strong>. Five-site visibility and LCO one-meter tracking limits have now been checked; weather, access and equipment sensitivity remain unestablished. UTC values are approximate geocentric conversions; BJD_TDB values retain the scientific time convention.</p>
<p><strong>No robust full LCO one-meter track is established.</strong> Three TIC 80387959 windows pass the sky screen, but only 20 March 2027 at CTIO passes the tracking limit, with about 82 sidereal seconds of margin. None passes the conservative mount-margin test. TIC 402358350 has no complete window in the tested five-site network. Other sites, equipment or explicitly revised observing plans could differ.</p>
<p>Public LCO images add no transit test: nine science exposures precede the predicted TIC 80387959 event. The two inspected baseline frames saturate both the target and its main neighbor, so they do not demonstrate usable photometric precision. An apparent TIC 402358350 spectral match has a pointing about 5.3° away; it is not established candidate spectroscopy.</p>
<div class="downloads"><a href="site-visibility-20261013.txt">Visibility and tracking limits ↗</a><a href="observing-access-20261013.txt">Telescope access options ↗</a><a href="decisive-observation-protocol-20261013.txt">Proposed observation protocol ↗</a><a href="lco-archive-metadata-20261013.txt">Archival image assessment ↗</a></div>
<p>Further <a href="eso-raw-metadata-20261013.txt">ESO raw-observation</a> and <a href="cheops-metadata-20261013.txt">CHEOPS visit</a> metadata searches return no pointings within two arcminutes of either target. These bounded archive nonmatches do not exclude companions or every off-axis observation. No new flux was opened. The <a href="remaining-evidence-audit-20261013.txt">remaining-evidence review</a> records the reviewed routes and observation dependencies.</p>
<p><a href="superwasp-metadata-20261013.txt">SuperWASP metadata</a> adds only seven measurements over 37 minutes for the nearest TIC 80387959 source and no source in the TIC 402358350 cone. No useful recurrence test is identified, and no light curve was opened. <a href="old-epoch-timing-20261013.txt">Backward timing propagation</a> also fails the original precision gates at four representative 2004–2009 dates; a narrow fixed-clock non-detection would be inconclusive.</p>
<p><strong>One alternative observing window is plausible, but not operationally verified:</strong> T17 at Siding Spring, 28 March 2027, approximately 12:05–17:43 UTC. It passes the sky requirements and an illustrative horizon model, but the actual obstruction mask, tracking/meridian behavior, access and photometric precision remain unverified. <a href="t17-feasibility-20261013.txt">Geometry and assumptions</a> · <a href="t17-review-20261013.txt">Independent review</a> · <a href="t17-access-inquiry-20261013.txt">Unsent operator inquiry</a>.</p>
<details><summary>Field diagrams and observation packet</summary><img src="followup-fields.png" alt="Catalog-coordinate diagrams of the target stars and selected competing sources, with east left and north up"/><p>Green marks targets; orange marks selected alternatives. These are catalog diagrams, not telescope images or source localizations. Update positions for the observing date using the packet’s proper motions.</p><div class="downloads"><a href="followup-events.csv" download>Event windows CSV ↓</a><a href="followup-targets.json">Targets and timing assumptions ↗</a><a href="followup-neighbors.csv" download>Neighbor requirements CSV ↓</a><a href="followup-planning-20261013.txt">Planning assessment ↗</a></div></details>
<div class="downloads"><a href="followup-overview-20261013.txt">Follow-up assessment ↗</a><a href="followup-evidence.zip" download>Complete follow-up records ↓</a><a href="followup-provenance.json">Source hashes ↗</a></div>
'''
 page.write_text(s[:start]+section+s[end:]);print('Exported',len(manifest),'follow-up evidence entries')
if __name__=='__main__':export()
