from django.conf.urls import url
from . import views

app_name = 'movieratings'
urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^toprated', views.TopRated.as_view(), name='toprated'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^allmovies', views.AllMovies.as_view(), name='all_movies'),
    url(r'^movie/(P<pk>[0-9]+)/$', views.MovieDetail.as_view(), name ='movie_detail'),
    url(r'^rater/(P<pk>[0-9]+)/$', views.RaterDetail.as_view(), name ='rater_detail'),
]
