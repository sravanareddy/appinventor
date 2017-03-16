
**Not filtering tutorials** 

Mahesh's results: ~0.89

Mahesh's results + only top 200 blocks (334 features): 
accuracy: 0.862142694761

top 500 + l1 regression (using static kfold) scaled
accuracy: 0.903195723405

top 500 + l1 regression (using static kfold) with English scaled
accuracy: ~0.905  (didn't record full number)

3/15 realized that I was double counting control features (also in allBlocks) new accuracies:
(w/ English and 591 features) 
**accuracy: 0.903150757842**


**Filtering tutorials** 

3/15 w/ English (591 features) 

**accuracy: 0.903662642851**
f1score: 0.84497938259222116


created block_by_category.json that has all of the blocks ordered by their headings 
certainly no other languages that I can see

databricks need credit card to set up 

created coefs.json to look at coefficients of the features  
