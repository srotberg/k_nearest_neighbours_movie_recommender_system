# k Nearest Neighbours Movie Recommender System
The system recommends movies that a user_id has not yet seen based on the how similar they are in taste other users.  
The system generates a list of k most similar users based on  a distance function that takes into account the difference 
in adjusted ratings of each user from user_id and the number of movies both of them saw. Then, the system takes all the movies 
user_id has not seen and weighs them their average rating and  by the number of k most similar other users who saw them.

You will need to use these packages:
pandas
numpy
copy
from operator import itemgetter
