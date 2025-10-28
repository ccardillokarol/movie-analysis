import csv
from datetime import datetime
from collections import defaultdict
import pickle


def movies_in_year_range(dataset_csv, start_year, end_year, output_array=False):

    filtered_movies = []

    with open(dataset_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        required_columns = {'id', 'title', 'revenue', 'release_date'}
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(f"Le colonne richieste {required_columns} non sono presenti nel dataset.")

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
                continue

    if output_array:
        return [[movie['id'], movie['title'], movie['revenue'], movie['release_date']] for movie in filtered_movies]
    else:
        return filtered_movies
def add_column_by_id(movies, source_csv, value_column,id_column="id"):


    id_to_value_map = {}

    with open(source_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        required_columns = {id_column, value_column}
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(f"Le colonne richieste {required_columns} non sono presenti nel dataset.")

        for row in reader:
            movie_id = row[id_column]
            value = row[value_column]
            if movie_id in id_to_value_map:
                id_to_value_map[movie_id].append(value)
            else:
                id_to_value_map[movie_id] = [value]

    for movie in movies:
        movie_id = movie.get('id') 
        movie[value_column] = id_to_value_map.get(movie_id, []) 

    return movies
def most_frequent_keywords(movies):


    keywords_count = {}

    for movie in movies:
        keywords_list = movie.get('keywords', [])

        if isinstance(keywords_list, list):
            for keyword in keywords_list:
                keyword = keyword.strip()
                if keyword:
                    keywords_count[keyword] = keywords_count.get(keyword, 0) + 1
        else:
            print(f"Attenzione: le parole chiave di {movie.get('title', 'film sconosciuto')} non sono una lista!")

    if not keywords_count:
        return []

    max_count = max(keywords_count.values())

    most_frequent = [(keyword, count) for keyword, count in keywords_count.items() if count == max_count]

    return most_frequent
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



