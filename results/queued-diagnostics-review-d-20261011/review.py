from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
reviews=[('two', 3920290, 0, 'Visible central dip with sparse cadence and substantial time-series gaps.'), ('two', 257984190, 0, 'Visible broad central dip amid scattered points and time-series gaps.'), ('two', 358699700, 2, 'Noisy broad central depression with markedly changing scatter; another period is retained by the coverage follow-up, not a second planet.'), ('two', 361980197, 0, 'Deep primary and a second prominent off-phase dip. Eclipsing-system or contamination suspect; neither the variable nor its host is established.')]
rows=[]
for tier,tic,rank,visual in reviews:
 p=Path(f'results/qlp-faint-midradius-remaining-{tier}-followup-20261011/{tic}-peak{rank}')
 dp=Path(f'results/qlp-faint-midradius-remaining-{tier.split("-")[0]}-20261011/targets/{tic}.json')
 read=lambda p:json.loads(p.read_text())
 f=read(p/'frozen.json');d=read(dp);h=read(p/'heldout.json');s=read(p/'secondary.json')['diagnostic'];b=f['best']
 assert sha(dp)==f['discovery_sha256']
 flags=d['screened_peaks'][rank]['flags']
 held=[]
 for r in h:
  if r['status']=='error':held.append(f"Sector {r['sector']}: ERROR ({r['error']}); not a nondetection.")
  else:held.append(f"Sector {r['sector']}: {r['conclusion']}, timing spread {r['timing_spread_days']:.4f} days.")
 note=f"# TIC {tic}: unresolved diagnostic\n\nTraining sectors {f['training_sectors']}. Native refinement: period {b['period']:.9f} days, duration {b['duration']:.6f} days, depth {b['depth']*1e6:.0f} ± {b['depth_err']*1e6:.0f} ppm (formal selected-fit error), {f['training_measurement']['supported_events']} supported events. Original flags: {', '.join(flags)}.\n\nVisually inspected discovery plot: {visual} The plot uses the discovery seed; the native refinement above differs slightly.\n\n"+' '.join(held)+f"\n\nTraining off-phase scan's selected maximum has formal SNR {s['best_dip']['snr']:.2f}; selection over phase and duration means this is not a calibrated false-alarm probability or binary confirmation. Inconclusive timing neither confirms nor reliably rejects recurrence. Pixel-source, quality and catalog checks remain pending. No secure host, novelty, or credible planet claim; retain for further review.\n"
 (p/'ASSESSMENT.md').write_text(note)
 save_json(p/'review.json',{'utc':now(),'discovery_sha256':sha(dp),'artifacts':{n:sha(p/n) for n in ['frozen.json','heldout.json','secondary.json','discovery.png','ASSESSMENT.md']},'plot_review':visual,'source_checks_pending':True})
 rows.append(f"| TIC {tic} (peak {rank}) | {b['period']:.6f} d | Diagnostic only; source checks pending, reserved timing inconclusive"+('; sector 26 data check failed.' if tic==18119757 else '.')+f" | [Assessment]({p}/ASSESSMENT.md) |")
p=Path('README.md');txt=p.read_text();anchor='|---|---:|---|---|\n';assert all(f'| TIC {tic} (peak {rank})' not in txt for _,tic,rank,_ in reviews)
p.write_text(txt.replace(anchor,anchor+'\n'.join(rows)+'\n',1))
print('Four inspected diagnostics recorded; discovery hashes verified.')
