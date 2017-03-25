"""Use variable and function names as well as strings
to predict language of user."""

import langid
from collections import defaultdict, Counter
import ujson

def extract_namestrings(user_summary):
    """get list of variable names and strings from all projects
    in user summary"""
    tokens = []
    for projectid in user_summary:
        screens = [key for key in user_summary[projectid].keys() if '*' not in key]
        for screentitle in screens:
            # blocks
            if user_summary[projectid][screentitle]['Blocks']=='NO BLOCKS':
                continue
            blocks = user_summary[projectid][screentitle]['Blocks']
            if blocks == 'MALFORMED BKYFILE':
                continue
            if blocks['Active Blocks']=='NO ACTIVE BLOCKS':
                continue
            for namesp in ['Global Variable Names', 'Procedure Names', 'Procedure Parameter Names', 'Strings']:
                for vname in blocks['Active Blocks'][namesp]:
                    tokens.append(vname)
            # components
            if user_summary[projectid][screentitle]['Components']=='N':
                continue
            for sname in user_summary[projectid][screentitle]['Components']['Strings']:
                tokens.append(sname)
    return tokens

def get_user_langs(summaryfile):
    """extract strings and variables for each user;
    use language ID on these to infer the language label
    (distant supervision)
    """
    user_langs = {}  # map user to language

    ignored = set()  # set of users with too few tokens

    ctr = 0
    for line in open('user_project_summaries.json'):
        summaries = ujson.loads(line)
        print 'Loaded summaries',

        for userid in summaries:
            tokens = extract_namestrings(summaries[userid])
            if len(tokens)<50:
                ignored.add(userid)
                print '*',
            else:
                print '.',
                types = Counter(tokens)
                languages = defaultdict(int)  # total log prob on each token
                for string in types:
                    lang, logprob = langid.classify(string)
                    languages[lang] += logprob*types[string]

                if 'la' in languages:
                    languages.pop('la')  # get rid of Latin

                # get argmax
                user_langs[userid] = max(languages, key=lambda x:x[1])[0]

        print ctr
        ctr+=1


    print 'Ignored', len(ignored), 'users with too few tokens'
    return user_langs

if __name__=='__main__':
    user_langs = get_user_langs('user_project_summaries.json')
    with open('user_inferredlangs.json', 'w') as o:
        ujson.dump(user_langs, o)
