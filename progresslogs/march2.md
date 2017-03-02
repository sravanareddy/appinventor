March 2 Results

Things accomplished: 
-filtered out tutorials
-created new features 
    - getClasses (ie Clock, SpeechRecognizer, Canvas,etc.)
    - getMathBlocks (math and boolean operations)
-created new helper functions to redo deciles with: 
    -decileDict-  returns a dictionary with the key as the project name and the value as the decile
    -getAverageDecileValues- returns the average value in each decile

-reworked decileTypesTopLevelBlocks, decileNumScreens, and decileOrphanBlocks to be more efficient and incorpate the new decile helper functions



Filtered tutorials (91 features): 

Chance: 0.478097765171
Accuracy: 0.565181195054

-the confusion matrix looks messed up. 

With filtering and new loop features (95 features): 
Chance: 0.478097765171
Accuracy: 0.567674352816

With classes, filtering, and loops (138 features):

Chance: 0.478097765171
Accuracy: 0.641512151032


w/ classes filtering, loops, and reworked decile features(148 features)
Chance: 0.479275910811
Accuracy: 0.67529756169


With classes, no filtering and loops (138 features): 

Chance: 0.479275910811 
Accuracy: 0.68017855338

W/ classes, no filtering, and loops, and reworked decile features (148 feature)
Chance: 0.479275910811
Accuracy: 0.681432178677


