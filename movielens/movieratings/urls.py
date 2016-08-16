from django.conf.urls import url
from . import views

app_name = 'movieratings'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^toprated', views.toprated, name='toprated'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^(P<pk>[0-9]+)/$', views.DetailView.as_view(), name ='movie_detail'),
    #url(r'^(P<pk>[0-9]+)/$', views.DetailView.as_view(), name ='rater_detail')
]
