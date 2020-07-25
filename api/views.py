"""api/views.py"""
# API Request : /api?limit={parameter}
# API Request : /api?page={parameter}
# API Request : /api?sort_by={parameter}
# API Request : /api?genre={parameter}
# API Request : /api?order_by={parameter}

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import MovieList
from django.views import View


class MovieListApi(View):
    def get(self, request):
        start = 0
        last = 20
        page = 1
        sort_by = 'id'
        genre = ''

        get_limit = request.GET.get('limit', '')
        get_page = request.GET.get('page', '')
        get_sort_by = request.GET.get('sort_by', '')
        get_genre = request.GET.get('genre', '')
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


    # postman 사용 POST 요청시 header에 X-CSRFToken : zbJi6TjifNkMPWXFalus0YXNquCqwQkeNz7g3Oy8XIm9LDpF0MB8lUg71EKJLG9J 추가
    def post(self, request):
        post_title = request.GET.get("title")
        post_year = request.GET.get('year')
        post_rating = request.GET.get('rating')
        post_genres = request.GET.get('genres')
        post_summary = request.GET.get('summary')

        if post_title and post_year and post_rating and post_genres and post_summary:
            MovieList.objects.create(title=post_title, year=post_year, rating=post_rating, genre=post_genres, summary=post_summary)
            
            return HttpResponse("Query was successful")
        else:
            return HttpResponse("Please enter all fields...")