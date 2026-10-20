from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha, save_json
out = Path(__file__).parent
rows = json.loads((out / 'results.json').read_text())['rows']
fig, axes = plt.subplots(2, 1, figsize=(11, 7), constrained_layout=True)
for ax, key, label in zip(axes, ['149919534', '149919536'], ['Target TIC149919534', 'Neighbor TIC149919536']):
    for j, row in enumerate(rows):
        values = [c['amplitudes'][key] for c in row['controls']]
        ax.scatter(np.full(len(values), j), values, color='gray', alpha=.45, s=12, label='8 distinct control windows' if j == 0 else None)
        for event, color, marker in [(1, 'tab:blue', 'o'), (2, 'tab:orange', '^')]:
            value = next(e['amplitudes'][key] for e in row['events'] if e['event'] == event)
            ax.scatter(j, value, color=color, marker=marker, s=30, label=f'Event {event}' if j == 0 else None)
    ax.axhline(0, color='black', lw=.6)
    ax.set_title(label)
    ax.set_ylabel('Conditional flux coefficient')
    ax.legend(fontsize=8, ncol=3)
axes[-1].set_xlabel('Model index (18 offset/broadening settings; alternating broadening 0 / 0.4 pixel)')
fig.suptitle('Matched off-event controls: model settings are not posterior samples')
fig.savefig(out / 'controls.png', dpi=150)
save_json(out / 'plot-manifest.json', {'script_sha256': sha(Path(__file__)), 'results_sha256': sha(out / 'results.json'), 'plot_sha256': sha(out / 'controls.png')})
