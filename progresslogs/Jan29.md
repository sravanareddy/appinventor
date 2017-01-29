January 29th 

-used Eni's tutorial comparison code to create dictionary of all projects that aren't tutorials {user: projects} that matches the layout of the summaries layout. 

-changed getAllProjects to either get all projects including tutorials, or to get all projects w/o tutorials. (I added an parameter, so if True if we want to filter, False if we don't want to filter out tuorials) 

-added code that mirrors the vectorizing code, but now "vectorizes" and fits a model that doesn't contain the tutorials 

-changed getProjectsinMINDUR to only look at the first 120 days (instead of the previous 150), so that we are not using data in the last 30 days of the user's activity. 


Issues: 
-I'm still not getting the right values when I run the code, so maybe we can look at that again on Thursday.

-there are 139 users who only had tutorials...so we probably should totally filter them out 

- The scores went down for me after the filtering (but my scores are pretty off)