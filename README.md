# k-Nearest Neighbours Movie Recommender System
This [script](https://github.com/srotberg/movie_k_nearest_neighbours_recommender_system/blob/master/k-nearest_neighbours_recommender_system_example.py) recommends movies that user_id has not yet seen. The code is based 
on the how similar user_id is in taste to other users. The system generates a list of the k most similar users based on a distance function that takes into account the difference in adjusted movie ratings of each user relative to the adjusted movie ratings by user_id and the number of movies both user_id and each other user saw. Then, the system takes all the movies user_id has not seen but the k most similar users have seen and weighs them by the average rating they got from the k most similar users and by the number of k most similar users who saw them. It lists the movies from top to bottom ratings.

For exmaple, when I take user_id=10 and use a weight on ratings equal to 0.2 with the 5 nearest neighbors, I get these as the top 10 recommendations:

|Top 10 Rated Movies by user_id=10|Top 10 Recommendations|
|-------------------|----------------------|
| The Intern (2015)| Godfather, The (1972)|
| First Daughter (2004)| Raiders of the Lost Ark (Indiana Jones and the Raiders of the Lost Ark) (1981)|
| Skyfall (2012) | Inception (2010)|
| Dark Knight Rises, The (2012)|Star Wars: Episode VI - Return of the Jedi (1983)|
| Troy (2004)| Star Wars: Episode V - The Empire Strikes Back (1980)|
| King's Speech, The (2010)| Star Wars: Episode IV - A New Hope (1977)|
| Notebook, The (2004)|Back to the Future (1985)|
| Despicable Me (2010)|Goodfellas (1990)|
| Education, An (2009) |Reservoir Dogs (1992)|
| Batman Begins (2005) |Guardians of the Galaxy (2014)|

You will need to use these packages:
* pandas 
* numpy
* copy
