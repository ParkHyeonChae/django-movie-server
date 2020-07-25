"""api/admin.py"""

from django.contrib import admin
from .models import MovieList
from django.contrib.auth.models import Group


class MovieListAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'year',
        'rating',
        'genres',
        'summary',
        
    )
    search_fields = (
        'title',
        'year',
        'rating',
        'genres',
    )


admin.site.register(MovieList, MovieListAdmin)
admin.site.unregister(Group)