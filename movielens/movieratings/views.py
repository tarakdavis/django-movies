from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count, Avg
from .models import Movie, Rating, Rater
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the movieratings index.")

def toprated(request):
    min_num = 50
    movies = Movies.objects.annotate(num_ratings=Count('rating')).filter(num_ratings__gte=min_num)
    toprated = movies.annotate(avg_rating=Avg('rating__score')).order_by('-avg_rating')
    return render(request, 'toprated.html', {'toprated': toprated})
