import ujson, os

DATADIR = 'rawdata/00'

# load summaries
summaries = {}
for userid in os.listdir(DATADIR):
    summaries[userid] = {}
    for projectname in os.listdir(os.path.join(DATADIR, userid)):
        if projectname.endswith('_summary.json'):
            summaries[userid][projectname.rsplit('_', 1)[0]] = ujson.load(open(os.path.join(DATADIR,
                                                                                           userid,
                                                                                           projectname)))


print 'Loaded summaries for', len(summaries), 'users'
print sum(map(len, summaries.values())), 'projects'

with open('user_project_summaries.json', 'w') as o:
    ujson.dump(summaries, o)


