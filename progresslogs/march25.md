(Sravana's fiddling)

1. Moved language labeling code to `namestrings_to_langs.py`. 
Ignored Latin from candidates, using next-best language instead.
Wrote new `user_inferredlangs.json`.

735 users were ignored because of fewer than 50 eligible tokens (variable names and strings).

2. Did some minor re-org of notebook code. 
To save memory, store non-tutorials as set of project names rather than summary dict.


   