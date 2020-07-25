"""
DB Field : title, year, rating, genres, summary

# sort_by : String (title, year, rating, peers, seeds, download_count, like_count, date_added)
# order_by : String (desc, asc)
# limit : Integer between 1 - 50 (inclusive)
"""

from django.test import TestCase
import requests
import json


# TESTCASE 1 - 영화정보 다운로드순 10개
api_url = 'https://yts.mx/api/v2/list_movies.json?sort_by=download_count&limit=10'
data = requests.get(api_url)
json_data = json.loads(data.text)

for data in json_data['data']['movies']:
    print(
        '제목 : ', data['title'], type(data['title']),
        '\n년도 : ', data['year'], type(data['year']),
        '\n평점 : ', data['rating'], type(data['rating']),
        '\n장르 : ', data['genres'], type(data['genres']),
        '\n개요 : ', data['summary'], type(data['summary']), '\n\n'
    )