"""api/views.py"""

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import MovieList


# def api_json_view(request):
#     queryset = MovieList.objects.values().order_by('id')[:20]

#     # API Request : /api?limit={parameter}
#     limit = int(request.GET.get('limit', ''))

#     # API Request : /api?page={parameter}
#     page = int(request.GET.get('page', ''))

#     # API Request : /api?sort_by={parameter}
#     sort_by = request.GET.get('sort_by', '')

#     if limit >= 1 and limit <= 50:
#         if sort_by:
#             if sort_by == 'title':
#                 queryset = MovieList.objects.values().order_by('title')[:limit]
#             elif sort_by == 'year':
#                 queryset = MovieList.objects.values().order_by('-year')[:limit]
#             elif sort_by == 'rating':
#                 queryset = MovieList.objects.values().order_by('-rating')[:limit]

       
#     data = list(queryset)

#     return JsonResponse(data, safe=False)


def api_json_view(request):
    start = 0
    last = 20
    page = 1
    sort_by = 'id'


    # API Request : /api?limit={parameter}
    get_limit = request.GET.get('limit', '')

    # API Request : /api?page={parameter}
    get_page = request.GET.get('page', '')

    # API Request : /api?sort_by={parameter}
    get_sort_by = request.GET.get('sort_by', '')

    # API Request : /api?order_by={parameter}
    get_order_by = request.GET.get('order_by', '')


    if get_limit:
        if int(get_limit) >= 1 and int(get_limit) <= 50:
            last = int(get_limit)

    if get_page:
        if int(get_page) >= 1 and int(get_page) * last <= 500:
            start = (last * int(get_page)) - last
            last = last * int(get_page)

    if get_sort_by:
        if get_sort_by == 'title':
            sort_by = 'title'
        elif get_sort_by == 'year':
            sort_by = '-year'
        elif get_sort_by == 'rating':
            sort_by = '-rating'

    if get_order_by:
        if get_order_by == 'asc':
            if sort_by[0] != '-':
                tmp_sort_by = []
                tmp_sort_by.append('-')
                tmp_sort_by.append(sort_by)
                sort_by = ''.join(tmp_sort_by)
            else:
                sort_by = sort_by[1:]




    queryset = MovieList.objects.values().order_by(sort_by)[start:last]

    data = list(queryset)

    return JsonResponse(data, safe=False)