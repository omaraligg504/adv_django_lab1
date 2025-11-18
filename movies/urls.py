from .views import MovieList , MovieRatingsNPlus1 , MovieRatingsOptimized,TopRatedMovies
from django.urls import path

urlpatterns = [
    path('', MovieList, name='movie-list'),
    path('ratings-nplus1/', MovieRatingsNPlus1, name='movie-ratings-nplus1'),
     path('ratings-optimized/', MovieRatingsOptimized, name='ratings-optimized'),
     path('top-rated/', TopRatedMovies, name='top-rated-movies'),
]
