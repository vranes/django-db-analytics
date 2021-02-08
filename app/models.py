from django.db import models
from django.contrib.auth.models import User
from datetime import date

class User(models.Model):
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'users'

class Anime(models.Model):
    title = models.CharField(max_length=100)
    episodes = models.IntegerField(default=1)
    genre = models.CharField(max_length=100)

    class Meta:
        db_table = 'anime'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def date_as_string(self):
        return self.createdat.strftime('%Y-%m-%d')

    class Meta:
        db_table = 'reviews'