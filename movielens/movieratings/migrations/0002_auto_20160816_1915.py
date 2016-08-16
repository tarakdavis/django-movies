# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-16 23:15
from __future__ import unicode_literals
from django.db import migrations
import csv


def load_data(apps, schema_editor):
    Movie = apps.get_model('movieratings', 'Movie')
    Rater = apps.get_model('movieratings', 'Rater')
    Rating = apps.get_model('movieratings', 'Rating')

    all_movies = {}
    all_raters = {}

    with open('../ml-1m/movies.dat', encoding='latin_1') as movies:
        reader = csv.reader(movies, delimiter='+')
        for row in reader:
            temp = Movie(id=int(row[0]), title=row[1], genre=row[2])
            all_movies[temp.id] = temp
            temp.save()

    with open('../ml-1m/users.dat') as raters:
        reader = csv.reader(raters, delimiter='+')
        for row in reader:
            temp = Rater(
                id=int(row[0]),
                gender=row[1],
                age=int(row[2]),
                occupation=int(row[3]))
            all_raters[temp.id] = temp
            temp.save()

    with open('../ml-1m/ratings.dat') as ratings:
        reader = csv.reader(ratings, delimiter='+')
        for row in reader:
            temp = Rating(
                rater=Rater.objects.get(id=int(row[0])),
                movie=Movie.objects.get(id=int(row[1])),
                score=int(row[2]))
            temp.save()


class Migration(migrations.Migration):

    dependencies = [
        ('movieratings', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data)
    ]
