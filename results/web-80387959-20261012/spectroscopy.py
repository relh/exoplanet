from query import query
V='https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync';G='https://datacentral.org.au/vo/tap/sync'
query('rave-schema',V,"select column_name,datatype,unit,description from TAP_SCHEMA.columns where table_name='\"III/283/ravedr6\"'")
query('galah-schema',G,"select column_name,datatype,unit,description from TAP_SCHEMA.columns where table_name='galah_dr4.mainstartable'")
query('rave-cone',V,"select * from \"III/283/ravedr6\" where 1=CONTAINS(POINT('ICRS',RAJ2000,DEJ2000),CIRCLE('ICRS',165.31041473672,-48.6136321332977,0.0166666667))")
