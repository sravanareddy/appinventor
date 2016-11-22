# Predicting User Retention

## Task

- Filtered users to subset that started (creation dates) at least MAXDUR days (where MAXDUR=300) before the end of data collection
- Predict, using first MINDUR days of activity, whether user "survives" for more than MINDUR days (where MINDUR=150) as indicated by creation dates
- This gives us 25324 users of the original 46319, roughly balanced between survivors and non-survivors
- Time features: number/percentage of projects created in each decile of time period, number/percentage of projects created on each day of the week, average length of projects (using created date). 
- Code summary features: average number of orphan blocks (a block unconnected to any other blocks), and number of orphan blocks in decile, average number of top level blocks, and number of top level blocks in decile, number of screens in project and number of screens created in decile. 

## Experiments

Chance is 0.52772073922
### All features 
All features KNN Score:  0.753849798626
All features KNN f1 score 0.7040729137 

All features Logistic Regression Score:  0.765103056148
All features Logistic f1 score 0.731482735274

All features KNN Score:  0.746624022743
All features KNN f1 score 0.695862363145 

All features Logistic Regression Score:  0.757640369581
All features Logistic f1 score 0.719187482844

All features KNN Score:  0.751658767773
All features KNN f1 score 0.698764012647 

All features Logistic Regression Score:  0.752488151659
All features Logistic f1 score 0.715201090661

### Time features only
Time features KNN Score:  0.787254205165
Time features KNN f1 score 0.750347511815 

Time features Logistic Regression Score:  0.527718550107
Time features Logistic f1 score 0.0

Time features KNN Score:  0.767945984364
Time features KNN f1 score 0.728783054133 

Time features Logistic Regression Score:  0.527718550107
Time features Logistic f1 score 0.0

Time features KNN Score:  0.781161137441
Time features KNN f1 score 0.743436588415 

Time features Logistic Regression Score:  0.527725118483
Time features Logistic f1 score 0.0
### Code features only

Code features KNN Score: 0.661809997631
Code features KNN f1 score 0.570741241919 

Code features Logistic Regression Score:  0.673300165837
Code features Logistic f1 score 0.63412045635

Code features KNN Score:  0.656479507226
Code features KNN f1 score 0.565477974228 

Code features Logistic Regression Score:  0.66583747927
Code features Logistic f1 score 0.621189740835

Code features KNN Score:  0.657701421801
Code features KNN f1 score 0.568096875467 

Code features Logistic Regression Score:  0.66528436019
Code features Logistic f1 score 0.625082946251


