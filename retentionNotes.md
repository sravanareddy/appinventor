# Predicting User Retention

## Task

- Filtered users to subset that started (creation dates) at least MAXDUR days (where MAXDUR=300) before the end of data collection
- Predict, using first MINDUR days of activity, whether user "survives" for more than MINDUR days (where MINDUR=150) as indicated by creation dates
- This gives us 25324 users of the original 46319, roughly balanced between survivors and non-survivors
- Time features: number/percentage of projects created in each decile of time period, number/percentage of projects created on each day of the week, average length of projects (using modified date). **clarify if needed**
- Code summary features: **fill in** 

## Experiments

All results are accuracies with 3-fold cross-validation.

### Time features only

**fill in average 3-fold accuracy using the best combinations of features, with the best classifier and normalization settings**

### Code features only

** fill in as before **
 

