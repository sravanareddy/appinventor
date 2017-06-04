"""Remove projects that are similar to many others"""

import ujson
import sys
from collections import defaultdict
from math import sqrt

SIM = 0.03
SIMANG = sqrt(2*SIM)

def find_hubs(filename):
    user_hyptutorial_projects = defaultdict(set)
    graph = ujson.load(open(filename))

    prevfiltered = defaultdict(set)
    for project1 in graph:
        user1, project1name = project1.split('-', 1)

        prevfiltered[user1].add(project1name)

        identical = [(project2.split('-', 1), sim) for project2, sim in graph[project1] if sim <= SIMANG ]
        if len(identical)>=3 and len(set([user2 for (user2, project2name), sim in identical]))>=3:
            user_hyptutorial_projects[user1].add(project1name)
            for (user2, project2name), _ in identical:
                user_hyptutorial_projects[user2].add(project2name)

    user_hypnontutorial_projects = {}
    for user in prevfiltered:
        user_hypnontutorial_projects[user] = prevfiltered[user] - user_hyptutorial_projects[user]

    with open('user_hyporiginal_projects.json', 'w') as o:
        ujson.dump(user_hypnontutorial_projects, o, indent=1)

    print len(user_hypnontutorial_projects)

if __name__=='__main__':
    find_hubs(sys.argv[1])
