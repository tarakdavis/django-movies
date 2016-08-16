from django.conf.urls import url, include
from django.contrib.auth.views import login, logout
from . import views

app_name = 'movieratings'
urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^toprated', views.TopRated.as_view(), name='toprated'),
<<<<<<< HEAD
    # url(r'^$', views.IndexView.as_view(), name='index'),
=======
    url(r'^$', views.IndexView, name='index'),
>>>>>>> 4ff4606ea7d2cc5869f3dd2779770101a9a9f12b
    url(r'^allmovies', views.AllMovies.as_view(), name='all_movies'),
    url(r'^movie/(P<pk>[0-9]+)/$', views.MovieDetail.as_view(), name ='movie_detail'),
    url(r'^rater/(P<pk>[0-9]+)/$', views.RaterDetail.as_view(), name ='rater_detail'),]
#========== REGISTRATION ================
<<<<<<< HEAD
     # Registration URLs
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/register/complete/$', views.registration_complete, name='registration_complete'),
            # Auth-related URLs:
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^accounts/loggedin/$', views.loggedin, name='loggedin'),
]
=======
 #     # Registration URLs
 #    url(r'^accounts/register/$', movieratings.views.register, name='register'),
 #    url(r'^accounts/register/complete/$', movieratings.views.registration_complete,name='registration_complete'),
 #            # Auth-related URLs:
 #     url(r'^accounts/login/$', django.contrib.auth.views.login, name='login'),
 #     url(r'^accounts/logout/$', django.contrib.auth.views.logout, name='logout'),
 #     url(r'^accounts/loggedin/$', movieratings.views.loggedin, name='loggedin'),
 # ]
>>>>>>> 4ff4606ea7d2cc5869f3dd2779770101a9a9f12b
#============== REGISTRATION ================
