# Predicting Language

## Task

- Filtered users to subset that started (creation dates) at least MAXDUR days (where MAXDUR=300) before the end of data collection
- Code summary features: average number of orphan blocks (a block unconnected to any other blocks), and number of orphan blocks in decile, average number of top level blocks, and number of top level blocks in decile, number of screens in project and number of screens created in decile, number of variables (global and local). 

## Experiments

All results are accuracies with 3-fold cross-validation.


### Time features only
 KNN Score: 0.589892076862
 F1 Score: 0.680842365005

 KNN Score: 0.587482688122
 F1 Score: 0.6756788812 
 
 KNN Score: 0.591509309389
 F1 Score: 0.680737852999


### Code features only
KNN Score: 0.504211634641
F1 Score: 0.593063706722

KNN Score: 0.506957726044
F1 Score: 0.598597681528

KNN Score: 0.508253004093
F1 Score: 0.596349186174
### All features

Chance is 44.59384683
Building a model with 55 features for LANGUAGE

KNN Score: 0.592261121348
F1 Score:  0.681591036075 

KNN Score: 0.590186638528
F1 Score:  0.675606318659

KNN Score: 0.594744486993
F1 Score:  0.681477205817
