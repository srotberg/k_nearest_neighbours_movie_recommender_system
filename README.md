# k-Nearest Neighbours Movie Recommender System
This [script](https://github.com/srotberg/movie_k_nearest_neighbours_recommender_system/blob/master/k-nearest_neighbours_recommender_system_example.py) recommends movies that user_id has not yet seen. The code is based 
on the how similar user_id is in taste to other users. The system generates a list of the k most similar users based on a distance function that takes into account the difference in adjusted movie ratings of each user relative to the adjusted movie ratings by user_id and the number of movies both user_id and each other user saw (I write about this problem below). Then, the system takes all the movies user_id has not seen but the k most similar users have seen and weighs them by the average rating they got from the k most similar users and by the number of k most similar users who saw them. It lists the movies from top to bottom ratings.

There is an interesting problem when it comes to deciding who the k-nearest neighbours are. Suppose we are recommending movies to Jack and user_1 only watched 1 movie that Jack watched but both Jack and user_1 gave the movie the exact same rating. Then, the distance in ratings between Jack and user_1 is zero. However, suppose user_2 watched 50 movies that Jack watched and they only differed in rating on one movie but gave all the other movies the same ratings. Then, the distance in ratings between Jack and user_2 is greater than 0. This means that user_1 seems to be more similar to Jack than user_2 if we do not consider the fact that user_2 watched more movies that Jack watched than user_1 did. To adjust for that, I create a function that uses both the similarity in ratings and the number of overlapping movies between Jack and the other user. Below is the function I use, where I define ```similar_taste``` to be the sum of squares of movie rating differences of movies both Jack and the other user saw and ```weight_on_taste``` is a number between 0 and 1 to be chosen by Jack: 
```
weight_on_taste*(1-1/(1+similar_taste))+(1-weight_on_taste)*()*((1/(1+number_of_movies_both_saw))
```
Notice that ```(1-1/(1+similar_taste))``` is a number between 0 and 1. It is 0 when ```similar_taste=0```(Jack and the other user are similar in taste) and it goes to ```1``` when ```similar_taste``` tends to infinity. So the more similar the taste, the smaller this term is, which implies a closer similarity to Jack. ```(1/(1+number_of_movies_both_saw)``` is similar; when ```number_of_movies_both_saw=0``` this term is ```1``` and as it goes to infinity it goes to 0, implying that Jack and the other user have watched many of the same movies. So the more overlapping movies, the lower this term is. Now, Jack will have to decide how much he cares about getting movie recommendations based on similar taste realtive to number of movie overlaps with other users, by picking ```weight_on_taste``` somewhere between ```0``` and ```1```.

When I take user_id=10 and use a weight on ratings equal to 0.2 with the 5 nearest neighbors, I get these as the top 10 recommendations:

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
