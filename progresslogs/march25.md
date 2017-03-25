(Sravana's fiddling)

1. Moved language labeling code to `namestrings_to_langs.py`. 
Re-ran `langid` in a more cautious fashion: 
inferring language of each token, combining log probabilities, and taking highest,
rather than concatenating tokens and classifying the result, 
which is problematic if the classifier uses bigrams.
Ignored Latin from candidates.
Wrote new `user_inferredlangs.json`.


   