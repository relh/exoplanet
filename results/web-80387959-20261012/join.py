from query import query
V='https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync';G='https://datacentral.org.au/vo/tap/sync'
for t in ['xgaiae3','repeats','madera']:
 query('rave-'+t+'-schema',V,f"select column_name,datatype,unit,description from TAP_SCHEMA.columns where table_name='\"III/283/{t}\"'")
query('galah-cone',G,"select sobject_id,tmass_id,gaiadr3_source_id,ra,dec from galah_dr4.mainstartable where 1=CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',165.31041473672,-48.6136321332977,0.0166666667))")
