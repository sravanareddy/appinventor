# Lyn Turbak, Benji Xie, Maja Svanberg
# AI2 summarizer
# Code adapted from jail.py

''' History (reverse chronological)

-------------------------------------------------------------------------------
2016/08/12-13 (Lyn):
====================

* Modified findProjectDirs so that:
  + it does not assume dirName argument is a list of user directories, 
    each of which contains a list of projects. It handles any directory structure
    whose leaves are .aia/.zip files or Benji-like project directories
  + It will ignore project directory XYZ if XYZ.zip already exisits; otherwise,
    it will create XYZ.zip.
  + It now displays relative file name with project number to give better sense of progress.

* Modified allProjectsToJSONFile so that:
  + It doesn't delete .zip files anymore. (if .zip files are created, as for Benji user data, 
    they're cached and the original project directories from which they're created are ignored 
    by findProjectDirs.)
  + It now displays relative file name with project number to give better sense of progress.

* Fixed bug in not correctly handling output directory structure for long-term dataset. 
  Before, put 00000, ..., 00999,... 01000, ..., 01999, ..., 02000 all in the same output directory.
  Now it puts them in 00/00000, ..., 00/00999, ..., 01/01000, ..., 01/01999, ... 02/02000, ...

* Fixed bug in findCreatedModifiedTimes for handling METADATA file in Benji-style projects 
  (didn't work before).

* Modified error/exception and warning messages to include details of project and file names.

* Replaced several instances of the pattern list += subList by list.extend(subList);
  the later is more efficient since it doesn't copy initial prefix of list. 

-------------------------------------------------------------------------------
2016/08/07 (Maja):
================

MAJOR CHANGES:
-------------
* Incorporated ai2topsummarizer.py
    + added global variable topSummary as a flag
    + Remade processRawBlockList (fka formatLists) with a check to be able to format the two kinds.
    + bkyToSummary does not add blocks to top if topSummary is true. Enabled 
    two different return statements. Appending lists of blocks instead of adding
    them, allowing us to find the top block of each group. 
    + Added check to projectToJSONProjectFileName to write different named summaries
        + XYZ_summary_top.json and XYZ_summary.json
    
MINOR CHANGES
-------------
* Changed names of functions for clarity
    + formatLists -> processRawBlockList
    + sortToDict -> sortListToDict
* An exception thrown used variable projectPath that no longer exists. 
    + Changed this to refer to relProjectPath
    
-------------------------------------------------------------------------------
2016/08/05 (Lyn):
================

MAJOR CHANGES
-------------
* Modified findProjectDirs to return a list of *relative* project paths, not *absolute* project paths.
  (This simplifies writing summary files to destination directory other than user directory.)
* Modified allProjectsToJSONFiles so that:
  + 2nd arg = numUsers has default value None, which returns projects of all users 
  + has new 3rd arg outputDir with default value None
    - A non-None value specifies (possibly new) target directory for summary .json files
    - A None value writes XYZ_summary.json file to same directory as .aia/.zip file
* Modified findProjectDirs so that numUsers has default value None, which returns projects of all users 
* Modified projectToJSONFile so that 1st arg is pathname relative to new 2nd arg and new 3rd argument 
  is outputDir with with default value None.
  + A non-None value specifies (possibly newly created) target directory for summary .json files
  + A None value writes XYZ_summary.json file to same directory as .aia/.zip file
* Modified scmToComponents to process components recursively, fixing bug in previous versions,
  which didn't correct process subcomponents of HorizontalArrangement, VerticalArrangement, and Canvas
* Defined isDeclarationType(generalType, specificType), which fixes several bugs in determining whether
  a block is a top-level declaration block. 
  + lexical_variable_get and lexical_variable_set used to be incorrectly treated as top-level declarations.
  + any "old-style" block, like 'DrawingCanvas_Clicked', 'DrawingCanvas_DrawCircle', or 'Button_SetText'
    was previously treated as a top-level declaration, but only the first is. Handling this correctly
    required introducing the dictionary AI1_v134a_component_specs from the AI1 to AI2 converter. 
* For old-style projects, replaced findComponentType/searchComponents by a mechanism that creates 
  (only once for each old-style screen) a dictionary mapping component names (like 'DrawingCanvas') 
  to component types (like 'Canvas').
* Modified blockType and upgradeFormat to handle generic methods and generic getters/setters.
  Name of generic blocks were not handled before, but now end in 'Generic'.
  E.g. Button.SetText is the non-generic setter, but Button.SetTextGeneric is the generic setter
* Modified scmToComponents to distinguish "Number of Component Types" from "Number of Components"
* Modified bkyToSummary to distinguish "*Number of Block Types" from "Number of Blocks"
* Fixed bug in findBlockInfo in categorizing global vs. local variable getters/setters

MINOR CHANGES
-------------
* Add new function projectToJSONProjectFileNamed that handles cases where projectPath contains dot
  in position other than extension
* Cleaned up use of global variables. It's generally considered bad style to pass parameters by global variable, 
  so passing information by explicit parameters is preferred. One exception is where a parameter would need
  to be passed down a long chain of calls to the point where it is used. 
  + Renamed global var projectPath to currentProjectPath, and declare it globally. 
    This is helpful for including projectPath in exception messages. 
  + Removed global var zippedFile. 
    Modified findName, findCreatedModifiedTimes, and friends to take explict zippedFile argument.
  + Removed global var screen and changed screenToJSON to take explicit screenName argument.
  + Removed global var scmFileName and changed scmToComponents to take explicit scmFileName argument.
  + Removed global name bkyFileName and changed bkyToSummary to take explicit arg
  + Added global currentScmJSONContents = to track contents of .scm file for currentScreen
* Modified findCreatedModifiedTimes to handle both META and METADATA files and projects without these
* Commented out dummyMeta, which is superseded by modified findCreatedModifiedTimes
* Simplified the collection of media in scmToComponents and findMedia. Made the findMedia function
  local to scmToComponents. 
* Added missing entries to blocklyTypeDict: 
  + 'text_split_at_spaces'
  + 'obfuscated_text', 
  + 'obsufcated_text' (early misspelling of 'obfuscated_text')

OTHER NOTES
-----------
* Use processTutorials() to create summaries for all tutorials.
  But you'll need to first set the global vars tutorialsInputDir and tutorialsOutputDir

-------------------------------------------------------------------------------
2015/08/03 (Maja)
================
* Fixed bug where no old-style format blocks were named "active blocks"
* Incorporated Eni's changes and instead of declaring an empty project to 
    have "NO BLOCKS", instead the empty dictionary structure is returned. 
    
-------------------------------------------------------------------------------
2015/08/02 (Maja)
================
* In an effort to speed up the code, passing down some parameters as global variables instead 
    of explicit. Later removed by Lyn.
    
-------------------------------------------------------------------------------
2015/07/22 (Lyn)
================
* Enabled summarizer to run on larger dataset, includes nextIndex functions
    to enable code to be run on separate occasions. 

-------------------------------------------------------------------------------
2015/07/15 (Maja)
================
* Fixed bug that caused old-style block not recognized by the upgrader to be handled
properly instead of returning "None.ACTION"
* Added commenting to parts of the code

-------------------------------------------------------------------------------
2015/07/12 (Maja)
================
* Fixed bug in old-style formatting upgrade, get_set is now handled properly. 

-------------------------------------------------------------------------------
2015/05 and 2015/06 (Maja)
================

Editing history forgone, all changes not recorded were made by Maja. 

-------------------------------------------------------------------------------
2015/04/23 (Benji)
================
* added error handling for missing SCM files, validation for screen 
    names startin with letter, timing execution
* added error handling for JSON loading
    
-------------------------------------------------------------------------------
2015/03/24 (Benji)
================
* handled issues relating to missing project.properties file and 
    improper case for scm and bky files
* added created and modified times to summary, handling cases for missing 
    META file, counting # of missing properties, META, case mismatches
    
-------------------------------------------------------------------------------
2015/01/19 (Maja)
================
* fixed bug of findComponentType requesting nonexisting keys
  
-------------------------------------------------------------------------------
2015/01/17 (Benji)
================
* fixed bug of trying to access zip file that did not exist in allProjectsToJSONFiles

-------------------------------------------------------------------------------
2015/01/15 (Maja)
================
* Cleaned up formatting of bkyToSummary(), following note Lyn made.

-------------------------------------------------------------------------------
2015/12/27 (Maja)
================
* Fixed bug in findMedia()

-------------------------------------------------------------------------------
2015/11/15 (Maja)
================
* Enabled upgrade of Old-Style blocks, added functions upgradeFormat() and findComponentType()

-------------------------------------------------------------------------------
2015/11/11 (Lyn):
================
* replace component_event, component_method, component_set_get by component-specific details. E.g.
  + not component_event, but Canvas.Draggged, ListPicker.AfterPicking, etc.  
  + not component_method, but Canvas.DrawLine
  + not component_set_get, but Label.GetText, Label.SetText

-------------------------------------------------------------------------------
2015/10 (Maja)
================
* Document created by Maja
     + Run by using allProjectsToJSONFiles()
     + Creates JSON sumaries of all .aia, .zip and directories representing 
     ai2 projects. 


'''



import os
import os.path
import json
import zipfile
import xml.etree.ElementTree as ET
import datetime
import sys # [2016/08/06, lyn] New, for sys.exc_info()

# for dummy project.properties and meta files 
DUMMY_PROJECT_NAME = '<<dummy_project_name>>'
DUMMY_USER_NAME = '<<dummy_user_name>>'
DUMMY_CREATED_TIME = -2
DUMMY_MODIFIED_TIME = -1
DUMMY_VERSION = -1
DUMMY_SCREEN_NAME = '<<dummy_screen_name>>'

num_missing_properties = 0
num_missing_meta = 0
num_missing_scm = 0
num_case_mismatches = 0

# *** Added by lyn 
print_every = 100

# *** Removed by lyn
'''
# meta_filename = 'METADATA' # 'METADATA' for old files, 'META' for new files
meta_filename = 'META' # 'METADATA' for old files, 'META' for new files
'''

# *** Added by lyn 
currentProjectPath = None # Global variable that tracks current project path being processed
currentScmJSONContents = None # Global variable that tracks contents of .scm file for currentScreen
currentComponentDictionary = {} # Global variable that contains dictionary mapping component names to component types for current screen

def allProjectsToJSONFiles(inputDir, numToKeep=None, outputDir=None):
    '''assumes cwd contains dir, that contains projects (in .aia, .zip, or as dir).
      + 2nd arg = numUsers has default value None, which returns projects of all users 
      + has new 3rd arg outputDir with default value None
        - A non-None value specifies (possibly new) target directory for summary .json files
        - A None value writes XYZ_summary.json file to same directory as .aia/.zip file.'''
    logwrite('allProjectsToJSONFiles({}, {}, {})'.format(inputDir, numToKeep, outputDir))
    logwrite('Finding projects (zipping as necessary) ...')
    listOfAllProjects = findProjectDirs(inputDir, numToKeep)
    logwrite("Done finding projects...")
    # *** Added by lyn 
    logwrite("Number of projects to process: " + str(len(listOfAllProjects)))
    # *** Added by lyn 
    num_projects_processed = 0
    for relProjectPath in listOfAllProjects:
        absProjectPath = os.path.join(inputDir, relProjectPath)
        if os.path.exists(absProjectPath):
            projectToJSONFile(relProjectPath, inputDir, outputDir)
            # [2016/08/12] Don't delete .zip file anymore! (Leave it in case we want to reprocess!)
            # if os.path.exists(absProjectPath.split('.')[0]) and absProjectPath.split('.')[1] == 'zip':
            #    # *** Note from Lyn: should only remove if it's not the main representation of the project!
            #    os.remove(absProjectPath)
        # *** Added by lyn 
        num_projects_processed += 1
        if num_projects_processed % print_every == 0: 
            logwrite(str(num_projects_processed) + ": " + relProjectPath)

# [2016/08/06, lyn] Modified this to return list of paths *relative* to dirName, rather than
#  *absolute* paths including dirName. This simplifies  This simplifies writing summary files 
# to a destination directory other than dirName.
def findProjectDirs(dirName, numToKeep=None):
    """
    given path to directory containing users (dirName) and number of users(numUsers),
    zip user directories and return list of PATHS RELATIVE TO DIRNAME to zipped project directories.
    If numUsers is None, return projects of all users; else return projects of
    first numUser users. 
    """
    relProjectPaths = []
    num_projects_processed = [0] # Listify to solve scoping issues
    def processFileOrDir(relPrefix, fileOrDir): # Recursively process directories until get to projects. 
        foundProject = False
        relPath = os.path.join(relPrefix, fileOrDir)
        absPath = os.path.join(dirName, relPath)
        if relPath.endswith('.aia') or relPath.endswith('.zip'):
            # Assume this is a project file
            relProjectPaths.append(relPath)
            foundProject = relPath
        elif os.path.isdir(absPath): 
            if isProjectDir(absPath):
                if not os.path.exists(absPath + '.zip'):
                    # Only zip project directory into .zip file if it hasn't been zipped already
                    zipdir(absPath, absPath + '.zip')
                    relZipFile = relPath + '.zip'
                    relProjectPaths.append(relZipFile)
                    foundProject = relZipFile
                # else do nothing!
            else: # Not a project directory; process contents recursively
                for fod in os.listdir(absPath):
                    processFileOrDir(relPath, fod)
        else: 
            # Ignore other files 
            pass
        if foundProject: 
            num_projects_processed[0] += 1
            if num_projects_processed[0] % print_every == 0: 
                logwrite(str(num_projects_processed[0]) + ": " + foundProject)

    # *** Added by lyn 
    filesOrDirs = os.listdir(dirName)
    if numToKeep != None:
        filesOrDirs = filesOrDirs[:numToKeep]
    for fileOrDir in filesOrDirs:
        processFileOrDir('', fileOrDir)
    return relProjectPaths

# [2016/08/12] Returns True iff absDirPath is an AI2 project directory like one
# in Benji's data. I.e., it contains only files and has at least a .scm or .bky file. 
def isProjectDir(absDirPath):
    filesOrDirs = os.listdir(absDirPath)
    for fileOrDir in filesOrDirs:
        if os.path.isdir(os.path.join(absDirPath, fileOrDir)):
            return False # Project file has no subdirs
        if fileOrDir.endswith('.scm') or fileOrDir.endswith('.bky'):
            return True
        # Otherwise try next fileOrDir
    return False # Return false if find no evidence it's project dir

def zipdir(path, ziph):
    """
    Given directory to path (path) and path to outputted zipped file (ziph),
    zip directory and return ziph
    """
    zf = zipfile.ZipFile(ziph, "w")
    for root, dirs, files in os.walk(path):
        for file in files:
            zf.write(os.path.join(root, file))
    zf.close()
    return ziph

# [2016/08/06, lyn] Modified this so that 1st arg is *relative* pathname to new 2nd arg, 
# and new 3rd arg (if non-None) specifies outputDir different from userDir. 
def projectToJSONFile(relProjectPath, userDir, outputDir=None):
    """
    Given path to zipped project (relProjectPath) relative to userDir, 
    create summary file and write to disk. 
    If outputDir is None, writes XYZ_summary.json file to same directory as .aia/.zip file
    If outputDir is non-None, writes XYZ_summary.json file (possibly newly created) outputDir.
    """
    if not relProjectPath.endswith('.zip') and not relProjectPath.endswith('.aia'):
        raise Exception("project " + relProjectPath +" is not .aia or  .zip") 
        #[2016-08-07 Maja] changed projectPath to relProjectPath

    global currentProjectPath
    currentProjectPath = os.path.join(userDir, relProjectPath) # Remember this absolute path as global for error handling
                                                               # Lyn sez: could avoid this by using try/except here instead
    try: 
        jsonProject = projectToJSON(currentProjectPath)
        if outputDir == None:
            # Write summary file to same directory as input file 
            jsonProjectFileName = projectToJSONProjectFileName(currentProjectPath)
        else:
            jsonProjectFileName = projectToJSONProjectFileName(os.path.join(outputDir, relProjectPath))
            (dirPath, basefile) = os.path.split(jsonProjectFileName) # Split jsonProjectFileName into directory path and base filename
            # Debugging:
            # print "***os.path.split***", (dirPath, basefile)
            # print "jsonProjectFileName", jsonProjectFileName
            if not os.path.exists(dirPath):
                os.makedirs(dirPath) # Make all intermediate directories that don't yet exist
                # Debugging:
                # print "dirPath", dirPath, os.path.exists(dirPath)
                # print "jsonProject", str(jsonProject)

            with open (jsonProjectFileName, 'w') as outFile:
                outFile.write(json.dumps(jsonProject,
                                         sort_keys=True,
                                         indent=2, separators=(',', ':')))
    except:
        packet = sys.exc_info()[:2]
        logwrite('***EXCEPTION' + " " + str(packet[0]) + " " + str(packet[1]))

# Introduced by Lyn. projectPath name might contain a dot, so 
# 
#   projectPath.split('.')[0] + '_summary.json'
# 
# won't always work.  Even though project name is guaranteed not to have dots, other components
# of projectPath might have dots.  E.g., suppose projectPath is 
# /Users/fturbak/ai2.users.long.term.randomized/03/03017/p001_002_AlexTalkToMe.aia
def projectToJSONProjectFileName(projectPath):
    parts = projectPath.split('.')
    allButExtension = '.'.join(parts[:-1])
    # [2016-08-07, Maja] adding check to enable different kinds of summaries
    if topSummary:
        return allButExtension + '_summary_top.json'
    return allButExtension + '_summary.json'

def projectToJSON(projectPath):
    """
    Given path to zipped project (projectPath), return JSON summary of project
    """
    summary = {}
    with zipfile.ZipFile(projectPath, 'r') as zippedFile:
        summary['**Project Name'] = findName(zippedFile)
        summary['**created'], summary['**modified'] = findCreatedModifiedTimes(zippedFile)
        listOfScreens = findScreenNames(zippedFile)
        summary['*Number of Screens'] = len(listOfScreens)
        media = []
        for screenName in listOfScreens:
            screenInfo = screenToJSON(zippedFile, screenName)
            summary[str(screenName)] = screenInfo[0]
            media.extend(screenInfo[1]) # [2016/08/13, lyn] More efficient to use .extend rather than += for lists
        summary['*Media Assets'] = list(set(media)) # list(set(...)) removes duplicates
    return summary


'''Given a Python zip file and a pathless filename (no slashes), extract the lines from filename,             
   regardless of path. E.g., Screen1.bky should work if archive name is Screen1.bky                                                                                  or src/appinventor/ai_fturbak/PROMOTO_IncreaseButton/Screen1.bky. 
   it also strips the file from '&'s and '>'  '''
def linesFromZippedFile(zippedFile, pathlessFilename):
    if "/" in pathlessFilename:
        raise RuntimeError("linesFromZippedFile -- filename should not contain slash: " + pathlessFilename 
                           + " in project " + currentProjectPath)
    names = zippedFile.namelist()
    if pathlessFilename in names:
        fullFilename = pathlessFilename
    else:
        matches = filter(lambda name: name.endswith("/" + pathlessFilename), names)
        if len(matches) == 1:
            fullFilename = matches[0]
        elif len(matches) == 0:
            if pathlessFilename == 'project.properties': # use dummy properties file if missing
                return dummyProperties()
            elif pathlessFilename == 'META': #use dummy META file if missing
                # return dummyMeta() 
                raise Exception("Should not look for META in zipped file {}; should be handled by findCreatedModifiedTimes".format(currentProjectPath)) # Lyn
            matches_alt = filter(lambda name: str.lower(name.split('/')[-1]) == str.lower(pathlessFilename), names) #considering case issues
            if len(matches_alt) == 1:
                global num_case_mismatches
                num_case_mismatches += 1
                fullFilename = matches_alt[0]
            else:
                suffix = pathlessFilename.split('.')[-1]
                if suffix == 'scm':
                    return dummyScm()
                elif suffix == 'bky':
                    if u'$Components' not in currentScmJSONContents[u'Properties']:
                        # .scm says empty .bky file is OK
                        logwrite("NOTE (*not* an error): Pretending there's an empty .bky file {} in project {} to match .scm file with no components".format(pathlessFilename, currentProjectPath))
                        return emptyBkyLines()
                    else:
                        raise RuntimeError("linesFromZippedFile -- no match for nonempty .bky file named: " + pathlessFilename
                                           + " in project " + currentProjectPath)
                else:
                    raise RuntimeError("linesFromZippedFile -- no match for file named: " + pathlessFilename
                                       + " in project " + currentProjectPath)
        else:
            raise RuntimeError("linesFromZippedFile -- multiple matches for file named: "
                         + pathlessFilename
                         + "[" + ",".join(matches) + "] -- in project" + currentProjectPath)
    return zippedFile.open(fullFilename).readlines()

def findName(zippedFile):
    """
    given zipfile of a project (zippedFile), return name of project 
    """
    pp = linesFromZippedFile(zippedFile, 'project.properties')
    if pp:
        return  pp[1][:-1].split('=')[1]
    return ""

'''2016/08/05: Modified by Lyn to handle both META and METADATA files and supersede dummyMeta()'''
def findCreatedModifiedTimes(zippedFile):
    """
    given a zipfile of a project (zippedFile), return tuple of created and modified times
    """
    names = zippedFile.namelist()
    if 'META' in names: 
        # Zipped file has metadata with one line that is JSON that looks like: 
        # {"name": "TALKTOME", "modified": 1438782081076, "created": 1438008239454}
        lines = linesFromZippedFile(zippedFile, 'META')
        if len(lines) != 1:
            raise Exception("project " + currentProjectPath + " has malformed META file with " + str(len(lines)) + " lines")
        else: 
            meta = json.loads(lines[0])
            return meta['created'], meta['modified']
    else: 
        # [2016/08/12, lyn] Fixed bug in handling of METADATA file 
        metadataFilenames = [name for name in names if name.endswith('METADATA')]
        if len(metadataFilenames) == 1:
            # Zipped file has metadata file with two lines that looks like: 
            # dateCreated = 1396713895474
            # dateModified = 1396714632270
            lines = linesFromZippedFile(zippedFile, 'METADATA')
            if len(lines) != 2:
                raise Exception("project " + currentProjectPath + " has malformed METADATA file with " + str(len(lines)) + " lines")
            else: 
                meta = map(lambda x: int(x.split(" = ")[1]), lines)
                return meta[0], meta[1]
        else: # supersede dummyMeta
            global num_missing_meta
            num_missing_meta += 1
            return str(DUMMY_CREATED_TIME), str(DUMMY_MODIFIED_TIME)

# [2016/08/05, lyn] modified to include names ending in either .bky or .scm'
def findScreenNames(zippedFile): 
    names = zippedFile.namelist()
    screens = []
    for file in names:
        name = str(file.split('/')[-1])
        extension = name[-4:]
        if (extension == '.scm' or extension == '.bky') and name[0].isalpha():
            # Lyn asks: what is name[0].isalpha() for? 
            screens.append(name[:-4])
    return list(set(screens)) # list(set(...)) removes duplicates 

def screenToJSON(zippedFile, screenName):
    scmFileName = screenName + '.scm'
    components = scmToComponents(zippedFile, scmFileName)
    bkyFileName = screenName + '.bky'
    bky = bkyToSummary(zippedFile, bkyFileName)
    return {'Components': components[0], 'Blocks': bky}, components[1] # components[1] is list of all media

# [2016/08/05, lyn] Introduced this helper function that returns JSON contents of .scm filex
def scmJSONContents(zippedFile, scmFileName):
    scmLines = linesFromZippedFile(zippedFile, scmFileName)
    if (len(scmLines) == 4
        and scmLines[0].strip() == '#|'
        and scmLines[1].strip() == '$JSON'
        and scmLines[3].strip() == '|#'):
        try:
            contents= json.loads(scmLines[2])
        except:
            e = sys.exc_info()[0]
            contents = {u'Properties':{}}
            logwrite("Malformed scm file {} in project {}. Error: {}".format(scmFileName, currentProjectPath, e)) # [2016/08/06, lyn] modified 
    else:
        try:
            contents = json.loads(scmLines)
        except:
            e = sys.exc_info()[0]
            contents = {u'Properties':{}}
            logwrite("Malformed scm file {} in project {}. Error: {}".format(scmFileName, currentProjectPath, e)) # [2016/08/06, lyn] modified 
    global currentScmJSONContents
    currentScmJSONContents = contents # Tracks contents of .scm file for currentScreen.
                                      # Used by upgradeFormat below to upgrade block types for old projects. 
    global currentComponentDictionary
    currentComponentDictionary = {} # Reset this to empty dict, and populate it only if we need to upgrade old-style components
    return contents

# [2016/08/06, lyn] Modified to distinguish number of components and number of different component types
def scmToComponents(zippedFile, scmFileName):
    numComponents = [0] # Listify to solve scope problem; does not count Screen itself
    components = {}
    strings = []
    media = []
    def recursivelyProcessComponents(componentDict):
       '''[2016/08/06, lyn] This function fixes bug in previous versions that processed only top-level components
          and did not descend into container components like HorizontalArrangement, VerticalArrangement, and Canvas.'''
       if u'$Components' in componentDict:
           # This is a container component -- i.e., Screen/Form, HorizontalArrangement, 
           # VerticalArrangement, or Canvas.
           for component in componentDict[u'$Components']:
               numComponents[0] += 1
               if component[u'$Type'] in components:
                   components[component['$Type']] += 1
               else: 
                   components[component['$Type']] = 1
               if u'Text' in component:
                   strings.append(component[u'Text'])
               findMedia(component)
               # Recursively process any subcomponents (of HorizontalArrangement, VerticalArrangement, or Canvas).
               recursivelyProcessComponents(component)
    # [2016/08/06] Lyn made this a local function to modify local media list directly
    def findMedia(component):
        # [2016/08/06] Lyn reorganized this: 
        for (key,value) in component.items():
            if (key == 'Picture' or \
                    key == 'Image' or \
                    key == 'Source' or \
                    key == 'BackgroundImage' or \
                    key == 'ResponseFileName'): # [2015/12/27, maja] these were the only keys I found in any of the tutorials that had files as values. 
                media.append(value) # Lyn sez: don't worry about dups here, nor whether value is string with dot. 
             # [2016/08/06] No need to specially process values that are lists (e.g., subcomponents)
             #   because that will be handled by recursive calls to recursivelyProcessComponents.
    contents = scmJSONContents(zippedFile, scmFileName)
    recursivelyProcessComponents(contents[u'Properties'])
    return ({'Number of Components': numComponents[0],        # [2016/08/06, lyn] Distinguish number of components
             'Number of Component Types': len(components), # and number of different component types!
             'Type and Frequency': components, 
             'Strings': strings
             }, list(set(media)) # Remove dups in media
            )

def elementTreeFromLines(lines):
    """ This function is designed to handle the following bad case: <xml xmlns="http://www.w3.org/1999/xhtml">
    for each file parse the xml to have a tree to run the stats collection on
    assumes if a namespace exists that it's only affecting the xml tag which is assumed to be the first tag"""
    # lines = open(filename, "r").readlines()                                     
    try:
        firstline = lines[0] #we are assuming that firstline looks like: <xml...>... we would like it to be: <xml>...                                                             
        if firstline[0:4] != "<xml":
            return ET.fromstringlist(['<xml></xml>'])
        else:
            closeindex = firstline.find(">")
            firstline = "<xml>" + firstline[closeindex + 1:]
            lines[0] = firstline
            #Invariant: lines[0] == "<xml>..." there should be no need to deal with namespace issues now
            return ET.fromstringlist(lines)
    except (IndexError, ET.ParseError):
        return ET.fromstringlist(['<MALFORMED></MALFORMED>'])

def bkyToSummary(zippedFile, bkyFileName):
  bkyLines = linesFromZippedFile(zippedFile, bkyFileName)
  rootElt = elementTreeFromLines(bkyLines)
  if rootElt.tag == 'MALFORMED':
      logwrite("***Project " + currentProjectPath + " has malformed .bky file " + bkyFileName)
      return 'MALFORMED BKYFILE'
  elif not rootElt.tag == 'xml':
      raise RuntimeError('bkyToSummary: Root of bky file is not xml but ' + rootElt.tag 
                         + " in project " + currentProjectPath)
  else:
      listOfBlocks = []
      listOfOrphans = []
      top  = []
      #if len(rootElt) < 1:
      #    return {'Active Blocks': {}, 'Orphan Blocks': {}}
      for child in rootElt:
          if child.tag == 'block':
              generalType = child.attrib['type']
              specificType = blockType(child) # [2015/11/11, lyn] Specially handle component_event, component_method, component_set_get
                                              # E.g., for generalType component_event, might have Button.Click;
                                              #       for generalType component_method, might have Canvas.DrawCircle
                                              #       for generalType component_set_get, might have Button.GetText or Button.SetText
                                              # Now also handles "old style" types. E.g. 'DrawingCanvas_Clicked' --> 'Canvas.Clicked'
              # [2016/08/07, Maja] add topSummary check if we need to append top or not
              # appending subblocks to list instead of adding them enables us recognize the first element as top block
              if not topSummary:
                  top.append(specificType) 
              if isDeclarationType(generalType, specificType): # declaration = top-level/root block 
                  listOfBlocks.append(findBlockInfo(child))
              else:
                  listOfOrphans.append(findBlockInfo(child))
      blocks = processRawBlockList(listOfBlocks)
      orphans = processRawBlockList(listOfOrphans)
    # [2016/08/07, Maja] Return formatting suitable for findClosest running on toplevelsummaries.
      if topSummary:
          return {'Active Blocks': blocks, 'Orphan Blocks': orphans}
      else:
          return {'*Top Level Blocks': sortListToDict(top), 'Active Blocks': blocks, 'Orphan Blocks': orphans}

declarationTypes = ['component_event', 'global_declaration', 'procedures_defnoreturn', 
                    'procedures_defreturn', 'procedures_callnoreturn', 'procedures_callreturn']

nonDeclarationTypes = ['component_method', 'component_set_get']

# [2016/08/06, lyn] This is new, and correctly handles several cases not handled correctly before:
# * lexical_variable_get and lexical_variable_set used to be incorrectly treated as top-level declarations.
# * any "old-style" block, like 'DrawingCanvas_Clicked', 'DrawingCanvas_DrawCircle', or 'StartButton_SetText'
#   was previously treated as a top-level declaration, but only the first is. 
def isDeclarationType(generalType, specificType):
    if generalType in declarationTypes: 
        return True
    elif generalType in nonDeclarationTypes:
        return False
    elif generalType in blockTypeDict: # e.g, math_add, lists_append_lists
        return False
    # If get here, generalType must be "old-style" type like 'DrawingCanvas_Clicked' 
    # and specificType must be upgraded type, like 'Canvas.Clicked'
    elif specificType in AI1_v134a_component_specs: # handles old-style component_event and component_method
        return AI1_v134a_component_specs[specificType]['type'] == 'component_event'
    else: 
        return False # Handles old-style component getters and setters. E.g. 'StartButton_GetText'
                     # as well as generic methods, E.g. Canvas.DrawCircleGeneric

#[2016-08-07] Added by Maja to append each block to its top level parent 
                # when "topSummary" is true
#[2016-08-07, Maja] rename for clarity
def processRawBlockList(inputList):
      blockDict = {}
      blockDict['Types'] = []
      blockDict['Procedure Names'] = []
      blockDict['Procedure Parameter Names'] = []
      blockDict['Global Variable Names'] = []
      blockDict['Local Variable Names'] = []
      blockDict['Strings'] = []
      blockDict['*Number of Blocks'] = 0 # [2016/08/07, Maja] number of blocks will not correspond to
                                        # length of input list since input list is nested
      #[2016-08-07] conditional added by Maja to append each block to its top level parent 
                # when "topSummary" is true, and do it the non-top level way if not
      for lyst in inputList:
        if topSummary:
            topBlockType = lyst[0]['Type']
            blockDict['Types'].append(topBlockType)
            blockDict['*Number of Blocks'] += 1
            for elt in lyst[1:]: # add all other blocks concatenated with topblock
                blockDict['Types'].append(topBlockType + '/' + elt['Type'])
                blockDict['*Number of Blocks'] += 1
            for dyct in lyst:
                for key in dyct:
                    if key != 'Type':
                        blockDict[key].extend(dyct[key]) # [2016/08/13, lyn] More efficient to use .extend rather than += for lists
        else:
            for dyct in lyst:
                blockDict['*Number of Blocks'] += 1
                for key in dyct:
                    if key == 'Type':
                        blockDict['Types'].append(dyct[key])
                    else:
                        blockDict[key].extend(dyct[key]) # [2016/08/13, lyn] More efficient to use .extend rather than += for lists
      for key in blockDict:
          if key != '*Number of Blocks':
              blockDict[key] = sortListToDict(blockDict[key])
      blockDict['*Number of Block Types'] = len(blockDict['Types']) # [2016/08/06, lyn] Add number of block types
      return blockDict

#[2016-08-07, Maja] rename for clarity
def sortListToDict(list):
    '''Give a list of strings, return a dictionary of histogram for strings'''
    output = {}
    for elt in list:
        if elt not in output: # Lyn sez: no need to use output.keys():
            output[elt] = 1
        else:
            output[elt] += 1
    return output

# [2016/08/06] Fixed bug in handling of categorizing var getters/setters as global or local
def findBlockInfo(xmlBlock):
    blockDict = {}
    tipe = blockType(xmlBlock) # [lyn, 2015/11/11] Specially handle component_event, component_method, component_set_get 
                               # [Maja, 2015/11/15] passing down zippedFile and bkyFileName to be able to handle old formatting
    blockDict['Type'] = tipe
    blockDict['Procedure Names'] = []
    blockDict['Procedure Parameter Names'] = []
    blockDict['Global Variable Names'] = []
    blockDict['Local Variable Names'] = []
    blockDict['Strings'] = []
    if tipe  == 'procedures_defnoreturn' or tipe == 'procedures_defreturn' or tipe == 'procedures_callnoreturn' or tipe == 'procedures_callreturn':
        for child in xmlBlock:
            if child.tag == 'title' or child.tag == 'field':
                blockDict['Procedure Names'] = [child.text]
            for param in child:
                if param.tag == 'arg':
                    blockDict['Procedure Parameter Names'].append(param.attrib['name'])
    if tipe  == 'global_declaration':
        for child in xmlBlock:
            if child.tag == 'field' or child.tag == 'title':
                blockDict['Global Variable Names'].append(child.text)
    if tipe == 'local_declaration_statement' or tipe == 'local_declaration_expression':
        for child in xmlBlock:
            if child.tag == 'title' or child.tag == 'field':
                blockDict['Local Variable Names'].append(child.text)
    # [2016/08/06] Fix bug in handling of categorizing var getters/setters as global or local
    if tipe == 'lexical_variable_get' or  tipe == 'lexical_variable_set':
        for child in xmlBlock:
            if child.tag == 'title' or child.tag == 'field':
                if child.text.startswith('global '):
                    blockDict['Global Variable Names'].append(child.text[len('global '):]) # Strip initial "global"
                elif child.text.startswith('input '): # Only in "old-style" projects
                    blockDict['Local Variable Names'].append(child.text[len('input '):]) # Strip initial "global"
                else: 
                    blockDict['Local Variable Names'].append(child.text)        
    if tipe == 'text':
        for child in xmlBlock:
            if child.tag == 'title' or child.tag == 'field':
                blockDict['Strings'].append(child.text)
    subBlocks = []
    for child in xmlBlock:
        for grandchild in child:
            if grandchild.tag == 'block':
                subBlocks.extend(findBlockInfo(grandchild)) # [2016/08/13, lyn] More efficient to use .extend rather than += for lists
    return [blockDict] + subBlocks

# [2016/08/06, lyn] Modified to handle generic methods and generic getters/setters
def blockType(xmlBlock):    
    ''' [2015/11/11, lyn] Specially handle component_event, component_method, component_set_get
         E.g., for generalType component_event, might have Button.Click;
               for generalType component_method, might have Canvas.DrawCircle
               for generalType component_set_get, might have Button.GetText or Button.SetText
         Now also handles "old style" types. E.g. 'DrawingCanvas_Clicked' --> 'Canvas.Clicked' 
         Now also handles generic methods and getters/setters: 
             e.g. Canvas.DrawCircleGeneric and Button.GetTextGeneric
    '''
    tipe = xmlBlock.attrib['type']    
    # Debugging:
    # print "***blockType", xmlBlock, tipe
    if tipe == 'component_event':
        for child in xmlBlock:
            if child.tag == 'mutation':
                return child.attrib['component_type'] + "." + child.attrib['event_name']
    elif tipe == 'component_method':
        for child in xmlBlock:
            if child.tag == 'mutation':
                methodName = child.attrib['component_type'] + "." + child.attrib['method_name']
                if child.attrib['is_generic'] == 'true':
                    methodName += 'Generic'
                return methodName
    elif tipe == 'component_set_get':
        for child in xmlBlock:
            if child.tag == 'mutation':
                getterSetterName = (child.attrib['component_type'] 
                                    + "." 
                                    + child.attrib['set_or_get'].capitalize() 
                                    + child.attrib['property_name'])
                if child.attrib['is_generic'] == 'true':
                    getterSetterName += 'Generic'
                return getterSetterName
    elif tipe not in blockTypeDict.keys():
        
        # handles component_set_get in the old format [Maja 2016-07-12]
        if tipe.endswith('etproperty'):
            
            #establish set or get [Maja 2016-07-12]
            if tipe.endswith('getproperty'):
                set_or_get = "Get"
            else:
                set_or_get = "Set"
                
            # find action taken [Maja 2016-07-12]
            for child in xmlBlock:
                if child.tag == 'title':
                    tipe = tipe.split("_")[0] + "_" + set_or_get + child.text
        # [Maja, 2015/11/15] handles the old style formatting 
        # e.g. 'DrawingCanvas_Clicked' --> 'Canvas.Clicked'
        return upgradeFormat(tipe)
    else:
        return tipe

# [Maja, 2015/11/15] Create
# [2016/08/06] Modified to handle generic types
def upgradeFormat(tipe):
    action = tipe.split('_')[-1]
    compName = '_'.join(tipe.split('_')[:-1]) # Fixed by lyn
    compType = findComponentType(compName)
    upgradedType = str(compType) + '.' + str(action)
    if compType == compName:
        upgradedType += 'Generic' # Handle generic types for old-style projects
    # Debugging:
    # print "***upgradeFormat***", tipe, upgradedType, currentProjectPath
    return upgradedType

def findComponentType(compName): 
    if currentComponentDictionary == {}: 
        populateCurrentComponentDictionary() # Populate dictionary if not already populated. 
    if compName in currentComponentDictionary:
        return currentComponentDictionary[compName] # Return answer from populated dictionary.
    elif compName in AI2_component_names:
        return compName
    else:
        raise Exception("Unable to find component name " + compName 
                        + " for old-style project " + currentProjectPath)

def populateCurrentComponentDictionary():
    '''Assume that currentComponentDictionary is currently {}. 
       Process the components in the currentScmJSONContents to populate currentComponentDictionary
       with mappings of component names (like 'DrawingCanvas') to component types (like 'Canvas').'''
    def recursivelyProcessComponents(componentDict):
        # Debugging: 
        # print componentDict[u'$Name'], "=>", componentDict[u'$Type']
        currentComponentDictionary[componentDict[u'$Name']] = componentDict[u'$Type']
        if u'$Components' in componentDict:
            for component in componentDict[u'$Components']:
                recursivelyProcessComponents(component)
    # Debugging: 
    # print("populating dictionary for " + currentProjectPath)
    recursivelyProcessComponents(currentScmJSONContents[u'Properties'])

# Lyn sez: the above code supersedes the following
"""
def findComponentType(compName): 
    ''' takes the component name, opens the .scm file, and finds the type of component '''
    scmLines = linesFromZippedFile(currentScmFileName)
    if (len(scmLines) == 4
        and scmLines[0].strip() == '#|'
        and scmLines[1].strip() == '$JSON'
        and scmLines[3].strip() == '|#'):
        data = json.loads(scmLines[2])
        
        # Makes sure all names are found and included [Maja 2016-07-12] 
    if u'$Components' in data[u'Properties'].keys():
        
        return searchComponents(compName[0], data[u'Properties'])

def searchComponents(name, components): #[Maja 2016-07-12]
    '''Takes a name and the value of a $Components (a dictionary) and
    returns the type of the component with the $Name name'''
    
    if '$Name' in components.keys() and components['$Name'].encode('utf-8') == name or \
    '$Type' in components.keys() and components['$Type'].encode('utf-8') == name:

        return components[u'$Type']

    elif "$Components" in components.keys():
        dlist = components["$Components"]
        
        for dyct in dlist:
            result = searchComponents(name, dyct)
        
            if result != None:
                return result
"""




def dummyProperties():
    """
    Return a list representing a dummy project properties file
    equivalent to output of linesFromZippedFile(myZip, 'project.properties')
    """
    global num_missing_properties
    num_missing_properties += 1   
    return ['main=appinventor.' + DUMMY_USER_NAME + '.' + DUMMY_PROJECT_NAME + '.Screen1\n',
     'name=' + DUMMY_PROJECT_NAME + '\n',
     'assets=../assets\n',
     'source=../src\n',
     'build=../build\n',
     'versioncode=1\n',
     'versionname=1.0\n',
     'useslocation=False\n',
     'aname=' + DUMMY_PROJECT_NAME + '\n']

# Removed by Lyn
'''
def dummyMeta():
    """
    Return dummy meta file for projects without META files
    """
    global num_missing_meta
    num_missing_meta += 1
    return ['{"name": "' + DUMMY_PROJECT_NAME + '", "modified": ' + str(DUMMY_MODIFIED_TIME) + ', "created": ' + str(DUMMY_CREATED_TIME) + '}']
'''

def dummyScm():
    """
    Return dummy SCM file for projects with missing SCM files
    """
    global num_missing_scm
    num_missing_scm += 1
    return '{"YaVersion":"' + str(DUMMY_VERSION) + '","Source":"Form","Properties":{"$Name":"' + str(DUMMY_SCREEN_NAME) + '","$Type":"Form","$Version":"' + str(DUMMY_VERSION) + '","AppName":"' + str(DUMMY_PROJECT_NAME) + '","Title":"' + str(DUMMY_SCREEN_NAME) + '","Uuid":"0"}}\n'

def emptyBkyLines():
    return ['<xml>', '</xml>']
    
"""
Given the path to a directory that contains users (dirName) and a file extension (fileType),
remove all files in the project directory that end with that file extension
"""
def cleanup(dirName, fileType):
    for user in os.listdir(dirName):
        user = os.path.join(dirName, user)
        if os.path.isdir(user):
          for project in os.listdir(user):
              projectPath = os.path.join(user, project)
              if projectPath.endswith(fileType):
                  os.remove(projectPath)

''' from jail.py '''
blockTypeDict = {

  # Component events                                                                                                    
  'component_event': {'kind': 'declaration'},

  # Component properties                                                                                                
  # These are handled specially in determineKind, which does not check these entries for kind                           
  'component_get': {'argNames': [], 'kind': 'expression'},
  'component_set': {'argNames': ['VALUE'], 'kind': 'statement'},

  # Component method calls                                                                                              
  # These are handled specially in determineKind, which does not check these entries for kind                           
  'component_method_call_expression': {'kind': 'expression'},
  'component_method_call_statement': {'kind': 'statement'},

  # Component value blocks (for generics)                                                                               
  'component_component_block': {'argNames': [], 'kind': 'expression'},

  # Variables                                                                                                          \
                                                                                                                        
  'global_declaration': {'argNames': ['VALUE'], 'kind': 'declaration'},
  'lexical_variable_get': {'argNames': [], 'kind': 'expression'},
  'lexical_variable_set': {'argNames': ['VALUE'], 'kind': 'statement'},
  'local_declaration_statement': {'kind': 'statement'},
  'local_declaration_expression': {'kind': 'expression'},
 # Procedure declarations and calls                                                                                   \
                                                                                                                        
  'procedures_defnoreturn': {'kind': 'declaration'},
  'procedures_defreturn': {'kind': 'declaration'},
  'procedures_callnoreturn': {'kind': 'statement'},
  'procedures_callreturn': {'kind': 'expression'},

  # Control blocks
                                                                                                                        
  'controls_choose': {'argNames': ['TEST', 'THENRETURN', 'ELSERETURN'], 'kind': 'expression'},
  'controls_if': {'kind': 'statement'}, # all sockets handled specially                                                 
  'controls_eval_but_ignore': {'argNames':['VALUE'], 'kind': 'statement'},
  'controls_forEach': {'argNames': ['LIST'], 'kind': 'statement'}, # body statement socket handled specially            
  'controls_forRange': {'argNames': ['START', 'END', 'STEP'], 'kind': 'statement'}, # body statement socket handled specially
  'controls_while': {'argNames': ['TEST'], 'kind': 'statement'}, # body statement socket handled specially              
  'controls_do_then_return': {'kind': 'expression'}, # all sockets handled specially                                    

  # Control ops on screen:                                                                                                             
  'controls_closeApplication': {'argNames':[], 'kind': 'statement'},
  'controls_closeScreen': {'argNames':[], 'kind': 'statement'},
  'controls_closeScreenWithPlainText': {'argNames':['TEXT'], 'kind': 'statement'},
  'controls_closeScreenWithValue': {'argNames':['SCREEN'], 'kind': 'statement'},
  'controls_getPlainStartText': {'argNames':[], 'kind': 'expression'},
  'controls_getStartValue': {'argNames':[], 'kind': 'expression'},
  'controls_openAnotherScreen': {'argNames':['SCREEN'], 'kind': 'statement'},
  'controls_openAnotherScreenWithStartValue': {'argNames':['SCREENNAME', 'STARTVALUE'], 'kind': 'statement'},

  # Colors

  'color_black': {'argNames': [], 'kind': 'expression'},
  'color_blue': {'argNames': [], 'kind': 'expression'},
  'color_cyan': {'argNames': [], 'kind': 'expression'},
  'color_dark_gray': {'argNames': [], 'kind': 'expression'},
  'color_light_gray': {'argNames': [], 'kind': 'expression'},
  'color_gray': {'argNames': [], 'kind': 'expression'},
  'color_green': {'argNames': [], 'kind': 'expression'},
  'color_magenta': {'argNames': [], 'kind': 'expression'},
  'color_orange': {'argNames': [], 'kind': 'expression'},
  'color_pink': {'argNames': [], 'kind': 'expression'},
  'color_red': {'argNames': [], 'kind': 'expression'},
  'color_white': {'argNames': [], 'kind': 'expression'},
  'color_yellow': {'argNames': [], 'kind': 'expression'},

  # Color ops:                                                                                                         \
                                                                                                                        
  'color_make_color': {'argNames':['COLORLIST'], 'kind': 'expression'},
  'color_split_color': {'argNames':['COLOR'], 'kind': 'expression'},

  # Logic                                                                                                               
  'logic_boolean': {'argNames': [], 'kind': 'expression'},
  'logic_false': {'argNames': [], 'kind': 'expression'}, # Together with logic boolean                                  
  'logic_compare': {'argNames': ['A', 'B'], 'kind': 'expression'},
  'logic_negate': {'argNames': ['BOOL'], 'kind': 'expression'},
  'logic_operation': {'argNames': ['A', 'B'], 'kind': 'expression'},
  'logic_or': {'argNames': ['A', 'B'], 'kind': 'expression'}, # Together with logic_operation                           

  # Lists                                                                                                               
  'lists_create_with': {'expandableArgName': 'ADD', 'kind': 'expression'},
  'lists_add_items': {'argNames': ['LIST'], 'expandableArgName':'ITEM', 'kind': 'statement'},
  'lists_append_list': {'argNames': ['LIST0', 'LIST1'], 'kind': 'statement'},
  'lists_copy': {'argNames': ['LIST'], 'kind': 'expression'},
  'lists_insert_item': {'argNames': ['LIST', 'INDEX', 'ITEM'], 'kind': 'statement'},
  'lists_is_list': {'argNames': ['ITEM'], 'kind': 'expression'},
  'lists_is_in': {'argNames':['ITEM', 'LIST'], 'kind': 'expression'},
  'lists_is_empty': {'argNames': ['LIST'], 'kind': 'expression'},
  'lists_length': {'argNames':['LIST'], 'kind': 'expression'},
  'lists_from_csv_row': {'argNames': ['TEXT'], 'kind': 'expression'},
  'lists_to_csv_row': {'argNames': ['LIST'], 'kind': 'expression'},
  'lists_from_csv_table': {'argNames': ['TEXT'], 'kind': 'expression'},
  'lists_to_csv_table': {'argNames': ['LIST'], 'kind': 'expression'},
  'lists_lookup_in_pairs': {'argNames': ['KEY', 'LIST', 'NOTFOUND'], 'kind': 'expression'},
  'lists_pick_random_item': {'argNames':['LIST'], 'kind': 'expression'},
  'lists_position_in': {'argNames':['ITEM', 'LIST'], 'kind': 'expression'},
  'lists_select_item': {'argNames': ['LIST', 'NUM'], 'kind': 'expression'},
  'lists_remove_item': {'argNames': ['LIST', 'INDEX'], 'kind': 'statement'},
  'lists_replace_item': {'argNames': ['LIST', 'NUM', 'ITEM'], 'kind': 'statement'},

  # Math

  'math_number': {'argNames': [], 'kind': 'expression'},
  'math_compare': {'argNames': ['A', 'B'], 'kind': 'expression'},
  'math_add': {'expandableArgName': 'NUM', 'kind': 'expression'},
  'math_multiply': {'expandableArgName': 'NUM', 'kind': 'expression'},
  'math_subtract': {'argNames':['A', 'B'], 'kind': 'expression'},
  'math_division': {'argNames':['A', 'B'], 'kind': 'expression'},
  'math_power': {'argNames':['A', 'B'], 'kind': 'expression'},
  'math_random_int': {'argNames':['FROM', 'TO'], 'kind': 'expression'},
  'math_random_float': {'argNames':[], 'kind': 'expression'},
  'math_random_set_seed': {'argNames':['NUM'], 'kind': 'statement'},
  'math_single': {'argNames':['NUM'], 'kind': 'expression'},
  'math_abs': {'argNames':['NUM'], 'kind': 'expression'}, # Together with math_single                                   
  'math_neg': {'argNames':['NUM'], 'kind': 'expression'}, # Together with math_single                                   
  'math_round': {'argNames':['NUM'], 'kind': 'expression'}, # Together with math_single                                 
  'math_ceiling': {'argNames':['NUM'], 'kind': 'expression'}, # Together with math_single                               
  'math_floor': {'argNames':['NUM'], 'kind': 'expression'}, # Together with math_single                                 
  'math_divide': {'argNames':['DIVIDEND', 'DIVISOR'], 'kind': 'expression'},
  'math_on_list': {'expandableArgName': 'NUM', 'kind': 'expression'},
  'math_trig': {'argNames':['NUM'], 'kind': 'expression'},
  'math_cos': {'argNames':['NUM'], 'kind': 'expression'}, # Together with math_trig                                     
  'math_tan': {'argNames':['NUM'], 'kind': 'expression'}, # Together with math_trig                                     
  'math_atan2': {'argNames':['Y', 'X'], 'kind': 'expression'},
  'math_convert_angles': {'argNames':['NUM'], 'kind': 'expression'},
  'math_format_as_decimal': {'argNames':['NUM', 'PLACES'], 'kind': 'expression'},
  'math_is_a_number': {'argNames':['NUM'], 'kind': 'expression'},
  'math_convert_number': {'argNames':['NUM'], 'kind': 'expression'},

  # Strings/text                                                                                                       
                                                                                                                        
  'text': {'argNames':[], 'kind': 'expression'},
  'text_join': {'expandableArgName': 'ADD', 'kind': 'expression'},
  'text_contains': {'argNames': ['TEXT', 'PIECE'], 'kind': 'expression'},
  'text_changeCase': {'argNames': ['TEXT'], 'kind': 'expression'},
  'text_isEmpty': {'argNames': ['VALUE'], 'kind': 'expression'},
  'text_compare': {'argNames': ['TEXT1', 'TEXT2'], 'kind': 'expression'},
  'text_length': {'argNames': ['VALUE'], 'kind': 'expression'},
  'text_replace_all': {'argNames': ['TEXT', 'SEGMENT', 'REPLACEMENT'], 'kind': 'expression'},
  'text_starts_at': {'argNames': ['TEXT', 'PIECE'], 'kind': 'expression'},
  'text_split': {'argNames': ['TEXT', 'AT'], 'kind': 'expression'},
  'text_split_at_spaces': {'argNames': ['TEXT'], 'kind': 'expression'}, # [2016/08/06, lyn] Added this missing entry
  'text_segment': {'argNames': ['TEXT', 'START', 'LENGTH'], 'kind': 'expression'},
  'text_trim': {'argNames': ['TEXT'], 'kind': 'expression'},
  'obfuscated_text': {'argNames': ['TEXT'], 'kind': 'expression'},  # [2016/08/06, lyn] Added this missing entry
  'obsufcated_text': {'argNames': ['TEXT'], 'kind': 'expression'},  # [2016/08/06, lyn] Added this missing entry (early misspelling of obfuscated_text)

}

# ----------------------------------------------------------------------
# Changes by lyn

''' Lyn snarfed the following JSON from his AI1 to AI2 converter.
    It describes component events and methods from v134a of AI1, which should be consistent
    with "old" projects that need to be upgraded. 
    Lyn manually edited it to change hyphens to dots in keys, e.g. "Button-Click" => "Button.Click"
'''
AI1_v134a_component_specs = {
    "AccelerometerSensor.AccelerationChanged": {"paramNames": ["xAccel", "yAccel", "zAccel"], "type": "component_event"},
    "AccelerometerSensor.Shaking": {"paramNames": [], "type": "component_event"},
    "ActivityStarter.ActivityError": {"paramNames": ["message"], "type": "component_event"},
    "ActivityStarter.AfterActivity": {"paramNames": ["result"], "type": "component_event"},
    "ActivityStarter.ResolveActivity": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "ActivityStarter.StartActivity": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Ball.Bounce": {"kind": "statement", "paramNames": ["edge"], "type": "component_method"},
    "Ball.CollidedWith": {"paramNames": ["other"], "type": "component_event"},
    "Ball.CollidingWith": {"kind": "expression", "paramNames": ["other", ""], "type": "component_method"},
    "Ball.Dragged": {"paramNames": ["startX", "startY", "prevX", "prevY", "currentX", "currentY"], "type": "component_event"},
    "Ball.EdgeReached": {"paramNames": ["edge"], "type": "component_event"},
    "Ball.Flung": {"paramNames": ["x", "y", "speed", "heading", "xvel", "yvel"], "type": "component_event"},
    "Ball.MoveIntoBounds": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Ball.MoveTo": {"kind": "statement", "paramNames": ["x", "y"], "type": "component_method"},
    "Ball.NoLongerCollidingWith": {"paramNames": ["other"], "type": "component_event"},
    "Ball.PointInDirection": {"kind": "statement", "paramNames": ["x", "y"], "type": "component_method"},
    "Ball.PointTowards": {"kind": "statement", "paramNames": ["target"], "type": "component_method"},
    "Ball.TouchDown": {"paramNames": ["x", "y"], "type": "component_event"},
    "Ball.TouchUp": {"paramNames": ["x", "y"], "type": "component_event"},
    "Ball.Touched": {"paramNames": ["x", "y"], "type": "component_event"},
    "BarcodeScanner.AfterScan": {"paramNames": ["result"], "type": "component_event"},
    "BarcodeScanner.DoScan": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "BluetoothClient.BluetoothError": {"paramNames": ["functionName", "message"], "type": "component_event"},
    "BluetoothClient.BytesAvailableToReceive": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "BluetoothClient.Connect": {"kind": "expression", "paramNames": ["address", ""], "type": "component_method"},
    "BluetoothClient.ConnectWithUUID": {"kind": "expression", "paramNames": ["address", "uuid", ""], "type": "component_method"},
    "BluetoothClient.Disconnect": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "BluetoothClient.IsDevicePaired": {"kind": "expression", "paramNames": ["address", ""], "type": "component_method"},
    "BluetoothClient.ReceiveSigned1ByteNumber": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "BluetoothClient.ReceiveSigned2ByteNumber": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "BluetoothClient.ReceiveSigned4ByteNumber": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "BluetoothClient.ReceiveSignedBytes": {"kind": "expression", "paramNames": ["numberOfBytes", ""], "type": "component_method"},
    "BluetoothClient.ReceiveText": {"kind": "expression", "paramNames": ["numberOfBytes", ""], "type": "component_method"},
    "BluetoothClient.ReceiveUnsigned1ByteNumber": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "BluetoothClient.ReceiveUnsigned2ByteNumber": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "BluetoothClient.ReceiveUnsigned4ByteNumber": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "BluetoothClient.ReceiveUnsignedBytes": {"kind": "expression", "paramNames": ["numberOfBytes", ""], "type": "component_method"},
    "BluetoothClient.Send1ByteNumber": {"kind": "statement", "paramNames": ["number"], "type": "component_method"},
    "BluetoothClient.Send2ByteNumber": {"kind": "statement", "paramNames": ["number"], "type": "component_method"},
    "BluetoothClient.Send4ByteNumber": {"kind": "statement", "paramNames": ["number"], "type": "component_method"},
    "BluetoothClient.SendBytes": {"kind": "statement", "paramNames": ["list"], "type": "component_method"},
    "BluetoothClient.SendText": {"kind": "statement", "paramNames": ["text"], "type": "component_method"},
    "BluetoothServer.AcceptConnection": {"kind": "statement", "paramNames": ["serviceName"], "type": "component_method"},
    "BluetoothServer.AcceptConnectionWithUUID": {"kind": "statement", "paramNames": ["serviceName", "uuid"], "type": "component_method"},
    "BluetoothServer.BluetoothError": {"paramNames": ["functionName", "message"], "type": "component_event"},
    "BluetoothServer.BytesAvailableToReceive": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "BluetoothServer.ConnectionAccepted": {"paramNames": [], "type": "component_event"},
    "BluetoothServer.Disconnect": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "BluetoothServer.ReceiveSigned1ByteNumber": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "BluetoothServer.ReceiveSigned2ByteNumber": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "BluetoothServer.ReceiveSigned4ByteNumber": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "BluetoothServer.ReceiveSignedBytes": {"kind": "expression", "paramNames": ["numberOfBytes", ""], "type": "component_method"},
    "BluetoothServer.ReceiveText": {"kind": "expression", "paramNames": ["numberOfBytes", ""], "type": "component_method"},
    "BluetoothServer.ReceiveUnsigned1ByteNumber": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "BluetoothServer.ReceiveUnsigned2ByteNumber": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "BluetoothServer.ReceiveUnsigned4ByteNumber": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "BluetoothServer.ReceiveUnsignedBytes": {"kind": "expression", "paramNames": ["numberOfBytes", ""], "type": "component_method"},
    "BluetoothServer.Send1ByteNumber": {"kind": "statement", "paramNames": ["number"], "type": "component_method"},
    "BluetoothServer.Send2ByteNumber": {"kind": "statement", "paramNames": ["number"], "type": "component_method"},
    "BluetoothServer.Send4ByteNumber": {"kind": "statement", "paramNames": ["number"], "type": "component_method"},
    "BluetoothServer.SendBytes": {"kind": "statement", "paramNames": ["list"], "type": "component_method"},
    "BluetoothServer.SendText": {"kind": "statement", "paramNames": ["text"], "type": "component_method"},
    "BluetoothServer.StopAccepting": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Button.Click": {"paramNames": [], "type": "component_event"},
    "Button.GotFocus": {"paramNames": [], "type": "component_event"},
    "Button.LongClick": {"paramNames": [], "type": "component_event"},
    "Button.LostFocus": {"paramNames": [], "type": "component_event"},
    "Camcorder.AfterRecording": {"paramNames": ["clip"], "type": "component_event"},
    "Camcorder.RecordVideo": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Camera.AfterPicture": {"paramNames": ["image"], "type": "component_event"},
    "Camera.TakePicture": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Canvas.Clear": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Canvas.Dragged": {"paramNames": ["startX", "startY", "prevX", "prevY", "currentX", "currentY", "draggedSprite"], "type": "component_event"},
    "Canvas.DrawCircle": {"kind": "statement", "paramNames": ["x", "y", "r"], "type": "component_method"},
    "Canvas.DrawLine": {"kind": "statement", "paramNames": ["x1", "y1", "x2", "y2"], "type": "component_method"},
    "Canvas.DrawPoint": {"kind": "statement", "paramNames": ["x", "y"], "type": "component_method"},
    "Canvas.DrawText": {"kind": "statement", "paramNames": ["text", "x", "y"], "type": "component_method"},
    "Canvas.DrawTextAtAngle": {"kind": "statement", "paramNames": ["text", "x", "y", "angle"], "type": "component_method"},
    "Canvas.Flung": {"paramNames": ["x", "y", "speed", "heading", "xvel", "yvel", "flungSprite"], "type": "component_event"},
    "Canvas.GetBackgroundPixelColor": {"kind": "expression", "paramNames": ["x", "y", ""], "type": "component_method"},
    "Canvas.GetPixelColor": {"kind": "expression", "paramNames": ["x", "y", ""], "type": "component_method"},
    "Canvas.Save": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "Canvas.SaveAs": {"kind": "expression", "paramNames": ["fileName", ""], "type": "component_method"},
    "Canvas.SetBackgroundPixelColor": {"kind": "statement", "paramNames": ["x", "y", "color"], "type": "component_method"},
    "Canvas.TouchDown": {"paramNames": ["x", "y"], "type": "component_event"},
    "Canvas.TouchUp": {"paramNames": ["x", "y"], "type": "component_event"},
    "Canvas.Touched": {"paramNames": ["x", "y", "touchedSprite"], "type": "component_event"},
    "CheckBox.Changed": {"paramNames": [], "type": "component_event"},
    "CheckBox.GotFocus": {"paramNames": [], "type": "component_event"},
    "CheckBox.LostFocus": {"paramNames": [], "type": "component_event"},
    "Clock.AddDays": {"kind": "expression", "paramNames": ["instant", "days", ""], "type": "component_method"},
    "Clock.AddHours": {"kind": "expression", "paramNames": ["instant", "hours", ""], "type": "component_method"},
    "Clock.AddMinutes": {"kind": "expression", "paramNames": ["instant", "minutes", ""], "type": "component_method"},
    "Clock.AddMonths": {"kind": "expression", "paramNames": ["instant", "months", ""], "type": "component_method"},
    "Clock.AddSeconds": {"kind": "expression", "paramNames": ["instant", "seconds", ""], "type": "component_method"},
    "Clock.AddWeeks": {"kind": "expression", "paramNames": ["instant", "weeks", ""], "type": "component_method"},
    "Clock.AddYears": {"kind": "expression", "paramNames": ["instant", "years", ""], "type": "component_method"},
    "Clock.DayOfMonth": {"kind": "expression", "paramNames": ["instant", ""], "type": "component_method"},
    "Clock.Duration": {"kind": "expression", "paramNames": ["start", "end", ""], "type": "component_method"},
    "Clock.FormatDate": {"kind": "expression", "paramNames": ["instant", ""], "type": "component_method"},
    "Clock.FormatDateTime": {"kind": "expression", "paramNames": ["instant", ""], "type": "component_method"},
    "Clock.FormatTime": {"kind": "expression", "paramNames": ["instant", ""], "type": "component_method"},
    "Clock.GetMillis": {"kind": "expression", "paramNames": ["instant", ""], "type": "component_method"},
    "Clock.Hour": {"kind": "expression", "paramNames": ["instant", ""], "type": "component_method"},
    "Clock.MakeInstant": {"kind": "expression", "paramNames": ["from", ""], "type": "component_method"},
    "Clock.MakeInstantFromMillis": {"kind": "expression", "paramNames": ["millis", ""], "type": "component_method"},
    "Clock.Minute": {"kind": "expression", "paramNames": ["instant", ""], "type": "component_method"},
    "Clock.Month": {"kind": "expression", "paramNames": ["instant", ""], "type": "component_method"},
    "Clock.MonthName": {"kind": "expression", "paramNames": ["instant", ""], "type": "component_method"},
    "Clock.Now": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "Clock.Second": {"kind": "expression", "paramNames": ["instant", ""], "type": "component_method"},
    "Clock.SystemTime": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "Clock.Timer": {"paramNames": [], "type": "component_event"},
    "Clock.Weekday": {"kind": "expression", "paramNames": ["instant", ""], "type": "component_method"},
    "Clock.WeekdayName": {"kind": "expression", "paramNames": ["instant", ""], "type": "component_method"},
    "Clock.Year": {"kind": "expression", "paramNames": ["instant", ""], "type": "component_method"},
    "ContactPicker.AfterPicking": {"paramNames": [], "type": "component_event"},
    "ContactPicker.BeforePicking": {"paramNames": [], "type": "component_event"},
    "ContactPicker.GotFocus": {"paramNames": [], "type": "component_event"},
    "ContactPicker.LostFocus": {"paramNames": [], "type": "component_event"},
    "ContactPicker.Open": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "EmailPicker.GotFocus": {"paramNames": [], "type": "component_event"},
    "EmailPicker.LostFocus": {"paramNames": [], "type": "component_event"},
    "FusiontablesControl.DoQuery": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "FusiontablesControl.ForgetLogin": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "FusiontablesControl.GotResult": {"paramNames": ["result"], "type": "component_event"},
    "FusiontablesControl.SendQuery": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "GameClient.FunctionCompleted": {"paramNames": ["functionName"], "type": "component_event"},
    "GameClient.GetInstanceLists": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "GameClient.GetMessages": {"kind": "statement", "paramNames": ["type", "count"], "type": "component_method"},
    "GameClient.GotMessage": {"paramNames": ["type", "sender", "contents"], "type": "component_event"},
    "GameClient.Info": {"paramNames": ["message"], "type": "component_event"},
    "GameClient.InstanceIdChanged": {"paramNames": ["instanceId"], "type": "component_event"},
    "GameClient.Invite": {"kind": "statement", "paramNames": ["playerEmail"], "type": "component_method"},
    "GameClient.Invited": {"paramNames": ["instanceId"], "type": "component_event"},
    "GameClient.LeaveInstance": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "GameClient.MakeNewInstance": {"kind": "statement", "paramNames": ["instanceId", "makePublic"], "type": "component_method"},
    "GameClient.NewInstanceMade": {"paramNames": ["instanceId"], "type": "component_event"},
    "GameClient.NewLeader": {"paramNames": ["playerId"], "type": "component_event"},
    "GameClient.PlayerJoined": {"paramNames": ["playerId"], "type": "component_event"},
    "GameClient.PlayerLeft": {"paramNames": ["playerId"], "type": "component_event"},
    "GameClient.SendMessage": {"kind": "statement", "paramNames": ["type", "recipients", "contents"], "type": "component_method"},
    "GameClient.ServerCommand": {"kind": "statement", "paramNames": ["command", "arguments"], "type": "component_method"},
    "GameClient.ServerCommandFailure": {"paramNames": ["command", "arguments"], "type": "component_event"},
    "GameClient.ServerCommandSuccess": {"paramNames": ["command", "response"], "type": "component_event"},
    "GameClient.SetInstance": {"kind": "statement", "paramNames": ["instanceId"], "type": "component_method"},
    "GameClient.SetLeader": {"kind": "statement", "paramNames": ["playerEmail"], "type": "component_method"},
    "GameClient.UserEmailAddressSet": {"paramNames": ["emailAddress"], "type": "component_event"},
    "GameClient.WebServiceError": {"paramNames": ["functionName", "message"], "type": "component_event"},
    "ImagePicker.AfterPicking": {"paramNames": [], "type": "component_event"},
    "ImagePicker.BeforePicking": {"paramNames": [], "type": "component_event"},
    "ImagePicker.GotFocus": {"paramNames": [], "type": "component_event"},
    "ImagePicker.LostFocus": {"paramNames": [], "type": "component_event"},
    "ImagePicker.Open": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "ImageSprite.Bounce": {"kind": "statement", "paramNames": ["edge"], "type": "component_method"},
    "ImageSprite.CollidedWith": {"paramNames": ["other"], "type": "component_event"},
    "ImageSprite.CollidingWith": {"kind": "expression", "paramNames": ["other", ""], "type": "component_method"},
    "ImageSprite.Dragged": {"paramNames": ["startX", "startY", "prevX", "prevY", "currentX", "currentY"], "type": "component_event"},
    "ImageSprite.EdgeReached": {"paramNames": ["edge"], "type": "component_event"},
    "ImageSprite.Flung": {"paramNames": ["x", "y", "speed", "heading", "xvel", "yvel"], "type": "component_event"},
    "ImageSprite.MoveIntoBounds": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "ImageSprite.MoveTo": {"kind": "statement", "paramNames": ["x", "y"], "type": "component_method"},
    "ImageSprite.NoLongerCollidingWith": {"paramNames": ["other"], "type": "component_event"},
    "ImageSprite.PointInDirection": {"kind": "statement", "paramNames": ["x", "y"], "type": "component_method"},
    "ImageSprite.PointTowards": {"kind": "statement", "paramNames": ["target"], "type": "component_method"},
    "ImageSprite.TouchDown": {"paramNames": ["x", "y"], "type": "component_event"},
    "ImageSprite.TouchUp": {"paramNames": ["x", "y"], "type": "component_event"},
    "ImageSprite.Touched": {"paramNames": ["x", "y"], "type": "component_event"},
    "ListPicker.AfterPicking": {"paramNames": [], "type": "component_event"},
    "ListPicker.BeforePicking": {"paramNames": [], "type": "component_event"},
    "ListPicker.GotFocus": {"paramNames": [], "type": "component_event"},
    "ListPicker.LostFocus": {"paramNames": [], "type": "component_event"},
    "ListPicker.Open": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "LocationSensor.LatitudeFromAddress": {"kind": "expression", "paramNames": ["locationName", ""], "type": "component_method"},
    "LocationSensor.LocationChanged": {"paramNames": ["latitude", "longitude", "altitude"], "type": "component_event"},
    "LocationSensor.LongitudeFromAddress": {"kind": "expression", "paramNames": ["locationName", ""], "type": "component_method"},
    "LocationSensor.StatusChanged": {"paramNames": ["provider", "status"], "type": "component_event"},
    "Notifier.AfterChoosing": {"paramNames": ["choice"], "type": "component_event"},
    "Notifier.AfterTextInput": {"paramNames": ["response"], "type": "component_event"},
    "Notifier.LogError": {"kind": "statement", "paramNames": ["message"], "type": "component_method"},
    "Notifier.LogInfo": {"kind": "statement", "paramNames": ["message"], "type": "component_method"},
    "Notifier.LogWarning": {"kind": "statement", "paramNames": ["message"], "type": "component_method"},
    "Notifier.ShowAlert": {"kind": "statement", "paramNames": ["notice"], "type": "component_method"},
    "Notifier.ShowChooseDialog": {"kind": "statement", "paramNames": ["message", "title", "button1Text", "button2Text", "cancelable"], "type": "component_method"},
    "Notifier.ShowMessageDialog": {"kind": "statement", "paramNames": ["message", "title", "buttonText"], "type": "component_method"},
    "Notifier.ShowTextDialog": {"kind": "statement", "paramNames": ["message", "title", "cancelable"], "type": "component_method"},
    "NxtColorSensor.AboveRange": {"paramNames": [], "type": "component_event"},
    "NxtColorSensor.BelowRange": {"paramNames": [], "type": "component_event"},
    "NxtColorSensor.ColorChanged": {"paramNames": ["color"], "type": "component_event"},
    "NxtColorSensor.GetColor": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "NxtColorSensor.GetLightLevel": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "NxtColorSensor.WithinRange": {"paramNames": [], "type": "component_event"},
    "NxtDirectCommands.DeleteFile": {"kind": "statement", "paramNames": ["fileName"], "type": "component_method"},
    "NxtDirectCommands.DownloadFile": {"kind": "statement", "paramNames": ["source", "destination"], "type": "component_method"},
    "NxtDirectCommands.GetBatteryLevel": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "NxtDirectCommands.GetBrickName": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "NxtDirectCommands.GetCurrentProgramName": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "NxtDirectCommands.GetFirmwareVersion": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "NxtDirectCommands.GetInputValues": {"kind": "expression", "paramNames": ["sensorPortLetter", ""], "type": "component_method"},
    "NxtDirectCommands.GetOutputState": {"kind": "expression", "paramNames": ["motorPortLetter", ""], "type": "component_method"},
    "NxtDirectCommands.KeepAlive": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "NxtDirectCommands.ListFiles": {"kind": "expression", "paramNames": ["wildcard", ""], "type": "component_method"},
    "NxtDirectCommands.LsGetStatus": {"kind": "expression", "paramNames": ["sensorPortLetter", ""], "type": "component_method"},
    "NxtDirectCommands.LsRead": {"kind": "expression", "paramNames": ["sensorPortLetter", ""], "type": "component_method"},
    "NxtDirectCommands.LsWrite": {"kind": "statement", "paramNames": ["sensorPortLetter", "list", "rxDataLength"], "type": "component_method"},
    "NxtDirectCommands.MessageRead": {"kind": "expression", "paramNames": ["mailbox", ""], "type": "component_method"},
    "NxtDirectCommands.MessageWrite": {"kind": "statement", "paramNames": ["mailbox", "message"], "type": "component_method"},
    "NxtDirectCommands.PlaySoundFile": {"kind": "statement", "paramNames": ["fileName"], "type": "component_method"},
    "NxtDirectCommands.PlayTone": {"kind": "statement", "paramNames": ["frequencyHz", "durationMs"], "type": "component_method"},
    "NxtDirectCommands.ResetInputScaledValue": {"kind": "statement", "paramNames": ["sensorPortLetter"], "type": "component_method"},
    "NxtDirectCommands.ResetMotorPosition": {"kind": "statement", "paramNames": ["motorPortLetter", "relative"], "type": "component_method"},
    "NxtDirectCommands.SetBrickName": {"kind": "statement", "paramNames": ["name"], "type": "component_method"},
    "NxtDirectCommands.SetInputMode": {"kind": "statement", "paramNames": ["sensorPortLetter", "sensorType", "sensorMode"], "type": "component_method"},
    "NxtDirectCommands.SetOutputState": {"kind": "statement", "paramNames": ["motorPortLetter", "power", "mode", "regulationMode", "turnRatio", "runState", "tachoLimit"], "type": "component_method"},
    "NxtDirectCommands.StartProgram": {"kind": "statement", "paramNames": ["programName"], "type": "component_method"},
    "NxtDirectCommands.StopProgram": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "NxtDirectCommands.StopSoundPlayback": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "NxtDrive.MoveBackward": {"kind": "statement", "paramNames": ["power", "distance"], "type": "component_method"},
    "NxtDrive.MoveBackwardIndefinitely": {"kind": "statement", "paramNames": ["power"], "type": "component_method"},
    "NxtDrive.MoveForward": {"kind": "statement", "paramNames": ["power", "distance"], "type": "component_method"},
    "NxtDrive.MoveForwardIndefinitely": {"kind": "statement", "paramNames": ["power"], "type": "component_method"},
    "NxtDrive.Stop": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "NxtDrive.TurnClockwiseIndefinitely": {"kind": "statement", "paramNames": ["power"], "type": "component_method"},
    "NxtDrive.TurnCounterClockwiseIndefinitely": {"kind": "statement", "paramNames": ["power"], "type": "component_method"},
    "NxtLightSensor.AboveRange": {"paramNames": [], "type": "component_event"},
    "NxtLightSensor.BelowRange": {"paramNames": [], "type": "component_event"},
    "NxtLightSensor.GetLightLevel": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "NxtLightSensor.WithinRange": {"paramNames": [], "type": "component_event"},
    "NxtSoundSensor.AboveRange": {"paramNames": [], "type": "component_event"},
    "NxtSoundSensor.BelowRange": {"paramNames": [], "type": "component_event"},
    "NxtSoundSensor.GetSoundLevel": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "NxtSoundSensor.WithinRange": {"paramNames": [], "type": "component_event"},
    "NxtTouchSensor.IsPressed": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "NxtTouchSensor.Pressed": {"paramNames": [], "type": "component_event"},
    "NxtTouchSensor.Released": {"paramNames": [], "type": "component_event"},
    "NxtUltrasonicSensor.AboveRange": {"paramNames": [], "type": "component_event"},
    "NxtUltrasonicSensor.BelowRange": {"paramNames": [], "type": "component_event"},
    "NxtUltrasonicSensor.GetDistance": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "NxtUltrasonicSensor.WithinRange": {"paramNames": [], "type": "component_event"},
    "OrientationSensor.OrientationChanged": {"paramNames": ["azimuth", "pitch", "roll"], "type": "component_event"},
    "PasswordTextBox.GotFocus": {"paramNames": [], "type": "component_event"},
    "PasswordTextBox.LostFocus": {"paramNames": [], "type": "component_event"},
    "Pedometer.CalibrationFailed": {"paramNames": [], "type": "component_event"},
    "Pedometer.GPSAvailable": {"paramNames": [], "type": "component_event"},
    "Pedometer.GPSLost": {"paramNames": [], "type": "component_event"},
    "Pedometer.Pause": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Pedometer.Reset": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Pedometer.Resume": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Pedometer.Save": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Pedometer.SimpleStep": {"paramNames": ["simpleSteps", "distance"], "type": "component_event"},
    "Pedometer.Start": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Pedometer.StartedMoving": {"paramNames": [], "type": "component_event"},
    "Pedometer.Stop": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Pedometer.StoppedMoving": {"paramNames": [], "type": "component_event"},
    "Pedometer.WalkStep": {"paramNames": ["walkSteps", "distance"], "type": "component_event"},
    "PhoneCall.MakePhoneCall": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "PhoneNumberPicker.AfterPicking": {"paramNames": [], "type": "component_event"},
    "PhoneNumberPicker.BeforePicking": {"paramNames": [], "type": "component_event"},
    "PhoneNumberPicker.GotFocus": {"paramNames": [], "type": "component_event"},
    "PhoneNumberPicker.LostFocus": {"paramNames": [], "type": "component_event"},
    "PhoneNumberPicker.Open": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "PhoneStatus.GetWifiIpAddress": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "PhoneStatus.isConnected": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "Player.Completed": {"paramNames": [], "type": "component_event"},
    "Player.Pause": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Player.PlayerError": {"paramNames": ["message"], "type": "component_event"},
    "Player.Start": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Player.Stop": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Player.Vibrate": {"kind": "statement", "paramNames": ["milliseconds"], "type": "component_method"},
    "Screen.BackPressed": {"paramNames": [], "type": "component_event"},
    "Screen.CloseScreenAnimation": {"kind": "statement", "paramNames": ["animType"], "type": "component_method"},
    "Screen.ErrorOccurred": {"paramNames": ["component", "functionName", "errorNumber", "message"], "type": "component_event"},
    "Screen.Initialize": {"paramNames": [], "type": "component_event"},
    "Screen.OpenScreenAnimation": {"kind": "statement", "paramNames": ["animType"], "type": "component_method"},
    "Screen.OtherScreenClosed": {"paramNames": ["otherScreenName", "result"], "type": "component_event"},
    "Screen.ScreenOrientationChanged": {"paramNames": [], "type": "component_event"},
    "Slider.PositionChanged": {"paramNames": ["thumbPosition"], "type": "component_event"},
    "Sound.Pause": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Sound.Play": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Sound.Resume": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Sound.SoundError": {"paramNames": ["message"], "type": "component_event"},
    "Sound.Stop": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Sound.Vibrate": {"kind": "statement", "paramNames": ["millisecs"], "type": "component_method"},
    "SoundRecorder.AfterSoundRecorded": {"paramNames": ["sound"], "type": "component_event"},
    "SoundRecorder.Start": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "SoundRecorder.StartedRecording": {"paramNames": [], "type": "component_event"},
    "SoundRecorder.Stop": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "SoundRecorder.StoppedRecording": {"paramNames": [], "type": "component_event"},
    "SpeechRecognizer.AfterGettingText": {"paramNames": ["result"], "type": "component_event"},
    "SpeechRecognizer.BeforeGettingText": {"paramNames": [], "type": "component_event"},
    "SpeechRecognizer.GetText": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "TextBox.GotFocus": {"paramNames": [], "type": "component_event"},
    "TextBox.HideKeyboard": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "TextBox.LostFocus": {"paramNames": [], "type": "component_event"},
    "TextToSpeech.AfterSpeaking": {"paramNames": ["result"], "type": "component_event"},
    "TextToSpeech.BeforeSpeaking": {"paramNames": [], "type": "component_event"},
    "TextToSpeech.Speak": {"kind": "statement", "paramNames": ["message"], "type": "component_method"},
    "Texting.MessageReceived": {"paramNames": ["number", "messageText"], "type": "component_event"},
    "Texting.SendMessage": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "TinyDB.GetValue": {"kind": "expression", "paramNames": ["tag", ""], "type": "component_method"},
    "TinyDB.StoreValue": {"kind": "statement", "paramNames": ["tag", "valueToStore"], "type": "component_method"},
    "TinyWebDB.GetValue": {"kind": "statement", "paramNames": ["tag"], "type": "component_method"},
    "TinyWebDB.GotValue": {"paramNames": ["tagFromWebDB", "valueFromWebDB"], "type": "component_event"},
    "TinyWebDB.StoreValue": {"kind": "statement", "paramNames": ["tag", "valueToStore"], "type": "component_method"},
    "TinyWebDB.ValueStored": {"paramNames": [], "type": "component_event"},
    "TinyWebDB.WebServiceError": {"paramNames": ["message"], "type": "component_event"},
    "Twitter.Authorize": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.CheckAuthorized": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.DeAuthorize": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.DirectMessage": {"kind": "statement", "paramNames": ["user", "message"], "type": "component_method"},
    "Twitter.DirectMessagesReceived": {"paramNames": ["messages"], "type": "component_event"},
    "Twitter.Follow": {"kind": "statement", "paramNames": ["user"], "type": "component_method"},
    "Twitter.FollowersReceived": {"paramNames": ["followers2"], "type": "component_event"},
    "Twitter.FriendTimelineReceived": {"paramNames": ["timeline"], "type": "component_event"},
    "Twitter.IsAuthorized": {"paramNames": [], "type": "component_event"},
    "Twitter.Login": {"kind": "statement", "paramNames": ["username", "password"], "type": "component_method"},
    "Twitter.MentionsReceived": {"paramNames": ["mentions"], "type": "component_event"},
    "Twitter.RequestDirectMessages": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.RequestFollowers": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.RequestFriendTimeline": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.RequestMentions": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.SearchSuccessful": {"paramNames": ["searchResults"], "type": "component_event"},
    "Twitter.SearchTwitter": {"kind": "statement", "paramNames": ["query"], "type": "component_method"},
    "Twitter.SetStatus": {"kind": "statement", "paramNames": ["status"], "type": "component_method"},
    "Twitter.StopFollowing": {"kind": "statement", "paramNames": ["user"], "type": "component_method"},
    "VideoPlayer.Completed": {"paramNames": [], "type": "component_event"},
    "VideoPlayer.GetDuration": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "VideoPlayer.Pause": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "VideoPlayer.SeekTo": {"kind": "statement", "paramNames": ["ms"], "type": "component_method"},
    "VideoPlayer.Start": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "VideoPlayer.VideoPlayerError": {"paramNames": ["message"], "type": "component_event"},
    "Voting.GotBallot": {"paramNames": [], "type": "component_event"},
    "Voting.GotBallotConfirmation": {"paramNames": [], "type": "component_event"},
    "Voting.NoOpenPoll": {"paramNames": [], "type": "component_event"},
    "Voting.RequestBallot": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Voting.SendBallot": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Voting.WebServiceError": {"paramNames": ["message"], "type": "component_event"},
    "Web.BuildRequestData": {"kind": "expression", "paramNames": ["list", ""], "type": "component_method"},
    "Web.ClearCookies": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Web.Delete": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Web.Get": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Web.GotFile": {"paramNames": ["url", "responseCode", "responseType", "fileName"], "type": "component_event"},
    "Web.GotText": {"paramNames": ["url", "responseCode", "responseType", "responseContent"], "type": "component_event"},
    "Web.HtmlTextDecode": {"kind": "expression", "paramNames": ["htmlText", ""], "type": "component_method"},
    "Web.JsonTextDecode": {"kind": "expression", "paramNames": ["jsonText", ""], "type": "component_method"},
    "Web.PostFile": {"kind": "statement", "paramNames": ["path"], "type": "component_method"},
    "Web.PostText": {"kind": "statement", "paramNames": ["text"], "type": "component_method"},
    "Web.PostTextWithEncoding": {"kind": "statement", "paramNames": ["text", "encoding"], "type": "component_method"},
    "Web.PutFile": {"kind": "statement", "paramNames": ["path"], "type": "component_method"},
    "Web.PutText": {"kind": "statement", "paramNames": ["text"], "type": "component_method"},
    "Web.PutTextWithEncoding": {"kind": "statement", "paramNames": ["text", "encoding"], "type": "component_method"},
    "Web.UriEncode": {"kind": "expression", "paramNames": ["text", ""], "type": "component_method"},
    "WebViewer.CanGoBack": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "WebViewer.CanGoForward": {"kind": "expression", "paramNames": [""], "type": "component_method"},
    "WebViewer.ClearLocations": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "WebViewer.GoBack": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "WebViewer.GoForward": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "WebViewer.GoHome": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "WebViewer.GoToUrl": {"kind": "statement", "paramNames": ["url"], "type": "component_method"}
}

''' List of AI2 component names. '''
AI2_component_names = [ # [2016/08/06, lyn], current list of AI2 componenets, as of today
    "AccelerometerSensor", 
    "ActivityStarter", 
    "Ball", 
    "BarcodeScanner",
    "BluetoothClient", 
    "BluetoothServer",
    "Button", 
    "Camcorder", 
    "Camera", 
    "Canvas", 
    "CheckBox", 
    "Clock", 
    "ContactPicker", 
    "DatePicker", 
    "EmailPicker", 
    "Ev3Motors", 
    "Ev3ColorSensor", 
    "Ev3GyroSensor", 
    "Ev3TouchSensor", 
    "Ev3UltrasonicSensor", 
    "Ev3Sound", 
    "Ev3UI", 
    "Ev3Commands", 
    "File", 
    "FirebaseDB", 
    "FusiontablesControl", 
    "GameClient", 
    "GyroscopeSensor", 
    "HorizontalArrangement", 
    "Image", 
    "ImagePicker", 
    "ImageSprite", 
    "Label", 
    "ListPicker", 
    "ListView", 
    "LocationSensor", 
    "NearField", 
    "Notifier", 
    "NxtColorSensor", 
    "NxtDirectCommands", 
    "NxtDrive", 
    "NxtLightSensor", 
    "NxtSoundSensor", 
    "NxtTouchSensor", 
    "NxtUltrasonicSensor", 
    "OrientationSensor", 
    "PasswordTextBox", 
    "Pedometer", 
    "PhoneCall", 
    "PhoneNumberPicker", 
    "PhoneStatus", 
    "Player", 
    "ProximitySensor", 
    "Screen", 
    "Slider", 
    "Sound", 
    "SoundRecorder", 
    "SpeechRecognizer", 
    "Spinner", 
    "TableArrangement", 
    "TextBox", 
    "Texting", 
    "TextToSpeech", 
    "TimePicker", 
    "TinyDB", 
    "TinyWebDB", 
    "Twitter", 
    "VerticalArrangement", 
    "VerticalScrollArrangement", 
    "VideoPlayer", 
    "Voting", 
    "Web", 
    "WebViewer",
    "YandexTranslate"
]


logFileName = '*unopenedFilename*'
logPrefix = 'ai2summarizerLyn'
printMessagesToConsole = True

def createLogFile():
    global logFileName
    if not os.path.exists("logs"):
        os.mkdir("logs")
    startTimeString = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")    
    logFileName = "logs/" + logPrefix + '-' + startTimeString

def logwrite (msg): 
    with open (logFileName, 'a') as logFile: 
        if printMessagesToConsole:
            print(msg) 
        logFile.write(msg + "\n")

# [2016/08/12, lyn] No longer needed 
'''
def padWithZeroes(num, digits):
  s = str(num)
  digitsToGo = digits - len(s)
  if digitsToGo > 0:
    return ('0' * digitsToGo) + s
  else: 
    return s
'''

# [2016/08/12, lyn] indexedDir is no longer used; it is superseded by topDir (see below)
#indexedDir = '/Users/fturbak/Projects/AppInventor2Stats/data/ai2_users_long_term_randomized'
#summaryDir = '/Users/fturbak/Projects/AppInventor2Stats/data/ai2_users_long_term_randomized_2016_08_06_test1'
#indexedDir = '/Users/Maja/Documents/AI/biggerprojects/ai2_users_long_term_randomized'
#summaryDir = '/Users/Maja/Documents/AI/biggerprojects/ai2_users_long_term_randomized_2016_08_07_test1'

topDir = '/Users/fturbak/Projects/AppInventor2Stats/data/ai2_users_long_term_randomized'
summaryDir = '/Users/fturbak/Projects/AppInventor2Stats/data/ai2_users_long_term_randomized_2016_08_13_nontop_final'
#topDir = '/Users/fturbak/Projects/AppInventor2Stats/data/benji_ai2_users_random'
#summaryDir = '/Users/fturbak/Projects/AppInventor2Stats/data/benji_ai2_users_random_2016_08_13_nontop_final'

# [2016/08/12, lyn] The following code is modified to handle more general input directory structure for data 
lastDirectoryProcessedFilename = 'lastDirectoryProcessed.txt'
lastTopDirFilename = 'lastTopDir.txt'

def readLastDirectoryProcessed(): 
    if not os.path.exists(lastDirectoryProcessedFilename):
        return None
    else:
        with open(lastDirectoryProcessedFilename, 'r') as inFile:
            return inFile.readline().strip()

def writeLastDirectoryProcessed(dirName): 
    with open(lastDirectoryProcessedFilename, 'w') as outFile:
        outFile.write(dirName)

def readLastTopDir(): 
    if not os.path.exists(lastTopDirFilename):
        return None
    else: 
        with open(lastTopDirFilename, 'r') as inFile:
            return inFile.readline().strip()

def writeLastTopDir(dirName): 
    with open(lastTopDirFilename, 'w') as outFile:
        outFile.write(dirName)

def processNext(): 
    if topDir != readLastTopDir():
        fromBeginning = True
        if os.path.exists(lastDirectoryProcessedFilename):
            os.remove(lastDirectoryProcessedFilename)
    elif os.path.exists(lastDirectoryProcessedFilename):
        # We have a choice: to continue with file after last one completely process, or do start fresh.
        lastDirectory = readLastDirectoryProcessed()
        logwrite("You have already processed directories through " + lastDirectory + ".")
        logwrite("To continue processing with the next directory, enter any input *other* than B or b.")
        logwrite("To process all directories again from the beginning, enter B or b.")
        answer = raw_input("> ").strip().lower()
        logwrite(answer)
        fromBeginning = (answer == 'b')
        if fromBeginning:
            os.remove(lastDirectoryProcessedFilename)
    else:
        fromBeginning = True
    writeLastTopDir(topDir)
    createLogFile()
    if isDirectoryOfUserDirectories(topDir): # Is topDir a directory of users? 
        # If so, process directly with processDir
        processDir('') # I.e., only use topDir
    else: # Otherwise, process subdirs of topDir with processDir
        allFiles = os.listdir(topDir)
        allDirs = [file for file in allFiles if os.path.isdir(os.path.join(topDir, file))]
        allDirsSorted = sorted(allDirs)
        lastIndex = len(allDirsSorted) - 1
        if fromBeginning:
            nextIndex = 0
        else: 
            nextIndex = allDirsSorted.index(lastDirectory) + 1
        while nextIndex <= lastIndex:
            nextDir = allDirsSorted[nextIndex]
            processDir(nextDir)
            writeLastDirectoryProcessed(nextDir)
            nextIndex += 1        

def processDir(dir): 
    global num_missing_properties, num_missing_meta, num_missing_scm, num_case_mismatches
    num_missing_properties = 0
    num_missing_meta = 0 
    num_missing_scm = 0
    num_case_mismatches = 0
    start = datetime.datetime.now()
    logwrite('*** Start processing directory {} with topSummary={} at {}'.format(dir, str(topSummary), str(start)))
    allProjectsToJSONFiles(os.path.join(topDir, dir), None, os.path.join(summaryDir, dir))
    end = datetime.datetime.now()
    logwrite('*** Done processing directory {} with topSummary={} at {}'.format(dir, str(topSummary), str(end)))
    logwrite("ran in {}".format(end-start))
    logwrite("Num missing project.properties: {}. Num missing META: {}. Num missing SCM: {}. Num case mismatches: {}".format(num_missing_properties, num_missing_meta, num_missing_scm, num_case_mismatches))


# Returns True if first subdir of dir is a directory of containing projects
# If there are no subdirs, return False
def isDirectoryOfUserDirectories(dir):
    for fileOrDir in os.listdir(dir):
        absPath = os.path.join(dir, fileOrDir)
        if os.path.isdir(absPath):
            return isUserDirectory(absPath)
    return False

# Returns True if directory contains a .aia or .zip project or directories that are ProjectDirectory
# Returns false otherwise. 
def isUserDirectory(dir):
    for fileOrDir in os.listdir(dir):
        absPath = os.path.join(dir, fileOrDir)
        if absPath.endswith('.aia') or absPath.endswith('.zip'): # Ignore other regular files
            return True
        elif os.path.isdir(absPath):
            return isProjectDir(absPath)
    return False

tutorialsInputDir = '/Users/fturbak/Projects/AppInventor2Stats/code/ai2_tutorialfinder/Tutorials'
tutorialsOutputDir = '/Users/fturbak/Projects/AppInventor2Stats/data/tutorial_summaries_top_2016_08_19'

# tutorialsInputDir = '/Users/Maja/Documents/AI/Tutorials'
# tutorialsOutputDir = '/Users/Maja/Documents/AI/Tutorials/summariesTest1'

# *** Added by Maja [2016-08-07]
topSummary = True # Global variable as flag for which kind of summary we are trying to produce
#topSummary = False

def processTutorials():
    allProjectsToJSONFiles(tutorialsInputDir, None, tutorialsOutputDir)
    

if __name__=='__main__':  
    processNext()
    # processTutorials()
    # allProjectsToJSONFiles('/Users/Maja/Documents/AI/Tutorials', 100000)

# print 'running...'
# start = datetime.datetime.now()

# Maja's tests
#cleanup('/Users/Maja/Documents/AI/Tutorials', '.json')
#projectToJSONFile('/Users/Maja/Documents/AI/Tutorials/AI_website/PicCall.zip')
#allProjectsToJSONFiles('/Users/Maja/Documents/AI/Tutorials', 100000)
# findComponentType('hey', '/Users/Maja/Documents/AI/PaintPot2Old.zip', 'Screen1.scm')
#print upgradeFormat('Canvas_Clicked', '/Users/Maja/Documents/AI/PaintPot2Old.zip', 'Screen1.scm')


# Lyn's testsx
# cleanup('/Users/fturbak/Projects/AppInventor2Stats/data/benji_ai2_users_random', '.zip')
# allProjectsToJSONFiles('/Users/fturbak/Projects/AppInventor2Stats/data/benji_ai2_users_random', 10)
# allProjectsToJSONFiles('/Users/fturbak/Projects/AppInventor2Stats/data/benji_ai2_users_random', 10003
# projectToJSONFile('/Users/fturbak/Projects/AppInventor2Stats/data/MIT-tutorials/HelloPurr.aia')

# This doesn't work because of splitting on dots!
# allProjectsToJSONFiles('../../../data/ai2_users_long_term_randomized/00', 1000

# allProjectsToJSONFiles('/Users/fturbak/Projects/AppInventor2Stats/data/benji_ai2_users_random_copy', 10000)
# allProjectsToJSONFiles('/Users/fturbak/Projects/AppInventor2Stats/data/ai2_users_long_term_randomized/00', 1000)
# allProjectsToJSONFiles('/Users/fturbak/Projects/AppInventor2Stats/data/ai2_users_long_term_randomized/01', 1000)


# Benji's Tests
# dir_small = "/Users/bxie/Documents/ai2_users_long_term_15k" 
# N = 15000
# cleanup(dir_small, 'summary.json')
# print 'cleanup done...'
# allProjectsToJSONFiles(dir_small, N)

# end = datetime.datetime.now()
# print 'done!'
# print "ran in {}".format(end-start)
# print "Num missing project.properties: {}. Num missing META: {}. Num missing SCM: {}. Num case mismatches: {}".format(num_missing_properties, num_missing_meta, num_missing_scm, num_case_mismatches)


