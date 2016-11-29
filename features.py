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
def getNumScreens(projects):
    numScreens = []
    for project in projects:
         numScreens.append(project['*Number of Screens'])
    return numpy.array(numScreens)

def getAllVariables(projects):
    '''returns a list with 0th element being the average number of local variables, the 1st element
    being the average number of global variables, and the 2nd element being the average number
    of variables in a project'''
    numScreens = getNumScreens(projects)
    gv_count = 0
    lv_count = 0
    i = 0
    variables = []
    while i < len(projects):
        for j in range(numScreens[i]):
            screenNum = "Screen"+ str(j + 1)
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
    numScreens = getNumScreens(projects)
    totalBlocks = 0
    i = 0
    while i < len(projects):
        for j in range(numScreens[i]):
            screenNum = "Screen"+ str(j + 1)
            if screenNum in projects[i].keys():
                if  not isinstance(projects[i][screenNum]['Blocks'], unicode):
                    if  not isinstance(projects[i][screenNum]['Blocks']['Active Blocks'],unicode):
                        totalBlocks += projects[i][screenNum]['Blocks']['Active Blocks']['*Number of Blocks']
        i+=1
    return totalBlocks / float(len(projects))

def getAverageTypeTLBlocks(projects):
    numScreens = getNumScreens(projects)
    tl_count = 0
    i = 0
    while i < len(projects):
        for j in range(numScreens[i]):
            screenNum = "Screen"+ str(j + 1)
            if screenNum in projects[i].keys():
                if  not isinstance(projects[i][screenNum]['Blocks'], unicode):
                    tl_count += len(projects[i][screenNum]['Blocks']['*Top Level Blocks'].keys())
        i+=1
    return tl_count / float(len(projects))

def getAverageOrphanBlocks(projects):
    numScreens = getNumScreens(projects)
    tl_count = 0
    i = 0
    while i < len(projects):
        for j in range(numScreens[i]):
            screenNum = "Screen"+ str(j + 1)
            if screenNum in projects[i].keys():
                if  not isinstance(projects[i][screenNum]['Blocks'], unicode):
                    if projects[i][screenNum]['Blocks']['Orphan Blocks'] != "NO ORPHAN BLOCKS":
                        tl_count += projects[i][screenNum]['Blocks']['Orphan Blocks']['*Number of Blocks']
        i+=1
    return tl_count / float(len(projects))

def decileNumScreens(projects):
    all_deciles = []
    for i in range(10):
        all_deciles.append([])

    first= int(projects[0]['**created'])
    last = int(projects[len(projects)-1]['**created'])
    decile_width = ((last - first) / (86400 * 1000.)) / 10

    for project in projects:
        numScreens = project['*Number of Screens']
        daysElapsed = (project['**created']-first)/(86400 * 1000.)
        #set index
        if daysElapsed == 0:
            index = 0
        else:
            index  = int(daysElapsed / decile_width)

        if index == 10:
            all_deciles[9].insert(0,numScreens)
        else:
            all_deciles[index].insert(0,numScreens)

    for i in range(10):
        if len(all_deciles[i]) == 0:
            all_deciles[i] = 0
        else:
            all_deciles[i] = sum(all_deciles[i])/ float(len(all_deciles[i]))
    return all_deciles

def decileTypesTopLevelBlocks(projects):
    '''measures how many types of TLblocks per project in each decile '''
    all_deciles = []
    for i in range(10):
        all_deciles.append([])

    first= int(projects[0]['**created'])
    last = int(projects[len(projects)-1]['**created'])
    decile_width = ((last - first) / (86400 * 1000.)) / 10


    for project in projects:
        numTL = 0
        numScreens = project['*Number of Screens']
        daysElapsed = (project['**created']-first)/(86400 * 1000.)

        for j in range(numScreens):
            screenNum = "Screen"+ str(j + 1)
            if screenNum in project.keys():
                if  not isinstance(project[screenNum]['Blocks'], unicode):
                    numTL = len(project[screenNum]['Blocks']['*Top Level Blocks'].keys())
    #set index
                if daysElapsed == 0:
                    index = 0
                else:
                    index  = int(daysElapsed / decile_width)

                if index == 10:
                    all_deciles[9].insert(0,numTL)
                else:
                    all_deciles[index].insert(0,numTL)
    for i in range(10):
        if len(all_deciles[i]) == 0:
            all_deciles[i] = 0
        else:
            all_deciles[i] = sum(all_deciles[i])/ float(len(all_deciles[i]))
    return all_deciles

def decileOrphanBlocks(projects):
    '''measures how many orphan blocks per project in each decile '''
    all_deciles = []
    for i in range(10):
        all_deciles.append([])
    first= int(projects[0]['**created'])
    last = int(projects[len(projects)-1]['**created'])
    decile_width = ((last - first) / (86400 * 1000.)) / 10

    for project in projects:
        numOrphan =0
        numScreens = project['*Number of Screens']
        daysElapsed = (project['**created']-first)/(86400 * 1000.)
        for j in range(numScreens):
            screenNum = "Screen"+ str(j + 1)
            if screenNum in project.keys():
                if  not isinstance(project[screenNum]['Blocks'], unicode):
                    if project[screenNum]['Blocks']['Orphan Blocks'] != "NO ORPHAN BLOCKS":
                        numOrphan += len(project[screenNum]['Blocks']['Orphan Blocks'].keys())

                    if daysElapsed == 0:
                        index = 0
                    else:
                        index  = int(daysElapsed / decile_width)

                    if index == 10:
                        all_deciles[9].insert(0,numOrphan)
                    else:
                        all_deciles[index].insert(0,numOrphan)

    for i in range(10):
        if len(all_deciles[i]) == 0:
            all_deciles[i] = 0
        else:
            all_deciles[i] = sum(all_deciles[i])/ float(len(all_deciles[i]))
    return all_deciles

def getAverageNumTLBlocks(projects):
    numScreens = getNumScreens(projects)
    count = 0
    i = 0
    while i < len(projects):
        for j in range(numScreens[i]):
            screenNum = "Screen"+ str(j + 1)
            if screenNum in projects[i].keys():
                if  not isinstance(projects[i][screenNum]['Blocks'], unicode):
                    types = projects[i][screenNum]['Blocks']['*Top Level Blocks'].keys()
                    for block in types:
                        count += projects[i][screenNum]['Blocks']['*Top Level Blocks'][block]
        i+=1
    return count / float(len(projects))

def averageNumComponents(projects):
    numScreens = getNumScreens(projects)
    numC = 0
    i = 0
    while i < len(projects):
        for j in range(numScreens[i]):
            screenNum = "Screen"+ str(j + 1)
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
    numScreens = getNumScreens(projects)
    s = 0
    i = 0
    while i < len(projects):
        for j in range(numScreens[i]):
            screenNum = "Screen"+ str(j + 1)
            if screenNum in projects[i].keys():
                if  not isinstance(projects[i][screenNum]['Components'], unicode):
                     if not isinstance(projects[i][screenNum]['Components']['Strings'],unicode):
                        s += len(projects[i][screenNum]['Components']['Strings'])
        i+=1
    return s / float(len(projects))

def averageNumTypeComponents(projects): #ignores duplicate components, tests variety 
    numScreens = getNumScreens(projects)
    numC = 0
    i = 0
    while i < len(projects):
        for j in range(numScreens[i]):
            screenNum = "Screen"+ str(j + 1)
            if screenNum in projects[i].keys():
                if  not isinstance(projects[i][screenNum]['Components'], unicode):
#                    if 'Number of Components' in projects[i][screenNum]['Components'].keys():
                    if not isinstance(projects[i][screenNum]['Components']['Type and Frequency'],unicode):
                       numC += len(projects[i][screenNum]['Components']['Type and Frequency'])
        i+=1
    return numC / float(len(projects))
    
def averageNumProcedures(projects): 
    numScreens = getNumScreens(projects)
    numProc = 0
    i = 0
    while i < len(projects):
        for j in range(numScreens[i]):
            screenNum = "Screen"+ str(j + 1)
            if screenNum in projects[i].keys():
                if  not isinstance(projects[i][screenNum]['Blocks'], unicode):
                    if  not isinstance(projects[i][screenNum]['Blocks']['Active Blocks'],unicode):
                        numProc += len(projects[i][screenNum]['Blocks']['Active Blocks']['Procedure Names'])
        i+=1
    return numProc / float(len(projects))
