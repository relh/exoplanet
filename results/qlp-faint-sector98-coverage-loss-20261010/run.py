"""Trace injected event coverage through the unchanged QLP preprocessing."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import save_json, sha, now
from exoplanet.archive import qlp_flux_columns
from exoplanet.qlp_campaign import bin_curve, empirical_errors
from exoplanet.search import flatten
from exoplanet.transit_model import integrated_box

out = Path(__file__).parent
parent = Path('results/qlp-faint-sector98-long-injections-20261010')
assert not (out/'results.json').exists()
records = []
for row in json.loads((parent/'results.json').read_text()):
    if row['radius_earth'] != 2:
        continue
    source = Path(f"data/qlp/{row['tic']}-s0098.fits")
    with fits.open(source) as h:
        d = h[1].data
        fc, ec, _ = qlp_flux_columns(d.names)
        raw, flux, err = [np.array(d[k], dtype=float) for k in ['TIME', fc, ec]]
        good = (d['QUALITY'] == 0) & np.isfinite(raw) & np.isfinite(flux) & (flux > 0)
        if not np.any(good & np.isfinite(err) & (err > 0)):
            ix = np.flatnonzero(good); ix = ix[np.argsort(raw[ix])]
            err[good] = empirical_errors(raw[ix], flux[ix])[0]
        good &= np.isfinite(err) & (err > 0)
        t, y, e = raw[good], flux[good], err[good]
        ix = np.argsort(t); t, y, e = t[ix], y[ix], e[ix]
    factor = 1-row['depth']*integrated_box(t, row['period'], row['epoch'], row['duration'], float(np.median(np.diff(t))))
    bt, by, be = bin_curve(t, y*factor, e*factor)
    clean = {str(w): flatten(bt, by, be, window=w)[0] for w in [1.5, 2.5]}
    times = {'raw_finite': raw[np.isfinite(raw)], 'quality_flux_error_valid': t, 'binned': bt,
             **{f'clean_window_{w}': v for w, v in clean.items()}}
    events = []
    start, stop = np.nanmin(raw), np.nanmax(raw)
    for phase in [0., .5]:
        origin = row['epoch'] + phase*row['period']
        for cycle in range(int(np.ceil((start-origin)/row['period'])), int(np.floor((stop-origin)/row['period']))+1):
            center = origin + cycle*row['period']
            counts = {}
            for name, tt in times.items():
                dt = np.abs(tt-center)
                counts[name] = {'inside': int(np.sum(dt < row['duration']/2)),
                                'local_baseline': int(np.sum((dt > row['duration']) & (dt < 3*row['duration'])))}
            events.append({'phase': phase, 'cycle': cycle, 'center_btjd': center, 'counts': counts})
    records.append({'tic': row['tic'], 'period': row['period'], 'injection': row,
                    'source': str(source), 'source_sha256': sha(source), 'events': events,
                    'stage_counts': {k: len(v) for k, v in times.items()}})
save_json(out/'results.json', {'utc': now(), 'script_sha256': sha(Path(__file__)),
    'injection_results_sha256': sha(parent/'results.json'), 'records': records,
    'interpretation': 'Coverage counts at injected primary and half-period phases, not fitted ephemerides. No search rerun or gate change. Two-Earth-radius subset; windows and original flux/error behavior unchanged. Counts alone do not measure event significance or establish a cause for alternate detrending.'})
for r in records:
    print(r['tic'], r['period'], [(x['phase'], x['cycle'], [v['inside'] for v in x['counts'].values()]) for x in r['events']])
