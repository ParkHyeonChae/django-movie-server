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
    # GET요청이 들어올 시 접근
    def get(self, request):
        # Parameter 초기값
        start = 0
        last = 20
        page = 1
        sort_by = 'id'
        genre = ''

        # GET요청으로 들어온 URL Parameter 저장
        get_limit = request.GET.get('limit', '')
        get_page = request.GET.get('page', '')
        get_sort_by = request.GET.get('sort_by', '')
        get_genre = request.GET.get('genre', '')
        get_order_by = request.GET.get('order_by', '')

        # limit Parameter
        if get_limit:
            if int(get_limit) >= 1 and int(get_limit) <= 50:
                last = int(get_limit)
            else:
                get_limit = 20
        else:
            get_limit = 20
            
        # page Parameter (페이지당 limit갯수를 반환하는 로직)
        if get_page:
            if int(get_page) >= 1 and int(get_page) * last <= 500:
                start = (last * int(get_page)) - last
                last = last * int(get_page)
            else:
                get_page = 1
        else:
            get_page = 1

        # sort_by Parameter
        if get_sort_by:
            if get_sort_by == 'title':
                sort_by = 'title'
            elif get_sort_by == 'year':
                sort_by = '-year'
            elif get_sort_by == 'rating':
                sort_by = '-rating'

        # genre Parameter
        if get_genre:
            genre = get_genre

        # order_by Parameter
        if get_order_by:
            if get_order_by == 'asc':
                if sort_by[0] != '-':
                    tmp_sort_by = []
                    tmp_sort_by.append('-')
                    tmp_sort_by.append(sort_by)
                    sort_by = ''.join(tmp_sort_by)
                else:
                    sort_by = sort_by[1:]

        # json Response에 출력될 movie 갯수
        movie_count = MovieList.objects.values().filter(genre__icontains=genre).order_by(sort_by).count()
        # json Response에 출력될 movie data
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
        # POST요청이 들어올 시 URL Parameter 저장
        post_title = request.GET.get("title")
        post_year = request.GET.get('year')
        post_rating = request.GET.get('rating')
        post_genres = request.GET.get('genres')
        post_summary = request.GET.get('summary')

        # 각 Parameter는 필수요소이므로 확인 후 DB에 저장
        if post_title and post_year and post_rating and post_genres and post_summary:
            MovieList.objects.create(title=post_title, year=post_year, rating=post_rating, genre=post_genres, summary=post_summary)

            return HttpResponse("Query was successful")
        else:
            return HttpResponse("Please enter all fields...")

    
def index(request):
    return render(request, 'api/index.html')