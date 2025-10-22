# TMDB Movie Analysis — Group 310631

A data analysis project exploring insights from **The Movie Database (TMDB)**.  
This repository includes Python scripts and output files that perform three analytical queries on a dataset of 5,000 movies, focusing on **revenue, popularity, and keyword trends**.

---

## PROJECT OVERVIEW
The goal of this project is to apply core Python programming and data manipulation skills to real-world data.  
The dataset was analyzed using **only the Python Standard Library**, demonstrating proficiency in file handling, data structures, and serialization.

---

## QUERIES IMPLEMENT
### 1 Top Production Companies by Revenue
Identifies the **five production companies** with the highest total revenue for movies released in the last decade.

### 2 Genre-Based Popularity and Votes
Calculates the **average popularity** and **total vote count** for all movies with a budget exceeding $20 million, grouped by genre.

### 3 Most Common Movie Keywords (2000–2010)
Finds the **most frequent keyword(s)** appearing in movies released between 2000 and 2010.

---

## Project Structure
- query1.py   # Code for revenue analysis by production company
- query2.py   # Code for genre-based popularity and votes
- query3.py   # Code for keyword frequency analysis
- query1.pkl  # Output file for Query 1
- query2.pkl  # Output file for Query 2
- query3.pkl  # Output file for Query 3
## DATASET
Subset of 5,000 movies from **The Movie Database (TMDB)**, divided into the following CSV files:
- `movies_table.csv` — core movie details  
- `genres_table.csv` — movie genres  
- `keywords_table.csv` — descriptive keywords  
- `production_companies.csv` — companies involved  
- `production_countries_table.csv` — production locations  

---

## TECHNOLOGIES USED
- **Python 3.x**
- Modules: `csv`, `json`, `pickle`, and other built-in libraries  
*(No third-party libraries used)*

---

## KEY LEARNING OUTCOMES
Efficient data handling and filtering using Python built-ins,
Experience with CSV and JSON parsing,
Understanding of serialization via Pickle,
Modular and organized project structure for clarity and scalability
 
