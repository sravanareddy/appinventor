from __future__ import division
import datetime
import numpy
from collections import Counter
import ujson

blocks_by_category = ujson.load(open('blocks_by_category.json'))
top_blocks = set(ujson.load(open('top_200_blocks.json')).keys())

summarystats = set(['local_vars', 'global_vars', 'procedures',
'procedure_params', 'orphan', 'toplevel', 'media_assets', 'numscreens', 'strings'])

components = set([u'component_SQLite', u'component_Sharing', u'component_FusiontablesControl', u'component_VideoPlayer', u'component_TextBox', u'component_GyroscopeSensor', u'component_TinyWebDB', u'component_CheckBox', u'component_Twitter', u'component_AccelerometerSensor', u'component_NxtLightSensor', u'component_BarcodeScanner', u'component_DigitalRead', u'component_AdMobInterstitial', u'component_UdooArduino',
u'component_mrSoundMeter', u'component_Button', u'component_MIOIOUltrasonidos', u'component_GameClient', u'component_NxtTouchSensor', u'component_UsbAccessory', u'component_Texting', u'component_Image', u'component_SpeechRecognizer', u'component_PasswordTextBox', u'component_Slider', u'component_TextToSpeech', u'component_Web', u'component_FirebaseDB', u'component_NxtColorSensor', u'component_ListView', u'component_AdMob',
u'component_DatePicker', u'component_TimePicker', u'component_Notifier', u'component_Label', u'component_ImagePicker', u'component_NxtUltrasonicSensor', u'component_TinyDB', u'component_BluetoothServer', u'component_OrientationSensor', u'component_ProximitySensor', u'component_EmailPicker', u'component_PhoneCall', u'component_NxtSoundSensor', u'component_Player', u'component_mrPlayer', u'component_Voting', u'component_LinkedDataListPicker',
u'component_ContactPicker', u'component_NearField', u'component_KitchenSink', u'component_NxtDirectCommands', u'component_WebViewer', u'component_GoogleCloudMessaging', u'component_BluetoothClient', u'component_mrSound', u'component_TableArrangement', u'component_SoundRecorder', u'component_Clock', u'component_Canvas', u'component_ListPicker', u'component_ActivityStarter', u'component_Camera', u'component_VerticalArrangement', u'component_LinkedData',
u'component_Spinner', u'component_Sound', u'component_HorizontalArrangement', u'component_BLE', u'component_File', u'component_Camcorder', u'component_Pedometer', u'component_PhoneNumberPicker', u'component_YandexTranslate', u'component_LocationSensor', u'component_NxtDrive'])

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
                relative_counts[key] += project_counts[project][key]
    return normalizeDict(relative_counts, len(project_counts))

# Blocks
def get_all_blocks(project_blockcounts):
    return get_average_counts(project_blockcounts)

def get_top_blocks(project_blockcounts):
    return get_average_counts(project_blockcounts, top_blocks)

def get_blocks_by_category(categories):
    bc = set()
    for category in categories:
        bc.update(blocks_by_category[category])
    def helper(project_blockcounts):
        return get_average_counts(project_blockcounts, bc)
    return helper

# OtherCounts
def get_all_othercounts(project_othercounts):
    return get_average_counts(project_othercounts)

def get_noncomponents(project_othercounts):
    return get_average_counts(project_othercounts, summarystats)

def get_components(project_othercounts):
    return get_average_counts(project_othercounts, components)

# Misc
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
