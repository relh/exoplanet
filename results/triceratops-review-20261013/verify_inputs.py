"""Independent reconstruction of prepared TRICERATOPS inputs; no network calls."""
from pathlib import Path
import csv
import hashlib
import json

import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from scipy.special import erf

R = Path('results/triceratops-20261013')
OUT = Path('results/triceratops-review-20261013')
checks = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


plan = json.loads((R / 'plan.json').read_text())
for filename, expected in plan['inputs'].items():
    check('input hash: ' + filename,
          hashlib.sha256(Path(filename).read_bytes()).hexdigest() == expected)

summary = []
correction = json.loads((R / 'catalog-correction-plan.json').read_text())
for tic, sector in [(80387959, 36), (402358350, 54)]:
    meta = json.loads((R / f'{tic}-input.json').read_text())
    prepared = np.load(R / f'{tic}-input.npz')
    original = np.load(f'results/paper-host-vetting-20261012/{tic}-s{sector}-sap.npz')
    X, y, err = original['design'], original['flux'], original['error']
    weight = 1 / err**2
    beta = np.linalg.solve(X.T @ (weight[:, None] * X), X.T @ (weight * y))
    check(f'{tic}: baseline coefficients', np.allclose(beta, original['beta'], atol=2e-12))
    event_ids = np.unique(original['event'])
    baseline = np.empty(len(y))
    for i, event in enumerate(event_ids):
        mask = original['event'] == event
        baseline[mask] = beta[1 + 2*i] + beta[2 + 2*i] * original['dt'][mask] / meta['clock']['duration']
    reference = np.mean(beta[1::2])
    expected_flux = 1 + (y - baseline) / reference
    check(f'{tic}: normalized native SAP', np.allclose(prepared['flux'], expected_flux, atol=2e-12))
    check(f'{tic}: depth reference', np.isclose(meta['depth'], beta[0] / reference, atol=2e-12))
    clock = meta['clock']
    expected_dt = original['time'] - (clock['transit_time'] + original['event'] * clock['period'])
    check(f'{tic}: fixed clock in days', np.allclose(prepared['time'], expected_dt, atol=1e-10))
    check(f'{tic}: unchanged points', len(prepared['time']) == len(y) == meta['n'])
    noise_mask = abs(expected_dt) > clock['duration'] / 2
    expected_sigma = np.std(expected_flux[noise_mask] - 1, ddof=1)
    check(f'{tic}: noise estimate', np.isclose(expected_sigma, meta['sigma'], atol=1e-12))
    check(f'{tic}: finite positive uncertainty', np.isfinite(meta['sigma']) and meta['sigma'] > 0)

    with (R / f'{tic}-stars.csv').open() as stream:
        stars = list(csv.DictReader(stream))
    catalog_path = ('results/neighbors-80387959-20261009/tic-neighbors.json'
                    if tic == 80387959 else 'results/neighbors-402358350-20261011/neighbors.json')
    raw = {str(row['ID']): row for row in json.loads(Path(catalog_path).read_text())}
    corrected = next(row for row in correction['records'] if row['tic'] == tic)
    removed = {row['remove'] for row in corrected['duplicates']}
    with (R / 'original-catalog' / f'{tic}-stars.csv').open() as stream:
        original_stars = list(csv.DictReader(stream))
    check(f'{tic}: only declared duplicate rows removed',
          {row['ID'] for row in stars} == {row['ID'] for row in original_stars} - removed)
    for duplicate in corrected['duplicates']:
        dropped, retained = raw[duplicate['remove']], raw[duplicate['keep']]
        check(f'{tic}: explicit duplicate {duplicate["remove"]}', dropped['disposition'] == 'DUPLICATE')
        check(f'{tic}: counterpart {duplicate["remove"]}', str(dropped['duplicate_id']) == duplicate['keep'])
        check(f'{tic}: exact source identity {duplicate["remove"]}',
              all(dropped[key] == retained[key] for key in ['ra','dec','Tmag','GAIA']))
        check(f'{tic}: counterpart retained {duplicate["remove"]}', duplicate['keep'] in {row['ID'] for row in stars})
    for row in stars:
        expected_id = raw[row['ID']].get('GAIA')
        check(f'{tic}: exact Gaia identifier {row["ID"]}', row['GAIA'] == ('' if expected_id is None else str(expected_id)))
    check(f'{tic}: target is row zero', int(stars[0]['ID']) == tic)
    check(f'{tic}: unique target', sum(int(row['ID']) == tic for row in stars) == 1)
    with fits.open(f'data/lightcurves/s{sector:04d}-{tic}.fits') as hd:
        aperture = np.array([(x, yy) for yy in range(hd[2].data.shape[0])
                             for x in range(hd[2].data.shape[1]) if int(hd[2].data[yy, x]) & 2])
        coords = WCS(hd[2].header).all_world2pix(
            np.array([[float(row['ra']), float(row['dec'])] for row in stars]), 0)
        timedel = float(hd[1].header['TIMEDEL'])
        integration = float(hd[1].header['INT_TIME']) * int(hd[1].header['NUM_FRM'])
    check(f'{tic}: actual SPOC aperture', np.array_equal(aperture, prepared['aperture']))
    check(f'{tic}: WCS origin', np.allclose(coords, prepared['pix_coords'], atol=1e-9))
    check(f'{tic}: cadence within 1 second of header', abs(meta['exptime'] - timedel) * 86400 < 1)
    magnitudes = np.array([float(row['Tmag']) for row in stars])
    relative = 10**(-0.4*(magnitudes - magnitudes.min()))
    captured = []
    for (cx, cy), amplitude in zip(coords, relative):
        scale = 0.75 * np.sqrt(2)
        ix = 0.5 * (erf((aperture[:, 0]+0.5-cx)/scale) - erf((aperture[:, 0]-0.5-cx)/scale))
        iy = 0.5 * (erf((aperture[:, 1]+0.5-cy)/scale) - erf((aperture[:, 1]-0.5-cy)/scale))
        captured.append(amplitude * np.sum(ix * iy))
    fractions = np.array(captured) / np.sum(captured)
    saved_fractions = np.array([float(row['fluxratio']) for row in stars])
    check(f'{tic}: Gaussian flux fractions', np.allclose(fractions, saved_fractions, atol=1e-13))
    for row, fraction in zip(stars, fractions):
        required = meta['depth'] / fraction if fraction > 1e-15 else np.inf
        eligible = 0 < float(row['tdepth']) <= 1
        if fraction > 1e-15:
            check(f'{tic}: SAP depth convention {row["ID"]}',
                  np.isclose(float(row['tdepth']), required if required <= 1 else 0, atol=1e-9))
        else:
            check(f'{tic}: negligible flux excluded {row["ID"]}', not eligible)
    summary.append(dict(tic=tic, sector=sector, samples=len(y), events=len(event_ids),
                        depth=meta['depth'], sigma=meta['sigma'], catalog_rows=len(stars),
                        eligible_hosts=sum(float(row['tdepth']) > 0 for row in stars),
                        exptime_seconds=meta['exptime']*86400, header_cadence_seconds=timedel*86400,
                        integration_seconds=integration, modeled_target_fraction=fractions[0]))

(OUT / 'input-verification.json').write_text(json.dumps(dict(
    passed=len(checks), checks=checks, summaries=summary,
    limitation='Checks prepared arithmetic and conventions, not catalog accuracy, aperture response validity, correlated-noise coverage or planet probability.'), indent=2) + '\n')
print(json.dumps(dict(passed=len(checks), summaries=summary), indent=2))
