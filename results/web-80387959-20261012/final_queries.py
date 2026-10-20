from query import query
V='https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync';G='https://datacentral.org.au/vo/tap/sync'
query('rave-gaia-join',V,'select * from "III/283/xgaiae3" where Gaiae3=5362389543781401216')
query('rave-repeats',V,"select * from \"III/283/repeats\" where ID='J110114.5-483649'")
query('rave-madera',V,"select * from \"III/283/madera\" where ObsID='20100502_1050m50_094'")
query('galah-box',G,'select sobject_id,tmass_id,gaiadr3_source_id,ra,dec from galah_dr4.mainstartable where ra between 165.284 and 165.337 and dec between -48.631 and -48.596')
