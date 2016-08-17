from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
from django.db.models import Count, Avg
from .models import Movie, Rating, Rater
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
#from django.core.context_processors.csrf import csrf

# ====================== REGISTRATION ============================
# ====================== REGISTRATION ============================


class IndexView(generic.ListView):
    template_name = 'movieratings/index.html'

    def register(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/accounts/register/complete')

        else:
            form = UserCreationForm()
        token = {}
        token.update(csrf(request))
        token['form'] = form

        return render_to_response('registration/registration_form.html', token)


    def registration_complete(request):
        return render_to_response('registration/registration_complete.html')


    #                   ==== login ====
    def loggedin(request):
        return render_to_response('registration/loggedin.html',
                                  {'username': request.user.username})


class AllMovies(generic.ListView):
    template_name = 'movieratings/all_movies.html'

    def get_queryset(self):
        return Movie.objects.all()


class MovieDetail(generic.DetailView):
    model = Movie
    template_name = 'movieratings/movie_detail.html'

    def get_object(self):
        return get_object_or_404(Movie, pk=self.kwargs.get("pk"))


class RaterDetail(generic.DetailView):
    model = Rater
    template_name = 'movieratings/rater_detail.html'

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

# def toprated(request):
#     min_num = 50
#     movies = Movies.objects.annotate(num_ratings=Count('rating')).filter(num_ratings__gte=min_num)
#     toprated = movies.annotate(avg_rating=Avg('rating__score')).order_by('-avg_rating')[:20]
#     return render(request, 'toprated.html', {'toprated': toprated})
