#features.py
import datetime 
import time 

def getAverageProjectLen(projects):
    num_projects = len(projects)
    total_project_length = 0 #the sum of all the lengths of the project (from date created to date modified)
    
    prev = projects[0]["**created"]
    for project in projects[1:]: 
        curr = project['**created']
        total_project_length += (curr - prev)/(86400.*1000)   #SR: added this to scale to days
        prev = curr 
    return int(total_project_length / float(num_projects))

def numProjects(projects):
	return len(projects)

def percentOnWeekday(projects):
    num_projs = numProjects(projects)
    weekday_projs = 0
    for project in projects: 
        if datetime.datetime.fromtimestamp(project['**created'] / 1e3).weekday() < 6: 
            weekday_projs += 1.0
    return weekday_projs / num_projs * 100

def percentOnDay(projects):
    num_projs = len(projects)
    weekday_projs = 0
    dow = [] 
    for i in range(7):
        dow.append(0)
    for project in projects: 
        date = datetime.datetime.fromtimestamp(project['**created'] / 1e3).weekday() 
        dow[date] += 1.0
    for i in range(7):
        dow[i] = dow[i] / num_projs * 100 
    return dow
    
def numProjectsInDecile(projects):
    ''' the first decile is the 0th decile (covering from 0-10% of the time), 
    the last decile is the 9th decile'''
    first= int(projects[0]['**created'])
    last = int(projects[len(projects)-1]['**created'])
    decile_width = ((last - first) / (86400 * 1000.)) / 10

    decileList = []   
    for i in range(10): 
        decileList.append(0)
        
    for project in projects: 
        daysElapsed = (project['**created']-first)/(86400 * 1000.)
        if daysElapsed == 0: 
            index = 0
        else: 
            index  = int(daysElapsed / decile_width)
        if index == 10: 
            decileList[9] = decileList[9] + 1
        else: 
            decileList[index] = decileList[index] + 1
    return decileList

##CODE FEATURES 
def getNumScreens(projects):
    numScreens = []
    for project in projects: 
         numScreens.append(project['*Number of Screens'])
    return numScreens

def averageNumScreens(projects):
    screenList = getNumScreens(projects)
    return sum(screenList)/ len(screenList)  

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
