"""api/models.py"""

from django.db import models


class MovieList(models.Model):
    title = models.CharField(max_length=50, verbose_name="영화제목")
    year = models.PositiveIntegerField(verbose_name='개봉년도')
    rating = models.FloatField(verbose_name='영화평점')
    genres = models.CharField(max_length=128, verbose_name='영화장르')
    summary = models.TextField(verbose_name='영화개요')

    class Meta:
        db_table = '영화리스트'
        verbose_name = '영화리스트'
        verbose_name_plural = '영화리스트'