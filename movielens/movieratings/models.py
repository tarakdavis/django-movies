from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=50)

    def __str__(self):
        return str(self.title, self.genre)


class Rater(models.Model):
    gender = models.CharField(max_length=1)
    age = models.IntegerField()
    occupation = models.IntegerField()
    # zipcode = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id, self.gender, self.age, self.occupation)

    def get_allratings_of_rater(name_id):
        all_rater_ratings = Rater.objects.all(id=name_id)
        return all_rater_ratings


class Rating(models.Model):
    score = models.IntegerField()
    # timestamp = models.DateTimeField()
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rater_id = models.ForeignKey(Rater, on_delete=models.CASCADE)

    def __str__(self):
        return ("{}.  {} - {}.  {} - {}.".format(self.score, self.movie_id, self.rater_id))

    def specific_movie_rating(name_id):
        all_movie_ratings = Rating.objects.filter(movie_id=name_id)
        return all_movie_ratings

    def get_movie_average_rating(which_one):
        the_movie = Rating.objects.filter(movie_id=which_one)
        agg_score = 0
        for each in the_movie:
            agg_score += each.score
        try:
            avg_rating = agg_score/len(the_movie)
        except:
            avg_rating = 0

        if len(the_movie) < 20:
            too_few = True
        return (avg_rating, too_few)
