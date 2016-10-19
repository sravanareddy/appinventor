import ujson, os

DATADIR = 'rawdata/'

# load summaries
with open('user_project_summaries.json', 'w') as o:
    for subdir in os.listdir(DATADIR):
        summaries = {}
        for i, userid in enumerate(os.listdir(os.path.join(DATADIR, subdir))):
            if (i+1)%50==0:
                print '.',
            summaries[userid] = {}
            for projectname in os.listdir(os.path.join(DATADIR, subdir, userid)):
                if projectname.endswith('_summary.json'):
                    summaries[userid][projectname.rsplit('_', 1)[0]] = ujson.load(open(os.path.join(DATADIR,
                                                                                                subdir,
                                                                                                userid,
                                                                                                projectname)))
        o.write(ujson.dumps(summaries))
        o.write('\n')
        print subdir
