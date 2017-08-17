import ujson
import time
from collections import defaultdict
import sys

thresh = int(sys.argv[1])

allnames = ujson.load(open('user_project_allblockcounts.json'))
projectnames = {user: ['_'.join(project.split('_')[2:]) for project in allnames[user]] for user in allnames}
projectnames = {user: set([projectname for projectname in projectnames[user] if len(projectname)>5]) for user in projectnames}

namecounts = defaultdict(int)
start = time.time()
for user in projectnames:
    for project in projectnames[user]:
        namecounts[project] += 1

remove = [name for name, count in namecounts.items() if count >= thresh]

with open('common_names{0}.json'.format(thresh), 'w') as o:
    ujson.dump(remove, o, indent=1)
