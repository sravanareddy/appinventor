from sklearn.datasets import load_svmlight_file
from scipy.spatial.distance import cdist
import ujson
import numpy as np
import sys

simthresh = int(sys.argv[1])

hyporiginal = ujson.load(open('user_hyporiginal_projects{0}.json'.format(simthresh)))

project_vectors, _ = load_svmlight_file('project_vectors.svml')
project_names = np.array(ujson.load(open('project_names.json')))
tut_vectors, _ = load_svmlight_file('knowntutorial_vectors.svml')
project_vectors = project_vectors.todense()
tut_vectors = tut_vectors.todense()
extra_cols = np.zeros((tut_vectors.shape[0], project_vectors.shape[1]-tut_vectors.shape[1]))
tut_vectors = np.hstack((tut_vectors, extra_cols))
print 'Loaded'

cd = cdist(project_vectors, tut_vectors, metric='cosine')
cdmin = cd.min(axis=1)
tooclose = set(project_names[cdmin<=simthresh/100.])
print len(tooclose)

user_hypnontutorial_projects = {}
for user in hyporiginal:
    user_hypnontutorial_projects[user] = set()
    for project in hyporiginal[user]:
        if user+'-'+project not in tooclose:
            user_hypnontutorial_projects[user].add(project)

with open('user_hypnontutorial_projects{0}.json'.format(simthresh), 'w') as o:
    ujson.dump(user_hypnontutorial_projects, o, indent=1)
