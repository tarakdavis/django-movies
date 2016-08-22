from django.contrib import admin
from movieratings.models import UserProfile

# Register your models here.
from .models import Rater, Rating, Movie

admin.site.register(Rater)

admin.site.register(Rating)

admin.site.register(Movie)

admin.site.register(UserProfile)
