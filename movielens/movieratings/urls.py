from django.conf.urls import url, include
from . import views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

app_name = 'movieratings'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^toprated', views.TopRated.as_view(), name='toprated'),
    # url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^genre/$', views.GenreView.as_view(), name='genre'),
    url(r'^allmovies/', views.AllMovies.as_view(), name='all_movies'),
    url(r'^movie/(?P<pk>[0-9]+)/$', views.MovieDetail.as_view(), name='movie_detail'),
    url(r'^rater/(?P<pk>[0-9]+)/$', views.RaterDetail.as_view(), name='rater_detail'),
    url(r'^newrating/', views.NewRating.as_view(), name='new_rating'),
    url(r'^register/$', views.register, name='register'), # these 3: conflicting with prior auths urls?
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    # url(r'^index/$', views.IndexView.as_view() name='index'),
    ]
