from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count, Avg
from .models import Movie, Rating, Rater
# Create your views here.
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'movieratings/index.html'

    def index(self):
        return HttpResponse("Hello, world. You're at the movieratings index.")

class MovieDetail(generic.DetailView):
    model = Movie
    template_name = 'movieratings/movie_detail.html'

    def get_queryset(self):
        return

class AllMovies(generic.ListView):
    template_name = 'movieratings/all_movies.html'

    def get_queryset(self):
        return Movie.objects.all()


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
