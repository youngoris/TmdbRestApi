from django.db import models

# Create your models here.
from django.db import models

class IMDBEntry(models.Model):
    imdb_id = models.CharField(max_length=255, primary_key=True)

class Director(models.Model):
    director_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    birth_year = models.IntegerField(null=True, blank=True)
    death_year = models.IntegerField(null=True, blank=True)
    primary_profession = models.CharField(max_length=255)
    known_for_titles = models.ManyToManyField(IMDBEntry)

    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movies(models.Model):
    tmdb_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    imdb_id = models.ForeignKey(IMDBEntry, on_delete=models.CASCADE)
    directors = models.ManyToManyField(Director, related_name='movies')
    casts = models.ManyToManyField(Actor)
    genres = models.ManyToManyField(Genre)
    
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    release_date = models.CharField(max_length=50)
    runtime = models.IntegerField()
    adult = models.BooleanField()
    revenue = models.BigIntegerField()
    budget = models.BigIntegerField()
    overview = models.TextField()

    def __str__(self):
        return self.title
    


    