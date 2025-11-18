from django.db import models

# Create your models here.
class Movie(models.Model):
    movieId=models.IntegerField(primary_key=True)
    title=models.CharField()
    genres=models.CharField()

