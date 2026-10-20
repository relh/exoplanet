"""Build an auditable target/sector inventory; never infer novelty from coverage."""
import argparse
import csv
import json
from pathlib import Path
import re
from concurrent.futures import ThreadPoolExecutor

from .pipeline import fetch, save_json, now


def sector_inventory(root, workers=4):
    """Discover all ordinary sector target-list links on the official HLSP page."""
    page = root / 'tess-spoc.html'
    page_info = fetch('https://archive.stsci.edu/hlsp/tess-spoc', page)
    links = re.findall(r'https?://archive\.stsci\.edu/hlsps/tess-spoc/target_lists/s\d+\.csv', page.read_text())
    links = sorted(set(url.replace('http:', 'https:') for url in links))
    if not links:
        raise ValueError('No sector lists found')

    def one(url):
        sector = int(re.search(r'/s(\d+)\.csv', url)[1])
        path = root / 'sectors' / f's{sector:04d}.csv'
        try:
            evidence = fetch(url, path)
            with path.open() as stream:
                rows = list(csv.DictReader(stream))
            if not rows or '#TIC_ID' not in rows[0]:
                raise ValueError('Unexpected target-list schema')
            ids = [int(row['#TIC_ID']) for row in rows]
            print(f'Sector {sector}: {len(ids)} targets', flush=True)
            return sector, ids, evidence
        except Exception as exc:
            print(f'Sector {sector}: {exc}', flush=True)
            return sector, None, {'error': f'{type(exc).__name__}: {exc}', 'url': url}

    mapping, evidence = {}, {}
    with ThreadPoolExecutor(workers) as pool:
        for sector, ids, info in pool.map(one, links):
            evidence[str(sector)] = info
            if ids is not None:
                for tic in ids:
                    mapping.setdefault(tic, []).append(sector)
    save_json(root / 'sector-provenance.json', {'created_utc': now(), 'page': page_info, 'sectors': evidence})
    # CSV keeps this broad inventory much smaller than JSON.
    with (root / 'coverage.csv').open('w') as stream:
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(['tic', 'sectors'])
        for tic, sectors in sorted(mapping.items()):
            writer.writerow([tic, ' '.join(map(str, sorted(sectors)))])
    return mapping


def fetch_small_stars(root):
    """TIC v8.2 query, fail closed on incomplete pagination or duplicate IDs."""
    import requests
    from .pipeline import sha
    request = {
        'service': 'Mast.Catalogs.Filtered.Tic.Rows',
        'params': {'columns': 'ID,ra,dec,Tmag,rad,Teff,d,contratio,disposition,duplicate_id',
            'filters': [
                {'paramName': 'rad', 'values': [{'min': 0.15, 'max': 0.8}]},
                {'paramName': 'Tmag', 'values': [{'min': 6, 'max': 12}]},
                {'paramName': 'd', 'values': [{'min': 0, 'max': 120}]},
            ]}, 'format': 'json', 'pagesize': 100000, 'page': 1}
    path = root / 'tic-small-stars.json'
    meta = root / 'tic-small-stars-provenance.json'
    if path.exists() and meta.exists():
        evidence = json.loads(meta.read_text())
        if sha(path) != evidence['sha256'] or evidence['request'] != request:
            raise ValueError('TIC cache mismatch')
    else:
        response = requests.post('https://mast.stsci.edu/api/v0/invoke',
            data={'request': json.dumps(request)}, timeout=(20, 180))
        response.raise_for_status()
        path.write_text(response.text)
        evidence = {'url': response.url, 'request': request, 'retrieved_utc': now(),
                    'sha256': sha(path), 'bytes': path.stat().st_size}
        save_json(meta, evidence)
    result = json.loads(path.read_text())
    if result.get('status') != 'COMPLETE':
        raise ValueError(f'Incomplete TIC query: {result.get("status")}')
    rows = result['data']
    if len(rows) != result['paging']['rowsFiltered'] or len({r['ID'] for r in rows}) != len(rows):
        raise ValueError('TIC results truncated or duplicate IDs')
    # Independently enforce cuts, even if the remote query changes behavior.
    for r in rows:
        if not (.15 <= r['rad'] <= .8 and 6 <= r['Tmag'] <= 12 and 0 <= r['d'] <= 120):
            raise ValueError('TIC row does not satisfy requested cuts')
    return rows, evidence


def training_sectors(sectors):
    """Prefer earliest >=2 adjacent old sectors; reserve years >=56 untouched.

    Limit to three sectors to keep a dense blind search computationally bounded.
    Sector numbers are only a coarse scheduling proxy; actual time spans are
    checked at search time. This does not certify unsearched targets.
    """
    old = sorted(s for s in sectors if s <= 55)
    groups = []
    for sector in old:
        if not groups or sector != groups[-1][-1] + 1:
            groups.append([sector])
        else:
            groups[-1].append(sector)
    options = [g[:3] for g in groups if len(g) >= 2]
    return options[0] if options else []


def select_targets(root, output, limit=300):
    from .pipeline import catalogs
    import shutil
    output.mkdir(parents=True, exist_ok=False)
    stars, tic_evidence = fetch_small_stars(root)
    known, catalog_evidence = catalogs(Path('data'), output)
    extra = {
        'ctoi': ('https://exofop.ipac.caltech.edu/tess/download_ctoi.php?sort=ctoi&output=csv', 'TIC ID'),
        'eb': ('https://archive.stsci.edu/hlsps/tess-ebs/hlsp_tess-ebs_tess_lcf-ffi_s0001-s0026_tess_v1.0_cat.csv', 'tess_id')}
    for name, (url, key) in extra.items():
        path = root / f'{name}.csv'
        catalog_evidence[name] = fetch(url, path)
        with path.open() as stream:
            rows = list(csv.DictReader(stream))
        if not rows or key not in rows[0]:
            raise ValueError(f'Invalid {name} schema')
        for row in rows:
            known.setdefault(int(row[key]), []).append({'catalog': name, **row})
        shutil.copyfile(path, output / f'catalog_{name}.csv')
    with (root / 'coverage.csv').open() as stream:
        coverage = {int(r['tic']): [int(s) for s in r['sectors'].split()] for r in csv.DictReader(stream)}
    eligible, counts = [], {}
    for star in stars:
        reason = None
        tic = int(star['ID'])
        sectors = coverage.get(tic, [])
        training = training_sectors(sectors)
        heldout = [s for s in sectors if s >= 56]
        if tic in known: reason = 'known_catalog_match'
        elif str(star.get('disposition') or '').upper() in {'ARTIFACT','DUPLICATE','SPLIT'}: reason = 'tic_disposition'
        elif star.get('duplicate_id'): reason = 'duplicate_id'
        elif star.get('contratio') is None or star['contratio'] > .2: reason = 'contamination_or_missing'
        elif star.get('Teff') is None or star['Teff'] > 5300: reason = 'temperature_or_missing'
        elif not training or not heldout: reason = 'insufficient_training_or_holdout'
        if reason:
            counts[reason] = counts.get(reason, 0) + 1
            continue
        score = star['rad']**2 * 10**(.2 * (star['Tmag'] - 10)) / len(training)**.5
        eligible.append({'tic': tic, 'star': star, 'sectors': sectors,
            'training_sectors': training, 'heldout_sectors': heldout,
            'priority_noise_proxy': score})
    eligible.sort(key=lambda x:(x['priority_noise_proxy'], x['tic']))
    save_json(output / 'eligible.json', eligible)
    save_json(output / 'selected.json', eligible[:limit])
    shutil.copyfile(root/'sector-provenance.json',output/'sector-provenance.json')
    save_json(output / 'selection.json', {'created_utc':now(),'tic':tic_evidence,
        'catalogs':catalog_evidence,'n_stars':len(stars),'exclusions':counts,
        'n_eligible':len(eligible),'n_selected':min(limit,len(eligible)),
        'rule':'radius 0.15..0.8 solar; Tmag 6..12; distance <=120pc; contamination <=0.2; Teff<=5300; >=2 adjacent sectors <=55 and >=1 sector >=56; no matched TOI/confirmed/CTOI/archived EB TIC',
        'ranking':'radius^2 * 10^(0.2*(Tmag-10)) / sqrt(number of training sectors); photometric noise proxy, not measured quietness',
        'coverage_limit':'All target lists linked by the fetched MAST TESS-SPOC page; not all TESS products or all observing sectors',
        'eb_limit':'MAST v1.0 EB catalog only; current Villanova and positional checks still required for promising signals'})
    print(f'{len(eligible)} eligible; selected {min(limit,len(eligible))}', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('data/targeting'))
    parser.add_argument('--output', type=Path)
    parser.add_argument('--limit', type=int, default=300)
    parser.add_argument('--inventory', action='store_true', help='Build/recheck sector inventory')
    args = parser.parse_args()
    if args.limit < 1:
        parser.error('limit must be positive')
    if args.inventory or not (args.root / 'coverage.csv').exists():
        mapping = sector_inventory(args.root)
        print(f'{len(mapping)} unique stars across available target lists', flush=True)
    if args.output:
        select_targets(args.root, args.output, args.limit)


if __name__ == '__main__':
    main()
