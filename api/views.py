"""api/views.py"""

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import MovieList


def all_list_view(request):
    queryset = MovieList.objects.values().order_by('id')[:20]

    # /api?sort_by={parameter}
    sort_by = request.GET.get('sort_by', '')

    if sort_by:
        if sort_by == 'title':
            queryset = MovieList.objects.values().order_by('title')[:20]
        elif sort_by == 'year':
            queryset = MovieList.objects.values().order_by('-year')[:20]
        elif sort_by == 'rating':
            queryset = MovieList.objects.values().order_by('-rating')[:20]

       
    data = list(queryset)

    return JsonResponse(data, safe=False)