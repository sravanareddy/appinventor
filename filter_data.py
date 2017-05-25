import ujson
import numpy as np
from sklearn.feature_extraction import DictVectorizer
import codecs
from sklearn.datasets import dump_svmlight_file

def print_datastats(blockcounts):
    print len(blockcounts), 'users and', sum(map(len, blockcounts.values())), 'projects'

def user_project_filter(counts, user_project_set):
    """only keep projects in user_project_set in counts"""
    filtered_counts = {}
    for user in counts:
        orig = set(user_project_set[user]) if user in user_project_set else set()
        if len(orig)>0:   # keep users who are active after removing projects
            filtered_counts[user] = {project: counts[user][project] for project in counts[user] if project in orig}
    return filtered_counts

def vectorize(blockcounts, ):
    # pre-compute block-count array for each project
    all_projects = []
    project_names = []
    for user in blockcounts:
        for project in blockcounts[user]:
            all_projects.append(blockcounts[user][project])
            project_names.append(user+'-'+project)

    vectorizer = DictVectorizer()
    project_vectors = vectorizer.fit_transform(all_projects)
    print 'Vectorized', project_vectors.shape
    return project_vectors, project_names, vectorizer.vocabulary_,

def main():
    # loads pre-computed counts of each active block type per project for every user
    blockcounts = ujson.load(open('user_project_allblockcounts.json'))
    print_datastats(blockcounts)
    # load user languages
    user_inferredlangs = ujson.load(open('user_inferredlangs.json'))
    common_langs = set(['el', 'fr', 'en', 'zh', 'pt', 'ca', 'de', 'ko', 'it', 'th', 'es'])
    blockcounts = {user: blockcounts[user] for user in blockcounts if user in user_inferredlangs and user_inferredlangs[user] in common_langs}
    print_datastats(blockcounts)
    # load non-tutorials
    nontutorials = ujson.load(open('user_nontutorial_projects.json'))
    # filter non-tutorials
    blockcounts = user_project_filter(blockcounts, nontutorials)
    print_datastats(blockcounts)
    # vectorize
    project_vectors, project_names, vocab = vectorize(blockcounts)
    # store
    dump_svmlight_file(project_vectors,
                       np.zeros(project_vectors.shape[0]),
                       'filtered_project_vectors.svml')
    with codecs.open('filtered_project_names.txt', 'w', 'utf8') as o:
        o.write('\n'.join(project_names))
    with open('filtered_featuremap.json', 'w') as o:
        ujson.dump(vocab, o)

if __name__=='__main__':
    main()
