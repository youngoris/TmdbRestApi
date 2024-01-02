# REST API Specification and Examples

## API Endpoints Overview

This document provides REST API specifications and examples for the TmdbRestApi project.

## Deployment Information

This project has been deployed on the Oracle Cloud server. Here are the details for accessing and testing the API:

**Server Address**: http://192.9.228.196:8000

### Access Credentials

- **Username**: cm3035
- **Password**: uol

Please use these credentials to access and test the various API endpoints. Tools such as Postman or curl can be used for making API requests.

POST http://192.9.228.196:8000//movies/create - add a new record
GET  http://192.9.228.196:8000//movies/<imdb_id>or<tmdb_id> - return

### Endpoints

- `/movie/<id>/`
- `/movies/actor/<actor_name>/`
- `/movies/genre/<genre_name>/`
- `/movies/director/<director_name>/`
- `/movies/top-rated/<top_n>/`
- `/movies/best-roi/<top_n>/`

## Detailed API Endpoints

### 1. Get Movie Detail

**Request:**
- Method: GET
- URL: `/movie/<id>/`
- URL Params: 
  - `id` : The TMDB ID or IMDB ID of the movie.

**Response:**
- A single movie object with details.

**Example:**
- Request: `GET /movie/2667/`
- Response:
  ```json
 {
    "index": null,
    "title": "The Blair Witch Project",
    "release_date": "1999-07-14",
    "vote_average": 6.336,
    "vote_count": 4359,
    "genres": [
        "Horror",
        "Mystery"
    ],
    "overview": "In October of 1994 three student filmmakers disappeared in the woods near Burkittsville, Maryland, while shooting a documentary. A year later their footage was found.",
    "casts": [
        "Rei Hance",
        "Michael C. Williams",
        "Joshua Leonard"
    ],
    "directors": [],
    "runtime": 81,
    "adult": false,
    "revenue": 248639099,
    "budget": 60000,
    "imdb_id": "tt0185937"
}
```

### 2. Get Movies by Actor

**Request:**
- Method: GET
- URL: `/movies/actor/<actor_name>/`
- URL Params: 
  - `actor_name` : Name of the actor (replace spaces with underscores).

**Response:**
- A list of movies featuring the specified actor.

**Example:**
- Request: `GET /movies/actor/emma_stone/`
- Response:
  ```json
  [
      {
          "index": 1,
          "title": "La La Land",
          "release_date": "2016-12-09",
          "vote_average": 7.9,
          "vote_count": 12566,
          "genres": ["Comedy", "Drama", "Music"],
          "overview": "Mia, an aspiring actress, and Sebastian, a dedicated jazz musician, are struggling to make ends meet in a city known for crushing hopes and breaking hearts.",
          "casts": ["Emma Stone", "Ryan Gosling", "John Legend"],
          "directors": ["Damien Chazelle"],
          "runtime": 128,
          "adult": false,
          "revenue": 446486225,
          "budget": 30000000,
          "imdb_id": "tt3783958"
      },
      ...
  ]
  ```

### 3. Get Movies by Genre

**Request:**
- Method: GET
- URL: `/movies/genre/<genre_name>/`
- URL Params: 
  - `genre_name` : Name of the genre (replace spaces with underscores).

**Response:**
- A list of movies of the specified genre.

**Example:**
- Request: `GET /movies/genre/action/`
- Response:
  ```json
  [
      {
          "index": 1,
          "title": "Avengers: Endgame",
          "release_date": "2019-04-26",
          "vote_average": 8.3,
          "vote_count": 18333,
          "genres": ["Action", "Adventure", "Science Fiction"],
          "overview": "After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe.",
          "casts": ["Robert Downey Jr.", "Chris Evans", "Mark Ruffalo"],
          "directors": ["Anthony Russo", "Joe Russo"],
          "runtime": 181,
          "adult": false,
          "revenue": 2797800564,
          "budget": 356000000,
          "imdb_id": "tt4154796"
      },
      ...
  ]
  ```

### 4. Get Top Rated Movies

**Request:**
- Method: GET
- URL: `/movies/top-rated/<top_n>/`
- URL Params: 
  - `top_n` : Number of top-rated movies to retrieve.

**Response:**
- A list of top `n` rated movies sorted by vote average.

**Example:**
- Request: `GET /movies/top-rated/5/`
- Response:
  ```json
  [
      {
          "index": 1,
          "title": "The Shawshank Redemption",
          "release_date": "1994-09-23",
          "vote_average": 8.7,
          "vote_count": 21607,
          "genres": ["Drama", "Crime"],
          "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
          "casts": ["Tim Robbins", "Morgan Freeman"],
          "directors": ["Frank Darabont"],
          "runtime": 142,
          "adult": false,
          "revenue": 28341469,
          "budget": 25000000,
          "imdb_id": "tt0111161"
      },
      ...
  ]
  ```

### 5. Get Movies by Best ROI

**Request:**
- Method: GET
- URL: `/movies/best-roi/<top_n>/`
- URL Params: 
  - `top_n` : Number of movies to retrieve based on best Return on Investment.

**Response:**
- A list of top `n` movies sorted by ROI.

**Example:**
- Request: `GET /movies/best-roi/5/`
- Response:
  ```json
  [
      {
          "index": 1,
          "title": "Paranormal Activity",
          "release_date": "2007-09-14",
          "vote_average": 6.3,
          "vote_count": 3577,
          "genres": ["Horror", "Thriller"],
          "overview": "After moving into a suburban home,

 a couple becomes increasingly disturbed by a nightly demonic presence.",
          "casts": ["Katie Featherston", "Micah Sloat"],
          "directors": ["Oren Peli"],
          "runtime": 86,
          "adult": false,
          "revenue": 193355800,
          "budget": 15000,
          "imdb_id": "tt1179904"
      },
      ...
  ]
  ```

This specification and examples provide a clear and comprehensive guide to the available endpoints in the TmdbRestApi project, detailing their functionality and structure for easy understanding and usage.