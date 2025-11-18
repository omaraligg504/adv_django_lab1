from django.http import JsonResponse
from .models import Movie
from django.shortcuts import render

def MovieList(request):
    movies = list(Movie.objects.values()) 
    return render(request, "movies/movies_list.html", {"movies": movies})

def MovieRatingsNPlus1(request):
    movies = Movie.objects.all()
    movie_data = []

    for movie in movies:
        ratings = [r.rating for r in movie.ratings.all()]  # <- use rating_set
        movie_data.append({
            "title": movie.title,
            "ratings": ratings
        })

    return render(request, "movies/movie_ratings.html", {"movies": movie_data})


def MovieRatingsOptimized(request):
    movies = Movie.objects.prefetch_related('ratings').all()

    movie_data = []
    for movie in movies:
        ratings = [r.rating for r in movie.ratings.all()]  # no extra query per movie
        movie_data.append({
            "title": movie.title,
            "ratings": ratings
        })

    return render(request, "movies/movie_ratings.html", {"movies": movie_data})


from ratings.models import Rating
from django.db.models import Avg, Count

def TopRatedMovies(request):
    movies = Movie.objects.annotate(avg_rating=Avg('ratings__rating')).order_by('-avg_rating')[:10]

    movie_data = []
    for movie in movies:
        movie_data.append({
            "title": movie.title,
            "avg_rating": movie.avg_rating,
        })

    return render(request, "movies/top_rated.html", {"movies": movie_data})


