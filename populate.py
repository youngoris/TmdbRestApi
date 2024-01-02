import os
import sys
import django
import csv
import datetime
from django.utils import timezone
from tqdm import tqdm 

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TmdbRestApi.settings')
django.setup()

from tmdbData.models import Movies, Actor, Director, Genre, IMDBEntry

data_movies = os.path.join(os.path.dirname(__file__), 'csv/tmdb_9999_popular_movies_database.csv')
data_directors = os.path.join(os.path.dirname(__file__), 'csv/directors_to_imdb_id.csv')
data_genres = os.path.join(os.path.dirname(__file__), 'csv/genres_id.csv')
data_casts = os.path.join(os.path.dirname(__file__), 'csv/tmdb_id_to_casts.csv')
data_movie_genres = os.path.join(os.path.dirname(__file__), 'csv/tmdb_id_to_genres.csv')


# Initialize sets for tracking and lists for bulk_create
actors_set = set()
directors_set = set()
genres_set = set()
movies_list = []

start_time = timezone.now()

# Loading movies from CSV and creating Movies instances.
movies_list = []
with open(data_movies) as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    next(data, None)   # Skipping the header row.
    for row in tqdm(data, desc="Loading Movies", unit="movies"): 
        # Convert the date from 'YYYY/MM/DD' format to 'YYYY-MM-DD'
        try:
            release_date = datetime.datetime.strptime(row[6], '%Y/%m/%d').strftime('%Y-%m-%d')
        except ValueError:
            # If the date format is incorrect or empty, set it to None or a default date
            release_date = '1900-01-01'  # use a default date
        # Skipping rows without imdb_id and ensuring tmdb_id is an integer.
        if not row[2]:  # imdb_id is in the third column
            continue  
        imdb_id, _ = IMDBEntry.objects.get_or_create(imdb_id=row[2])
        # Skipping rows without tmdb_id and ensuring tmdb_id is an integer.
        try:
            tmdb_id = int(row[0])
        except ValueError:
            print(f"Invalid tmdb_id in row: {row}")
            continue
        # Creating and appending movie instances.
        movie = Movies(
            tmdb_id=tmdb_id, 
            title=row[1],
            vote_average=float(row[3]) if row[3] else 0.0,
            vote_count=int(row[4]) if row[4] else 0,
            imdb_id=imdb_id,
            release_date=release_date,  
            runtime=int(row[7]) if row[7] else 0,
            adult=row[8].lower() == 'true',
            revenue=int(row[9]) if row[9] else 0,
            budget=int(row[10]) if row[10] else 0,
            overview=row[14],
        )
        movies_list.append(movie)
# Bulk create for movies
Movies.objects.bulk_create(movies_list)

# Loading and creating actors from CSV.
# Before processing actor data, create a dictionary with the actor name as the key and the actor object as the value
actors_dict = {actor.name: actor for actor in Actor.objects.all()}

# Process actor data
new_actors = []
with open(data_casts) as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    next(data, None)
    for row in tqdm(data, desc="Processing Actors", unit="actors"):
        actor_names = row[1].split(',')[:3]
        for name in actor_names:
            name = name.strip()
            if name not in actors_dict:
                # If the actor is not in the dictionary, create a new actor object and add it to the list
                new_actor = Actor(name=name)
                new_actors.append(new_actor)
                actors_dict[name] = new_actor

# Use bulk_create to add new actors in bulk
Actor.objects.bulk_create(new_actors)

# Establish a connection between the film and the actors
with open(data_casts) as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    next(data, None)
    for row in tqdm(data, desc="Linking Movies and Actors", unit="links"):
        movie_id, actor_names_str = row
        try:
            movie = Movies.objects.get(tmdb_id=int(movie_id))
        except Movies.DoesNotExist:
            print(f"Movie with tmdb_id {movie_id} not found, skipping.")
            continue

        actor_names = actor_names_str.split(',')[:3]
        actors = [actors_dict[name.strip()] for name in actor_names if name.strip() in actors_dict]
        movie.casts.add(*actors)

# Load and create directors with IMDBEntry relationship
directors_list = []
imdb_entries_set = set()
# Loading and creating directors and their relationships with IMDBEntry.
with open(data_directors) as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    next(data, None)  # Skip header row
    for row in tqdm(data, desc="Processing Directors", unit="directors"): 
        # Handle special cases in death_year and birth_year
        birth_year = int(row[2]) if row[2] and row[2] != '\\N' else None
        death_year = int(row[3]) if row[3] and row[3] != '\\N' else None
        
        director_id = row[0]
        name = row[1]
        # Check if the director already exists
        if not Director.objects.filter(director_id=director_id).exists():
            director = Director(
                director_id=director_id,
                name=name,
                birth_year=birth_year,
                death_year=death_year,
                primary_profession=row[4]
            )
            directors_list.append(director)
            director.save() # Save the director to get the primary key
        # If the director exists, get the existing instance
        else:
            director = Director.objects.get(director_id=director_id)
        # Process IMDBEntry relationships
        known_titles = row[5].split(',')  # Assuming known titles/IMDB IDs are in the 6th column
        for title in known_titles:
            title = title.strip()
            if title:
                imdb_entry, created = IMDBEntry.objects.get_or_create(imdb_id=title)
                director.known_for_titles.add(imdb_entry)
                if created:
                    imdb_entries_set.add(imdb_entry)
# Bulk creation of new directors.
Director.objects.bulk_create(directors_list)

# Loading genres and creating Genre instances.
with open(data_genres) as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    next(data, None)  # Skip header row
    for row in tqdm(data, desc="Processing Genres", unit="genres"):  
        genre_id_str = row[0].strip()
        if genre_id_str:  # Skip empty genre_id
            genre_id = int(genre_id_str)  # Convert to integer
            name = row[1].strip()
            Genre.objects.get_or_create(genre_id=genre_id, name=name)

# Establishing relationships between movies and genres.
# Step 1: Create dictionaries for fast lookup
movies_dict = {movie.tmdb_id: movie for movie in Movies.objects.all()}
genres_dict = {genre.genre_id: genre for genre in Genre.objects.all()}

# Step 2: Process each movie-genre link
with open(data_movie_genres) as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    next(data, None)
    for row in tqdm(data, desc="Linking Movies and Genres", unit="links"):
        movie_id, genre_ids_str = row
        movie = movies_dict.get(int(movie_id))

        if movie:
            genre_ids = genre_ids_str.split(',')
            genres_to_add = []
            for genre_id in genre_ids:
                if genre_id.strip():  # Check if genre_id is not empty
                    genre = genres_dict.get(int(genre_id.strip()))
                    if genre:
                        genres_to_add.append(genre)

            # Add all genres to the movie in one go
            movie.genres.add(*genres_to_add)
                    
# Calculating and printing the time taken for the data loading process.
end_time = timezone.now()
print(f"Loading CSV took: {(end_time-start_time).total_seconds()} seconds.")