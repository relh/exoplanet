import csv,json
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.time import Time
from PRF import TESS_PRF
from exoplanet.pixel_vet import difference_events
from exoplanet.prf_fit import fit_templates,fit_shift
from exoplanet.pipeline import save_json,sha,now

out=Path(__file__).parent
models=json.loads((out/'models.json').read_text())
frozen=Path('results/qlp-faint-midradius-single-review-20261011/422626648-peak0/frozen.json')
best=json.loads(frozen.read_text())['best']
gaia_path=Path('results/gaia-422626648-scene-20261011/gaia_source.json')
gaia={r['source_id']:r for r in json.loads(gaia_path.read_text())}
neighbor_path=Path('results/neighbors-422626648-20261011/neighbors.json')
stars=json.loads(neighbor_path.read_text())
host_ids=['422626648', '1178220390', '1178220382', '1178220387', '1178220389', '1178220385', '422626659', '1178220386', '1178220388', '1178220391', '422626636', '422626640', '1178220401']
gids=['6254811248843788416', '6254811248836563328', '6254811072743963776', '6254811180118959360', '6254811244541895680', '6254811141463441152', '6254811248843793792', '6254811141463447552', '6254811180124306048', '6254811278901638656', '6254811077045091456', '6254811111404833024', '6254811454996147840']
rows=[]
for meta in models['sectors']:
    sector=meta['sector']
    with fits.open(meta['pixel_path']) as h:
        d=h[1].data; wcs=WCS(h[2].header)
        t=np.asarray(d['TIME'],float); finite=np.isfinite(t);t=t[finite]
        flux=np.asarray(d['FLUX'][finite],float);err=np.asarray(d['FLUX_ERR'][finite],float)
        quality=d['QUALITY'][finite]; year=Time(2457000+np.median(t),format='jd').jyear
    prf=TESS_PRF(meta['camera'],meta['ccd'],sector,meta['col'],meta['row'],localdatadir='data/prf/start_s0004')
    positions={}; missing_pm=[]
    for tic,gid in zip(host_ids,gids):
        r=gaia[gid]
        if not r['pmra'] or not r['pmdec']: missing_pm.append(tic)
        dt=year-float(r['ref_epoch']); dec=float(r['dec'])
        ra=float(r['ra'])+dt*float(r['pmra'] or 0)/(3600000*np.cos(np.deg2rad(dec)))
        dec+=dt*float(r['pmdec'] or 0)/3600000
        positions[tic]=np.array(wcs.world_to_pixel_values(ra,dec))
    scene_ids=[];scene_pos=[]
    for star in sorted(stars,key=lambda s:s.get('Tmag') or 99):
        tic=str(star['ID'])
        if (star.get('Tmag') or 99)>18 and tic not in positions:continue
        if tic in positions: pos=positions[tic]
        else:
            # TIC ra/dec J2000; linear proper motion only, no parallax correction.
            dec=star['dec'];ra=star['ra']+(year-2000)*(star.get('pmRA') or 0)/(3600000*np.cos(np.deg2rad(dec)))
            dec+=(year-2000)*(star.get('pmDEC') or 0)/3600000
            pos=np.array(wcs.world_to_pixel_values(ra,dec))
        if np.all(pos>-1)&np.all(pos<np.array(flux.shape[1:][::-1])) and all(np.linalg.norm(pos-p)>.01 for p in scene_pos):
            scene_ids.append(tic);scene_pos.append(pos)
    phase=(t-best['transit_time']+best['period']/2)%best['period']-best['period']/2
    outside=(quality==0)&(abs(phase)>3*best['duration'])
    scene=np.nanmedian(flux[outside],axis=0)
    # Uniform scene weights: reference PRF mismatch dominates formal photon error.
    alignment=fit_shift(scene,np.ones(scene.shape),scene_pos,prf.locate)
    diff,sigma,events,numbers=difference_events(t,flux,err,quality,best)
    templates={tic:prf.locate(*(pos+alignment['shift']),scene.shape) for tic,pos in positions.items()}
    hypotheses=[]
    for tic,template in templates.items():
        f=fit_templates(diff,sigma,[template])
        hypotheses.append(dict(tic=tic,chi2=f['chi2'],dof=f['dof'],amplitude=float(f['coefficients'][0])))
    free=fit_shift(diff,sigma,[positions['422626648']+alignment['shift']],prf.locate,bound=1.2,nonnegative=False)
    # Deterministic matched-model injections test resolvability at actual formal
    # pixel errors. They do NOT include mission PRF mismatch or red noise.
    rng=np.random.default_rng(422626648+sector);injections=[]
    for tic,template in templates.items():
        amplitude=max(next(h['amplitude'] for h in hypotheses if h['tic']==tic),0)
        wins={k:0 for k in templates}
        for i in range(100):
            synthetic=amplitude*template+rng.normal(size=diff.shape)*sigma
            fs={k:fit_templates(synthetic,sigma,[v])['chi2'] for k,v in templates.items()}
            wins[min(fs,key=fs.get)]+=1
        injections.append(dict(injected_tic=tic,amplitude=amplitude,winners=wins))
    np.savez_compressed(out/f's{sector}-images.npz',scene=scene,scene_model=alignment['model'],difference=diff,error=sigma,free_model=free['model'],**{'template_'+k:v for k,v in templates.items()})
    row=dict(missing_pm_assumed_zero=missing_pm,sector=sector,year=year,scene_ids=scene_ids,positions={k:v.tolist() for k,v in positions.items()},scene_positions=np.array(scene_pos).tolist(),alignment=alignment['shift'].tolist(),alignment_boundary=alignment['boundary'],scene_fractional_rms=float(np.sqrt(np.mean((scene-alignment['model'])**2))/np.max(scene)),hypotheses=hypotheses,free_offset_from_target=free['shift'].tolist(),free_boundary=free['boundary'],free_chi2=free['chi2'],injections=injections,n_events=len(events))
    rows.append(row)
    save_json(out/'fits.json',dict(created_utc=now(),script_sha256=sha(Path(__file__)),module_sha256=sha(Path('src/exoplanet/prf_fit.py')),frozen_sha256=sha(frozen),gaia_sha256=sha(gaia_path),neighbors_sha256=sha(neighbor_path),sectors=rows,limitations='Conditional diagonal-error fits. Scene registration and PRF mismatch uncertainties not propagated; no host probabilities. Short clock is posthoc on opened sectors; no blind validation. Injection noise is independent and uses identical PRF, not empirical systematics. Proper motion linear; parallax ignored. Missing Gaia proper motions assumed zero, uncertain positions. Scene stars T<=18 plus all tested hosts, deduplicated within .01 pixel (both close hypotheses retained); faint/outside scene sources omitted.'))
    print(sector,'alignment',alignment['shift'],'hypotheses',hypotheses,'free',free['shift'],flush=True)
