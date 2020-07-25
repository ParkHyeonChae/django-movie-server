"""api/test.py

DB Field : title, year, rating, genre, summary

# sort_by : String (title, year, rating, peers, seeds, download_count, like_count, date_added)
# order_by : String (desc, asc)
# limit : Integer between 1 - 50 (inclusive)
"""

from django.test import TestCase
import requests
import json
from .models import MovieList


# TESTCASE 1 - 영화정보 다운로드순 10개
api_url = 'https://yts.mx/api/v2/list_movies.json?sort_by=download_count&limit=10'
data = requests.get(api_url)
json_data = json.loads(data.text)

for data in json_data['data']['movies']:
    print(
        '제목 : ', data['title'], type(data['title']),
        '\n년도 : ', data['year'], type(data['year']),
        '\n평점 : ', data['rating'], type(data['rating']),
        '\n장르 : ', data['genre'], type(data['genre']),
        '\n개요 : ', data['summary'], type(data['summary']), '\n\n'
    )


# TESTCASE 2 - 영화정보 DB 입력
# MovieList.objects.create(title="test", year=2020, rating=1.1, genre=['1','2'], summary="test")
# print(MovieList.objects.all())



# TESTCASE 3 - 영화정보 DB 조회
queryset = MovieList.objects.all()
queryset = queryset.filter(genres__icontains='1')

for model_instance in queryset:
    print(model_instance)