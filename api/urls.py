"""api/urls.py"""

from django.urls import path
from . import views

app_name = 'api'


urlpatterns = [
    # path('', views.api_json_view, name='api_json_view'),
    path('', views.MovieListApi.as_view(), name='movie_list_api'),
]