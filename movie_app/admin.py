from django.contrib import admin
from movie_app.models import Director, Movie, Review
from movie_app.models import Category, SearchWord

# Register your models here.

admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(SearchWord)



