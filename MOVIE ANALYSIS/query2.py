
import csv
import pickle
from collections import defaultdict

#Write a Python script that calculates the average popularity and total vote count for movies with a budget over $20 million,
#grouped by genre. The resulting pickle file must contain a list of tuples, each containing the genre, average popularity,
# and total vote count.

"""

Task: Retrieve the votes and popularity of movies with a budget above $20 million, grouped by genre.

Results: Movie name || Genre || Popularity || Votes

Procedure:
1. Select movies based on budget from the dataset movies_table.csv (to get popularity and vote_count)
2. Cross-reference with the Genres_table.csv file
3. Collect all genres from the resulting array, calculate the average popularity and total votes

Expected output:
("Action", 12.5, 23435)
("Drama", 8.7, 12340)
# Format → (genre, average popularity, total votes)







"""


def filter_movies_by_budget(dataset_csv, budget_limit=20_000_000):
    '''
    Filters movies by budget.
    '''

    #Lista che contiene tutti i film
    filtered_movies = []

    with open(dataset_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        required_columns = {'id', 'title', 'popularity', 'vote_count', 'budget'}
        # Column check
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(f"The required columns {required_columns} are not present in the dataset.")
        # Building the filtered_movies array
        for row in reader:
            try:
                budget = float(row['budget'])
                if budget > budget_limit:  # Budget check
                    filtered_movies.append({
                       # Data casting
                        'id': row['id'],  # Add the id
                        'title': row['title'],
                        'popularity': float(row['popularity']),
                        'budget':float(row['budget']),
                        'vote_count': int(row['vote_count'])
                    })
            except (ValueError, KeyError):
                continue

    return filtered_movies
 
def add_movie_genres_by_id(movies, genres_csv):
    """
    Adds genres to each movie in the existing movie array based on the movie ID.

    """
   # Create a dictionary to map movie IDs to their genres
    movie_genres_map = {}

    with open(genres_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Check for the presence of the required columns
        required_columns = {'id', 'genres'}
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(f"The required columns {required_columns} are not present in the dataset.")

         # Building the movie_genres_map dictionary
        for row in reader:
            movie_id = row['id']
            genre = row['genres']
            if movie_id in movie_genres_map:
                movie_genres_map[movie_id].append(genre)
            else:
                movie_genres_map[movie_id] = [genre]

    # Add genres to existing movies
    for movie in movies:
        movie_id = movie.get('id')  # Assuming there is an 'id' field in the movies
        movie['genres'] = movie_genres_map.get(movie_id, [])  # Add genres or an empty list

    return movies
movies = filter_movies_by_budget('movies_table.csv')

def calculate_genre_statistics(movies):
    """
    Calculates the average popularity and total votes for each genre.


    """

   # Dictionaries to sum popularity and count votes by genre
    genre_popularity = defaultdict(float) 
    genre_vote_count = defaultdict(int)
    genre_movie_count = defaultdict(int)  # Variable used for the average

   # Iterate over the movies using 2 for loops 
    for movie in movies:
        # Instantiate the various variables
        genres = movie.get('genres', [])
        popularity = movie.get('popularity', 0.0)
        vote_count = movie.get('vote_count', 0)

        for genre in genres:
            genre_popularity[genre] += popularity
            genre_vote_count[genre] += vote_count
            genre_movie_count[genre] += 1

   # Calculate the average popularity for each genre
    genre_statistics = []
    for genre in genre_popularity:
        avg_popularity = genre_popularity[genre] / genre_movie_count[genre]
        total_votes = genre_vote_count[genre]
        genre_statistics.append((genre, avg_popularity, total_votes))

    return genre_statistics
def save_to_pickle(data, pickle_file):
    """
    Saving a generic object to a pickle file.
    """
    try:
        with open(pickle_file, 'wb') as f:
            pickle.dump(data, f)
        print(f"Saving data at {pickle_file}")
    except Exception as e:
        print(f"Error: {e}")
def load_from_pickle(pickle_file):
    """
    Function to retrieve data from a pickle file.
    """
    try:
        with open(pickle_file, 'rb') as f:
            data = pickle.load(f)
        
        print("Pickle file content:")
        print("=" * 40)
        if isinstance(data, list):
            for i, item in enumerate(data, start=1):
                print(f"{i}. {item}")
        elif isinstance(data, dict):
            for key, value in data.items():
                print(f"{key}: {value}")
        else:
            print(data)
        print("=" * 40)

        return data
    except Exception as e:
        print(f"Error: {e}")

movies = filter_movies_by_budget('movies_table.csv')
movies_with_genres = add_movie_genres_by_id(movies, 'genres_table.csv')
output = calculate_genre_statistics(movies_with_genres)

save_to_pickle(output,'query2.pkl')
load_from_pickle('query2.pkl')


