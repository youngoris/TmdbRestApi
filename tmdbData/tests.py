from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Movies, Actor, Director, Genre, IMDBEntry

class MoviesModelTest(TestCase):
    """ Test module for Movies model """

    def setUp(self):
        # Create instances of your models here
        self.imdb_entry = IMDBEntry.objects.create(imdb_id="tt1234567")
        self.movie = Movies.objects.create(
            tmdb_id=424,
            title="Schindler's List",
            imdb_id=self.imdb_entry,
            vote_average=8.573,
            vote_count=14594,
            release_date="1993-12-15",
            runtime=195,
            adult=False,
            revenue=321365567,
            budget=22000000,
            overview="The true story of how businessman Oskar Schindler saved over a thousand Jewish lives from the Nazis while they worked as slaves in his factory during World War II."
        )

    def test_movie_creation(self):
        """ Test the movie model creation """
        self.assertEqual(self.movie.title, "Schindler's List")
        self.assertEqual(self.movie.imdb_id.imdb_id, "tt1234567")

class MoviePostTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.imdb_entry = IMDBEntry.objects.create(imdb_id="tt0000001")

        # 创建测试用的 Genre, Actor, 和 Director 实例
        self.genre_action = Genre.objects.create(name="Action")
        self.genre_adventure = Genre.objects.create(name="Adventure")
        self.genre_comedy = Genre.objects.create(name="Comedy")
        self.actor_emma = Actor.objects.create(name="Emma Stone")
        self.actor_tom = Actor.objects.create(name="Tom Hanks")
        self.actor_will = Actor.objects.create(name="Will Smith")
        self.director_spielberg = Director.objects.create(name="Steven Spielberg")

        # 更新 movie_data 以使用这些实例
        self.movie_data = {
            "tmdb_id": 8888,
            "title": "A New Movie",
            "release_date": "2024-01-01",
            "vote_average": 10.0,
            "vote_count": 10000,
            "overview": "A brief overview of the movie.",
            "runtime": 180,
            "adult": False,
            "revenue": 100000000,
            "budget": 2000000,
            "imdb_id": "tt0000001",
            "genres": ["Action", "Adventure", "Comedy"],
            "casts": ["Emma Stone", "Tom Hanks", "Will Smith"],
            "directors": ["Steven Spielberg"]
        }

    def test_create_movie(self):
        response = self.client.post(reverse('create-movie'), self.movie_data, format='json')
        print("Status Code:", response.status_code)
        print("Response Data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




class MoviesApiTestCase(TestCase):
    """ Test suite for the api views """

    def setUp(self):
        self.client = APIClient()
        self.imdb_entry = IMDBEntry.objects.create(imdb_id="tt6751668")
        self.movie = Movies.objects.create(
            tmdb_id=496243,
            title='Parasite',
            imdb_id=self.imdb_entry, 
            vote_average=8.515,
            vote_count=16430,
            release_date='2019-05-30',
            runtime=133,
            adult=False,
            revenue=257591776,
            budget=11363000,
            overview="All unemployed, Ki-taek's family takes peculiar interest in the wealthy and glamorous Parks for their livelihood until they get entangled in an unexpected incident."
        )

    def test_get_movie_detail(self):
        """ Test retrieving details of a specific movie. """
        response = self.client.get(reverse('movie-detail', kwargs={'id': self.movie.tmdb_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.movie.title)

    def test_get_movies_by_actor(self):
        """ Test retrieving movies by a specific actor. """
        actor = Actor.objects.create(name='Martin Balsam')
        self.movie.casts.add(actor)
        response = self.client.get(reverse('movies-by-actor', kwargs={'actor_name': 'Martin_Balsam'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(item['title'] == self.movie.title for item in response.data))

    def test_get_movies_by_genre(self):
        """ Test retrieving movies by a specific genre. """
        genre = Genre.objects.create(name='Comedy', genre_id=123)
        self.movie.genres.add(genre)
        response = self.client.get(reverse('movies-by-genre', kwargs={'genre_name': 'Comedy'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if response.data contains 'results' key
        if 'results' in response.data:
            movie_list = response.data['results']
        else:
            movie_list = response.data

        self.assertTrue(any(item['title'] == self.movie.title for item in movie_list))


    def test_get_top_rated_movies(self):
        """ Test retrieving top-rated movies. """
        response = self.client.get(reverse('top-rated-movies', kwargs={'top_n': 10}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) <= 10)

    def test_get_best_roi_movies(self):
        """ Test retrieving movies with the best ROI. """
        response = self.client.get(reverse('best-roi-movies', kwargs={'top_n': 5}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) <= 5)
