from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
from django.db.models import Count, Avg
from .models import Movie, Rating, Rater
from django.contrib.auth import authenticate, login, logout
from django.views import View, generic
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from movieratings.forms import UserForm
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt


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


class DefineGenre(generic.ListView):
    template_name = 'base.html'
    model = Movie
    select_related = ['genre']
    context_object_name = 'genres'

    def get_queryset(self):
        genres = Movie.objects.filter('genre')
        return genres



class GenreView(generic.ListView):
    model = Movie
    select_related = ['genre']
    template_name = 'genres.html'
    context_object_name = 'genre_results'
    # q = {
    #     'act': "Action",
    #     'adve': 'Adventure',
    #     'ani': 'Animation',
    #     'chil': "Children",
    #     'com': 'Comedy',
    #     'doc': "Documentary",
    #     'drama': 'Drama',
    #     'fant': "Fantasy",
    #     'noir': "Film-Noir",
    #     'horror': "Horror",
    #     'mus': "Musical",
    #     'mys': "Mystery",
    #     'rom': "Romance",
    #     'sci': "Sci-Fi",
    #     'thr': "Thriller",
    #     'war': "War",
    #     'west': "Western"}

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            searched_genre = self.model.objects.filter(genre__icontains=query)
            return searched_genre


# class IndexView(generic.ListView):
#     template_name = 'movieratings/index.html'
#
#     def get(self, request, *args, **kwargs):
#         return HttpResponse(request)


class AllMovies(generic.ListView):
    template_name = 'movieratings/all_movies.html'
    context_object_name = 'all_movies'

    def get_queryset(self):
        params = self.request.GET
        if "sort" in params:
            print(params['sort'])
            print('LEN OF PARAMS', len(params))
            movies = Movie.objects.all()
            for sort_thing in params.values():
                print(sort_thing)
                movies.order_by(sort_thing)


        # movies = Movie.objects.order_by('title')
        return movies


class MovieDetail(generic.DetailView):
    model = Movie
    template_name = 'movieratings/movie_detail.html'
    # context_object_name = 'movie'

    def get_context_data(self, *args, **kwargs):
        ctx = super(MovieDetail, self).get_context_data(*args, **kwargs)
        ratings = self.get_object().rating_set.all()
        ctx['avg_rating'] = ratings.aggregate(Avg('score'))['score__avg']
        one = ratings.filter(score=1)
        two = ratings.filter(score=2)
        three = ratings.filter(score=3)
        four = ratings.filter(score=4)
        five = ratings.filter(score=5)
        ctx['five'] = len(five)
        ctx['four'] = len(four)
        ctx['three'] = len(three)
        ctx['two'] = len(two)
        ctx['one'] = len(one)
        ctx['r_five'] = five
        ctx['r_four'] = four
        ctx['r_three'] = three
        ctx['r_two'] = two
        ctx['r_one'] = one
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
        occupation = rater.occupation_word()
        ctx['occupation'] = occupation
        ctx['toprated'] = toprated[:5]
        ctx['picks'] = preferred_genre[:5]
        ctx['age_bracket'] = rater.age_bracket()
        return ctx


class NewRating(generic.ListView):
    template_name = 'movieratings/new_rating.html'
    context_object_name = 'new_rating'
    model = Rating

    # def get(self, request, *args, **kwargs):
    #     ctx = Rating.objects.all()
    #     return ctx


class TopRated(generic.ListView):
    template_name = 'movieratings/toprated.html'
    context_object_name = 'toprated'

    def get_queryset(self):
        min_num = 50
        movies = Movie.objects.annotate(num_ratings=Count('rating')).filter(num_ratings__gte=min_num)
        toprated = movies.annotate(avg_rating=Avg('rating__score')).order_by('-avg_rating')[:20]
        return toprated


# @csrf_exempt
def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():  # and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render(request,
            'movieratings/register.html',
            {'user_form': user_form, 'registered': registered},
            context)


# @ensure_csrf_cookie
# @csrf_exempt
def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/movieratings/toprated')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Movie account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        # return render('movieratings/login.html', {}, context)
        return render(request, 'movieratings/login.html')

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/movieratings/')

def index(request):
    return render_to_response('movieratings/index.html')
