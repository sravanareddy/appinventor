#features.py
import datetime
import numpy
from collections import Counter

def normalizeDict(d, n):
    '''normalizes dictionary values by n'''
    if n == 0:
        n == 1.
    else:
        n = float(n)

    for entry in d:
        d[entry] = d[entry] / n

    return d

##CODE FEATURES
def get_average_counts(project_counts, filterSet=None):
    """for each project (dictionary of counts), normalize by the number of projects.
    If filterSet is not None, only keep those keys in the set.
    """
    relative_counts = Counter()
    for project in project_counts:
        for key in project_counts[project]:
            if not filterSet or key in filterSet:
                relative_counts += project_counts[project][key]
    return normalizeDict(relative_counts, len(project_counts))

def get_math_blocks(project_blockcounts):
    math_set = {'math_divide', 'math_cos', 'math_format_as_decimal',
               'math_neg', 'math_trig', 'math_floor', 'math_random_float',
                'math_number', 'math_on_list', 'math_round', 'math_tan',
                'math_multiply', 'math_atan2', 'math_convert_angles',
                'math_random_int', 'math_compare', 'math_random_set_seed',
                'math_ceiling', 'math_subtract', 'math_single', 'math_power',
                'math_abs', 'math_is_a_number', 'math_division',
                'math_convert_number', 'math_add',
                'logic_boolean', 'logic_compare', 'logic_false',
                'logic_negate', 'logic_operation','logic_or'}
    return get_average_counts(project_blockcounts, math_set)

def get_controls_blocks(project_blockcounts):
    return get_average_blockcounts(project_blockcounts, {'controls_if': 0, 'controls_forEach': 0 , 'controls_while': 0, 'controls_choose': 0})

def get_classes(project_othercounts):
    class_set = {'TableArrangement', 'DatePicker', 'Canvas',
                 'CheckBox', 'Web', 'Clock', 'BluetoothServer', 'ActivityStarter',
                 'Texting', 'Label', 'Spinner', 'Camera', 'BluetoothClient',
                 'PhoneCall', 'LocationSensor', 'VerticalArrangement',
                 'HorizontalArrangement', 'Sharing', 'TextToSpeech',
                 'GoogleMap', 'Slider', 'OrientationSensor', 'ListView',
                 'PhoneNumberPicker', 'TinyDB', 'NxtDirectCommands', 'Sound',
                 'ListPicker', 'SpeechRecognizer', 'Button', 'WebViewer', 'BarcodeScanner',
                 'NxtDrive', 'Camcorder', 'Notifier', 'TextBox', 'AccelerometerSensor',
                 'Image', 'VideoPlayer', 'TinyWebDB', 'Player', 'File', 'YandexTranslate'}
    return get_average_counts(project_othercounts, class_set)

def collapse_blocks(block_counts_dict):
    """Collapse fine-grained blocks"""
    newDict = Counter()
    for key in block_counts_dict:
        if '_' in key:
            newKey = key.split("_")[0]
        elif '.' in key:
            newKey = key.split(".")[0]
        else:
            newKey = key
        newDict[newKey] += block_counts_dict[key]
    return newDict

#TODO: re-implement Emma's featurizer functions in terms of the code above from the preprocessed data

# Decile stuff, ignore for now
def deltaDeciles(decileDict, name):
    values = sortDeciles(decileDict)
    deltas = {}
    for i in range(10):
        if i== 0: pass
        else: deltas[str(i) + " " + name] = values[i]-values[i-1]
    return deltas


def sortDeciles(decileDict):
    deciles_sorted = []
    keys = decileDict.keys()
    for key in keys:
        deciles_sorted.insert(int(key[-1]), decileDict[key])
    return deciles_sorted


def decileDict(projects):
    '''returns a dictionary with the key as the project name and the value as the decile'''
    deciles = {}
    decile_width = len(projects)/10
    if decile_width == 0: decile_width = 1
    for project in projects:
        index = projects.index(project) / decile_width
        if index > 9:
            index = 9

        deciles[project['**Project Name']] = index

    return deciles

def getAverageDecileValues(decile_list):
    '''returns the average of each decile'''
    return numpy.nan_to_num([numpy.average(sub_list) for sub_list in decile_list])

def decileOrphanBlocks(projects):
    '''measures how many orphan blocks per project in each decile '''
    decile_dict = decileDict(projects)

    all_deciles = []
    for i in range(10):
        all_deciles.append([])


    i = 0
    numScreens = getScreenNames(projects)

    for project in projects:
        numOrphan =0
        for screenName in numScreens[i]:
            if screenName in project:
                 if 'Blocks' in project[screenName] and project[screenName]['Blocks'] != 'NO BLOCKS' and project[screenName]['Blocks'] != 'MALFORMED BKYFILE':
                    if project[screenName]['Blocks']['Orphan Blocks'] != "NO ORPHAN BLOCKS":
                        numOrphan += len(project[screenName]['Blocks']['Orphan Blocks'])
                    index = decile_dict[project['**Project Name']]
                    all_deciles[index].append(numOrphan)

        i += 1
    return getAverageDecileValues(all_deciles)

def decileTypesTopLevelBlocks(projects):
    '''measures how many types of TLblocks per project in each decile '''
    numScreens = getScreenNames(projects)
    decile_dict = decileDict(projects)
    all_deciles = []

    for i in range(10):
        all_deciles.append([])
    i= 0
    for project in projects:
        numTL = 0

        for screenName in numScreens[i]:
            if screenName in project:
                if 'Blocks' in project[screenName] and project[screenName]['Blocks'] != 'NO BLOCKS' and project[screenName]['Blocks'] != 'MALFORMED BKYFILE':
                    try:
                        numTL = len(project[screenName]['Blocks']['*Top Level Blocks'])
                    except TypeError:
                        print project[screenName]
                    index = decile_dict[project['**Project Name']]
                    all_deciles[index].append(numTL)
        i+=1
    return getAverageDecileValues(all_deciles)




def decileNumScreens(projects):
    all_deciles = []
    decile_dict = decileDict(projects)

    for i in range(10):
        all_deciles.append([])

    for project in projects:
        numScreens = project['*Number of Screens']
        index = decile_dict[project['**Project Name']]
        all_deciles[index].append(numScreens)
    return getAverageDecileValues(all_deciles)
