from django.db import models
from .models import Movie, Rating, Rater


def class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=50)


def class Rater(models.Model):
    gender = models.CharField(max_length=1)
    age = models.IntegerField()
    occupation = models.IntegerField()
    # zipcode = models.CharField(max_length=10)


def class Rating(models.Model)
    score = models.IntegerField()
    # timestamp = models.DateTimeField()
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rater_id = models.ForeignKey(Rater, on_delete=models.CASCADE)
