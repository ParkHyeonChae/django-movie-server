"""api/urls.py"""

from django.urls import path
from . import views

app_name = 'api'


urlpatterns = [
    path('', views.all_list_view, name='all_list'),
]