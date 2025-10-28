import csv
from datetime import datetime

import pickle

def last_decades_movie(dataset_csv, years=10):
    """
    Extracts the movies from the last decade (modifiable parameter) and returns an array
    """
    
    # Variables for calculating the decade
    current_year = datetime.now().year 
    cutoff_year = current_year - years

    # List to store the movies from the last 10 years.
    filtered_movies = []

    # Opening a CSV file in read mode.
    with open(dataset_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Takes the movies from the CSV file from the last 10 years using a for loop
        for row in reader:
            # Conditional conversion: only processes rows with a valid date
            release_date = row['release_date'].strip()  # Removes empty spaces
            if release_date:  # Checks that it is not an empty string
                release_date = datetime.strptime(release_date, '%Y-%m-%d')  # Year format: yyyy-mm-dd
                if release_date.year > cutoff_year:  # Year check
                    filtered_movies.append({
                        # Casting of the data
                        'id': row['id'],
                        'title': row['title'],
                        'revenue': float(row['revenue']),
                        'release_date': row['release_date']
                    })

    # Returns an array with the following fields.
    return filtered_movies  # Return the dictionaries directly

def add_production_companies(movies, production_companies_csv):
    """
    Adds the 'production_companies' column to the movie results based on the movie’s ID

    """

    # Contains all the IDs of the companies taken from a file.
    # This variable is a dictionary
    id_to_companies = {}

    # read file
    with open(production_companies_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Check the various fields
        required_columns = {'id', 'production_companies'}
        if not required_columns.issubset(reader.fieldnames):
            print(f"The requested columns. {required_columns} are not present in the dataset..")

        # Construction of the id_to_companies dictionary
        for row in reader:
            movie_id = row['id']  #movie_id = 19995
            company = row['production_companies']  # company = Ingenious Film Partners


            if movie_id in id_to_companies: 
                # If the movie ID already exists in id_to_companies, another production company is added.
                id_to_companies[movie_id].append(company)
            else:
                # If it doesn’t exist, another field is created
                id_to_companies[movie_id] = [company]   #285,Walt Disney Pictures
        '''
        Structure of id_to_companies
            '1': ['Universal Pictures', 'Amblin Entertainment'],
            '2': ['Pixar Animation Studios'],
            '3': ['Warner Bros.', 'DC Films']
        '''

    # A new field production_companies is added to the array passed as a parameter
    for movie in movies:
        movie['production_companies'] = id_to_companies.get(movie['id'], [])

    return movies

def top_5_companies_by_revenue(movies):
    """
    Calculates the top 5 production companies with the highest revenue
    """

    # Dictionary to sum the revenues for each company
    company_revenue = defaultdict(float)   #The empty dictionary that is instantiated is represented like this      "[],0.0"

    #  Iteration over the movies using two for-loops to get the revenue of each production company.
    for movie in movies:
        if isinstance(movie, dict):
            revenue = movie.get('revenue', 0)
            companies = movie.get('production_companies', [])
            if isinstance(companies, list):
                for company in companies:
                    company_revenue[company] += revenue

    # Sort the companies by revenue in descending order
    sorted_companies = sorted(company_revenue.items(), key=lambda x: x[1], reverse=True)
    # Takes only the top 5
    top_5_companies = sorted_companies[:5]

    return top_5_companies

def save_to_pickle(data, pickle_file):
    """
    Saving a generic object to a pickle file.
    """
    with open(pickle_file, 'wb') as f:
        pickle.dump(data, f)
    print(f"Saving data at {pickle_file}")

def load_from_pickle(pickle_file):
    """
    Function to get (or load) data from a pickle file.
    """
    with open(pickle_file, 'rb') as f:
        data = pickle.load(f)
    
    print("top 5 companies by revenue")
    print("=" * 40)
    
    # Check the type of an object without using isinstance
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

# Example functions for data management
movies_result = last_decades_movie('movies_table.csv')
enhanced_movies = add_production_companies(movies_result, 'production_companies_table.csv')
top_5 = top_5_companies_by_revenue(enhanced_movies)

# Saving and loading data
save_to_pickle(top_5, 'query1.pkl')
load_from_pickle('query1.pkl')
