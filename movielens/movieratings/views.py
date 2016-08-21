from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
from django.db.models import Count, Avg
from .models import Movie, Rating, Rater
from django.contrib.auth import authenticate, login
from django.views import View, generic
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# from django.db.models import Q


# working on pulling up actual movie and not a blank movie detail page
class SearchView(generic.ListView):
    model = Movie
    select_related = ['title']
    template_name = 'movieratings/search.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            searched_movies = self.model.objects.filter(title__icontains=query)
            return searched_movies


class IndexView(View):
    template_name = 'movieratings/index.html'

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')


class AuthView():
    template_name = 'movieratings/WIP.html'

    def auth_user():
        user = authenticate(username='john', password='secret')
        if user is not None:
            pass  # A backend authenticated the credentials
        else:
            pass  # No backend authenticated the credentials
        return HttpResponse('')


    # def register(request):
    #     if request.method == 'POST':
    #         form = UserCreationForm(request.POST)
    #         if form.is_valid():
    #             form.save()
    #             return HttpResponseRedirect('/accounts/register/complete')
    #
    #     else:
    #         form = UserCreationForm()
    #     token = {}
    #     token.update(csrf(request))
    #     token['form'] = form
    #
    #     return render_to_response('registration/registration_form.html', token)
    #
    #
    # def registration_complete(request):
    #     return render_to_response('registration/registration_complete.html')
    #
    #
    # #                   ==== login ====
    # def loggedin(request):
    #     return render_to_response('registration/loggedin.html',
    #                               {'username': request.user.username})


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

    def get_context_data(self, *args, **kwargs):
        ctx = super(MovieDetail, self).get_context_data(*args, **kwargs)
        ratings = self.get_object().rating_set.all()
        ctx['avg_rating'] = ratings.aggregate(Avg('score'))['score__avg']
        ctx['five'] = len(ratings.filter(score=5))
        ctx['four'] = len(ratings.filter(score=4))
        ctx['three'] = len(ratings.filter(score=3))
        ctx['two'] = len(ratings.filter(score=2))
        ctx['one'] = len(ratings.filter(score=1))
        ctx['r_five'] = ratings.filter(score=5)
        ctx['r_four'] = ratings.filter(score=4)
        ctx['r_three'] = ratings.filter(score=3)
        ctx['r_two'] = ratings.filter(score=2)
        ctx['r_one'] = ratings.filter(score=1)
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
    model = Rater
    template_name = 'movieratings/rater_detail.html'
    context_object_name = 'rater'

    def get_context_data(self, *args, **kwargs):
        ctx = super(RaterDetail, self).get_context_data(*args, **kwargs)
        rater = self.object
        favorite_genres = rater.favorite_genres()
        print(favorite_genres)
        movies = rater.movies_not_rated().annotate(num_rat=Count('rating')).filter(num_rat__gte=50)
        toprated = movies.annotate(avg_rating=Avg('rating__score')).order_by('-avg_rating')
        preferred_genre = toprated.filter(genre__contains=favorite_genres[0])

        #|Q(genre__contains=favorite_genres[1])|Q(genre__contains=favorite_genres[2]))

        occupation = rater.occupation_word()
        ctx['occupation'] = occupation
        ctx['toprated'] = toprated[:5]
        ctx['picks'] = preferred_genre[:5]
        ctx['age_bracket'] = rater.age_bracket()
        return ctx


class TopRated(generic.ListView):
    template_name = 'movieratings/toprated.html'
    context_object_name = 'toprated'

    def get_queryset(self):
        min_num = 50
        movies = Movie.objects.annotate(num_ratings=Count('rating')).filter(num_ratings__gte=min_num)
        toprated = movies.annotate(avg_rating=Avg('rating__score')).order_by('-avg_rating')[:20]
        return toprated
