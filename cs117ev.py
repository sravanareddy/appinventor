from __future__ import division
import ujson
import numpy as np

SIM = 0.03
print SIM

manual = ujson.load(open('cs117annotated.json'))

hypnon = ujson.load(open('user_hypnontutorial_projects.json'))
hypnon = {user: set(['_'.join(project.split('_')[:2]) for project in hypnon[user]]) for user in hypnon}

false_original = set()
false_unoriginal = set()

cd = np.loadtxt('cs117_tutsim.npytxt') # distances between cs117 projects and tutorials
project_names = ujson.load(open('cs117_project_names.json'))

tutorial_unoriginal = set()
for i, project in enumerate(project_names):
    if cd[i].min() <= SIM:
        tutorial_unoriginal.add(project)

for user in hypnon:
    for project in hypnon[user]:
        userproject = user+'-'+project
        if userproject in manual['unoriginal']:
            false_original.add(userproject)

for userproject in manual['original']:
    user = userproject[:5]
    project = userproject[6:]
    if project not in hypnon[user] or project in tutorial_unoriginal:
        false_unoriginal.add(userproject)

print 1-len(false_original)/len(manual['unoriginal'])
print 1-len(false_unoriginal)/len(manual['original'])
print 1-(len(false_unoriginal)+len(false_original))/(len(manual['unoriginal'])+len(manual['original']))
