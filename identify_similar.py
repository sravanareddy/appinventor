from __future__ import division
import ujson
from scipy.spatial.distance import pdist
from sklearn.preprocessing import Binarizer
from sklearn.neighbors import BallTree
from sklearn.feature_extraction import DictVectorizer
import time
import networkx as nx
import numpy as np
import sys

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

def vectorize(blockcounts):
    # pre-compute block-count array for each project
    all_projects = []
    project_names = []
    for user in blockcounts:
        for project in blockcounts[user]:
            all_projects.append(blockcounts[user][project])
            project_names.append(user+'-'+project)

    vectorizer = DictVectorizer()
    project_vectors = vectorizer.fit_transform(all_projects)
    print 'Vectorized'
    print project_vectors.shape
    return project_vectors, vectorizer.vocabulary_, project_names

def pairwise(project_vectors, project_names, ann):
    distances = {}
    G = nx.Graph()

    if ann=='ball':
        binarizer = Binarizer()
        project_vectors_bin = binarizer.fit_transform(project_vectors)
        print 'Binarized'

        tree = BallTree(project_vectors_bin, metric='jaccard', leaf_size=len(project_names)/100)
        neighbors, distances = tree.query_radius(project_vectors_bin, 0.7, return_distance=True)
        print 'Retrieved neighbors'
        for i, project1 in enumerate(project_names):
            for ji, j in enumerate(neighbors[i]):
                project2 = project_names[j]
                if project1[:5]!=project2[:5]: # ignore if projects are from the same user
                    G.add_edge(project1, project2, weight=1-distances[i][ji])

    elif ann=='annoy':
        from annoy import AnnoyIndex
        tree = AnnoyIndex(project_vectors.shape[1], metric='angular')
        for i in range(project_vectors.shape[0]):
            tree.add_item(i, project_vectors[i])
        tree.build(1000)

        for i, project1 in enumerate(project_names):
            neighbors, distances = tree.get_nns_by_item(i, 100, include_distances=True)
            for ji, j in enumerate(neighbors):
                project2 = project_names[j]
                if project1[:5]!=project2[:5] and distances[ji]<0.5: # ignore if projects are from the same user
                    G.add_edge(project1, project2, weight=1-distances[ji])
            if (i+1)%5==0:
                print i+1,

    print 'Computed similarities'
    return G

def write_neighbors(G, outfile):
    neighbors = {}
    for project in G.nodes():
        if G.degree(project)>=5:
            neighbors[project] = G[project]
    with open(outfile, 'w') as o:
        ujson.dump(neighbors, o)

def main(ann):
    # loads pre-computed counts of each active block type per project for every user
    blockcounts = ujson.load(open('user_project_allblockcounts.json'))
    print_datastats(blockcounts)
    # load non-tutorials
    nontutorials = ujson.load(open('user_nontutorial_projects.json'))
    # filter non-tutorials
    blockcounts = user_project_filter(blockcounts, nontutorials)
    print_datastats(blockcounts)
    # vectorize
    project_vectors, vocab, project_names = vectorize(blockcounts)
    # compute similarities
    G = pairwise(project_vectors.todense(), project_names, ann)
    write_neighbors(G, 'all.neighbors')

if __name__=='__main__':
    main(sys.argv[1])
