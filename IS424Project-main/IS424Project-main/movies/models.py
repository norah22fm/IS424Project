from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    release_year = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title
    def get_avg_rating(self):
        avg = self.rating_set.aggregate(models.Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0.0
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"