
import csv
import pickle
from collections import defaultdict

#Write a Python script that calculates the average popularity and total vote count for movies with a budget over $20 million,
#grouped by genre. The resulting pickle file must contain a list of tuples, each containing the genre, average popularity,
# and total vote count.

"""-

1.	Select the movies from the dataset movies_table.csv based on their budget
(here, take the popularity and vote_count columns).
	2.	Perform a cross-search (join) with the table Genres_table.csv.
	3.	From the resulting array, take all the genres, then calculate:
	•	the average popularity, and
	•	the total number of votes.
    ("Action", 12.5, 20345)   # genre, average popularity, total votes  
    ("Drama", 8.7, 12340)





"""


def filter_movies_by_budget(dataset_csv, budget_limit=20_000_000):


    filtered_movies = []

    with open(dataset_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        required_columns = {'id', 'title', 'popularity', 'vote_count', 'budget'}
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(f"Le colonne richieste {required_columns} non sono presenti nel dataset.")
        for row in reader:
            try:
                budget = float(row['budget'])
                if budget > budget_limit:
                    filtered_movies.append({

                        'id': row['id'],
                        'title': row['title'],
                        'popularity': float(row['popularity']),
                        'budget':float(row['budget']),
                        'vote_count': int(row['vote_count'])
                    })
            except (ValueError, KeyError):
                continue

    return filtered_movies
 
def add_movie_genres_by_id(movies, genres_csv):

    movie_genres_map = {}

    with open(genres_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        required_columns = {'id', 'genres'}
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(f"Le colonne richieste {required_columns} non sono presenti nel dataset.")

        for row in reader:
            movie_id = row['id']
            genre = row['genres']
            if movie_id in movie_genres_map:
                movie_genres_map[movie_id].append(genre)
            else:
                movie_genres_map[movie_id] = [genre]

    for movie in movies:
        movie_id = movie.get('id')
        movie['genres'] = movie_genres_map.get(movie_id, [])

    return movies
movies = filter_movies_by_budget('movies_table.csv')

def calculate_genre_statistics(movies):


    genre_popularity = defaultdict(float)
    genre_vote_count = defaultdict(int)
    genre_movie_count = defaultdict(int)


    for movie in movies:
        genres = movie.get('genres', [])
        popularity = movie.get('popularity', 0.0)
        vote_count = movie.get('vote_count', 0)

        for genre in genres:
            genre_popularity[genre] += popularity
            genre_vote_count[genre] += vote_count
            genre_movie_count[genre] += 1

    genre_statistics = []
    for genre in genre_popularity:
        avg_popularity = genre_popularity[genre] / genre_movie_count[genre]
        total_votes = genre_vote_count[genre]
        genre_statistics.append((genre, avg_popularity, total_votes))

    return genre_statistics
def save_to_pickle(data, pickle_file):

    try:
        with open(pickle_file, 'wb') as f:
            pickle.dump(data, f)
        print(f"Saving data at {pickle_file}")
    except Exception as e:
        print(f"Error: {e}")
def load_from_pickle(pickle_file):
    
    try:
        with open(pickle_file, 'rb') as f:
            data = pickle.load(f)
        
        print("Contenuto del file pickle:")
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

