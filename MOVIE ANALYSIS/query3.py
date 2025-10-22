import csv
from datetime import datetime
from collections import defaultdict
import pickle
'''
    trovare la piu' comune keyword per i film rilasciati dal 2000 al 2010
    RISULTATO : keyword(piu' di due se c'e' una tie)

    PROCEDIMENTO
    1.Prendere movies_table.csv i film rilasciati dal 2000 al 2010
    2.Ricerca incrociata tramite id per associare il film alla keyword
    3.Classificazione delle keyword 
'''

def movies_in_year_range(dataset_csv, start_year, end_year, output_array=False):
    """
    Estrae i film da un dataset CSV in base a un range di anni specificato.
    Ritorna l'array con i film filtrati dall'anno
    """
    # Lista per salvare i film nel range di anni specificato
    filtered_movies = []

    # Legge il file CSV e filtra i film in base all'anno di uscita
    with open(dataset_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Controlla che il dataset contenga le colonne necessarie
        required_columns = {'id', 'title', 'revenue', 'release_date'}
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(f"Le colonne richieste {required_columns} non sono presenti nel dataset.")

        # Filtra i film in base all'intervallo di anni
        for row in reader:
            try:
                release_date = datetime.strptime(row['release_date'], '%Y-%m-%d')
                if start_year <= release_date.year <= end_year:
                    filtered_movies.append({
                        'id': row['id'],
                        'title': row['title'],
                        'revenue': float(row['revenue']) if row['revenue'] else 0.0,
                        'release_date': row['release_date']
                    })
            except (ValueError, KeyError):
                # Ignora righe con dati non validi
                continue

    # Restituisce un array con i seguenti campi
    #se nella funzione ci e' dato un parametro array, allora ritornera quello, se no ritorna l'array istanziato all'interno della funzione filtered movie
    if output_array:
        return [[movie['id'], movie['title'], movie['revenue'], movie['release_date']] for movie in filtered_movies]
    else:
        return filtered_movies
def add_column_by_id(movies, source_csv, value_column,id_column="id"):
    """
    Aggiunge una colonna arbitraria a ciascun film nell'array di film esistente basandosi sull'ID del film.
    id_column e' gia istanziata, ma possiamo usare questa funzione piu' genericamente cambiando il parametro id_column

    """
   
    id_to_value_map = {}

    with open(source_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Controlla la presenza delle colonne necessarie
        required_columns = {id_column, value_column}
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(f"Le colonne richieste {required_columns} non sono presenti nel dataset.")

        # Costruzione del dizionario id_to_value_map
        for row in reader:
            movie_id = row[id_column]
            value = row[value_column]
            if movie_id in id_to_value_map:
                id_to_value_map[movie_id].append(value)
            else:
                id_to_value_map[movie_id] = [value]

    # Aggiunge i valori ai film esistenti
    for movie in movies:
        movie_id = movie.get('id') 
        movie[value_column] = id_to_value_map.get(movie_id, []) 

    return movies
def most_frequent_keywords(movies):
    """
    Trova le parole chiave più frequenti nella lista dei film.


    """
    #dizionario
    keywords_count = {}

    for movie in movies:
        keywords_list = movie.get('keywords', [])  # Prende la lista delle parole chiave

        if isinstance(keywords_list, list):  # Verifica che sia una lista
            for keyword in keywords_list:
                keyword = keyword.strip()  # Rimuove gli spazi prima e dopo
                if keyword:  # Se la parola chiave non è vuota
                    keywords_count[keyword] = keywords_count.get(keyword, 0) + 1
        else:
            print(f"Attenzione: le parole chiave di {movie.get('title', 'film sconosciuto')} non sono una lista!")

    # Verifica se ci sono parole chiave nel dizionario
    if not keywords_count:
        return []  # Ritorna una lista vuota se non ci sono parole chiave

    #conteggio delle parole con ricorrenza massima
    max_count = max(keywords_count.values())

    # Trova tutte le parole chiave con il conteggio massimo
    most_frequent = [(keyword, count) for keyword, count in keywords_count.items() if count == max_count]

    # Se ci sono più parole chiave con lo stesso conteggio massimo, restituiamo una lista
    return most_frequent
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
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None

dataset_csv = 'movies_table.csv'
result = movies_in_year_range(dataset_csv, start_year=2000, end_year=2010, output_array=False)
result = add_column_by_id(result, "keywords_table.csv", value_column='keywords')

keywords = most_frequent_keywords(result)

save_to_pickle(keywords,'query3.pkl')
result =  load_from_pickle('query3.pkl')
print(result)



