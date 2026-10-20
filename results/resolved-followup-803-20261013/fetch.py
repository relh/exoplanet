from query import query
u='https://api.skymapper.nci.org.au/public/tap/sync'
r=query('photometry',u,'SELECT * FROM dr4.photometry WHERE object_id=411683754')
ids=','.join(sorted(set(x['image_id'] for x in r['rows'])))
if ids: query('images',u,f'SELECT * FROM dr4.images WHERE image_id IN ({ids})')
