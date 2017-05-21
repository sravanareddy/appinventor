from __future__ import division
import ujson
from scipy.spatial.distance import pdist
from sklearn.preprocessing import Binarizer
from sklearn.neighbors import BallTree
from sklearn.feature_extraction import DictVectorizer
import time
import networkx as nx
import numpy as np

def print_datastats(blockcounts):
    print len(blockcounts), 'users and', sum(map(len, blockcounts.values())), 'projects'

def user_project_filter(counts, user_project_set):
    """only keep projects in user_project_set in counts"""
    filtered_counts = {}
    for user in counts:
        orig = set(user_project_set[user]) if user in user_project_set else set()
        if len(orig)>=10:   # keep users who are active after removing projects
            filtered_counts[user] = {project: counts[user][project] for project in counts[user] if project in orig}
    return filtered_counts

def jaccardsim(v1, v2):
    return np.sum(np.minimum(v1, v2))/np.sum(np.maximum(v1, v2))

def vectorize(binarize=False):
    # pre-compute block-count array for each project
    all_projects = []
    project_names = []
    for user in blockcounts:
        for project in blockcounts[user]:
            if user in nontutorials and project in nontutorials[user]:
                all_projects.append(blockcounts[user][project])
                project_names.append(user+'-'+project)

    vectorizer = DictVectorizer()
    project_vectors = vectorizer.fit_transform(all_projects)
    if binarize:
        binarizer = Binarizer()
        project_vectors = binarizer.fit_transform(project_vectors)
    print 'Vectorized'
    print project_vectors.shape
    return project_vectors, vectorizer.vocabulary_, project_names

def write_pairwise(project_vectors, project_names, outfile):
    distances = {}
    G = nx.Graph()
    for i, project1 in enumerate(project_names):
        for j, project2 in enumerate(project_names[i+1:]):
            if project1[:5]!=project2[:5]: # should be different users
                sim = jaccardsim(project_vectors[i], project_vectors[i+j+1, :])
                if sim>=0.5:
                    G.add_edge(project1, project2, weight=sim)
        if (i+1)%5==0:
            print i+1,
    print 'Computed similarities'
    neighbors = {}
    for project in project_names:
        if G.has_node(project) and G.degree(project)>=5:
            neighbors[project] = G[project]
    with open(outfile, 'w') as o:
        ujson.dump(neighbors, o)

if __name__=='__main__':
    # loads pre-computed counts of each active block type per project for every user
    blockcounts = ujson.load(open('user_project_allblockcounts.json'))
    print_datastats(blockcounts)
    # load non-tutorials
    nontutorials = ujson.load(open('user_nontutorial_projects.json'))
    # filter non-tutorials
    blockcounts = user_project_filter(blockcounts, nontutorials)
    print_datastats(blockcounts)
    # vectorize
    project_vectors, vocab, project_names = vectorize()
    # compute similarities
    write_pairwise(project_vectors[:5000].todense(), project_names[:5000], 'all.neighbors')
