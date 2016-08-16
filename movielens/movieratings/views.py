from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count, Avg
from .models import Movie, Rating, Rater
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'movieratings/index.html'

    def index(self):
        return HttpResponse("Hello, world. You're at the movieratings index.")


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
    model=Rater
    template_name='movieratings/rater_detail.html'

    def get_object(self):
        return get_object_or_404(Rater, pk=self.kwargs.get("pk"))


class TopRated(generic.ListView):
    template_name='movieratings/toprated.html'
    context_object_name='toprated'

    def get_queryset(self):
        min_num=50
        movies=Movie.objects.annotate(num_ratings=Count('rating')).filter(num_ratings__gte=min_num)
        toprated=movies.annotate(avg_rating=Avg('rating__score')).order_by('-avg_rating')[:20]
        return toprated

# def toprated(request):
#     min_num = 50
#     movies = Movies.objects.annotate(num_ratings=Count('rating')).filter(num_ratings__gte=min_num)
#     toprated = movies.annotate(avg_rating=Avg('rating__score')).order_by('-avg_rating')[:20]
#     return render(request, 'toprated.html', {'toprated': toprated})
