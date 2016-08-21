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
# import operator
from movieratings.forms import UserForm, UserProfileForm
from django.template import RequestContext


# class SearchListView(generic.ListView):
#     """
#     Display a Blog List page filtered by the search query.
#     """
#     # paginate_by = 10
#     template_name = 'movieratings/movie_detail.html'
#
#     def get_queryset(self):
#         result = super(SearchListView, self).get_queryset()
#
#         query = self.request.GET.get('q')
#         if query:
#             query_list = query.split()
#             result = result.filter(
#                 reduce(operator.and_,
#                        (Q(title__icontains=q) for q in query_list)) |
#                 reduce(operator.and_,
#                        (Q(content__icontains=q) for q in query_list))
#             )
#         return result


# working on pulling up actual movie and not a blank movie detail page
class SearchView(generic.ListView):
    model = Movie
    select_related = ['title']
    template_name = 'movieratings/movie_detail.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            self.model.objects.filter(title__icontains=query)
            return MovieDetail.ctx
        else:
            return HttpResponseRedirect(AllMovies)


class IndexView(View):
    template_name = 'movieratings/index.html'

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')


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
        rater = self.get_object()
        favorite_genres = rater.favorite_genres()
        movies = rater.movies_not_rated().annotate(num_ratings=Count('rating')).filter(num_ratings__gte=50)
        toprated = movies.annotate(avg_rating=Avg('rating__score')).order_by('-avg_rating')
        preferred_genre = toprated.filter(Q(genre__contains=favorite_genres[0])|Q(genre__contains=favorite_genres[1])|Q(genre__contains=favorite_genres[2]))
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


# class AuthView():
#     template_name = 'movieratings/registration_form.html'
#
#     def auth_user():
#         user = authenticate(username='john', password='secret')
#         if user is not None:
#             pass  # A backend authenticated the credentials
#         else:
#             pass  # No backend authenticated the credentials
#         return HttpResponse('')

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
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'movieratings/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

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
                return HttpResponseRedirect('/movieratings/')
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
        return render_to_response('movieratings/login.html', {}, context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/movieratings/')
