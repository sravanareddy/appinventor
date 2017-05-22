from __future__ import division
import ujson
from scipy.spatial.distance import pdist
from sklearn.preprocessing import Binarizer
from sklearn.neighbors import BallTree
from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import PCA
from collections import defaultdict
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

def vectorize(blockcounts, user_inferredlangs):
    # pre-compute block-count array for each project
    all_projects = []
    project_names = []
    for user in user_inferredlangs:
        lang = user_inferredlangs[user]
        if user in blockcounts and lang in ['el', 'fr', 'en', 'zh', 'pt', 'ca', 'de', 'ko', 'it', 'th', 'es']:
            for project in blockcounts[user]:
                all_projects.append(blockcounts[user][project])
                project_names.append(user+'-'+project)

    vectorizer = DictVectorizer()
    project_vectors = vectorizer.fit_transform(all_projects)
    print 'Vectorized', project_vectors.shape

    return project_vectors, np.array(project_names), vectorizer.vocabulary_,

def pairwise(project_vectors, project_names, metric):
    distances = {}
    G = nx.Graph()

    original_numprojects = project_vectors.shape[0]
    samples = np.random.randint(0,
                                original_numprojects,
                                size=(int(original_numprojects/10),)) # take random sample of projects
    project_vectors = project_vectors[samples].todense()
    project_names = project_names[samples]

    if metric=='jaccard':
        #binarizer = Binarizer()
        #project_vectors = binarizer.fit_transform(project_vectors)
        #print 'Binarized'

        start = time.time()
        tree = BallTree(project_vectors,
                            metric='jaccard',
                            leaf_size=len(project_names)/100)
        print 'Built tree'
        neighbors, distances = tree.query_radius(project_vectors,
                                                     0.7,
                                                     return_distance=True)
        print 'Retrieved neighbors'
        for i, project1 in enumerate(project_names):
            for ji, j in enumerate(neighbors[i]):
                project2 = project_names[j]
                if project1[:5]!=project2[:5]: # ignore if projects are from the same user
                    G.add_edge(project1, project2, weight=1-distances[i][ji])
        print 'Added edges'
        print 'Finished in', time.time()-start, 'seconds'


    elif metric=='cosine':
        start = time.time()

        from annoy import AnnoyIndex
        tree = AnnoyIndex(project_vectors.shape[1], metric='angular')
        for i in range(project_vectors.shape[0]):
            p = project_vectors[i, :].tolist()[0]
            tree.add_item(i, p)
        tree.build(1000)

        for i, project1 in enumerate(project_names):
            neighbors, distances = tree.get_nns_by_item(i, 100, include_distances=True)
            for ji, j in enumerate(neighbors):
                project2 = project_names[j]
                if project1[:5]!=project2[:5] and distances[ji]<0.7: # ignore if projects are from the same user
                    G.add_edge(project1, project2, weight=1-distances[ji])

        print 'Finished in', time.time()-start, 'seconds'


    return G

def write_neighbors(G, outfile):
    neighbors = {}
    for project1 in G.nodes():
        if G.degree(project1)>=5:
            neighbors[project1] = {}
            for project2 in G[project1]:
                neighbors[project1][project2] = G[project1][project2]['weight']
    # sort
    for project1 in neighbors:
        neighbors[project1] = sorted(neighbors[project1].items(), key=lambda x:x[1], reverse=True)
    # write
    with open(outfile, 'w') as o:
        ujson.dump(neighbors, o, indent=4)

def main(metric):
    # loads pre-computed counts of each active block type per project for every user
    blockcounts = ujson.load(open('user_project_allblockcounts.json'))
    print_datastats(blockcounts)
    # load non-tutorials
    nontutorials = ujson.load(open('user_nontutorial_projects.json'))
    # filter non-tutorials
    blockcounts = user_project_filter(blockcounts, nontutorials)
    print_datastats(blockcounts)
    # load user languages
    user_inferredlangs = ujson.load(open('user_inferredlangs.json'))
    # vectorize
    project_vectors, project_names, vocab = vectorize(blockcounts, user_inferredlangs)
    # compute similarities between projects within the same language
    G = pairwise(project_vectors, project_names, metric)
    write_neighbors(G, 'all.neighbors')

if __name__=='__main__':
    main(sys.argv[1])
