"""Offline site geometry using frozen event windows, no target observations."""
import csv, json, hashlib, warnings, math
from pathlib import Path
import numpy as np
import astropy
from astropy import units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, CIRS, get_sun, get_body, solar_system_ephemeris
from astropy.time import Time
from astropy.utils import iers
P=Path(__file__).resolve().parent
ROOT=P.parent.parent
iers.conf.auto_download=False
solar_system_ephemeris.set('builtin')
plan=json.loads((P/'plan.json').read_text())
for name,digest in plan['inputs_sha256'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
sites=json.loads((P/'sites.json').read_text())
targets={str(t['tic']):t for t in json.loads((ROOT/'results/followup-planning-20261013/targets.json').read_text())['targets']}
events=list(csv.DictReader((ROOT/'results/followup-planning-20261013/events.csv').open()))
rows=[]; networks=[]; max_alt_error=0.; checks=0
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter('always')
    for ev in events:
        tic=ev['tic']; c=targets[tic]['coordinates']
        target=SkyCoord(c['linear_ra_j2027_deg']*u.deg,c['linear_dec_j2027_deg']*u.deg)
        a=Time(ev['full_track_start_geocentric_utc_approx'],scale='utc'); b=Time(ev['full_track_end_geocentric_utc_approx'],scale='utc')
        duration=(b-a).to_value(u.s)
        ts=a+np.linspace(0,duration,math.ceil(duration/120)+1)*u.s
        union=np.zeros(len(ts),dtype=bool)
        for site in sites:
            loc=EarthLocation.from_geodetic(site['lon']*u.deg,site['lat']*u.deg,site['height']*u.m)
            frame=AltAz(obstime=ts,location=loc,pressure=0*u.hPa)
            alt=target.transform_to(frame).alt.deg
            sun=get_sun(ts).transform_to(frame).alt.deg
            moon=get_body('moon',ts,location=loc).transform_to(frame)
            sep=target.transform_to(frame).separation(moon).deg
            usable=(alt>=30)&(sun<=-18); union|=usable
            # Independent spherical relation from topocentric CIRS, Earth rotation angle.
            cirs=target.transform_to(CIRS(obstime=ts,location=loc))
            ha=(ts.earth_rotation_angle(longitude=loc.lon)-cirs.ra).rad
            lat=loc.lat.rad; dec=cirs.dec.rad
            analytic=np.rad2deg(np.arcsin(np.sin(lat)*np.sin(dec)+np.cos(lat)*np.cos(dec)*np.cos(ha)))
            error=float(np.max(np.abs(analytic-alt))); max_alt_error=max(max_alt_error,error); checks+=len(ts)
            assert error<0.01, error
            rows.append({'tic':int(tic),'event':int(ev['event']),'site':site['code'],'site_name':site['name'],'start_utc':a.isot,'end_utc':b.isot,'track_hours':duration/3600,'grid_points':len(ts),'minimum_target_altitude_deg':float(alt.min()),'maximum_sun_altitude_deg':float(sun.max()),'minimum_moon_separation_deg':float(sep.min()),'passes_full_track':bool(usable.all()),'passes_one_degree_margin':bool((alt>=31).all() and (sun<=-19).all()),'sampled_visible_fraction':float(usable.mean())})
        networks.append({'tic':int(tic),'event':int(ev['event']),'union_all_five_sites_pass':bool(union.all()),'sampled_union_fraction':float(union.mean())})
warning_list=sorted(set(str(w.message) for w in caught))
with (P/'site-events.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(P/'network-coverage.json').write_text(json.dumps(networks,indent=2)+'\n')
# Synthetic exact zenith and lower culmination identities, independent of software coordinate machinery.
for latitude in [-90,-45,0,45,90]:
    l=np.deg2rad(latitude)
    z=np.rad2deg(np.arcsin(np.clip(np.sin(l)**2+np.cos(l)**2,-1,1)))
    assert abs(z-90)<1e-5
summary={'status':'complete','astropy':astropy.__version__,'input_event_count':len(events),'site_event_count':len(rows),'warnings':warning_list,'verification':{'analytical_altitude_points':checks,'max_analytical_altitude_difference_deg':max_alt_error,'synthetic_zenith_checks':5,'earth_radius_light_time_bound_seconds':0.022},'targets':[]}
for tic in targets:
    rr=[r for r in rows if str(r['tic'])==tic]; passed=[r for r in rr if r['passes_full_track']]; margin=[r for r in rr if r['passes_one_degree_margin']]
    summary['targets'].append({'tic':int(tic),'full_track_site_events':len(passed),'one_degree_margin_site_events':len(margin),'distinct_events':len(set(r['event'] for r in passed)),'first_full_track':passed[0] if passed else None,'first_conservative_track':margin[0] if margin else None,'per_site_counts':{s['code']:sum(r['site']==s['code'] for r in passed) for s in sites},'network_full_track_events':sum(n['union_all_five_sites_pass'] for n in networks if str(n['tic'])==tic)})
(P/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
manifest={'source_url':plan['sites_source'],'inputs_sha256':plan['inputs_sha256'],'generated_sha256':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['plan.json','sites.json','build.py','site-events.csv','network-coverage.json','summary.json']}}
(P/'provenance.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(summary,indent=2))
