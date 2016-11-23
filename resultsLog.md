# Log of results

## Features
- Time features: number of projects created in each decile of time period, number of projects created on each day of the week, mean and stdev of length of projects, mean and stdev of intervals between projects, number of projects.

- Code summary features: average number of orphan blocks (a block unconnected to any other blocks), andnumber of orphan blocks in decile, average number of top level blocks, and number of top level blocks \
in decile, number of screens in project and number of screens created in decile.

## Task: Predicting User Retention

- Filtered users to subset that started (creation dates) at least MAXDUR days (where MAXDUR=300) before the end of data collection
- Predict, using first MINDUR days of activity, whether user "survives" for more than MINDUR days (where MINDUR=150) as indicated by creation dates
- This gives us 25346 users of the original 46320, roughly balanced between survivors and non-survivors

### Experiments

Chance is 0.5266

#### Time features only
KNN accuracy:  0.8562
KNN f1 score: 0.8330

Logistic regression accuracy: 0.8331
Logistic regression f1 score: 0.8067

#### Code features only
KNN accuracy: 0.6664
KNN f1 score: 0.5672

Logistic regression accuracy: 0.6786
Logistic regression f1 score: 0.6370

#### Time and code features

KNN accuracy: 0.8109 
KNN f1 score: 0.7683

Logistic regression accuracy: 0.8361
Logistic regression f1 score: 0.8117

## Task: Predicting User Language

Language labels come from running `langid` on user's strings and variables.
Only languages with at least 500 users are retained. 
Can we predict a user's language from their coding patterns?

### Experiments

Chance is 0.5143

#### Time features only

Logistic regression accuracy: 0.5337

#### Code features only
Logistic regression accuracy: 0.5874

### Time and code features
Logistic regression accuracy: 0.5984

 