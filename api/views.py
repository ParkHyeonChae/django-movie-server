"""api/views.py"""

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import MovieList


def api_json_view(request):
    start = 0
    last = 20
    page = 1
    sort_by = 'id'
    genre = ''

    # API Request : /api?limit={parameter}
    get_limit = request.GET.get('limit', '')

    # API Request : /api?page={parameter}
    get_page = request.GET.get('page', '')

    # API Request : /api?sort_by={parameter}
    get_sort_by = request.GET.get('sort_by', '')

    # API Request : /api?genre={parameter}
    get_genre = request.GET.get('genre', '')

    # API Request : /api?order_by={parameter}
    get_order_by = request.GET.get('order_by', '')

    if get_limit:
        if int(get_limit) >= 1 and int(get_limit) <= 50:
            last = int(get_limit)
        else:
            get_limit = 20
    else:
        get_limit = 20
        
    if get_page:
        if int(get_page) >= 1 and int(get_page) * last <= 500:
            start = (last * int(get_page)) - last
            last = last * int(get_page)
        else:
            get_page = 1
    else:
        get_page = 1

    if get_sort_by:
        if get_sort_by == 'title':
            sort_by = 'title'
        elif get_sort_by == 'year':
            sort_by = '-year'
        elif get_sort_by == 'rating':
            sort_by = '-rating'

    if get_genre:
        genre = get_genre

    if get_order_by:
        if get_order_by == 'asc':
            if sort_by[0] != '-':
                tmp_sort_by = []
                tmp_sort_by.append('-')
                tmp_sort_by.append(sort_by)
                sort_by = ''.join(tmp_sort_by)
            else:
                sort_by = sort_by[1:]


    movie_count = MovieList.objects.values().filter(genre__icontains=genre).order_by(sort_by).count()
    queryset = MovieList.objects.values().filter(genre__icontains=genre).order_by(sort_by)[start:last]
    data = list(queryset)

    json_data = {
        "status": "ok",
        "status_message": "Query was successful",
        "data": {
            "movie_count": movie_count,
            "limit": int(get_limit),
            "page_number": int(get_page),
        }
    }
    if data:
        json_data['data']['movies'] = data


    return JsonResponse(json_data, safe=False)
        
