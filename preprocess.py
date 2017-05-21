# pre-process summaries data
import ujson
from collections import Counter

def load_summaries(filename):
    summaries = {}
    ctr = 0
    for line in open(filename): # lazy iteration because the file is large
        ctr += 1
        summaries.update(ujson.loads(line))
        print ctr,
    return summaries

def write_users_projects_counts(summaries, countfunc, filename):
    """Apply countfunc function (which returns a dictionary of counts for each project for the summary)
    to every project"""
    user_project_counts = {}
    for user in summaries:
        user_project_counts[user] = {}
        for project in summaries[user]:
            user_project_counts[user][project] = countfunc(summaries[user][project])
    with open(filename, 'w') as o:
        ujson.dump(user_project_counts, o)

def get_block_counts(summary):
    '''computes a dictionary
    with the key as a block name ie math_add
    and a value that is the # of occurances of that block in the project.
    '''
    block_dict = Counter()
    for screenName in summary:
        if '*' not in screenName and 'Active Blocks' in summary[screenName]['Blocks'] and 'Types' in summary[screenName]['Blocks']['Active Blocks']:
            blocks = summary[screenName]['Blocks']['Active Blocks']['Types']
            for block in blocks:
                block_dict[block] += summary[screenName]['Blocks']['Active Blocks']['Types'][block]
    return block_dict

def get_other_counts(summary):
    '''computes a dictionary with counts of
    number of screens,
    orphan blocks, top-level blocks,
    the number of components of each type,
    global variables, local variables,
    media assets,
    strings,
    procedures, procedure params
    for a project
    '''
    counts = Counter()
    for screenName in summary:
        # number of screens
        counts['numscreens'] += 1
        if '*' not in screenName:
            # orphan and top level blocks
            if 'Blocks' in summary[screenName] and summary[screenName]['Blocks'] != 'NO BLOCKS' and summary[screenName]['Blocks'] != 'MALFORMED BKYFILE':
                if summary[screenName]['Blocks']['Orphan Blocks'] != "NO ORPHAN BLOCKS":
                    counts['orphan'] += len(summary[screenName]['Blocks']['Orphan Blocks'])
                try:
                    counts['toplevel'] += len(summary[screenName]['Blocks']['*Top Level Blocks'])
                except TypeError:
                    print summary[screenName]
                if summary[screenName]['Blocks']['Active Blocks'] != 'NO ACTIVE BLOCKS':
                    # local and global vars
                    counts['local_vars'] += len(summary[screenName]['Blocks']['Active Blocks']['Local Variable Names'])
                    counts['global_vars'] += len(summary[screenName]['Blocks']['Active Blocks']['Global Variable Names'])
                    # procedures and procedure parameters
                    counts['procedures'] += len(summary[screenName]['Blocks']['Active Blocks']['Procedure Names'])
                    counts['procedure_params'] += len(summary[screenName]['Blocks']['Active Blocks']['Procedure Parameter Names'])
                    # block strings
                    counts['strings'] += len(summary[screenName]['Blocks']['Active Blocks']['Strings'])
            # components of each type
            if 'Components' in summary[screenName] and 'Type and Frequency' in summary[screenName]['Components']:
                for comp_type in summary[screenName]['Components']['Type and Frequency']:
                    counts['component_'+comp_type] += 1
                # component strings
                counts['strings'] += len(summary[screenName]['Components']['Strings'])

        elif screenName=='*Media Assets':
            counts['media_assets'] += 1

        return counts

if __name__=='__main__':
    summaries = load_summaries('user_project_summaries.json')
    write_users_projects_counts(summaries, get_block_counts, 'user_project_allblockcounts.json')
