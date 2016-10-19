import ujson, os

DATADIR = 'rawdata/'

# load summaries
summaries = {}
for subdir in os.listdir(DATADIR):
    print subdir
    for userid in os.listdir(os.path.join(DATADIR, subdir)):
        summaries[userid] = {}
        for projectname in os.listdir(os.path.join(DATADIR, subdir, userid)):
            if projectname.endswith('_summary.json'):
                summaries[userid][projectname.rsplit('_', 1)[0]] = ujson.load(open(os.path.join(DATADIR,
                                                                                                subdir,
                                                                                                userid,
                                                                                                projectname)))


print 'Loaded summaries for', len(summaries), 'users'
print sum(map(len, summaries.values())), 'projects'

with open('user_project_summaries.json', 'w') as o:
    ujson.dump(summaries, o, indent=2)
