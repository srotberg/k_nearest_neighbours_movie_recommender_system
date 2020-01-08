"""
k-nearest neighbours recommender system
The system recommends movies that a user_id has not yet seen
based on the how similar they are in taste other users. 
The system generates a list of k most similar users based on 
a distance function that takes into account the difference
in adjusted ratings of each user from user_id and the number
of movies both of them saw. Then, the system takes all the movies 
user_id has not seen and weighs them their average rating and 
by the number of k most similar other users who saw them
"""

import pandas as pd
import numpy as np
import copy
from operator import itemgetter

def create_utility_matrix(file_name,highest_rating):
    """ Returns an array utility_matrix with user id 
    (represented as an index number) for the rows and movie id 
    (represented as an index number) for the columns. 
    Each cell in utility_matrix is a user rating of a specific movie. 
    Also returns dictionaries user_index_to_id and movie_index_to_id
    which map a user_index in the matrix to their id and a movie index
    in the matrix to their id.
        
    Args:
        file_name: string used to read the .csv file
        
        highest_rating: float which is the highest possible rating
        a user can give a movie
    """
    
    # gets the file as a DataFrame
    df=pd.read_csv(file_name)
        
    # creates a dictionary mapping indeces to id's
    user_index_to_id={}
    movie_index_to_id={}
    
    # keeps track of the key that will be used in the matrix
    count_user_index=0
    count_movie_index=0
    
    # iterating over all the rows in df to find the number of
    # user_ids and number of movie_ids which are important for knowing
    # the utility matrix dimensions
    for key, row in df.iterrows():
                
        # checks if user_id is already in the dictionary
        if row[0] not in user_index_to_id.values():
            
            # adds row[0] to the dictionary and the key is just a count-up           
            user_index_to_id[str(count_user_index)]=row[0]
            
            # raises the count by 1
            count_user_index+=1
                        
        # checks if movie_id is a value in the dictionary
        if row[1] not in movie_index_to_id.values():
            
            # adds row[1] to the dictionary and the key is just a count-up
            movie_index_to_id[str(count_movie_index)]=row[1]
                        
            count_movie_index+=1        
        
    # initializes the utility matrix with all cells equal to 20*highest_rating
    utility_matrix=np.ones((count_user_index,count_movie_index))*\
        -(20*highest_rating)
                            
    # keeps track of the indeces of df
    count_index=0
        
    # iterating over all the rows in df
    for key, row in df.iterrows():
                
        # finds the row of the curernt index
        index_1=df.iloc[count_index]
                   
        # increases count_index by 1
        count_index+=1
        
        # gets the user and movie indeces based on the id of the
        # user and movie from df
        user_index=int(list(user_index_to_id.keys())\
                   [list(user_index_to_id.values()).index(index_1[0])])
        movie_index=int(list(movie_index_to_id.keys())\
                    [list(movie_index_to_id.values()).index(index_1[1])])
        
        # gives the value of the rating associated with
        # the cell in df to the utility matrix at indeces user_index
        # and movie_index
        utility_matrix[user_index,movie_index]=\
            float(index_1[2])
        
    return [utility_matrix,user_index_to_id,movie_index_to_id]

def adjust_ratings(utility_matrix,highest_rating):
    """ Returns updated array called utility_matrix which adjusts the ratings
    of a user up if they never rated any movie a 5. So for instance,
    of the highest rating is 4 and the highest rating possible is 5,
    then all ratings are raised by 1
    
    Args:
        utility_matrix: an array of preferences for users and movies
        
        highest_rating: float which is the highest rating possible
    """
    
    # loops over all the rows in the matrix
    for row in range(len(utility_matrix)):
        
        # adjusts the ratings of the current row
        # by adding the highest rating possible and subtracting the 
        # highest the user has ranked
        utility_matrix[row,:]=utility_matrix[row,:]+\
            highest_rating-np.amax(utility_matrix[row,:])
            
    utility_matrix[utility_matrix<-16*highest_rating]=-20*highest_rating
                        
    return utility_matrix
                    
def k_nearest_neighbours\
    (utility_matrix,user_index_to_id,k_nearest,user_id,highest_rating,\
     minimum_movies_both_users_have_to_watch):
    """ Returns a list called k_nearest_dict, which lists the
    users who have the most overlapping preferences with user_id,
    whom we are recommending movies to.
    It also returns an array with the number of movies
    each k nearest neighbours saw that user_id also saw
    
    Args:
        utility_matrix: array of preferences for users and movies
        
        user_index_to_id: array that maps user index to user_id
        
        k_nearest: integer which is telling us how 
        
        many neighbours to look for with similar preferences
        
        user_id: integer of the user_id we are recommending to   
        
        highest_rating: float that indicates what is the highest possbile 
        movie rating
        
        minimum_movies_both_users_have_to_watch: integer of how
        many movies both user have to watch to consider adding the user
        as a nearest neighbour
    """
    
    # gets the user index based on the id of the user
    user_index=int(list(user_index_to_id.keys())\
        [list(user_index_to_id.values()).index(user_id)])
    
    # creates a dictionary with user_index as key and with value that is the
    # distance in movie preferences
    k_nearest_dict={}
    k_nearest_array=np.ones(k_nearest)*10000000000
    k_nearest_index_array=np.ones(k_nearest)*-1
    k_nearest_overlap_array=np.zeros(k_nearest)
    
    # loops over all the rows in utility_matrix
    for row in range(len(utility_matrix)):
                
        # checks if the user_id is different than the one given
        if row!=user_index:
                
            # gets the row for the user_id we are interested in
            user_preferences=\
                copy.deepcopy(utility_matrix[user_index,:])
                                       
            user_preferences[user_preferences>=0]=1
                        
            # sets all the cells that are greater than 90 to 0
            # these are movies that user_index has the not seen
            user_preferences[user_preferences<-16*highest_rating]=0
                        
            # gets the user preferences 
            user_compared_preferences=\
                copy.deepcopy(utility_matrix[row,:])
           
            user_compared_preferences\
                [user_compared_preferences>=0]=1
            
            # sets all the cells that are less than -90 to 0
            # these are movies that row had the not seen
            # but the other user has
            user_compared_preferences\
                [user_compared_preferences<-16*highest_rating]=0
            
            # counts the number of overlaps
            number_of_movies_both_saw=\
                np.sum((user_compared_preferences!=0) & \
                       (user_preferences!=0))
                                                
            # gets the row for the user_id we are interested in
            user_preferences=\
                copy.deepcopy(utility_matrix[user_index,:])
            
            # gets the user preferences 
            user_compared_preferences=\
                copy.deepcopy(utility_matrix[row,:])
            
            # subtracts one vector from another
            distance=np.subtract\
                (user_preferences,user_compared_preferences)
             
            # excludes the movies without overlap                         
            distance[distance<-16*highest_rating]=0
            distance[distance>16*highest_rating]=0
                        
            # measures the distance in preferences
            distance_scalar=np.sum(list(np.array(distance)**2))
            
            # multiply scalar
            multiply_scalar=1000
                        
            # checks if both users saww any of the same movies
            if number_of_movies_both_saw>0: 
            
                objective_function=\
                    (distance_scalar/(number_of_movies_both_saw**2))+\
                    (multiply_scalar/number_of_movies_both_saw)
                    
            else:
                
                objective_function=max(k_nearest_array)+1
            
            # finds the location of the minimum point
            loc=np.argmax(k_nearest_array)
                                
            # checks if the distance/number_of_movies_both_saw
            # is greater than the minimum value in the array
            # and if they had any overlap
            if objective_function<\
                max(k_nearest_array) and \
                number_of_movies_both_saw>\
                minimum_movies_both_users_have_to_watch:
                
                # finds the location of the minimum point
                loc=np.argmax(k_nearest_array)
                
                # replaces the minimum with the current distance in taste
                k_nearest_array[loc]=\
                    objective_function
                
                # saves the index of the user in the array by
                # replacing the index of the user with the least 
                # overlaps with the user of interest
                k_nearest_index_array[loc]=\
                    row
                    
                k_nearest_overlap_array[loc]=\
                    number_of_movies_both_saw
                                                                               
    # loops over the number of nearest neighbours
    for index in range(len(k_nearest_index_array)):
        
        # checke that there was a neighbour to look at
        if k_nearest_index_array[index]!=-1:
          
            # adds to the dictionary the index as key and the values
            # are the number of overlaps
            k_nearest_dict\
                [k_nearest_index_array[index]]=\
                k_nearest_array[index]
          
    return [k_nearest_dict,k_nearest_overlap_array]
                
def list_of_movies_user_id_has_not_seen\
    (utility_matrix,user_index_to_id,movie_index_to_id,
     k_nearest,user_id,highest_rating):
    """ Returns a list called movies_user_id_hasnt_seen 
    which lists the movie indeces that the k_nearest neighbours saw,
    but user_id did not
    
    Args:
        utility_matrix: array with user index and movie index for movie preferences
        
        user_index_to_id: dictionary that maps user_index to user_id
        
        movie_index_to_id: dictionary that maps movie_index to movie_id
        
        k_nearest: dictionary of the overlapping movies
        
        user_id: integer of the id of the user we are recommending movies to
        
        highest_rating: the highest possible rating for a movie
    """
    
    # initiates the list
    movies_user_id_hasnt_seen=[]
    
    # gets the user index for keys that are equal to user_id
    user_index=int(list(user_index_to_id.keys())\
               [list(user_index_to_id.values()).index(user_id)])
    
    # gets the preferences of the user with user_id
    user_preferences=copy.deepcopy(utility_matrix[user_index,:])
    
    # loops over all the rows in the matrix
    for user_index in k_nearest:
                                                   
        # gets the user preferences 
        user_compared_preferences=\
            copy.deepcopy(utility_matrix[int(user_index),:])
                
        # adds the two vectors together
        distance=np.subtract(user_preferences,user_compared_preferences)
        
        # sets all the cells that are greater than -higher_rating to 0.
        # these are movies that user with index row had the not seen
        distance[distance>-highest_rating]=0
                        
        # sets all the cells that are less than -90 to 0
        # these are movies that user_id had the not seen
        # but user_index has seen
        distance[distance<-16*highest_rating]=1
                
        # looping the overlapped vectors
        for movie_index in range(len(distance)):
                
            # checks if user_index has not seen the movie yet
            if distance[movie_index]==1:
                
                # checks if the movie was already added to the
                # list of movies user_id has not seen
                if movie_index not in movies_user_id_hasnt_seen:
                
                    # adds the movie_index to the list of 
                    # movies user_id has not yet seen but that
                    # the k_nearest neighbours have
                    movies_user_id_hasnt_seen.append(movie_index)
                    
    return movies_user_id_hasnt_seen

def average_rating_of_movies_user_has_not_seen\
    (utility_matrix,movies_user_id_hasnt_seen,user_index_to_id,\
     movie_index_to_id,k_nearest_dict,user_id,highest_rating,\
     weigh_by_popularity):
    """ Returns the average rating of a movie the k_nearest neighbours gave
    to a movie that user_id has not seen yet and someone in the 
    k_neighbours liked
    
    Args:
        utility_matrix: array of utility matrix based on user index and
        movie index which corresponds to a rating
        
        movies_user_id_hasnt_seen: a list of movie_indeces that user_id
        has not yet seen, but were seen the k_nearest neighbours
        
        user_index_to_id: dictionary that maps user_index to user_id
        
        movie_index_to_id: dictionarythat maps movie_index to movie_id
        
        k_nearest_dict: dictionary of k_neaerest neighbours and how
        similar they are to user_id in their preferences over movies
        they both saw
                
        user_id: integer which the id of the user we are recommending movies to
        
        highest_rating: flaot which is the highest rating possible for a movie
        
        weight_by_populariy: boolean which say whether to weight the 
        recommendation by the amount of k_nearest neighbours who saw the movie
    """
    
    # initiates a dictionary for movie_index as a kay and 
    # average rating as a value
    average_ratings={}
    
    # loops over all movie indeces that user_id has not seen
    # and one of the k_nearest neighbours liked
    for movie_index in movies_user_id_hasnt_seen:
    
        count=0
        rating=0
                        
        # loops over all the k_nearest neighbours indeces
        for user_index in k_nearest_dict:
                                        
            # gets the preferences of the neighbour user_index
            user_preferences=\
                copy.deepcopy(utility_matrix[int(user_index),:])
                    
            # checks if the user has seen movie_index
            if user_preferences[int(movie_index)]!=-20*highest_rating:
                
                # adds the rating of the user to rating
                rating+=user_preferences[int(movie_index)]
                
                # add one more count to
                count+=1
                
        # compute the average rating of movie_index
        rating=rating/count
        
        if (weigh_by_popularity==True) and (len(k_nearest_dict)-1)>0:
                                
            # adds the average rating to the list after 
            # adjusting it to the number
            # of neighbours who watch and the average rating
            average_ratings[movie_index]=\
                (rating+highest_rating*((count-1)/ \
                (len(k_nearest_dict)-1)))/ \
                (2*highest_rating)
                
        else:
            
            # adds the average rating to the list
            average_ratings[movie_index]=rating
        
    return average_ratings

def create_recommendation_list\
    (average_ratings,movie_index_to_id,\
    movie_id_file_name='movies_ids.csv'):
    """ Returns a sorted list from highest to lower 
    of movies with their rating.
    
    Args:
        average_ratings: dictionary with movie_index as key 
        and its rating as value
        movie_index_to_id: dictionary with movie_index as key 
        and movie_id as value
        movie_id_file_name: string for the name of the movie_id file
    """
        
    # read the movies_id and names as a DataFrame
    movie_id_to_name=pd.read_csv(movie_id_file_name)
    
    # initiates the recommendation list
    recommendation_list={}
        
    # loops over all average rating
    for movie_index in average_ratings:
                
        # gets the movie_ide based on the movie index
        movie_id=int(movie_index_to_id[str(int(movie_index))])
        
        # gets the movie info for movie id
        movie_info=\
             movie_id_to_name\
             [movie_id_to_name\
             [movie_id_to_name.columns[0]]==movie_id]
         
        # gets the name of the movie with movie_id
        movie_title=movie_info[movie_info.columns[1]].values[0]
                                  
        # checks if the movie is not already in the recommendation list
        if movie_title[0][0] not in recommendation_list:
                          
            recommendation_list\
                [movie_title]=\
                average_ratings[movie_index]
    
    sort_recommedation_list=\
        sorted(recommendation_list.items(),\
        key=itemgetter(1),reverse=True)
    
    return sort_recommedation_list

# user_id we are recommending movies to
user_id=10

# highest possible rating
highest_rating=5

# the number of most similar taste users we want to compare user_id
k_nearest=2

# the minimum number of movies both user_id and another user
# have had to see to be considered as a neighbour
minimum_movies_both_users_have_to_watch=1

# the ratings file name
file_name='ratings_list.csv'

# the file name mapping movie_id to movie name
movie_id_file_name='movies_ids.csv'

# checks whether to weigh the rating of the movie by the number
# of most similar users who have watch the movie
weigh_by_popularity=True

# checks if we need to create a utility matrix
utility_matrix_exists=True

# checks if there is a need to create utility_matrix
if not utility_matrix_exists:
                  
    # calls a function that creates two dictionaries mapping user index to
    # user id and movie index to movie id and also creates an array called
    # utility_matrix that maps user index and movie index to a rating.
    utility_matrix,user_index_to_id,movie_index_to_id=\
        create_utility_matrix(file_name,highest_rating)  
        
    # calls a function that adjusts the ratings of users who never give a 
    # the highest possible rating
    utility_matrix=\
        adjust_ratings\
        (utility_matrix,\
        highest_rating)
                
# calls a function that returns a dictionary of all the user indecs and
# distance in taste of the neighbours with the most similar tastes
k_nearest_dict,k_nearest_overlap_array=\
    k_nearest_neighbours\
    (utility_matrix,user_index_to_id,\
     k_nearest,user_id,highest_rating,\
     minimum_movies_both_users_have_to_watch)
        
# calls a function that  finds all the movies that the k_nearest neighbours
# saw but the user_id has not
movies_user_id_has_not_seen=\
    list_of_movies_user_id_has_not_seen\
    (utility_matrix,user_index_to_id,\
    movie_index_to_id,k_nearest_dict,user_id,\
    highest_rating)
              
# calls a function that calculates the average ratings of
# all the movies the user has not seen which can be based also
# on how many neighbours saw it
average_ratings=\
    average_rating_of_movies_user_has_not_seen\
    (utility_matrix,movies_user_id_has_not_seen,\
    user_index_to_id,movie_index_to_id,\
    k_nearest_dict,user_id,highest_rating,\
    weigh_by_popularity)
    
# generates the recommeded movies sorted by highest ratings to lowest ratings
recommendation_list=\
    create_recommendation_list\
    (average_ratings,\
    movie_index_to_id,\
    movie_id_file_name)