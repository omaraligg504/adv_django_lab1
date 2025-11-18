from django.db import models
# Create your models here.
class Rating(models.Model):
    userId = models.IntegerField(null=False)
    movieId = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='ratings')
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    timestamp = models.BigIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['userId', 'movieId'], name='unique_rating')
        ]
