from django.db import models

# Create your models here.
class Tag(models.Model):
    userId = models.IntegerField(null=False)
    movieId = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='tags')
    tag = models.CharField(max_length=255)
    timestamp = models.BigIntegerField()
