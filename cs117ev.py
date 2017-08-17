from __future__ import division
import ujson
import numpy as np
import sys

simthresh = int(sys.argv[1])

hypnon = ujson.load(open('user_hypnontutorial_projects{0}.json'.format(simthresh)))
hypnonids = {user: set(['_'.join(project.split('_')[:2]) for project in hypnon[user]]) for user in hypnon}

manual = ujson.load(open('cs117annotated.json'))
for k in ['original', 'unoriginal']:
    manual[k] = set(manual[k])

manual_all = manual['original'].union(manual['unoriginal'])

hyp_original = set()
hyp_unoriginal = set()

project_names = ujson.load(open('cs117_project_names.json'))

# original
for user in hypnonids:
    for project in hypnonids[user]:
        userproject = user+'-'+project
        if userproject in manual_all:
            hyp_original.add(userproject)

# unoriginal
for userproject in manual_all:
    user = userproject[:5]
    project = userproject[6:]
    if project not in hypnonids[user]:
        hyp_unoriginal.add(userproject)

true_original = len(manual['original'].intersection(hyp_original))
true_unoriginal = len(manual['unoriginal'].intersection(hyp_unoriginal))
print 'True original', true_original
print 'True unoriginal', true_unoriginal

precision = true_original/len(hyp_original)
recall = true_original/len(manual['original'])

print 'Recall', recall
print 'Precision', precision
