from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
from django.db.models import Count, Avg
from .models import Movie, Rating, Rater
from django.views import View, generic
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required



class IndexView(View):
    template_name = 'movieratings/index.html'

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')


class AllMovies(generic.ListView):
    template_name = 'movieratings/all_movies.html'
    context_object_name = 'all_movies'

    def get_queryset(self):
        movies = Movie.objects.order_by('title')
        return movies


# def movie_detail(request, pk):
#     movie = get_object_or_404(Movie, pk=pk)
#     ratings = movie.rating_set.all()
#     avg_rating = ratings.aggregate(Avg('score'))['score__avg']
#     context = {'movie': movie, 'ratings': ratings,
#                'avg_rating': avg_rating}
#     return render(request, 'movieratings/movie_detail.html', context)

class MovieDetail(generic.DetailView):
    model = Movie
    template_name = 'movieratings/movie_detail.html'
    # context_object_name = 'movie'
    #
    def get_context_data(self, *args, **kwargs):
        ctx = super(MovieDetail, self).get_context_data(*args, **kwargs)
        ratings = self.get_object().rating_set.all()
        ctx['avg_rating'] = ratings.aggregate(Avg('score'))['score__avg']
        ctx['five'] = len(ratings.filter(score=5))
        ctx['four'] = len(ratings.filter(score=4))
        ctx['three'] = len(ratings.filter(score=3))
        ctx['two'] = len(ratings.filter(score=2))
        ctx['one'] = len(ratings.filter(score=1))
        return ctx

# class MovieGenreDetail(generic.DetailView):
#     model = Movie
#     template_name = 'movieratings/movie_detail.html'
#     context_object_name = 'movie'
#
    # def get_each_genre(self):
    #     genres = Movie.genre
    #     genres_list = genres.split('|')
    #     return genres_list


class RaterDetail(generic.DetailView):
    model = Movie
    template_name = 'movieratings/rater_detail.html'
    context_object_name = 'rater'

    def get_object(self):
        return get_object_or_404(Rater, pk=self.kwargs.get("pk"))


class TopRated(generic.ListView):
    template_name = 'movieratings/toprated.html'
    context_object_name = 'toprated'

    def get_queryset(self):
        min_num = 50
        movies = Movie.objects.annotate(num_ratings=Count('rating')).filter(num_ratings__gte=min_num)
        toprated = movies.annotate(avg_rating=Avg('rating__score')).order_by('-avg_rating')[:20]
        return toprated
