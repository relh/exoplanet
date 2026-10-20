from pathlib import Path
import json,re
R=Path('results/triceratops-20261013');s=json.loads((R/'summary.json').read_text());p=R/'ASSESSMENT.md';text=p.read_text();start=text.find('<!-- RESULTS -->');end=text.find('<!-- END RESULTS -->')
if start>=0:text=text[:start]+text[end+len('<!-- END RESULTS -->'):]
lines=['<!-- RESULTS -->','## Results','', '| Target | Target-primary planet weight | FPP | NFPP | Any-host planet weight |','|---|---:|---:|---:|---:|']
for t in s['targets']:
 vals=[t['metrics'][k]['value_1m'] for k in ['target_planet','FPP','NFPP','any_host_planet']]
 lines.append('| TIC '+str(t['tic'])+' | '+' | '.join('Pending' if v is None else f'{v*100:.2f}%' for v in vals)+' |')
lines+=['','These are **single-seed, million-draw, model-conditional weights**. They do not estimate the probability that a candidate is real or previously unknown. Numerical convergence remains unestablished because the bounded experiment does not repeat the million-draw calculation.','']
for t in s['targets']:
 r=t['metrics']['target_planet']['range_100k'];nf=t['metrics']['NFPP']['range_100k'];delta=t['metrics']['target_planet']['delta_1m_from_100k_median']
 if r:lines.append(f"For TIC {t['tic']}, three 100,000-draw seeds give target-primary planet weights of {100*r[0]:.2f}–{100*r[1]:.2f}% and NFPP of {100*nf[0]:.2f}–{100*nf[1]:.2f}%.")
 if delta is not None:lines.append(f'The million-draw target-primary estimate differs from the smaller-run median by {delta*100:+.2f} percentage points.')
 if t.get('dominant_alternatives'):lines.append('Largest alternative scenarios: '+ '; '.join(f"TIC {a['tic']} {a['scenario']} ({a['weight']*100:.2f}%)" for a in t['dominant_alternatives'][:4])+'.')
 lines.append('')
if all(t.get('threshold_comparison') and not t['threshold_comparison']['original_numerical_validation_thresholds_met'] for t in s['targets']):lines+=['Neither candidate meets the original joint numerical validation thresholds (FPP < 1.5% and NFPP < 0.1%) in the million-draw calculation. Their prior signal, timing and source-attribution limitations remain in force.','']
lines+=['### Sensitivity and diagnostic controls','','| Input | Noise multiplier | Target-primary planet weight | FPP | NFPP |','|---|---:|---:|---:|---:|']
for t in s['targets']:
 for d in t['sensitivity_runs']+t['diagnostic_controls']:
  if d['status']=='completed':lines.append(f"| TIC {d['tic']} / {d['control']} | {d['noise']:g} | {100*d['target_planet']:.2f}% | {100*d['FPP']:.2f}% | {100*d['NFPP']:.2f}% |")
for d in s['known_planet_control']:
 if d['status']=='completed':lines.append(f"| Kepler-93 b / sector 40 | {d['noise']:g} | {100*d['target_planet']:.2f}% | {100*d['FPP']:.2f}% | {100*d['NFPP']:.2f}% |")
for t in s['targets']:
 for d in t['diagnostic_controls']:
  if d['control']=='flat' and d['status']=='completed':lines+=['',f"With TIC {t['tic']}'s flux set to a constant 1 (no dimming), the model assigns {100*d['target_planet']:.2f}% to target-primary planets and {100*d['any_host_planet']:.2f}% to planets on any modeled host. The scenario family excludes a general no-signal/artifact alternative, so these weights cannot measure whether a detected planet is real."]
if s['known_planet_control']:
 lines+=['','The restricted Kepler-93 b control does not meet the original validation thresholds. Its known planetary status comes from additional published evidence, not this single-sector calculation. This experiment therefore does not reproduce that published validation or calibrate candidate reliability.']
lines+=['','Each sensitivity/control calculation uses 100,000 draws and seed 13. Flat and inverted tests retain the observed-depth neighbor eligibility and the supplied period; they test behavior when a candidate is forced into the astrophysical scenario family, not a false-alarm rate. No control output is a calibrated reliability estimate.','', '[Machine-readable results and adopted run list](summary.json). All scenario tables and warnings are retained alongside the individual run summaries.','<!-- END RESULTS -->','']
text=text.replace('## Inputs and scope','\n'.join(lines)+'\n## Inputs and scope')
if s['status']=='complete':text=text.replace('**Calculation in progress. No candidate disposition change.**','**The bounded exploratory calculation is complete. Neither candidate is validated; both retain their previous unresolved assessments.**')
p.write_text(re.sub(r"\n{3,}", "\n\n", text))
