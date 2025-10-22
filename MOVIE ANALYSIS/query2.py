
import csv
import pickle
from collections import defaultdict

#Write a Python script that calculates the average popularity and total vote count for movies with a budget over $20 million,
#grouped by genre. The resulting pickle file must contain a list of tuples, each containing the genre, average popularity,
# and total vote count.

"""

Traccia : Prendere i voti e la popolarita dei film con un budget sopra i 20 milioni raggrapputati per genere
    
Risultati : Nome film || Genere || Popolarita || Voti 

Procedimento :
1. Prendere i film in base al budget dal dataset movies_tables.csv (qua prendere la popolarita e vote_count)
2.Ricerca incrocita con la tabella Genres_table.csv
3.Prendo tutti i generi dall'array restituito, faccio la media della popularity e il totale dei voti
    Output desiderato
    ("Action", 12.5, 20345),  # genere, media popolarità, totale voti
    ("Drama", 8.7, 12340),





"""


def filter_movies_by_budget(dataset_csv, budget_limit=20_000_000):
    '''
    Filtra i film tramite budget
    '''

    #Lista che contiene tutti i film
    filtered_movies = []

    with open(dataset_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        required_columns = {'id', 'title', 'popularity', 'vote_count', 'budget'}
        #Controllo delle colonne
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(f"Le colonne richieste {required_columns} non sono presenti nel dataset.")
        #Costruzione dell'array filterd_movies
        for row in reader:
            try:
                budget = float(row['budget'])
                if budget > budget_limit:  #controllo del budget
                    filtered_movies.append({
                        #casting dei dati
                        'id': row['id'],  # Aggiungi l'id
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
    Aggiunge i generi a ciascun film nell'array di film esistente basandosi sull'ID del film.

    """
    # Crea un dizionario per mappare gli ID dei film ai loro generi
    movie_genres_map = {}

    with open(genres_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Controlla la presenza delle colonne necessarie
        required_columns = {'id', 'genres'}
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(f"Le colonne richieste {required_columns} non sono presenti nel dataset.")

         # Costruzione del dizionario movie_genres_map
        for row in reader:
            movie_id = row['id']
            genre = row['genres']
            if movie_id in movie_genres_map:
                movie_genres_map[movie_id].append(genre)
            else:
                movie_genres_map[movie_id] = [genre]

    # Aggiunge i generi ai film esistenti
    for movie in movies:
        movie_id = movie.get('id')  # Assumendo che ci sia un campo 'id' nei film
        movie['genres'] = movie_genres_map.get(movie_id, [])  # Aggiunge i generi o una lista vuota

    return movies
movies = filter_movies_by_budget('movies_table.csv')

def calculate_genre_statistics(movies):
    """
    Calcola la media della popolarità e il totale dei voti per ogni genere.


    """

    # Dizionari per sommare popolarità e contare i voti per genere
    genre_popularity = defaultdict(float) 
    genre_vote_count = defaultdict(int)
    genre_movie_count = defaultdict(int)  #variabile utilizzata per la media 

    # Itera sui film con 2 cicli for 
    for movie in movies:
        #instanzia le varie variabili
        genres = movie.get('genres', [])
        popularity = movie.get('popularity', 0.0)
        vote_count = movie.get('vote_count', 0)

        for genre in genres:
            genre_popularity[genre] += popularity
            genre_vote_count[genre] += vote_count
            genre_movie_count[genre] += 1

    # Calcola la media della popolarità per ogni genere
    genre_statistics = []
    for genre in genre_popularity:
        avg_popularity = genre_popularity[genre] / genre_movie_count[genre]
        total_votes = genre_vote_count[genre]
        genre_statistics.append((genre, avg_popularity, total_votes))

    return genre_statistics
def save_to_pickle(data, pickle_file):
    """
    Salvataggio di un oggetto generico in un file pickle.
    """
    try:
        with open(pickle_file, 'wb') as f:
            pickle.dump(data, f)
        print(f"Saving data at {pickle_file}")
    except Exception as e:
        print(f"Error: {e}")
def load_from_pickle(pickle_file):
    """
    Funzione per prendere i dati da un file pickle.
    """
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

