from django.db import models
# from movieratings.models import Movie, Rater, Rating


class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)

    def __str__(self):
        return str(self.title, self.genre)


class Rater(models.Model):
    gender = models.CharField(max_length=2)
    age = models.IntegerField()
    occupation = models.IntegerField()
    # zipcode = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id, self.gender, self.age, self.occupation)

    def get_allratings_of_rater(name_id):
        all_rater_ratings = Rater.objects.all(id=name_id)
        return all_rater_ratings

    def get_average_rating_of_this_rater(name_id):
        all_of_his_ratings = Rater.get_allratings_of_rater.objects.filter(name_id)
        total = sum(all_of_his_ratings) / all_of_his_ratings.objects.all().count()
        return total


class Rating(models.Model):
    score = models.IntegerField()
    # timestamp = models.DateTimeField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rater = models.ForeignKey(Rater, on_delete=models.CASCADE)

    def __str__(self):
        return ("{}.  {} - {}.  {} - {}.".format(self.score, self.movie_id, self.rater_id))

    # def specific_movie_rating(name_id):
    #     all_movie_ratings = Rating.objects.filter(movie_id=name_id)
    #     return all_movie_ratings
    #
    # def get_movie_average_rating(which_one):
    #     too_few = False
    #     the_movie = Rating.objects.filter(movie_id=which_one)
    #     agg_score = 0
    #     for each in the_movie:
    #         agg_score += each.score
    #     try:
    #         avg_rating = agg_score/len(the_movie)
    #     except:
    #         avg_rating = 0
    #
    #     if len(the_movie) < 20:
    #         too_few = True
    #     return (avg_rating, too_few)
    #
    # def get_top_rated_movies(num):
    #         averages = []
    #         top = []
    #         top_movies = Movie.objects.all().count()
    #         for i in range(top_movies):
    #             avg, not_enough_reviews = Rating.get_movie_average_rating(i+1)
    #             if not_enough_reviews is False:
    #                 averages.append((avg, i+1))
    #             print("\n"*50)
    #             c = (i+1) / 1683
    #             print("Percentage complete:  ", c, "%")
    #         averages.sort(reverse=True)
    #         for i in range(num):
    #             top.append(averages[i])
    #         return top      # returns list of TUPLES !
