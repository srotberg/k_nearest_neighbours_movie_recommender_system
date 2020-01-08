# k-Nearest Neighbours Movie Recommender System
This [script](https://github.com/srotberg/movie_k_nearest_neighbours_recommender_system/blob/master/k-nearest_neighbours_recommender_system_example.py) recommends movies that user_id has not yet seen. The code is based 
on the how similar user_id is in taste to other users. The system generates a list of the k most similar users based on a distance function that takes into account the difference in adjusted movie ratings of each user relative to the adjusted movie ratings by user_id and the number of movies both user_id and each other user saw. Then, the system takes all the movies user_id has not seen but the k most similar users have seen and weighs them by the average rating they got from the k most similar users and by the number of k most similar users who saw them. It lists the movies from top to bottom ratings.

You will need to use these packages:
* pandas 
* numpy
* copy
* from operator import itemgetter
