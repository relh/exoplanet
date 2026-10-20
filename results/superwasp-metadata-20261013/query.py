import json,pathlib,datetime,hashlib
from access import get,R
p=json.loads((R/'plan.json').read_text()); targets=p['targets']+[{'tic':'control','ra':15*(6+39/60+54.26/3600),'dec':35+31/60+25.7/3600}]
cols='sourceid,ra,dec,npts,obsstart,obsstop,hjdstart,hjdstop,hjd_ref,wasp_mag,tm_mean,tm_stddevwrtmean,tm_median,tm_stddevwrtmed,tm_medabsdev,tile'
qs=[]
for t in targets:
 q=f"select {cols} from superwasptimeseries where contains(point('ICRS',ra,dec),circle('ICRS',{t['ra']},{t['dec']},{p['radius_arcsec']/3600}))=1"
 qs.append({'target':t,'query':q})
a=R/'queries.json';assert not a.exists();a.write_text(json.dumps({'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'queries':qs},indent=2)+'\n');(R/'queries.sha256').write_text(hashlib.sha256(a.read_bytes()).hexdigest()+'  queries.json\n')
for x in qs:get('cone-'+str(x['target']['tic']),'https://exoplanetarchive.ipac.caltech.edu/TAP/sync',{'query':x['query'],'format':'json','MAXREC':10000})
