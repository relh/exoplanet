"""Reconstruct raw preprocessing/refinement and independently check fixed depths."""
import json
from pathlib import Path
import numpy as np
from exoplanet.followup import refine_training
from exoplanet.pipeline import sha,now,save_json
from run import O,load

def depth(y,e,a,b):
    if a.sum()<2 or b.sum()<5:return None
    # Explicit precision sums, independently of fixed_measure/depth_measure.
    wa=np.reciprocal(np.square(e[a]));wb=np.reciprocal(np.square(e[b]))
    d=float(np.dot(y[b],wb)/wb.sum()-np.dot(y[a],wa)/wa.sum());err=float(np.sqrt(1/wa.sum()+1/wb.sum()))
    return dict(depth=d,error=err,snr=d/err,n=int(a.sum()))
def measurement(t,y,e,clock,saved):
    p,ep,d=clock['period'],clock['transit_time'],clock['duration'];phase=(t-ep+p/2)%p-p/2;event=np.rint((t-ep)/p).astype(int);a=abs(phase)<d/2;b=(abs(phase)>d)&(abs(phase)<min(3*d,p/2));total=depth(y,e,a,b)
    assert (total is None)==(saved['total'] is None)
    if total:
        for k in total:np.testing.assert_allclose(total[k],saved['total'][k],rtol=1e-8,atol=1e-10)
    events=[]
    for n in np.unique(event[a]):
        z=depth(y,e,a&(event==n),b&(event==n))
        if z:events.append((int(n),z))
    assert len(events)==len(saved['events']);supported=0
    for (n,z),s in zip(events,saved['events']):
        assert n==s['event']
        for k in z:np.testing.assert_allclose(z[k],s[k],rtol=1e-8,atol=1e-10)
        supported+=z['snr']>=2
    assert supported==saved['supported_events']
    return total,supported
p=json.loads((O/'plan.json').read_text());r=json.loads((O/'results.json').read_text());assert r['plan_sha256']==sha(O/'plan.json')
assert len(r['rows'])==6
for path,h in p['source_hashes'].items():assert sha(Path(path))==h
for path,m in p['raw'].items():assert sha(Path(path))==m['sha256']
checks=[]
for row in r['rows']:
    assert row['status']=='measured',row
    name=row['name'];f=json.loads((O/f'{name}-training.json').read_text());assert sha(O/f'{name}-training.json')==row['training_sha256'];assert p['created_utc']<=f['created_utc']<=row['scored_utc'];assert not set(row['excluded'])&set(row['training']);assert sorted(row['excluded']+row['training'])==[9,10,36,37,63,64]
    t,y,e,_=load(row['training'],row['window']);tt,yy,ee,_=load(row['excluded'],row['window']);z=np.load(O/f'{name}.npz')
    for key,a in dict(t=t,y=y,e=e,tt=tt,yy=yy,ee=ee).items():np.testing.assert_array_equal(a,z[key])
    best,ranges=refine_training(t,y,e,p['seed'],seed_baseline=p['seed_baseline']);assert best==f['best']==row['best'];assert ranges==f['ranges']
    _,ns=measurement(t,y,e,best,f['measurement']);total,nh=measurement(tt,yy,ee,best,row['measurement']);measurement(tt,yy,ee,p['seed'],row['seed_reference'])
    epochs=np.rint((np.array([tt.min(),tt.max()])-best['transit_time'])/best['period']);offsets=[]
    for period,epoch in ranges['profile_timing_pairs']:
        epoch+=round((best['transit_time']-epoch)/period)*period
        offsets.extend(abs(epoch-best['transit_time']+epochs*(period-best['period'])))
    spread=max(offsets,default=0)+3*ranges['conditional_epoch_floor_days'];np.testing.assert_allclose(spread,row['timing_spread_days'])
    precise=spread<best['duration']/2 and not ranges['search_boundary_hit'] and ns>=3;expected=None if total is None else best['depth']/total['error'];assert precise==row['timing_precise']
    result='timing_prediction_inconclusive' if not precise else 'insufficient_coverage' if total is None else 'conditional_recovery_requires_further_vetting' if total['snr']>=5 and nh>=2 else 'not_recovered_despite_expected_sensitivity' if expected>=5 and total['snr']<2 else 'insufficient_evidence'
    assert result==row['conclusion'];np.testing.assert_allclose(expected,row['expected_formal_snr']);checks.append(name)
save_json(O/'verification.json',dict(created_utc=now(),status='passed',checks=checks,script_sha256=sha(Path(__file__)),scope='Six raw reconstructions, six shared-BLS training refits, eighteen independent fixed-clock total/event measurements, disjoint groups, clock provenance, freeze-before-score and six independently reconstructed timing/conclusion rules. Refitting shares BLS implementation; no independent physical validation or calibrated significance.'))
print('verified',checks)
