"""Remove projects that are similar to many others"""

import ujson
import sys
from collections import defaultdict
from math import sqrt


def find_hubs(filename, simthresh):
    simang = sqrt(2*simthresh/100.)

    user_hyptutorial_projects = defaultdict(set)
    graph = ujson.load(open(filename))

    common_names = set(ujson.load(open('common_names30.json')))

    prevfiltered = defaultdict(set)
    for project1 in graph:
        user1, project1name = project1.split('-', 1)
        if '_'.join(project1name.split('_')[2:]) in common_names:
            user_hyptutorial_projects[user1].add(project1name)
            print project1name,
            continue

        prevfiltered[user1].add(project1name)

        identical = [(project2.split('-', 1), sim) for project2, sim in graph[project1] if sim <= simang ]
        if len(identical)>=3 and len(set([user2 for (user2, project2name), sim in identical]))>=3:
            user_hyptutorial_projects[user1].add(project1name)
            for (user2, project2name), _ in identical:
                user_hyptutorial_projects[user2].add(project2name)

    user_hyporiginal_projects = {}
    for user in prevfiltered:
        user_hyporiginal_projects[user] = prevfiltered[user] - user_hyptutorial_projects[user]

    with open('user_hyporiginal_projects{0}.json'.format(simthresh), 'w') as o:
        ujson.dump(user_hyporiginal_projects, o, indent=1)

    print len(user_hyporiginal_projects)

if __name__=='__main__':
    find_hubs(sys.argv[1], int(sys.argv[2]))
