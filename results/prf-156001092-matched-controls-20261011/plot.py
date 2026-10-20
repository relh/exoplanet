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
for ax, key, label in zip(axes, ['target_amplitude', 'neighbor090_amplitude'], ['Target TIC156001092', 'Neighbor TIC156001090']):
    for j, row in enumerate(rows):
        values = [c[key] for c in row['controls']]
        ax.scatter(np.full(len(values), j), values, color='gray', alpha=.45, s=12, label='14 distinct control windows' if j == 0 else None)
        for event, color, marker in [(2, 'tab:blue', 'o'), (3, 'tab:orange', '^')]:
            value = next(e[key] for e in row['events'] if e['event'] == event)
            ax.scatter(j, value, color=color, marker=marker, s=30, label=f'Event {event}' if j == 0 else None)
    ax.axhline(0, color='black', lw=.6)
    ax.axvline(17.5, color='black', ls=':', lw=.7)
    ax.set_title(label)
    ax.set_ylabel('Conditional flux coefficient')
    ax.legend(fontsize=8, ncol=3)
axes[-1].set_xlabel('Archived model index (0–17: Gaia mapping 0; 18–35: mapping 1; alternating broadening 0 / 0.4 pixel)')
fig.suptitle('Matched off-event controls: model settings are not posterior samples')
fig.savefig(out / 'controls.png', dpi=150)
save_json(out / 'plot-manifest.json', {'script_sha256': sha(Path(__file__)), 'results_sha256': sha(out / 'results.json'), 'plot_sha256': sha(out / 'controls.png')})
