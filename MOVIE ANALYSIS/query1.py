import csv
from datetime import datetime

import pickle

def last_decades_movie(dataset_csv, years=10):
    """
    Estrae i film dell'ultima decade(parametro modificabile) e restituisce un array 
    """
    
    # variabili per il calcolo della decade
    current_year = datetime.now().year 
    cutoff_year = current_year - years

    # Lista per salvare i film negli ultimi 10 anni
    filtered_movies = []

    # Apertura di un file csv nella modalita lettura 
    with open(dataset_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Prende i film nel file csv degli ultimi 10 anni tramite un ciclo for
        for row in reader:
            # Conversione condizionale: passa solo righe con una data valida
            release_date = row['release_date'].strip()  # Rimuove spazi vuoti
            if release_date:  # Verifica che non sia una stringa vuota
                release_date = datetime.strptime(release_date, '%Y-%m-%d')  # formato dell'anno yyyy-mm-dd
                if release_date.year > cutoff_year:  # controllo dell'anno 
                    filtered_movies.append({
                        # Casting dei dati
                        'id': row['id'],
                        'title': row['title'],
                        'revenue': float(row['revenue']),
                        'release_date': row['release_date']
                    })

    # ritorna un array con i seguenti campi
    return filtered_movies  # Restituisci direttamente i dizionari

def add_production_companies(movies, production_companies_csv):
    """
    Aggiunge la colonna `production_companies` al risultato dei film basandosi sull'id del film.

    """

    # Contiene tutti gli id delle compagnie prese da un file 
    # E' un dizionario questa variabile
    id_to_companies = {}

    # Lettura file
    with open(production_companies_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Controllo dei vari campi 
        required_columns = {'id', 'production_companies'}
        if not required_columns.issubset(reader.fieldnames):
            print(f"Le colonne richieste {required_columns} non sono presenti nel dataset.")

        # Costruzione del dizionario id_to_companies
        for row in reader:
            movie_id = row['id']  #movie_id = 19995
            company = row['production_companies']  #company = Ingenious Film Partners


            if movie_id in id_to_companies: 
                # Se c'e' gia il movie id in id_to_companies, viene aggiunta un'altra production company 
                id_to_companies[movie_id].append(company)
            else:
                # Se non c'e' Viene creato un altro campo
                id_to_companies[movie_id] = [company]   #285,Walt Disney Pictures
        '''
        Struttura di id_to_companies
            '1': ['Universal Pictures', 'Amblin Entertainment'],
            '2': ['Pixar Animation Studios'],
            '3': ['Warner Bros.', 'DC Films']
        '''

    # Viene aggiunto all'array dato come parametro un altro campo production_companies
    for movie in movies:
        movie['production_companies'] = id_to_companies.get(movie['id'], [])

    return movies

def top_5_companies_by_revenue(movies):
    """
    Calcola le top 5 compagnie di produzione con il maggiore revenue
    """

    # Dizionario per sommare i revenue per ciascuna compagnia 
    company_revenue = defaultdict(float)   #Il dizionario istnaziato vuoto e' rappresentanto cosi        "[],0.0"

    # Iterazione dei film tramite due cicli for  per prendere la revenue di ogni compagnia di produzione 
    for movie in movies:
        if isinstance(movie, dict):
            revenue = movie.get('revenue', 0)
            companies = movie.get('production_companies', [])
            if isinstance(companies, list):
                for company in companies:
                    company_revenue[company] += revenue

    # Ordina le compagnie per revenue in ordine decrescente
    sorted_companies = sorted(company_revenue.items(), key=lambda x: x[1], reverse=True)
    # Prende solo la top5
    top_5_companies = sorted_companies[:5]

    return top_5_companies

def save_to_pickle(data, pickle_file):
    """
    Salvataggio di un oggetto generico in un file pickle.
    """
    with open(pickle_file, 'wb') as f:
        pickle.dump(data, f)
    print(f"Saving data at {pickle_file}")

def load_from_pickle(pickle_file):
    """
    Funzione per prendere i dati da un file pickle.
    """
    with open(pickle_file, 'rb') as f:
        data = pickle.load(f)
    
    print("top 5 companies by revenue")
    print("=" * 40)
    
    # Controllo del tipo di oggetto senza usare isinstance
    if type(data) == list:
        for i, item in enumerate(data, start=1):
            print(f"{i}. {item}")
    elif type(data) == dict:
        for key, value in data.items():
            print(f"{key}: {value}")
    else:
        print(data)
    print("=" * 40)

    return data

# Funzioni di esempio per la gestione dei dati
movies_result = last_decades_movie('movies_table.csv')
enhanced_movies = add_production_companies(movies_result, 'production_companies_table.csv')
top_5 = top_5_companies_by_revenue(enhanced_movies)

# Salvataggio e caricamento dei dati
save_to_pickle(top_5, 'query1.pkl')
load_from_pickle('query1.pkl')