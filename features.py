#features.py
import datetime
import numpy

##TIME FEATURES
def timediff(t1, t2):
    """difference between times (millisec precision) as days"""
    return (t1-t2)/(86400.*1000)

def getProjectIntervals(projects):
    """List of intervals between consecutive projects"""
    intervals = []
    prev = projects[0]["**created"]
    for project in projects[1:]:
        curr = project['**created']
        intervals.append(timediff(curr, prev))
        prev = curr
    return numpy.array(intervals)

def getProjectLengths(projects):
    """Lengths (according to last modified date) of projects"""
    return numpy.array([timediff(project["**modified"], project["**created"]) for project in projects])

def numProjects(projects):
	return len(projects)

def numOnDay(projects):
    """number of projects per day of the week"""
    num_projs = len(projects)
    weekday_projs = 0
    dow = []
    for i in range(7):
        dow.append(0)
    for project in projects:
        date = datetime.datetime.fromtimestamp(project['**created'] / 1e3).weekday()
        dow[date] += 1.0
    return numpy.array(dow)

def percentOnWeekday(projectsdow):
    """percentage of projects on a weekday, given number of projects for each day"""
    return sum(projectsdow[:5]) / sum(projectsdow) * 100

def projectsPerUserPeriod(projects, bins=10):
    '''histogram of number of projects across user's lifespan'''
    first= projects[0]['**created']
    daysElapsed = [timediff(project['**created'], first) for project in projects]
    hist, _ = numpy.histogram(daysElapsed, bins=bins)
    return hist

##CODE FEATURES
def getScreenNames(projects): 
    screenNames = []
    for project in projects: 
        projectScreens = [key for key in project.keys() if '*' not in key]
        screenNames.append(projectScreens)
    return screenNames

def getNumScreens(projects):
    numScreens = []
    for project in projects:
         numScreens.append(project['*Number of Screens'])
    return numpy.array(numScreens)

def getAllVariables(projects):
    '''returns a list with 0th element being the average number of local variables, the 1st element
    being the average number of global variables, and the 2nd element being the average number
    of variables in a project'''
    numScreens = getScreenNames(projects)

    gv_count = 0
    lv_count = 0
    i = 0
    variables = []
    while i < len(projects):
        for screenNum in numScreens[i]:
#             print screenNum
            if screenNum in projects[i].keys():
                if  not isinstance(projects[i][screenNum]['Blocks'], unicode):
                    if projects[i][screenNum]['Blocks']['Active Blocks'] != 'NO ACTIVE BLOCKS':
                        lv_count += len(projects[i][screenNum]['Blocks']['Active Blocks']['Local Variable Names'].keys())
                        gv_count += len(projects[i][screenNum]['Blocks']['Active Blocks']['Global Variable Names'].keys())
        i+=1
    variables.append(lv_count)
    variables.append(gv_count)
    variables.append(lv_count + gv_count)
    return [v/float(len(projects)) for v in variables]


def averageNumBlocks(projects):
    numScreens = getScreenNames(projects)
    totalBlocks = 0
    i = 0
    while i < len(projects):
        for screenNum in numScreens[i]:
            if screenNum in projects[i].keys():
                if  not isinstance(projects[i][screenNum]['Blocks'], unicode):
                    if  not isinstance(projects[i][screenNum]['Blocks']['Active Blocks'],unicode):
                        totalBlocks += projects[i][screenNum]['Blocks']['Active Blocks']['*Number of Blocks']
        i+=1
    return totalBlocks / float(len(projects))

def getAverageTypeTLBlocks(projects):
    numScreens = getScreenNames(projects)
    tl_count = 0
    i = 0
    while i < len(projects):
        for screenNum in numScreens[i]:
            if screenNum in projects[i].keys():
                if  not isinstance(projects[i][screenNum]['Blocks'], unicode):
                    tl_count += len(projects[i][screenNum]['Blocks']['*Top Level Blocks'].keys())
        i+=1
    return tl_count / float(len(projects))

def getAverageOrphanBlocks(projects):
    numScreens = getScreenNames(projects)
    tl_count = 0
    i = 0
    while i < len(projects):
        for screenNum in numScreens[i]:
            if screenNum in projects[i].keys():
                if  not isinstance(projects[i][screenNum]['Blocks'], unicode):
                    if projects[i][screenNum]['Blocks']['Orphan Blocks'] != "NO ORPHAN BLOCKS":
                        tl_count += projects[i][screenNum]['Blocks']['Orphan Blocks']['*Number of Blocks']
        i+=1
    return tl_count / float(len(projects))



def getAverageNumTLBlocks(projects):
    numScreens = getScreenNames(projects)
    count = 0
    i = 0
    while i < len(projects):
        for screenNum in numScreens[i]:
            if screenNum in projects[i].keys():
                if  not isinstance(projects[i][screenNum]['Blocks'], unicode):
                    types = projects[i][screenNum]['Blocks']['*Top Level Blocks'].keys()
                    for block in types:
                        count += projects[i][screenNum]['Blocks']['*Top Level Blocks'][block]
        i+=1
    return count / float(len(projects))

def averageNumComponents(projects):
    numScreens = getScreenNames(projects)
    numC = 0
    i = 0
    while i < len(projects):
        for screenNum in numScreens[i]:
            if screenNum in projects[i].keys():
                if  not isinstance(projects[i][screenNum]['Components'], unicode):
#                    if 'Number of Components' in projects[i][screenNum]['Components'].keys():
                    if not isinstance(projects[i][screenNum]['Components']['Number of Components'],unicode):
                        numC += projects[i][screenNum]['Components']['Number of Components']
        i+=1
    return numC / float(len(projects))

def aveNumMediaAssets(projects):
    count = 0
    for project in projects:
        count += len(project['*Media Assets'])
    return count / float(len(projects))

def averageNumStrings(projects): #counts unique strings
    numScreens = getScreenNames(projects)
    s = 0
    i = 0
    while i < len(projects):
        for screenNum in numScreens[i]:
            if screenNum in projects[i].keys():
                if  not isinstance(projects[i][screenNum]['Components'], unicode):
                     if not isinstance(projects[i][screenNum]['Components']['Strings'],unicode):
                        s += len(projects[i][screenNum]['Components']['Strings'])
        i+=1
    return s / float(len(projects))

def averageNumTypeComponents(projects): #ignores duplicate components, tests variety 
    numScreens = getScreenNames(projects)
    numC = 0
    i = 0
    while i < len(projects):
        for screenNum in numScreens[i]:
            if screenNum in projects[i].keys():
                if  not isinstance(projects[i][screenNum]['Components'], unicode):
#                    if 'Number of Components' in projects[i][screenNum]['Components'].keys():
                    if not isinstance(projects[i][screenNum]['Components']['Type and Frequency'],unicode):
                       numC += len(projects[i][screenNum]['Components']['Type and Frequency'])
        i+=1
    return numC / float(len(projects))

def averageNumProcedures(projects): 
    numScreens = getScreenNames(projects)
    numProc = 0
    i = 0
    while i < len(projects):
        for screenNum in numScreens[i]:
            if screenNum in projects[i].keys():
                if  not isinstance(projects[i][screenNum]['Blocks'], unicode):
                    if  not isinstance(projects[i][screenNum]['Blocks']['Active Blocks'],unicode):
                        numProc += len(projects[i][screenNum]['Blocks']['Active Blocks']['Procedure Names'])
        i+=1
    return numProc / float(len(projects))


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


def normalizeDict(d, projects): 
    '''normalizes dictionary by # of projects'''
    np = numProjects(projects)
    if float(np) == 0: np == 1
    for entry in d: 
        try: 
            d[entry] = d[entry] / float(np)
        except ZeroDivisionError: 
            print entry, np
    return d

def getControlsBlocks(projects):
    '''returns the number of ifs, forEach loops, while loops, choose / num projects'''
    controls_dict = {'controls_if': 0, 'controls_forEach': 0 , 'controls_while': 0, 'controls_choose': 0}
    numScreens = getScreenNames(projects)
    i= 0
    while i < len(projects):
        for screenName in numScreens[i]:
            if screenName in projects[i] and 'Active Blocks' in projects[i][screenName]['Blocks'] and 'Types' in projects[i][screenName]['Blocks']['Active Blocks']:
                allBlocks = projects[i][screenName]['Blocks']['Active Blocks']['Types']
                
                if 'controls_if' in allBlocks: 
                    controls_dict['controls_if'] += projects[i][screenName]['Blocks']['Active Blocks']['Types']['controls_if']
                if 'controls_forEach' in allBlocks: 
                    controls_dict['controls_forEach'] += projects[i][screenName]['Blocks']['Active Blocks']['Types']['controls_forEach']
                if 'controls_while' in allBlocks: 
                    controls_dict['controls_while'] += projects[i][screenName]['Blocks']['Active Blocks']['Types']['controls_while']
                if 'controls_choose' in allBlocks: 
                    controls_dict['controls_choose'] += projects[i][screenName]['Blocks']['Active Blocks']['Types']['controls_choose']
               
        i+=1
    final_dict = normalizeDict(controls_dict, projects)
    return final_dict




def getClasses(projects):
    class_dict = {u'TableArrangement':0, u'DatePicker':0, u'Canvas':0,
                  u'CheckBox':0, u'Web':0, u'Clock':0, u'BluetoothServer':0, u'ActivityStarter':0,
                  u'Texting':0, u'Label':0, u'Spinner':0, u'Camera':0, u'BluetoothClient':0, 
                  u'PhoneCall':0, u'LocationSensor':0, u'VerticalArrangement':0,
                  u'HorizontalArrangement':0, u'Sharing':0, u'TextToSpeech':0,
                  u'GoogleMap' :0, u'Slider':0, u'OrientationSensor':0, u'ListView':0, 
                  u'PhoneNumberPicker':0, u'TinyDB':0, u'NxtDirectCommands':0, u'Sound':0,
                  u'ListPicker':0, u'SpeechRecognizer':0, u'Button':0, u'WebViewer':0, u'BarcodeScanner':0,
                  u'NxtDrive':0, u'Camcorder':0, u'Notifier':0, u'TextBox':0, u'AccelerometerSensor':0,
                  u'Image':0, u'VideoPlayer':0, u'TinyWebDB':0, u'Player':0, u'File':0, u'YandexTranslate':0}
    
    screenNames = getScreenNames(projects)
    i= 0
    while i < len(projects):
        for screenName in screenNames[i]:
            if screenName in projects[i] and 'Components' in projects[i][screenName] and 'Type and Frequency' in projects[i][screenName]['Components']:
                types = projects[i][screenName]['Components']['Type and Frequency']
                for entry in types: 
                    if entry in class_dict: 
                        class_dict[entry] += projects[i][screenName]['Components']['Type and Frequency'][entry]
        i+=1
    final_dict = normalizeDict(class_dict, projects)

    return final_dict

def getMathBlocks(projects): 
    math_dict = {'math_divide':0, u'math_cos':0, u'math_format_as_decimal':0,
                    u'math_neg':0, u'math_trig':0, u'math_floor':0, u'math_random_float':0,
                    u'math_number':0, u'math_on_list':0, u'math_round':0, u'math_tan':0,
                    u'math_multiply':0, u'math_atan2':0, u'math_convert_angles':0, 
                    u'math_random_int':0, u'math_compare':0, u'math_random_set_seed':0,
                    u'math_ceiling':0, u'math_subtract':0, u'math_single':0, u'math_power':0,
                    u'math_abs':0, u'math_is_a_number':0, u'math_division':0, 
                    u'math_convert_number':0, u'math_add':0, 'logic_boolean':0,
                 'logic_compare':0,'logic_false':0,'logic_negate':0,'logic_operation':0,'logic_or':0}
    
    screenNames = getScreenNames(projects)
    i= 0
    while i < len(projects):
        for screenName in screenNames[i]:
                if screenName in projects[i] and 'Active Blocks' in projects[i][screenName]['Blocks'] and 'Types' in projects[i][screenName]['Blocks']['Active Blocks']:
                    blocks = projects[i][screenName]['Blocks']['Active Blocks']['Types']
                    for entry in blocks: 
                        if entry in math_dict: 
                            math_dict[entry] += projects[i][screenName]['Blocks']['Active Blocks']['Types'][entry]
        i+=1
    final_dict = normalizeDict(math_dict, projects)

    
    return final_dict

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

def getBlocks(projects, block_dict): 
    '''returns  a dictionary with the key as a block name ie math_add 
    and a value that is the # of occurances of that block / numProjects'''
    screenNames = getScreenNames(projects)
    i= 0
    while i < len(projects):
        for screenName in screenNames[i]:
                if screenName in projects[i] and 'Active Blocks' in projects[i][screenName]['Blocks'] and 'Types' in projects[i][screenName]['Blocks']['Active Blocks']:
                    blocks = projects[i][screenName]['Blocks']['Active Blocks']['Types']
                    for block in blocks: 
                         if block in block_dict: 
                            block_dict[block] += projects[i][screenName]['Blocks']['Active Blocks']['Types'][block]
        i+=1
    final_dict = normalizeDict(block_dict, projects)

    return final_dict

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
                    


