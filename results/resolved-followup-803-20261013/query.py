import requests,json,hashlib,datetime, pathlib,io,csv
R=pathlib.Path('results/resolved-followup-803-20261013'); D=pathlib.Path('data/resolved-followup-803-20261013')
def query(name,url,adql):
 t=datetime.datetime.now(datetime.timezone.utc).isoformat(); r=requests.get(url,params={'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':adql},timeout=120);p=D/(name+'.csv');p.write_bytes(r.content)
 out={'url':r.url,'utc':t,'status':r.status_code,'sha256':hashlib.sha256(r.content).hexdigest(),'path':str(p),'query':adql,'rows':list(csv.DictReader(io.StringIO(r.text))) if r.ok and not r.text.lstrip().startswith('<') else [],'error':r.text[:1000] if not r.ok or r.text.lstrip().startswith('<') else None};(R/(name+'.json')).write_text(json.dumps(out,indent=2));print(name,r.status_code,len(out['rows']));return out
if __name__=='__main__':
 ids='5362389543781401216,5362389543781400192,5362389509421660800';url='https://gea.esac.esa.int/tap-server/tap/sync'
 query('gaia',url,f'SELECT source_id,ra,dec,pmra,pmdec,phot_g_mean_mag,phot_variable_flag,has_epoch_photometry,ruwe,non_single_star FROM gaiadr3.gaia_source WHERE source_id IN ({ids})')
 query('gaia-class',url,f'SELECT * FROM gaiadr3.vari_classifier_result WHERE source_id IN ({ids})')
 query('skymapper-metadata','https://api.skymapper.nci.org.au/public/tap/sync',"SELECT object_id,raj2000,dej2000 FROM dr4.master WHERE 1=CONTAINS(POINT('ICRS',raj2000,dej2000),CIRCLE('ICRS',165.298890344901,-48.6198214730704,0.000833333333))")
