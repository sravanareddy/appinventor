from __future__ import division
import ujson
from collections import defaultdict
import time
import networkx as nx
import numpy as np
import sys
from annoy import AnnoyIndex
from sklearn.datasets import load_svmlight_file
import argparse
import codecs

def get_slices(project_vectors, project_names, sliceprop, sliceindex):
    original_numprojects = project_vectors.shape[0]
    slicesize = int(original_numprojects/sliceprop)
    samples = range(sliceindex*slicesize, (sliceindex+1)*slicesize)
    project_vectors = project_vectors[samples]
    project_names = project_names[samples]
    print project_vectors.shape
    return project_vectors, project_names

def build_tree(project_vectors, project_names, numtrees, outfile):
    start = time.time()
    tree = AnnoyIndex(project_vectors.shape[1], metric='angular')
    for i in range(project_vectors.shape[0]):
        p = project_vectors[i, :].tolist()[0]
        tree.add_item(i, p)
    tree.build(numtrees)
    tree.save(outfile)
    print 'Finished in', time.time()-start, 'seconds'

def compute_neighbors(tree, ref_project_names, project_vectors, project_names, k):
    """Compute k nearest neighbors for each vector in project_vectors"""
    start = time.time()
    G = nx.Graph()
    for i, project1 in enumerate(project_names):
        p = project_vectors[i, :].tolist()[0]
        neighbors, distances = tree.get_nns_by_vector(p, k,
                                                      include_distances=True)
        for ji, j in enumerate(neighbors):
            project2 = ref_project_names[j]
            if project1[:5]!=project2[:5]: # ignore if projects are from the same user
                G.add_edge(project1, project2, weight=distances[ji])

    neighbors = {}
    for project1 in G.nodes():
        if G.degree(project1)>=5:
            neighbors[project1] = {}
            for project2 in G[project1]:
                neighbors[project1][project2] = G[project1][project2]['weight']
    # sort
    for project1 in neighbors:
        neighbors[project1] = sorted(neighbors[project1].items(), key=lambda x:x[1])

    print 'Finished in', time.time()-start, 'seconds'

    return neighbors

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('basefile', help='basename of files')
    parser.add_argument('--build', help='build tree', action="store_true")
    parser.add_argument('sliceprop', help='slice size as a proportion of the data', type=int)
    parser.add_argument('--numtrees', type=int)
    parser.add_argument('--k', help='number of nearest neighbors', type=int)
    parser.add_argument('--treefile', help='filename with stored tree')
    args = parser.parse_args()

    project_vectors, _ = load_svmlight_file(args.basefile+'_vectors.svml', dtype=np.int16)
    project_vectors = project_vectors.todense()
    project_names = np.array(codecs.open(args.basefile+'_names.txt', 'r', 'utf8').read().split())
    print 'Loaded data'

    if args.build:
        # build trees from slices
        for sliceindex in range(args.sliceprop):
            slice_project_vectors, slice_project_names = get_slices(project_vectors,
                                                    project_names,
                                                    args.sliceprop,
                                                    sliceindex)
            outfile = args.basefile+'-tree{0}-{1}-{2}.ann'.format(args.numtrees, args.sliceprop, sliceindex)
            build_tree(slice_project_vectors, slice_project_names, args.numtrees, outfile)
    else:
        tree = AnnoyIndex(project_vectors.shape[1])
        tree.load(args.treefile+'.ann')
        print 'Loaded tree'
        _, ref_project_names = get_slices(project_vectors,
                                          project_names,
                                          int(args.treefile.split('-')[1]),
                                          int(args.treefile.split('-')[2]))
        for sliceindex in range(25):
            test_project_vectors, test_project_names = get_slices(project_vectors,
                                                                  project_names,
                                                                  args.sliceprop,
                                                                  sliceindex)
            neighbors = compute_neighbors(tree,
                                          ref_project_names,
                                          test_project_vectors,
                                          test_project_names,
                                          args.k)
            outfile = 'unfiltered-neighbors-{0}-{1}-{2}.json'.format(args.treefile, args.sliceprop, sliceindex)
            with open(outfile, 'w') as o:
                ujson.dump(neighbors, o, indent=1)
            print sliceindex
