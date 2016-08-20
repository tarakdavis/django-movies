from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model

class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)

    def __str__(self):
        return "{}".format(self.title)


class Rater(models.Model):
    gender = models.CharField(max_length=2)
    age = models.IntegerField()
    occupation = models.IntegerField()
    user = models.OneToOneField(User, null=True)
    # zipcode = models.CharField(max_length=10)

    def __str__(self):
        return "{}: {}, {}, {}".format(self.id, self.gender, self.age, self.occupation)

    def movies_not_rated(self):
        return Movie.objects.exclude(id__in=self.rating_set.all())


class Rating(models.Model):
    score = models.IntegerField()
    # timestamp = models.DateTimeField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rater = models.ForeignKey(Rater, on_delete=models.CASCADE)

    def __str__(self):
        return ("Rater: {}, Movie: {}, Score: {}".format(self.rater_id, self.movie.title, self.score))
