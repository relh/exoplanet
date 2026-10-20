from query import query
V='https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync';G='https://datacentral.org.au/vo/tap/sync'
query('galah-target',G,"select * from galah_dr4.mainstartable where gaiadr3_source_id=5362389543781401216 or tmass_id='11011449-4836490'")
query('rave-all-tables',V,"select table_name,description from TAP_SCHEMA.tables where table_name like '%III/283/%'")
